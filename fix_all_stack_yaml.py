import yaml
import os

# Files that might have the \n issue (multiline inputs/outputs)
files_to_fix = [
    './dsa-problems/Stacks/testcases/STK-005-workshop-next-taller-width.yaml',
    './dsa-problems/Stacks/testcases/STK-007-trading-desk-threshold-jump.yaml',
    './dsa-problems/Stacks/testcases/STK-009-lab-sliding-min-stack.yaml'
]

def fix_yaml_file(filepath):
    """Fix YAML file to have actual newlines instead of escaped \\n"""
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} - not found")
        return False
    
    # Read the YAML file
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    
    # Check if any test case has \n in input or output
    has_issue = False
    for category in ['samples', 'public', 'hidden']:
        if category in data:
            for tc in data[category]:
                if '\\n' in tc.get('input', '') or '\\n' in tc.get('output', ''):
                    has_issue = True
                    break
    
    if not has_issue:
        print(f"Skipping {filepath} - no \\n found")
        return False
    
    # Fix all test cases
    for category in ['samples', 'public', 'hidden']:
        if category in data:
            for tc in data[category]:
                if '\\n' in tc['input']:
                    tc['input'] = tc['input'].replace('\\n', '\n')
                if '\\n' in tc['output']:
                    tc['output'] = tc['output'].replace('\\n', '\n')
    
    # Write back with proper formatting
    with open(filepath, 'w') as f:
        # Write problem_id
        f.write(f"problem_id: {data['problem_id']}\n")
        
        for category in ['samples', 'public', 'hidden']:
            if category not in data:
                continue
            f.write(f"{category}:\n")
            for tc in data[category]:
                # Use multiline format if input has newlines
                if '\n' in tc['input']:
                    f.write("- input: |\n")
                    for line in tc['input'].split('\n'):
                        f.write(f"    {line}\n")
                else:
                    f.write(f"- input: {tc['input']}\n")
                
                # Use multiline format if output has newlines
                if '\n' in tc['output']:
                    f.write("  output: |\n")
                    for line in tc['output'].split('\n'):
                        f.write(f"    {line}\n")
                else:
                    f.write(f"  output: {tc['output']}\n")
    
    print(f"Fixed {filepath}")
    return True

# Fix all files
for filepath in files_to_fix:
    fix_yaml_file(filepath)

print("\nDone fixing YAML files")
