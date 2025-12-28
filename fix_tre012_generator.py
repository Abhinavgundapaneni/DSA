#!/usr/bin/env python3
"""Generate test cases for TRE-012 (LCA with blocked nodes)"""

import yaml
import random
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from tree_generator_utils import generate_connected_binary_tree

def generate_blocked_tree_with_query(n, seed):
    """Generate tree with value, blocked, left, right + query u,v"""
    random.seed(seed)
    if n == 0:
        return [], 0, 0
    
    tree = generate_connected_binary_tree(n, seed)
    blocked_tree = []
    
    for val, left, right in tree:
        blocked = random.randint(0, 1)
        blocked_tree.append((val, blocked, left, right))
    
    # Ensure at least 2 unblocked nodes for query
    unblocked = [i for i, (_, b, _, _) in enumerate(blocked_tree) if b == 0]
    if len(unblocked) < 2:
        # Force first two nodes to be unblocked
        blocked_tree[0] = (blocked_tree[0][0], 0, blocked_tree[0][2], blocked_tree[0][3])
        if n > 1:
            blocked_tree[1] = (blocked_tree[1][0], 0, blocked_tree[1][2], blocked_tree[1][3])
        unblocked = [i for i, (_, b, _, _) in enumerate(blocked_tree) if b == 0]
    
    # Pick two random unblocked nodes for query
    u, v = random.sample(unblocked, 2)
    
    return blocked_tree, u, v

def format_blocked_tree_input(nodes, u, v):
    """Format as input string"""
    if not nodes:
        return f"0\n0 0"
    
    lines = [str(len(nodes))]
    for val, blocked, left, right in nodes:
        lines.append(f"{val} {blocked} {left} {right}")
    lines.append(f"{u} {v}")
    
    return "\n".join(lines)

# Sample test cases
samples = [
    "5\n6 1 1 2\n2 0 3 4\n8 0 -1 -1\n1 0 -1 -1\n5 0 -1 -1\n3 4",
    "1\n10 0 -1 -1\n0 0",
    "3\n5 1 1 2\n3 0 -1 -1\n7 0 -1 -1\n1 2"
]

# Extract and run editorial
import re
from io import StringIO

with open('dsa-problems/Trees/editorials/TRE-012-robotics-lca-blocked.md', 'r', encoding='utf-8') as f:
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
    'problem_id': 'TRE_ROBOTICS_LCA_BLOCKED__3142',
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
    seed = 12000 + i * 10
    n = random.Random(seed).randint(1, 30)
    tree, u, v = generate_blocked_tree_with_query(n, seed)
    inp = format_blocked_tree_input(tree, u, v)
    output = run_solution(inp)
    cases['public'].append({'input': inp, 'output': output})

# Hidden
for i in range(30):
    seed = 120000 + i * 10
    n = random.Random(seed).randint(1, 100)
    tree, u, v = generate_blocked_tree_with_query(n, seed)
    inp = format_blocked_tree_input(tree, u, v)
    output = run_solution(inp)
    cases['hidden'].append({'input': inp, 'output': output})

# Write YAML
with open('dsa-problems/Trees/testcases/TRE-012-robotics-lca-blocked.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(cases, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)

print(f"✓ Generated TRE-012: {len(cases['samples'])} samples, {len(cases['public'])} public, {len(cases['hidden'])} hidden")
