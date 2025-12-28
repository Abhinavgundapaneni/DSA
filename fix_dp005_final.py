import yaml
import re
import os
from io import StringIO
import sys

prob_num = 'DP-005'
fix_indices = [1, 17, 18, 19]  # public[1], hidden[17,18,19] based on 0-indexed

# Extract editorial
files = [f for f in os.listdir('dsa-problems/DP/editorials') if f.startswith(prob_num)]
editorial_path = os.path.join('dsa-problems/DP/editorials', files[0])

with open(editorial_path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'### Python.*?```python\n(.*?)```'
match = re.search(pattern, content, re.DOTALL)
code = match.group(1)

namespace = {}
exec(code, namespace)

print(f'Extracted function names: {[k for k in namespace.keys() if not k.startswith("__")]}')

# Load test cases
test_file = os.path.join('dsa-problems/DP/testcases', f'{prob_num}-keyboard-row-edit-distance-shift.yaml')
with open(test_file, 'r', encoding='utf-8') as f:
    tests = yaml.safe_load(f)

print(f'\nOriginal outputs for indices to fix:')
for idx in fix_indices:
    if idx <= 2:  # public
        tc = tests['public'][idx]
        print(f'  public[{idx}]: {tc.get("output", "MISSING")}')
    else:  # hidden
        tc = tests['hidden'][idx - 3]
        print(f'  hidden[{idx-3}]: {tc.get("output", "MISSING")}')

# Execute on test cases and regenerate
main = namespace['main']
fixed_count = 0

for idx in fix_indices:
    if idx <= 2:  # public
        tc = tests['public'][idx]
    else:  # hidden
        tc = tests['hidden'][idx - 3]
    
    # Run solution
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    # Mock stdin - ensure input ends with newline
    old_stdin = sys.stdin
    input_text = tc['input']
    if not input_text.endswith('\n'):
        input_text += '\n'
    sys.stdin = StringIO(input_text)
    
    try:
        main()
        new_output = sys.stdout.getvalue().strip()
    except Exception as e:
        new_output = f"ERROR: {e}"
    finally:
        sys.stdout = old_stdout
        sys.stdin = old_stdin
    
    # Update
    old_output = tc.get('output', 'MISSING')
    tc['output'] = new_output
    
    if old_output != new_output:
        fixed_count += 1
        print(f'\nFixed {"public" if idx <= 2 else "hidden"}[{idx if idx <= 2 else idx-3}]:')
        print(f'  Old: {old_output}')
        print(f'  New: {new_output}')

print(f'\n{fixed_count} test cases updated')

# Write back - preserve multiline format
with open(test_file, 'w', encoding='utf-8') as f:
    yaml.dump(tests, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)

print(f'Updated {test_file}')
