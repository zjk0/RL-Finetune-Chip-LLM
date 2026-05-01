import pickle
from verl.utils.reward_score.codev_eval_toolkit.verify import eda_tools
import pyarrow.parquet as pq

file = "/home/kai/none/ChipLLM/datasets/zhuyaoyu-CodeV-R1-dataset/snapshots/688a48d6308414b9d8bceed27a9c08ee36a4fa6b/codev_r1_rl_train.parquet"
dataset = pq.read_table(file).to_pylist()

gt = dataset[0]['reward_model']['ground_truth']  # 字节流
example_ans = pickle.loads(gt)['answer']['code']  # 代码

tool = eda_tools(quiet = True)
testbench_code = tool.generate_testbench(example_ans)
print(testbench_code)