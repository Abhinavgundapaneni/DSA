import re, sys, traceback
from io import StringIO

with open('dsa-problems/Sorting/editorials/SRT-004-min-inversions-one-swap.md', 'r') as f:
    content = f.read()

pattern = r'### Python.*?```python\n(.*?)```'
match = re.search(pattern, content, re.DOTALL)
code = match.group(1)

print("Editorial code:")
print(code)
print("\n" + "="*60)

# Try to run it
test_input = "5\n2 4 1 3 5"

old_stdin, old_stdout = sys.stdin, sys.stdout
sys.stdin, sys.stdout = StringIO(test_input), StringIO()

namespace = {}
exec(code, namespace)

try:
    namespace['main']()
    result = sys.stdout.getvalue()
    sys.stdin, sys.stdout = old_stdin, old_stdout
    print(f"Output: {result}")
except Exception as e:
    sys.stdin, sys.stdout = old_stdin, old_stdout
    print(f"Error:")
    traceback.print_exc()
