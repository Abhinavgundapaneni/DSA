#!/usr/bin/env python3
"""Quick test for TreesDP problems."""
import os
import re
import sys
import yaml
import subprocess
import tempfile
from pathlib import Path

BASE = Path(r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\TreesDP")

def extract_python_solution(editorial_file):
    """Extract Python solution from editorial markdown."""
    with open(editorial_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find Python code block
    patterns = [
        r'### Python.*?```python\n(.*?)```',
        r'## Python Solution.*?```python\n(.*?)```',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            code = match.group(1)
            # Check if it has main or __name__
            if 'def main' in code or '__name__' in code:
                return code
    return None

def run_test(code, test_input, timeout=10):
    """Run a single test."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, temp_file],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip(), result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT", -1
    finally:
        os.unlink(temp_file)

def test_problem(prob_id, max_tests=5):
    """Test a single problem."""
    editorial_file = BASE / "editorials" / f"{prob_id}.md"
    testcase_file = BASE / "testcases" / f"{prob_id}.yaml"
    
    if not editorial_file.exists():
        # Try with name suffix
        pattern = f"{prob_id}-*.md"
        matches = list((BASE / "editorials").glob(pattern))
        if matches:
            editorial_file = matches[0]
        else:
            print(f"  No editorial found for {prob_id}")
            return
    
    if not testcase_file.exists():
        pattern = f"{prob_id}-*.yaml"
        matches = list((BASE / "testcases").glob(pattern))
        if matches:
            testcase_file = matches[0]
        else:
            print(f"  No testcases found for {prob_id}")
            return
    
    code = extract_python_solution(editorial_file)
    if not code:
        print(f"  NO CODE extracted from {editorial_file.name}")
        return
    
    with open(testcase_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    testcases = data.get('testcases', [])
    passed = 0
    failed = 0
    
    for i, tc in enumerate(testcases[:max_tests]):
        inp = tc.get('input', '')
        expected = tc.get('output', '').strip()
        
        actual, error, returncode = run_test(code, inp)
        
        if actual is None:
            print(f"  Test {i+1}: TIMEOUT")
            failed += 1
        elif actual == expected:
            passed += 1
        else:
            print(f"  Test {i+1}: WRONG")
            print(f"    Got: {repr(actual[:100])}")
            print(f"    Exp: {repr(expected[:100])}")
            failed += 1
    
    print(f"  {prob_id}: {passed}/{passed+failed} in first {max_tests} tests")

def main():
    if len(sys.argv) > 1:
        prob_ids = sys.argv[1:]
    else:
        prob_ids = [f"TDP-{i:03d}" for i in range(1, 17)]
    
    for prob_id in prob_ids:
        print(f"\n{prob_id}:")
        test_problem(prob_id)

if __name__ == "__main__":
    main()
