import yaml
from pathlib import Path

path = Path(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Strings\testcases\STR-013-run-length-decode-cap.yaml')
data = yaml.safe_load(open(path, encoding='utf-8'))
inp = data['hidden'][2]['input'].split('\n')[0]
cap = int(data['hidden'][2]['input'].split('\n')[1])
expected = data['hidden'][2]['output']

print('Input string:', repr(inp))
print('Cap:', cap)
print('Expected output length:', len(expected))
print()

# Parse manually
print('Manual parsing:')
i = 0
total = 0
while i < len(inp):
    char = inp[i]
    i += 1
    num = ''
    while i < len(inp) and inp[i].isdigit():
        num += inp[i]
        i += 1
    count = int(num) if num else 1
    actual_count = min(count, cap)
    print(f'  {char}{num} → {actual_count} {char}s')
    total += actual_count

print(f'\nTotal characters: {total}')
print(f'Expected: {len(expected)}')
print(f'Difference: {len(expected) - total}')

# Count in expected
from collections import Counter
print(f'\nExpected char counts: {Counter(expected)}')
