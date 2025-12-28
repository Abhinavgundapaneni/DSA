def lcs_with_skip_limit(a: str, b: str, s: int) -> int:
    n, m = len(a), len(b)
    prev = [0] * (m + 1)
    cur = [0] * (m + 1)

    for i in range(1, n + 1):
        cur[0] = 0
        ai = a[i - 1]
        for j in range(1, m + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev, cur = cur, prev

    L = prev[m]
    return L if n - L <= s else -1

def main():
    a = input().strip()
    b = input().strip()
    s = int(input())
    print(lcs_with_skip_limit(a, b, s))

if __name__ == "__main__":
    main()
