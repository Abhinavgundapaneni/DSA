import yaml

test_file = 'dsa-problems/DP/testcases/DP-005-keyboard-row-edit-distance-shift.yaml'
with open(test_file, 'r', encoding='utf-8') as f:
    tests = yaml.safe_load(f)

print('Before fixes:')
print(f'Hidden[17]: {repr(tests["hidden"][17]["input"])}')
print(f'Hidden[18]: {repr(tests["hidden"][18]["input"])}')
print(f'Hidden[28]: {repr(tests["hidden"][28]["input"])}')

# Fix hidden[17]: "string\n" -> "string\n\n"
tests['hidden'][17]['input'] += '\n'

# Fix hidden[18]: "\n" -> "\n\n"
tests['hidden'][18]['input'] += '\n'

print('\nAfter fixes:')
print(f'Hidden[17]: {repr(tests["hidden"][17]["input"])}')
print(f'Hidden[18]: {repr(tests["hidden"][18]["input"])}')

# Write back
with open(test_file, 'w', encoding='utf-8') as f:
    yaml.dump(tests, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=999999)

print(f'\nUpdated {test_file}')
