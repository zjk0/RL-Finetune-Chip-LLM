import argparse
import json
import os
import re
import uuid
import base64
import subprocess
from tqdm import tqdm

def load_json(filename):
    if filename.endswith('.jsonl'):
        data = []
        with open(filename, 'r') as f:
            for line in f:
                data.append(json.loads(line))
        return data
    else:
        with open(filename, 'r') as f:
            return json.load(f)
        
# def run_synthesis_ppa(name, code, top_module, gold_ppa_metrics):

#     try:        
#         # Create a folder with the name
#         folder_path = f"/root/{name}"
#         subprocess.run(
#             ["docker", "exec", "eda_env", "bash", "-c", f'mkdir -p {folder_path}'],
#             capture_output=True,
#             text=True,
#             timeout=5
#         )
#         encoded_code = base64.b64encode(code.encode()).decode()
#         # Copy the design code to the folder
#         subprocess.run(
#             ["docker", "exec", "eda_env", "bash", "-c", f'echo "{encoded_code}" | base64 -d > {folder_path}/design.v'],
#             capture_output=True,
#             text=True,
#             timeout=5
#         )
        
#         # Copy the run_synthesis_ppa.sh script to the folder
#         subprocess.run(
#             ["docker", "exec", "eda_env", "bash", "-c", f'cp /root/ppa_scripts/run_synthesis_ppa.sh {folder_path}/'],
#             capture_output=True,
#             text=True,
#             timeout=5
#         )
        
#         # Run the synthesis and PPA analysis script inside the Docker container in the new folder
#         process = subprocess.run(
#             ["docker", "exec", "eda_env", "bash", "-c", 
#                 f'cd {folder_path} && export PATH="/root/oss-cad-suite/bin:$PATH" && TOP_MODULE={top_module} INPUT_VERILOG={folder_path}/design.v {folder_path}/run_synthesis_ppa.sh'],
#             capture_output=True,
#             text=True,
#             timeout=60
#         )
        
#         if process.returncode != 0:
#             return 0.0, None  # Error in execution

#         # Get the content from the PPA metrics JSON file
#         ppa_metrics_process = subprocess.run(
#             ["docker", "exec", "eda_env", "bash", "-c", f'cat {folder_path}/ppa_metrics.json'],
#             capture_output=True,
#             text=True,
#             timeout=5
#         )
        

        
#         if ppa_metrics_process.returncode != 0:
#             return 0.0, None  # Error in execution

#         # Parse the PPA JSON output
#         ppa_metrics = json.loads(ppa_metrics_process.stdout)
#         # Example: Use total power as a reward metric
#         total_power = ppa_metrics.get("power", {}).get("total_power_W", 0.0)
#         total_area = ppa_metrics.get("area", {}).get("design_area_um2", 0.0)
#         total_delay = ppa_metrics.get("performance", {}).get("max_path_delay_ns", 0.0)

#         if gold_ppa_metrics == None:
#             if total_power > 0 and total_area > 0 and total_delay >= 0:
#                 return 0.1, ppa_metrics
#             else:
#                 return 0.0, None
#         else:
#             gold_power = gold_ppa_metrics.get("power", {}).get("total_power_W", 0.0)
#             gold_area = gold_ppa_metrics.get("area", {}).get("design_area_um2", 0.0)
#             gold_delay = gold_ppa_metrics.get("performance", {}).get("max_path_delay_ns", 0.0)

#             if gold_power > 0 and gold_area > 0 and gold_delay >= 0:
#                 if total_power > 0 and total_area > 0 and total_delay >= 0:
#                     if gold_power * gold_area * gold_delay == 0 or total_power * total_area * total_delay == 0:
#                         return 0.1, ppa_metrics
#                     else:
#                         ratio = (gold_power/total_power) * (gold_area/total_area) * (gold_delay/total_delay)
#                         # Clamp the ratio between 0.5 and 3.0
#                         ratio = max(0.1, ratio)
#                         return ratio, ppa_metrics
#                 else:
#                     return 0.0, None
#             else:
#                 if total_power > 0 and total_area > 0 and total_delay >= 0:
#                     return 0.1, ppa_metrics
#                 else:
#                     return 0.0, None

