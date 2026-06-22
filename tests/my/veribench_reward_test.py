import json
from openai import OpenAI
import re
import subprocess
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def extract_verilog(completion: str) -> str:
    pattern = re.compile(r"```verilog\n(.*?)\n```", re.DOTALL)
    matches = pattern.findall(completion)
    extracted_answer = matches[-1] if len(matches) >= 1 else ""
    return extracted_answer
    
def run_iverilog(testbench_path: str, verilog_code_path: str):
    result = subprocess.run(
        ["iverilog", "-o", f"{os.path.dirname(verilog_code_path)}/simulation.out", verilog_code_path, testbench_path],
        capture_output = True,
        text = True,
        timeout = 10
    )
    if result.returncode != 0:
        result = subprocess.run(
            ['iverilog', '-Wall', '-Winfloop', '-Wno-timescale', '-g2012', '-o', f"{os.path.dirname(verilog_code_path)}/simulation.out", verilog_code_path, testbench_path],
            capture_output = True,
            text = True,
            timeout = 10
        )
    
    if result.returncode == 0:
        result = subprocess.run(
            ["vvp", f"{os.path.dirname(verilog_code_path)}/simulation.out"],
            capture_output = True,
            text = True,
            timeout = 30
        )
        if result.returncode == 0:
            return f"Simulation output:\n{result.stdout}"
        else:
            return f"Simulation failed with error:\n{result.stderr}"
    else:
        return f"Compilation failed with error:\n{result.stderr}"
        
def calc_reward(testbench, verilog_code_list):
    verilog_code_path = "/root/autodl-tmp/ChipSeek-R1/iverilog_test/verilog_code.v"
    testbench_path = "/root/autodl-tmp/ChipSeek-R1/iverilog_test/testbench.v"
    
    with open(testbench_path, "w") as f:
        f.write(testbench)
        
    with ThreadPoolExecutor() as executor:
        futures = []
        for verilog_code in verilog_code_list:
            with open(verilog_code_path, "w") as f:
                f.write(verilog_code)
            future = executor.submit(run_iverilog, testbench_path, verilog_code_path)
            futures.append(future)
            
        rewards = []
        i = 1
        for future in futures:
            iverilog_result = future.result()
            print(f"Result for Verilog code {i}:\n{iverilog_result}\n")
            if "Simulation output:" not in iverilog_result:
                reward = 0.0
            else:
                if "failed" in iverilog_result:
                    reward = 0.0
                else:
                    reward = 1.0
            rewards.append(reward)
            i += 1
            
    return rewards

if __name__ == "__main__":
    path = "/root/autodl-tmp/ChipSeek-R1/data/Veribench-53K.json"
    with open(path, "r") as f:
        data_list = json.load(f)

    index = 1
    question = data_list[index]["question"]
    testbench = data_list[index]["testbench"]

    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

    verilog_code_list = []
    for _ in tqdm(range(2)):
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": f"{question}\n\nJust give me the code within ````verilog\n...\n``` without any explanation."},
            ],
            max_tokens=12800,
            temperature=0.7,
            stream=False,
            extra_body={"thinking": {"type": "enabled"}}
        )

        verilog_code = extract_verilog(response.choices[0].message.content)
        verilog_code_list.append(verilog_code)
        
    print("Reward:", calc_reward(testbench, verilog_code_list))