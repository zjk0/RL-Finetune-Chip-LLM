from peft import LoraConfig, TaskType
import peft
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import Trainer, TrainingArguments
import datasets
import json
import os
from datetime import datetime

def to_json(datas, path):
    with open(path, "w", encoding = "utf-8") as fp:
        for data in datas:
            data["input"] = data["instruction"]
            del data["instruction"]
            json.dump(data, fp, ensure_ascii = False)
            fp.write("\n")

def preprocess_dataset(dataset, dataset_dir):
    dataset_list = list(dataset["train"])
    dataset_len = len(dataset_list)
    train_data_len = int(0.9 * dataset_len)
    train_dataset_list = dataset_list[0: train_data_len]
    test_dataset_list = dataset_list[train_data_len: dataset_len]
    
    os.makedirs(dataset_dir, exist_ok = True)
    train_dataset_path = os.path.join(dataset_dir, "train_data.json")
    test_dataset_path = os.path.join(dataset_dir, "test_data.json")
    
    to_json(train_dataset_list, train_dataset_path)
    to_json(test_dataset_list, test_dataset_path)
    
    new_dataset = datasets.load_dataset(dataset_dir)
    return new_dataset

def tokenized_func(data):
    input_ids, attention_mask, labels = [], [], []
    batch_size = len(data["input"])
    
    for i in range(batch_size):
        message = f"{data["input"][i]}\n\n{data["output"][i]}"
        message_tokens = tokenizer(message, padding = "max_length", truncation = True, max_length = 1024)
        
        input_ids.append(message_tokens["input_ids"])
        attention_mask.append(message_tokens["attention_mask"])
        
        prefix_tokens = tokenizer(f"{data["input"][i]}\n\n")
        label = message_tokens["input_ids"].copy()
        label[0: len(prefix_tokens)] = [-100] * len(prefix_tokens)
        labels.append(label)
        
    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}

model_path = "./llm-models/Qwen3-0.6B"
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

dataset_path = "./datasets/KSU-HW-SEC-verilog-code"
dataset = datasets.load_dataset(dataset_path)
dataset_dir = "./chip-llm/finetune/Qwen3-0.6B-verilog-lora-sft/dataset"
dataset = preprocess_dataset(dataset, dataset_dir)
# print(dataset)
tokenized_dataset = dataset.map(tokenized_func, batched = True, batch_size = 32)
dataset.cleanup_cache_files()

lora_config = LoraConfig(
    task_type = TaskType.CAUSAL_LM, 
    inference_mode = False, 
    r = 8, 
    lora_alpha = 32, 
    lora_dropout = 0.1
)
model = peft.get_peft_model(model, lora_config)
# model.print_trainable_parameters()

time = datetime.now()
time_str = time.strftime("%Y-%m%d-%H_%M_%S")

training_args = TrainingArguments(
    output_dir = "./chip-llm/finetune/Qwen3-0.6B-verilog-lora-sft/output", 
    eval_strategy = "steps", 
    eval_steps = 100, 
    num_train_epochs = 5, 
    save_steps = 400, 
    logging_steps = 10, 
    learning_rate = 1e-4, 
    gradient_accumulation_steps = 16, 
    per_device_train_batch_size = 2, 
    per_device_eval_batch_size = 2, 
    save_total_limit = 1, 
    run_name = f"Qwen3-0.6B-verilog-lora-sft-{time_str}"
)

trainer = Trainer(
    model = model, 
    train_dataset = tokenized_dataset["train"], 
    eval_dataset = tokenized_dataset["test"], 
    args = training_args
)

trainer.train()