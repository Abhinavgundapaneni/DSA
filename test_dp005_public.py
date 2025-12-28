import yaml, re, sys
from io import StringIO

# Load editorial
with open('dsa-problems/DP/editorials/DP-005-keyboard-row-edit-distance-shift.md', 'r', encoding='utf-8') as f:
    content = f.read()
match = re.search(r'### Python.*?```python\n(.*?)```', content, re.DOTALL)
code = match.group(1)

namespace = {}
exec(code, namespace)
main = namespace['main']

# Load tests
with open('dsa-problems/DP/testcases/DP-005-keyboard-row-edit-distance-shift.yaml', encoding='utf-8') as f:
    tests = yaml.safe_load(f)

# Test each public
for i in range(3):
    tc = tests['public'][i]
    inp = tc['input']
    expected = tc['output']
    
    sys.stdin = StringIO(inp + '\n' if not inp.endswith('\n') else inp)
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        main()
        result = sys.stdout.getvalue().strip()
        status = '✓' if result == expected else 'WRONG'
    except Exception as e:
        result = f'ERROR: {e}'
        status = 'ERROR'
    finally:
        sys.stdout = old_stdout
    
    print(f'Public[{i}]: {status}')
    print(f'  Input: {repr(inp)}')
    print(f'  Expected: {expected}')
    print(f'  Got: {result}')
