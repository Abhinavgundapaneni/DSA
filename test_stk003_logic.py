#!/usr/bin/env python3
def weighted_deduplication(s: str, weights: list[int]) -> tuple[str, int]:
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
    
    return reduced, total_removed

# Test with sample
s = "aabba"
weights = [1, 2, 3, 1, 2]
reduced, total = weighted_deduplication(s, weights)
print(f"Input: s='{s}', w={weights}")
print(f"Output: '{reduced}'")
print(f"Total: {total}")
print(f"Expected: 'a' and 8")

# Trace through
print("\nStep by step:")
stack = []
total_removed = 0
for i, c in enumerate(s):
    print(f"{i}: '{c}' w={weights[i]}, stack={stack}")
    if stack and stack[-1][0] == c:
        sum_w = stack[-1][1] + weights[i]
        print(f"   Match! Sum={sum_w}, even={sum_w%2==0}")
        if sum_w % 2 == 0:
            total_removed += sum_w
            stack.pop()
            print(f"   Removed, total={total_removed}")
        else:
            stack.append((c, weights[i]))
            print(f"   Odd sum, push")
    else:
        stack.append((c, weights[i]))
        print(f"   No match, push")
        
print(f"\nFinal: {stack}, total={total_removed}")
