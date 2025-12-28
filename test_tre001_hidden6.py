import yaml
import re
import sys
from io import StringIO

# Load editorial
with open('dsa-problems/Trees/editorials/TRE-001-campus-directory-multi-tree.md', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'### Python.*?```python\n(.*?)```', content, re.DOTALL)
code = match.group(1)

namespace = {}
exec(code, namespace)
main = namespace['main']

# Load test
tests = yaml.safe_load(open('dsa-problems/Trees/testcases/TRE-001-campus-directory-multi-tree.yaml', encoding='utf-8'))
inp = tests['hidden'][6]['input']
expected = tests['hidden'][6]['output']

# Run editorial
sys.stdin = StringIO(inp)
old_stdout = sys.stdout
sys.stdout = StringIO()

main()
result = sys.stdout.getvalue()

sys.stdout = old_stdout

print('Expected:')
print(expected)
print('\nActual:')
print(result)
print('\nMatch:', result.strip() == expected.strip())
