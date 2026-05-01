import json

path = "/home/kai/none/CodeV-R1/test/testbench/VerilogEval_v2.0.0/verilog_eval_v2.json"
with open(path, "r") as f:
    benchmark = json.load(f)

count = 0
for data in benchmark:
    if data["ppa"]["power"] * data["ppa"]["performance"] * data["ppa"]["area"] <= 0:
        # print(data["top_module"])
        count += 1
        
print(count)