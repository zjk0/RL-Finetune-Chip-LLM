import argparse
import json
import os
import re
from tqdm import tqdm

# Import vLLM
from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest

def load_json(filename):
    des_data = []
    with open(filename, 'r') as f:
        for line in f:
            data = json.loads(line)
            des_data.append(data)
    return des_data

def parse_verilog_code(response):
    pattern = re.compile(r"```verilog\n(.*?)```", re.DOTALL)
    matches = pattern.findall(response)
    extracted_answer = matches[-1] if len(matches) >= 1 else ""
    if extracted_answer == "":
        extracted_answer = response
    # Remove top module interface using string operations
    if extracted_answer != "":
        completion = re.sub(r'module top_module[^;]+;', '', extracted_answer)
        while len(completion) > 0 and completion[0] == '\n':
            completion = completion[1:]
    else:
        completion = ""
    return completion

# Function to format prompts based on chosen template
def format_prompt_with_template(prompt_text, template, system_prompt=""):
    if template == "qwen":
        # Qwen's chat template
        if system_prompt:
            return f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{prompt_text}<|im_end|>\n<|im_start|>assistant\n"
        else:
            return f"<|im_start|>user\n{prompt_text}<|im_end|>\n<|im_start|>assistant\n"
    elif template == "llama":
        # Llama-style chat template
        if system_prompt:
            return f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt_text} [/INST]"
        else:
            return f"<s>[INST] {prompt_text} [/INST]"
    elif template == "vicuna":
        # Vicuna-style chat template
        if system_prompt:
            return f"SYSTEM: {system_prompt}\nUSER: {prompt_text}\nASSISTANT:"
        else:
            return f"USER: {prompt_text}\nASSISTANT:"
    elif template == "raw":
        # No template, use raw prompt with system prompt
        if system_prompt:
            return f"System: {system_prompt}\n\nUser: {prompt_text}\n\nAssistant:"
        else:
            return prompt_text
    else:
        # Default to Qwen
        if system_prompt:
            return f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{prompt_text}<|im_end|>\n<|im_start|>assistant\n"
        else:
            return f"<|im_start|>user\n{prompt_text}<|im_end|>\n<|im_start|>assistant\n"

