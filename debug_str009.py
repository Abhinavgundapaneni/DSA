#!/usr/bin/env python3
"""Debug STR-009 failures"""
import yaml
from pathlib import Path

class TrieNode:
    def __init__(self):
        self.children = {}
        self.strings = []

def minimal_removal_unique_prefixes(L: int, strings: list[str]) -> int:
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

# Load test cases
path = Path(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Strings\testcases\STR-009-minimal-removal-unique-prefixes.yaml')
data = yaml.safe_load(open(path, encoding='utf-8'))

print("STR-009 FAILURES:")
print("="*80)

for i, tc in enumerate(data['hidden']):
    lines = tc['input'].split('\n')
    L = int(lines[0])
    n = int(lines[1])
    strings = lines[2:2+n]
    
    expected = int(tc['output'])
    actual = minimal_removal_unique_prefixes(L, strings)
    
    if actual != expected:
        print(f"\n✗ Hidden[{i}]:")
        print(f"  L={L}, n={n}")
        print(f"  Strings: {strings}")
        print(f"  Expected: {expected}")
        print(f"  Actual: {actual}")
        print(f"  Difference: {actual - expected}")
