"""Reward functions for GRPO training."""

import asyncio
import json
import math
import re
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from latex2sympy2_extended import NormalizationConfig
from math_verify import LatexExtractionConfig, parse, verify
import subprocess
import tempfile
import os
import base64

from .utils import is_e2b_available


if is_e2b_available():
    from dotenv import load_dotenv
    from e2b_code_interpreter import AsyncSandbox
    from e2b_code_interpreter import Sandbox

    load_dotenv()


def accuracy_reward(completions, solution, **kwargs):
    """Reward function that checks if the completion is the same as the ground truth."""
    contents = [completion[0]["content"] for completion in completions]
    rewards = []
    for content, sol in zip(contents, solution):
        gold_parsed = parse(
            sol,
            extraction_mode="first_match",
            extraction_config=[LatexExtractionConfig()],
        )
        if len(gold_parsed) != 0:
            # We require the answer to be provided in correct latex (no malformed operators)
            answer_parsed = parse(
                content,
                extraction_config=[
                    LatexExtractionConfig(
                        normalization_config=NormalizationConfig(
                            nits=False,
                            malformed_operators=False,
                            basic_latex=True,
                            equations=True,
                            boxed="all",
                            units=True,
                        ),
                        # Ensures that boxed is tried first
                        boxed_match_priority=0,
                        try_extract_without_anchor=False,
                    )
                ],
                extraction_mode="first_match",
            )
            # Reward 1 if the content is the same as the ground truth, 0 otherwise
            try:
                reward = float(verify(answer_parsed, gold_parsed))
            except Exception as e:
                print(f"verify failed: {e}, answer: {answer_parsed}, gold: {gold_parsed}")
                reward = 0.0
        else:
            # If the gold solution is not parseable, we reward 1 to skip this example
            reward = 1.0
            print("Failed to parse gold solution: ", sol)
        rewards.append(reward)

    return rewards


def format_reward(completions, **kwargs):
    """Reward function that checks if the reasoning process is enclosed within <think> and </think> tags, while the final answer is enclosed within <answer> and </answer> tags."""
    pattern1 = r"^<think>\n.*?\n</think>\n<answer>\n.*?\n</answer>$"
    pattern2 = r"^<think>\n.*?\n</think>\n\n<answer>\n.*?\n</answer>$"
    completion_contents = [completion[0]["content"] for completion in completions]
    matches1 = [re.match(pattern1, content, re.DOTALL | re.MULTILINE) for content in completion_contents]
    matches2 = [re.match(pattern2, content, re.DOTALL | re.MULTILINE) for content in completion_contents]
    
    rewards = []
    for match1, match2 in zip(matches1, matches2):
        if match1 or match2:
            rewards.append(1.0)
        else:
            rewards.append(0.0)
            
    return rewards

def tag_count_reward(completions, **kwargs) -> list[float]:
    """Reward function that checks if we produce the desired number of think and answer tags associated with `format_reward()`.

    Adapted from: https://gist.github.com/willccbb/4676755236bb08cab5f4e54a0475d6fb#file-grpo_demo-py-L90
    """

    def count_tags(text: str) -> float:
        count = 0.0
        if text.count("<think>\n") == 1:
            count += 0.25
        if text.count("\n</think>\n") == 1:
            count += 0.25
        if text.count("\n<answer>\n") == 1:
            count += 0.25
        if text.count("\n</answer>") == 1:
            count += 0.25
        return count

    contents = [completion[0]["content"] for completion in completions]
    return [count_tags(c) for c in contents]


def reasoning_steps_reward(completions, **kwargs):
    r"""Reward function that checks for clear step-by-step reasoning.
    Regex pattern:
        Step \d+: - matches "Step 1:", "Step 2:", etc.
        ^\d+\. - matches numbered lists like "1.", "2.", etc. at start of line
        \n- - matches bullet points with hyphens
        \n\* - matches bullet points with asterisks
        First,|Second,|Next,|Finally, - matches transition words
    """
    pattern = r"(Step \d+:|^\d+\.|\n-|\n\*|First,|Second,|Next,|Finally,)"
    completion_contents = [completion[0]["content"] for completion in completions]
    matches = [len(re.findall(pattern, content)) for content in completion_contents]

    # Magic number 3 to encourage 3 steps and more, otherwise partial reward
    return [min(1.0, count / 3) for count in matches]


