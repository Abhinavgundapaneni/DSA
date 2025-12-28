"""Fix all DP test cases by regenerating outputs with editorial solutions."""

import yaml
import re
import os
from io import StringIO
import sys

def fix_problem(prob_num, fix_indices=None):
    """Fix test cases for a specific problem."""
    print(f"\nFixing {prob_num}...")
    
    # Extract editorial
    files = [f for f in os.listdir('dsa-problems/DP/editorials') if f.startswith(prob_num)]
    if not files:
        print(f"  No editorial found")
        return
    
    editorial_path = os.path.join('dsa-problems/DP/editorials', files[0])
    with open(editorial_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'### Python.*?```python\n(.*?)```'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"  No Python code found")
        return
    
    code = match.group(1)
    namespace = {}
    exec(code, namespace)
    
    # Load test file
    test_files = [f for f in os.listdir('dsa-problems/DP/testcases') if f.startswith(prob_num)]
    if not test_files:
        return
    
    test_path = os.path.join('dsa-problems/DP/testcases', test_files[0])
    with open(test_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Fix hidden tests
    hidden = data.get('hidden', [])
    fixed_count = 0
    
    for idx in (fix_indices or []):
        if idx >= len(hidden):
            continue
        
        tc = hidden[idx]
        if 'input' not in tc or 'output' not in tc:
            print(f"  Hidden[{idx}]: missing input/output")
            continue
        
        try:
            input_text = tc['input'].strip()
            old_output = tc['output'].strip()
            
            # Run editorial
            old_stdin, old_stdout = sys.stdin, sys.stdout
            sys.stdin = StringIO(input_text)
            sys.stdout = StringIO()
            
            namespace['main']()
            
            new_output = sys.stdout.getvalue().strip()
            sys.stdin, sys.stdout = old_stdin, old_stdout
            
            if new_output != old_output:
                hidden[idx]['output'] = new_output
                fixed_count += 1
                print(f"  Hidden[{idx}]: {old_output} -> {new_output}")
        except Exception as e:
            sys.stdin, sys.stdout = old_stdin, old_stdout
            print(f"  Hidden[{idx}]: ERROR - {str(e)[:100]}")
    
    if fixed_count > 0:
        # Save
        with open(test_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"  Fixed {fixed_count} test cases")
    else:
        print(f"  No changes needed")

# Fix each problem
fix_problem('DP-006', [35, 36, 37])
fix_problem('DP-008', [35, 36, 37])
fix_problem('DP-012', [35, 36])
fix_problem('DP-014', [35, 36, 37])
fix_problem('DP-016', [35, 36, 37, 38])

print("\nAll fixes complete!")
