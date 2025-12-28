import yaml

test_file = 'dsa-problems/DP/testcases/DP-005-keyboard-row-edit-distance-shift.yaml'
with open(test_file, 'r', encoding='utf-8') as f:
    tests = yaml.safe_load(f)

print("Public[1] input:")
print(repr(tests['public'][1]['input']))
print("\nSplit by lines:")
lines = tests['public'][1]['input'].split('\n')
for i, line in enumerate(lines):
    print(f"  Line {i}: {repr(line)}")
