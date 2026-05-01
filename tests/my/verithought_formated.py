import json
from transformers import AutoTokenizer
from tqdm import tqdm

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
json_path = "/root/autodl-tmp/ChipSeek-R1/data/hf_complete_trainset.jsonl"
dataset = []

with open(json_path, "r") as json_file:
    for line in tqdm(json_file):
        data = json.loads(line.strip())
        question = data["question"]
        instruction = f"{question}\nPlease start your Verilog code with <answer> and end with </answer>."
        input = ""
        thinking_process = data["reasoning_trace"]
        code = data["ground_truth"]
        output = f"<think>\n{thinking_process}\n</think>\n\n<answer>\n{code}\n</answer>"
        
        message = [
            {"role": "user", "content": instruction},
        ]
        inputs = tokenizer.apply_chat_template(
            message, 
            add_generation_prompt = True,
            tokenize = False
        )
        # print(inputs)
        sft_inputs = f"{inputs}{output}"
        sft_inputs_tokens = tokenizer(sft_inputs)
        
        tokens_len = len(sft_inputs_tokens["input_ids"])
        print(f"tokens_len: {tokens_len}")
        if not tokens_len > 32768:
            print("----------------------- OK -----------------------")
            dataset.append({"instruction": instruction, "input": input, "output": output})

new_json_path = "/root/autodl-tmp/ChipSeek-R1/data/veri_thought.json"
with open(new_json_path, "w") as new_json_file:
    json.dump(dataset, new_json_file, indent = 4)