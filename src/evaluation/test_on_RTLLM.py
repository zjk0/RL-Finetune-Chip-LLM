import argparse
import json
import os
import re
from tqdm import tqdm
from openai import OpenAI
import truststore
truststore.inject_into_ssl()  # Forces Python to use system certificates

# Import vLLM
from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest

def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

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
    elif template == "deepseek":
        # DeepSeek-style chat template
        if system_prompt:
            return f"<｜begin▁of▁sentence｜>{system_prompt}\n\nUser: {prompt_text}\n\nA: "
        else:
            return f"<｜begin▁of▁sentence｜>User: {prompt_text}\n\nA: "
    else:
        # Default to Qwen
        if system_prompt:
            return f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{prompt_text}<|im_end|>\n<|im_start|>assistant\n"
        else:
            return f"<|im_start|>user\n{prompt_text}<|im_end|>\n<|im_start|>assistant\n"

# Function to extract Verilog code from the response
def extract_verilog_code(response):
    pattern = re.compile(r"```(?:verilog)?\s*(.*?)```", re.DOTALL)
    matches = pattern.findall(response)
    if matches:
        return matches[-1].strip()
    else:
        # Try to extract code without markdown code blocks
        pattern = re.compile(r"module\s+\w+\s*\(.*?endmodule", re.DOTALL)
        matches = pattern.findall(response)
        if matches:
            return matches[0].strip()
        return ""

def extract_verilog_code_rtlcoder(s_full):
    if len(s_full.split('endmodulemodule', 1)) == 2:
        s = s_full.split('endmodulemodule', 1)[0] + "\n" + "endmodule"
    else:
        s = s_full.rsplit('endmodule', 1)[0] + "\n" + "endmodule"
    if s.find('top_module') != -1:
        s = s.split('top_module', 1)[0]
        s = s.rsplit('endmodule', 1)[0] + "\n" + "endmodule"
    index = s.rfind('tb_module')
    if index == -1:
        index = s.find('testbench')
    if index != -1:
        s_tmp = s[:index]
        s = s_tmp.rsplit("endmodule", 1)[0] + "\n" + "endmodule"
    return s

