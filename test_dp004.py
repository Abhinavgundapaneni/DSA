def exact_count_subset_sum(arr: list[int], target: int, k: int) -> bool:
    if k == 0:
        return target == 0
    if target < 0:
        return False

    bits = [0] * (k + 1)
    bits[0] = 1  # only sum 0 is reachable with 0 items

    mask = (1 << (target + 1)) - 1
    for x in arr:
        if x > target:
            # shift will push bits beyond target; masking will drop them
            pass
        for cnt in range(k, 0, -1):
            bits[cnt] |= (bits[cnt - 1] << x)
            bits[cnt] &= mask

    return ((bits[k] >> target) & 1) == 1

def main():
    n, target, k = map(int, input().split())
    arr = list(map(int, input().split()))
    print("true" if exact_count_subset_sum(arr, target, k) else "false")

if __name__ == "__main__":
    main()
