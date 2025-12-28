#!/usr/bin/env python3
"""Test STR-009 logic"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.strings = []

def minimal_removal_current(L: int, strings: list[str]) -> int:
    """Current implementation"""
    root = TrieNode()
    
    for s in strings:
        node = root
        for i, c in enumerate(s):
            if i == L:
                break
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.strings.append(s)
    
    total_deletions = 0
    
    def find_conflicts(node, depth):
        nonlocal total_deletions
        if depth == L:
            if len(node.strings) > 1:
                node.strings.sort(key=lambda x: -len(x))
                for s in node.strings[1:]:
                    if len(s) >= L:
                        total_deletions += len(s) - (L - 1)
            return
        for child in node.children.values():
            find_conflicts(child, depth + 1)
    
    find_conflicts(root, 0)
    return total_deletions

# Test cases
tests = [
    (2, ['ab', 'ac', 'ad'], 0),  # All distinct
    (2, ['abc', 'abd', 'acc'], 2),  # Two with prefix "ab"
]

for L, strings, expected in tests:
    result = minimal_removal_current(L, strings)
    status = "✓" if result == expected else "✗"
    print(f"{status} L={L}, strings={strings}")
    print(f"  Expected: {expected}, Got: {result}")
    print()
