---
problem_id: DP_LIS_DIFF_RANGE__5881
display_id: DP-006
slug: strict-jump-lis-bounded
title: "Strict Jump LIS With Max Gap"
difficulty: Medium
difficulty_score: 64
topics:
  - Dynamic Programming
  - Segment Tree
  - Coordinate Compression
tags:
  - dp
  - lis
  - segment-tree
  - fenwick
  - medium
premium: true
subscription_tier: basic
---

# DP-006: Strict Jump LIS With Max Gap

## 📋 Problem Summary

Find the longest subsequence (preserving original order) where consecutive chosen values differ by a bounded range:

`d <= next - prev <= g`

This resembles LIS, but instead of “increasing” you need “difference in [d, g]”.

Constraints (`n` up to 100,000) force an `O(n log n)` approach.

## 🌍 Real-World Scenario

**Scenario Title:** Controlled Temperature Sampling

Suppose you’re processing sensor readings from a campus server room. You want to pick a sequence of readings (in time order) such that each new reading increases by:

- at least `d` (meaning a meaningful rise), but
- at most `g` (meaning it’s not a sudden spike)

This resembles trend detection in monitoring systems, finance (bounded jump prices), and anomaly analysis.

**Why This Problem Matters:**

- Trains “LIS with constraints” thinking (common interview pattern)
- Teaches coordinate compression + range maximum query
- Reinforces that `n=1e5` kills quadratic DP

![Real-World Application](../images/DP-006/real-world-scenario.png)

## ✅ Input/Output Clarifications

- Subsequence must preserve indices (`i1 < i2 < ...`).
- If `d = 0`, equal consecutive values are allowed.
- Negative numbers are allowed in the array.
- Answer is at least 1 (pick any single element).

## Detailed Explanation

### Value Range and Gap Visualization

```
Array: [10, 5, 20, 12, 8, 25]
d=3, g=15 (valid jump range)

For each element, valid previous values must be in [current - g, current - d]:

Step 0 (value 10):
  Can extend from values in [10-15, 10-3] = [-5, 7]
  No elements qualify → dp[0] = 1

Step 1 (value 5):
  Can extend from values in [5-15, 5-3] = [-10, 2]
  No elements qualify → dp[1] = 1

Step 2 (value 20):
  Can extend from values in [20-15, 20-3] = [5, 17]
  Values {10, 5, 12, 8} qualify
  Best dp among {10, 5, 12, 8} = 1
  dp[2] = 1 + 1 = 2

Step 3 (value 12):
  Can extend from values in [12-15, 12-3] = [-3, 9]
  Values {10, 5, 8} have dp = 1
  dp[3] = 1 + 1 = 2

Step 4 (value 8):
  Can extend from values in [8-15, 8-3] = [-7, 5]
  Value {5} qualifies with dp = 1
  dp[4] = 1 + 1 = 2

Step 5 (value 25):
  Can extend from values in [25-15, 25-3] = [10, 22]
  Values {20, 12} qualify
  Best dp among {20, 12} = 2
  dp[5] = 1 + 2 = 3

Answer: max(dp) = 3
```

### Naive DP (why it fails)

Classic DP idea:

`dp[i] = 1 + max(dp[j])` over all `j < i` such that `d <= a[i] - a[j] <= g`

This is correct but checking all `j` for each `i` costs `O(n^2)` in the worst case.

With `n=1e5`, that’s impossible.

### Key Insight: Query by value range, not by scanning indices

For each current value `x = a[i]`, we need the best previous dp among values in:

`[x - g, x - d]`

So the problem becomes:

- maintain a data structure over values that supports:
  - update at value `v`: store the best dp ending at `v`
  - query over a value interval: maximum dp in that interval

This is exactly a segment tree / Fenwick tree for range maximum.

### Coordinate Compression

Values are up to 1e9 and can be negative. We compress them:

1) Collect all values `a[i]` and sort unique to `vals`.
2) Map each `a[i]` to an index in `vals`.
3) To query `[x-g, x-d]`, find:
   - `L = lower_bound(vals, x-g)`
   - `R = upper_bound(vals, x-d) - 1`

