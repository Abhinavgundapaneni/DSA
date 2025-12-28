import yaml

with open('dsa-problems/DP/testcases/DP-005-keyboard-row-edit-distance-shift.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

public = data.get('public', [])
hidden = data.get('hidden', [])

print('Public tests:')
for i, tc in enumerate(public):
    has_out = 'output' in tc
    print(f'  [{i}] output={has_out}')

print(f'\nHidden tests 17-19:')
for i in [17, 18, 19]:
    if i < len(hidden):
        has_out = 'output' in hidden[i]
        print(f'  [{i}] output={has_out}')
