import sys
lines = sys.stdin.read().strip().split('\n')
print(f"Number of lines: {len(lines)}")
for i, line in enumerate(lines):
    print(f"Line {i}: {repr(line)}")
