---
problem_id: DP_BAL_PART_SIZE__5120
display_id: DP-012
slug: balanced-partition-size-limit
title: "Balanced Partition With Size Limit"
difficulty: Medium
difficulty_score: 56
topics:
  - Dynamic Programming
  - Subset Sum
  - Optimization
tags:
  - dp
  - subset-sum
  - partition
  - medium
premium: true
subscription_tier: basic
---

# DP-012: Balanced Partition With Size Limit

## 📋 Problem Summary

Partition an array into two groups so that:

- the absolute difference of group sums is at most `D`
- among all such partitions, the **larger group size** is minimized

Return the minimum possible size of the larger group, or `-1` if no valid partition exists.

## 🌍 Real-World Scenario

**Scenario Title:** Fair Lab Team Split With Budget Deviation Limit

In a lab, students have “workload scores” (positive or negative depending on prior credits). You must split the class into two teams:

- total workload difference between teams must be within `D`
- keep team sizes as balanced as possible (minimize larger team)

This models constrained fair-split problems in scheduling, load balancing, and hiring panels.

**Why This Problem Matters:**

- Combines subset-sum feasibility with a size optimization
- Requires careful DP design when values can be negative
- Shows how to derive the optimal size from reachable sums

![Real-World Application](../images/DP-012/real-world-scenario.png)

## ✅ Clarifications

- Both groups are allowed to be empty in principle; the DP will tell if that’s optimal or feasible.
- Values may be negative, so sums can be negative; we must offset indices.
- We do **not** minimize the difference (it’s constrained), we minimize `max(sizeA, sizeB)`.

## Detailed Explanation

### Reformulate the goal

Let:

- `n` = number of elements
- `total = sum(a)`
- pick a subset `S` of size `k` with sum `s`

The other group has:

- size `n-k`
- sum `total - s`

Constraint:

`| (total - s) - s | = | total - 2s | <= D`

Objective:

Minimize `max(k, n-k)` among all `(k, s)` that satisfy the constraint.

### DP over subset size and sum

Because `n <= 50` and `|a[i]| <= 500`, the total absolute sum is at most `50 * 500 = 25000`.

We can do a classic 0/1 subset DP with size:

`dp[k] = set of reachable sums using exactly k elements`

Initialize:

- `dp[0] = {0}`
- `dp[k>0] = ∅`

For each value `x`:

- iterate `k` from `n-1` down to `0`:
  - for each sum `s` in `dp[k]`, add `s+x` to `dp[k+1]`

After processing all elements, check all `(k, s)`:

- if `| total - 2s | <= D`, candidate answer = `max(k, n-k)`
- take the minimum candidate

If no candidate exists, answer = `-1`.

### Why this works

The DP enumerates all possible subset sizes and sums. The constraint only depends on `s` and `k` (through `total` and `n-k`). So scanning all reachable `(k,s)` pairs finds the optimal size.

### Complexity

- States: `O(n * number_of_sums)`; we store sets of sums per k
- Each step inserts new sums: worst-case sums count is `O(n * value_range)` which is fine for `n=50, range=25000`
- Time: roughly `O(n^2 * value_range)` but prunes well in practice at these limits
- Space: `O(n * value_range)` for reachable sums