Then query the segment tree on indices `[L, R]`.

### DP recurrence with segment tree

For each `x = a[i]`:

- `best = query(L, R)` (0 if empty range)
- `dp_i = best + 1`
- update at index of `x`: `tree[idx(x)] = max(tree[idx(x)], dp_i)`

This is safe because:

- we process elements in index order
- updates represent subsequences ending at already-processed positions

### Decision Tree for LIS with Bounded Jumps

```
For each element a[i] at index i:
    │
    ├─ Compute valid value range: [a[i] - g, a[i] - d]
    │
    ├─ Coordinate compress range to indices [L, R]
    │   │
    │   ├─ L = lower_bound(vals, a[i] - g)
    │   └─ R = upper_bound(vals, a[i] - d) - 1
    │
    ├─ Query segment tree for max dp in range [L, R]
    │   │
    │   └─ best = tree.query(L, R)
    │
    ├─ Compute dp[i] = best + 1
    │
    ├─ Update segment tree at compressed index of a[i]
    │   │
    │   └─ tree.update(index(a[i]), dp[i])
    │
    └─ Update global answer: ans = max(ans, dp[i])

Final answer: ans
```

## Naive Approach

### Algorithm

For each i:

1. Compute dp[i] by scanning all j < i and checking diff range.
2. Return max dp[i].

### Complexity

- Time: `O(n^2)` (TLE)
- Space: `O(n)`

## Optimal Approach (Compression + Segment Tree)

### Algorithm

1. Coordinate compress values of `a`.
2. Initialize a segment tree storing max dp per value index (initial 0).
3. For i = 0..n-1:
   - x = a[i]
   - compute value range `[x-g, x-d]`
   - query tree for maximum in that compressed index range
   - dp_i = best + 1
   - update tree at index of x with dp_i
4. Return global maximum dp_i.

### Complexity

- Time: `O(n log n)`
- Space: `O(n)` for compressed list and segment tree

![Algorithm Visualization](../images/DP-006/algorithm-visualization.png)
![Algorithm Steps](../images/DP-006/algorithm-steps.png)

## Implementations

### Java (Segment Tree)

```java
import java.util.*;

class Solution {
    static class SegTree {
        int n;
        int[] t;
        SegTree(int n) {
            this.n = n;
            this.t = new int[4 * n];
        }
        void update(int idx, int val) { update(1, 0, n - 1, idx, val); }
        private void update(int node, int l, int r, int idx, int val) {
            if (l == r) { t[node] = Math.max(t[node], val); return; }
            int mid = (l + r) >>> 1;
            if (idx <= mid) update(node << 1, l, mid, idx, val);
            else update(node << 1 | 1, mid + 1, r, idx, val);
            t[node] = Math.max(t[node << 1], t[node << 1 | 1]);
        }
        int query(int ql, int qr) {
            if (ql > qr) return 0;
            return query(1, 0, n - 1, ql, qr);
        }
        private int query(int node, int l, int r, int ql, int qr) {
            if (qr < l || r < ql) return 0;
            if (ql <= l && r <= qr) return t[node];
            int mid = (l + r) >>> 1;
            return Math.max(query(node << 1, l, mid, ql, qr), query(node << 1 | 1, mid + 1, r, ql, qr));
        }
    }

    private static int lowerBound(long[] a, long x) {
        int l = 0, r = a.length;
        while (l < r) {
            int m = (l + r) >>> 1;
            if (a[m] >= x) r = m;
            else l = m + 1;
        }
        return l;
    }

    private static int upperBound(long[] a, long x) {
        int l = 0, r = a.length;
        while (l < r) {
            int m = (l + r) >>> 1;
            if (a[m] <= x) l = m + 1;
            else r = m;
        }
        return l;
    }

    public int longestBoundedDiffSubsequence(int[] arr, long d, long g) {
        int n = arr.length;
        long[] vals = new long[n];
        for (int i = 0; i < n; i++) vals[i] = arr[i];
        Arrays.sort(vals);
        int m = 0;
        for (int i = 0; i < n; i++) {
            if (i == 0 || vals[i] != vals[i - 1]) vals[m++] = vals[i];
        }
        vals = Arrays.copyOf(vals, m);

        SegTree st = new SegTree(m);
        int ans = 1;

        for (int x0 : arr) {
            long x = x0;
            long lo = x - g;
            long hi = x - d;
            int L = lowerBound(vals, lo);
            int R = upperBound(vals, hi) - 1;
            int best = st.query(L, R);
            int dp = best + 1;

            int idx = lowerBound(vals, x);
            st.update(idx, dp);
            ans = Math.max(ans, dp);
        }
        return ans;
    }
}
```

