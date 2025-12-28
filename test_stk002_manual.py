#!/usr/bin/env python3
import yaml

# Test STK-002
with open(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Stacks\testcases\STK-002-lab-mixed-bracket-repair.yaml', encoding='utf-8') as f:
    tc = yaml.safe_load(f)

sample = tc['samples'][0]
print("Input:", repr(sample['input']))
print("Expected:", repr(sample['output']))

# Extract Python code from editorial
import re
with open(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Stacks\editorials\STK-002-lab-mixed-bracket-repair.md', encoding='utf-8') as f:
    content = f.read()
    match = re.search(r'### Python.*?```python\n(.*?)```', content, re.DOTALL)
    if match:
        code = match.group(1)
        print("\nExtracted code length:", len(code))
        print("First 200 chars:", code[:200])
        
        # Execute it
        exec(code)
        result = can_repair(sample['input'])
        print("\nResult:", result)
        print("Result as string:", "true" if result else "false")
