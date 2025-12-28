import re

# Test the extraction pattern
with open('dsa-problems/MathAdvanced/editorials/MTH-001-polynomial-multiplication-fft.md', 'r', encoding='utf-8') as f:
    content = f.read()

patterns = [
    r'### Python.*?```python\n(.*?)```',
    r'## Python Solution.*?```python\n(.*?)```',
    r'##\s*Python.*?```python\n(.*?)```',
]

for i, pattern in enumerate(patterns):
    match = re.search(pattern, content, re.DOTALL)
    if match:
        code = match.group(1)
        print(f"Pattern {i} matched!")
        print(f"Code length: {len(code)}")
        print(f"First 500 chars:\n{code[:500]}")
        print(f"\nLast 500 chars:\n{code[-500:]}")
        break
else:
    print("No pattern matched!")
