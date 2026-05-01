import json
import re
import pyarrow.parquet as pq

path = "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_rl/codev_r1_rl.parquet"
# path = "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_rl_ppa/codev_r1_rl_ppa.parquet"
# path = "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_rl_train.parquet"
dataset = pq.read_table(path).to_pylist()

print(len(dataset))
print(dataset[9].keys())
# print(dataset[10]["question"][1]["content"])
# print(dataset[9]["ground_truth"][0]["content"])

# dataset_path = "/root/autodl-tmp/ChipSeek-R1/data/Veribench-100/Veribench-100.json"
# with open(dataset_path, "r") as f:
#     dataset = json.load(f)
    
# print(dataset[5]["problem"])
    
# for i in range(len(dataset)):
#     problem = dataset[i]["problem"]
#     dataset[i]["problem"] = f'''{problem}
    
# Return the result in exactly the following format:
# <think>
# Your thinking process here.
# </think>
# <answer>
# ```verilog
# Your verilog code here.
# ```
# </answer>
# '''

# with open(dataset_path, "w") as f:
#     json.dump(dataset, f, indent=4)
    