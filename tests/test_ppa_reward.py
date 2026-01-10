import json
import tempfile
import subprocess
import os
import re
import base64
def extract_verilog(completion: str) -> str:
    pattern = re.compile(r"```verilog\n(.*?)```", re.DOTALL)
    matches = pattern.findall(completion)
    extracted_answer = matches[-1] if len(matches) >= 1 else ""
    return extracted_answer

def verilog_ppa_reward(completions, **kwargs) -> list[float]:
    """Reward function that evaluates Verilog code snippets for Power, Performance, and Area (PPA) using a Docker container.

    Assumes the dataset contains a `verification_info` column with testbenches and top module information.
    """
    rewards = []
    
    def run_synthesis_ppa(name, code, top_module, gold_ppa_metrics):
        try:
            encoded_code = base64.b64encode(code.encode()).decode()
            # Create a folder with the name
            folder_path = f"/root/autodl-tmp/ChipSeek-R1/ppa_test/{name}"
            subprocess.run(
                ['mkdir', '-p', folder_path],
                capture_output=True,
                text=True,
                timeout=1
            )
            
            # Copy the design code to the folder
            process = subprocess.run(
                ['bash', '-c', f'echo {encoded_code} | base64 -d > {folder_path}/design.v'],
                capture_output=True,
                text=True,
                timeout=1
            )
            
            # Copy the run_synthesis_ppa.sh script to the folder
            subprocess.run(
                ['cp', '/root/autodl-tmp/ChipSeek-R1/src/ppa_script/run_synthesis_ppa.sh', folder_path],
                capture_output=True,
                text=True,
                timeout=1
            )
            
            # Run the synthesis and PPA analysis script inside the Docker container in the new folder
            process = subprocess.run(
                ["bash", "-c", 
                f'cd {folder_path} && export PATH="/root/autodl-tmp/oss-cad-suite/bin:$PATH" && TOP_MODULE={top_module} INPUT_VERILOG={folder_path}/design.v {folder_path}/run_synthesis_ppa.sh'],
                capture_output=True,
                text=True,
                timeout=60
            )

            
            # Get the content from the PPA metrics JSON file
            ppa_metrics_process = subprocess.run(
                ['cat', f'{folder_path}/ppa_metrics.json'],
                capture_output=True,
                text=True,
                timeout=1
            )
            
            # Use the output from the ppa_metrics.json file
            process = ppa_metrics_process

            if process.returncode != 0:
                return 0.0  # Error in execution

            # Parse the PPA JSON output
            ppa_metrics = json.loads(process.stdout)
            # Example: Use total power as a reward metric
            total_power = ppa_metrics.get("power", {}).get("total_power_W", 0.0)
            total_area = ppa_metrics.get("area", {}).get("design_area_um2", 0.0)
            total_delay = ppa_metrics.get("performance", {}).get("max_path_delay_ns", 0.0)
            print(total_power, total_delay, total_area)
            
            # Remove the folder after execution
            subprocess.run(
                ['rm', '-rf', folder_path],
                capture_output=True,
                text=True,
                timeout=60
            )

            if gold_ppa_metrics == None:
                if total_power > 0 and total_area > 0 and total_delay >= 0:
                    return 1.0
                else:
                    return 0.0
            else:
                gold_power = gold_ppa_metrics.get("power", {}).get("total_power_W", 0.0)
                gold_area = gold_ppa_metrics.get("area", {}).get("design_area_um2", 0.0)
                gold_delay = gold_ppa_metrics.get("performance", {}).get("max_path_delay_ns", 0.0)

                if gold_power > 0 and gold_area > 0 and gold_delay >= 0:
                    if total_power > 0 and total_area > 0 and total_delay >= 0:
                        if gold_power * gold_area * gold_delay == 0 or total_power * total_area * total_delay == 0:
                            return 1.0
                        else:
                            ratio = (gold_power * gold_area * gold_delay)**(1/3) / (total_power * total_area * total_delay)**(1/3)
                            # Clamp the ratio between 0.5 and 3.0
                            ratio = max(0.01, min(3.0, ratio))
                            return 1.0 + ratio
                    else:
                        return 0.0
                else:
                    if total_power > 0 and total_area > 0 and total_delay >= 0:
                        return 1.0
                    else:
                        return 0.0

        except Exception as e:
            return 0.0

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

