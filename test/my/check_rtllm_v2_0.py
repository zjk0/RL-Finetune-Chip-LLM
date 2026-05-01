import json

path = "/home/kai/none/CodeV-R1/test/testbench/RTLLM_v2.0_full/rtllm_v2_0.json"
with open(path, "r") as f:
    rtllm_v2 = json.load(f)

count = 0
for data in rtllm_v2:
    if data["ppa"]["power"] * data["ppa"]["performance"] * data["ppa"]["area"] <= 0:
        print(data["top_module"])
        count += 1
        
print(count)