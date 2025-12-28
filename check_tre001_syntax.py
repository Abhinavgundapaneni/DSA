import re

with open('dsa-problems/Trees/editorials/TRE-001-campus-directory-multi-tree.md', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'### Python.*?```python\n(.*?)```'
match = re.search(pattern, content, re.DOTALL)

if match:
    code = match.group(1)
    print(f"Extracted {len(code.split(chr(10)))} lines of Python code")
    
    # Try to compile it
    try:
        compile(code, '<string>', 'exec')
        print("✓ Code compiles successfully")
    except SyntaxError as e:
        print(f"✗ Syntax error: {e}")
        print(f"  Line {e.lineno}: {e.text}")
else:
    print("No Python code block found")
