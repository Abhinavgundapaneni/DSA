#!/usr/bin/env python3
"""
Universal binary tree generator for all Trees problems.
Generates proper connected binary trees.
"""

import random

def generate_connected_binary_tree(n, seed=None):
    """
    Generate a random connected binary tree with n nodes.
    Returns list of (value, left, right) tuples where indices are valid.
    """
    if seed is not None:
        random.seed(seed)
    
    if n == 0:
        return []
    
    if n == 1:
        return [(random.randint(1, 100), -1, -1)]
    
    # Build tree by assigning children from unassigned pool
    nodes = [(random.randint(1, 100), -1, -1) for _ in range(n)]
    unassigned = list(range(1, n))  # All nodes except root
    random.shuffle(unassigned)
    
    for i in range(n):
        if not unassigned:
            break
        
        val, left, right = nodes[i]
        
        # Assign left child with 70% probability
        if unassigned and random.random() < 0.7:
            left = unassigned.pop(0)
        
        # Assign right child with 70% probability
        if unassigned and random.random() < 0.7:
            right = unassigned.pop(0)
        
        nodes[i] = (val, left, right)
    
    return nodes

def count_leaves(nodes):
    """Count leaf nodes in tree (all nodes with both children = -1, regardless of reachability)."""
    if not nodes:
        return 0
    
    count = 0
    for val, left, right in nodes:
        if left == -1 and right == -1:
            count += 1
    
    return count

def tree_height(nodes):
    """Calculate tree height (-1 for empty, 0 for single node)."""
    if not nodes:
        return -1
    
    def dfs(idx):
        if idx == -1:
            return -1
        val, left, right = nodes[idx]
        return 1 + max(dfs(left), dfs(right))
    
    return dfs(0)

def format_tree_input(nodes):
    """Format tree as input string."""
    if not nodes:
        return "0"
    lines = [str(len(nodes))]
    for val, left, right in nodes:
        lines.append(f"{val} {left} {right}")
    return "\n".join(lines)

# Test the generator
if __name__ == "__main__":
    # Test connected tree
    tree = generate_connected_binary_tree(10, seed=42)
    print("Generated tree (10 nodes):")
    print(format_tree_input(tree))
    print(f"\nLeaves: {count_leaves(tree)}")
    print(f"Height: {tree_height(tree)}")
