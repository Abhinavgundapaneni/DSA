def is_vowel(c):
    return c in 'aeiou'

s = "programming"
# p r o g r a m m i n g
# 0 1 2 3 4 5 6 7 8 9 10
# C C V C C V C C V C C

print("All alternating substrings of length >= 2:")
for start in range(len(s)):
    for end in range(start + 1, len(s) + 1):
        substr = s[start:end]
        # Check if alternating
        is_alt = True
        for i in range(len(substr) - 1):
            if is_vowel(substr[i]) == is_vowel(substr[i+1]):
                is_alt = False
                break
        if is_alt and len(substr) >= 2:
            v_or_c = ''.join(['V' if is_vowel(c) else 'C' for c in substr])
            print(f"  {start:2d}-{end-1:2d}: '{substr:12s}' ({len(substr)}) {v_or_c}")

print("\nLongest alternating substrings:")
max_len = 0
longest = []
for start in range(len(s)):
    for end in range(start + 1, len(s) + 1):
        substr = s[start:end]
        is_alt = True
        for i in range(len(substr) - 1):
            if is_vowel(substr[i]) == is_vowel(substr[i+1]):
                is_alt = False
                break
        if is_alt:
            if len(substr) > max_len:
                max_len = len(substr)
                longest = [(start, end, substr)]
            elif len(substr) == max_len:
                longest.append((start, end, substr))

for start, end, substr in longest:
    print(f"  Length {len(substr)}: '{substr}' at positions {start}-{end-1}")
