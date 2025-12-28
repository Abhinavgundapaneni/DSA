#!/usr/bin/env python3
import re, yaml

# Extract code from editorial
with open(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Stacks\editorials\STK-003-conveyor-weighted-deduplication.md', encoding='utf-8') as f:
    content = f.read()
    match = re.search(r'### Python.*?```python\n(.*?)```', content, re.DOTALL)
    code = match.group(1)

print("Extracted code:")
print(code[:400])
print("\n" + "="*80 + "\n")

# Load test case
with open(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Stacks\testcases\STK-003-conveyor-weighted-deduplication.yaml', encoding='utf-8') as f:
    tc = yaml.safe_load(f)

sample = tc['samples'][0]
print("Test input:", repr(sample['input']))
print("Expected output:", repr(sample['output']))

# Execute
exec(code)
lines = sample['input'].split('\\n')
s = lines[0]
weights = list(map(int, lines[1].split()))

print("\nExecuting with s='{}', weights={}".format(s, weights))
reduced, total = reduce_stack(s, weights)
print("Got: '{}' and {}".format(reduced, total))
print("Expected: 'a' and 8")
