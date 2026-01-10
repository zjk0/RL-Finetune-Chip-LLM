import base64
import subprocess
import json

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
        
        print(process.stdout)
        
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
        
verilog_code = '''
module comparator_3bit(
    input [2:0] A,
    input [2:0] B,
    output reg [1:0] A_greater,
    output reg [1:0] A_equal,
    output reg [1:0] A_less
);

always @(*) begin
    if (A > B) begin
        A_greater = 1'b1;
    end else if (A == B) begin
        A_greater = 1'b0;
        A_equal = 1'b1;
    end else begin
        A_greater = 1'b0;
        A_equal = 1'b0;
        A_less = 1'b1;
    end
end

endmodule
'''

# verilog_code = '''
# module comparator_3bit (
#     input [2:0] A,
#     input [2:0] B,
#     output A_greater,
#     output A_equal,
#     output A_less
# );

#     assign A_greater = (A > B) ? 1'b1 : 1'b0;
#     assign A_equal = (A == B) ? 1'b1 : 1'b0;
#     assign A_less = (A < B) ? 1'b1 : 1'b0;

# endmodule
# '''

ppa_metrics = {
    "power": {
        "report": "Power analysis completed successfully with NanGate 45nm library",
        "total_power_W": 5.26e-06,
        "internal_power_W": 2.98e-06,
        "switching_power_W": 1.99e-06,
        "leakage_power_W": 3e-07,
        "details": "See power_report.txt for full details"
    },
    "area": {
        "design_area_um2": 11.704,
        "technology": "NanGate 45nm",
        "total_cells": 13,
        "note": "Combination of Yosys synthesis and OpenROAD analysis"
    },
    "performance": {
        "design_type": "Combinational logic",
        "max_path_delay_ns": 0.1,
        "clock_period_ns": -1,
        "timing_met": False
    }
}

output = run_synthesis_ppa("test", verilog_code, "comparator_3bit", ppa_metrics)
print(output)