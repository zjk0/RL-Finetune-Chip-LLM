import subprocess
import base64
import uuid
import re
import json
from tqdm import tqdm

def run_iverilog(name, code, testbench):
    unique_id = uuid.uuid4().hex
    encoded_code = base64.b64encode(code.encode()).decode()
    testbench_b64 = base64.b64encode(testbench.encode()).decode()
    ret_val = 0.0
    try: 
        folder_path = f"/code_test/{name}_{unique_id}"
        subprocess.run(
            ["docker", "exec", "verilog-eval", "bash", "-c", f'mkdir {folder_path}'],
            capture_output=True,
            text=True,
            timeout=5
        )

        subprocess.run(
            ["docker", "exec", "verilog-eval", "bash", "-c", f'echo "{encoded_code}" | base64 -d > {folder_path}/design.v'],
            capture_output=True,
            text=True,
            timeout=5
        )
        subprocess.run(
            ["docker", "exec", "verilog-eval", "bash", "-c", f"echo '{testbench_b64}' | base64 -d > {folder_path}/testbench.v"],
            capture_output=True,
            text=True,
            timeout=5
        )
        compile_process = subprocess.run(
            ["docker", "exec", "verilog-eval", "bash", "-c", 
                f'iverilog -Wall -Winfloop -Wno-timescale -g2012 -o {folder_path}/a.out {folder_path}/design.v {folder_path}/testbench.v'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if compile_process.returncode == 0:   
            sim_process = subprocess.run(
                ["docker", "exec", "verilog-eval", "bash", "-c", f'vvp {folder_path}/a.out'],
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
                ["docker", "exec", "iverilog", "bash", "-c", f'mkdir {folder_path}'],
                capture_output=True,
                text=True,
                timeout=5
            )

            subprocess.run(
                ["docker", "exec", "iverilog", "bash", "-c", f'echo "{encoded_code}" | base64 -d > {folder_path}/design.v'],
                capture_output=True,
                text=True,
                timeout=5
            )
            subprocess.run(
                ["docker", "exec", "iverilog", "bash", "-c", f"echo '{testbench_b64}' | base64 -d > {folder_path}/testbench.v"],
                capture_output=True,
                text=True,
                timeout=5
            )
            compile_process_1 = subprocess.run(
                ["docker", "exec", "iverilog", "bash", "-c", 
                    f'iverilog -o {folder_path}/a.out {folder_path}/design.v {folder_path}/testbench.v'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if compile_process_1.returncode == 0:   
                sim_process = subprocess.run(
                    ["docker", "exec", "iverilog", "bash", "-c", f'vvp {folder_path}/a.out'],
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
        return 0.0
    finally:
        try:
            subprocess.run(
                ["docker", "exec", "verilog-eval", "bash", "-c", f'rm -rf {folder_path}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            subprocess.run(
                ["docker", "exec", "iverilog", "bash", "-c", f'rm -rf {folder_path}'],
                capture_output=True,
                text=True,
                timeout=5
            )
        except:
            pass

def test_verilog_code():
    with open('/public/data/verilog_reasoning_data_grpo_ppa.json', 'r') as file:
        data = json.load(file)
    
    pass_count = 0
    fail_count = 0
    top_module_fail_count = 0
    failed_problems = []

    for sample in tqdm(data):
        name = sample["problem_id"]
        code = sample["gold_standard_solution"]
        testbench = sample["verification_info"]["testbench"]
        result = run_iverilog(name, code, testbench)
        if result == 1.0:
            pass_count += 1
        else:
            fail_count += 1
            failed_problems.append(name)
            print(f"Test {name}: Fail")
            if sample["verification_info"]["top_module"] == "top_module":
                top_module_fail_count += 1

    with open('failed_problems.txt', 'w') as fail_file:
        for problem_id in failed_problems:
            fail_file.write(f"{problem_id}\n")

    print(f"Total Pass: {pass_count}")
    print(f"Total Fail: {fail_count}")
    print(f"top module fail: {top_module_fail_count}")

test_verilog_code()
