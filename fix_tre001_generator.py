#!/usr/bin/env python3
"""
Fixed test generator for TRE-001: Campus Directory Multi-Tree Comparison
Generates proper test cases with TWO binary trees.
"""

import random
import yaml
import os

def traverse_tree(n, nodes, node_idx, order):
    """Traverse binary tree in pre/in/post order."""
    if node_idx == -1 or node_idx >= n:
        return []
    
    val, left, right = nodes[node_idx]
    
    if order == 'pre':
        return [val] + traverse_tree(n, nodes, left, order) + traverse_tree(n, nodes, right, order)
    elif order == 'in':
        return traverse_tree(n, nodes, left, order) + [val] + traverse_tree(n, nodes, right, order)
    else:  # post
        return traverse_tree(n, nodes, left, order) + traverse_tree(n, nodes, right, order) + [val]

def traverse_all(n, nodes):
    """Get all three traversals."""
    if n == 0:
        return [[], [], []]
    pre = traverse_tree(n, nodes, 0, 'pre')
    ino = traverse_tree(n, nodes, 0, 'in')
    post = traverse_tree(n, nodes, 0, 'post')
    return [pre, ino, post]

def structural_identical(n1, t1, n2, t2):
    """Check if two trees are structurally identical (ignore values)."""
    if n1 != n2:
        return False
    if n1 == 0:
        return True
    
    def check(i1, i2):
        if i1 == -1 and i2 == -1:
            return True
        if i1 == -1 or i2 == -1:
            return False
        if i1 >= n1 or i2 >= n2:
            return False
        
        _, l1, r1 = t1[i1]
        _, l2, r2 = t2[i2]
        
        return check(l1, l2) and check(r1, r2)
    
    return check(0, 0)

def generate_random_tree(n, seed=None):
    """Generate a random binary tree with n nodes, all reachable from root."""
    if seed:
        random.seed(seed)
    
    if n == 0:
        return []
    if n == 1:
        return [(random.randint(1, 100), -1, -1)]
    
    nodes = [(random.randint(1, 100), -1, -1) for _ in range(n)]
    remaining = list(range(1, n))
    random.shuffle(remaining)
    
    # BFS-style assignment: assign children to nodes in order
    i = 0
    while remaining and i < n:
        # Assign left child
        if nodes[i][1] == -1 and remaining:
            left_child = remaining.pop(0)
            nodes[i] = (nodes[i][0], left_child, nodes[i][2])
        
        # Assign right child
        if nodes[i][2] == -1 and remaining:
            right_child = remaining.pop(0)
            nodes[i] = (nodes[i][0], nodes[i][1], right_child)
        
        i += 1
    
    return nodes

def format_tree_input(nodes):
    """Format tree as input string."""
    lines = [str(len(nodes))]
    for val, left, right in nodes:
        lines.append(f"{val} {left} {right}")
    return "\n".join(lines)

def generate_test_case(n1, n2, seed1, seed2):
    """Generate one test case with two trees."""
    t1 = generate_random_tree(n1, seed1)
    t2 = generate_random_tree(n2, seed2)
    
    # Input
    inp = format_tree_input(t1) + "\n" + format_tree_input(t2)
    
    # Output
    trav1 = traverse_all(n1, t1)
    trav2 = traverse_all(n2, t2)
    same = structural_identical(n1, t1, n2, t2)
    
    matches = []
    # Only compare if both trees are non-empty
    if n1 > 0 and n2 > 0:
        if trav1[0] == trav2[0]:
            matches.append("preorder")
        if trav1[1] == trav2[1]:
            matches.append("inorder")
        if trav1[2] == trav2[2]:
            matches.append("postorder")
    
    output_lines = []
    for i in range(3):
        output_lines.append(" ".join(str(x) for x in trav1[i]) if trav1[i] else "")
    for i in range(3):
        output_lines.append(" ".join(str(x) for x in trav2[i]) if trav2[i] else "")
    output_lines.append("true" if same else "false")
    output_lines.append(" ".join(matches) if matches else "NONE")
    
    return {'input': inp, 'output': "\n".join(output_lines)}

def main():
    cases = {'problem_id': 'TRE_CAMPUS_DIRECTORY_MULTI_TREE__4813', 'samples': [], 'public': [], 'hidden': []}
    
    # Sample 1: From problem statement
    t1 = [(2, 1, 2), (1, -1, -1), (3, -1, -1)]
    t2 = [(1, -1, 1), (2, -1, 2), (3, -1, -1)]
    inp = format_tree_input(t1) + "\n" + format_tree_input(t2)
    
    trav1 = traverse_all(3, t1)
    trav2 = traverse_all(3, t2)
    same = structural_identical(3, t1, 3, t2)
    matches = []
    if trav1[1] == trav2[1]:
        matches.append("inorder")
    
    output_lines = [
        "2 1 3", "1 2 3", "1 3 2",
        "1 2 3", "1 2 3", "3 2 1",
        "false", "inorder"
    ]
    cases['samples'].append({'input': inp, 'output': "\n".join(output_lines)})
    
    # Sample 2: Two identical trees
    t1 = t2 = [(1, -1, -1)]
    inp = format_tree_input(t1) + "\n" + format_tree_input(t2)
    cases['samples'].append({'input': inp, 'output': "1\n1\n1\n1\n1\n1\ntrue\npreorder inorder postorder"})
    
    # Sample 3: Both empty
    cases['samples'].append({'input': "0\n0", 'output': "\n\n\n\n\n\ntrue\nNONE"})
    
    # Public tests (5)
    for i in range(5):
        seed = 100 + i * 10
        n1 = random.Random(seed).randint(1, 10)
        n2 = random.Random(seed + 1).randint(1, 10)
        cases['public'].append(generate_test_case(n1, n2, seed, seed + 1))
    
    # Hidden tests (30)
    for i in range(30):
        seed = 1000 + i * 10
        n1 = random.Random(seed).randint(0, 50)
        n2 = random.Random(seed + 1).randint(0, 50)
        cases['hidden'].append(generate_test_case(n1, n2, seed, seed + 1))
    
    # Write YAML
    output_path = os.path.join(os.path.dirname(__file__), "dsa-problems", "Trees", "testcases", "TRE-001-campus-directory-multi-tree.yaml")
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(cases, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)
    
    print(f"Generated TRE-001: {len(cases['samples'])} samples, {len(cases['public'])} public, {len(cases['hidden'])} hidden")

if __name__ == "__main__":
    main()
