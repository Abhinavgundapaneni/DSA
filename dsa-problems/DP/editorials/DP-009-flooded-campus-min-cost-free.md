---
problem_id: DP_GRID_FREE_CELL__4415
display_id: DP-009
slug: flooded-campus-min-cost-free
title: "Flooded Campus Min Cost With Free Cells"
difficulty: Medium
difficulty_score: 57
topics:
  - Dynamic Programming
  - Grid DP
  - Shortest Path
tags:
  - dp
  - grid
  - min-cost
  - medium
premium: true
subscription_tier: basic
---

# DP-009: Flooded Campus Min Cost With Free Cells

## 📋 Problem Summary

You need the minimum-cost path from the top-left to bottom-right of a grid, moving only right or down. Each cell has a non-negative cost. You can mark up to `f` cells to be **free** (cost 0). Each cell can be discounted at most once.

Compute the minimum possible total cost.

## 🌍 Real-World Scenario

**Scenario Title:** Campus Flood Evacuation with Emergency Passes

Imagine a flooded campus where every building crossing has a “cost” (time/risk). You can distribute a limited number of “emergency passes” (`f` passes) that let evacuees cross certain cells at zero cost. Paths can only move right or down along designated corridors.

Goal: minimize total crossing cost by choosing the best cells to make free.

This maps directly to the grid DP with a “free cell” budget.

**Why This Problem Matters:**

- Teaches DP with an extra resource dimension (free cells)
- Shows how to adapt classic min-path DP to handle discounts/bonuses
- Reinforces O(m·n·f) reasoning within tight constraints

![Real-World Application](../images/DP-009/real-world-scenario.png)

## ✅ Clarifications

- You may use fewer than `f` free cells if that is optimal.
- Freeing `(0,0)` or `(m-1,n-1)` is allowed.
- Movement: only right or down.
- Costs are non-negative, so taking a free cell is never worse locally, but you must manage the budget globally.
- Answer fits in 64-bit because costs up to `10^4` over `200x200` is ≤ 4e8 even before discounts.

## Detailed Explanation

### ASCII Diagram: Grid with Costs and Free Cells

```
Grid 3x3 with f=1 (1 free cell allowed):
Cost values and free cells marked:

    [0]  [5]  [3]
     1    2    3
    [2]  [1]  [4]  ← row 1, col 1 is FREE (marked with *)
     4    5    6
    [6]  [2]  [1]

Path with budget f=1:
Start (0,0) → (0,1) → (0,2) → (1,2) → (2,2)
Costs: 0 + 5 + 3 + 4 + 1 = 13

Path using free cell:
Start (0,0) → (1,0) → (1,1)* → (1,2) → (2,2)
         ↓     cost 2    FREE    cost 4    cost 1
Costs: 0 + 2 + 0 + 4 + 1 = 7 (saves 6 by using free cell)
```

### Classic min-path DP (baseline)

Without free cells:

`dp[r][c] = cost[r][c] + min(dp[r-1][c], dp[r][c-1])`

With `f` free cells, you need to know how many free cells have been used so far.

### DP state with free-cell budget

Let:

`dp[r][c][k] = minimum cost to reach (r,c) having used exactly k free cells`

Range:

- `0 <= r < m`
- `0 <= c < n`
- `0 <= k <= f`

Transition from top or left:

1) **Do not use a free cell at (r,c)**:

`dp[r][c][k] = cost[r][c] + min(dp[r-1][c][k], dp[r][c-1][k])`

2) **Use a free cell at (r,c)** (only if `k > 0`):

`dp[r][c][k] = min(dp[r][c][k], 0 + min(dp[r-1][c][k-1], dp[r][c-1][k-1]))`

Take the min of these possibilities.

Base:

- `dp[0][0][0] = cost[0][0]` (not free)
- If `f > 0`, `dp[0][0][1] = 0` (free the start)
- Elsewhere initialize to INF.

Answer:

`min_{k=0..f} dp[m-1][n-1][k]`

### Complexity

- Time: `O(m * n * f)`
- Space: `O(m * n * f)` (can be reduced to `O(n * f)` with rolling rows)

