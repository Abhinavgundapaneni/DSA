MOD = 1_000_000_007

def count_paths_with_turn_limit(m: int, n: int, T: int) -> int:
    if m == 1 and n == 1:
        return 1

    dpR = [[[0] * (T + 1) for _ in range(n)] for __ in range(m)]
    dpD = [[[0] * (T + 1) for _ in range(n)] for __ in range(m)]

    if n >= 2:
        dpR[0][1][0] = 1
    if m >= 2:
        dpD[1][0][0] = 1

    for r in range(m):
        for c in range(n):
            if (r, c) in [(0, 0), (0, 1), (1, 0)]:
                continue
            for t in range(T + 1):
                if c - 1 >= 0:
                    dpR[r][c][t] = (dpR[r][c][t] + dpR[r][c - 1][t]) % MOD
                    if t - 1 >= 0:
                        dpR[r][c][t] = (dpR[r][c][t] + dpD[r][c - 1][t - 1]) % MOD
                if r - 1 >= 0:
                    dpD[r][c][t] = (dpD[r][c][t] + dpD[r - 1][c][t]) % MOD
                    if t - 1 >= 0:
                        dpD[r][c][t] = (dpD[r][c][t] + dpR[r - 1][c][t - 1]) % MOD

    ans = 0
    for t in range(T + 1):
        ans = (ans + dpR[m - 1][n - 1][t] + dpD[m - 1][n - 1][t]) % MOD
    return ans

def main():
    m, n, T = map(int, input().split())
    print(count_paths_with_turn_limit(m, n, T))

if __name__ == "__main__":
    main()
