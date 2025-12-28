def identify_runs(s):
    """Identify all runs in a string."""
    runs = []
    i = 0
    while i < len(s):
        start = i
        char = s[i]
        while i < len(s) and s[i] == char:
            i += 1
        runs.append((char, i - start, start))
    return runs

# Test cases
test_cases = [
    ("a", 1, "a"),
    ("abbccc", 2, "abb3"),
    ("xyzzz", 3, "xy3"),
    ("mississippi", 3, "mis2is2ip2i"),
    ("aabbcc", 2, "a2b2c2"),
    ("aaabbaaa", 3, "a3b2a3"),
]

for s, w, expected in test_cases:
    runs = identify_runs(s)
    print(f"Input: '{s}', w={w}, Expected: '{expected}'")
    print(f"  Runs: {runs}")
    
    # Try to figure out the compression logic
    result = []
    for char, count, start in runs:
        if count >= w:
            compressed = char + str(count)
        else:
            compressed = char * count
        result.append(f"{compressed}")
    
    got = ''.join(result)
    print(f"  With rule (count >= w): '{got}' {'✓' if got == expected else '✗'}")
    
    # Try: only compress if saves space
    result2 = []
    for char, count, start in runs:
        compressed_form = char + str(count)
        if count >= w and len(compressed_form) < count:
            result2.append(compressed_form)
        else:
            result2.append(char * count)
    
    got2 = ''.join(result2)
    print(f"  With rule (count >= w AND saves space): '{got2}' {'✓' if got2 == expected else '✗'}")
    
    print()
