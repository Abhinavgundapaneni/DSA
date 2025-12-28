import yaml

tests=yaml.safe_load(open('dsa-problems/Trees/testcases/TRE-001-campus-directory-multi-tree.yaml', encoding='utf-8'))
print('Public[0] output:')
print(tests['public'][0]['output'])
print('\n---\nLines:', len(tests['public'][0]['output'].split('\n')))
