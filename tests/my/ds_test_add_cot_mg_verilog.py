from datasets import load_dataset
import json
import re
from tqdm import tqdm
from transformers import pipeline
import os

def find_module_name(text: str):
    bound_1 = "Module header:"
    bound_2_list = [" #", "#", " \(", "\(", ";"]
    next_bound_1 = "module "
    next_bound_2 = " endmodule"
    
    for bound_2 in bound_2_list:
        pattern = re.compile(rf"{bound_1}\n\n(.*?){bound_2}", re.DOTALL)
        matches = pattern.findall(text)
        temp = matches[-1] if len(matches) >= 1 else ""
        temp = temp + " endmodule"
        pattern = re.compile(rf"{next_bound_1}(.*?){next_bound_2}", re.DOTALL)
        matches = pattern.findall(temp)
        module_name = matches[-1] if len(matches) >= 1 else ""
        if module_name != "":
            break
    
    return module_name
    
def find_module_header(text: str):
    bound_1 = "Module header:"
    bound_2 = ";"
    pattern = re.compile(rf"{bound_1}\n\n(.*?){bound_2}", re.DOTALL)
    matches = pattern.findall(text)
    module_header = matches[-1] if len(matches) >= 1 else ""
    module_header = module_header + ";"
    return module_header
    
def find_description(text: str, is_block_level: bool):
    if is_block_level:
        bound_1 = "Here are block level summaries:"
    else:
        bound_1 = "Implement the Verilog module based on the following description. Assume that signals are positive clock/clk edge triggered unless otherwise stated."
    bound_2 = " Module header:"
    pattern = re.compile(rf"{bound_1}\n\n(.*?)\n\n{bound_2}", re.DOTALL)
    matches = pattern.findall(text)
    description = matches[-1] if len(matches) >= 1 else ""
    return description

dataset = load_dataset("/root/autodl-tmp/ChipLLM/datasets/mg-verilog", data_files = "/root/autodl-tmp/ChipLLM/datasets/mg-verilog/data-00000-of-00001.arrow")
data = dataset["train"][100]
module_name = find_module_name(data["description"]["detailed_global_summary"])
block_description = find_description(data["description"]["block_summary"], is_block_level = True)
high_level_description = find_description(data["description"]["high_level_global_summary"], is_block_level = False)
detailed_description = find_description(data["description"]["detailed_global_summary"], is_block_level = False)
instruction = (
    f"Module name: {module_name}\n\n"
    "<Block description>\n\n"
    f"{block_description}\n"
    "<High level description>\n\n"
    f"{high_level_description}\n\n"
    "<Detailed description>\n\n"
    f"{detailed_description}\n\n"
)

module_header = find_module_header(data["description"]["detailed_global_summary"])
module_code = data["code"]
code = f"{module_header}{module_code}"

print(f"{code}\n")

# prompt = f"""
# You are a hardware design expert. Given the following code description and corresponding Verilog code, provide the reasoning content explaining how you would approach solving the task of generating Verilog code based on the description. Make sure your reasoning process is clear, coherent and concise.
# - Code Description: {instruction}
# - Verilog Code: {code}
# """

prompt = f"""
Task Description:
Below is the implementation of a Verilog module. Based on this implementation, generate a detailed reasoning chain that explains how the Verilog code is derived from the task description. Focus on providing a clear, concise, and logically connected explanation for each design decision step by step.

Verilog Implementation:
{code}

Natural Language Description:
{instruction}

Please provide a response that includes the reasoning chain, explaining the design process step by step in a concise and coherent manner, and also include the generated Verilog code.
"""

def find_answer(text: str):
    pattern = re.compile(r'"content":"(.*?)","reasoning_content"', re.DOTALL)
    matches = pattern.findall(text)
    answer = matches[-1] if len(matches) >= 1 else ""
    return answer

import requests

def DeepSeek(prompt):
    url = "https://api.deepseek.com/chat/completions"

    payload = json.dumps({
        "messages": [
            {
                "content": "You are a helpful assistant",
                "role": "system"
            },
            {
                "content": prompt,
                "role": "user"
            }
        ],
        "model": "deepseek-reasoner",
        "thinking": {
            "type": "enabled"
        },
        "frequency_penalty": 0,
        "max_tokens": 4096,
        "presence_penalty": 0,
        "response_format": {
            "type": "text"
        },
        "stop": None,
        "stream": False,
        "stream_options": None,
        "temperature": 1,
        "top_p": 1,
        "tools": None,
        "tool_choice": "none",
        "logprobs": False,
        "top_logprobs": None
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {os.getenv("DEEPSEEK_API_KEY")}'
    }

    success = False
    while not success:
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            # print(type(response))
            answer = find_answer(response.text)
            # print(len(answer))
            print(response.text)
            print(answer)
            if len(answer) > 0:
                success = True
        except Exception as e:
            print(e)
            pass 

    return answer

# url = "https://api.deepseek.com/chat/completions"

# payload = json.dumps({
#   "messages": [
#     {
#       "content": "You are a helpful assistant",
#       "role": "system"
#     },
#     {
#       "content": prompt,
#       "role": "user"
#     }
#   ],
#   "model": "deepseek-reasoner",
#   "thinking": {
#     "type": "enabled"
#   },
#   "frequency_penalty": 0,
#   "max_tokens": 4096,
#   "presence_penalty": 0,
#   "response_format": {
#     "type": "text"
#   },
#   "stop": None,
#   "stream": False,
#   "stream_options": None,
#   "temperature": 1,
#   "top_p": 1,
#   "tools": None,
#   "tool_choice": "none",
#   "logprobs": False,
#   "top_logprobs": None
# })
# headers = {
#   'Content-Type': 'application/json',
#   'Accept': 'application/json',
#   'Authorization': f'Bearer {os.getenv("DEEPSEEK_API_KEY")}'
# }

# response = requests.request("POST", url, headers=headers, data=payload)

# print(type(response.text))


response = DeepSeek(prompt)
