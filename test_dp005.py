ROW1 = set("qwertyuiop")
ROW2 = set("asdfghjkl")
ROW3 = set("zxcvbnm")
LEFT = set("qwertasdfgzxcvb")

def row(c: str) -> int:
    if c in ROW1: return 1
    if c in ROW2: return 2
    return 3

def hand(c: str) -> int:
    return 0 if c in LEFT else 1

def rep_cost(x: str, y: str) -> int:
    if x == y: return 0
    if row(x) == row(y): return 1
    return 2 if hand(x) == hand(y) else 3

def min_keyboard_edit_cost(a: str, b: str) -> int:
    n, m = len(a), len(b)
    prev = list(range(m + 1))
    cur = [0] * (m + 1)

    for i in range(1, n + 1):
        cur[0] = i
        ca = a[i - 1]
        for j in range(1, m + 1):
            cb = b[j - 1]
            cur[j] = min(
                prev[j] + 1,               # delete
                cur[j - 1] + 1,            # insert
                prev[j - 1] + rep_cost(ca, cb)  # replace/match
            )
        prev, cur = cur, prev

    return prev[m]

def main():
    a = input().strip()
    b = input().strip()
    print(min_keyboard_edit_cost(a, b))

if __name__ == "__main__":
    main()
