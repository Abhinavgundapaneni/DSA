"""
Verify DP-011 example manually.
Input: 1234, M=7, K=0, Lmax=2

Need expressions where:
- Each chunk has length <= 2
- At least one minus sign
- Value % 7 == 0
"""

# All valid expressions with chunk length <= 2 and at least one minus:
expressions = [
    # Format: (expression, value, value % 7)
    ("1-2-3-4", 1-2-3-4, (1-2-3-4) % 7),
    ("1-2-34", 1-2-34, (1-2-34) % 7),
    ("1-23-4", 1-23-4, (1-23-4) % 7),
    ("1-23+4", 1-23+4, (1-23+4) % 7),
    ("12-3-4", 12-3-4, (12-3-4) % 7),
    ("12-3+4", 12-3+4, (12-3+4) % 7),
    ("12-34", 12-34, (12-34) % 7),
    ("1+2-3-4", 1+2-3-4, (1+2-3-4) % 7),
    ("1+2-34", 1+2-34, (1+2-34) % 7),
    ("1+23-4", 1+23-4, (1+23-4) % 7),
]

print("Valid expressions with chunk length <= 2 and at least one minus:")
print()

count = 0
for expr, val, mod_val in expressions:
    status = "✓" if mod_val == 0 else " "
    print(f"{status} {expr:15s} = {val:4d} ≡ {mod_val} (mod 7)")
    if mod_val == 0:
        count += 1

print()
print(f"Count of expressions where value % 7 == 0: {count}")
