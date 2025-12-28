from bisect import bisect_left, bisect_right

def longest_bounded_diff_subsequence(a: list[int], d: int, g: int) -> int:
    vals = sorted(set(a))
    m = len(vals)

    size = 1
    while size < m:
        size <<= 1
    seg = [0] * (2 * size)

    def seg_update(pos: int, val: int) -> None:
        i = pos + size
        if val > seg[i]:
            seg[i] = val
            i //= 2
            while i:
                seg[i] = seg[2 * i] if seg[2 * i] > seg[2 * i + 1] else seg[2 * i + 1]
                i //= 2

    def seg_query(l: int, r: int) -> int:
        if l > r:
            return 0
        l += size
        r += size
        res = 0
        while l <= r:
            if (l & 1) == 1:
                if seg[l] > res:
                    res = seg[l]
                l += 1
            if (r & 1) == 0:
                if seg[r] > res:
                    res = seg[r]
                r -= 1
            l //= 2
            r //= 2
        return res

    ans = 1
    for x in a:
        lo = x - g
        hi = x - d
        L = bisect_left(vals, lo)
        R = bisect_right(vals, hi) - 1
        best = seg_query(L, R)
        dp = best + 1
        idx = bisect_left(vals, x)
        seg_update(idx, dp)
        if dp > ans:
            ans = dp

    return ans

def main():
    n = int(input())
    a = list(map(int, input().split()))
    d, g = map(int, input().split())
    print(longest_bounded_diff_subsequence(a, d, g))

if __name__ == "__main__":
    main()
