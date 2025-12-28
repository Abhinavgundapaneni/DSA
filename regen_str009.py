#!/usr/bin/env python3
"""Regenerate STR-009 test cases"""
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

# Create test cases
tc = {
    'problem_id': 'STR_MINIMAL_REMOVAL_UNIQUE_PREFIXES__1009',
    'samples': [],
    'public': [],
    'hidden': []
}

# Samples
samples = [
    (2, ['ab', 'ac', 'ad']),
    (2, ['abc', 'abd', 'acc'])
]

for L, strings in samples:
    inp = f"{L}\n{len(strings)}\n" + "\n".join(strings)
    out = str(minimal_removal_unique_prefixes(L, strings))
    tc['samples'].append({'input': inp, 'output': out})

# Public
public = [
    (1, ['a', 'b', 'c']),
    (2, ['test', 'best']),
    (3, ['hello', 'world'])
]

for L, strings in public:
    inp = f"{L}\n{len(strings)}\n" + "\n".join(strings)
    out = str(minimal_removal_unique_prefixes(L, strings))
    tc['public'].append({'input': inp, 'output': out})

# Hidden - corrected
hidden = [
    (2, ['xyz', 'xya']),
    (2, ['test', 'temp']),
    (3, ['abc', 'def', 'ghi']),
    (2, ['a', 'a']),
    (2, ['ab', 'ab']),
    (3, ['test', 'test', 'test']),
    (2, ['test', 'test', 'test', 'test', 'test']),
    (3, ['hello', 'world', 'help', 'wonder']),
    (4, ['test', 'testing', 'tester']),
    (2, ['aa', 'ab', 'ba', 'bb']),
    (1, ['x', 'y', 'z']),
    (5, ['hello', 'world']),
    (2, ['aaa', 'aab', 'bbb']),
    (3, ['testing', 'tested', 'tester']),
    (3, ['test', 'test', 'case', 'case', 'test']),
    (4, ['abcde', 'abcdf', 'abcdg']),
    (2, ['a'*10, 'a'*10]),
    (3, ['abc'*5, 'abc'*5]),
    (2, ['test']),
    (2, ['ab', 'cd', 'ef', 'gh']),
    (3, ['abc', 'abd', 'abe', 'abf']),
    (2, ['xy', 'xz', 'yz']),
    (4, ['test', 'best', 'rest', 'west']),
    (2, ['aaa', 'aaa', 'aaa']),
    (3, ['hello', 'help', 'held']),
    (2, ['x', 'xx', 'xxx'])
]

for L, strings in hidden:
    inp = f"{L}\n{len(strings)}\n" + "\n".join(strings)
    out = str(minimal_removal_unique_prefixes(L, strings))
    tc['hidden'].append({'input': inp, 'output': out})

# Save
path = Path(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Strings\testcases\STR-009-minimal-removal-unique-prefixes.yaml')
with open(path, 'w', encoding='utf-8') as f:
    yaml.dump(tc, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

print(f"✅ Regenerated STR-009: {len(tc['samples'])} samples, {len(tc['public'])} public, {len(tc['hidden'])} hidden")
