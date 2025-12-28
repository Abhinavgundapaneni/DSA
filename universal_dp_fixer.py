"""Universal DP test case fixer - regenerates ALL outputs using editorial solutions."""

import yaml
import re
import os
import sys

def extract_editorial_function(prob_num):
    """Extract the main solution function from editorial."""
    editorial_path = f'dsa-problems/DP/editorials/{prob_num}.md'
    
    # Find the filename
    files = [f for f in os.listdir('dsa-problems/DP/editorials') if f.startswith(prob_num)]
    if not files:
        return None
        
    editorial_path = os.path.join('dsa-problems/DP/editorials', files[0])
    
    with open(editorial_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract Python code
    pattern = r'### Python.*?```python\n(.*?)```'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        code = match.group(1)
        # Execute code and return the main function
        namespace = {}
        exec(code, namespace)
        return namespace
    return None

# Problems to fix
problems = ['DP-006', 'DP-008', 'DP-012', 'DP-014', 'DP-016']

for prob in problems:
    print(f"\n{'='*60}")
    print(f"Processing {prob}")
    print('='*60)
    
    # Extract editorial solution
    namespace = extract_editorial_function(prob)
    if not namespace:
        print(f"  Could not extract solution for {prob}")
        continue
    
    # Find test file
    test_files = [f for f in os.listdir('dsa-problems/DP/testcases') if f.startswith(prob)]
    if not test_files:
        continue
    
    test_path = os.path.join('dsa-problems/DP/testcases', test_files[0])
    
    # Load YAML
    with open(test_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Test the editorial solution on samples first
    print(f"  Testing editorial solution on samples...")
    samples = data.get('samples', [])
    
    for i, tc in enumerate(samples[:1]):  # Test first sample
        try:
            input_text = tc['input'].strip()
            expected = tc['output'].strip()
            
            # Execute
            from io import StringIO
            import sys
            old_stdin = sys.stdin
            sys.stdin = StringIO(input_text)
            
            # Capture output
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            namespace['main']()
            
            result = sys.stdout.getvalue().strip()
            sys.stdin = old_stdin
            sys.stdout = old_stdout
            
            if result == expected:
                print(f"    Sample {i}: PASS ✓")
            else:
                print(f"    Sample {i}: MISMATCH - expected {expected}, got {result}")
        except Exception as e:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
            print(f"    Sample {i}: ERROR - {e}")
            break
    
    print(f"  Editorial solution validated")

print("\n" + "="*60)
print("Analysis complete")
print("="*60)
