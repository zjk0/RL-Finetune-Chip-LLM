from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import Trainer, TrainingArguments
import datasets
import numpy as np
import evaluate
import json
import wandb
import os
from datetime import datetime

import torch
from transformers.trainer_utils import has_length
from transformers.trainer_pt_utils import LengthGroupedSampler
# from transformers.trainer_utils import is_datasets_available
from transformers.utils import is_datasets_available
from torch.utils.data import RandomSampler
from typing import Optional
from torch.utils.data import Dataset

def dataset_to_json(dataset, dataset_path):
    with open(dataset_path, "w", encoding = "utf-8") as fp:
        for data in dataset:
            del data["instruction"]
            del data["metrics"]
            json.dump(data, fp, ensure_ascii = False)
            fp.write("\n")

def preprocess_dataset(dataset, dataset_dir):
    dataset_list = list(dataset["train"])
    dataset_len = len(dataset_list)
    train_data_len = int(dataset_len * 0.9)
    train_data_list = dataset_list[0: train_data_len]
    test_data_list = dataset_list[train_data_len: dataset_len]
    
    os.makedirs(dataset_dir, exist_ok = True)
    train_dataset_path = os.path.join(dataset_dir, "train_data.jsonl")
    test_dataset_path = os.path.join(dataset_dir, "test_data.jsonl")
    
    dataset_to_json(train_data_list, train_dataset_path)
    dataset_to_json(test_data_list, test_dataset_path)
    
    new_dataset = datasets.load_dataset(dataset_dir)
    return new_dataset

def tokenize_func(data):
    input_ids, attention_mask, labels = [], [], []
    batch_size = len(data["question"])
    
    for i in range(batch_size):
        message = f"{data["question"][i]}\n\n<think>\n{data["think"][i]}\n</think>\n\n{data["answer"][i]}"
        message_tokens = tokenizer(message, padding = "max_length", truncation = True, max_length = 512)
        
        input_ids.append(message_tokens["input_ids"])
        attention_mask.append(message_tokens["attention_mask"])
        
        question_tokens = tokenizer(f"{data["question"][i]}\n\n")
        label = message_tokens["input_ids"].copy()
        label[0: len(question_tokens)] = [-100] * len(question_tokens)
        labels.append(label)
    
    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}

model_path = "./llm-models/Qwen3-0.6B"
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

dataset_path = "./datasets/krisfu-delicate-medical-data"
dataset = datasets.load_dataset(dataset_path)
# print(dataset)
dataset_dir = "./chip-llm/finetune/Qwen3-0.6B-medical-full_param-sft/dataset"
dataset = preprocess_dataset(dataset, dataset_dir)

# print(dataset)

tokenized_dataset = dataset.map(tokenize_func, batched = True, batch_size = 32)
dataset.cleanup_cache_files()
# print(tokenized_dataset)

time = datetime.now()
time_str = time.strftime("%Y-%m%d-%H_%M_%S")

training_args = TrainingArguments(
    output_dir = "./chip-llm/finetune/Qwen3-0.6B-medical-full_param-sft/output", 
    eval_strategy = "steps", 
    eval_steps = 100, 
    num_train_epochs = 5, 
    save_steps = 400, 
    logging_steps = 10, 
    learning_rate = 1e-4, 
    gradient_checkpointing = True, 
    gradient_accumulation_steps = 4, 
    per_device_train_batch_size = 1, 
    per_device_eval_batch_size = 1, 
    save_total_limit = 1, 
    run_name = f"Qwen3-0.6B-medical-full_param-sft-{time_str}"
)

class myTrainer(Trainer):
    def _get_train_sampler(self, train_dataset: Optional[Dataset] = None) -> Optional[torch.utils.data.Sampler]:
        if train_dataset is None:
            train_dataset = self.train_dataset
        if train_dataset is None or not has_length(train_dataset):
            return None

        # Build the sampler.
        if self.args.group_by_length:
            if is_datasets_available() and isinstance(train_dataset, datasets.Dataset):
                lengths = (
                    train_dataset[self.args.length_column_name]
                    if self.args.length_column_name in train_dataset.column_names
                    else None
                )
            else:
                lengths = None
            model_input_name = (
                self.processing_class.model_input_names[0] if self.processing_class is not None else None
            )
            return LengthGroupedSampler(
                self.args.train_batch_size * self.args.gradient_accumulation_steps,
                dataset=train_dataset,
                lengths=lengths,
                model_input_name=model_input_name,
            )

        else:
            return RandomSampler(train_dataset, replacement = True)

trainer = myTrainer(
    model = model, 
    train_dataset = tokenized_dataset["train"], 
    eval_dataset = tokenized_dataset["test"], 
    args = training_args
)

# train_loader = trainer.get_train_dataloader()
# print(train_loader.sampler)
# # print(getattr(train_loader, "replacement"))
# train_sampler = trainer._get_train_sampler()
# print(train_sampler)
# print(getattr(train_sampler, "replacement"))

trainer.train()