### Python (Fenwick Tree for max)

```python
from bisect import bisect_left, bisect_right

class FenwickMax:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i: int, val: int) -> None:
        # i is 0-based
        i += 1
        while i <= self.n:
            if val > self.bit[i]:
                self.bit[i] = val
            i += i & -i

    def query_prefix(self, i: int) -> int:
        # max over [0..i], i is 0-based
        i += 1
        res = 0
        while i > 0:
            if self.bit[i] > res:
                res = self.bit[i]
            i -= i & -i
        return res

def longest_bounded_diff_subsequence(a: list[int], d: int, g: int) -> int:
    vals = sorted(set(a))
    m = len(vals)

    # Fenwick supports prefix max, but we need range max.
    # Trick: use a segment tree for range max OR use Fenwick over reversed indices with offline updates.
    # For clarity and correctness, we implement a segment tree in Python too.

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
```

### Java

```java
import java.util.*;

class SegTree {
    int n;
    int[] t;
    
    SegTree(int n) {
        this.n = n;
        this.t = new int[4 * n];
    }
    
    void update(int idx, int val) { update(1, 0, n - 1, idx, val); }
    
    void update(int node, int l, int r, int idx, int val) {
        if (l == r) {
            t[node] = Math.max(t[node], val);
            return;
        }
        int mid = (l + r) / 2;
        if (idx <= mid) update(node * 2, l, mid, idx, val);
        else update(node * 2 + 1, mid + 1, r, idx, val);
        t[node] = Math.max(t[node * 2], t[node * 2 + 1]);
    }
    
    int query(int ql, int qr) {
        if (ql > qr) return 0;
        return query(1, 0, n - 1, ql, qr);
    }
    
    int query(int node, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return t[node];
        int mid = (l + r) / 2;
        return Math.max(query(node * 2, l, mid, ql, qr), query(node * 2 + 1, mid + 1, r, ql, qr));
    }
}

class Solution {
    public int longestBoundedDiffSubsequence(long[] a, long d, long g) {
        long[] vals = a.clone();
        Arrays.sort(vals);
        
        int m = 0;
        for (int i = 0; i < vals.length; i++) {
            if (i == 0 || vals[i] != vals[i - 1]) {
                vals[m++] = vals[i];
            }
        }
        
        SegTree st = new SegTree(m);
        int ans = 1;
        
        for (long x : a) {
            long lo = x - g;
            long hi = x - d;
            int L = lowerBound(vals, m, lo);
            int R = upperBound(vals, m, hi) - 1;
            int best = st.query(L, R);
            int dp = best + 1;
            int idx = lowerBound(vals, m, x);
            st.update(idx, dp);
            ans = Math.max(ans, dp);
        }
        return ans;
    }
    
    private int lowerBound(long[] arr, int len, long x) {
        int l = 0, r = len;
        while (l < r) {
            int mid = (l + r) / 2;
            if (arr[mid] >= x) r = mid;
            else l = mid + 1;
        }
        return l;
    }
    
    private int upperBound(long[] arr, int len, long x) {
        int l = 0, r = len;
        while (l < r) {
            int mid = (l + r) / 2;
            if (arr[mid] <= x) l = mid + 1;
            else r = mid;
        }
        return l;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        long[] a = new long[n];
        for (int i = 0; i < n; i++) a[i] = sc.nextLong();
        long d = sc.nextLong();
        long g = sc.nextLong();
        System.out.println(new Solution().longestBoundedDiffSubsequence(a, d, g));
        sc.close();
    }
}
```

