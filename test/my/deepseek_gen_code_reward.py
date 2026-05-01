from openai import OpenAI
import os
import pyarrow.parquet as pq
import re
import pickle
from verl.utils.reward_score.codev import compute_score
from verl.utils.reward_score.codev_eval_toolkit.eval_codev import verify_one_sample, verify_one_sample_wrapper
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_verilog(completion: str) -> str:
    pattern = re.compile(r"```verilog\n(.*?)```", re.DOTALL)
    matches = pattern.findall(completion)
    extracted_answer = matches[-1] if len(matches) >= 1 else ""
    return extracted_answer

path = "/home/kai/none/ChipLLM/datasets/zhuyaoyu-CodeV-R1-dataset/snapshots/688a48d6308414b9d8bceed27a9c08ee36a4fa6b/codev_r1_rl_train.parquet"
dataset = pq.read_table(path).to_pylist()

index = 56
prompt = dataset[index]["question"][1]["content"]
ground_truth = dataset[index]['reward_model']['ground_truth']
ground_truth = pickle.loads(ground_truth)
ground_truth = ground_truth['answer']

os.environ["all_proxy"] = "http://127.0.0.1:7897/"

verilog_code_list = []
for _ in tqdm(range(12)):
    # for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
    client = OpenAI(api_key="sk-5b13a90466bf48c9af7f477a4d6bac8e", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": f"{prompt}\n\nJust give me the code within ````verilog\n...\n``` without any explanation."},
        ],
        max_tokens=25600,
        temperature=0.7,
        stream=False,
        extra_body={"thinking": {"type": "enabled"}}
    )

    verilog_code = extract_verilog(response.choices[0].message.content)
    if verilog_code != "":
        print("Extracted verilog code successfully.")
    verilog_code_list.append(verilog_code)
    
print("Get verilog code")
rewards = []
start = time.perf_counter()
for verilog_code in verilog_code_list:
    result = verify_one_sample(ground_truth, verilog_code)
    if result["correct"] == "True":
        reward = 1.0
    elif result["correct"] == "Partially True":
        reward = 0.4
    else:
        reward = 0.0
    rewards.append(reward)
cost_time = time.perf_counter() - start
print(f"Time: {cost_time}")
print(f"Rewards: {rewards}")

rewards_with_thread = [0.0] * len(verilog_code_list)
start = time.perf_counter()
with ThreadPoolExecutor(max_workers = 6) as executor:
    futures = {executor.submit(verify_one_sample, ground_truth, verilog_code): i for i, verilog_code in enumerate(verilog_code_list)}
    for future in as_completed(futures):
        i = futures[future]
        result = future.result()
        if result["correct"] == "True":
            reward = 1.0
        elif result["correct"] == "Partially True":
            reward = 0.4
        else:
            reward = 0.0
        rewards_with_thread[i] = reward

cost_time = time.perf_counter() - start
print(f"Time with thread: {cost_time}")
print(f"Rewards with thread: {rewards_with_thread}")
