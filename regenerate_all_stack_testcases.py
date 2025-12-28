#!/usr/bin/env python3
"""
Regenerate ALL Stack test cases to match their problem statements
Being truthful: Most test cases don't match the problem statements!
"""
import yaml
import random
from pathlib import Path

random.seed(42)

tc_dir = Path(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Stacks\testcases')

# STK-002: Wildcard bracket matching (true/false)
def can_balance_wildcards(s):
    """Check if wildcards can make brackets balanced"""
    # Greedy approach: try to match brackets, use wildcards as needed
    stack = []
    stars = []
    
    for i, c in enumerate(s):
        if c in '([{':
            stack.append((c, i))
        elif c == '?':
            stars.append(i)
        else:
            matching = {')': '(', ']': '[', '}': '{'}
            if stack and stack[-1][0] == matching[c]:
                stack.pop()
            elif stars:
                stars.pop()
            else:
                return "false"
    
    # Match remaining opens with stars
    while stack and stars:
        if stack[-1][1] < stars[-1]:
            stack.pop()
            stars.pop()
        else:
            break
    
    return "true" if not stack else "false"

# STK-003: Weighted deduplication with even-sum removal
def weighted_dedup_even_sum(s, weights):
    """Remove matching adjacent chars if weight sum is even"""
    stack = []
    total_removed = 0
    
    for i, c in enumerate(s):
        if stack and stack[-1][0] == c:
            if (stack[-1][1] + weights[i]) % 2 == 0:
                removed_weight = stack[-1][1] + weights[i]
                total_removed += removed_weight
                stack.pop()
            else:
                stack.append((c, weights[i]))
        else:
            stack.append((c, weights[i]))
    
    reduced = ''.join(c for c, w in stack)
    return f"{reduced if reduced else 'EMPTY'}\\n{total_removed}"

# STK-005: Next taller within width w
def next_taller_width(heights, w):
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
    
    return result

# STK-007: Steps to threshold jump (array output)
def threshold_jump_steps(prices, threshold):
    """For each position, find steps to price >= threshold higher"""
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
    
    return result

# STK-009: Min-stack with MIN k operation
def min_stack_operations(ops):
    """Process stack operations including MIN k"""
    stack = []
    result = []
    
    for op in ops:
        cmd = op[0]
        if cmd == "PUSH":
            stack.append(int(op[1]))
        elif cmd == "POP":
            if stack:
                result.append(str(stack.pop()))
            else:
                result.append("EMPTY")
        elif cmd == "MIN":
            k = int(op[1])
            if len(stack) >= k:
                top_k = stack[-k:]
                result.append(str(min(top_k)))
            else:
                result.append("EMPTY")
    
    return result

print("Regenerating Stack test cases to match problem statements...")
print("=" * 80)

# STK-002: Wildcard brackets
tc_002 = {'problem_id': 'STK_LAB_MIXED_BRACKET_REPAIR__7391', 'samples': [], 'public': [], 'hidden': []}

samples_002 = [
    "(?[?])?",  # true
    "(()]",     # true  
    "([)]",     # false
]

for s in samples_002:
    tc_002['samples'].append({'input': s, 'output': can_balance_wildcards(s)})

# Add public and hidden test cases
public_002 = ["()", "([{}])", "(?)", "((", "?"]
for s in public_002:
    tc_002['public'].append({'input': s, 'output': can_balance_wildcards(s)})

# Generate 30 hidden test cases
for _ in range(30):
    length = random.randint(1, 20)
    chars = random.choices(['(', ')', '[', ']', '{', '}', '?'], k=length)
    s = ''.join(chars)
    tc_002['hidden'].append({'input': s, 'output': can_balance_wildcards(s)})

with open(tc_dir / 'STK-002-lab-mixed-bracket-repair.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(tc_002, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
print("✅ STK-002: Regenerated with wildcard matching (true/false)")

# STK-003: Weighted deduplication with even-sum removal
tc_003 = {'problem_id': 'STK_CONVEYOR_WEIGHTED_DEDUPLICATION__5318', 'samples': [], 'public': [], 'hidden': []}

samples_003 = [
    ("aabba", [1, 2, 3, 1, 2]),
    ("abc", [1, 1, 1]),
    ("aabbcc", [2, 2, 3, 3, 4, 4]),
]

for s, w in samples_003:
    tc_003['samples'].append({'input': f"{s}\\n{' '.join(map(str, w))}", 'output': weighted_dedup_even_sum(s, w)})

# Public cases
public_003 = [
    ("aa", [1, 1]),
    ("aa", [1, 2]),
    ("abba", [1, 1, 1, 1]),
]

for s, w in public_003:
    tc_003['public'].append({'input': f"{s}\\n{' '.join(map(str, w))}", 'output': weighted_dedup_even_sum(s, w)})

# Hidden cases
for _ in range(30):
    length = random.randint(1, 20)
    s = ''.join(random.choices('abc', k=length))
    w = [random.randint(1, 10) for _ in range(length)]
    tc_003['hidden'].append({'input': f"{s}\\n{' '.join(map(str, w))}", 'output': weighted_dedup_even_sum(s, w)})

with open(tc_dir / 'STK-003-conveyor-weighted-deduplication.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(tc_003, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
print("✅ STK-003: Regenerated with even-sum removal logic")

# STK-005: Next taller with width constraint
tc_005 = {'problem_id': 'STK_WORKSHOP_NEXT_TALLER_WIDTH__8156', 'samples': [], 'public': [], 'hidden': []}

samples_005 = [
    ([4, 5, 2, 10], 2),
    ([1, 2, 3, 4, 5], 1),
    ([5, 4, 3, 2, 1], 3),
]

for heights, w in samples_005:
    result = next_taller_width(heights, w)
    tc_005['samples'].append({
        'input': f"{len(heights)} {w}\\n{' '.join(map(str, heights))}",
        'output': ' '.join(map(str, result))
    })

# Public
for _ in range(5):
    n = random.randint(3, 10)
    heights = [random.randint(1, 20) for _ in range(n)]
    w = random.randint(1, n)
    result = next_taller_width(heights, w)
    tc_005['public'].append({
        'input': f"{n} {w}\\n{' '.join(map(str, heights))}",
        'output': ' '.join(map(str, result))
    })

# Hidden
for _ in range(30):
    n = random.randint(5, 30)
    heights = [random.randint(1, 100) for _ in range(n)]
    w = random.randint(1, n)
    result = next_taller_width(heights, w)
    tc_005['hidden'].append({
        'input': f"{n} {w}\\n{' '.join(map(str, heights))}",
        'output': ' '.join(map(str, result))
    })

with open(tc_dir / 'STK-005-workshop-next-taller-width.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(tc_005, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
print("✅ STK-005: Regenerated with width parameter w")

# STK-007: Threshold jump (array of steps)
tc_007 = {'problem_id': 'STK_TRADING_DESK_THRESHOLD_JUMP__2549', 'samples': [], 'public': [], 'hidden': []}

samples_007 = [
    ([10, 15, 12, 20, 18], 3),
    ([5, 5, 5, 5], 1),
    ([1, 10, 2, 20], 5),
]

for prices, t in samples_007:
    result = threshold_jump_steps(prices, t)
    tc_007['samples'].append({
        'input': f"{len(prices)} {t}\\n{' '.join(map(str, prices))}",
        'output': ' '.join(map(str, result))
    })

# Public + Hidden
for _ in range(35):
    n = random.randint(3, 20)
    prices = [random.randint(1, 100) for _ in range(n)]
    t = random.randint(1, 20)
    result = threshold_jump_steps(prices, t)
    entry = {
        'input': f"{n} {t}\\n{' '.join(map(str, prices))}",
        'output': ' '.join(map(str, result))
    }
    if _ < 5:
        tc_007['public'].append(entry)
    else:
        tc_007['hidden'].append(entry)

with open(tc_dir / 'STK-007-trading-desk-threshold-jump.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(tc_007, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
print("✅ STK-007: Regenerated with array output (steps for each position)")

# STK-009: Min-stack with MIN k operation  
tc_009 = {'problem_id': 'STK_LAB_SLIDING_MIN_STACK__5027', 'samples': [], 'public': [], 'hidden': []}

samples_009 = [
    [['PUSH', '5'], ['PUSH', '3'], ['PUSH', '7'], ['MIN', '2'], ['MIN', '3']],
    [['PUSH', '10'], ['MIN', '1'], ['POP'], ['MIN', '1']],
]

for ops in samples_009:
    result = min_stack_operations(ops)
    input_str = f"{len(ops)}\\n" + "\\n".join(' '.join(op) for op in ops)
    output_str = "\\n".join(result)
    tc_009['samples'].append({'input': input_str, 'output': output_str})

# Public + Hidden
for _ in range(35):
    num_ops = random.randint(3, 15)
    ops = []
    stack_size = 0
    for _ in range(num_ops):
        if stack_size == 0:
            ops.append(['PUSH', str(random.randint(-10, 10))])
            stack_size += 1
        else:
            choice = random.choice(['PUSH', 'POP', 'MIN'])
            if choice == 'PUSH':
                ops.append(['PUSH', str(random.randint(-10, 10))])
                stack_size += 1
            elif choice == 'POP':
                ops.append(['POP'])
                stack_size -= 1
            else:
                k = random.randint(1, min(stack_size, 5))
                ops.append(['MIN', str(k)])
    
    result = min_stack_operations(ops)
    input_str = f"{len(ops)}\\n" + "\\n".join(' '.join(op) for op in ops)
    output_str = "\\n".join(result)
    entry = {'input': input_str, 'output': output_str}
    
    if _ < 5:
        tc_009['public'].append(entry)
    else:
        tc_009['hidden'].append(entry)

with open(tc_dir / 'STK-009-lab-sliding-min-stack.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(tc_009, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
print("✅ STK-009: Regenerated with MIN k operation")

print("\n" + "=" * 80)
print("REGENERATION COMPLETE!")
print("=" * 80)
print("Regenerated test cases for problems with mismatches:")
print("  - STK-002: Now tests wildcard bracket matching (true/false)")
print("  - STK-003: Now tests even-sum weight removal")
print("  - STK-005: Now includes width parameter w")
print("  - STK-007: Now outputs array of steps for each position")
print("  - STK-009: Now tests MIN k operation (not sliding window)")
