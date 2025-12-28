test_input = """2 3
1 1"""

lines = test_input.strip().split('\n')
print(f"Line 1: {lines[0]}")
print(f"Line 2: {lines[1]}")

# Parse
parts_line1 = lines[0].split()
parts_line2 = lines[1].split()

print(f"\nLine 1 parts: {parts_line1}")
print(f"Line 2 parts: {parts_line2}")

# Expected format: k n P[0]...P[k-1] MOD
# But test has:
# Line 1: k n
# Line 2: P[0]...P[k-1] (maybe MOD too?)

# Let's check the editorial expectation
print(f"\nk={parts_line1[0]}, n={parts_line1[1]}")
print(f"P values: {parts_line2}")
print(f"Total values in line 2: {len(parts_line2)}")
