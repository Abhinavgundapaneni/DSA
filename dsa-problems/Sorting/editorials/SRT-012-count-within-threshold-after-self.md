---
title: Count Within Threshold After Self
slug: count-within-threshold-after-self
difficulty: Medium
difficulty_score: 56
tags:
- Merge Sort
- Counting
- Divide and Conquer
problem_id: SRT_COUNT_WITHIN_THRESHOLD_AFTER_SELF__7028
display_id: SRT-012
topics:
- Sorting
- Divide and Conquer
- Counting
---
# Count Within Threshold After Self - Editorial

## Problem Summary

For each element `a[i]` in an array, count how many elements `a[j]` to its right (where `j > i`) satisfy the condition `a[i] - a[j] <= T`. This is equivalent to finding the number of `j > i` such that `a[j] >= a[i] - T`.

## Real-World Scenario

Imagine you are a **Real Estate Analyst**.
-   You have a list of house prices sold over time (chronological order).
-   For each house sale, you want to know: "How many future sales were priced at least `X` dollars?" where `X` is slightly less than the current house price (specifically `Price - T`).
-   This helps understand if the market sustained a certain price level after a specific sale.
-   Since the dataset is huge, you need an efficient way to count this for every single transaction.

## Problem Exploration

### 1. Naive Approach
-   For each `i`, iterate `j` from `i+1` to `n-1`.
-   Check if `a[j] >= a[i] - T`.
-   Complexity: `O(N^2)`. Too slow for `N=200,000`.

### 2. Divide and Conquer (Merge Sort)
-   This problem is very similar to "Count of Smaller Numbers After Self" (inversions).
-   We can use Merge Sort to solve it.
-   In the merge step, we have two sorted subarrays: `Left` and `Right`.
-   Indices in `Left` are smaller than indices in `Right` (in the original array).
-   For each element `L[p]` in `Left`, we want to count elements `R[q]` in `Right` such that `R[q] >= L[p] - T`.
-   Since both `Left` and `Right` are sorted, we can use a two-pointer approach or binary search.
-   **Two Pointers**:
    -   Iterate `p` through `Left`.
    -   Find the first index `q` in `Right` such that `Right[q] >= Left[p] - T`.
    -   Since `Right` is sorted, all elements from `q` to end satisfy the condition.
    -   Count is `len(Right) - q`.
    -   Does `q` move monotonically?
    -   As `L[p]` increases, `L[p] - T` increases.
    -   So the required threshold for `Right` elements increases.
    -   This means `q` (the first valid index) will move to the right (increase).
    -   Yes, monotonicity holds. We can maintain `q`.
-   After counting, we perform the standard merge to sort the combined array for the next level of recursion.

### 3. Coordinate Compression + BIT
-   Alternative: Iterate `i` from `n-1` down to `0`.
-   For `a[i]`, we want to query the number of already processed elements (which are to the right) that are `>= a[i] - T`.
-   This is a range sum query on values `[a[i] - T, infinity]`.
-   Since values are large (`10^9`), we need coordinate compression or a dynamic segment tree.
-   However, `a[i] - T` might not be present in the array, so simple rank compression of `a` isn't enough. We need to compress `a` values AND `a - T` values? Or use `lower_bound` on compressed values.
-   Merge Sort is often cleaner as it avoids coordinate compression details.

### 4. Algorithm Details (Merge Sort)
-   Store pairs `(value, original_index)` to update the answer array correctly.
-   `mergeSort(arr)`:
    -   Split into `left` and `right`.
    -   Recursively call.
    -   **Count Step**:
        -   `p = 0`, `q = 0`.
        -   For each element in `left`:
            -   While `q < right.length` and `right[q].val < left[p].val - T`: `q++`.
            -   `count[left[p].index] += right.length - q`.
            -   `p++`.
    -   **Merge Step**: Standard merge of sorted arrays.

## Approaches

### Approach 1: Modified Merge Sort
-   Use Merge Sort to sort the array while counting.
-   During the merge phase, before actually merging, perform a linear scan with two pointers to count valid pairs.
-   Complexity: `O(N log N)`.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    private long[] counts;
    
    private class Pair {
        int val;
        int idx;
        Pair(int val, int idx) {
            this.val = val;
            this.idx = idx;
        }
    }
    
    public long[] countWithinThreshold(int[] arr, long T) {
        int n = arr.length;
        counts = new long[n];
        Pair[] pairs = new Pair[n];
        for (int i = 0; i < n; i++) {
            pairs[i] = new Pair(arr[i], i);
        }
        
        mergeSort(pairs, T);
        return counts;
    }
    
    private Pair[] mergeSort(Pair[] arr, long T) {
        int n = arr.length;
        if (n <= 1) return arr;
        
        int mid = n / 2;
        Pair[] left = mergeSort(Arrays.copyOfRange(arr, 0, mid), T);
        Pair[] right = mergeSort(Arrays.copyOfRange(arr, mid, n), T);
        
        // Count step
        int q = 0;
        for (int p = 0; p < left.length; p++) {
            // We want count of right[q] >= left[p].val - T
            // Since right is sorted ascending, we skip elements < left[p].val - T
            long threshold = (long)left[p].val - T;
            while (q < right.length && right[q].val < threshold) {
                q++;
            }
            counts[left[p].idx] += (right.length - q);
        }
        
        // Merge step
        return merge(left, right);
    }
    
    private Pair[] merge(Pair[] left, Pair[] right) {
        Pair[] res = new Pair[left.length + right.length];
        int i = 0, j = 0, k = 0;
        while (i < left.length && j < right.length) {
            if (left[i].val <= right[j].val) {
                res[k++] = left[i++];
            } else {
                res[k++] = right[j++];
            }
        }
        while (i < left.length) res[k++] = left[i++];
        while (j < right.length) res[k++] = right[j++];
        return res;
    }
}
```

### Python

```python
def count_within_threshold(arr: list[int], T: int) -> list[int]:
    n = len(arr)
    counts = [0] * n
    pairs = [(arr[i], i) for i in range(n)]
    
    def merge_sort(sub_arr):
        if len(sub_arr) <= 1:
            return sub_arr
            
        mid = len(sub_arr) // 2
        left = merge_sort(sub_arr[:mid])
        right = merge_sort(sub_arr[mid:])
        
        # Count step
        q = 0
        for p in range(len(left)):
            threshold = left[p][0] - T
            while q < len(right) and right[q][0] < threshold:
                q += 1
            counts[left[p][1]] += (len(right) - q)
            
        # Merge step
        res = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i][0] <= right[j][0]:
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                j += 1
        res.extend(left[i:])
        res.extend(right[j:])
        return res
        
    merge_sort(pairs)
    return counts

