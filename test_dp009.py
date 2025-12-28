INF = 10**18

def min_cost_with_free_cells(cost: list[list[int]], f: int) -> int:
    m, n = len(cost), len(cost[0])
    dp = [[[INF] * (f + 1) for _ in range(n)] for __ in range(m)]
    dp[0][0][0] = cost[0][0]
    if f > 0:
        dp[0][0][1] = 0

    for r in range(m):
        for c in range(n):
            for k in range(f + 1):
                cur = dp[r][c][k]
                if cur >= INF:
                    continue
                if c + 1 < n:
                    dp[r][c + 1][k] = min(dp[r][c + 1][k], cur + cost[r][c + 1])
                    if k + 1 <= f:
                        dp[r][c + 1][k + 1] = min(dp[r][c + 1][k + 1], cur)
                if r + 1 < m:
                    dp[r + 1][c][k] = min(dp[r + 1][c][k], cur + cost[r + 1][c])
                    if k + 1 <= f:
                        dp[r + 1][c][k + 1] = min(dp[r + 1][c][k + 1], cur)

    return min(dp[-1][-1])

def main():
    m, n = map(int, input().split())
    cost = []
    for _ in range(m):
        cost.append(list(map(int, input().split())))
    f = int(input())
    print(min_cost_with_free_cells(cost, f))

if __name__ == "__main__":
    main()
