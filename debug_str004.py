import sys
import yaml
import subprocess
import tempfile
import os

def extract_python_solution(editorial_file):
    """Extract Python solution from editorial markdown."""
    with open(editorial_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    patterns = [
        r'### Python.*?```python\n(.*?)```',
        r'## Python Solution.*?```python\n(.*?)```',
        r'##\s*Python.*?```python\n(.*?)```',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1)
    return None

def run_test_case(solution_code, test_input):
    """Run a single test case through the solution."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(solution_code)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, temp_file],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip(), result.stderr.strip() if result.stderr else None
    except Exception as e:
        return None, str(e)
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass

# Test STR-004
editorial_file = r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Strings\editorials\STR-004-alternating-vowel-consonant-substring.md"
testcase_file = r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Strings\testcases\STR-004-alternating-vowel-consonant-substring.yaml"

solution_code = extract_python_solution(editorial_file)
with open(testcase_file, 'r', encoding='utf-8') as f:
    tc_data = yaml.safe_load(f)

print("Testing all hidden test cases for STR-004:\n")
for idx, tc in enumerate(tc_data['hidden']):
    test_input = tc['input']
    expected_output = tc['output'].strip()
    
    actual_output, error = run_test_case(solution_code, test_input)
    actual_output = actual_output.strip() if actual_output else ""
    
    if error:
        print(f"Hidden[{idx}] ERROR: {test_input[:30]}")
        print(f"  Error: {error[:100]}")
    elif actual_output != expected_output:
        print(f"Hidden[{idx}] FAIL: input='{test_input}'")
        print(f"  Expected: {repr(expected_output)}")
        print(f"  Got:      {repr(actual_output)}")
        print()
