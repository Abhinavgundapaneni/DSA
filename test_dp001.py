MOD = 1_000_000_007

def count_ways(n: int, J: int, cracked: list[bool]) -> int:
    if cracked[n]:
        return 0

    dp = [0] * (n + 1)
    dp[0] = 1
    window_sum = 1  # sum of dp[max(0, i-J) .. i-1] when processing i

    for i in range(1, n + 1):
        # Block landing on cracked steps.
        dp[i] = 0 if cracked[i] else window_sum
        window_sum = (window_sum + dp[i]) % MOD
        out = i - J
        if out >= 0:
            window_sum = (window_sum - dp[out]) % MOD

    return dp[n]

def main():
    n, J = map(int, input().split())
    m = int(input().strip())
    cracked = [False] * (n + 1)
    if m > 0:
        arr = list(map(int, input().split()))
        for x in arr:
            if 1 <= x <= n:
                cracked[x] = True
    print(count_ways(n, J, cracked))

if __name__ == "__main__":
    main()