def len_reward(completions: list[Dict[str, str]], solution: list[str], **kwargs) -> float:
    """Compute length-based rewards to discourage overthinking and promote token efficiency.

    Taken from the Kimi 1.5 tech report: https://arxiv.org/abs/2501.12599

    Args:
        completions: List of model completions
        solution: List of ground truth solutions

    Returns:
        List of rewards where:
        - For correct answers: reward = 0.5 - (len - min_len)/(max_len - min_len)
        - For incorrect answers: reward = min(0, 0.5 - (len - min_len)/(max_len - min_len))
    """
    contents = [completion[0]["content"] for completion in completions]

    # First check correctness of answers
    correctness = []
    for content, sol in zip(contents, solution):
        gold_parsed = parse(
            sol,
            extraction_mode="first_match",
            extraction_config=[LatexExtractionConfig()],
        )
        if len(gold_parsed) == 0:
            # Skip unparseable examples
            correctness.append(True)  # Treat as correct to avoid penalizing
            print("Failed to parse gold solution: ", sol)
            continue

        answer_parsed = parse(
            content,
            extraction_config=[
                LatexExtractionConfig(
                    normalization_config=NormalizationConfig(
                        nits=False,
                        malformed_operators=False,
                        basic_latex=True,
                        equations=True,
                        boxed=True,
                        units=True,
                    ),
                    boxed_match_priority=0,
                    try_extract_without_anchor=False,
                )
            ],
            extraction_mode="first_match",
        )
        correctness.append(verify(answer_parsed, gold_parsed))

    # Calculate lengths
    lengths = [len(content) for content in contents]
    min_len = min(lengths)
    max_len = max(lengths)

    # If all responses have the same length, return zero rewards
    if max_len == min_len:
        return [0.0] * len(completions)

    rewards = []
    for length, is_correct in zip(lengths, correctness):
        lambda_val = 0.5 - (length - min_len) / (max_len - min_len)

        if is_correct:
            reward = lambda_val
        else:
            reward = min(0, lambda_val)

        rewards.append(float(reward))

    return rewards


def get_cosine_scaled_reward(
    min_value_wrong: float = -1.0,
    max_value_wrong: float = -0.5,
    min_value_correct: float = 0.5,
    max_value_correct: float = 1.0,
    max_len: int = 1000,
):
    def cosine_scaled_reward(completions, solution, **kwargs):
        """Reward function that scales based on completion length using a cosine schedule.

        Shorter correct solutions are rewarded more than longer ones.
        Longer incorrect solutions are penalized less than shorter ones.

        Args:
            completions: List of model completions
            solution: List of ground truth solutions

        This function is parameterized by the following arguments:
            min_value_wrong: Minimum reward for wrong answers
            max_value_wrong: Maximum reward for wrong answers
            min_value_correct: Minimum reward for correct answers
            max_value_correct: Maximum reward for correct answers
            max_len: Maximum length for scaling
        """
        contents = [completion[0]["content"] for completion in completions]
        rewards = []

        for content, sol in zip(contents, solution):
            gold_parsed = parse(sol, extraction_mode="first_match", extraction_config=[LatexExtractionConfig()])
            if len(gold_parsed) == 0:
                rewards.append(1.0)  # Skip unparseable examples
                print("Failed to parse gold solution: ", sol)
                continue

            answer_parsed = parse(
                content,
                extraction_config=[
                    LatexExtractionConfig(
                        normalization_config=NormalizationConfig(
                            nits=False,
                            malformed_operators=False,
                            basic_latex=True,
                            equations=True,
                            boxed=True,
                            units=True,
                        ),
                        boxed_match_priority=0,
                        try_extract_without_anchor=False,
                    )
                ],
                extraction_mode="first_match",
            )

            is_correct = verify(answer_parsed, gold_parsed)
            gen_len = len(content)

            # Apply cosine scaling based on length
            progress = gen_len / max_len
            cosine = math.cos(progress * math.pi)

            if is_correct:
                min_value = min_value_correct
                max_value = max_value_correct
            else:
                # Swap min/max for incorrect answers
                min_value = max_value_wrong
                max_value = min_value_wrong

            reward = min_value + 0.5 * (max_value - min_value) * (1.0 + cosine)
            rewards.append(float(reward))

        return rewards

    return cosine_scaled_reward


