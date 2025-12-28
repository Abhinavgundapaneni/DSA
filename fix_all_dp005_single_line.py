import yaml

test_file = 'dsa-problems/DP/testcases/DP-005-keyboard-row-edit-distance-shift.yaml'
with open(test_file, 'r', encoding='utf-8') as f:
    tests = yaml.safe_load(f)

fixed = 0
for i, tc in enumerate(tests['hidden']):
    inp = tc['input']
    lines = inp.split('\n')
    # If input has only 1 line (or 1 line + empty string), add newline
    if len(lines) < 2 or (len(lines) == 2 and lines[1] == ''):
        tc['input'] = inp.rstrip('\n') + '\n\n'
        fixed += 1
        print(f'Fixed hidden[{i}]: {repr(inp)} -> {repr(tc["input"])}')

print(f'\nTotal fixed: {fixed}')

# Write back
with open(test_file, 'w', encoding='utf-8') as f:
    yaml.dump(tests, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)

print(f'Updated {test_file}')
