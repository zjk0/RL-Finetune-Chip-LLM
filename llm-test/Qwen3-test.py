from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "./llm-models/Qwen3-0.6B"

# load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name, 
    torch_dtype = "auto", 
    device_map = "auto"
)

# prepare the model input
prompt = "如果我发烧了，我可以吃点什么药？"
messages = [
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages, 
    tokenize = False, 
    add_generation_prompt = True, 
    enable_thinking = True
)
model_inputs = tokenizer([text], return_tensors = "pt").to(model.device)

# conduct text completion
generated_ids = model.generate(
    **model_inputs, 
    max_new_tokens = 32768
)
output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()

# parsing thinking content
try:
    index = len(output_ids) - output_ids[::-1].index(151668)
except ValueError:
    index = 0
    
thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens = True).strip("\n")
content = tokenizer.decode(output_ids[index:], skip_special_tokens = True).strip("\n")

print("thinking context: \n", thinking_content)
print("\ncontent: \n", content)