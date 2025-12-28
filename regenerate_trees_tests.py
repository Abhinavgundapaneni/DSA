#!/usr/bin/env python3
"""
Universal test regenerator for Trees problems.
Runs editorial solutions on properly generated trees to create correct expected outputs.
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
        return None
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def regenerate_tests_for_problem(problem_num, problem_id, sample_inputs):
    """Regenerate tests for one problem using its editorial."""
    editorial_files = [f for f in os.listdir('dsa-problems/Trees/editorials') if f.startswith(f'TRE-{problem_num:03d}')]
    if not editorial_files:
        print(f"  No editorial found for TRE-{problem_num:03d}")
        return None
    
    editorial_path = os.path.join('dsa-problems/Trees/editorials', editorial_files[0])
    code = extract_python_solution(editorial_path)
    if not code:
        print(f"  No Python code in editorial for TRE-{problem_num:03d}")
        return None
    
    cases = {'problem_id': problem_id, 'samples': [], 'public': [], 'hidden': []}
    
    # Generate samples from provided inputs
    for inp in sample_inputs:
        output = run_solution(code, inp)
        if output is not None:
            cases['samples'].append({'input': inp, 'output': output})
    
    # Generate public tests
    for i in range(5):
        seed = 300 + problem_num * 100 + i * 10
        n = random.Random(seed).randint(1, 30)
        tree = generate_connected_binary_tree(n, seed)
        inp = format_tree_input(tree)
        output = run_solution(code, inp)
        if output is not None:
            cases['public'].append({'input': inp, 'output': output})
    
    # Generate hidden tests
    for i in range(30):
        seed = 3000 + problem_num * 100 + i * 10
        n = random.Random(seed).randint(0, 100)
        tree = generate_connected_binary_tree(n, seed)
        inp = format_tree_input(tree)
        output = run_solution(code, inp)
        if output is not None:
            cases['hidden'].append({'input': inp, 'output': output})
    
    return cases

def main():
    # Problem definitions: (number, problem_id, sample_inputs)
    problems = [
        (4, 'TRE_SEMINAR_LEVEL_ORDER_ODD__1683', [
            '4\n10 1 2\n5 3 -1\n12 -1 -1\n7 -1 -1',
            '1\n1 -1 -1',
            '0'
        ]),
        (6, 'TRE_LAB_PATH_SUM_ONE_TURN__9521', [
            '5\n1 1 2\n2 -1 3\n3 -1 4\n4 -1 -1\n5 -1 -1',
            '1\n10 -1 -1',
            '0'
        ]),
        (7, 'TRE_SPORTS_DOME_WEIGHTED_DIAMETER__3847', [
            '5\n10 1 2\n5 -1 3\n15 -1 4\n3 -1 -1\n2 -1 -1',
            '1\n7 -1 -1',
            '0'
        ]),
    ]
    
    for prob_num, prob_id, samples in problems:
        print(f"\nGenerating TRE-{prob_num:03d}...")
        cases = regenerate_tests_for_problem(prob_num, prob_id, samples)
        
        if cases and len(cases['samples']) > 0:
            # Write YAML
            test_files = [f for f in os.listdir('dsa-problems/Trees/testcases') if f.startswith(f'TRE-{prob_num:03d}')]
            if test_files:
                output_path = os.path.join('dsa-problems/Trees/testcases', test_files[0])
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(cases, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)
                print(f"  ✓ Generated: {len(cases['samples'])} samples, {len(cases['public'])} public, {len(cases['hidden'])} hidden")
            else:
                print(f"  ✗ No test file found")
        else:
            print(f"  ✗ Failed to generate")

if __name__ == "__main__":
    main()