#     except Exception as e:
#         return 0.0, None
#     finally:
#         # Clean up temporary files
#         try:
#             subprocess.run(
#                 ["docker", "exec", "eda_env", "bash", "-c", f'rm -rf {folder_path}'],
#                 timeout=5,
#                 capture_output=True
#             )
#         except:
#             pass

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
            return 0.0, None  # Error in execution

        # Get the content from the PPA metrics JSON file
        ppa_metrics_process = subprocess.run(
            ['cat', f'{folder_path}/ppa_metrics.json'],
            capture_output=True,
            text=True,
            timeout=5
        )
        

        
        if ppa_metrics_process.returncode != 0:
            return 0.0, None  # Error in execution

        # Parse the PPA JSON output
        ppa_metrics = json.loads(ppa_metrics_process.stdout)
        # Example: Use total power as a reward metric
        total_power = ppa_metrics.get("power", {}).get("total_power_W", 0.0)
        total_area = ppa_metrics.get("area", {}).get("design_area_um2", 0.0)
        total_delay = ppa_metrics.get("performance", {}).get("max_path_delay_ns", 0.0)

        if gold_ppa_metrics == None:
            if total_power > 0 and total_area > 0 and total_delay >= 0:
                return 0.1, ppa_metrics
            else:
                return 0.0, None
        else:
            gold_power = gold_ppa_metrics.get("power", {}).get("total_power_W", 0.0)
            gold_area = gold_ppa_metrics.get("area", {}).get("design_area_um2", 0.0)
            gold_delay = gold_ppa_metrics.get("performance", {}).get("max_path_delay_ns", 0.0)

            if gold_power > 0 and gold_area > 0 and gold_delay >= 0:
                if total_power > 0 and total_area > 0 and total_delay >= 0:
                    if gold_power * gold_area * gold_delay == 0 or total_power * total_area * total_delay == 0:
                        return 0.1, ppa_metrics
                    else:
                        ratio = (gold_power/total_power) * (gold_area/total_area) * (gold_delay/total_delay)
                        # Clamp the ratio between 0.5 and 3.0
                        ratio = max(0.1, ratio)
                        return ratio, ppa_metrics
                else:
                    return 0.0, None
            else:
                if total_power > 0 and total_area > 0 and total_delay >= 0:
                    return 0.1, ppa_metrics
                else:
                    return 0.0, None

    except Exception as e:
        return 0.0, None
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

# def run_iverilog(name, code, testbench):
#     unique_id = uuid.uuid4().hex
#     encoded_code = base64.b64encode(code.encode()).decode()
#     testbench_b64 = base64.b64encode(testbench.encode()).decode()
#     ret_val = 0.0
#     try: 
#         folder_path = f"/code_test/{name}_{unique_id}"
#         subprocess.run(
#             ["docker", "exec", "iverilog", "bash", "-c", f'mkdir {folder_path}'],
#             capture_output=True,
#             text=True,
#             timeout=5
#         )

#         subprocess.run(
#             ["docker", "exec", "iverilog", "bash", "-c", f'echo "{encoded_code}" | base64 -d > {folder_path}/design.v'],
#             capture_output=True,
#             text=True,
#             timeout=5
#         )
#         subprocess.run(
#             ["docker", "exec", "iverilog", "bash", "-c", f"echo '{testbench_b64}' | base64 -d > {folder_path}/testbench.v"],
#             capture_output=True,
#             text=True,
#             timeout=5
#         )
#         compile_process = subprocess.run(
#             ["docker", "exec", "iverilog", "bash", "-c", 
#                 f'iverilog -o {folder_path}/a.out {folder_path}/design.v {folder_path}/testbench.v'],
#             capture_output=True,
#             text=True,
#             timeout=5
#         )
#         if compile_process.returncode == 0:   
#             sim_process = subprocess.run(
#                 ["docker", "exec", "iverilog", "bash", "-c", f'vvp {folder_path}/a.out'],
#                 capture_output=True,
#                 text=True,
#                 timeout=30
#             )

