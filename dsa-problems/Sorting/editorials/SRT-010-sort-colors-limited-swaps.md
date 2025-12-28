---
title: Sort Colors With Limited Swaps
slug: sort-colors-limited-swaps
difficulty: Medium
difficulty_score: 57
tags:
  - Greedy
  - Adjacent Swaps
  - Sorting
problem_id: SRT_SORT_COLORS_LIMITED_SWAPS__4762
display_id: SRT-010
topics:
  - Sorting
  - Greedy
  - Adjacent Swaps
---

# Sort Colors With Limited Swaps - Editorial

## Problem Summary

You are given an array consisting of only 0s, 1s, and 2s. You are allowed to perform at most `S` adjacent swaps. Your goal is to make the array as lexicographically small as possible.

## 🌍 Real-World Scenario

**Scenario Title:** Emergency Traffic Queue Management

Imagine you are managing a **Traffic Queue**.

- Vehicles are of three types: Emergency (0), Public Transport (1), and Private Cars (2).
- You want Emergency vehicles at the front, followed by Public Transport, then Private Cars.
- However, the road is narrow (single lane), and you can only swap adjacent vehicles.
- Each swap takes time/effort, and you have a limited budget of `S` swaps.
- You want to prioritize the most important vehicles as much as possible within your budget.

![Real-World Application](../images/SRT-010/real-world-scenario.png)

## Problem Exploration

### 1. Lexicographically Smallest

- "Lexicographically smallest" means we want smaller numbers at the beginning of the array.
- Ideally, we want `0`s at the start, then `1`s, then `2`s.
- Since we have a budget `S`, we should greedily try to bring the smallest available number to the current position `i`, provided the cost (distance) is within `S`.

### 2. Greedy Strategy

- Iterate through positions `i` from `0` to `n-1`.
- At each position `i`, we want to place the smallest possible value found in the reachable range `[i, i + S]`.
- Since values are only 0, 1, 2, we search for the first occurrence of `0` in `[i, i + S]`.
- If found at index `j`, we move it to `i`. Cost is `j - i`. Subtract from `S`.
- If no `0` is reachable, search for `1`.
- If no `1` is reachable, we must settle for `2` (which is already there or nearby).

### 3. Optimization for 0, 1, 2

- Since there are only 3 values, we don't need a general Range Minimum Query (RMQ) structure.
- We can just store the indices of all 0s, 1s, and 2s in three separate queues (or lists).
- At current position `i`, we check the head of the `0-queue`. Let its index be `idx0`.
  - If `idx0` is valid (not used) and `cost = (current_pos_of_idx0 - i) <= S`, we pick it.
  - Yes. If we move an element from `j` to `i`, all elements between `i` and `j` shift right.
  - Using a Fenwick Tree (BIT) can track how many elements have been moved to the front, allowing us to calculate the _current_ index of an original index.
  - Current Index of `orig_idx` = `orig_idx` + (number of elements originally after it that moved before it) - (number of elements originally before it that moved after it?? No).
  - With `N=200,000`, `O(N^2)` is too slow. We need `O(N log N)` or `O(N)`.

### 4. Simplified Greedy with Queues

- Store indices of 0s, 1s, 2s in queues `Q0, Q1, Q2`.
- We construct the result array one by one.
- For the current slot in result (say `k`-th slot):
  - Check `Q0`: `idx = Q0.peek()`. Cost = `query_bit(idx)`. (Number of elements strictly before `idx` that are NOT yet moved).
  - If `cost <= S`, pick 0. Remove from `Q0`. Update BIT (mark `idx` as removed). `S -= cost`.
  - Else check `Q1`.
  - Else pick `Q2`.
- BIT is initialized with 1s at all positions. When an element is moved, update position to 0.
- `query(idx)` returns how many elements are still "active" before `idx`. This is exactly the number of swaps needed to bring `arr[idx]` to the current front.

## Approaches

### Approach 1: Greedy with Fenwick Tree

- Store locations of 0s, 1s, 2s.
- Use BIT to track active elements and calculate displacement costs.
- Iterate `N` times to fill the result array.
- Complexity: `O(N log N)`.

## Implementations

### Java

