import yaml

problems_to_check = [
    'GRD-004-library-power-backup',
    'GRD-005-shuttle-overtime-minimizer',
    'GRD-006-robotics-component-bundling-loss-quality',
    'GRD-007-campus-wifi-expansion',
    'GRD-009-shuttle-refuel-with-refund',
    'GRD-011-campus-event-ticket-caps',
    'GRD-014-festival-bandwidth-split',
    'GRD-016-shuttle-schedule-delay-minimizer',
]

for problem in problems_to_check:
    yaml_path = f'dsa-problems/Greedy/testcases/{problem}.yaml'
    
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # Get first sample
        if data and 'samples' in data and len(data['samples']) > 0:
            sample = data['samples'][0]
            print(f"\n{problem}:")
            print(f"  Input: {sample['input'][:100]}...")
            print(f"  Correct Output: {sample['output']}")
    except Exception as e:
        print(f"\n{problem}: Error - {e}")