def main():
    n, t = map(int, input().split())
    arr = list(map(int, input().split()))
    result = count_within_threshold(arr, t)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
    struct Pair {
        int val;
        int idx;
    };
    
    vector<long long> counts;
    
    vector<Pair> mergeSort(vector<Pair>& arr, long long T) {
        int n = arr.size();
        if (n <= 1) return arr;
        
        int mid = n / 2;
        vector<Pair> left(arr.begin(), arr.begin() + mid);
        vector<Pair> right(arr.begin() + mid, arr.end());
        
        left = mergeSort(left, T);
        right = mergeSort(right, T);
        
        // Count step
        int q = 0;
        for (int p = 0; p < left.size(); p++) {
            long long threshold = (long long)left[p].val - T;
            while (q < right.size() && right[q].val < threshold) {
                q++;
            }
            counts[left[p].idx] += (right.size() - q);
        }
        
        // Merge step
        vector<Pair> res;
        res.reserve(n);
        int i = 0, j = 0;
        while (i < left.size() && j < right.size()) {
            if (left[i].val <= right[j].val) {
                res.push_back(left[i++]);
            } else {
                res.push_back(right[j++]);
            }
        }
        while (i < left.size()) res.push_back(left[i++]);
        while (j < right.size()) res.push_back(right[j++]);
        return res;
    }

public:
    vector<long long> countWithinThreshold(const vector<int>& arr, long long T) {
        int n = arr.size();
        counts.assign(n, 0);
        vector<Pair> pairs(n);
        for (int i = 0; i < n; i++) {
            pairs[i] = {arr[i], i};
        }
        
        mergeSort(pairs, T);
        return counts;
    }
};
```

### JavaScript

```javascript
class Solution {
  countWithinThreshold(arr, T) {
    const n = arr.length;
    const counts = new Array(n).fill(0); // Use regular array, counts can be large but fit in double precision usually
    // Or use BigInt if n is very large, but max count is N, fits in number.
    
    const pairs = arr.map((val, idx) => ({ val, idx }));
    
    const mergeSort = (subArr) => {
      if (subArr.length <= 1) return subArr;
      
      const mid = Math.floor(subArr.length / 2);
      const left = mergeSort(subArr.slice(0, mid));
      const right = mergeSort(subArr.slice(mid));
      
      // Count step
      let q = 0;
      for (let p = 0; p < left.length; p++) {
        const threshold = left[p].val - T;
        while (q < right.length && right[q].val < threshold) {
          q++;
        }
        counts[left[p].idx] += (right.length - q);
      }
      
      // Merge step
      const res = [];
      let i = 0, j = 0;
      while (i < left.length && j < right.length) {
        if (left[i].val <= right[j].val) {
          res.push(left[i++]);
        } else {
          res.push(right[j++]);
        }
      }
      while (i < left.length) res.push(left[i++]);
      while (j < right.length) res.push(right[j++]);
      return res;
    };
    
    mergeSort(pairs);
    return counts;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
`3 1`
`4 1 3`

1.  **Split**: `[4]`, `[1, 3]`.
2.  **Process Right**: `[1]`, `[3]`.
    -   Count: `1` vs `3`. `1 - 1 = 0`. `3 >= 0`. Count for `1` += 1.
    -   Merge: `[1, 3]`.
3.  **Process Root**: `Left=[(4,0)]`, `Right=[(1,1), (3,2)]`.
    -   `p=0 (4)`. Threshold `4 - 1 = 3`.
    -   Check `Right`:
        -   `q=0`. `1 < 3`. `q++`.
        -   `q=1`. `3 < 3`? No. `3 >= 3`. Stop.
    -   Count for `4` += `2 - 1 = 1`. (Element is 3).
4.  **Counts**:
    -   Index 0 (4): 1.
    -   Index 1 (1): 1.
    -   Index 2 (3): 0.
5.  **Result**: `1 1 0`.

## Proof of Correctness

-   **Divide and Conquer**: The problem is decomposed into counting pairs `(i, j)` where `i` is in the left half and `j` is in the right half. Pairs entirely within left or right are handled recursively.
-   **Sorting**: Sorting allows efficient counting in `O(N)` per merge step.
-   **Condition**: `a[j] >= a[i] - T` is correctly checked using the sorted property.

## Interview Extensions

1.  **Reverse Condition?**
    -   `a[i] > a[j] + T`. Similar logic, just different threshold.
2.  **Updates?**
    -   Dynamic updates require a Segment Tree or Fenwick Tree (possibly with coordinate compression).

### Common Mistakes

-   **Sorting**: Losing original indices. Must store pairs.
-   **Threshold Logic**: `a[j] >= a[i] - T` vs `a[j] <= a[i] - T`. Be careful with inequalities.
-   **Integer Overflow**: `a[i] - T` can underflow `int`. Use `long`.
