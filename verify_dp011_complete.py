"""
Generate ALL possible expressions for 1234 with chunk length <= 2
"""

def generate_all_expressions(s, max_chunk_len):
    """Generate all expressions recursively"""
    n = len(s)
    results = []
    
    def recurse(pos, expr, has_minus):
        if pos == n:
            if has_minus:  # At least one minus required
                results.append(expr)
            return
        
        # Try different chunk lengths
        for length in range(1, min(max_chunk_len + 1, n - pos + 1)):
            chunk = s[pos:pos+length]
            
            # Skip leading zeros (except single "0")
            if chunk[0] == '0' and length > 1:
                continue
            
            if pos == 0:
                # First chunk, no operator
                recurse(pos + length, chunk, False)
            else:
                # Can add or subtract
                recurse(pos + length, expr + '+' + chunk, has_minus)
                recurse(pos + length, expr + '-' + chunk, True)  # Now has minus
    
    recurse(0, "", False)
    return results

expressions = generate_all_expressions("1234", 2)

print(f"Total expressions with at least one minus: {len(expressions)}")
print()

# Evaluate and check which ones give value % 7 == 0
matches = []
for expr in expressions:
    val = eval(expr)
    mod_val = val % 7
    if mod_val == 0:
        matches.append((expr, val, mod_val))
        print(f"✓ {expr:15s} = {val:4d} ≡ {mod_val} (mod 7)")

print()
print(f"Count where value % 7 == 0: {len(matches)}")
