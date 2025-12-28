def is_vowel(c):
    return c in 'aeiou'

s = "programming"
# Let's trace the expected answer "ograr"
substr = "ograr"
print(f"Checking if '{substr}' is alternating:")
for i, c in enumerate(substr):
    print(f"  {i}: '{c}' -> {'V' if is_vowel(c) else 'C'}")
print()

# Let's find it in the string
idx = s.find(substr)
print(f"Found at index: {idx}")
print(f"Substring from {idx} to {idx+5}: {s[idx:idx+5]}")
print()

# So the answer is at indices 2-6 (inclusive)
# Let's trace the algorithm
print("Manual trace:")
max_len = 1
best_start = 0
current_len = 1
start = 0
prev_is_vowel = is_vowel(s[0])

print(f"0: '{s[0]}' ({'V' if prev_is_vowel else 'C'}) -> len=1, start=0")

for i in range(1, len(s)):
    curr_is_vowel = is_vowel(s[i])
    if curr_is_vowel != prev_is_vowel:
        current_len += 1
        if current_len > max_len:
            max_len = current_len
            best_start = start
        status = f"ALT -> len={current_len}, max={max_len}, best_start={best_start}"
    else:
        start = i
        current_len = 1
        status = f"BREAK -> reset start={start}, len=1"
    
    print(f"{i}: '{s[i]}' ({'V' if curr_is_vowel else 'C'}) {status}")
    prev_is_vowel = curr_is_vowel

print(f"\nFinal: best_start={best_start}, max_len={max_len}")
print(f"Result: {s[best_start:best_start+max_len]}")
