import pyarrow.parquet as pq
import pyarrow as pa

# path = "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_rl_train.parquet"
# dataset = pq.read_table(path).to_pylist()

# for data in dataset:
#     data["problem"] = data["question"][1]["content"]
#     data.pop("question")

# table = pa.Table.from_pylist(dataset)
# pq.write_table(table, "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_rl/codev_r1_rl.parquet")

path = "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_rl/codev_r1_rl_1.parquet"
path_ppa = "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_rl_ppa/codev_r1_rl_ppa_1.parquet"
dataset = pq.read_table(path).to_pylist()
dataset_ppa = pq.read_table(path_ppa).to_pylist()

print(dataset[0]["problem"])
print(dataset_ppa[0]["problem"])

# print(len(dataset))
# print(dataset[0].keys())
# dataset_cut = dataset[0: 100]
# table = pa.Table.from_pylist(dataset_cut)
# pq.write_table(table, "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_rl_100/codev_r1_rl_100.parquet")
# new_dataset = []
# new_dataset_ppa = []
# for data in dataset:
#     data["problem"] = data["question"][1]["content"]
#     new_dataset.append(data)
# for data_ppa in dataset_ppa:
#     data_ppa["problem"] = data_ppa["question"][1]["content"]
#     new_dataset_ppa.append(data_ppa)
    
# table = pa.Table.from_pylist(new_dataset)
# pq.write_table(table, "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_rl/codev_r1_rl_1.parquet")
# table = pa.Table.from_pylist(new_dataset_ppa)
# pq.write_table(table, "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_rl_ppa/codev_r1_rl_ppa_1.parquet")