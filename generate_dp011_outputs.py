"""Generate correct outputs for all DP-011 test inputs."""

MOD = 1_000_000_007

def count_expressions(s, M, K, L):
    n = len(s)
    dp = [[[0]*2 for _ in range(M)] for __ in range(n+1)]
    for l in range(1, min(L, n) + 1):
        if s[0] == '0' and l > 1:
            break
        val = int(s[0:l]) % M
        dp[l][val][0] = 1
    for pos in range(1, n):
        for rem in range(M):
            for used in range(2):
                ways = dp[pos][rem][used]
                if ways == 0:
                    continue
                for l in range(1, min(L, n - pos) + 1):
                    if s[pos] == '0' and l > 1:
                        break
                    val = int(s[pos:pos+l])
                    addRem = (rem + val) % M
                    subRem = (rem - val) % M
                    dp[pos+l][addRem][used] = (dp[pos+l][addRem][used] + ways) % MOD
                    dp[pos+l][subRem][1] = (dp[pos+l][subRem][1] + ways) % MOD
    return dp[n][K][1]

# All test cases from the YAML file
test_cases = [
    # samples
    ("1234", 7, 0, 2),
    ("1", 5, 1, 1),
    # public
    ("12", 3, 0, 2),
    ("505", 5, 0, 3),
    ("123", 4, 1, 2),
    # hidden
    ("91", 6, 0, 2),
    ("7631", 9, 0, 4),
    ("9074", 5, 4, 1),
    ("0", 2, 1, 3),
]

print("Correct outputs for DP-011 test cases:")
print("="*60)
for s, M, K, L in test_cases:
    result = count_expressions(s, M, K, L)
    print(f"s='{s}', M={M}, K={K}, L={L} -> {result}")
