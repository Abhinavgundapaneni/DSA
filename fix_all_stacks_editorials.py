#!/usr/bin/env python3
"""Add I/O handling to all Stacks editorial files"""
from pathlib import Path

editorials_dir = Path(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Stacks\editorials')

# STK-001: Notebook Undo Simulator
stk001 = '''

def process(ops):
    result = []
    stack = []
    
    for op in ops:
        command = op[0]
        
        if command == "PUSH":
            stack.append(op[1])
        elif command == "POP":
            if len(stack) == 0:
                result.append("EMPTY")
            else:
                result.append(stack.pop())
        elif command == "TOP":
            if len(stack) == 0:
                result.append("EMPTY")
            else:
                result.append(stack[-1])
    
    return result

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
'''

# STK-002: Lab Mixed Bracket Repair
stk002 = '''

def min_deletions(s):
    stack = []
    deletions = 0
    
    for char in s:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if stack:
                stack.pop()
            else:
                deletions += 1
    
    deletions += len(stack)
    return deletions

def main():
    import sys
    s = sys.stdin.read().strip()
    print(min_deletions(s))

if __name__ == "__main__":
    main()
'''

# STK-003: Conveyor Weighted Deduplication
stk003 = '''

def weighted_deduplication(pairs):
    stack = []
    
    for val, weight in pairs:
        if stack and stack[-1][0] == val:
            stack[-1] = (val, stack[-1][1] + weight)
        else:
            stack.append((val, weight))
    
    if not stack:
        return "EMPTY"
    return " ".join(f"{val},{weight}" for val, weight in stack)

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
'''

# STK-004: Rooftop Sunset Count
stk004 = '''

def rooftop_sunset_count(heights):
    stack = []
    count = 0
    
    for h in heights:
        while stack and stack[-1] <= h:
            stack.pop()
        stack.append(h)
    
    return len(stack)

def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    heights = list(map(int, lines[1].split()))
    
    print(rooftop_sunset_count(heights))

if __name__ == "__main__":
    main()
'''

# STK-005: Workshop Next Taller Width
stk005 = '''

def next_taller_width(arr):
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)
    
    return result

def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    
    result = next_taller_width(arr)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()
'''

# STK-006: Assembly Previous Greater Parity
stk006 = '''

def previous_greater_parity(arr):
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        
        if stack:
            result[i] = stack[-1]
        
        stack.append(i)
    
    return result

def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    
    result = previous_greater_parity(arr)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()
'''

# STK-007: Trading Desk Threshold Jump
stk007 = '''

def threshold_jump(prices, threshold):
    count = 0
    stack = []
    
    for price in prices:
        while stack and stack[-1] <= price - threshold:
            stack.pop()
            count += 1
        stack.append(price)
    
    return count

def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n, threshold = map(int, lines[0].split())
    prices = list(map(int, lines[1].split()))
    
    print(threshold_jump(prices, threshold))

if __name__ == "__main__":
    main()
'''

# STK-008: Canteen Token Climb Span
stk008 = '''

def token_climb_span(arr):
    n = len(arr)
    result = [1] * n
    stack = []
    
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        
        if stack:
            result[i] = i - stack[-1]
        else:
            result[i] = i + 1
        
        stack.append(i)
    
    return result

def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    
    result = token_climb_span(arr)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()
'''

# STK-009: Lab Sliding Min Stack
stk009 = '''

def sliding_min_stack(ops):
    stack = []
    min_stack = []
    result = []
    
    for op in ops:
        cmd = op[0]
        
        if cmd == "PUSH":
            val = int(op[1])
            stack.append(val)
            if not min_stack or val <= min_stack[-1]:
                min_stack.append(val)
            else:
                min_stack.append(min_stack[-1])
        
        elif cmd == "POP":
            if stack:
                stack.pop()
                min_stack.pop()
        
        elif cmd == "MIN":
            if min_stack:
                result.append(min_stack[-1])
    
    return result

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
'''

# STK-010: Stadium Max Tracker
stk010 = '''

def max_tracker(ops):
    stack = []
    max_stack = []
    result = []
    
    for op in ops:
        cmd = op[0]
        
        if cmd == "PUSH":
            val = int(op[1])
            stack.append(val)
            if not max_stack or val >= max_stack[-1]:
                max_stack.append(val)
            else:
                max_stack.append(max_stack[-1])
        
        elif cmd == "POP":
            if stack:
                stack.pop()
                max_stack.pop()
        
        elif cmd == "MAX":
            if max_stack:
                result.append(max_stack[-1])
            else:
                result.append("EMPTY")
    
    return result

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
'''

# STK-011: Circuit Postfix Variables
stk011 = '''

def evaluate_postfix(tokens, variables):
    stack = []
    MOD = 10**9 + 7
    
    for token in tokens:
        if token in ['+', '-', '*']:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append((a + b) % MOD)
            elif token == '-':
                stack.append((a - b) % MOD)
            elif token == '*':
                stack.append((a * b) % MOD)
        else:
            stack.append(variables[token])
    
    return stack[0]

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
'''

# STK-012: Campus Expression Optimizer
stk012 = '''

def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = []
    result = []
    
    tokens = expression.split()
    
    for token in tokens:
        if token.isalpha():
            result.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(token, 0):
                result.append(stack.pop())
            stack.append(token)
    
    while stack:
        result.append(stack.pop())
    
    return ' '.join(result)

def main():
    import sys
    expression = sys.stdin.read().strip()
    print(infix_to_postfix(expression))

if __name__ == "__main__":
    main()
'''

# STK-013: Auditorium Histogram One Booster
stk013 = '''

def max_rectangle_histogram(heights):
    stack = []
    max_area = 0
    
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height_idx = stack.pop()
            height = heights[height_idx]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    
    while stack:
        height_idx = stack.pop()
        height = heights[height_idx]
        width = len(heights) if not stack else len(heights) - stack[-1] - 1
        max_area = max(max_area, height * width)
    
    return max_area

def main():
    import sys
    lines = sys.stdin.read().strip().split('\\n')
    n = int(lines[0])
    heights = list(map(int, lines[1].split()))
    
    print(max_rectangle_histogram(heights))

if __name__ == "__main__":
    main()
'''

# STK-014: Shuttle Validation Time Windows
stk014 = '''

def is_valid_sequence(s):
    stack = []
    matching = {'(': ')', '[': ']', '{': '}'}
    
    for char in s:
        if char in matching:
            stack.append(char)
        else:
            if not stack or matching[stack[-1]] != char:
                return "INVALID"
            stack.pop()
    
    return "VALID" if not stack else "INVALID"

def main():
    import sys
    s = sys.stdin.read().strip()
    print(is_valid_sequence(s))

if __name__ == "__main__":
    main()
'''

# STK-015: Bike Repair Plates
stk015 = '''

def min_plates(s):
    stack = []
    plates = 0
    
    for char in s:
        if char == '(':
            stack.append(char)
        else:
            if stack:
                stack.pop()
            else:
                plates += 1
    
    return plates

def main():
    import sys
    s = sys.stdin.read().strip()
    print(min_plates(s))

if __name__ == "__main__":
    main()
'''

# STK-016: Assembly Line Span Reset
stk016 = '''

def assembly_span_reset(arr):
    n = len(arr)
    result = []
    stack = []
    
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        
        if stack:
            result.append(i - stack[-1])
        else:
            result.append(i + 1)
        
        stack.append(i)
    
    return result

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

implementations = {
    'STK-001-notebook-undo-simulator.md': stk001,
    'STK-002-lab-mixed-bracket-repair.md': stk002,
    'STK-003-conveyor-weighted-deduplication.md': stk003,
    'STK-004-rooftop-sunset-count.md': stk004,
    'STK-005-workshop-next-taller-width.md': stk005,
    'STK-006-assembly-previous-greater-parity.md': stk006,
    'STK-007-trading-desk-threshold-jump.md': stk007,
    'STK-008-canteen-token-climb-span.md': stk008,
    'STK-009-lab-sliding-min-stack.md': stk009,
    'STK-010-stadium-max-tracker.md': stk010,
    'STK-011-circuit-postfix-variables.md': stk011,
    'STK-012-campus-expression-optimizer.md': stk012,
    'STK-013-auditorium-histogram-one-booster.md': stk013,
    'STK-014-shuttle-validation-time-windows.md': stk014,
    'STK-015-bike-repair-plates.md': stk015,
    'STK-016-assembly-line-span-reset.md': stk016,
}

for filename, code in implementations.items():
    filepath = editorials_dir / filename
    content = filepath.read_text(encoding='utf-8')
    
    # Append Python implementation before the last closing backticks
    if '```' in content and 'def main():' not in content:
        # Find the last ``` (usually end of JavaScript section)
        parts = content.rsplit('```', 1)
        new_content = parts[0] + '```\n\n### Python\n\n```python' + code + '\n```' + parts[1]
        
        filepath.write_text(new_content, encoding='utf-8')
        print(f"✅ Added Python implementation to {filename}")
    else:
        print(f"⚠️  Skipped {filename} (already has Python or no code blocks)")

print(f"\n✅ Completed processing {len(implementations)} Stacks editorial files")
