import yaml

tests=yaml.safe_load(open('dsa-problems/Trees/testcases/TRE-001-campus-directory-multi-tree.yaml', encoding='utf-8'))
print('Sample 0 input:')
print(repr(tests['samples'][0]['input']))
print('\nExpected output:')
print(repr(tests['samples'][0]['output']))
