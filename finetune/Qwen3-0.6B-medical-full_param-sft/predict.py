from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "./chip-llm/finetune/Qwen3-0.6B-medical-full_param-sft/output/checkpoint-1122"
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer_path = "./llm-models/Qwen3-0.6B"
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

prompt = "如果我发烧了，我可以吃点什么药？"
message = [
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    message, 
    tokenize = False, 
    add_generation_prompt = True, 
    enable_thinking = True
)
input = tokenizer([text], return_tensors = "pt").to(model.device)

output = model.generate(**input, max_new_tokens = 32768)
output_ids = output[0].tolist()
output_content = tokenizer.decode(output_ids, skip_special_tokens = True).strip("\n")
print(output_content)