Given `m,n <= 200`, `f <= 10`, total states ≈ 200*200*11 = 440k, which is fine.

### Decision Tree for Free Cell Usage

```
At position (i,j) with free_used cells:
    │
    ├─ Option 1: Use regular cost
    │   └─ cost_here = grid[i][j]
    │       dp[i][j][free_used] = min(dp[i-1][j][free_used], dp[i][j-1][free_used]) + cost_here
    │
    └─ Option 2: Use free cell (if free_used < f)
        └─ cost_here = 0
            dp[i][j][free_used+1] = min(dp[i-1][j][free_used], dp[i][j-1][free_used]) + 0

Final Answer: min_{k=0..f} dp[m-1][n-1][k]
```

![Algorithm Visualization](../images/DP-009/algorithm-visualization.png)
![Algorithm Steps](../images/DP-009/algorithm-steps.png)

## 🧩 Edge Cases (Checklist)

- `f = 0`: becomes classic min-path sum.
- `f >= m*n`: you can free every cell ⇒ answer is 0.
- Single cell (`m=n=1`): answer is `min(cost[0][0], 0 if f>0 else cost[0][0])`.
- Rows/cols of length 1: only one path; choose the cheapest cells to free along that line.

## 🚀 Space Optimization (Optional)

You can reduce space to `O(n * f)` using rolling rows:

- Keep two rows of size `[n][f+1]`
- Update row by row

Time remains `O(m * n * f)`.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    private static final long INF = (long)4e18;

    public int minCostWithFreeCells(int[][] cost, int f) {
        int m = cost.length, n = cost[0].length;
        long[][][] dp = new long[m][n][f + 1];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                Arrays.fill(dp[i][j], INF);
            }
        }

        dp[0][0][0] = cost[0][0];
        if (f > 0) dp[0][0][1] = 0;

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                for (int k = 0; k <= f; k++) {
                    long cur = dp[r][c][k];
                    if (cur == INF) continue;

                    // Move Right
                    if (c + 1 < n) {
                        // pay cost
                        dp[r][c + 1][k] = Math.min(dp[r][c + 1][k], cur + cost[r][c + 1]);
                        // free cell
                        if (k + 1 <= f) dp[r][c + 1][k + 1] = Math.min(dp[r][c + 1][k + 1], cur);
                    }
                    // Move Down
                    if (r + 1 < m) {
                        dp[r + 1][c][k] = Math.min(dp[r + 1][c][k], cur + cost[r + 1][c]);
                        if (k + 1 <= f) dp[r + 1][c][k + 1] = Math.min(dp[r + 1][c][k + 1], cur);
                    }
                }
            }
        }

        long ans = INF;
        for (int k = 0; k <= f; k++) ans = Math.min(ans, dp[m - 1][n - 1][k]);
        return (int) ans;
    }
}
```

### Python

```python
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
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