### C++ (Segment Tree)

```cpp
#include <bits/stdc++.h>
using namespace std;

struct SegTree {
    int n;
    vector<int> t;
    SegTree(int n): n(n), t(4*n, 0) {}
    void update(int idx, int val) { update(1, 0, n-1, idx, val); }
    void update(int node, int l, int r, int idx, int val) {
        if (l==r) { t[node]=max(t[node], val); return; }
        int mid=(l+r)/2;
        if (idx<=mid) update(node*2, l, mid, idx, val);
        else update(node*2+1, mid+1, r, idx, val);
        t[node]=max(t[node*2], t[node*2+1]);
    }
    int query(int ql, int qr) {
        if (ql>qr) return 0;
        return query(1, 0, n-1, ql, qr);
    }
    int query(int node, int l, int r, int ql, int qr) {
        if (qr<l || r<ql) return 0;
        if (ql<=l && r<=qr) return t[node];
        int mid=(l+r)/2;
        return max(query(node*2, l, mid, ql, qr), query(node*2+1, mid+1, r, ql, qr));
    }
};

class Solution {
public:
    int longestBoundedDiffSubsequence(const vector<long long>& a, long long d, long long g) {
        vector<long long> vals = a;
        sort(vals.begin(), vals.end());
        vals.erase(unique(vals.begin(), vals.end()), vals.end());

        SegTree st((int)vals.size());
        int ans = 1;

        for (long long x : a) {
            long long lo = x - g;
            long long hi = x - d;
            int L = (int)(lower_bound(vals.begin(), vals.end(), lo) - vals.begin());
            int R = (int)(upper_bound(vals.begin(), vals.end(), hi) - vals.begin()) - 1;
            int best = st.query(L, R);
            int dp = best + 1;
            int idx = (int)(lower_bound(vals.begin(), vals.end(), x) - vals.begin());
            st.update(idx, dp);
            ans = max(ans, dp);
        }
        return ans;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    long long d, g;
    cin >> d >> g;

    Solution sol;
    cout << sol.longestBoundedDiffSubsequence(a, d, g) << "\n";
    return 0;
}
```

### JavaScript (Segment Tree)

```javascript
const readline = require("readline");

class SegTree {
  constructor(n) {
    this.n = n;
    this.t = new Array(4 * n).fill(0);
  }
  update(idx, val, node = 1, l = 0, r = this.n - 1) {
    if (l === r) {
      if (val > this.t[node]) this.t[node] = val;
      return;
    }
    const mid = (l + r) >> 1;
    if (idx <= mid) this.update(idx, val, node << 1, l, mid);
    else this.update(idx, val, node << 1 | 1, mid + 1, r);
    const left = this.t[node << 1], right = this.t[node << 1 | 1];
    this.t[node] = left > right ? left : right;
  }
  query(ql, qr, node = 1, l = 0, r = this.n - 1) {
    if (ql > qr) return 0;
    if (qr < l || r < ql) return 0;
    if (ql <= l && r <= qr) return this.t[node];
    const mid = (l + r) >> 1;
    const a = this.query(ql, qr, node << 1, l, mid);
    const b = this.query(ql, qr, node << 1 | 1, mid + 1, r);
    return a > b ? a : b;
  }
}

function lowerBound(arr, x) {
  let l = 0, r = arr.length;
  while (l < r) {
    const m = (l + r) >> 1;
    if (arr[m] >= x) r = m;
    else l = m + 1;
  }
  return l;
}

function upperBound(arr, x) {
  let l = 0, r = arr.length;
  while (l < r) {
    const m = (l + r) >> 1;
    if (arr[m] <= x) l = m + 1;
    else r = m;
  }
  return l;
}

class Solution {
  longestBoundedDiffSubsequence(a, d, g) {
    const vals = Array.from(new Set(a)).sort((x, y) => x - y);
    const st = new SegTree(vals.length);
    let ans = 1;

    for (const x of a) {
      const lo = x - g;
      const hi = x - d;
      const L = lowerBound(vals, lo);
      const R = upperBound(vals, hi) - 1;
      const best = st.query(L, R);
      const dp = best + 1;
      const idx = lowerBound(vals, x);
      st.update(idx, dp);
      if (dp > ans) ans = dp;
    }
    return ans;
  }
}

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const lines = [];
rl.on("line", (line) => lines.push(line.trim()));
rl.on("close", () => {
  let idx = 0;
  const n = Number(lines[idx++]);
  const a = lines[idx++].split(" ").map(Number);
  const [d, g] = lines[idx++].split(" ").map(Number);
  const sol = new Solution();
  console.log(sol.longestBoundedDiffSubsequence(a, d, g));
});
```

