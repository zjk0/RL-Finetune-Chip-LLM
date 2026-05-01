import os
import json
import subprocess
import argparse
import re
import networkx as nx
from tqdm import tqdm

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
    try:
        process = subprocess.run(
            ["bash", "-c", 
                f'cd {code_folder} && export PATH="/root/autodl-tmp/oss-cad-suite/bin:$PATH" && TOP_MODULE={module_name} INPUT_VERILOG={code_folder}/{verilog_code_file} {code_folder}/run_synthesis_ppa.sh'],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if process.returncode != 0:
            print("Error in running synthesis and PPA script:", process.stderr)
            return {"power": -1, "performance": -1, "area": -1}
        
        process = subprocess.run(
            ['cat', f'{code_folder}/ppa_metrics.json'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if process.returncode != 0:
            return {"power": -1, "performance": -1, "area": -1}
        
        ppa_result = json.loads(process.stdout)
        power = ppa_result.get("power", {}).get("total_power_W", 0.0)
        performance = ppa_result.get("performance", {}).get("max_path_delay_ns", 0.0)
        area = ppa_result.get("area", {}).get("design_area_um2", 0.0)
        
        return {"power": power, "performance": performance, "area": area}
    except Exception as e:
        print("Exception occurred during PPA computation:", str(e))
        return {"power": -1, "performance": -1, "area": -1}
    finally:
        subprocess.run(
            ["rm", "-r", code_folder], 
            capture_output = True, 
            text = True, 
            timeout = 5
        )

problem_folder = "/root/autodl-tmp/ChipSeek-R1/benchmark_codev/RTLLM_v2.0_full/origin_problems"
design_name = [
    "accu", "adder_8bit", "adder_16bit", "adder_32bit", "adder_bcd", "adder_pipe_64bit", "alu", 
    "asyn_fifo", "barrel_shifter", "calendar", "clkgenerator", "comparator_3bit", "comparator_4bit", 
    "counter_12", "div_16bit", "edge_detect", "fixed_point_adder", "fixed_point_substractor", "float_multi", 
    "freq_div", "freq_divbyeven", "freq_divbyfrac", "freq_divbyodd", "fsm", "instr_reg", "JC_counter", 
    "LFSR", "LIFObuffer", "multi_8bit", "multi_16bit", "multi_booth_8bit", "multi_pipe_4bit", "multi_pipe_8bit", 
    "parallel2serial", "pe", "pulse_detect", "radix2_div", "RAM", "right_shifter", "ring_counter", "ROM", 
    "sequence_detector", "serial2parallel", "signal_generator", "square_wave", "sub_64bit", "synchronizer",
    "traffic_light", "up_down_counter", "width_8to16"
]

for design in tqdm(design_name):
    if design == "freq_div":
        design_folder = os.path.join(problem_folder, design)
        if os.path.exists(design_folder):    
            ppa_folder = "/root/autodl-tmp/ChipSeek-R1/tests/ppa_test"
            if not os.path.exists(ppa_folder):
                os.makedirs(ppa_folder)
                
            subprocess.run(
                ["cp", os.path.join(design_folder, f"verified_{design}.v"), "/root/autodl-tmp/ChipSeek-R1/src/ppa_script/run_synthesis_ppa.sh", ppa_folder], 
                capture_output = True, 
                text = True,
                timeout = 5
            )
            
            with open(os.path.join(design_folder, f"verified_{design}.v"), "r") as f:
                verilog_code = f.read()
                
            top_module = auto_top(verilog_code)
            ppa_result = ppa_compute(ppa_folder, f"verified_{design}.v", top_module)
            print(ppa_result)
