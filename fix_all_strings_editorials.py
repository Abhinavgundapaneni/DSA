#!/usr/bin/env python3
"""
Add main() functions and input/output handling to all Strings editorials.
"""
import re
from pathlib import Path

# Map of problem ID to I/O handling code
IO_HANDLERS = {
    "STR-001": '''
def main():
    import sys
    s = sys.stdin.read().strip()
    result = normalize_badge(s)
    print(result)

if __name__ == "__main__":
    main()
''',
    
    "STR-002": '''
def main():
    import sys
    s = sys.stdin.read().strip()
    result = can_rotate_to_palindrome(s)
    print("true" if result else "false")

if __name__ == "__main__":
    main()
''',
    
    "STR-003": '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    s = lines[0]
    k = int(lines[1])
    result = smallest_missing_substring(s, k)
    print(result)

if __name__ == "__main__":
    main()
''',
    
    "STR-004": '''
def main():
    import sys
    s = sys.stdin.read().strip()
    length, substring = longest_alternating_vc(s)
    print(length)
    print(substring)

if __name__ == "__main__":
    main()
''',
    
    "STR-005": '''
def main():
    import sys
    s = sys.stdin.read().strip()
    result = count_equal_distinct_splits(s)
    print(result)

if __name__ == "__main__":
    main()
''',
    
    "STR-006": '''
def main():
    import sys
    s = sys.stdin.read().strip()
    result = minimal_unique_rotation(s)
    print(result)

if __name__ == "__main__":
    main()
''',
    
    "STR-007": '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    s = lines[0]
    w = int(lines[1])
    result = compress_with_window(s, w)
    print(result)

if __name__ == "__main__":
    main()
''',
    
    "STR-008": '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    s = lines[0]
    p = lines[1]
    k = int(lines[2])
    result = count_k_mismatch_anagrams(s, p, k)
    print(result)

if __name__ == "__main__":
    main()
''',
    
    "STR-009": '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    L = int(lines[0])
    strings = lines[1:L+1]
    result = minimal_removal_unique_prefixes(L, strings)
    print(result)

if __name__ == "__main__":
    main()
''',
    
    "STR-010": '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    s = lines[0]
    k = int(lines[1])
    result = can_balance_with_skips(s, k)
    print("true" if result else "false")

if __name__ == "__main__":
    main()
''',
    
    "STR-011": '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    s = lines[0]
    L = int(lines[1])
    result = longest_chunked_decomposition(s, L)
    print(result)

if __name__ == "__main__":
    main()
''',
    
    "STR-012": '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    s = lines[0]
    max_freq = int(lines[1])
    MOD = 1000000007
    result = count_distinct_subsequences_with_limit(s, max_freq, MOD)
    print(result)

if __name__ == "__main__":
    main()
''',
    
    "STR-013": '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    s = lines[0]
    cap = int(lines[1])
    result = decode_with_cap(s, cap)
    print(result)

if __name__ == "__main__":
    main()
''',
    
    "STR-014": '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    arr = lines[1:n+1]
    k = int(lines[n+1])
    T = set(lines[n+2:n+2+k])
    count, window = shortest_covering_window(arr, T)
    print(count)
    for item in window:
        print(item)

if __name__ == "__main__":
    main()
''',
    
    "STR-015": '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    strings = lines[1:n+1]
    result = cyclic_shift_equivalence_classes(strings)
    print(result)

if __name__ == "__main__":
    main()
''',
    
    "STR-016": '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    s = lines[0]
    k = int(lines[1])
    result = minimal_delete_k_periodic(s, k)
    print(result)

if __name__ == "__main__":
    main()
'''
}

def fix_editorial(file_path, problem_id):
    """Add main() and if __name__ block to editorial."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has main()
    if 'if __name__ == "__main__"' in content:
        return False
    
    # Find the end of Python code block
    match = re.search(r'(### Python.*?```python\n.*?)(```)', content, re.DOTALL)
    if not match:
        print(f"  ⚠️  Could not find Python code block")
        return False
    
    # Insert main() before the closing ```
    io_handler = IO_HANDLERS.get(problem_id, '')
    if not io_handler:
        print(f"  ⚠️  No I/O handler defined for {problem_id}")
        return False
    
    new_content = content[:match.end(1)] + io_handler + '\n' + content[match.end(1):]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    base_path = Path(r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Strings\editorials")
    
    print("="*80)
    print("FIXING STRINGS EDITORIALS - ADDING I/O HANDLING")
    print("="*80)
    print()
    
    editorial_files = sorted(base_path.glob("STR-*.md"))
    success_count = 0
    
    for file_path in editorial_files:
        problem_id = file_path.stem.split('-')[0] + '-' + file_path.stem.split('-')[1]
        print(f"[{problem_id}] {file_path.name}")
        
        if fix_editorial(file_path, problem_id):
            print(f"  ✅ Added I/O handling")
            success_count += 1
        else:
            print(f"  ⏭️  Skipped (already has or error)")
    
    print()
    print("="*80)
    print(f"Fixed {success_count}/{len(editorial_files)} editorials")
    print("="*80)

if __name__ == "__main__":
    main()
