def identify_runs(s):
    """Identify all runs in a string."""
    runs = []
    i = 0
    while i < len(s):
        start = i
        char = s[i]
        while i < len(s) and s[i] == char:
            i += 1
        runs.append((char, i - start))
    return runs

# Test different compression rules
test_cases = [
    ("a", 1, "a"),
    ("abbccc", 2, "abb3"),
    ("xyzzz", 3, "xy3"),
    ("mississippi", 3, "mis2is2ip2i"),
    ("aabbcc", 2, "a2b2c2"),
    ("aaabbaaa", 3, "a3b2a3"),
    ("aabbaabb", 3, "aab2aab2"),
]

for s, w, expected in test_cases:
    runs = identify_runs(s)
    
    # Rule: compress only if count > w (strictly greater)
    result1 = []
    for char, count in runs:
        if count > w:
            result1.append(char + str(count))
        else:
            result1.append(char * count)
    got1 = ''.join(result1)
    
    # Rule: compress only if it saves space (count >= 3 OR count == 2 and w <= 2)
    # Actually, let me try: compress only if count > w OR (count == w AND w <= 2)
    result2 = []
    for char, count in runs:
        if count > w or (count == w and w <= 2):
            result2.append(char + str(count))
        else:
            result2.append(char * count)
    got2 = ''.join(result2)
    
    print(f"'{s}' w={w} → expect '{expected}'")
    print(f"  Runs: {runs}")
    print(f"  Rule (count > w):                    '{got1}' {'✓' if got1 == expected else '✗'}")
    print(f"  Rule (count>w OR count==w AND w<=2): '{got2}' {'✓' if got2 == expected else '✗'}")
    print()
