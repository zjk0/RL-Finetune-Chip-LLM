from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("yang-z/CodeV-DS-6.7B")
model = AutoModelForCausalLM.from_pretrained("yang-z/CodeV-DS-6.7B")