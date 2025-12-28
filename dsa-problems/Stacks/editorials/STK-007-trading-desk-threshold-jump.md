---
title: Trading Desk Threshold Jump
slug: trading-desk-threshold-jump
difficulty: Medium
difficulty_score: 48
tags:
- Stack
- Monotonic Stack
- Next Greater Element
problem_id: STK_TRADING_DESK_THRESHOLD_JUMP__2549
display_id: STK-007
topics:
- Stack
- Monotonic Stack
- Arrays
---
# Trading Desk Threshold Jump - Editorial

## Problem Summary

For each price `p[i]` in an array, find the number of steps forward (distance) to the nearest future price `p[j]` (where `j > i`) such that `p[j] >= p[i] + t`. If no such price exists, output `0`.


## Constraints

- `1 <= n <= 200000`
- `0 <= p[i], t <= 10^9`
## Real-World Scenario

Imagine you are an **Algorithmic Trader**.
-   You buy a stock at price `P`.
-   You have a strict rule: you only sell if the price rises by at least `T` dollars (i.e., reaches `P + T`).
-   You want to know, for every possible buying moment in history, how long you would have had to wait to trigger a sell.
-   If the price never rose by `T` after that point, you would have been stuck holding the bag forever (wait time 0 or infinity).

## Problem Exploration

### 1. Next Greater Element Variation
-   This is very similar to the "Next Greater Element" problem.
-   Standard NGE: Find nearest `j > i` such that `p[j] > p[i]`.
-   Our Problem: Find nearest `j > i` such that `p[j] >= p[i] + t`.
-   The condition `p[j] >= p[i] + t` depends on both `p[i]` and `p[j]`.

### 2. Segment Tree Approach
-   This problem requires finding the nearest future index with a value threshold.
-   We use **Coordinate Compression** with a **Segment Tree** to efficiently query minimum indices.
-   The approach:
    1. Map all values to ranks using coordinate compression.
    2. Build a Segment Tree that stores minimum indices for value ranges.
    3. Process prices from right to left.
    4. For each position, query for the nearest future price meeting the threshold.
-   **Complexity**: `O(N log N)` for both coordinate compression and segment tree operations.

## Approaches

### Approach 1: Coordinate Compression + Segment Tree
-   Map values to ranks.
-   Use a Segment Tree to store the minimum index for each value range.
-   Process Right-to-Left.
-   Complexity: `O(N log N)`.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    int[] tree;
    int size;

    void update(int node, int start, int end, int idx, int val) {
        if (start == end) {
            tree[node] = val; // We process R-to-L, so new val (index i) is always smaller/better
            return;
        }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, val);
        else update(2 * node + 1, mid + 1, end, idx, val);
        tree[node] = Math.min(tree[2 * node], tree[2 * node + 1]);
    }

    int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return Integer.MAX_VALUE;
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return Math.min(query(2 * node, start, mid, l, r), query(2 * node + 1, mid + 1, end, l, r));
    }

    public int[] thresholdJump(int[] prices, int t) {
        int n = prices.length;
        TreeSet<Integer> sortedValues = new TreeSet<>();
        for (int p : prices) {
            sortedValues.add(p);
            // We don't strictly need p+t in compression if we use lower_bound logic on just p values
            // But adding p+t makes it easier to map exactly.
        }
        
        // Map values to ranks 0..m-1
        List<Integer> distinct = new ArrayList<>(sortedValues);
        Map<Integer, Integer> rankMap = new HashMap<>();
        for (int i = 0; i < distinct.size(); i++) {
            rankMap.put(distinct.get(i), i);
        }
        
        size = distinct.size();
        tree = new int[4 * size];
        Arrays.fill(tree, Integer.MAX_VALUE);
        
        int[] result = new int[n];
        
        for (int i = n - 1; i >= 0; i--) {
            int target = prices[i] + t;
            // Find rank of smallest value >= target
            int r = Collections.binarySearch(distinct, target);
            if (r < 0) r = -r - 1; // Insertion point
            
            if (r < size) {
                int nearestIdx = query(1, 0, size - 1, r, size - 1);
                if (nearestIdx != Integer.MAX_VALUE) {
                    result[i] = nearestIdx - i;
                } else {
                    result[i] = 0;
                }
            } else {
                result[i] = 0;
            }
            
            update(1, 0, size - 1, rankMap.get(prices[i]), i);
        }
        
        return result;
    }
}
```

### Python

```python
def threshold_jump(prices: list[int], t: int) -> list[int]:
    """For each index, find steps to next price >= p[i] + t"""
    n = len(prices)
    result = []
    
    for i in range(n):
        target = prices[i] + t
        steps = 0
        found = False
        
        # Search forward for first price >= target
        for j in range(i + 1, n):
            steps += 1
            if prices[j] >= target:
                found = True
                break
        
        result.append(steps if found else 0)
    
    return result

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n, threshold = map(int, lines[0].split())
    prices = list(map(int, lines[1].split()))
    
    result = threshold_jump(prices, threshold)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()

```

### C++

```cpp
#include <vector>
#include <algorithm>
#include <map>

using namespace std;

class Solution {
    vector<int> tree;
    int size;

    void update(int node, int start, int end, int idx, int val) {
        if (start == end) {
            tree[node] = val;
            return;
        }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, val);
        else update(2 * node + 1, mid + 1, end, idx, val);
        tree[node] = min(tree[2 * node], tree[2 * node + 1]);
    }

    int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 2e9;
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return min(query(2 * node, start, mid, l, r), query(2 * node + 1, mid + 1, end, l, r));
    }

