import yaml
import re
import os
from io import StringIO
import sys

prob_num = 'DP-009'

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
main = namespace['main']

# Load test cases
test_file = 'dsa-problems/DP/testcases/DP-009-flooded-campus-min-cost-free.yaml'
with open(test_file, 'r', encoding='utf-8') as f:
    tests = yaml.safe_load(f)

print(f'Fixing DP-009 hidden tests 24 and 25')

for idx in [24, 25]:
    tc = tests['hidden'][idx]
    
    # Run solution
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    # Mock stdin
    old_stdin = sys.stdin
    input_text = tc['input']
    if not input_text.endswith('\n'):
        input_text += '\n'
    sys.stdin = StringIO(input_text)
    
    try:
        main()
        new_output = sys.stdout.getvalue().strip()
        tc['output'] = new_output
        print(f'Hidden[{idx}]: Generated output = {new_output}')
    except Exception as e:
        print(f'Hidden[{idx}]: ERROR: {e}')
    finally:
        sys.stdout = old_stdout
        sys.stdin = old_stdin

# Write back
with open(test_file, 'w', encoding='utf-8') as f:
    yaml.dump(tests, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)

print(f'\nUpdated {test_file}')
