import pyarrow.parquet as pq
import subprocess
import os
import re
import networkx as nx
from openai import OpenAI
import json

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

def ppa_compute(code_folder, verilog_code_file, module_name):
    subprocess.run(
        ["cp", "/root/autodl-tmp/ChipSeek-R1/src/ppa_script/run_synthesis_ppa.sh", code_folder],
        capture_output = True,
        text = True,
        timeout = 5
    )
    
    try:
        process = subprocess.run(
            ["bash", "-c", 
                f'cd {code_folder} && export PATH="/root/autodl-tmp/oss-cad-suite/bin:$PATH" && TOP_MODULE={module_name} INPUT_VERILOG={code_folder}/{verilog_code_file} {code_folder}/run_synthesis_ppa.sh'],
            capture_output = True,
            text = True,
            timeout = 60
        )
        
        if process.returncode != 0:
            print("Error in running synthesis and PPA script:", process.stderr)
            return {"power": -1, "performance": -1, "area": -1}
        
        process = subprocess.run(
            ['cat', f'{code_folder}/ppa_metrics.json'],
            capture_output = True,
            text = True,
            timeout = 5
        )
        
        if process.returncode != 0:
            return {"power": -1, "performance": -1, "area": -1}
        
        ppa_result = json.loads(process.stdout)
        power = ppa_result.get("power", {}).get("total_power_W", 0.0)
        performance = ppa_result.get("performance", {}).get("max_path_delay_ns", 0.0)
        area = ppa_result.get("area", {}).get("design_area_um2", 0.0)
        
        return {"power": power, "performance": performance, "area": area}
    except Exception as e:
        return {"power": -1, "performance": -1, "area": -1}
    finally:
        subprocess.run(
            ["rm", "-r", code_folder],
            capture_output = True,
            text = True,
            timeout = 5
        )
    
path = "/root/autodl-tmp/ChipSeek-R1/data/codev_r1_rl_train.parquet"
dataset = pq.read_table(path).to_pylist()

index = 90
top_module = auto_top(dataset[index]["ground_truth"][0]["content"])
ppa_folder = "/root/autodl-tmp/ChipSeek-R1/tests/ppa"
ground_truth_file = "ground_truth.v"
ground_truth_path = f"{ppa_folder}/{ground_truth_file}"
os.makedirs(ppa_folder, exist_ok=True)
with open(ground_truth_path, "w") as f:
    f.write(dataset[index]["ground_truth"][0]["content"])
ppa_result = ppa_compute(ppa_folder, ground_truth_file, top_module)
print(ppa_result)