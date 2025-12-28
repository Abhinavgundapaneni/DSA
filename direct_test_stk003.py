#!/usr/bin/env python3
def reduce_stack(s: str, w: list[int]) -> tuple[str, int]:
    """Remove adjacent matching chars if weight sum is even"""
    stack = []
    total_removed = 0
    
    for char, weight in zip(s, w):
        if stack and stack[-1][0] == char and (stack[-1][1] + weight) % 2 == 0:
            total_removed += stack[-1][1] + weight
            stack.pop()
        else:
            stack.append((char, weight))
            
    reduced_s = "".join(item[0] for item in stack)
    if not reduced_s:
        reduced_s = "EMPTY"
    return reduced_s, total_removed

# Direct test
s = "aabba"
w = [1, 2, 3, 1, 2]
reduced, total = reduce_stack(s, w)
print(f"Result: '{reduced}', {total}")
print(f"Expected: 'a', 8")
print(f"Match: {reduced == 'a' and total == 8}")

# Test with file I/O simulation
test_input = "aabba\n1 2 3 1 2"
lines = test_input.split('\n')
s2 = lines[0]
w2 = list(map(int, lines[1].split()))
reduced2, total2 = reduce_stack(s2, w2)
output = f"{reduced2}\n{total2}"
expected = "a\n8"
print(f"\nWith I/O: {repr(output)}")
print(f"Expected: {repr(expected)}")
print(f"Match: {output == expected}")
