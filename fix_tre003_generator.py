#!/usr/bin/env python3
"""Fixed test generator for TRE-003: Garden Leaf Count"""

import yaml
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from tree_generator_utils import generate_connected_binary_tree, count_leaves, format_tree_input
import random

def main():
    cases = {'problem_id': 'TRE_GARDEN_LEAF_COUNT__2475', 'samples': [], 'public': [], 'hidden': []}
    
    # Sample 1: From problem statement
    tree = [(7, 1, 2), (4, -1, -1), (8, -1, -1)]
    cases['samples'].append({
        'input': format_tree_input(tree),
        'output': '2'
    })
    
    # Sample 2: Single node
    tree = [(1, -1, -1)]
    cases['samples'].append({
        'input': format_tree_input(tree),
        'output': '1'
    })
    
    # Sample 3: Empty tree
    cases['samples'].append({
        'input': '0',
        'output': '0'
    })
    
    # Public tests (5)
    for i in range(5):
        seed = 200 + i * 10
        n = random.Random(seed).randint(1, 30)
        tree = generate_connected_binary_tree(n, seed)
        leaves = count_leaves(tree)
        cases['public'].append({
            'input': format_tree_input(tree),
            'output': str(leaves)
        })
    
    # Hidden tests (30)
    for i in range(30):
        seed = 2000 + i * 10
        n = random.Random(seed).randint(0, 100)
        tree = generate_connected_binary_tree(n, seed)
        leaves = count_leaves(tree)
        cases['hidden'].append({
            'input': format_tree_input(tree),
            'output': str(leaves)
        })
    
    # Write YAML
    output_path = os.path.join(os.path.dirname(__file__), "dsa-problems", "Trees", "testcases", "TRE-003-garden-leaf-count.yaml")
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(cases, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)
    
    print(f"Generated TRE-003: {len(cases['samples'])} samples, {len(cases['public'])} public, {len(cases['hidden'])} hidden")

if __name__ == "__main__":
    main()