#             if sim_process.returncode == 0:
#                 if "pass" in sim_process.stdout.lower():
#                     ret_val = 1.0
#                 else:
#                     match = re.search(r'Mismatches: ([0-9]*) in ([0-9]*) samples', sim_process.stdout)
#                     if match:
#                         cor, tot = [int(i) for i in match.groups()]
#                         if cor == 0:
#                             ret_val = 1.0
#         if ret_val == 0.0:
#             subprocess.run(
#                 ["docker", "exec", "verilog-eval", "bash", "-c", f'mkdir {folder_path}'],
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )

#             subprocess.run(
#                 ["docker", "exec", "verilog-eval", "bash", "-c", f'echo "{encoded_code}" | base64 -d > {folder_path}/design.v'],
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )
#             subprocess.run(
#                 ["docker", "exec", "verilog-eval", "bash", "-c", f"echo '{testbench_b64}' | base64 -d > {folder_path}/testbench.v"],
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )
#             compile_process_1 = subprocess.run(
#                 ["docker", "exec", "verilog-eval", "bash", "-c", 
#                     f'iverilog -Wall -Winfloop -Wno-timescale -g2012 -o {folder_path}/a.out {folder_path}/design.v {folder_path}/testbench.v'],
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )
#             if compile_process_1.returncode == 0:   
#                 sim_process = subprocess.run(
#                     ["docker", "exec", "verilog-eval", "bash", "-c", f'vvp {folder_path}/a.out'],
#                     capture_output=True,
#                     text=True,
#                     timeout=30
#                 )

#                 if sim_process.returncode == 0:
#                     if "pass" in sim_process.stdout.lower():
#                         ret_val = 1.0
#                     else:
#                         match = re.search(r'Mismatches: ([0-9]*) in ([0-9]*) samples', sim_process.stdout)
#                         if match:
#                             cor, tot = [int(i) for i in match.groups()]
#                             if cor == 0:
#                                 ret_val = 1.0 
#         if ret_val == 0.0 and (compile_process.returncode == 0 or compile_process_1.returncode == 0):
#             ret_val = 0.2
#         return ret_val
#     except Exception as e:
#         print(f"Error running iverilog for {name}: {str(e)}")
#         return 0.0
#     finally:
#         try:
#             subprocess.run(
#                 ["docker", "exec", "verilog-eval", "bash", "-c", f'rm -rf {folder_path}'],
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )
#             subprocess.run(
#                 ["docker", "exec", "iverilog", "bash", "-c", f'rm -rf {folder_path}'],
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )
#         except:
#             pass

