---
problem_id: DP_STOCK_WEEK_REST_FEE__6420
display_id: DP-015
slug: stock-trading-weekly-rest-fee
title: "Stock Trading With Weekly Rest and Fee"
difficulty: Medium
difficulty_score: 55
topics:
  - Dynamic Programming
  - Greedy
  - Finance
tags:
  - dp
  - stocks
  - cooldown
  - medium
premium: true
subscription_tier: basic
---

# DP-015: Stock Trading With Weekly Rest and Fee

## 📋 Problem Summary

You have `n` days of stock prices (`day 0` is Monday). After each sale on day `i`, you must rest until the next Monday (`i - (i % 7) + 7`), during which you cannot buy. Each sale pays `price[i] - fee`. Compute the maximum profit with unlimited transactions under this weekly cooldown.

## 🌍 Real-World Scenario

**Scenario Title:** Compliance-Limited Trading Desk

A trading desk is allowed to trade freely during the week, but any sale triggers a mandatory compliance review that lasts until the following Monday. During that review window, new positions cannot be opened, though existing positions can be held until sold. Transaction fees apply per sale.

Traders need a fast tool to find the best profit plan for the upcoming quarter’s price projections, honoring the week-long cooldown after each sale.

**Why This Problem Matters:**

- Extends classic stock DP with a **time-aligned cooldown** (next Monday) instead of a fixed one-day pause.
- Highlights scheduling concepts: actions unlock on specific future days.
- Reinforces separating **“can buy”** and **“holding”** states when availability is time-dependent.

![Real-World Application](../images/DP-015/real-world-scenario.png)

## Detailed Explanation

We maintain two primary states:

- `buyable`: best profit when **not holding** and allowed to buy today.
- `hold`: best profit while **holding** a stock.

Selling today:

- Creates profit `hold + price[i] - fee`.
- Unlocks future buying on the next Monday after today.

To implement the unlock, keep an array `unlock[d]` storing the best profit that becomes buyable on day `d`. Each morning, if `unlock[i]` is set, merge it into `buyable`.

Transitions per day `i`:

1. `buyable = max(buyable, unlock[i])` (if present).
2. `hold = max(hold, buyable - price[i])` (buy or keep holding).
3. If previously holding, selling yields `sellProfit = hold_prev + price[i] - fee` and schedules `unlock[nextMonday] = max(unlock[nextMonday], sellProfit)`.
4. Track answer as the best of all non-holding profits and final possible sale.

Corner cases:

- If you never buy, profit stays 0.
- Buying and selling the same day is disallowed; we use `hold_prev` before today’s buy transition to compute sells.

## Naive Approach

**Intuition:**
Enumerate all buy/sell decisions with DFS/backtracking and enforce cooldowns.

**Algorithm:**

1. From day `i`, choose to buy (if allowed), sell (if holding), or skip.
2. When selling on day `i`, jump recursion to `nextMonday` for the next decision.
3. Track best profit over all paths.

**Time Complexity:** Exponential in `n`.  
**Space Complexity:** Recursion depth `O(n)`.

**Why This Works:**
It simulates every valid schedule, respecting cooldown jumps.

**Limitations:**

- Intractable for `n = 1e5`.
- Recomputes overlapping subproblems heavily.

## Optimal Approach

**Key Insight:**
You only need today’s best **buyable** profit, today’s **hold** profit, and a calendar of future **unlock** profits.

**Algorithm:**

1. Initialize `buyable = 0`, `hold = -INF`, `unlock` array sized `n+8` with `-INF`.
2. For each day `i`:
   - If `unlock[i]` exists, `buyable = max(buyable, unlock[i])`.
   - `newHold = max(hold, buyable - price[i])`.
   - If `hold` was finite, compute `sellProfit = hold + price[i] - fee`, update answer, and set `unlock[nextMonday(i)] = max(..., sellProfit)`.
   - Assign `hold = newHold`.
3. After the loop, also consider selling the final held stock on the last day.
4. Answer is the maximum seen non-holding profit (including pending unlocks).

**Time Complexity:** `O(n)`  
**Space Complexity:** `O(n)` for the unlock array; can be reduced with a map if sparse.

**Why This Is Optimal:**
Each day is processed once with constant work; unlock scheduling handles the week-aligned cooldown precisely.

