from dotenv import load_dotenv
load_dotenv()
from e2b_code_interpreter import Sandbox
import json

# The Python code to test
code_snippet = """
for _ in range(int(input())):
    n = int(input())
    mass = []
    zo = 0
    oz = 0
    zz = 0
    oo = 0
    ozs = []
    zos = []
    ozss = set()
    zoss = set()
    for j in range(n):
        k = input()
        mass.append(k)
        if k[0] == '0' and k[-1] == '1':
            zoss.add(k)
            zos.append(j + 1)
            zo += 1
        elif k[0] == '1' and k[-1] == '0':
            ozss.add(k)
            ozs.append(j + 1)
            oz += 1
        elif k[0] == '0' and k[-1] == '0':
            zz += 1
        else:
            oo += 1
    if zz and oo and not oz and not zo:
        print(-1)
        continue
    else:
        if zo > oz:
            print((zo - oz) // 2)
            ans = []
            need = (zo - oz) // 2
            i = 0
            while need:
                zzz = mass[zos[i] - 1][len(mass[zos[i] - 1]) - 1:: -1]
                if zzz not in ozss:
                    ans.append(zos[i])
                    need -= 1
                i += 1
            print(*ans)
        else:
            print((oz - zo) // 2)
            ans = []
            need = (oz - zo) // 2
            i = 0
            while need:
                zzz = mass[ozs[i] - 1][len(mass[ozs[i] - 1]) - 1:: -1]
                if zzz not in zoss:
                    ans.append(ozs[i])
                    need -= 1
                i += 1
            print(*ans)
"""

# Test case
test_cases = [
    {
        "input": "4\n4\n0001\n1000\n0011\n0111\n3\n010\n101\n0\n2\n00000\n00001\n4\n01\n001\n0001\n00001\n",
        "output": "1\n3\n-1\n0\n\n2\n1 2\n"
    }
]

evaluation_script = """
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
            print(f"Execution error: {{process.stderr}}")
            continue

        output = process.stdout.strip()
        expected = case["output"].strip()
        print(f"Output: {{output}}")
        print(f"Expected: {{expected}}")
        if output == expected:
            passed += 1

    success_rate = (passed / total)
    return success_rate

code_snippet = {code}
test_cases = {test_cases}

result = evaluate_code(code_snippet, test_cases)
print(f"Success rate: {{result}}")
"""

script = evaluation_script.format(
        code=json.dumps(code_snippet),
        test_cases=json.dumps(test_cases)
    )

with Sandbox(timeout=30, request_timeout=3) as sbx:
    # Try to reproduce the error from code_reward function
    try:
        
        execution = sbx.run_code(script)
        print("Execution result:")
        print(execution.text)
        print("Logs:")
        print(execution.logs)
    except Exception as e:
        print(f"Error from E2B executor: {e}")