public:
    vector<int> thresholdJump(const vector<int>& prices, int t) {
        int n = prices.size();
        vector<int> distinct = prices;
        sort(distinct.begin(), distinct.end());
        distinct.erase(unique(distinct.begin(), distinct.end()), distinct.end());
        
        size = distinct.size();
        tree.assign(4 * size, 2e9);
        
        vector<int> result(n, 0);
        
        for (int i = n - 1; i >= 0; i--) {
            long long target = (long long)prices[i] + t;
            auto it = lower_bound(distinct.begin(), distinct.end(), target);
            
            if (it != distinct.end()) {
                int r = distance(distinct.begin(), it);
                int nearestIdx = query(1, 0, size - 1, r, size - 1);
                if (nearestIdx != 2e9) {
                    result[i] = nearestIdx - i;
                }
            }
            
            int rank = lower_bound(distinct.begin(), distinct.end(), prices[i]) - distinct.begin();
            update(1, 0, size - 1, rank, i);
        }
        
        return result;
    }
};
```

### JavaScript

```javascript
class Solution {
  thresholdJump(prices, t) {
    const n = prices.length;
    
    // Coordinate Compression
    const distinct = Array.from(new Set(prices)).sort((a, b) => a - b);
    const rankMap = new Map();
    distinct.forEach((val, idx) => rankMap.set(val, idx));
    const m = distinct.length;
    
    // Segment Tree
    const tree = new Int32Array(4 * m).fill(2e9);
    
    const update = (node, start, end, idx, val) => {
      if (start === end) {
        tree[node] = val;
        return;
      }
      const mid = Math.floor((start + end) / 2);
      if (idx <= mid) update(2 * node, start, mid, idx, val);
      else update(2 * node + 1, mid + 1, end, idx, val);
      tree[node] = Math.min(tree[2 * node], tree[2 * node + 1]);
    };
    
    const query = (node, start, end, l, r) => {
      if (r < start || end < l) return 2e9;
      if (l <= start && end <= r) return tree[node];
      const mid = Math.floor((start + end) / 2);
      return Math.min(query(2 * node, start, mid, l, r),
                      query(2 * node + 1, mid + 1, end, l, r));
    };
    
    const result = new Int32Array(n).fill(0);
    
    // Binary Search helper
    const lowerBound = (arr, target) => {
      let l = 0, r = arr.length;
      while (l < r) {
        const mid = Math.floor((l + r) / 2);
        if (arr[mid] < target) l = mid + 1;
        else r = mid;
      }
      return l;
    };
    
    for (let i = n - 1; i >= 0; i--) {
      const target = prices[i] + t;
      const r = lowerBound(distinct, target);
      
      if (r < m) {
        const nearestIdx = query(1, 0, m - 1, r, m - 1);
        if (nearestIdx !== 2e9) {
          result[i] = nearestIdx - i;
        }
      }
      
      update(1, 0, m - 1, rankMap.get(prices[i]), i);
    }
    
    return Array.from(result);
  }
}
```

### Python

```python

def threshold_jump(prices, threshold):
    count = 0
    stack = []
    
    for price in prices:
        while stack and stack[-1] <= price - threshold:
            stack.pop()
            count += 1
        stack.append(price)
    
    return count

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n, threshold = map(int, lines[0].split())
    prices = list(map(int, lines[1].split()))
    
    print(threshold_jump(prices, threshold))

if __name__ == "__main__":
    main()

```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:** `3 1 4 6 5`, `t=2`

1.  **Distinct**: `[1, 3, 4, 5, 6]`. Ranks: `1->0, 3->1, 4->2, 5->3, 6->4`.
2.  Process right to left:
    -   `i=4` (5): Target `5+2=7`. No element >= 7. Res `0`.
    -   `i=3` (6): Target `6+2=8`. No element >= 8. Res `0`.
    -   `i=2` (4): Target `4+2=6`. Element `6` at index 3. Res `3 - 2 = 1`.
    -   `i=1` (1): Target `1+2=3`. Element `3` at index 0, `4` at index 2. Nearest is index 2. Res `2 - 1 = 1`.
    -   `i=0` (3): Target `3+2=5`. Element `5` at index 4, `6` at index 3. Nearest is index 3. Res `3 - 0 = 3`.

**Output:** `3 1 1 0 0`

## Proof of Correctness

-   **Range Query**: By mapping values to ranks, we transform the condition `val >= target` into `rank >= target_rank`.
-   **Min Index**: The Segment Tree efficiently finds the minimum index in the suffix of ranks, which corresponds to the nearest future element satisfying the value condition.
-   **Right-to-Left**: Processing in reverse ensures that when we query for `p[i]`, the tree only contains indices `j > i`.

## Interview Extensions

1.  **Max Wait Time**: Find the maximum wait time instead of per-element.
2.  **Dynamic Updates**: What if prices change? (SegTree handles updates in `O(log N)`).

### Common Mistakes

-   **Coordinate Compression**: Forgetting to compress values when they can be up to `10^9`.
-   **SegTree Range**: Querying `[0, size-1]` instead of `[target_rank, size-1]`.
-   **Infinity**: Initializing min-tree with 0 instead of infinity.
