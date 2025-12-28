import yaml
import subprocess
import tempfile
import os

# Test QUE-002
with open('dsa-problems/Queues/testcases/QUE-002-circular-shuttle-buffer-overwrite.yaml', 'r') as f:
    data = yaml.safe_load(f)

# Extract Python editorial code
with open('dsa-problems/Queues/editorials/QUE-002-circular-shuttle-buffer-overwrite.md', 'r', encoding='utf-8') as f:
    content = f.read()
    py_start = content.find('### Python')
    py_code_start = content.find('```python', py_start)
    py_code_end = content.find('```', py_code_start + 10)
    py_code = content[py_code_start+10:py_code_end]

# Test sample 0
sample = data['samples'][0]
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(py_code)
    fname = f.name

result = subprocess.run(['python', fname], input=sample['input'], capture_output=True, text=True)
expected = sample['output'].strip()
actual = result.stdout.strip()

print('QUE-002 Sample 0:')
print(f'Expected:\n{expected}')
print(f'\nActual:\n{actual}')
print(f'\nMatch: {expected == actual}')

os.unlink(fname)
