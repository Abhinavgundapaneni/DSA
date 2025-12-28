#!/usr/bin/env python3
"""Test STR-007 compression logic"""

def compress_original(s: str, w: int) -> str:
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

def compress_smart(s: str, w: int) -> str:
    """Only compress if it actually saves space"""
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
            compressed = char + str(run_length)
            original = char * run_length
            # Only use compression if it's shorter
            if len(compressed) < len(original):
                result.append(compressed)
            else:
                result.append(original)
        else:
            result.append(char * run_length)
    return ''.join(result)

# Test cases
tests = [
    ("a", 1),
    ("aa", 2),
    ("aaa", 3),
    ("aaabbbbcc", 3),
]

print("Original implementation:")
for s, w in tests:
    print(f"  s='{s}', w={w} → '{compress_original(s, w)}'")

print("\nSmart implementation (only compress if shorter):")
for s, w in tests:
    print(f"  s='{s}', w={w} → '{compress_smart(s, w)}'")
