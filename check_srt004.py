import re
import sys
from io import StringIO
import traceback

# Check SRT-004 runtime error
with open('dsa-problems/Sorting/editorials/SRT-004-merge-k-sorted-capacity.md', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'### Python.*?```python\n(.*?)```'
match = re.search(pattern, content, re.DOTALL)
code = match.group(1)

# Get sample input from test file
import yaml
with open('dsa-problems/Sorting/testcases/SRT-004-merge-k-sorted-capacity.yaml', 'r', encoding='utf-8') as f:
    tests = yaml.safe_load(f)

test_input = tests['samples'][0]['input']

print("Testing SRT-004:")
print("Input:")
print(test_input)
print("\n" + "="*60)

old_stdin = sys.stdin
old_stdout = sys.stdout
sys.stdin = StringIO(test_input)
sys.stdout = StringIO()

namespace = {}
exec(code, namespace)

try:
    namespace['main']()
    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    
    print('Output:')
    print(result)
except Exception as e:
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    print(f'Runtime Error:')
    traceback.print_exc()
