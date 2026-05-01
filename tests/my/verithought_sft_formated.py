import json
import re

json_path = "/root/autodl-tmp/ChipSeek-R1/data/lf_complete_trainset_reasoning.jsonl"
with open(json_path, "r") as json_file:
    dataset = json.load(json_file)
    new_dataset = []
    for data in dataset:
        new_instruction = re.sub(r"CODE BEGIN", "<answer>", data["instruction"])
        new_instruction = re.sub(r"CODE END", "</answer>", new_instruction)
        new_output = re.sub(r"CODE BEGIN", "<answer>", data["output"])
        new_output = re.sub(r"CODE END", "</answer>", new_output)
        new_output = re.sub(r"</think>\n<answer>", "</think>\n\n<answer>", new_output)
        new_dataset.append({"instruction": new_instruction, "input": data["input"], "output": new_output})
        
new_json_path = "/root/autodl-tmp/ChipSeek-R1/data/new_lf_complete_trainset_reasoning.json"
with open(new_json_path, "w") as new_json_file:
    json.dump(new_dataset, new_json_file, indent = 4)