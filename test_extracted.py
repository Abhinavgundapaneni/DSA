import re

with open(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Greedy\editorials\GRD-012-workshop-task-cooldown-priority.md', encoding='utf-8') as f:
    content = f.read()

pattern = r'### Python.*?```python\n(.*?)```'
match = re.search(pattern, content, re.DOTALL)

if match:
    code = match.group(1)
    
    # Save extracted code
    with open('extracted_editorial_grd012.py', 'w') as f:
        f.write(code)
    
    print("Saved extracted code to extracted_editorial_grd012.py")
    
    # Test it
    exec(code)
    
    # Test public[1]
    result = min_slots([('A', 13, 2), ('B', 11, 2), ('C', 18, 1)], 8)
    print(f"\nPublic[1] result: {result}, expected: 245")
