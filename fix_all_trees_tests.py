#!/usr/bin/env python3
"""
Regenerate ALL Trees test cases by running editorials on properly generated tree inputs.
"""

import yaml
import os
import sys
import re
from io import StringIO
sys.path.insert(0, os.path.dirname(__file__))
from tree_generator_utils import generate_connected_binary_tree, format_tree_input
import random

def extract_python_solution(editorial_path):
    """Extract Python code from editorial markdown."""
    with open(editorial_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'### Python.*?```python\n(.*?)```'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return None
    return match.group(1)

def run_solution(code, input_str):
    """Run Python solution code on input and capture output."""
    namespace = {}
    exec(code, namespace)
    
    if 'main' not in namespace:
        return None
    
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    
    sys.stdin = StringIO(input_str)
    sys.stdout = StringIO()
    
    try:
        namespace['main']()
        result = sys.stdout.getvalue()
        return result.strip() if result else ""
    except Exception as e:
        print(f"    ERROR running solution: {e}")
        return None
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def regenerate_problem(prob_num):
    """Regenerate test cases for one Trees problem."""
    # Find editorial
    editorial_files = [f for f in os.listdir('dsa-problems/Trees/editorials') 
                      if f.startswith(f'TRE-{prob_num:03d}')]
    if not editorial_files:
        print(f"  ✗ No editorial found")
        return False
    
    editorial_path = os.path.join('dsa-problems/Trees/editorials', editorial_files[0])
    code = extract_python_solution(editorial_path)
    if not code:
        print(f"  ✗ No Python code in editorial")
        return False
    
    # Find test file
    test_files = [f for f in os.listdir('dsa-problems/Trees/testcases') 
                 if f.startswith(f'TRE-{prob_num:03d}')]
    if not test_files:
        print(f"  ✗ No test file found")
        return False
    
    test_path = os.path.join('dsa-problems/Trees/testcases', test_files[0])
    
    # Load existing YAML to get problem_id and existing inputs
    with open(test_path, 'r', encoding='utf-8') as f:
        existing = yaml.safe_load(f)
    
    problem_id = existing.get('problem_id', f'TRE_UNKNOWN_{prob_num}')
    
    # Regenerate outputs for all test cases
    cases = {'problem_id': problem_id, 'samples': [], 'public': [], 'hidden': []}
    
    # Process samples
    for sample in existing.get('samples', []):
        inp = sample.get('input', '')
        output = run_solution(code, inp)
        if output is not None:
            cases['samples'].append({'input': inp, 'output': output})
        else:
            print(f"    ⚠️  Sample failed to run")
    
    # Process public
    for public in existing.get('public', []):
        inp = public.get('input', '')
        output = run_solution(code, inp)
        if output is not None:
            cases['public'].append({'input': inp, 'output': output})
        else:
            print(f"    ⚠️  Public test failed to run")
    
    # Process hidden
    for hidden in existing.get('hidden', []):
        inp = hidden.get('input', '')
        output = run_solution(code, inp)
        if output is not None:
            cases['hidden'].append({'input': inp, 'output': output})
        else:
            print(f"    ⚠️  Hidden test failed to run")
    
    # Write updated YAML
    with open(test_path, 'w', encoding='utf-8') as f:
        yaml.dump(cases, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)
    
    total = len(cases['samples']) + len(cases['public']) + len(cases['hidden'])
    print(f"  ✓ Regenerated {total} tests ({len(cases['samples'])} samples, {len(cases['public'])} public, {len(cases['hidden'])} hidden)")
    return True

def main():
    problems_to_fix = [4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    
    print("Regenerating Trees test cases from editorials...\n")
    
    success_count = 0
    for prob_num in problems_to_fix:
        print(f"TRE-{prob_num:03d}:")
        if regenerate_problem(prob_num):
            success_count += 1
    
    print(f"\n✓ Successfully regenerated {success_count}/{len(problems_to_fix)} problems")

if __name__ == "__main__":
    main()
