# ChipSeek-R1

## Framework

![framework](assets/framework.jpg)

Overall Framework of **ChipSeek-R1**

## Setup

### 1. LLaMA Factory Environment (for SFT)

Supervised Fine-Tuning (SFT) relies on the LLaMA Factory library. Please follow their official installation instructions to set up the environment:

*   **LLaMA Factory Repository:** [https://github.com/hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)

Ensure you have the necessary dependencies installed as per their guide.

### 2. GRPO Environment

GRPO training and the PPA evaluation scripts require the trl environment setup, including specific Python packages and EDA tool Docker containers.

**a. TRL Environment**

To run the code in this project, first, create a Python virtual environment using e.g. uv. To install uv, follow the [UV Installation Guide](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv venv chipseekr1 --python 3.11 && source chipseekr1/bin/activate && uv pip install --upgrade pip
```

Next, install vLLM and FlashAttention:

```bash
uv pip install vllm==0.8.3
uv pip install setuptools && uv pip install flash-attn --no-build-isolation
```

This will also install PyTorch `v2.5.1` and it is very important to use this version since the vLLM binaries are compiled for it. You can then install the remaining dependencies for your specific use case via `pip install -e .[LIST OF MODES]`. For most contributors, we recommend:

```bash
GIT_LFS_SKIP_SMUDGE=1 uv pip install -e ".[dev]"
```

**b. EDA Tool Docker Containers:**

Build the necessary Docker containers for simulation (Icarus Verilog) and synthesis/PPA analysis (Yosys, OpenROAD):

*   **Build Icarus Verilog Docker:**
    ```bash
    docker build -t iverilog -f docker/iverilog/Dockerfile .
    ```

*   **Build EDA Environment Docker (Yosys, OpenROAD):**
    ```bash
    docker build -t eda_env -f docker/eda/Dockerfile .
    ```

Ensure Docker is running on your system before executing these commands.

## Dataset Format

Example data formats used for training and evaluation can be found in the `data/` directory:

*   **SFT Data:** See `data/sft_dataset_example.json` for the instruction/output format used in supervised fine-tuning.
*   **GRPO/RTLLM Data:** See `data/r1_dataset_example.json` for the format including problem descriptions, gold solutions, testbenches, and PPA metrics used in GRPO and RTLLM evaluation.

## Training

### 1. Supervised Fine-Tuning (SFT)

SFT is performed using LLaMA Factory.

*   **Configuration:** The SFT training configuration is defined in `recipes/Qwen2.5-7B-Instruct/sft/verilog_sft.yaml`. Modify this file to change dataset paths, hyperparameters, etc.
*   **Run Training:** Execute the training using the `llamafactory-cli`. Adjust `CUDA_VISIBLE_DEVICES` as needed.

    ```bash
    CUDA_VISIBLE_DEVICES=0,1,2,3 FORCE_TORCHRUN=1 llamafactory-cli train recipes/Qwen2.5-7B-Instruct/sft/verilog_sft.yaml
    ```

### 2. GRPO Training

GRPO training utilizes the `accelerate` library and scripts adapted from Open R1.

*   **Configuration:** Key configurations are found in:
    *   `recipes/Qwen2.5-7B-Instruct/grpo/config_demo_code_ppa_func.yaml`: GRPO specific parameters, model details, dataset paths, reward weights.
    *   `recipes/accelerate_configs/zero4.yaml`: Distributed training configuration (e.g., DeepSpeed ZeRO stage).
*   **Run Training:** Launch the GRPO training script using `accelerate launch`. Adjust `CUDA_VISIBLE_DEVICES` and `--num_processes` according to your hardware setup.

    ```bash
    CUDA_VISIBLE_DEVICES=0,1,2,3,4,5 ACCELERATE_LOG_LEVEL=info accelerate launch \
      --config_file recipes/accelerate_configs/zero4.yaml \
      --num_processes=5 src/open_r1/grpo.py \ 
      --config recipes/Qwen2.5-7B-Instruct/grpo/config_demo_code_ppa_func.yaml
    ```

## Evaluation

Evaluation scripts are located in the `src/evaluation/` directory. Ensure the Open R1 environment (Python packages and Docker containers) is set up as described earlier.

### 1. RTLLM Benchmark

Generate Verilog code solutions for the RTLLM benchmark problems.

*   **Script:** `src/evaluation/test_on_RTLLM.py`
*   **Usage:**
    ```bash
    python src/evaluation/test_on_RTLLM.py \
      --model <path_to_your_trained_model_or_hf_name> \
      --n <number_of_samples_per_problem> \
      --temperature <sampling_temperature> \
      --gpu_ids <gpu_ids_to_use> \
      --benchmark_path benchmark/rtllm_benchmark.json
      # Add other arguments like --lora_path if needed
    ```
    Example:
    ```bash
    python src/evaluation/test_on_RTLLM.py --model /root_extends/model/Qwen2.5-Coder-7B-Verilog-sft --n 10 --temperature 0.7 --gpu_ids 0
    ```
    This will generate a `.jsonl` file in the `generated_code/` directory containing the generated solutions.

### 2. VerilogEval Benchmark

Generate Verilog code solutions for the VerilogEval benchmark problems (Human or Machine generated).

*   **Script:** `src/evaluation/test_on_verilogeval_vllm.py`
*   **Usage:**
    ```bash
    python src/evaluation/test_on_verilogeval_vllm.py \
      --model <path_to_your_trained_model_or_hf_name> \
      --bench_type <Human_or_Machine> \
      --n <number_of_samples_per_problem> \
      --temperature <sampling_temperature> \
      --gpu_ids <gpu_ids_to_use> \
      # Add other arguments as needed
    ```
    Example:
    ```bash
    python src/evaluation/test_on_verilogeval_vllm.py --model /root_extends/model/Qwen2.5-Coder-7B-Verilog-sft --bench_type Human --n 10 --temperature 0.7 --gpu_ids 0
    ```
    This will also generate a `.jsonl` file in the `generated_code/` directory.

### 3. PPA Verification (for RTLLM)

Verify the functional correctness (using Icarus Verilog) and estimate the Power, Performance, and Area (PPA) metrics (using Yosys and OpenROAD) for the code generated for the RTLLM benchmark. This requires the EDA tool Docker containers (`iverilog` and `eda_env`) to be running.

*   **Script:** `src/evaluation/verify_RTLLM.py`
*   **Usage:**
    ```bash
    python src/evaluation/verify_RTLLM.py \
      --generated_code_path <path_to_rtllm_results.jsonl> \
      --testbench_path <path_to_rtllm_benchmark_data_with_testbenches.json> \
      --output_path <path_to_save_verification_summary.json>
    ```
    Example:
    ```bash
    python src/evaluation/verify_RTLLM.py \
      --generated_code_path generated_code/rtllm_YourModelName_vllm.jsonl \
      --testbench_path /public_extends/data/verilog_designs_data_ppa.json \
      --output_path verification_results.json
    ```
    This script will output a JSON file containing detailed verification results, pass rates, and PPA scores for each problem.


