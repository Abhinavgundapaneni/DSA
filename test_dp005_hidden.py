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

# Test all hidden
failures = []
for i in range(len(tests['hidden'])):
    tc = tests['hidden'][i]
    inp = tc['input']
    expected = tc['output']
    
    sys.stdin = StringIO(inp + '\n' if not inp.endswith('\n') else inp)
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        main()
        result = sys.stdout.getvalue().strip()
        if result != expected:
            failures.append((i, inp, expected, result))
    except Exception as e:
        failures.append((i, inp, expected, f'ERROR: {e}'))
    finally:
        sys.stdout = old_stdout

print(f'Total hidden tests: {len(tests["hidden"])}')
print(f'Failures: {len(failures)}')
for idx, inp, exp, got in failures:
    print(f'\nHidden[{idx}]:')
    print(f'  Input: {repr(inp[:50])}...' if len(inp) > 50 else f'  Input: {repr(inp)}')
    print(f'  Expected: {exp}')
    print(f'  Got: {got}')