def main():
    parser = argparse.ArgumentParser(description='Process Verilog evaluation with vLLM.')
    parser.add_argument('--model', type=str, default="/root_extends/model/Qwen2.5-Coder-7B-Verilog-sft")
    parser.add_argument('--bench_type', type=str, default="Human") # it can be Machine or Human
    parser.add_argument('--n', type=int, default=10) # 'n' represent how many code candidates generated for each instruction
    parser.add_argument('--temperature', type=float, default=0.7)
    parser.add_argument('--tensor_parallel_size', type=int, default=1) # Number of GPUs to use for tensor parallelism
    parser.add_argument('--max_model_len', type=int, default=4096) # Maximum context length
    parser.add_argument('--gpu_utils', type=float, default=0.95) # Maximum tokens to generate
    parser.add_argument('--gpu_ids', type=str, default="0", help="Comma-separated list of GPU IDs to use (e.g., '0,1,2')")
    parser.add_argument('--chat_template', type=str, default="qwen", 
                        help="Chat template to use: 'qwen', 'llama', 'vicuna', 'raw'")
    parser.add_argument('--system_prompt', type=str, 
                        default="You are a helpful AI Assistant that provides well-reasoned and detailed responses. You first think about the reasoning process as an internal monologue and then provide the user with the answer. Respond in the following format: <think>\n...\n</think>\n<answer>\n...\n</answer>",
                        help="System prompt to use for the model")
    parser.add_argument('--use_system_prompt', action='store_true', 
                        help="Whether to use the system prompt")
    parser.add_argument("--lora_path", type=str, default=None)
    args = parser.parse_args()

    # Set visible GPUs based on user input
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_ids
    print(f"Using GPUs: {args.gpu_ids}")

    system_prompt = args.system_prompt if args.use_system_prompt else ""
    if args.use_system_prompt:
        print(f"Using system prompt: {system_prompt}")
    else:
        print("System prompt disabled")

    model_name_base = args.model.split("/")[-1]

    # Get the current working directory
    workspace_path = os.getcwd()
    print(f"Current workspace path: {workspace_path}")

    descri_path = workspace_path + '/benchmark/VerilogDescription_' + args.bench_type + '.jsonl'
    input_path = workspace_path + '/benchmark/VerilogEval_' + args.bench_type + '.jsonl'

    des_data = load_json(descri_path)
    input_data = load_json(input_path)

    # Create a dictionary to store descriptions indexed by task_id
    descriptions_by_id = {item['task_id']: item['detail_description'] for item in des_data}

    # Create the combined data with task_id and concatenated prompts
    combined_data = []
    for input_item in input_data:
        task_id = input_item['task_id']
        if task_id in descriptions_by_id:
            combined_item = {
                'task_id': task_id,
                'prompt': 'Solve the following coding problem using the programming language verilog. Output the code between ```verilog and ```.\n' + descriptions_by_id[task_id] + '\nThe module interface is shown below:\n' + input_item['prompt']
            }
            combined_data.append(combined_item)
        else:
            print(f"Task ID {task_id} not found in descriptions_by_id")

    # Initialize vLLM engine
    print(f"Initializing vLLM with model: {args.model}")
    print(f"Using context length of {args.max_model_len} tokens")
    print(f"Note: 32K context requires ~24GB GPU RAM per GPU for 7B model, ~40GB for 14B")

    # Add swap space for PagedAttention with long contexts
    os.environ["VLLM_USE_SWAP"] = "1"

    if args.lora_path != None:
        enable_lora = True
    else:
        enable_lora = False

    llm = LLM(
        model=args.model,
        tensor_parallel_size=args.tensor_parallel_size,
        trust_remote_code=True,
        max_model_len=args.max_model_len,
        dtype="bfloat16",  # Using bfloat16 for better performance
        gpu_memory_utilization=args.gpu_utils,  # Higher utilization for long contexts
        swap_space=4,  # Add 4GB swap space for handling long contexts
        enable_lora = enable_lora
    )

    # Create output directory if it doesn't exist
    os.makedirs('generated_code', exist_ok=True)
    output_file = f'generated_code/verilogeval_{model_name_base}_{args.bench_type}_vllm.jsonl'

    # Prepare all prompts that need to be generated
    all_prompts = []
    task_ids = []

    # Set stop tokens based on template
    if args.chat_template == "qwen":
        stop_tokens = ["<|im_end|>"]
    elif args.chat_template == "llama":
        stop_tokens = ["</s>"]
    elif args.chat_template == "vicuna":
        stop_tokens = ["USER:"]
    else:
        stop_tokens = None

    print(f"Using chat template: {args.chat_template}")
    print("Preparing prompts...")

    for data in combined_data:
        for _ in range(args.n):
            prompt_text = data['prompt']
            formatted_prompt = format_prompt_with_template(prompt_text, args.chat_template, system_prompt)
            all_prompts.append(formatted_prompt)
            task_ids.append(data['task_id'])

    print(f"Total inference tasks: {len(all_prompts)}")

    # Set sampling parameters
    sampling_params = SamplingParams(
        temperature=args.temperature,
        max_tokens=4096,
        stop=stop_tokens
    )

    # Generate completions using vLLM's efficient batching
    print("Generating completions with vLLM...")
    if enable_lora:
        outputs = llm.generate(
            all_prompts, 
            sampling_params, 
            lora_request=LoRARequest("lora_adapter", 1, args.lora_path)
        )
    else:
        outputs = llm.generate(all_prompts, sampling_params)

    # Initialize valid results list
    valid_results = []

    # Map to track which prompts still need valid code
    regeneration_map = {}
    for i, (output, task_id, formatted_prompt) in enumerate(zip(outputs, task_ids, all_prompts)):
        response = output.outputs[0].text
        verilog_code = parse_verilog_code(response)
        
        if verilog_code:
            # Valid code found, save the result
            valid_results.append({
                "task_id": task_id,
                "completion": verilog_code,
                "response": response
            })
        else:
            # No code found, add to regeneration map
            regeneration_map[i] = {
                "prompt": formatted_prompt,
                "task_id": task_id
            }

    # Keep regenerating until all prompts have valid code or max attempts reached
    max_regeneration_attempts = 3
    current_attempt = 0

    while regeneration_map and current_attempt < max_regeneration_attempts:
        current_attempt += 1
        print(f"Regeneration attempt {current_attempt}: {len(regeneration_map)} prompts need regeneration")
        
        # Prepare prompts for this regeneration batch
        regeneration_prompts = []
        regeneration_indices = []
        
        for idx, item in regeneration_map.items():
            regeneration_prompts.append(item["prompt"])
            regeneration_indices.append(idx)
        
        # Generate new responses
        if enable_lora:
            regenerated_outputs = llm.generate(
                regeneration_prompts, 
                sampling_params, 
                lora_request=LoRARequest("lora_adapter", 1, args.lora_path)
            )
        else:
            regenerated_outputs = llm.generate(regeneration_prompts, sampling_params)
        
        # Process regenerated outputs
        for i, (output, idx) in enumerate(zip(regenerated_outputs, regeneration_indices)):
            response = output.outputs[0].text
            verilog_code = parse_verilog_code(response)
            
            if verilog_code:
                # Valid code found in regenerated response
                valid_results.append({
                    "task_id": regeneration_map[idx]["task_id"],
                    "completion": verilog_code,
                    "response": response
                })
                # Remove from regeneration map
                del regeneration_map[idx]

    # Write only valid results to the output file
    with open(output_file, 'w') as f:
        for result in tqdm(valid_results, desc="Writing results"):
            f.write(json.dumps(result) + "\n")

    print(f"Inference completed with vLLM. Results saved to {output_file}")
    print(f"Total valid responses with code: {len(valid_results)}/{len(all_prompts)}")
    if regeneration_map:
        print(f"Warning: {len(regeneration_map)} prompts still failed to generate valid code after {max_regeneration_attempts} attempts")
        
if __name__ == "__main__":
    main()