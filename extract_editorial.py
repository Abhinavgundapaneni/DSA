import re

with open(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Greedy\editorials\GRD-012-workshop-task-cooldown-priority.md', encoding='utf-8') as f:
    content = f.read()

pattern = r'### Python.*?```python\n(.*?)```'
match = re.search(pattern, content, re.DOTALL)

if match:
    code = match.group(1)
    print("Found Python code!")
    print(f"Code length: {len(code)} chars")
    print("\n=== Lines around interrupt logic ===")
    lines = code.split('\n')
    for i in range(35, min(50, len(lines))):
        print(f"{i:3d}: {lines[i]}")
else:
    print("No Python code found!")
