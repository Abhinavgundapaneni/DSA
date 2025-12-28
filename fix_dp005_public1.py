import yaml

test_file = 'dsa-problems/DP/testcases/DP-005-keyboard-row-edit-distance-shift.yaml'
with open(test_file, 'r', encoding='utf-8') as f:
    tests = yaml.safe_load(f)

print(f'Before: public[1] input = {repr(tests["public"][1]["input"])}')

# Fix public[1] to have "abc\n\n" (abc followed by empty line, then newline)
tests['public'][1]['input'] = 'abc\n\n'

print(f'After: public[1] input = {repr(tests["public"][1]["input"])}')

# Write back
with open(test_file, 'w', encoding='utf-8') as f:
    yaml.dump(tests, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)

print(f'Updated {test_file}')