```java
import java.util.*;

class Solution {

    public int[] sortWithSwapsFixed(int[] arr, long S) {
        int n = arr.length;
        Queue<Integer> q0 = new LinkedList<>();
        Queue<Integer> q1 = new LinkedList<>();
        Queue<Integer> q2 = new LinkedList<>();

        for (int i = 0; i < n; i++) {
            if (arr[i] == 0) q0.add(i);
            else if (arr[i] == 1) q1.add(i);
            else q2.add(i);
        }

        int[] bit = new int[n + 1];
        for (int i = 0; i < n; i++) update(bit, i + 1, 1);

        int[] res = new int[n];

        for (int i = 0; i < n; i++) {
            Integer idx0 = q0.peek();
            Integer idx1 = q1.peek();
            Integer idx2 = q2.peek();

            long cost0 = (idx0 != null) ? query(bit, idx0) : Long.MAX_VALUE;
            long cost1 = (idx1 != null) ? query(bit, idx1) : Long.MAX_VALUE;

            if (cost0 <= S) {
                S -= cost0;
                res[i] = 0;
                q0.poll();
                update(bit, idx0 + 1, -1);
            } else if (cost1 <= S) {

                S -= cost1;
                res[i] = 1;
                q1.poll();
                update(bit, idx1 + 1, -1);
            } else {
                // Pick the element with minimum index (cost 0)
                int minIdx = Integer.MAX_VALUE;
                if (idx0 != null) minIdx = Math.min(minIdx, idx0);
                if (idx1 != null) minIdx = Math.min(minIdx, idx1);
                if (idx2 != null) minIdx = Math.min(minIdx, idx2);

                if (idx0 != null && minIdx == idx0) { res[i]=0; q0.poll(); update(bit, idx0+1, -1); }
                else if (idx1 != null && minIdx == idx1) { res[i]=1; q1.poll(); update(bit, idx1+1, -1); }
                else { res[i]=2; q2.poll(); update(bit, idx2+1, -1); }
            }
        }
        return res;
    }

    private void update(int[] bit, int idx, int val) {
        for (; idx < bit.length; idx += idx & -idx) bit[idx] += val;
    }

    private int query(int[] bit, int idx) {
        int sum = 0;
        for (; idx > 0; idx -= idx & -idx) sum += bit[idx];
        return sum;
    }
}
```

### Python

```python
from collections import deque

def sort_with_swaps(arr: list[int], S: int) -> list[int]:
    n = len(arr)
    q0 = deque([i for i, x in enumerate(arr) if x == 0])
    q1 = deque([i for i, x in enumerate(arr) if x == 1])
    q2 = deque([i for i, x in enumerate(arr) if x == 2])

    bit = [0] * (n + 1)

    def update(i, val):
        while i <= n:
            bit[i] += val
            i += i & (-i)

    def query(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s

    for i in range(n):
        update(i + 1, 1)

    res = []
    for _ in range(n):
        idx0 = q0[0] if q0 else None
        idx1 = q1[0] if q1 else None
        idx2 = q2[0] if q2 else None

        cost0 = query(idx0) if idx0 is not None else float('inf')
        cost1 = query(idx1) if idx1 is not None else float('inf')

        if cost0 <= S:
            S -= cost0
            res.append(0)
            q0.popleft()
            update(idx0 + 1, -1)
        elif cost1 <= S:
            S -= cost1
            res.append(1)
            q1.popleft()
            update(idx1 + 1, -1)
        else:
            # Pick min index
            min_idx = float('inf')
            if idx0 is not None: min_idx = min(min_idx, idx0)
            if idx1 is not None: min_idx = min(min_idx, idx1)
            if idx2 is not None: min_idx = min(min_idx, idx2)

            if idx0 is not None and min_idx == idx0:
                res.append(0)
                q0.popleft()
                update(idx0 + 1, -1)
            elif idx1 is not None and min_idx == idx1:
                res.append(1)
                q1.popleft()
                update(idx1 + 1, -1)
            else:
                res.append(2)
                q2.popleft()
                update(idx2 + 1, -1)

    return res

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    s = int(input())
    result = sort_with_swaps(arr, s)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <queue>
#include <algorithm>
#include <climits>

using namespace std;

class Solution {
    vector<int> bit;
    int n;

    void update(int idx, int val) {
        for (; idx <= n; idx += idx & -idx) bit[idx] += val;
    }

    int query(int idx) {
        int sum = 0;
        for (; idx > 0; idx -= idx & -idx) sum += bit[idx];
        return sum;
    }

public:
    vector<int> sortWithSwaps(const vector<int>& arr, long long S) {
        n = arr.size();
        queue<int> q0, q1, q2;
        for (int i = 0; i < n; i++) {
            if (arr[i] == 0) q0.push(i);
            else if (arr[i] == 1) q1.push(i);
            else q2.push(i);
        }

        bit.assign(n + 1, 0);
        for (int i = 0; i < n; i++) update(i + 1, 1);

        vector<int> res;
        res.reserve(n);

        for (int i = 0; i < n; i++) {
            int idx0 = q0.empty() ? -1 : q0.front();
            int idx1 = q1.empty() ? -1 : q1.front();
            int idx2 = q2.empty() ? -1 : q2.front();

            long long cost0 = (idx0 != -1) ? query(idx0) : LLONG_MAX;
            long long cost1 = (idx1 != -1) ? query(idx1) : LLONG_MAX;

            if (cost0 <= S) {
                S -= cost0;
                res.push_back(0);
                q0.pop();
                update(idx0 + 1, -1);
            } else if (cost1 <= S) {
                S -= cost1;
                res.push_back(1);
                q1.pop();
                update(idx1 + 1, -1);
            } else {
                int minIdx = INT_MAX;
                if (idx0 != -1) minIdx = min(minIdx, idx0);
                if (idx1 != -1) minIdx = min(minIdx, idx1);
                if (idx2 != -1) minIdx = min(minIdx, idx2);

                if (idx0 != -1 && minIdx == idx0) {
                    res.push_back(0); q0.pop(); update(idx0 + 1, -1);
                } else if (idx1 != -1 && minIdx == idx1) {
                    res.push_back(1); q1.pop(); update(idx1 + 1, -1);
                } else {
                    res.push_back(2); q2.pop(); update(idx2 + 1, -1);
                }
            }
        }
        return res;
    }
};
```

