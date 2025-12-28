import re
import subprocess
import tempfile
import sys
import os

# Extract code exactly like test framework does
with open('dsa-problems/MathAdvanced/editorials/MTH-001-polynomial-multiplication-fft.md', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'### Python.*?```python\n(.*?)```'
match = re.search(pattern, content, re.DOTALL)
solution_code = match.group(1)

# Test input
test_input = """2 2
1 2
3 4"""

# Run exactly like test framework
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(solution_code)
    temp_file = f.name

try:
    result = subprocess.run(
        [sys.executable, temp_file],
        input=test_input,
        capture_output=True,
        text=True,
        timeout=10
    )
    
    print(f"Return code: {result.returncode}")
    print(f"Stdout: '{result.stdout.strip()}'")
    print(f"Stderr: '{result.stderr.strip()}'")
    
finally:
    os.unlink(temp_file)
