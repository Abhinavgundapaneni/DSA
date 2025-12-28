from collections import deque

INF = 10**30

def min_cost(k: int, target: int, d: list[int], c: list[int], p: list[int]) -> int:
    dp = [INF] * (target + 1)
    dp[0] = 0

    for i in range(k):
        denom = d[i]
        cap = min(c[i], target // denom)
        t = min(c[i] // 2, cap)
        penalty = p[i]

        nxt = [INF] * (target + 1)

        for r in range(denom):
            qmax = (target - r) // denom
            if qmax < 0:
                continue

            L1 = min(cap, t)
            dq_no = deque()
            dq_pen = deque()

            def key(sum_idx: int, q: int) -> int:
                return dp[sum_idx] - q

            for q in range(qmax + 1):
                s_q = r + q * denom

                # push into no-pen deque (window [q-L1, q])
                if dp[s_q] < INF:
                    kv = dp[s_q] - q
                    while dq_no and kv <= key(r + dq_no[-1] * denom, dq_no[-1]):
                        dq_no.pop()
                    dq_no.append(q)

                min_y = q - L1
                while dq_no and dq_no[0] < min_y:
                    dq_no.popleft()

                best = INF
                if dq_no:
                    y = dq_no[0]
                    best = min(best, q + key(r + y * denom, y))

                # penalty deque (window [q-cap, q-(t+1)])
                if cap > t:
                    y_add = q - (t + 1)
                    if y_add >= 0:
                        s_add = r + y_add * denom
                        if dp[s_add] < INF:
                            kv = dp[s_add] - y_add
                            while dq_pen and kv <= key(r + dq_pen[-1] * denom, dq_pen[-1]):
                                dq_pen.pop()
                            dq_pen.append(y_add)

                    min_y_pen = q - cap
                    while dq_pen and dq_pen[0] < min_y_pen:
                        dq_pen.popleft()

                    if dq_pen:
                        y = dq_pen[0]
                        best = min(best, q + penalty + key(r + y * denom, y))

                s = r + q * denom
                nxt[s] = min(nxt[s], best)

        dp = nxt

    return -1 if dp[target] >= INF else dp[target]


def main():
    k, target = map(int, input().split())
    d, c, p = [], [], []
    for _ in range(k):
        di, ci, pi = map(int, input().split())
        d.append(di); c.append(ci); p.append(pi)
    print(min_cost(k, target, d, c, p))


if __name__ == "__main__":
    main()