def main():
    parser = argparse.ArgumentParser(description='Process RTLLM benchmark evaluation with vLLM.')
    parser.add_argument('--model', type=str)
    parser.add_argument('--n', type=int, default=10) # 'n' represent how many code candidates generated for each instruction
    parser.add_argument('--temperature', type=float, default=0.7)
    parser.add_argument('--tensor_parallel_size', type=int, default=1) # Number of GPUs to use for tensor parallelism
    parser.add_argument('--max_model_len', type=int, default=4096) # Maximum context length
    parser.add_argument('--gpu_utils', type=float, default=0.95) # Maximum tokens to generate
    parser.add_argument('--gpu_ids', type=str, default="0", help="Comma-separated list of GPU IDs to use (e.g., '0,1,2')")
    parser.add_argument('--chat_template', type=str, default="qwen", 
                        help="Chat template to use: 'qwen', 'llama', 'vicuna', 'raw', 'deepseek'")
    parser.add_argument('--system_prompt', type=str, 
                        default="You are a helpful AI Assistant that provides well-reasoned and detailed responses. You first think about the reasoning process as an internal monologue and then provide the user with the answer. Respond in the following format: <think>\n...\n</think>\n<answer>\n...\n</answer>",
                        help="System prompt to use for the model")
    parser.add_argument('--use_system_prompt', action='store_true', 
                        help="Whether to use the system prompt")
    parser.add_argument('--lora_path', type=str, default=None,
                        help="Path to the PEFT adapter directory (e.g., LoRA weights). If specified, --model should be the base model path.")
    parser.add_argument('--benchmark_path', type=str,
                        help="Path to the benchmark data")
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

    workspace_path = os.getcwd()
    print(f"Current workspace path: {workspace_path}")

    # Load RTLLM benchmark data
    benchmark_path = os.path.join(workspace_path, args.benchmark_path)
    print(f"Loading benchmark data from {benchmark_path}")
    benchmark_data = load_json(benchmark_path)

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

    # Prepare all prompts that need to be generated
    all_prompts = []
    problem_ids = []

    # Create a list of prompts for each sample in the benchmark
    for sample in benchmark_data:
        problem_text = sample.get('problem', '')
        problem_id = sample.get('problem_id', '')
        
        if not problem_text or not problem_id:
            continue
        
        for _ in range(args.n):  # Generate multiple prompts for each sample
            problem_text = 'Solve the following coding problem using the programming language verilog. Output the code between ```verilog and ```.\n' + problem_text
            formatted_prompt = format_prompt_with_template(problem_text, args.chat_template, system_prompt)
            all_prompts.append(formatted_prompt)
            problem_ids.append(problem_id)

    print(f"Total inference tasks: {len(all_prompts)}")

    # Create output directory if it doesn't exist
    os.makedirs('generated_code', exist_ok=True)
    output_file = f'generated_code/rtllm_{model_name_base}_vllm.jsonl'

    # Initialize valid results list
    valid_results = []

    if args.model != "gpt-4o":
        # Initialize vLLM engine
        print(f"Initializing vLLM with model: {args.model}")
        if args.lora_path:
            print(f"Applying LoRA adapter from: {args.lora_path}")
        print(f"Using context length of {args.max_model_len} tokens")

        # Add swap space for PagedAttention with long contexts
        os.environ["VLLM_USE_SWAP"] = "1"
        # --- MODIFICATION START ---
        enable_lora_flag = False
        lora_adapter_paths = None
        if args.lora_path:
            if not os.path.exists(args.lora_path):
                raise ValueError(f"LoRA path specified but not found: {args.lora_path}")
            enable_lora_flag = True
            lora_adapter_paths = args.lora_path
            print(f"  Base model path: {args.model}")
            print(f"  LoRA adapter path: {args.lora_path}")

        llm = LLM(
            model=args.model,
            tensor_parallel_size=args.tensor_parallel_size,
            trust_remote_code=True,
            max_model_len=args.max_model_len,
            dtype="bfloat16",  # Using bfloat16 for better performance
            gpu_memory_utilization=args.gpu_utils,  # Higher utilization for long contexts
            swap_space=4,  # Add 4GB swap space for handling long contexts
            enable_lora=enable_lora_flag, # Enable LoRA if path is provided
        )


        # Set sampling parameters
        sampling_params = SamplingParams(
            temperature=args.temperature,
            max_tokens=3500,
            stop=stop_tokens
        )

        # Generate completions using vLLM's efficient batching
        print("Generating completions with vLLM...")
        if enable_lora_flag:
            outputs = llm.generate(all_prompts, sampling_params, lora_request=LoRARequest("verilog_adapter", 1, lora_adapter_paths))
        else:
            outputs = llm.generate(all_prompts, sampling_params)


        # Map to track which prompts still need valid code
        regeneration_map = {}
        for i, (output, problem_id, formatted_prompt) in enumerate(zip(outputs, problem_ids, all_prompts)):
            response = output.outputs[0].text
            verilog_code = extract_verilog_code(response)
            
            if verilog_code:
                # Valid code found, save the result
                valid_results.append({
                    "problem_id": problem_id,
                    "completion": verilog_code,
                    "response": response
                })
            else:
                # No code found, add to regeneration map
                regeneration_map[i] = {
                    "prompt": formatted_prompt,
                    "problem_id": problem_id
                }

        # Keep regenerating until all prompts have valid code or max attempts reached
        max_regeneration_attempts = 10
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
            regenerated_outputs = llm.generate(regeneration_prompts, sampling_params)
            
            # Process regenerated outputs
            for i, (output, idx) in enumerate(zip(regenerated_outputs, regeneration_indices)):
                response = output.outputs[0].text
                if "rtlcoder" in args.model.lower():
                    verilog_code = extract_verilog_code_rtlcoder(response)
                else:
                    verilog_code = extract_verilog_code(response)
                
                if verilog_code:
                    # Valid code found in regenerated response
                    valid_results.append({
                        "problem_id": regeneration_map[idx]["problem_id"],
                        "completion": verilog_code,
                        "response": response
                    })
                    # Remove from regeneration map
                    del regeneration_map[idx]
        if regeneration_map:
            print(f"Warning: {len(regeneration_map)} prompts still failed to generate valid code after {max_regeneration_attempts} attempts")

    else:
        print("Using GPT-4o")
        for prompt, problem_id in tqdm(zip(all_prompts, problem_ids), total=len(all_prompts), desc="Generating with GPT-4o"):
            client = OpenAI()
            response = client.responses.create(
                model="gpt-4o",
                input=prompt,
                max_output_tokens=2048
            )
            verilog_code = extract_verilog_code(response.output_text)
            valid_results.append({
                "problem_id": problem_id,
                "completion": verilog_code,
                "response": response.output_text
            })

    # Write only valid results to the output file
    with open(output_file, 'w') as f:
        for result in tqdm(valid_results, desc="Writing results"):
            f.write(json.dumps(result) + "\n")

    print(f"Inference completed with vLLM. Results saved to {output_file}")
    print(f"Total valid responses with code: {len(valid_results)}/{len(all_prompts)}")

if __name__ == "__main__":
    main()