import os
import json
import subprocess
import argparse
import re
import networkx as nx
from tqdm import tqdm
import uuid
import argparse
import numpy as np
import sys
sys.path.append("/root/autodl-tmp/ChipSeek-R1")
from testbench_verify.eval_codev import verify_one_sample
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed

def auto_top(verilog_code):
    instance_graph = nx.DiGraph()
    note_pattern = r"(//[^\n]*|/\*[\s\S]*?\*/)"
    new_code = re.sub(note_pattern, "", verilog_code)
    new_code = re.sub(r"(?:\s*?\n)+", "\n", new_code)
    module_def_pattern = r"(module\s+)([a-zA-Z_][a-zA-Z0-9_\$]*|\\[!-~]+?(?=\s))(\s*\#\s*\([\s\S]*?\))?(\s*(?:\([^;]*\))?\s*;)([\s\S]*?)?(endmodule)"
    module_defs = re.findall(module_def_pattern, new_code, re.DOTALL)
    if not module_defs:
        raise Exception("No module found in auto_top().")
    module_names = [m[1] for m in module_defs]
    instance_graph.add_nodes_from(module_names)
    for mod in module_defs:
        this_mod_name = mod[1]
        this_mod_body = mod[4]
        for submod in module_names:
            if submod != this_mod_name:
                module_instance_pattern = rf"({re.escape(submod)})(\s)(\s*\#\s*\([\s\S]*?\))?([a-zA-Z_][a-zA-Z0-9_\$]*|\\[!-~]+?(?=\s))(\s*(?:\([^;]*\))?\s*;)"
                module_instances = re.findall(
                    module_instance_pattern, this_mod_body, re.DOTALL
                )
                if module_instances:
                    instance_graph.add_edge(this_mod_name, submod)
    instance_tree_size = {}
    for n in instance_graph.nodes:
        if instance_graph.in_degree(n) == 0:
            instance_tree_size[n] = nx.descendants(instance_graph, n)
    top_module = max(instance_tree_size, key=instance_tree_size.get)
    return top_module
        
def ppa_compute(code_folder, verilog_code, log = False):
    id = uuid.uuid4().hex
    task_folder = os.path.join(code_folder, f"{id}")
    os.makedirs(task_folder, exist_ok = True)
    subprocess.run(
        ["cp", "/root/autodl-tmp/ChipSeek-R1/src/ppa_script/run_synthesis_ppa.sh", task_folder], 
        capture_output = True, 
        text = True, 
        timeout = 5
    )
    verilog_code_path = os.path.join(task_folder, "design.v")
    with open(verilog_code_path, "w") as f:
        f.write(verilog_code)
    module_name = auto_top(verilog_code)
    
    try:
        process = subprocess.run(
            ["bash", "-c", 
                f'cd {task_folder} && export PATH="/root/autodl-tmp/oss-cad-suite/bin:$PATH" && TOP_MODULE={module_name} INPUT_VERILOG={verilog_code_path} {task_folder}/run_synthesis_ppa.sh'],
            capture_output = True,
            text = True,
            timeout = 600
        )
        
        if process.returncode != 0:
            print("Error in running synthesis and PPA script:", process.stderr) if log == True else None
            return {"power": -1, "performance": -1, "area": -1, "sysnthesis": False}
        
        process = subprocess.run(
            ["cat", f"{task_folder}/synthesis.log"],
            capture_output = True,
            text = True,
            timeout = 5
        )
        if process.returncode != 0:
            print("Error while reading synthesis.log:", process.stderr) if log == True else None
            return {"power": -1, "performance": -1, "area": -1, "sysnthesis": False}
        
        if "ERROR" in process.stdout:
            print("Synthesis error details:\n", process.stdout) if log == True else None
            return {"power": -1, "performance": -1, "area": -1, "sysnthesis": False}
        else:
            process = subprocess.run(
                ['cat', f'{task_folder}/ppa_metrics.json'],
                capture_output = True,
                text = True,
                timeout = 5
            )
            
            if process.returncode != 0:
                print("Error while reading ppa_metrics.json:", process.stderr) if log == True else None
                return {"power": -1, "performance": -1, "area": -1, "sysnthesis": True}
            
            ppa_result = json.loads(process.stdout)
            power = ppa_result.get("power", {}).get("total_power_W", 0.0)
            performance = ppa_result.get("performance", {}).get("max_path_delay_ns", 0.0)
            area = ppa_result.get("area", {}).get("design_area_um2", 0.0)
            
            return {"power": power, "performance": performance, "area": area, "sysnthesis": True}
    except Exception as e:
        print("Error:", str(e)) if log == True else None
        return {"power": -1, "performance": -1, "area": -1, "sysnthesis": False}
    finally:
        subprocess.run(
            ["rm", "-r", task_folder],
            capture_output = True,
            text = True,
            timeout = 5
        )
        
