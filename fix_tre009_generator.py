#!/usr/bin/env python3
"""Generate test cases for TRE-009 (vertical order with weight threshold)"""

import yaml
import random
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from tree_generator_utils import generate_connected_binary_tree

def generate_weighted_tree_with_threshold(n, seed):
    """Generate tree with value, weight, left, right + threshold W"""
    random.seed(seed)
    if n == 0:
        w = random.randint(1, 100)
        return [], w
    
    tree = generate_connected_binary_tree(n, seed)
    weighted_tree = []
    
    for val, left, right in tree:
        weight = random.randint(1, 10000)
        weighted_tree.append((val, weight, left, right))
    
    # Generate threshold W
    w = random.randint(1, n * 5000)
    
    return weighted_tree, w

def format_weighted_tree_input(nodes, w):
    """Format as input string"""
    if not nodes:
        return f"0\n{w}"
    
    lines = [str(len(nodes))]
    for val, weight, left, right in nodes:
        lines.append(f"{val} {weight} {left} {right}")
    lines.append(str(w))
    
    return "\n".join(lines)

# Sample test cases from problem
samples = [
    "6\n8 100 1 2\n4 200 3 -1\n10 150 4 5\n2 50 -1 -1\n6 100 -1 -1\n12 75 -1 -1\n300",
    "1\n5 1000 -1 -1\n500",
    "0\n100"
]

# Extract and run editorial
import re
from io import StringIO

with open('dsa-problems/Trees/editorials/TRE-009-campus-vertical-order-weight.md', 'r', encoding='utf-8') as f:
    editorial = f.read()

pattern = r'### Python.*?```python\n(.*?)```'
match = re.search(pattern, editorial, re.DOTALL)
code = match.group(1)

def run_solution(input_str):
    namespace = {}
    exec(code, namespace)
    
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = StringIO(input_str)
    sys.stdout = StringIO()
    
    try:
        namespace['main']()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Build test cases
cases = {
    'problem_id': 'TRE_CAMPUS_VERTICAL_ORDER_WEIGHT__7421',
    'samples': [],
    'public': [],
    'hidden': []
}

# Samples
for inp in samples:
    output = run_solution(inp)
    cases['samples'].append({'input': inp, 'output': output})

# Public
for i in range(5):
    seed = 9000 + i * 10
    n = random.Random(seed).randint(1, 30)
    tree, w = generate_weighted_tree_with_threshold(n, seed)
    inp = format_weighted_tree_input(tree, w)
    output = run_solution(inp)
    cases['public'].append({'input': inp, 'output': output})

# Hidden
for i in range(30):
    seed = 90000 + i * 10
    n = random.Random(seed).randint(0, 100)
    tree, w = generate_weighted_tree_with_threshold(n, seed)
    inp = format_weighted_tree_input(tree, w)
    output = run_solution(inp)
    cases['hidden'].append({'input': inp, 'output': output})

# Write YAML
with open('dsa-problems/Trees/testcases/TRE-009-campus-vertical-order-weight.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(cases, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)

print(f"✓ Generated TRE-009: {len(cases['samples'])} samples, {len(cases['public'])} public, {len(cases['hidden'])} hidden")
