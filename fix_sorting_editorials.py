#!/usr/bin/env python3
"""
Find and fix function name mismatches in Sorting editorials.
"""

import os
import re

def check_and_fix_editorial(filepath):
    """Check if main() calls match function definitions and fix if needed."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract Python code section
    pattern = r'### Python.*?```python\n(.*?)```'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return None, "No Python code found"
    
    code = match.group(1)
    
    # Find all function definitions
    func_defs = re.findall(r'def\s+(\w+)\s*\(', code)
    if not func_defs:
        return None, "No functions found"
    
    # Find function calls in main()
    main_match = re.search(r'def main\(\):.*?(?=\ndef|\Z)', code, re.DOTALL)
    if not main_match:
        return None, "No main() found"
    
    main_code = main_match.group(0)
    
    # Find function calls (exclude builtins)
    func_calls = set(re.findall(r'(\w+)\s*\(', main_code))
    builtins = {'print', 'int', 'input', 'list', 'map', 'split', 'range', 'len', 'str', 'float', 'sorted', 'enumerate'}
    func_calls = func_calls - builtins - {'main'}
    
    # Check for mismatches
    undefined_calls = func_calls - set(func_defs)
    
    if not undefined_calls:
        return None, "OK"
    
    # Try to fix
    fixes = []
    for undefined in undefined_calls:
        # Find similar function names
        for defined in func_defs:
            if defined != 'main' and (undefined in defined or defined in undefined):
                fixes.append((undefined, defined))
                break
    
    if not fixes:
        return None, f"Undefined: {undefined_calls}, but no obvious fix"
    
    # Apply fixes
    new_content = content
    for old_name, new_name in fixes:
        # Replace in the Python code section
        old_code = match.group(0)
        new_code = re.sub(rf'\b{old_name}\s*\(', f'{new_name}(', old_code)
        new_content = new_content.replace(old_code, new_code)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return fixes, "Fixed"

# Check all SRT editorials
print("Checking Sorting editorials for function name mismatches...\n")

for i in range(4, 17):
    files = [f for f in os.listdir('dsa-problems/Sorting/editorials') if f.startswith(f'SRT-{i:03d}')]
    if not files:
        continue
    
    filepath = os.path.join('dsa-problems/Sorting/editorials', files[0])
    fixes, status = check_and_fix_editorial(filepath)
    
    if fixes:
        print(f"SRT-{i:03d}: Fixed {fixes}")
    elif status == "OK":
        print(f"SRT-{i:03d}: ✓ OK")
    else:
        print(f"SRT-{i:03d}: ⚠️  {status}")
