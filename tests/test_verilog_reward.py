"""Reward functions for GRPO training."""

import asyncio
import json
import math
import re
from typing import Dict
import base64

from latex2sympy2_extended import NormalizationConfig
from math_verify import LatexExtractionConfig, parse, verify
from transformers.utils.import_utils import _is_package_available
import subprocess
# Use same as transformers.utils.import_utils
_e2b_available = _is_package_available("e2b")


def is_e2b_available() -> bool:
    return _e2b_available


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
    pattern = r"^<think>\n.*?\n</think>\n<answer>\n.*?\n</answer>$"
    completion_contents = [completion[0]["content"] for completion in completions]
    matches = [re.match(pattern, content, re.DOTALL | re.MULTILINE) for content in completion_contents]
    return [1.0 if match else 0.0 for match in matches]


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


def extract_verilog(completion: str) -> str:
    pattern = re.compile(r"```verilog\n(.*?)```", re.DOTALL)
    matches = pattern.findall(completion)
    extracted_answer = matches[-1] if len(matches) >= 1 else ""
    return extracted_answer


def verilog_code_reward(completions, **kwargs) -> list[float]:
    """Reward function that evaluates Verilog code snippets using the E2B code interpreter.

    Assumes the dataset contains a `verification_info` column with testbenches.
    """

    
    code_snippets = [extract_verilog(completion[-1]["content"]) for completion in completions]
    verification_infos = kwargs["verification_info"]
    names = kwargs.get("problem_id", "test")
    rewards = []
    def run_iverilog(name, code, testbench):

        folder_path = f"/code_test/{name}"
        testbench_b64 = base64.b64encode(testbench.encode()).decode()

        # Copy the design code to the folder
        try: 
            subprocess.run(
                ["docker", "exec", "verilog-eval", "bash", "-c", f'mkdir {folder_path}'],
                capture_output=True,
                text=True,
                timeout=1
            )

            subprocess.run(
                ["docker", "exec", "-i", "verilog-eval", "bash", "-c", f'cat > {folder_path}/design.v'],
                input=code,
                capture_output=True,
                text=True,
                timeout=1
            )
            subprocess.run(
                ["docker", "exec", "verilog-eval", "bash", "-c", f"echo '{testbench_b64}' | base64 -d > {folder_path}/testbench.v"],
                capture_output=True,
                text=True,
                timeout=5  # Increased timeout to ensure completion
            )
            compile_process = subprocess.run(
                ["docker", "exec", "verilog-eval", "bash", "-c", 
                 f'iverilog -Wall -Winfloop -Wno-timescale -g2012 -o {folder_path}/a.out {folder_path}/design.v {folder_path}/testbench.v'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if compile_process.returncode != 0:
                subprocess.run(
                    ["docker", "exec", "verilog-eval", "bash", "-c", f'rm -rf {folder_path}'],
                )
                return 0.0  # Compilation failed
            
            sim_process = subprocess.run(
                ["docker", "exec", "verilog-eval", "bash", "-c", f'vvp {folder_path}/a.out'],
                capture_output=True,
                text=True,
                timeout=30
            )

            # subprocess.run(
            #     ["docker", "exec", "verilog-eval", "bash", "-c", f'rm -rf {folder_path}'],
            # )


            if sim_process.returncode == 0:
                print(sim_process.stdout)
                if "pass" in sim_process.stdout.lower():
                    return 1.0
                else:
                    match = re.search(r'Mismatches: ([0-9]*) in ([0-9]*) samples', sim_process.stdout)
                    if match:
                        cor, tot = [int(i) for i in match.groups()]
                        if cor == 0:
                            return 1.0
                    return 0.0
            else:
                return 0.0
        except Exception as e:
            print(e)
            return 0.0
        


    try:
        for code, info, name in zip(code_snippets, verification_infos, names):
            testbench = info["testbench"]
            reward = run_iverilog(name, code, testbench)
            # Check if reward is a float, if it is, append to rewards, else append 0.0
            if isinstance(reward, float):
                rewards.append(reward)
            else:
                rewards.append(0.0)
    except Exception as e:
        print(f"Error from verilog-eval: {e}")
        rewards = [0.0] * len(completions)

    return rewards

# Example usage of verilog_code_reward function
def test_verilog_reward():
    """Test the verilog_code_reward function with a simple 8-bit adder example."""
    # Correct 8-bit adder implementation
    correct_adder = """
module top_module (
        input a, 
        input b, 
        output q
);

        assign q = a&b;

endmodule
"""

    # Incorrect 8-bit adder implementation (missing carry bit)
    incorrect_adder = """
module top_module (
        input a, 
        input b, 
        output q
);

        assign q = a|b;

endmodule
"""

    # Testbench for the 8-bit adder
    testbench = """
`timescale 1 ps/1 ps
`define OK 12
`define INCORRECT 13
module reference_module (
        input a, 
        input b, 
        output q
);

        assign q = a&b;

endmodule


module stimulus_gen (
        input clk,
        output logic a,b,
        output reg[511:0] wavedrom_title,
        output reg wavedrom_enable
);


// Add two ports to module stimulus_gen:
//    output [511:0] wavedrom_title
//    output reg wavedrom_enable

        task wavedrom_start(input[511:0] title = "");
        endtask

        task wavedrom_stop;
                #1;
        endtask



        initial begin
                {a,b} <= 0;
                @(negedge clk) wavedrom_start("Unknown circuit");
                        @(posedge clk) {a,b} <= 0;
                        repeat(8) @(posedge clk) {a,b} <= {a,b} + 1;
                @(negedge clk) wavedrom_stop();

                repeat(100) @(posedge clk, negedge clk)
                        {a,b} <= $urandom;
                $finish;
        end

endmodule

module tb();

        typedef struct packed {
                int errors;
                int errortime;
                int errors_q;
                int errortime_q;

                int clocks;
        } stats;

        stats stats1;


        wire[511:0] wavedrom_title;
        wire wavedrom_enable;
        int wavedrom_hide_after_time;

        reg clk=0;
        initial forever
                #5 clk = ~clk;

        logic a;
        logic b;
        logic q_ref;
        logic q_dut;

        initial begin 
                $dumpfile("wave.vcd");
                $dumpvars(1, stim1.clk, tb_mismatch ,a,b,q_ref,q_dut );
        end


        wire tb_match;          // Verification
        wire tb_mismatch = ~tb_match;

        stimulus_gen stim1 (
                .clk,
                .* ,
                .a,
                .b );
        reference_module good1 (
                .a,
                .b,
                .q(q_ref) );

        top_module top_module1 (
                .a,
                .b,
                .q(q_dut) );


        bit strobe = 0;
        task wait_for_end_of_timestep;
                repeat(5) begin
                        strobe <= !strobe;  // Try to delay until the very end of the time step.
                        @(strobe);
                end
        endtask


        final begin
                if (stats1.errors_q) $display("Hint: Output '%s' has %0d mismatches. First mismatch occurred at time %0d.", "q", stats1.errors_q, stats1.errortime_q);
                else $display("Hint: Output '%s' has no mismatches.", "q");

                $display("Hint: Total mismatched samples is %1d out of %1d samples\\n", stats1.errors, stats1.clocks);
                $display("Simulation finished at %0d ps", $time);
                $display("Mismatches: %1d in %1d samples", stats1.errors, stats1.clocks);
        end

        // Verification: XORs on the right makes any X in good_vector match anything, but X in dut_vector will only match X.
        assign tb_match = ( { q_ref } === ( { q_ref } ^ { q_dut } ^ { q_ref } ) );
        // Use explicit sensitivity list here. @(*) causes NetProc::nex_input() to be called when trying to compute
        // the sensitivity list of the @(strobe) process, which isn't implemented.
        always @(posedge clk, negedge clk) begin

                stats1.clocks++;
                if (!tb_match) begin
                        if (stats1.errors == 0) stats1.errortime = $time;
                        stats1.errors++;
                end
                if (q_ref !== ( q_ref ^ q_dut ^ q_ref ))
                begin if (stats1.errors_q == 0) stats1.errortime_q = $time;
                        stats1.errors_q = stats1.errors_q+1'b1; end

        end
endmodule
"""

    # Create mock completions and verification info
    mock_completions = [
        [{"content": f"```verilog\n{correct_adder}\n```"}],
        [{"content": f"```verilog\n{incorrect_adder}\n```"}]
    ]
    
    mock_verification_info = [
        {"testbench": testbench},
        {"testbench": testbench}
    ]

    mock_names = [
        "correct_code",
        "wrong_code"
    ]
    
    # Call the reward function
    rewards = verilog_code_reward(
        mock_completions, 
        verification_info=mock_verification_info,
        problem_id=mock_names
    )
    
    print("Verilog reward test results:")
    print(f"Correct implementation reward: {rewards[0]}")
    print(f"Incorrect implementation reward: {rewards[1]}")
    
    return rewards


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
    
if __name__ == "__main__":
    test_verilog_reward()