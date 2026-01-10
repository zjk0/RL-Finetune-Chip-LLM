import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set GPU device
os.environ["CUDA_VISIBLE_DEVICES"] = "7"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_name = "/public/Qwen2.5-7B-Verilog-GRPO-ppa/best_model"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)


prompt = '''Please act as a professional verilog designer.

Implement a simplified radix-2 divider on 8-bit signed or unsigned integers. and the inputs are two 8-bit operands. The module accepts a dividend and a divisor as inputs and provides a 16-bit result containing both the quotient and the remainder. The design supports both signed and unsigned division operations.

Module name:  
    radix2_div 

Input ports:
    clk: Clock signal used for synchronous operation.
    rst: The reset signal to initialize or reset the module.
    sign: 1-bit indicates if the operation is signed (1) or unsigned (0).
    dividend: 8-bit input signal representing the dividend for division.
    divisor: 8-bit input signal representing the divisor for division.
    opn_valid: 1-bit indicates that a valid operation request is present.
Output ports:
    res_valid: 1-bit output signal indicating the result is valid and ready.
    result: 16-bit the output containing the remainder in the upper 8 bits and the quotient in the lower 8 bits.

Implementation:

Operation Start:
When opn_valid is high and res_valid is low, the module saves the inputs dividend and divisor.
Initializes the shift register SR with the absolute value of the dividend shifted left by one bit.
Sets NEG_DIVISOR to the negated absolute value of the divisor.
Sets the counter cnt to 1 and start_cnt to 1 to begin the division process.

Division Process(If start_cnt is high, the module performs the following steps):
If the counter cnt reaches 8 (most significant bit of cnt is set), the division is complete:
cnt and start_cnt are cleared.
Updates the shift register SR with the final remainder and quotient.
Otherwise, the counter cnt is incremented, and the shift register SR is updated based on the subtraction result:
Computes the subtraction of NEG_DIVISOR.
Uses a multiplexer to select the appropriate result based on the carry-out.
Updates SR by shifting left and inserting the carry-out.

Result Validity:
res_valid is managed based on the reset signal, the counter, and whether the result has been consumed.

Give me the complete code.

'''

prompt_easy = "Who is the president of the United States?"
messages = [
    {"role": "system", "content": "You are a helpful AI Assistant that provides well-reasoned and detailed responses. You first think about the reasoning process as an internal monologue and then provide the user with the answer. Respond in the following format: <think>\n...\n</think>\n<answer>\n...\n</answer>"},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)


for i in range(5):
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=4096
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(response)