![Algorithm Visualization](../images/DP-012/algorithm-visualization.png)
![Algorithm Steps](../images/DP-012/algorithm-steps.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public int minLargerGroupSize(int[] a, int D) {
        int n = a.length;
        int total = 0;
        for (int x : a) total += x;

        List<Set<Integer>> dp = new ArrayList<>();
        for (int i = 0; i <= n; i++) dp.add(new HashSet<>());
        dp.get(0).add(0);

        for (int x : a) {
            for (int k = n - 1; k >= 0; k--) {
                for (int s : new ArrayList<>(dp.get(k))) {
                    dp.get(k + 1).add(s + x);
                }
            }
        }

        int ans = Integer.MAX_VALUE;
        for (int k = 0; k <= n; k++) {
            for (int s : dp.get(k)) {
                if (Math.abs(total - 2 * s) <= D) {
                    ans = Math.min(ans, Math.max(k, n - k));
                }
            }
        }
        return ans == Integer.MAX_VALUE ? -1 : ans;
    }
}
```

### Python

```python
def min_larger_group_size(a: list[int], D: int) -> int:
    n = len(a)
    total = sum(a)
    dp = [set() for _ in range(n + 1)]
    dp[0].add(0)

    for x in a:
        for k in range(n - 1, -1, -1):
            for s in list(dp[k]):
                dp[k + 1].add(s + x)

    ans = None
    for k in range(n + 1):
        for s in dp[k]:
            if abs(total - 2 * s) <= D:
                cand = max(k, n - k)
                if ans is None or cand < ans:
                    ans = cand
    return -1 if ans is None else ans

def main():
    n, D = map(int, input().split())
    a = list(map(int, input().split()))
    print(min_larger_group_size(a, D))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    int minLargerGroupSize(const vector<int>& a, int D) {
        int n = (int)a.size();
        int total = accumulate(a.begin(), a.end(), 0);
        vector<unordered_set<int>> dp(n + 1);
        dp[0].insert(0);

        for (int x : a) {
            for (int k = n - 1; k >= 0; k--) {
                vector<int> cur(dp[k].begin(), dp[k].end());
                for (int s : cur) dp[k + 1].insert(s + x);
            }
        }

        int ans = INT_MAX;
        for (int k = 0; k <= n; k++) {
            for (int s : dp[k]) {
                if (abs(total - 2 * s) <= D) {
                    ans = min(ans, max(k, n - k));
                }
            }
        }
        return ans == INT_MAX ? -1 : ans;
    }
};
```

### JavaScript

```javascript
class Solution {
  minLargerGroupSize(a, D) {
    const n = a.length;
    const total = a.reduce((s, x) => s + x, 0);
    const dp = Array.from({ length: n + 1 }, () => new Set());
    dp[0].add(0);

    for (const x of a) {
      for (let k = n - 1; k >= 0; k--) {
        for (const s of Array.from(dp[k])) {
          dp[k + 1].add(s + x);
        }
      }
    }

    let ans = Infinity;
    for (let k = 0; k <= n; k++) {
      for (const s of dp[k]) {
        if (Math.abs(total - 2 * s) <= D) {
          ans = Math.min(ans, Math.max(k, n - k));
        }
      }
    }
    return ans === Infinity ? -1 : ans;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
Example: `a = [3,1,4,2], D = 1`

- `total = 10`
- Pick subset `{3,2}` (k=2, sum=5): other group sum=5, diff=0 ≤ 1, larger size = 2.
- No partition can make the larger size 1 (you’d need groups of sizes 1 and 3; diff would be ≥ 3).
- So answer = 2.

![Example Visualization](../images/DP-012/example-1.png)

## ✅ Proof of Correctness

The DP enumerates all possible pairs `(k, s)`:

- `k` = number of elements chosen for group A
- `s` = sum of those elements

For each pair, group B has size `n - k` and sum `total - s`. The partition constraint holds iff `|total - 2s| <= D`. For all such feasible pairs, we compute `max(k, n-k)`. The minimum of this value is exactly the optimal larger-group size.

Since the DP includes every subset size and sum combination, it captures all possible partitions; thus the minimum found is optimal. If no feasible pair exists, answer is `-1`.

### Common Mistakes to Avoid

1. **Minimizing the sum difference instead of respecting the constraint**
2. **Forgetting negative values** (need sets/offsets; using only positive indices will break)
3. **Not using descending k in the subset loop** (would reuse an element multiple times)
4. **Stopping early after finding one feasible partition** (need the min larger size)



## Related Concepts

- Subset DP over size and sum
- Partition problems with additional objectives
- Handling negative numbers in subset sums
