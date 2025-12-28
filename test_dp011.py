MOD = 1_000_000_007

def count_expressions(s: str, M: int, K: int, L: int) -> int:
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
                    addRem = ((rem + val) % M + M) % M
                    subRem = ((rem - val) % M + M) % M
                    dp[pos+l][addRem][used] = (dp[pos+l][addRem][used] + ways) % MOD
                    dp[pos+l][subRem][1] = (dp[pos+l][subRem][1] + ways) % MOD

    return dp[n][K][1]

def main():
    s = input().strip()
    M, K, L = map(int, input().split())
    print(count_expressions(s, M, K, L))

if __name__ == "__main__":
    main()
