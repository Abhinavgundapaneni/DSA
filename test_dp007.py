def max_sum_gap_three(a: list[int]) -> int:
    dp_i_3 = 0
    dp_i_2 = 0
    dp_i_1 = 0

    for x in a:
        cur = max(dp_i_1, x + dp_i_3)
        dp_i_3, dp_i_2, dp_i_1 = dp_i_2, dp_i_1, cur

    return dp_i_1

def main():
    n = int(input().strip())
    a = list(map(int, input().split()))
    print(max_sum_gap_three(a))

if __name__ == "__main__":
    main()
