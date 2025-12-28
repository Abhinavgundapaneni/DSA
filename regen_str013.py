#!/usr/bin/env python3
"""Regenerate STR-013 test cases"""
import yaml
from pathlib import Path

def run_length_decode_cap(encoded: str, cap: int) -> str:
    result = []
    i = 0
    while i < len(encoded):
        if encoded[i].isalpha():
            char = encoded[i]
            i += 1
            num_str = ''
            while i < len(encoded) and encoded[i].isdigit():
                num_str += encoded[i]
                i += 1
            if num_str:
                count = int(num_str)
                result.append(char * min(count, cap))
    return ''.join(result)

# Create test cases
tc = {
    'problem_id': 'STR_RUN_LENGTH_DECODE_CAP__1013',
    'samples': [],
    'public': [],
    'hidden': []
}

# Samples
samples = [
    ('a3b2c1', 100),
    ('x5y3', 2)
]

for enc, cap in samples:
    inp = f"{enc}\n{cap}"
    out = run_length_decode_cap(enc, cap)
    tc['samples'].append({'input': inp, 'output': out})

# Public
public = [
    ('a10', 5),
    ('a1b1c1', 100),
    ('z20', 10)
]

for enc, cap in public:
    inp = f"{enc}\n{cap}"
    out = run_length_decode_cap(enc, cap)
    tc['public'].append({'input': inp, 'output': out})

# Hidden
hidden = [
    ('a5b5c5', 100),
    ('x100', 50),
    ('a50b60c70', 100),  # The problematic test case
    ('m10n20o30', 25),
    ('p100q100r100', 75),
    ('a1b2c3d4e5', 100),
    ('x50y50', 40),
    ('a10b10c10', 5),
    ('z1000', 500),
    ('a1', 100),
    ('a100b100', 100),
    ('x5y5z5', 3),
    ('a20b20c20d20', 15),
    ('m50', 100),
    ('a10b20c30', 20),
    ('x100', 100),
    ('a5b10c15', 8),
    ('z50', 25),
    ('a1b1c1d1e1', 100),
    ('m100n100', 50),
    ('a25b25c25d25', 20),
    ('x10y10z10', 100),
    ('a100', 10),
    ('m5n5o5p5', 100),
    ('a50b50', 50),
    ('x200', 150),
    ('a10b10c10d10e10', 7),
    ('z100', 1)
]

for enc, cap in hidden:
    inp = f"{enc}\n{cap}"
    out = run_length_decode_cap(enc, cap)
    tc['hidden'].append({'input': inp, 'output': out})

# Save
path = Path(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Strings\testcases\STR-013-run-length-decode-cap.yaml')
with open(path, 'w', encoding='utf-8') as f:
    yaml.dump(tc, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

print(f"✅ Regenerated STR-013: {len(tc['samples'])} samples, {len(tc['public'])} public, {len(tc['hidden'])} hidden")