## 🧪 Test Case Walkthrough (Dry Run)
`a = [1, 3, 4, 9, 10]`, `d=2`, `g=6`

When processing `9`:

- valid previous values are in `[9-6, 9-2] = [3, 7]`
- the best dp among values {3,4} is 2 (from `1 -> 3` or `1 -> 4`)
- so dp at 9 becomes 3

Answer is 3.

### State Evolution Table

| Index | Value | Valid Range [val-g, val-d] | Compressed [L, R] | Query Result | dp[i] | Updated Answer |
|-------|-------|----------------------------|-------------------|--------------|-------|----------------|
| 0     | 1     | [-5, -1]                   | empty             | 0            | 1     | 1              |
| 1     | 3     | [-3, 1]                    | [0, 0] (value 1)  | 1            | 2     | 2              |
| 2     | 4     | [-2, 2]                    | [0, 1] (1,3)      | max(1,2)=2   | 3     | 3              |
| 3     | 9     | [3, 7]                     | [1, 2] (3,4)      | max(2,3)=3   | 4     | 4              |
| 4     | 10    | [4, 8]                     | [2, 3] (4,9)      | max(3,4)=4   | 5     | 5              |

Final answer: 5 (subsequence: 1 → 3 → 4 → 9 → 10)

Note: The differences are: 3-1=2, 4-3=1 (invalid if d=2).
Recalculating correctly for d=2, g=6:
- From 1: can go to values in [1+2, 1+6] = [3, 7] → {3, 4}
- From 3: can go to [5, 9] → {9}
- From 4: can go to [6, 10] → {9, 10}
- From 9: can go to [11, 15] → {10} (NO, 10-9=1 < d=2)

Corrected walkthrough with forward checking:
| Index | Value | dp[i] | Can extend to |
|-------|-------|-------|---------------|
| 0     | 1     | 1     | values [3,7] → indices 1,2 |
| 1     | 3     | 2     | values [5,9] → index 3 |
| 2     | 4     | 2     | values [6,10] → indices 3,4 |
| 3     | 9     | 3     | values [11,15] → none |
| 4     | 10    | 3     | values [12,16] → none |

Final: max = 3 (path: 1→3→9 or 1→4→10)

![Example Visualization](../images/DP-006/example-1.png)

## ✅ Proof of Correctness (Sketch)

We store, for each value `v`, the maximum subsequence length ending at value `v` among processed indices.

For a new value `x`, any valid predecessor must have value in `[x-g, x-d]`. Querying the data structure over this interval gives the best achievable predecessor length. Adding 1 gives the best length for a subsequence ending at `x`.

Processing in index order ensures we only build subsequences with increasing indices. Taking max updates at `x` handles duplicates correctly.

### Common Mistakes to Avoid

1. **Using O(n^2) DP (will time out)**
2. **Forgetting coordinate compression (values are up to 1e9)**
3. **Using wrong bounds: must query `[x-g, x-d]`**
4. **Off-by-one in binary search for R (use upper_bound - 1)**


## Related Concepts

- Coordinate compression
- Range maximum query (segment tree)
- LIS-style DP