class Solution {
    static const long long INF = (long long)4e18;
public:
    int minCostWithFreeCells(const vector<vector<int>>& cost, int f) {
        int m = cost.size(), n = cost[0].size();
        vector<vector<vector<long long>>> dp(m, vector<vector<long long>>(n, vector<long long>(f + 1, INF)));
        dp[0][0][0] = cost[0][0];
        if (f > 0) dp[0][0][1] = 0;

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                for (int k = 0; k <= f; k++) {
                    long long cur = dp[r][c][k];
                    if (cur == INF) continue;
                    if (c + 1 < n) {
                        dp[r][c + 1][k] = min(dp[r][c + 1][k], cur + cost[r][c + 1]);
                        if (k + 1 <= f) dp[r][c + 1][k + 1] = min(dp[r][c + 1][k + 1], cur);
                    }
                    if (r + 1 < m) {
                        dp[r + 1][c][k] = min(dp[r + 1][c][k], cur + cost[r + 1][c]);
                        if (k + 1 <= f) dp[r + 1][c][k + 1] = min(dp[r + 1][c][k + 1], cur);
                    }
                }
            }
        }

        long long ans = INF;
        for (int k = 0; k <= f; k++) ans = min(ans, dp[m - 1][n - 1][k]);
        return (int)ans;
    }
};
```

### JavaScript

```javascript
class Solution {
  minCostWithFreeCells(cost, f) {
    const m = cost.length, n = cost[0].length;
    const INF = 4e18;
    const dp = Array.from({ length: m }, () =>
      Array.from({ length: n }, () => new Array(f + 1).fill(INF))
    );
    dp[0][0][0] = cost[0][0];
    if (f > 0) dp[0][0][1] = 0;

    for (let r = 0; r < m; r++) {
      for (let c = 0; c < n; c++) {
        for (let k = 0; k <= f; k++) {
          const cur = dp[r][c][k];
          if (cur >= INF) continue;
          if (c + 1 < n) {
            dp[r][c + 1][k] = Math.min(dp[r][c + 1][k], cur + cost[r][c + 1]);
            if (k + 1 <= f) dp[r][c + 1][k + 1] = Math.min(dp[r][c + 1][k + 1], cur);
          }
          if (r + 1 < m) {
            dp[r + 1][c][k] = Math.min(dp[r + 1][c][k], cur + cost[r + 1][c]);
            if (k + 1 <= f) dp[r + 1][c][k + 1] = Math.min(dp[r + 1][c][k + 1], cur);
          }
        }
      }
    }

    let ans = INF;
    for (let k = 0; k <= f; k++) ans = Math.min(ans, dp[m - 1][n - 1][k]);
    return ans;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
Sample:

```
2 2
5 3
4 1
f = 1
```

- Start `(0,0)=5`
- Best free choice is `(0,0)`:
  - cost = 0 + 3 + 1 = 4
- Any other free choice gives 6 or more

Answer: 4.

### State Evolution Table

| Row | Col | Free Used | Cost at Cell | DP[i][j][f] | Decision |
|-----|-----|-----------|--------------|-------------|----------|
| 0   | 0   | 0         | 5            | 5           | Pay cost |
| 0   | 0   | 1         | 5            | 0           | Use free |
| 0   | 1   | 0         | 3            | 8           | From (0,0,0) + 3 |
| 0   | 1   | 1         | 3            | 3           | From (0,0,1) + 3 OR (0,0,0) + free |
| 0   | 1   | 2         | 3            | 0           | From (0,0,1) + free |
| 1   | 0   | 0         | 4            | 9           | From (0,0,0) + 4 |
| 1   | 0   | 1         | 4            | 4           | From (0,0,1) + 4 OR (0,0,0) + free |
| 1   | 1   | 0         | 1            | 9           | min(from top, from left) + 1 |
| 1   | 1   | 1         | 1            | 4           | min options with k=1 |
| 1   | 1   | 2         | 1            | 1           | Best path using 2 free cells |

**Best Answer:** min(dp[1][1][0], dp[1][1][1], dp[1][1][2]) = min(9, 4, 1) = **1** (if we can use 2 free cells)
With f=1: min(dp[1][1][0], dp[1][1][1]) = min(9, 4) = **4**

![Example Visualization](../images/DP-009/example-1.png)

## ✅ Proof of Correctness

We consider all ways to reach each cell `(r,c)` with any allowed number of free cells `k`. For each move, we try:

- paying the next cell’s cost, or
- marking the next cell free (if budget permits)

Thus every valid path with ≤ f free cells is represented. Taking the min over `k` at the destination gives the optimal cost. Because transitions only come from top or left (the only allowed moves), and we take minima over all feasible previous states, the DP finds the global optimum.

### Common Mistakes to Avoid

1. **Forgetting to allow freeing the start or end cell**
2. **Mixing up “exactly k free cells” vs “at most f”**
   - We store exact k in state, then take min over k at the end.
3. **Overflow in INT**
   - Use 64-bit (`long`/`long long`); costs can sum to ~4e8 before discounts.
4. **Not initializing unreachable states to INF**
5. **Confusing move directions** (only Right/Down allowed)


## Related Concepts

- Grid shortest path with constraints
- DP with resource budgets
- 3D DP vs space-optimized rolling