def run_iverilog(name, code, testbench):
    unique_id = uuid.uuid4().hex
    encoded_code = base64.b64encode(code.encode()).decode()
    testbench_b64 = base64.b64encode(testbench.encode()).decode()
    ret_val = 0.0
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
            ['iverilog', '-o', f'{folder_path}/a.out', f'{folder_path}/design.v', f'{folder_path}/testbench.v'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if compile_process.returncode == 0:   
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
                ['iverilog', '-Wall', '-Winfloop', '-Wno-timescale', '-g2012', '-o', f'{folder_path}/a.out', f'{folder_path}/design.v', f'{folder_path}/testbench.v'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if compile_process_1.returncode == 0:   
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
        if ret_val == 0.0 and (compile_process.returncode == 0 or compile_process_1.returncode == 0):
            ret_val = 0.2
        return ret_val
    except Exception as e:
        print(f"Error running iverilog for {name}: {str(e)}")
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

def main():
    parser = argparse.ArgumentParser(description='Verify RTLLM generated code.')
    parser.add_argument('--generated_code_path', type=str, default="generated_code/rtllm_checkpoint-2300_vllm.jsonl",
                        help='Path to the generated code jsonl file')
    parser.add_argument('--testbench_path', type=str, default="/public_extends/data/verilog_designs_data_ppa.json",
                        help='Path to the testbench json file')
    parser.add_argument('--output_path', type=str, default="verification_results.json",
                        help='Path to save verification results')
    args = parser.parse_args()

    # Load generated code
    print(f"Loading generated code from {args.generated_code_path}")
    generated_code = load_json(args.generated_code_path)
    
    # Load testbenches
    print(f"Loading testbenches from {args.testbench_path}")
    testbench_data = load_json(args.testbench_path)
    
    # Create a dictionary of testbenches indexed by problem_id
    testbenches = {}
    top_modules = {}
    ppa_metrics = {}
    for item in testbench_data:
        if "problem_id" in item and "verification_info" in item and "testbench" in item["verification_info"]:
            testbenches[item["problem_id"]] = item["verification_info"]["testbench"]
            if "top_module" in item["verification_info"]:
                top_modules[item["problem_id"]] = item["verification_info"]["top_module"]
            if "ppa_metrics" in item:
                ppa_metrics[item["problem_id"]] = item["ppa_metrics"]
    
    print(f"Found {len(testbenches)} testbenches")
    
    # Group generated code by problem_id
    problem_codes = {}
    for entry in generated_code:
        problem_id = entry.get("problem_id")
        if problem_id not in problem_codes:
            problem_codes[problem_id] = []
        problem_codes[problem_id].append(entry.get("completion", ""))
    
    print(f"Found {len(problem_codes)} unique problems with generated code")
    
    # Verify each problem
    results = {}
    highest_ppa_scores = []
    i = 0
    for problem_id, codes in tqdm(problem_codes.items(), desc="Verifying problems"):
        if problem_id not in testbenches:
            print(f"Warning: No testbench found for problem {problem_id}")
            continue
        testbench = testbenches[problem_id]
        top_module = top_modules.get(problem_id, None)
        gold_ppa_metric = ppa_metrics.get(problem_id, None)
        
        problem_results = []
        ppa_results = []
        any_passed = False
        highest_ppa = 0.0
        highest_ppa_metrics = None
        best_solution = None
        for i, code in enumerate(codes):
            if not code.strip():
                result = 0.0
                ppa_result = 0.0
            else:
                result = run_iverilog(f"{problem_id}_{i}", code, testbench)
                
                # If iverilog passes, run synthesis PPA
                if result == 1.0 and top_module:
                    ppa_result, ppa = run_synthesis_ppa(f"{problem_id}_{i}", code, top_module, gold_ppa_metric)
                    ppa_results.append(ppa_result)
                    if highest_ppa < ppa_result:
                        highest_ppa = ppa_result
                        highest_ppa_metrics = ppa
                        best_solution = code
                else:
                    ppa_result = 0.0
                
            problem_results.append(result)
            if result == 1.0:
                any_passed = True
        
        results[problem_id] = {
            "individual_results": problem_results,
            "any_passed": any_passed,
            "pass_rate": sum(1 for r in problem_results if r == 1.0) / len(problem_results) if problem_results else 0,
            "ppa_results": ppa_results,
            "highest_ppa": highest_ppa,
            "highest_ppa_metrics": highest_ppa_metrics,
            "best_solution": best_solution
        }
        
        # Only add to highest_ppa_scores if any solution passed and has a valid PPA score
        if any_passed and highest_ppa > 0:
            highest_ppa_scores.append(highest_ppa)
        i += 1
    
    # Calculate overall statistics
    total_problems = len(results)
    problems_with_passing_solution = sum(1 for r in results.values() if r["any_passed"])
    avg_highest_ppa_score = sum(highest_ppa_scores) / len(highest_ppa_scores) if highest_ppa_scores else 0.0
    
    summary = {
        "total_problems": total_problems,
        "problems_with_passing_solution": problems_with_passing_solution,
        "success_rate": problems_with_passing_solution / total_problems if total_problems > 0 else 0,
        "average_highest_ppa_score": avg_highest_ppa_score,
        "problems_with_ppa_scores": len(highest_ppa_scores),
        "detailed_results": results
    }
    
    # Save results
    with open(args.output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nVerification completed!")
    print(f"Total problems: {total_problems}")
    print(f"Problems with at least one passing solution: {problems_with_passing_solution}")
    print(f"Success rate: {summary['success_rate']:.2%}")
    print(f"Average highest PPA score: {avg_highest_ppa_score:.2f} (from {len(highest_ppa_scores)} problems)")
    print(f"Detailed results saved to {args.output_path}")

if __name__ == "__main__":
    main()
