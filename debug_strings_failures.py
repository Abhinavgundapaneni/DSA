#!/usr/bin/env python3
"""Debug remaining Strings failures by examining actual test cases."""

import yaml
import sys
from pathlib import Path

def compress_with_window(s: str, w: int) -> str:
    """STR-007 implementation"""
    if not s:
        return ""
    result = []
    i = 0
    while i < len(s):
        start = i
        char = s[i]
        while i < len(s) and s[i] == char:
            i += 1
        run_length = i - start
        if run_length >= w:
            result.append(char + str(run_length))
        else:
            result.append(char * run_length)
    return ''.join(result)

def decode_with_cap(s: str, cap: int) -> str:
    """STR-013 implementation"""
    result = []
    i = 0
    n = len(s)
    while i < n:
        char = s[i]
        i += 1
        count_str = ""
        while i < n and s[i].isdigit():
            count_str += s[i]
            i += 1
        count = int(count_str) if count_str else 1
        actual_count = min(count, cap)
        result.append(char * actual_count)
    return ''.join(result)

# Test STR-007
print("="*80)
print("STR-007 DEBUGGING")
print("="*80)

str007_path = Path(r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Strings\testcases\STR-007-log-compression-window.yaml")
with open(str007_path, 'r', encoding='utf-8') as f:
    tc007 = yaml.safe_load(f)

print("\nSamples:")
for i, tc in enumerate(tc007['samples']):
    s, w = tc['input'].split('\n')
    w = int(w)
    expected = tc['output']
    actual = compress_with_window(s, w)
    status = "✓" if actual == expected else "✗"
    print(f"{status} Sample {i}: s='{s}', w={w}")
    print(f"  Expected: '{expected}'")
    print(f"  Actual:   '{actual}'")

print("\nHidden (failures only):")
fail_count = 0
for i, tc in enumerate(tc007['hidden']):
    s, w = tc['input'].split('\n')
    w = int(w)
    expected = tc['output']
    actual = compress_with_window(s, w)
    if actual != expected:
        fail_count += 1
        print(f"✗ Hidden {i}: s='{s}', w={w}")
        print(f"  Expected: '{expected}'")
        print(f"  Actual:   '{actual}'")
        if fail_count >= 5:
            print(f"  ... (showing first 5 failures)")
            break

# Test STR-013
print("\n" + "="*80)
print("STR-013 DEBUGGING")
print("="*80)

str013_path = Path(r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Strings\testcases\STR-013-run-length-decode-cap.yaml")
with open(str013_path, 'r', encoding='utf-8') as f:
    tc013 = yaml.safe_load(f)

print("\nHidden (failures only):")
for i, tc in enumerate(tc013['hidden']):
    s, cap = tc['input'].split('\n')
    cap = int(cap)
    expected = tc['output']
    actual = decode_with_cap(s, cap)
    if actual != expected:
        print(f"✗ Hidden {i}: s='{s}', cap={cap}")
        print(f"  Expected length: {len(expected)}, actual length: {len(actual)}")
        print(f"  Expected: '{expected[:100]}...'")
        print(f"  Actual:   '{actual[:100]}...'")
        break
