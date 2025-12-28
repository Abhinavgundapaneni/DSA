#!/usr/bin/env python3
"""
Fix remaining Strings editorial issues and regenerate test cases.
"""
import yaml
from pathlib import Path

def can_rotate_to_palindrome(s):
    """Check if any rotation IS a palindrome."""
    n = len(s)
    for i in range(n):
        rotation = s[i:] + s[:i]
        if rotation == rotation[::-1]:
            return True
    return False

def regenerate_str002_tests():
    """Regenerate STR-002 tests with correct rotation logic."""
    
    test_cases = {
        'problem_id': 'STR_LAB_CODE_PALINDROME_ROTATE__1002',
        'samples': [],
        'public': [],
        'hidden': []
    }
    
    # Samples
    samples = ['aab', 'abc']
    for s in samples:
        result = can_rotate_to_palindrome(s)
        test_cases['samples'].append({
            'input': s,
            'output': 'true' if result else 'false'
        })
    
    # Public
    public = ['racecar', 'aabbcc', 'a', 'aa', 'abcd']
    for s in public:
        result = can_rotate_to_palindrome(s)
        test_cases['public'].append({
            'input': s,
            'output': 'true' if result else 'false'
        })
    
    # Hidden - use correct rotation logic
    hidden = [
        'aabbccddee', 'aabbccddeeff', 'aabbccddee', 'aabbccddeea',
        'zzz', 'a', 'aa', 'ab', 'aba', 'abc', 'aab', 'baa',
        'abcd', 'abcba', 'racecar', 'noon', 'level', 'aaa',
        'aaaa', 'aaaaa', 'xyz', 'test', 'abcdefg', 'palindrome',
        'rotated', 'example', 'mississippi', 'rotations',
        'abcabc', 'xyzzyx', 'aabbcc', 'testtest', 'longstring', 'minimal'
    ]
    
    for s in hidden:
        result = can_rotate_to_palindrome(s)
        test_cases['hidden'].append({
            'input': s,
            'output': 'true' if result else 'false'
        })
    
    # Save
    output_path = Path(r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Strings\testcases\STR-002-lab-code-palindrome-rotate.yaml")
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(test_cases, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"✅ Regenerated STR-002 with {len(test_cases['samples'])} samples, {len(test_cases['public'])} public, {len(test_cases['hidden'])} hidden")

if __name__ == "__main__":
    print("="*80)
    print("FIXING REMAINING STRINGS PROBLEMS")
    print("="*80)
    print()
    
    print("[1/4] Regenerating STR-002 test cases...")
    regenerate_str002_tests()
    
    print("\n" + "="*80)
    print("Fixes complete! Run test_topic_editorials.py STRINGS to validate")
    print("="*80)