def get_repetition_penalty_reward(ngram_size: int, max_penalty: float):
    """
    Computes N-gram repetition penalty as described in Appendix C.2 of https://arxiv.org/abs/2502.03373.
    Reference implementation from: https://github.com/eddycmu/demystify-long-cot/blob/release/openrlhf/openrlhf/reward/repetition.py

    Args:
    ngram_size: size of the n-grams
    max_penalty: Maximum (negative) penalty for wrong answers
    """
    if max_penalty > 0:
        raise ValueError(f"max_penalty {max_penalty} should not be positive")

    def zipngram(text: str, ngram_size: int):
        words = text.lower().split()
        return zip(*[words[i:] for i in range(ngram_size)])

    def repetition_penalty_reward(completions, **kwargs) -> float:
        """
        reward function the penalizes repetitions
        ref implementation: https://github.com/eddycmu/demystify-long-cot/blob/release/openrlhf/openrlhf/reward/repetition.py

        Args:
            completions: List of model completions
        """

        contents = [completion[0]["content"] for completion in completions]
        rewards = []
        for completion in contents:
            if completion == "":
                rewards.append(0.0)
                continue
            if len(completion.split()) < ngram_size:
                rewards.append(0.0)
                continue

            ngrams = set()
            total = 0
            for ng in zipngram(completion, ngram_size):
                ngrams.add(ng)
                total += 1

            scaling = 1 - len(ngrams) / total
            reward = scaling * max_penalty
            rewards.append(reward)
        return rewards

    return repetition_penalty_reward


def extract_code(completion: str) -> str:
    pattern = re.compile(r"```python\n(.*?)```", re.DOTALL)
    matches = pattern.findall(completion)
    extracted_answer = matches[-1] if len(matches) >= 1 else ""
    return extracted_answer


def code_reward(completions, **kwargs) -> list[float]:
    """Reward function that evaluates code snippets using the E2B code interpreter.

    Assumes the dataset contains a `verification_info` column with test cases.
    """
    if not is_e2b_available():
        raise ImportError(
            "E2B is not available and required for this reward function. Please install E2B with "
            "`pip install e2b-code-interpreter` and add an API key to a `.env` file."
        )

    # TODO: add support for other languages in E2B: https://e2b.dev/docs/code-interpreting/supported-languages
    """Returns a reward function that evaluates code snippets in a sandbox."""
    evaluation_script_template = """
    import subprocess
    import json

    def evaluate_code(code, test_cases):
        passed = 0
        total = len(test_cases)
        exec_timeout = 5

        for case in test_cases:
            process = subprocess.run(
                ["python3", "-c", code],
                input=case["input"],
                text=True,
                capture_output=True,
                timeout=exec_timeout
            )

            if process.returncode != 0:  # Error in execution
                continue

            output = process.stdout.strip()
            if output.strip() == case["output"].strip():
                passed += 1

        success_rate = (passed / total)
        return success_rate

    code_snippet = {code}
    test_cases = json.loads({test_cases})

    evaluate_code(code_snippet, test_cases)
    """
    code_snippets = [extract_code(completion[-1]["content"]) for completion in completions]
    verification_info = kwargs["verification_info"]
    scripts = [
        evaluation_script_template.format(code=json.dumps(code), test_cases=json.dumps(json.dumps(info["test_cases"])))
        for code, info in zip(code_snippets, verification_info)
    ]
    try:
        rewards = run_async_from_sync(scripts, "python")
    except Exception as e:
        print(f"Error from E2B executor: {e}")
        rewards = [0.0] * len(completions)

    return rewards

