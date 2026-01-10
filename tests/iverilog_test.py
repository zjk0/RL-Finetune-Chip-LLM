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

def run_iverilog(name, code, testbench):
    unique_id = uuid.uuid4().hex
    encoded_code = base64.b64encode(code.encode()).decode()
    testbench_b64 = base64.b64encode(testbench.encode()).decode()
    ret_val = 0.0
    try: 
        folder_path = f"./iverilog_test/{name}_{unique_id}"
        subprocess.run(
            ['mkdir', folder_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        subprocess.run(
            ['echo', f'{encoded_code} | base64 -d > {folder_path}/design.v'],
            capture_output=True,
            text=True,
            timeout=5
        )
        subprocess.run(
            ['echo', f'{testbench_b64} | base64 -d > {folder_path}/testbench.v'],
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
                ['echo', f'{encoded_code} | base64 -d > {folder_path}/design.v'],
                capture_output=True,
                text=True,
                timeout=5
            )
            subprocess.run(
                ['echo', f'{testbench_b64} | base64 -d > {folder_path}/testbench.v'],
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
    for item in testbench_data:
        if "problem_id" in item and "verification_info" in item and "testbench" in item["verification_info"]:
            testbenches[item["problem_id"]] = item["verification_info"]["testbench"]
    
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
    i = 0
    for problem_id, codes in tqdm(problem_codes.items(), desc="Verifying problems"):
        if problem_id not in testbenches:
            print(f"Warning: No testbench found for problem {problem_id}")
            continue
        testbench = testbenches[problem_id]
        
        problem_results = []
        any_passed = False
        best_solution = None
        for i, code in enumerate(codes):
            if not code.strip():
                result = 0.0
            else:
                result = run_iverilog(f"{problem_id}_{i}", code, testbench)
                
            problem_results.append(result)
            if result == 1.0:
                any_passed = True
        
        results[problem_id] = {
            "individual_results": problem_results,
            "any_passed": any_passed,
            "pass_rate": sum(1 for r in problem_results if r == 1.0) / len(problem_results) if problem_results else 0,
            "best_solution": best_solution
        }
        
        i += 1
    
    # Calculate overall statistics
    total_problems = len(results)
    problems_with_passing_solution = sum(1 for r in results.values() if r["any_passed"])
    
    summary = {
        "total_problems": total_problems,
        "problems_with_passing_solution": problems_with_passing_solution,
        "success_rate": problems_with_passing_solution / total_problems if total_problems > 0 else 0,
        "detailed_results": results
    }
    
    # Save results
    with open(args.output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nVerification completed!")
    print(f"Total problems: {total_problems}")
    print(f"Problems with at least one passing solution: {problems_with_passing_solution}")
    print(f"Success rate: {summary['success_rate']:.2%}")
    print(f"Detailed results saved to {args.output_path}")

if __name__ == "__main__":
    main()