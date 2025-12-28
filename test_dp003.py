NEG = -(10**30)

def max_value_required_weight(n: int, W: int, R: int, items: list[tuple[int, int]]) -> int:
    dp = [NEG] * (W + 1)
    dp[0] = 0

    for wi, vi in items:
        for wt in range(W, wi - 1, -1):
            if dp[wt - wi] != NEG:
                dp[wt] = max(dp[wt], dp[wt - wi] + vi)

    ans = max(dp[R:W+1])
    return -1 if ans == NEG else ans

def main():
    n, W, R = map(int, input().split())
    items = [tuple(map(int, input().split())) for _ in range(n)]
    print(max_value_required_weight(n, W, R, items))

if __name__ == "__main__":
    main()
