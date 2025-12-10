from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "./chip-llm/finetune/Qwen3-0.6B-verilog-lora-sft/output/checkpoint-3545"
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer_path = "./llm-models/Qwen3-0.6B"
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

prompt =  """
Please act as a professional verilog designer and implement the module.
(1) Module name: matrix_mult_4x4

(2) Input port and its function:
   - clk: Clock signal used for synchronous operations.
   - reset_n: Active low asynchronous reset signal.
   - a: First 4x4 matrix input.
   - b: Second 4x4 matrix input.

(3) Output port and its function:
   - c: 4x4 matrix output, the result of a * b.

(4) Description of the implementation process:
   - Design a 4*4 matrix multiplier with an area less than 500 μm².
   - Use pipelined or time-multiplexed architecture if needed to reduce area.
   - ...
"""
text = f"input:\n{prompt}\n\noutput:\n"
input = tokenizer(text, return_tensors = "pt").to(model.device)

output = model.generate(**input, max_new_tokens = 32768)
output_ids = output[0].tolist()
output_content = tokenizer.decode(output_ids, skip_special_tokens = True).strip("\n")
print(output_content)