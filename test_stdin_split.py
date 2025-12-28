import subprocess
import sys

code = '''import sys
lines = sys.stdin.read().strip().split('\\n')
print(f"Number of lines: {len(lines)}")
for i, line in enumerate(lines):
    print(f"Line {i}: {repr(line)}")
'''

with open('test_stdin.py', 'w') as f:
    f.write(code)

# Test with the actual input from test case
test_input = 'aabba\\n1 2 3 1 2'
print(f"Input: {repr(test_input)}")
print()

result = subprocess.run([sys.executable, 'test_stdin.py'], 
                       input=test_input, capture_output=True, text=True)
print("Output:")
print(result.stdout)
if result.stderr:
    print("Errors:")
    print(result.stderr)