![Algorithm Visualization](../images/DP-015/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public long maxProfit(int[] prices, long fee) {
        int n = prices.length;
        final long NEG = (long)-4e18;
        long buyable = 0, hold = NEG, ans = 0;
        long[] unlock = new long[n + 8];
        Arrays.fill(unlock, NEG);
        for (int i = 0; i < n; i++) {
            if (unlock[i] != NEG) buyable = Math.max(buyable, unlock[i]);
            long prevHold = hold;
            hold = Math.max(hold, buyable - prices[i]);
            if (prevHold != NEG) {
                long sellProfit = prevHold + prices[i] - fee;
                ans = Math.max(ans, sellProfit);
                int nextMonday = i - (i % 7) + 7;
                if (nextMonday < unlock.length) {
                    unlock[nextMonday] = Math.max(unlock[nextMonday], sellProfit);
                }
            }
        }
        if (hold != NEG) ans = Math.max(ans, hold + prices[n - 1] - fee);
        ans = Math.max(ans, buyable);
        for (int i = n; i < unlock.length; i++) ans = Math.max(ans, unlock[i]);
        return ans;
    }
}
```

### Python

```python
from typing import List

def max_profit(prices: List[int], fee: int) -> int:
    n = len(prices)
    NEG = -4 * 10**18
    buyable = 0
    hold = NEG
    unlock = [NEG] * (n + 8)
    ans = 0
    for i, p in enumerate(prices):
        if unlock[i] != NEG:
            buyable = max(buyable, unlock[i])
        prev_hold = hold
        hold = max(hold, buyable - p)
        if prev_hold != NEG:
            sell_profit = prev_hold + p - fee
            ans = max(ans, sell_profit)
            next_monday = i - (i % 7) + 7
            if next_monday < len(unlock):
                unlock[next_monday] = max(unlock[next_monday], sell_profit)
    if hold != NEG:
        ans = max(ans, hold + prices[-1] - fee)
    ans = max(ans, buyable)
    for val in unlock[n:]:
        ans = max(ans, val)
    return ans

def main():
    n, fee = map(int, input().split())
    prices = list(map(int, input().split()))
    print(max_profit(prices, fee))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

long long maxProfit(const vector<int>& prices, long long fee) {
    int n = (int)prices.size();
    const long long NEG = (long long)-4e18;
    long long buyable = 0, hold = NEG, ans = 0;
    vector<long long> unlock(n + 8, NEG);
    for (int i = 0; i < n; ++i) {
        if (unlock[i] != NEG) buyable = max(buyable, unlock[i]);
        long long prevHold = hold;
        hold = max(hold, buyable - prices[i]);
        if (prevHold != NEG) {
            long long sellProfit = prevHold + prices[i] - fee;
            ans = max(ans, sellProfit);
            int nextMonday = i - (i % 7) + 7;
            if (nextMonday < (int)unlock.size()) {
                unlock[nextMonday] = max(unlock[nextMonday], sellProfit);
            }
        }
    }
    if (hold != NEG) ans = max(ans, hold + prices.back() - fee);
    ans = max(ans, buyable);
    for (int i = n; i < (int)unlock.size(); ++i) ans = max(ans, unlock[i]);
    return ans;
}
```

### JavaScript

```javascript
const NEG = BigInt(-4e18);

function maxProfit(prices, fee) {
  const n = prices.length;
  let buyable = 0n, hold = NEG, ans = 0n;
  const unlock = Array(n + 8).fill(NEG);
  for (let i = 0; i < n; i++) {
    if (unlock[i] !== NEG) buyable = buyable > unlock[i] ? buyable : unlock[i];
    const prevHold = hold;
    hold = hold > buyable - BigInt(prices[i]) ? hold : buyable - BigInt(prices[i]);
    if (prevHold !== NEG) {
      const sellProfit = prevHold + BigInt(prices[i]) - BigInt(fee);
      if (sellProfit > ans) ans = sellProfit;
      const nextMonday = i - (i % 7) + 7;
      if (nextMonday < unlock.length && sellProfit > unlock[nextMonday]) {
        unlock[nextMonday] = sellProfit;
      }
    }
  }
  if (hold !== NEG) ans = ans > hold + BigInt(prices[n - 1]) - BigInt(fee) ? ans : hold + BigInt(prices[n - 1]) - BigInt(fee);
  if (buyable > ans) ans = buyable;
  for (let i = n; i < unlock.length; i++) if (unlock[i] > ans) ans = unlock[i];
  return Number(ans);
}
```

### Common Mistakes to Avoid

1. **Selling with today’s buy.**
   - ❌ Using updated `hold` to sell permits same-day buy-and-sell.
   - ✅ Use `hold_prev` (state before buying today) when computing a sale.

2. **Ignoring the week boundary.**
   - ❌ Cooldown of fixed 1 day instead of jumping to next Monday.
   - ✅ Compute `nextMonday = i - (i % 7) + 7` for every sale.

3. **Overflow with large prices.**
   - ❌ Storing profits in 32-bit integers.
   - ✅ Use 64-bit (or BigInt) for all arithmetic.



## Related Concepts

- Cooldown stock DP
- State unlocking by time
- Greedy vs DP boundary conditions