def extract_code(completion: str) -> str:
    pattern = re.compile(r"```python\n(.*?)```", re.DOTALL)
    matches = pattern.findall(completion)
    extracted_answer = matches[-1] if len(matches) >= 1 else ""
    return extracted_answer

def extract_verilog(completion: str) -> str:
    pattern = re.compile(r"<answer>\n(.*?)\n</answer>", re.DOTALL)
    matches = pattern.findall(completion)
    extracted_answer = matches[-1] if len(matches) >= 1 else ""
    
    if extracted_answer == "":
        pattern = re.compile(r"```verilog\n(.*?)\n```", re.DOTALL)
        matches = pattern.findall(completion)
        extracted_answer = matches[-1] if len(matches) >= 1 else ""
    
    return extracted_answer

def run_synthesis_ppa(name, code, top_module, gold_ppa_metrics):

    try:        
        # Create a folder with the name
        folder_path = f"/root/autodl-tmp/ChipSeek-R1/ppa_test/{name}"
        subprocess.run(
            ['mkdir', '-p', folder_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        encoded_code = base64.b64encode(code.encode()).decode()
        # Copy the design code to the folder
        subprocess.run(
            ['bash', '-c', f'echo {encoded_code} | base64 -d > {folder_path}/design.v'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Copy the run_synthesis_ppa.sh script to the folder
        subprocess.run(
            ['cp', '/root/autodl-tmp/ChipSeek-R1/src/ppa_script/run_synthesis_ppa.sh', folder_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Run the synthesis and PPA analysis script inside the Docker container in the new folder
        process = subprocess.run(
            ["bash", "-c", 
                f'cd {folder_path} && export PATH="/root/autodl-tmp/oss-cad-suite/bin:$PATH" && TOP_MODULE={top_module} INPUT_VERILOG={folder_path}/design.v {folder_path}/run_synthesis_ppa.sh'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if process.returncode != 0:
            return 0.0  # Error in execution

        # Get the content from the PPA metrics JSON file
        ppa_metrics_process = subprocess.run(
            ['cat', f'{folder_path}/ppa_metrics.json'],
            capture_output=True,
            text=True,
            timeout=5
        )
        

        
        if ppa_metrics_process.returncode != 0:
            return 0.0  # Error in execution

        # Parse the PPA JSON output
        ppa_metrics = json.loads(ppa_metrics_process.stdout)
        # Example: Use total power as a reward metric
        total_power = ppa_metrics.get("power", {}).get("total_power_W", 0.0)
        total_area = ppa_metrics.get("area", {}).get("design_area_um2", 0.0)
        total_delay = ppa_metrics.get("performance", {}).get("max_path_delay_ns", 0.0)

        if gold_ppa_metrics == None:
            if total_power > 0 and total_area > 0 and total_delay >= 0:
                return 0.1
            else:
                return 0.0
        else:
            gold_power = gold_ppa_metrics.get("power", {}).get("total_power_W", 0.0)
            gold_area = gold_ppa_metrics.get("area", {}).get("design_area_um2", 0.0)
            gold_delay = gold_ppa_metrics.get("performance", {}).get("max_path_delay_ns", 0.0)

            if gold_power > 0 and gold_area > 0 and gold_delay >= 0:
                if total_power > 0 and total_area > 0 and total_delay >= 0:
                    if gold_power * gold_area * gold_delay == 0 or total_power * total_area * total_delay == 0:
                        return 0.1
                    else:
                        ratio = (gold_power/total_power) * (gold_area/total_area) * (gold_delay/total_delay)
                        # Clamp the ratio between 0.5 and 3.0
                        ratio = max(0.1, min(ratio,3))
                        return ratio
                else:
                    return 0.0
            else:
                if total_power > 0 and total_area > 0 and total_delay >= 0:
                    return 0.1
                else:
                    return 0.0

    except Exception as e:
        return 0.0
    finally:
        # Clean up temporary files
        try:
            subprocess.run(
                ['rm', '-rf', folder_path],
                timeout=5,
                capture_output=True
            )
        except:
            pass

def run_iverilog(name, code, testbench):
    unique_id = uuid.uuid4().hex
    encoded_code = base64.b64encode(code.encode()).decode()
    testbench_b64 = base64.b64encode(testbench.encode()).decode()
    ret_val = 0.0
    # ret_val = -1.0
    try: 
        folder_path = f"/root/autodl-tmp/ChipSeek-R1/iverilog_test/{name}_{unique_id}"
        subprocess.run(
            ['mkdir', folder_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        subprocess.run(
            ['bash', '-c', f'echo {encoded_code} | base64 -d > {folder_path}/design.v'],
            capture_output=True,
            text=True,
            timeout=5
        )
        subprocess.run(
            ['bash', '-c', f'echo {testbench_b64} | base64 -d > {folder_path}/testbench.v'],
            capture_output=True,
            text=True,
            timeout=5
        )
        compile_process = subprocess.run(
            ['iverilog', '-Wall', '-Winfloop', '-Wno-timescale', '-g2012', '-o', f'{folder_path}/a.out', f'{folder_path}/design.v', f'{folder_path}/testbench.v'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if compile_process.returncode == 0:
            ret_val = 0.2
            sim_process = subprocess.run(
                ['vvp', f'{folder_path}/a.out'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if sim_process.returncode == 0:
                if "pass" in sim_process.stdout.lower():
                    ret_val = 1.0
                else:
                    match = re.search(r'Mismatches: ([0-9]*) in ([0-9]*) samples', sim_process.stdout)
                    if match:
                        cor, tot = [int(i) for i in match.groups()]
                        if cor == 0:
                            ret_val = 1.0
        if ret_val == 0.0:
            subprocess.run(
                ['mkdir', folder_path],
                capture_output=True,
                text=True,
                timeout=5
            )

            subprocess.run(
                ['bash', '-c', f'echo {encoded_code} | base64 -d > {folder_path}/design.v'],
                capture_output=True,
                text=True,
                timeout=5
            )
            subprocess.run(
                ['bash', '-c', f'echo {testbench_b64} | base64 -d > {folder_path}/testbench.v'],
                capture_output=True,
                text=True,
                timeout=5
            )
            compile_process_1 = subprocess.run(
                ['iverilog', '-o', f'{folder_path}/a.out', f'{folder_path}/design.v', f'{folder_path}/testbench.v'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if compile_process_1.returncode == 0:
                ret_val = 0.2
                sim_process = subprocess.run(
                    ['vvp', f'{folder_path}/a.out'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if sim_process.returncode == 0:
                    if "pass" in sim_process.stdout.lower():
                        ret_val = 1.0
                    else:
                        match = re.search(r'Mismatches: ([0-9]*) in ([0-9]*) samples', sim_process.stdout)
                        if match:
                            cor, tot = [int(i) for i in match.groups()]
                            if cor == 0:
                                ret_val = 1.0 
        # if ret_val == 0.0 and (compile_process.returncode == 0 or compile_process_1.returncode == 0):
        #     ret_val = 0.2
        return ret_val
    except Exception as e:
        return 0.0
    finally:
        try:
            subprocess.run(
                ['rm', '-rf', f'{folder_path}'],
                capture_output=True,
                text=True,
                timeout=5
            )
        except:
            pass


def verilog_code_reward(completions, **kwargs) -> list[float]:
    """Reward function that evaluates Verilog code snippets using the E2B code interpreter.

    Assumes the dataset contains a `verification_info` column with testbenches.
    """

    code_snippets = [extract_verilog(completion[-1]["content"]) for completion in completions]
    verification_infos = kwargs["verification_info"]
    names = kwargs.get("problem_id", "test")
    rewards = [0.0] * len(completions)  # Initialize rewards with 0.0
    gold_ppa_metrics = kwargs.get("ppa_metrics", None)

    with ThreadPoolExecutor() as executor:
        futures = []
        for i, (code, info, name) in enumerate(zip(code_snippets, verification_infos, names)):
            testbench = info["testbench"]
            future = executor.submit(run_iverilog, name, code, testbench)
            futures.append((i, future))

        for i, future in futures:
            try:
                reward = future.result()
                if isinstance(reward, float):
                    rewards[i] = reward
            except Exception as e:
                print(f"Error from verilog-eval for completion {i}: {e}")

    with ThreadPoolExecutor() as executor:
        futures = []
        for reward, code, info, name, gold_ppa_metric in zip(rewards, code_snippets, verification_infos, names, gold_ppa_metrics):
            if reward > 0 and info["top_module"]:
                future = executor.submit(
                    run_synthesis_ppa,
                    f"{name}_{uuid.uuid4().hex}",  # Unique folder name
                    code,
                    info["top_module"],
                    gold_ppa_metric
                )
                futures.append(future)
            else:
                futures.append(None)
        
        ppa_rewards = [f.result() if f else 0.0 for f in futures]

    for i in range(len(rewards)):
        rewards[i] = rewards[i] + ppa_rewards[i]

    for r in rewards:
        if r != 0:
            break

    return rewards


def verilog_ppa_reward(completions, **kwargs) -> list[float]:
    """Reward function that evaluates Verilog code snippets for Power, Performance, and Area (PPA) using a Docker container.

    Assumes the dataset contains a `verification_info` column with testbenches and top module information.
    """
    rewards = []

    code_snippets = [extract_verilog(completion[-1]["content"]) for completion in completions]
    verification_info = kwargs["verification_info"]
    name = kwargs.get("problem_id", "test_problem")
    gold_ppa_metrics = kwargs.get("ppa_metrics", None)
    for code, info, n, gold_ppa_m in zip(code_snippets, verification_info, name, gold_ppa_metrics):
        top_module = info["top_module"]
        if top_module != None and top_module != "":
            output = run_synthesis_ppa(n, code, info["top_module"], gold_ppa_m)
            rewards.append(output)
        else:
            rewards.append(0.0)

    return rewards

def get_verilog_format_reward(completions, **kwargs):
    pattern = r"^<think>\n.*?\n</think>\n<answer>\n.*?\n</answer>$"
    completion_contents = [completion[0]["content"] for completion in completions]
    matches = [re.match(pattern, content, re.DOTALL | re.MULTILINE) for content in completion_contents]
    return [1.0 if match else 0.0 for match in matches]

def get_code_format_reward(language: str = "python"):
    """Format reward function specifically for code responses.

    Args:
        language: Programming language supported by E2B https://e2b.dev/docs/code-interpreting/supported-languages
    """
    pattern = rf"^<think>\n.*?\n</think>\n<answer>\n.*?```{language}.*?```.*?\n</answer>$"

    def code_format_reward(completions, **kwargs):
        completion_contents = [completion[0]["content"] for completion in completions]
        matches = [re.match(pattern, content, re.DOTALL | re.MULTILINE) for content in completion_contents]
        return [1.0 if match else 0.0 for match in matches]

    return code_format_reward


def run_async_from_sync(scripts: list[str], language: str) -> list[float]:
    """Function wrapping the `run_async` function."""
    # Create a new event loop and set it
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Run the async function and get the result
        rewards = loop.run_until_complete(run_async(scripts, language))
    finally:
        loop.close()

    return rewards


async def run_async(scripts: list[str], language: str) -> list[float]:
    # Create the sandbox by hand, currently there's no context manager for this version
    sbx = await AsyncSandbox.create(timeout=30, request_timeout=3)

    # Create a list of tasks for running scripts concurrently
    tasks = [run_script(sbx, script, language) for script in scripts]

    # Wait for all tasks to complete and gather their results as they finish
    results = await asyncio.gather(*tasks)
    rewards = list(results)  # collect results

    # Kill the sandbox after all the tasks are complete
    await sbx.kill()

    return rewards


async def run_script(sbx, script: str, language: str) -> float:
    execution = await sbx.run_code(script, language=language)
    try:
        return float(execution.text)
    except (TypeError, ValueError):
        return 0.0