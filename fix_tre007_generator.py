#!/usr/bin/env python3
"""Generate test cases for TRE-007 (weighted diameter)"""

import yaml
import random

def generate_weighted_tree(n, seed):
    """Generate tree with value, left, right, leftWeight, rightWeight"""
    random.seed(seed)
    if n == 0:
        return []
    
    nodes = []
    unassigned = list(range(1, n))
    
    for i in range(n):
        val = random.randint(1, 100)
        left, right = -1, -1
        lw, rw = 0, 0
        
        # Assign children
        if unassigned and random.random() < 0.7:
            left = unassigned.pop(0)
            lw = random.randint(1, 20)
        
        if unassigned and random.random() < 0.7:
            right = unassigned.pop(0)
            rw = random.randint(1, 20)
        
        nodes.append((val, left, right, lw, rw))
    
    return nodes

def format_weighted_tree(nodes):
    """Format as input string"""
    if not nodes:
        return "0"
    
    lines = [str(len(nodes))]
    for val, left, right, lw, rw in nodes:
        lines.append(f"{val} {left} {right} {lw} {rw}")
    
    return "\n".join(lines)

# Sample test cases
samples = [
    "4\n1 1 2 3 1\n2 3 -1 2 0\n3 -1 -1 0 0\n4 -1 -1 0 0",
    "1\n7 -1 -1 0 0",
    "0"
]

# Generate test cases
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Extract and run editorial
import re
from io import StringIO

with open('dsa-problems/Trees/editorials/TRE-007-sports-dome-weighted-diameter.md', 'r', encoding='utf-8') as f:
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
    'problem_id': 'TRE_SPORTS_DOME_WEIGHTED_DIAMETER__9532',
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
    seed = 7000 + i * 10
    n = random.Random(seed).randint(1, 30)
    tree = generate_weighted_tree(n, seed)
    inp = format_weighted_tree(tree)
    output = run_solution(inp)
    cases['public'].append({'input': inp, 'output': output})

# Hidden
for i in range(30):
    seed = 70000 + i * 10
    n = random.Random(seed).randint(0, 100)
    tree = generate_weighted_tree(n, seed)
    inp = format_weighted_tree(tree)
    output = run_solution(inp)
    cases['hidden'].append({'input': inp, 'output': output})

# Write YAML
with open('dsa-problems/Trees/testcases/TRE-007-sports-dome-weighted-diameter.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(cases, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)

print(f"✓ Generated TRE-007: {len(cases['samples'])} samples, {len(cases['public'])} public, {len(cases['hidden'])} hidden")
