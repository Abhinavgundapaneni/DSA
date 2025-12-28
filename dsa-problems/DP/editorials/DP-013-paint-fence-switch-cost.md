---
problem_id: DP_PAINT_FENCE_SWITCH_COST__4281
display_id: DP-013
slug: paint-fence-switch-cost
title: "Paint Fence With Switch Cost"
difficulty: Medium
difficulty_score: 55
topics:
  - Dynamic Programming
  - Optimization
  - Combinatorics
tags:
  - dp
  - optimization
  - painting
  - medium
premium: true
subscription_tier: basic
---

# DP-013: Paint Fence With Switch Cost

## 📋 Problem Summary

Paint `n` posts using `k` colors. Painting any post costs 1. When two consecutive posts differ in color, you also pay a switch cost `s[i]` for post `i` (1-indexed). You may not place the same color on three consecutive posts. Return the minimum total cost, or `-1` if impossible.

Key constraints: `1 <= n <= 1e5`, `1 <= k <= 50`, no more than two adjacent posts may share a color, switch costs up to `1e4`.

## 🌍 Real-World Scenario

**Scenario Title:** Theme Park Queue Barriers

A theme park updates queue barriers daily. Each post is wrapped with colored tape: every wrap costs the same amount of tape (cost 1). For visual variety, maintenance rules ban three identical colors in a row. However, swapping tape rolls between consecutive posts slows the crew: at post `i`, swapping rolls adds extra effort `s[i]` (based on distance to supply carts and supervisor inspection frequency).

The operations manager wants the cheapest plan to wrap the day’s `n` posts with `k` available colors, obeying the “no three identical” policy. If the crew has only one color and more than two posts, the manager must report “impossible.”

**Why This Problem Matters:**

- Shows how to model **local repetition limits** (max streak length) in DP.
- Illustrates **state compression** from `O(k^2)` to `O(k)` via “best/second-best” tracking.
- Reinforces careful handling of **impossibility conditions** (e.g., `k = 1`, `n > 2`).

![Real-World Application](../images/DP-013/real-world-scenario.png)

## Detailed Explanation

We decide colors left to right. The constraint “no three identical” means the state must remember the streak length of the current color (1 or 2). Switching colors incurs a post-specific cost `s[i]`.

State idea for post `i` and color `c`:

- `dp1[c]`: min cost if post `i` uses color `c` with streak length exactly 1 (the previous post has a different color).
- `dp2[c]`: min cost if post `i` uses color `c` with streak length exactly 2 (previous post is also `c`).

Base (post 1): every color costs 1, streak = 1. For later posts:

- Extend streak to length 2: only from `dp1[c]`, add paint cost `+1`.
- Switch to color `c`: choose the cheapest prior color `!= c`, add paint cost `+1` and switch cost `s[i]`.

Naively, for each color we would scan all other colors (`O(k^2)` per post). We can do better by keeping:

- `min1`: overall best previous cost, with color `c1`.
- `min2`: second best previous cost.

For color `c`, the best “other color” cost is `min1` unless `c == c1`, in which case use `min2`. This drops the transition to `O(k)` per post, giving `O(nk)` total.

Corner case: if `k = 1`, the rule “no three identical” allows `n <= 2` only; otherwise answer is `-1`.

## Naive Approach

**Intuition:**
Track per-color streaks and, when switching, try every other color.

**Algorithm:**

1. Initialize `dp1[c] = 1`, `dp2[c] = INF` for all colors.
2. For each post `i` from 2 to `n`:
   - For every color `c`, set:
     - `new_dp2[c] = dp1[c] + 1` (extend to streak 2).
     - `new_dp1[c] = min_{p != c}(min(dp1[p], dp2[p])) + 1 + s[i]`.
3. Replace `dp` arrays with `new_dp`.
4. Answer = min over `dp1` and `dp2`; if still `INF`, return `-1`.

**Time Complexity:** `O(n * k^2)`  
**Space Complexity:** `O(k)`

**Why This Works:**
The state captures streak length, preventing a third repetition. Trying all other colors ensures the cheapest valid switch.

**Limitations:**

- Too slow for `k = 50`, `n = 1e5` (`2.5e8` transitions).
- Recomputes the same min across colors repeatedly.

## Optimal Approach

**Key Insight:**
Maintain the best and second-best previous costs to find the cheapest “other color” in `O(1)` per color.

**Algorithm:**

1. Handle `k = 1` separately: return `n` if `n <= 2`, else `-1`.
2. Initialize `dp1[c] = 1`, `dp2[c] = INF`.
3. For each post `i` from 2 to `n`:
   - Compute `best[c] = min(dp1[c], dp2[c])` for all `c`.
   - Find `(min1, color1)` and `min2` among `best`.
   - For each color `c`:
     - `ndp2[c] = dp1[c] + 1` (extend streak).
     - `bestOther = (c == color1) ? min2 : min1`.
     - If `bestOther` finite, `ndp1[c] = bestOther + 1 + s[i]`.
   - Replace `dp1, dp2` with `ndp1, ndp2`.
4. Answer = min over `dp1, dp2`; return `-1` if infinite.

**Time Complexity:** `O(n * k)`  
**Space Complexity:** `O(k)`  
**Why This Is Optimal:**
Only two global minima are needed to know the cheapest way to switch to any color. Every post has `k` updates, which is optimal given we must consider each color.

