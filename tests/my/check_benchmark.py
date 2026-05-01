import json

path = "/root/autodl-tmp/ChipSeek-R1/benchmark_codev/verilog_eval_v2.json"
with open(path, "r") as f:
    rtllm_v2 = json.load(f)

count = 0
for data in rtllm_v2:
    if data["ppa"]["power"] * data["ppa"]["performance"] * data["ppa"]["area"] <= 0:
        # print(data["top_module"])
        count += 1
        
print(count)