def test_ppa_reward():
    """Test the verilog_ppa_reward function with a simple 8-bit adder example and a FSM control circuit example."""
    # Correct 8-bit adder implementation
    correct_adder = """
module DFF_RST_SET (
    input D,
    input C,
    input R,
    input S,
    output reg Q
);

always @(posedge C) begin
    // Handle synchronous set first
    if (S)
        Q <= 1;
    // Handle async reset next
    else if (R)
        Q <= 0;
    // If neither set nor reset, update Q based on the clock edge
    else
        Q <= D;
end

endmodule

"""

    # Incorrect 8-bit adder implementation (missing carry bit)
    incorrect_adder = """
module DFF_RST_SET (
    input D,
    input C,
    input R,
    input S,
    output reg Q
);

reg D_prev;

always @(posedge C) begin
    if (R) begin
        Q <= 0;  // Asynchronous reset when R is high
    end else if (S) begin
        Q <= 1;  // Synchronous set when S is high
    end else begin
        Q <= D;  // Normal operation, Q follows D
    end
end

always @(*) begin
    D_prev = D;  // Capture the current value of D
end

endmodule

"""

    # Correct FSM control circuit implementation
    correct_fsm = """
module DFF_RST_SET (
    input D,
    input C,
    input R,
    input S,
    output reg Q
);

always @(posedge C or posedge R or posedge S) begin
    if (R) begin
        Q <= 0;  // Asynchronous reset
    end else if (S) begin
        Q <= 1;  // Synchronous set
    end else begin
        Q <= D;  // Capture D value when clock is high
    end
end

endmodule

"""

    # Incorrect FSM control circuit implementation (incorrect state transitions)
    incorrect_fsm = """
module fsm_control(
    input clk,
    input reset,
    input in,
    output reg out
);
    reg [1:0] state, next_state;
    parameter S0 = 2'b00, S1 = 2'b01, S2 = 2'b10;

    always @(posedge clk or posedge reset) begin
        if (reset)
            state <= S0;
        else
            state <= next_state;
    end

    always @(*) begin
        case (state)
            S0: if (in) next_state = S2; else next_state = S0;  // Incorrect transition
            S1: if (in) next_state = S0; else next_state = S0;  // Incorrect transition
            S2: if (in) next_state = S1; else next_state = S1;  // Incorrect transition
            default: next_state = S0;
        endcase
    end

    always @(*) begin
        case (state)
            S0: out = 0;
            S1: out = 1;
            S2: out = 0;
            default: out = 0;
        endcase
    end
endmodule
"""

    # Create mock completions and verification info
    mock_completions = [
        [{"content": f"```verilog\n{correct_adder}\n```"}],
        [{"content": f"```verilog\n{incorrect_adder}\n```"}],
        [{"content": f"```verilog\n{correct_fsm}\n```"}],
        [{"content": f"```verilog\n{incorrect_fsm}\n```"}]
    ]
    
    mock_verification_info = [
        {"top_module": "DFF_RST_SET"},
        {"top_module": "DFF_RST_SET"},
        {"top_module": "DFF_RST_SET"},
        {"top_module": "fsm_control"}
    ]

    mock_problem_id = ["adder_8bit_1", "adder_8bit_2", "fsm_control_1", "fsm_control_2"]
    
    gold_ppa_metrics = [{
  "power": {
    "report": "Power analysis completed successfully with NanGate 45nm library",
    "total_power_W": 3.37e-07,
    "internal_power_W": 3.02e-06,
    "switching_power_W": 1.64e-06,
    "leakage_power_W": 3.37e-07,
    "details": "See power_report.txt for full details"
  },
  "area": {
    "design_area_um2": 13.034000,
    "technology": "NanGate 45nm",
    "total_cells": 15,
    "note": "Combination of Yosys synthesis and OpenROAD analysis"
  },
  "performance": {
    "design_type": "Combinational logic",
    "max_path_delay_ns": 0.06,
    "clock_period_ns": -1,
    "timing_met": False
  }
},
{
  "power": {
    "report": "Power analysis completed successfully with NanGate 45nm library",
    "total_power_W": 3.37e-07,
    "internal_power_W": 3.02e-06,
    "switching_power_W": 1.64e-06,
    "leakage_power_W": 3.37e-07,
    "details": "See power_report.txt for full details"
  },
  "area": {
    "design_area_um2": 13.034000,
    "technology": "NanGate 45nm",
    "total_cells": 15,
    "note": "Combination of Yosys synthesis and OpenROAD analysis"
  },
  "performance": {
    "design_type": "Combinational logic",
    "max_path_delay_ns": 0.06,
    "clock_period_ns": -1,
    "timing_met": False
  }
},
{
  "power": {
    "report": "Power analysis completed successfully with NanGate 45nm library",
    "total_power_W": 3.37e-07,
    "internal_power_W": 3.02e-06,
    "switching_power_W": 1.64e-06,
    "leakage_power_W": 3.37e-07,
    "details": "See power_report.txt for full details"
  },
  "area": {
    "design_area_um2": 13.034000,
    "technology": "NanGate 45nm",
    "total_cells": 15,
    "note": "Combination of Yosys synthesis and OpenROAD analysis"
  },
  "performance": {
    "design_type": "Combinational logic",
    "max_path_delay_ns": 0.06,
    "clock_period_ns": -1,
    "timing_met": False
  }
},
{
  "power": {
    "report": "Power analysis completed successfully with NanGate 45nm library",
    "total_power_W": 3.37e-07,
    "internal_power_W": 3.02e-06,
    "switching_power_W": 1.64e-06,
    "leakage_power_W": 3.37e-07,
    "details": "See power_report.txt for full details"
  },
  "area": {
    "design_area_um2": 13.034000,
    "technology": "NanGate 45nm",
    "total_cells": 15,
    "note": "Combination of Yosys synthesis and OpenROAD analysis"
  },
  "performance": {
    "design_type": "Combinational logic",
    "max_path_delay_ns": 0.06,
    "clock_period_ns": -1,
    "timing_met": False
  }
}
]
    # Call the reward function
    rewards = verilog_ppa_reward(
        mock_completions, 
        verification_info=mock_verification_info,
        problem_id=mock_problem_id,
        ppa_metrics = gold_ppa_metrics
    )
    
    print("PPA reward test results:")
    print(f"Correct adder implementation reward: {rewards[0]}")
    print(f"Incorrect adder implementation reward: {rewards[1]}")
    print(f"Correct FSM implementation reward: {rewards[2]}")
    print(f"Incorrect FSM implementation reward: {rewards[3]}")
    
    return rewards

if __name__ == "__main__":
    test_ppa_reward()