"""Check all DP test files for missing outputs."""
import yaml
import os

problems = ['DP-005', 'DP-006', 'DP-008', 'DP-009', 'DP-012', 'DP-014', 'DP-016']

for prob in problems:
    yaml_files = [f for f in os.listdir('dsa-problems/DP/testcases') if f.startswith(prob)]
    if not yaml_files:
        continue
    
    filepath = os.path.join('dsa-problems/DP/testcases', yaml_files[0])
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        samples = data.get('samples', [])
        public = data.get('public', [])
        hidden = data.get('hidden', [])
        
        missing_sample = [i for i, tc in enumerate(samples) if 'output' not in tc]
        missing_public = [i for i, tc in enumerate(public) if 'output' not in tc]
        missing_hidden = [i for i, tc in enumerate(hidden) if 'output' not in tc]
        
        print(f'\n{prob}:')
        print(f'  Samples: {len(samples)} tests, missing output: {missing_sample}')
        print(f'  Public: {len(public)} tests, missing output: {missing_public}')
        print(f'  Hidden: {len(hidden)} tests, missing output: {missing_hidden}')
        
    except Exception as e:
        print(f'\n{prob}: ERROR - {e}')
