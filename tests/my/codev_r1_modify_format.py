import json
import re
from tqdm import tqdm
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
system = """You are a helpful assistant. The assistant first thinks about the reasoning process in the mind and then provides the user with the answer. The reasoning process and answer are enclosed within <think> </think> and <answer> </answer> tags, respectively, i.e., <think>
reasoning process here
</think>
<answer>
answer here
</answer>. \u00a0Now the user asks you to write verilog code. After thinking, when you finally reach a conclusion, enclose the final verilog code in ```verilog ``` within <answer> </answer> tags. i.e., <answer>
```verilog
module top_module(in, out, ...) ...
```
</answer>""" 

dataset_path = "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_sft.jsonl"
new_dataset_list = []
with open(dataset_path, "r") as dataset:
    for data in tqdm(dataset):
        data = json.loads(data.strip())
        instruction = data["prompt"]
        output = data["response"]
        output = re.sub(r"<think>", r"<think>\n", output)
        # output = re.sub(r"```verilog\n", "", output)
        # output = re.sub(r"```\n", "", output)
        
        message = [
            {"role": "system", "content": system},
            {"role": "user", "content": instruction},
        ]
        inputs = tokenizer.apply_chat_template(
            message, 
            add_generation_prompt = True,
            tokenize = False
        )
        sft_inputs = f"{inputs}{output}"
        sft_inputs_tokens = tokenizer(sft_inputs)
        tokens_len = len(sft_inputs_tokens["input_ids"])
        if not tokens_len > 32768:
            new_dataset_list.append({"instruction": instruction, "input": "", "output": output, "system": system})
        else:
            print("\nLonger than max sequence length\n")
        
new_dataset_path = "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_sft_formated.json"
with open(new_dataset_path, "w") as file:
    json.dump(new_dataset_list, file, indent = 4)