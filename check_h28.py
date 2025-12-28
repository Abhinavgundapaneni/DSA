import yaml

tests=yaml.safe_load(open('dsa-problems/DP/testcases/DP-005-keyboard-row-edit-distance-shift.yaml', encoding='utf-8'))
print(repr(tests['hidden'][28]['input']))
print('Expected:', tests['hidden'][28]['output'])