def compute_score(completions_info):
    score_list = [0.0] * len(completions_info["info"])
    
    ppa_folder = "/root/autodl-tmp/ChipSeek-R1/benchmark_eval/ppa_eval"
    os.makedirs(ppa_folder, exist_ok = True)
    
    verilog_code_list = []        
    for i, info in enumerate(completions_info["info"]):
        verilog_code_list.append(info["code"])
        if info["syntax"] == 1 and info["func"] == 1:
            score_list[i] += 1.0
        elif info["syntax"] == 1 and info["func"] != 1:
            score_list[i] += 0.2
        else:
            score_list[i] = 0.0
    
    with ThreadPoolExecutor(max_workers = 10) as executor:
        futures = {
            executor.submit(ppa_compute, ppa_folder, verilog_code): i 
            for i, verilog_code in enumerate(verilog_code_list) 
            if score_list[i] == 1.0
        }
        reference_ppa = completions_info["reference_ppa"]
        for future in as_completed(futures):
            i = futures[future]
            ppa_result = future.result()
            if ppa_result["sysnthesis"] == True:
                score_list[i] += 0.4
                if ppa_result["power"] != -1 and ppa_result["performance"] != -1 and ppa_result["area"] != -1:
                    if reference_ppa["power"] * reference_ppa["performance"] * reference_ppa["area"] == 0:
                        score_list[i] += 0.1
                    elif reference_ppa["power"] * reference_ppa["performance"] * reference_ppa["area"] > 0:
                        if ppa_result["power"] * ppa_result["performance"] * ppa_result["area"] != 0:
                            power_ratio = reference_ppa["power"] / ppa_result["power"]
                            performance_ratio = reference_ppa["performance"] / ppa_result["performance"]
                            area_ratio = reference_ppa["area"] / ppa_result["area"]
                            value = power_ratio * performance_ratio * area_ratio
                            value_geo_mean = value ** (1 / 3)
                            score_list[i] += max(0.01, min(value_geo_mean - 1.0, 0.6))
                    else:
                        score_list[i] += 1.0
                                
    return score_list
        
def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--completions_info_path", type = str, default = None, required = True)
    parser.add_argument("--output_path", type = str, default = "output.json")
    
    return parser.parse_args()

def change_format(obj):
    with open("/root/autodl-tmp/ChipSeek-R1/eval_output/ppa_eval/rtllm_v2_0.json", "r") as f:
        reference_list = json.load(f)
    
    result = []
    for i, info in enumerate(obj):
        if i < 50:
            for reference in reference_list:
                if reference["top_module"] == info["task_id"]:
                    reference_ppa = reference["ppa"]
                    break
            
            result.append({
                "task_id": info["task_id"], 
                "reference_ppa": reference_ppa,
                "info": []
            })
        
        result[i % 50]["info"].append({
            "code": info["code"], 
            "syntax": info["syntax"], 
            "func": info["semantic"],
        })
        
    return result

def main():
    args = parse_args()
    
    with open(args.completions_info_path, "r") as f:
        completions_info_list = [json.loads(line.strip()) for line in f]
    
    completions_info_list = change_format(completions_info_list)
    
    name_and_score = []
    score_list = []
    for completions_info in tqdm(completions_info_list):
        completions_score_list = compute_score(completions_info)
        completions_score = np.mean(completions_score_list)
        # completions_score = max(completions_score_list)
        name_and_score.append({
            "task_id": completions_info["task_id"], 
            "score": completions_score
        })
        score_list.append(completions_score)
        
    final_score = np.mean(score_list)
    score_info = [{
        "score": final_score, 
        "detail": name_and_score
    }]
        
    with open(args.output_path, "w") as f:
        json.dump(score_info, f, indent = 4)
    
if __name__ == "__main__":
    main()