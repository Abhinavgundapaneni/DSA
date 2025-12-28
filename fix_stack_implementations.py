#!/usr/bin/env python3
"""
COMPREHENSIVE Stack Editorials Fix
Fixes all Python implementations to match regenerated test cases
Being truthful: Most editorials had bugs or wrong algorithms!
"""
from pathlib import Path
import re

ed_dir = Path(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Stacks\editorials')

# Correct implementations for each problem

implementations = {
    'STK-002': '''def can_repair(s: str) -> bool:
    """Check if wildcards can balance brackets"""
    stack = []
    stars = []
    
    pairs = {')': '(', ']': '[', '}': '{'}
    
    for i, c in enumerate(s):
        if c in '([{':
            stack.append((c, i))
        elif c == '?':
            stars.append(i)
        else:
            if stack and stack[-1][0] == pairs[c]:
                stack.pop()
            elif stars:
                stars.pop()
            else:
                return False
    
    while stack and stars:
        if stack[-1][1] < stars[-1]:
            stack.pop()
            stars.pop()
        else:
            break
    
    return not stack''',

    'STK-003': '''def weighted_dedup(s: str, weights: list[int]) -> tuple[str, int]:
    """Remove adjacent matching chars if weight sum is even"""
    stack = []
    total_removed = 0
    
    for i, c in enumerate(s):
        if stack and stack[-1][0] == c:
            if (stack[-1][1] + weights[i]) % 2 == 0:
                total_removed += stack[-1][1] + weights[i]
                stack.pop()
            else:
                stack.append((c, weights[i]))
        else:
            stack.append((c, weights[i]))
    
    reduced = ''.join(c for c, w in stack)
    if not reduced:
        reduced = "EMPTY"
    
    return reduced, total_removed''',

    'STK-005': '''def next_taller_within_width(heights: list[int], w: int) -> list[int]:
    """Find next taller height within distance w"""
    n = len(heights)
    result = []
    
    for i in range(n):
        found = -1
        for j in range(i + 1, min(i + w + 1, n)):
            if heights[j] > heights[i]:
                found = heights[j]
                break
        result.append(found)
    
    return result''',

    'STK-007': '''def threshold_jump_steps(prices: list[int], threshold: int) -> list[int]:
    """For each position, find steps to threshold jump"""
    n = len(prices)
    result = []
    
    for i in range(n):
        target = prices[i] + threshold
        steps = 0
        for j in range(i + 1, n):
            if prices[j] >= target:
                steps = j - i
                break
        result.append(steps)
    
    return result''',

    'STK-009': '''def min_stack_ops(ops: list[list[str]]) -> list[str]:
    """Process MIN k operations on stack"""
    stack = []
    result = []
    
    for op in ops:
        if op[0] == "PUSH":
            stack.append(int(op[1]))
        elif op[0] == "POP":
            if stack:
                result.append(str(stack.pop()))
            else:
                result.append("EMPTY")
        elif op[0] == "MIN":
            k = int(op[1])
            if len(stack) >= k:
                result.append(str(min(stack[-k:])))
            else:
                result.append("EMPTY")
    
    return result''',
}

# Main functions for I/O handling

main_functions = {
    'STK-002': '''
def main():
    import sys
    s = sys.stdin.read().strip()
    result = can_repair(s)
    print("true" if result else "false")

if __name__ == "__main__":
    main()''',

    'STK-003': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    s = lines[0]
    weights = list(map(int, lines[1].split()))
    reduced, total = weighted_dedup(s, weights)
    print(reduced)
    print(total)

if __name__ == "__main__":
    main()''',

    'STK-005': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n, w = map(int, lines[0].split())
    heights = list(map(int, lines[1].split()))
    result = next_taller_within_width(heights, w)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()''',

    'STK-007': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n, threshold = map(int, lines[0].split())
    prices = list(map(int, lines[1].split()))
    result = threshold_jump_steps(prices, threshold)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()''',

    'STK-009': '''
def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    m = int(lines[0])
    ops = []
    for i in range(1, m + 1):
        ops.append(lines[i].split())
    result = min_stack_ops(ops)
    for r in result:
        print(r)

if __name__ == "__main__":
    main()''',
}

print("Fixing Stack editorial implementations...")
print("=" * 80)

for problem_id, impl_code in implementations.items():
    # Find editorial file
    files = list(ed_dir.glob(f'{problem_id}-*.md'))
    if not files:
        print(f"⚠️  {problem_id}: File not found")
        continue
    
    file = files[0]
    content = file.read_text(encoding='utf-8')
    
    # Find Python section
    match = re.search(r'### Python\s+```python\n(.*?)\n```', content, re.DOTALL)
    if not match:
        print(f"⚠️  {problem_id}: No Python section found")
        continue
    
    old_python = match.group(1)
    
    # Replace with correct implementation + main
    new_python = impl_code + '\\n' + main_functions[problem_id]
    
    new_content = content.replace(
        f'### Python\\n\\n```python\\n{old_python}\\n```',
        f'### Python\\n\\n```python\\n{new_python}\\n```'
    )
    
    file.write_text(new_content, encoding='utf-8')
    print(f"✅ {problem_id}: Fixed implementation")

print("\\n" + "=" * 80)
print("COMPLETE! Fixed 5 Stack editorials with correct implementations")
