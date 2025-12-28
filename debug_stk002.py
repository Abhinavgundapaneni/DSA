#!/usr/bin/env python3
"""Debug STK-002"""
import yaml
from pathlib import Path

# Load test case
tc_file = Path(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Stacks\testcases\STK-002-lab-mixed-bracket-repair.yaml')
with open(tc_file, encoding='utf-8') as f:
    tc = yaml.safe_load(f)

# Get first sample
sample = tc['samples'][0]
print("Input:")
print(repr(sample['input']))
print("\nExpected:")
print(repr(sample['output']))

# Test the function
def min_deletions(s: str) -> int:
    stack = []
    for ch in s:
        if ch == '(':
            stack.append(ch)
        elif ch == ')':
            if stack and stack[-1] == '(':
                stack.pop()
            else:
                stack.append(ch)
    return len(stack)

inp = sample['input'].strip()
result = min_deletions(inp)
print("\nActual:")
print(result)
