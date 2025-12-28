#!/usr/bin/env python3
"""Fix Stacks editorial Python sections to add I/O handling"""
from pathlib import Path
import re

editorials_dir = Path(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Stacks\editorials')

# Map of problem -> main() function code
main_functions = {
    'STK-001': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    m = int(lines[0])
    ops = []
    for i in range(1, m + 1):
        parts = lines[i].split()
        ops.append(parts)
    
    result = process(ops)
    for r in result:
        print(r)

if __name__ == "__main__":
    main()
''',
    'STK-002': '''
def main():
    import sys
    s = sys.stdin.read().strip()
    print(min_deletions(s))

if __name__ == "__main__":
    main()
''',
    'STK-003': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    pairs = []
    for i in range(1, n + 1):
        val, weight = map(int, lines[i].split())
        pairs.append((val, weight))
    
    print(weighted_deduplication(pairs))

if __name__ == "__main__":
    main()
''',
    'STK-004': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    heights = list(map(int, lines[1].split()))
    
    print(rooftop_sunset_count(heights))

if __name__ == "__main__":
    main()
''',
    'STK-005': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    
    result = next_taller_width(arr)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()
''',
    'STK-006': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    
    result = previous_greater_parity(arr)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()
''',
    'STK-007': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n, threshold = map(int, lines[0].split())
    prices = list(map(int, lines[1].split()))
    
    print(threshold_jump(prices, threshold))

if __name__ == "__main__":
    main()
''',
    'STK-008': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    
    result = token_climb_span(arr)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()
''',
    'STK-009': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    m = int(lines[0])
    ops = []
    for i in range(1, m + 1):
        parts = lines[i].split()
        ops.append(parts)
    
    result = sliding_min_stack(ops)
    for r in result:
        print(r)

if __name__ == "__main__":
    main()
''',
    'STK-010': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    m = int(lines[0])
    ops = []
    for i in range(1, m + 1):
        parts = lines[i].split()
        ops.append(parts)
    
    result = max_tracker(ops)
    for r in result:
        print(r)

if __name__ == "__main__":
    main()
''',
    'STK-011': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    tokens = lines[1].split()
    k = int(lines[2])
    variables = {}
    for i in range(3, 3 + k):
        var, val = lines[i].split()
        variables[var] = int(val)
    
    print(evaluate_postfix(tokens, variables))

if __name__ == "__main__":
    main()
''',
    'STK-012': '''
def main():
    import sys
    expression = sys.stdin.read().strip()
    print(infix_to_postfix(expression))

if __name__ == "__main__":
    main()
''',
    'STK-013': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    heights = list(map(int, lines[1].split()))
    
    print(max_rectangle_histogram(heights))

if __name__ == "__main__":
    main()
''',
    'STK-014': '''
def main():
    import sys
    s = sys.stdin.read().strip()
    print(is_valid_sequence(s))

if __name__ == "__main__":
    main()
''',
    'STK-015': '''
def main():
    import sys
    s = sys.stdin.read().strip()
    print(min_plates(s))

if __name__ == "__main__":
    main()
''',
    'STK-016': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    
    result = assembly_span_reset(arr)
    for r in result:
        print(r)

if __name__ == "__main__":
    main()
'''
}

for file in editorials_dir.glob('STK-*.md'):
    problem_id = file.stem[:7]  # e.g., 'STK-001'
    
    if problem_id not in main_functions:
        print(f"⚠️  No main function defined for {problem_id}")
        continue
    
    content = file.read_text(encoding='utf-8')
    
    # Find the Python section
    match = re.search(r'(### Python\s+```python\n.*?)\n```', content, re.DOTALL)
    
    if not match:
        print(f"⚠️  No Python section found in {file.name}")
        continue
    
    python_section = match.group(1)
    
    # Check if main() already exists
    if 'def main():' in python_section:
        print(f"✓ {file.name} already has main()")
        continue
    
    # Add main() and if __name__ block
    new_python_section = python_section + main_functions[problem_id]
    
    # Replace in content
    new_content = content.replace(python_section + '\n```', new_python_section + '\n```')
    
    file.write_text(new_content, encoding='utf-8')
    print(f"✅ Added main() to {file.name}")

print("\n✅ Completed fixing Stacks editorials")