### JavaScript

```javascript
class Solution {
  sortWithSwaps(arr, S) {
    const n = arr.length;
    const q0 = [],
      q1 = [],
      q2 = [];
    for (let i = 0; i < n; i++) {
      if (arr[i] === 0) q0.push(i);
      else if (arr[i] === 1) q1.push(i);
      else q2.push(i);
    }

    // Use pointers for queue simulation to avoid O(N) shift
    let p0 = 0,
      p1 = 0,
      p2 = 0;

    const bit = new Int32Array(n + 1);
    const update = (idx, val) => {
      for (; idx <= n; idx += idx & -idx) bit[idx] += val;
    };
    const query = (idx) => {
      let sum = 0;
      for (; idx > 0; idx -= idx & -idx) sum += bit[idx];
      return sum;
    };

    for (let i = 0; i < n; i++) update(i + 1, 1);

    const res = [];

    for (let i = 0; i < n; i++) {
      const idx0 = p0 < q0.length ? q0[p0] : -1;
      const idx1 = p1 < q1.length ? q1[p1] : -1;
      const idx2 = p2 < q2.length ? q2[p2] : -1;

      const cost0 = idx0 !== -1 ? query(idx0) : Infinity;
      const cost1 = idx1 !== -1 ? query(idx1) : Infinity;

      if (cost0 <= S) {
        S -= cost0;
        res.push(0);
        p0++;
        update(idx0 + 1, -1);
      } else if (cost1 <= S) {
        S -= cost1;
        res.push(1);
        p1++;
        update(idx1 + 1, -1);
      } else {
        let minIdx = Infinity;
        if (idx0 !== -1) minIdx = Math.min(minIdx, idx0);
        if (idx1 !== -1) minIdx = Math.min(minIdx, idx1);
        if (idx2 !== -1) minIdx = Math.min(minIdx, idx2);

        if (idx0 !== -1 && minIdx === idx0) {
          res.push(0);
          p0++;
          update(idx0 + 1, -1);
        } else if (idx1 !== -1 && minIdx === idx1) {
          res.push(1);
          p1++;
          update(idx1 + 1, -1);
        } else {
          res.push(2);
          p2++;
          update(idx2 + 1, -1);
        }
      }
    }
    return res;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input:**
`3`
`2 1 0`
`1`

1.  **Init**: `Q0=[2], Q1=[1], Q2=[0]`. `BIT=[1,1,1]`. `S=1`.
2.  **Step 1**:
    - `idx0=2`. `cost0 = query(2) = 2`. `2 > 1`. Can't pick 0.
    - `idx1=1`. `cost1 = query(1) = 1`. `1 <= 1`. Pick 1.
    - `S = 1 - 1 = 0`. `res=[1]`. `Q1` empty. `BIT` update `2` -> `[1,0,1]`.
3.  **Step 2**:
    - `idx0=2`. `cost0 = query(2) = 1`. `1 > 0`. Can't pick 0.
    - `idx1=null`.
    - Pick min index. `min(2, 0) = 0`. `idx2=0`.
    - Pick 2. `res=[1, 2]`. `Q2` empty. `BIT` update `1` -> `[0,0,1]`.
4.  **Step 3**:
    - `idx0=2`. `cost0=0`. `0 <= 0`. Pick 0.
    - `res=[1, 2, 0]`.
5.  **Result**: `1 2 0`.

## Proof of Correctness

- **Greedy Choice**: We always prefer smaller values.
- **Cost Calculation**: The BIT correctly maintains the number of elements _currently_ preceding any original index `j`. This is exactly the number of swaps needed to move `arr[j]` to the front of the remaining array.
- **Feasibility**: We only pick if `cost <= S`. If we can't afford a better element, we are forced to pick the current front element (cost 0), which preserves the relative order of un-swapped elements.

## Interview Extensions

1.  **Values up to K?**
    - Same logic, just check `Q0` to `QK`. `O(N * K)`.
2.  **Minimize Inversions?**
    - This greedy strategy minimizes the lexicographical value, which is different from minimizing inversions. But minimizing inversions with limited swaps is harder (or simpler? Bubble sort logic).

### Common Mistakes

- **Incorrect Cost**: Using `idx - i` assumes no elements were moved. BIT is necessary.
- **Queue Management**: In JS, `shift()` is `O(N)`. Use pointers or a proper Queue class.
