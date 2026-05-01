import json

path = "/root/autodl-tmp/ChipSeek-R1/data/Veribench-53K/Veribench-53K.json"

with open(path, "r") as f:
    veribench = json.load(f)

print(veribench[0].get("problem"))

# for data in veribench:
#     data["problem"] = data.pop("question")

# path = "/root/autodl-tmp/ChipSeek-R1/data/Veribench/Veribench-53K-1.json"
# with open(path, "w") as f:
#     json.dump(veribench, f, indent=4)