![Algorithm Visualization](../images/DP-013/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public long minCost(int n, int k, int[] s) {
        if (k == 1) return n <= 2 ? n : -1;
        final long INF = (long)4e18;
        long[] dp1 = new long[k];
        long[] dp2 = new long[k];
        Arrays.fill(dp1, 1);
        Arrays.fill(dp2, INF);

        for (int i = 1; i < n; i++) {
            long min1 = INF, min2 = INF;
            int c1 = -1;
            for (int c = 0; c < k; c++) {
                long v = Math.min(dp1[c], dp2[c]);
                if (v < min1) { min2 = min1; min1 = v; c1 = c; }
                else if (v < min2) { min2 = v; }
            }
            long[] ndp1 = new long[k];
            long[] ndp2 = new long[k];
            Arrays.fill(ndp1, INF);
            Arrays.fill(ndp2, INF);
            for (int c = 0; c < k; c++) {
                if (dp1[c] < INF) ndp2[c] = dp1[c] + 1; // extend streak
                long bestOther = (c == c1) ? min2 : min1;
                if (bestOther < INF) ndp1[c] = bestOther + 1 + s[i];
            }
            dp1 = ndp1; dp2 = ndp2;
        }
        long ans = INF;
        for (int c = 0; c < k; c++) ans = Math.min(ans, Math.min(dp1[c], dp2[c]));
        return ans >= INF ? -1 : ans;
    }
}
```

### Python

```python
from typing import List

def min_cost(n: int, k: int, s: List[int]) -> int:
    if k == 1:
        return n if n <= 2 else -1
    INF = 4 * 10**18
    dp1 = [1] * k
    dp2 = [INF] * k
    for i in range(1, n):
        best = [min(dp1[c], dp2[c]) for c in range(k)]
        min1 = min2 = INF
        c1 = -1
        for c, v in enumerate(best):
            if v < min1:
                min2 = min1
                min1 = v
                c1 = c
            elif v < min2:
                min2 = v
        ndp1 = [INF] * k
        ndp2 = [INF] * k
        for c in range(k):
            if dp1[c] < INF:
                ndp2[c] = dp1[c] + 1
            best_other = min1 if c != c1 else min2
            if best_other < INF:
                ndp1[c] = best_other + 1 + s[i]
        dp1, dp2 = ndp1, ndp2
    ans = min(min(dp1), min(dp2))
    return -1 if ans >= INF else ans

def main():
    n, k = map(int, input().split())
    s = list(map(int, input().split()))
    print(min_cost(n, k, s))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

long long minCost(int n, int k, const vector<int>& s) {
    if (k == 1) return n <= 2 ? n : -1;
    const long long INF = (long long)4e18;
    vector<long long> dp1(k, 1), dp2(k, INF);
    for (int i = 1; i < n; ++i) {
        long long min1 = INF, min2 = INF;
        int c1 = -1;
        for (int c = 0; c < k; ++c) {
            long long v = min(dp1[c], dp2[c]);
            if (v < min1) { min2 = min1; min1 = v; c1 = c; }
            else if (v < min2) { min2 = v; }
        }
        vector<long long> ndp1(k, INF), ndp2(k, INF);
        for (int c = 0; c < k; ++c) {
            if (dp1[c] < INF) ndp2[c] = dp1[c] + 1;
            long long bestOther = (c == c1) ? min2 : min1;
            if (bestOther < INF) ndp1[c] = bestOther + 1 + s[i];
        }
        dp1.swap(ndp1);
        dp2.swap(ndp2);
    }
    long long ans = *min_element(dp1.begin(), dp1.end());
    ans = min(ans, *min_element(dp2.begin(), dp2.end()));
    return ans >= INF ? -1 : ans;
}
```

### JavaScript

```javascript
function minCost(n, k, s) {
  if (k === 1) return n <= 2 ? n : -1;
  const INF = BigInt(4e18);
  let dp1 = Array(k).fill(1n);
  let dp2 = Array(k).fill(INF);
  for (let i = 1; i < n; i++) {
    let min1 = INF, min2 = INF, c1 = -1;
    for (let c = 0; c < k; c++) {
      const v = dp1[c] < dp2[c] ? dp1[c] : dp2[c];
      if (v < min1) { min2 = min1; min1 = v; c1 = c; }
      else if (v < min2) { min2 = v; }
    }
    const ndp1 = Array(k).fill(INF);
    const ndp2 = Array(k).fill(INF);
    for (let c = 0; c < k; c++) {
      if (dp1[c] < INF) ndp2[c] = dp1[c] + 1n;
      const bestOther = c === c1 ? min2 : min1;
      if (bestOther < INF) ndp1[c] = bestOther + 1n + BigInt(s[i]);
    }
    dp1 = ndp1; dp2 = ndp2;
  }
  let ans = dp1.concat(dp2).reduce((a, b) => (a < b ? a : b), INF);
  return ans >= INF ? -1 : Number(ans);
}
```

### Common Mistakes to Avoid

1. **Forgetting the impossibility when `k = 1` and `n > 2`.**
   - ❌ Allowing three identical posts produces an invalid plan.
   - ✅ Return `-1` early for this case.

2. **Switching to the same color.**
   - ❌ Adding switch cost when the color stays the same double-charges.
   - ✅ Apply switch cost only when the current color differs from the previous one.

3. **Allowing streak length 3.**
   - ❌ Transitioning from `dp2[c]` to `dp2[c]` creates three in a row.
   - ✅ Extend streak only from `dp1[c]`; `dp2` is terminal for that color on this post.



## Related Concepts

- Bounded streak DP
- State compression with minima
- 0/1 decision DP
