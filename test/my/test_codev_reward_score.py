import pickle
from verl.utils.reward_score.codev import compute_score

if __name__ == '__main__':
    file = "/home/kai/none/ChipLLM/datasets/zhuyaoyu-CodeV-R1-dataset/snapshots/688a48d6308414b9d8bceed27a9c08ee36a4fa6b/codev_r1_rl_train.parquet"
    import pyarrow.parquet as pq
    data = pq.read_table(file).to_pylist()
    
    sep = "============================================"
    print(data[0].keys())
    # correct
    gt = data[0]['reward_model']['ground_truth']
    example_ans = pickle.loads(gt)['answer']['code']
    example_output = f"<think></think>  <answer>\n```verilog\n{example_ans}```\n</answer>"
    reward = compute_score(example_output, gt)
    print(f"{sep}\n{example_output}\n{sep}\n{reward}")

    # wrong format
    example_output = f"<think> <answer></think> ```verilog\n{example_ans}```</answer>"
    reward = compute_score(example_output, gt)
    print(f"{sep}\n{example_output}\n{sep}\n{reward}")

    # wrong answer
    example_output = f"<think> </think> <answer>\n```verilog\n```\n</answer>"
    reward = compute_score(example_output, gt)
    print(f"{sep}\n{example_output}\n{sep}\n{reward}")