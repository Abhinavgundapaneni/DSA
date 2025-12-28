test_input = """10
11
0 7
2 4
1 5
1 8
0 9
1 4
6 7
2 9
4 8
0 5
2 5"""

# Try to parse
lines = test_input.strip().split('\n')
n = int(lines[0])
m = int(lines[1])

print(f"n={n}, m={m}")
print(f"Total lines: {len(lines)}, expected m={m}")
print("First few edge lines:")
for i in range(2, min(7, len(lines))):
    parts = lines[i].split()
    print(f"  Line {i}: {parts} ({len(parts)} parts)")
