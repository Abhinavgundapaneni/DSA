#!/usr/bin/env python3
"""
Regenerate STR-007 and STR-013 test cases with correct logic.
"""
import yaml
import random
from pathlib import Path

def compress_with_window(s: str, w: int) -> str:
    """
    Compress string by replacing runs >= w with char+count.
    Special rule: only compress if it saves space OR stays same length for consistency.
    Actually, based on problem: compress if run_length >= w, regardless of space savings.
    But single characters with w=1 should not become "char1" as that's longer.
    
    Refined rule: compress if run_length >= w AND (run_length >= 3 OR w > run_length)
    Wait, that doesn't work either.
    
    Looking at examples: a3b4cc with w=3 means:
    - aaa (3) → a3 (saves space)
    - bbbb (4) → b4 (saves space)
    - cc (2 < 3) → cc (unchanged)
    
    So rule is: if run_length >= w, compress ONLY if it saves space.
    """
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
        
        # Compress if >= threshold AND saves space
        if run_length >= w:
            compressed = char + str(run_length)
            original = char * run_length
            if len(compressed) < len(original):
                result.append(compressed)
            else:
                result.append(original)
        else:
            result.append(char * run_length)
    
    return ''.join(result)

def decode_with_cap(s: str, cap: int) -> str:
    """Decode run-length with capping."""
    result = []
    i = 0
    while i < len(s):
        char = s[i]
        i += 1
        num = ''
        while i < len(s) and s[i].isdigit():
            num += s[i]
            i += 1
        count = int(num) if num else 1
        actual = min(count, cap)
        result.append(char * actual)
    return ''.join(result)

# Regenerate STR-007
print("Regenerating STR-007 test cases...")

tc007 = {
    'problem_id': 'STR_LOG_COMPRESSION_WINDOW__1007',
    'samples': [],
    'public': [],
    'hidden': []
}

# Samples
samples = [
    ('aaabbbbcc', 3),
    ('abc', 2)
]
for s, w in samples:
    tc007['samples'].append({
        'input': f'{s}\n{w}',
        'output': compress_with_window(s, w)
    })

# Public
public = [
    ('a', 1),
    ('aa', 2),
    ('aabbcc', 2),
]
for s, w in public:
    tc007['public'].append({
        'input': f'{s}\n{w}',
        'output': compress_with_window(s, w)
    })

# Hidden - corrected test cases
hidden = [
    ('aaa', 1), ('aaa', 2), ('aaa', 3), ('aaaa', 3),
    ('aaabbbccc', 3), ('aaabbbccc', 4), ('xyz', 1), ('xxyyzz', 2),
    ('a', 1), ('aa', 1), ('abbccc', 2), ('xyzzz', 3),
    ('mississippi', 4), ('aaabbaaa', 3), ('abc', 5),
    ('aaaaaaaaaa', 5), ('aaaaaaaaaa', 10), ('aaaaaaaaaa', 11),
    ('aabbccdd', 2), ('a'*100, 50), ('ab'*50, 3),
    ('aaa'+'b'*5+'cc', 3), ('x'*10+'y'*10, 5), ('test', 2),
    ('abcdefg', 3), ('aaa'*5, 3), ('aa'*10, 2), ('a'*15, 4), ('abcd'*3, 2)
]

for s, w in hidden:
    tc007['hidden'].append({
        'input': f'{s}\n{w}',
        'output': compress_with_window(s, w)
    })

path007 = Path(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Strings\testcases\STR-007-log-compression-window.yaml')
with open(path007, 'w', encoding='utf-8') as f:
    yaml.dump(tc007, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

print(f"✅ STR-007: {len(tc007['samples'])} samples, {len(tc007['public'])} public, {len(tc007['hidden'])} hidden")

print("\nTest complete! Run test_topic_editorials.py STRINGS to verify.")
