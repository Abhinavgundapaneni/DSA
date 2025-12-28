---
title: Closest Pair in Sorted Circular Array
slug: closest-pair-sorted-circular
difficulty: Medium
difficulty_score: 49
tags:
- Two Pointers
- Circular Arrays
- Searching
problem_id: SRT_CLOSEST_PAIR_SORTED_CIRCULAR__3817
display_id: SRT-013
topics:
- Sorting
- Two Pointers
- Circular Arrays
---
# Closest Pair in Sorted Circular Array - Editorial

## Problem Summary

You are given a sorted array that has been rotated at some pivot. You need to find a pair of elements `(a[i], a[j])` such that their sum is closest to a given `target`.

## Real-World Scenario

Imagine you are a **Jeweler** making a custom ring.
-   You have a collection of gemstones arranged in a circle by size (carat weight).
-   The arrangement was originally sorted, but the display case was rotated, so the smallest stone is somewhere in the middle, followed by larger ones, wrapping around to the start.
-   A customer wants a ring with two stones whose total weight is exactly `target` carats (or as close as possible).
-   You want to find the best pair without checking every possible combination.

## Problem Exploration

### 1. Structure of Rotated Sorted Array
-   A sorted array `[1, 2, 3, 4, 5]` rotated might look like `[4, 5, 1, 2, 3]`.
-   The smallest element (pivot) is `1` at index 2.
-   The largest element is `5` at index 1 (pivot - 1).
-   The array is effectively sorted if we start reading from the pivot index and wrap around modulo `n`.

### 2. Two-Pointer Approach
-   In a standard sorted array, we find a pair with sum closest to `target` using `L=0`, `R=n-1`.
    -   If `sum < target`, `L++`.
    -   If `sum > target`, `R--`.
-   In a rotated array, the "logical" start (smallest) is at `pivot`, and the "logical" end (largest) is at `pivot - 1`.
-   Let `L = pivot` and `R = (pivot - 1 + n) % n`.
-   We calculate `sum = a[L] + a[R]`.
-   Update best pair if `abs(sum - target)` is minimal.
-   If `sum < target`: We need a larger sum. Move `L` to the "next larger" element. `L = (L + 1) % n`.
-   If `sum > target`: We need a smaller sum. Move `R` to the "next smaller" element. `R = (R - 1 + n) % n`.
-   **Termination**:
    -   In a linear array, we stop when `L > R`.
    -   In a circular array, `L` and `R` are indices modulo `n`.
    -   We stop when `L` and `R` cross or meet.
    -   Specifically, since `L` moves "forward" and `R` moves "backward" (logically), we stop when `L` effectively passes `R`.
    -   Or simply: count iterations? No, `L` and `R` might move unevenly.
    -   Condition: `L != R`. But what if they cross?
    -   Since we start with `L` at min and `R` at max, they cover the full range.
    -   If `L` increments and becomes `R` (or `R` decrements and becomes `L`), we have checked the full range.
    -   Since `L` starts at min and `R` at max, `L` is "left" and `R` is "right".
    -   We stop when `L` crosses `R`.
    -   We stop when `L` effectively passes `R`.
    -   Let's just track the number of elements in the range `[L, R]`. Initially `n`.
    -   Here, we can just map logical indices `0` to `n-1` to physical indices `(pivot + i) % n`.
    -   Let `l = 0`, `r = n - 1`.
    -   Physical `pL = (pivot + l) % n`, `pR = (pivot + r) % n`.
    -   While `l < r`:
        -   `sum = a[pL] + a[pR]`.
        -   Update best.
        -   If `sum < target`: `l++`.
        -   Else: `r--`.
    -   This completely abstracts away the rotation!

### 3. Finding the Pivot
-   We can find the pivot (index of minimum element) in `O(log n)` using binary search, or `O(n)` linearly.
-   Since the 2-pointer scan is `O(n)`, finding the pivot in `O(n)` is acceptable.
-   Pivot is the index `i` such that `a[i] < a[i-1]` (with wrap around). Or simply the index of the minimum element.

## Approaches

### Approach 1: Find Pivot + Logical Two Pointers
-   Find index of minimum element `pivot`.
-   Use logical pointers `l=0`, `r=n-1`.
-   Map to physical indices: `real(i) = (pivot + i) % n`.
-   Standard 2-pointer logic.
-   Complexity: `O(N)`.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public int[] closestPairCircular(int[] arr, int target) {
        int n = arr.length;
        if (n == 0) return new int[]{};
        
        // Find pivot (index of minimum element)
        int pivot = 0;
        for (int i = 1; i < n; i++) {
            if (arr[i] < arr[pivot]) {
                pivot = i;
            }
        }
        
        int l = 0;
        int r = n - 1;
        
        long minDiff = Long.MAX_VALUE;
        int res1 = -1, res2 = -1;
        
        while (l < r) {
            int pL = (pivot + l) % n;
            int pR = (pivot + r) % n;
            
            long sum = (long)arr[pL] + arr[pR];
            long diff = Math.abs(sum - target);
            
            if (diff < minDiff) {
                minDiff = diff;
                res1 = arr[pL];
                res2 = arr[pR];
            }
            
            if (sum < target) {
                l++;
            } else {
                r--;
            }
        }
        
        return new int[]{res1, res2};
    }
}
```

### Python

```python
def closest_pair_circular(arr: list[int], target: int) -> list[int]:
    n = len(arr)
    if n == 0:
        return []
        
    # Find pivot
    pivot = 0
    for i in range(1, n):
        if arr[i] < arr[pivot]:
            pivot = i
            
    l, r = 0, n - 1
    min_diff = float('inf')
    res = []
    
    while l < r:
        pL = (pivot + l) % n
        pR = (pivot + r) % n
        
        curr_sum = arr[pL] + arr[pR]
        diff = abs(curr_sum - target)
        
        if diff < min_diff:
            min_diff = diff
            res = [arr[pL], arr[pR]]
            
        if curr_sum < target:
            l += 1
        else:
            r -= 1
            
    return res

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    target = int(input())
    result = closest_pair_circular(arr, target)
    print(result[0], result[1])

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <cmath>
#include <climits>
#include <algorithm>

using namespace std;

class Solution {
public:
    vector<int> closestPairCircular(const vector<int>& arr, int target) {
        int n = arr.size();
        if (n == 0) return {};
        
        int pivot = 0;
        for (int i = 1; i < n; i++) {
            if (arr[i] < arr[pivot]) {
                pivot = i;
            }
        }
        
        int l = 0;
        int r = n - 1;
        long long minDiff = LLONG_MAX;
        int res1 = -1, res2 = -1;
        
        while (l < r) {
            int pL = (pivot + l) % n;
            int pR = (pivot + r) % n;
            
            long long sum = (long long)arr[pL] + arr[pR];
            long long diff = abs(sum - target);
            
            if (diff < minDiff) {
                minDiff = diff;
                res1 = arr[pL];
                res2 = arr[pR];
            }
            
            if (sum < target) {
                l++;
            } else {
                r--;
            }
        }
        
        return {res1, res2};
    }
};
```

### JavaScript

```javascript
class Solution {
  closestPairCircular(arr, target) {
    const n = arr.length;
    if (n === 0) return [];
    
    let pivot = 0;
    for (let i = 1; i < n; i++) {
      if (arr[i] < arr[pivot]) {
        pivot = i;
      }
    }
    
    let l = 0;
    let r = n - 1;
    let minDiff = Infinity;
    let res = [];
    
    while (l < r) {
      const pL = (pivot + l) % n;
      const pR = (pivot + r) % n;
      
      const sum = arr[pL] + arr[pR];
      const diff = Math.abs(sum - target);
      
      if (diff < minDiff) {
        minDiff = diff;
        res = [arr[pL], arr[pR]];
      }
      
      if (sum < target) {
        l++;
      } else {
        r--;
      }
    }
    
    return res;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input:**
`5`
`4 5 1 2 3`
`7`

1.  **Pivot**: `1` is at index 2. `pivot = 2`.
2.  **Logical Map**:
    -   `l=0` -> `idx=(2+0)%5 = 2` (val 1).
    -   `r=4` -> `idx=(2+4)%5 = 1` (val 5).
3.  **Step 1**:
    -   `sum = 1 + 5 = 6`. `diff = |6-7| = 1`. `Best = (1, 5)`.
    -   `6 < 7`. `l++`.
4.  **Step 2**:
    -   `l=1` -> `idx=(2+1)%5 = 3` (val 2).
    -   `r=4` -> `idx=1` (val 5).
    -   `sum = 2 + 5 = 7`. `diff = 0`. `Best = (2, 5)`.
    -   `7 == 7`. `r--`.
5.  **Step 3**:
    -   `l=1` -> `idx=3` (val 2).
    -   `r=3` -> `idx=(2+3)%5 = 0` (val 4).
    -   `sum = 2 + 4 = 6`. `diff = 1`. No update.
    -   `6 < 7`. `l++`.
6.  **Step 4**:
    -   `l=2` -> `idx=4` (val 3).
    -   `r=3` -> `idx=0` (val 4).
    -   `sum = 3 + 4 = 7`. `diff = 0`. `Best = (3, 4)`. (Tie, update allowed).
    -   `7 == 7`. `r--`.
7.  **Loop End**: `l=2, r=2`. Stop.
8.  **Result**: `4 3` (or `3 4`).

## Proof of Correctness

-   **Mapping**: By mapping `(pivot + i) % n`, we treat the circular array as a linear sorted array.
-   **Two Pointers**: The standard two-pointer technique correctly finds the closest pair sum in a sorted array in `O(N)`.
-   **Pivot**: Finding the minimum element correctly identifies the start of the sorted sequence.

## Interview Extensions

1.  **Duplicates?**
    -   Pivot finding might take `O(N)` in worst case (e.g., `2 2 2 1 2`), but our linear scan is already `O(N)`, so it doesn't hurt complexity.
2.  **Find Pivot in O(log N)?**
    -   Yes, if no duplicates. `O(log N)` binary search.

### Common Mistakes

-   **Modulo Arithmetic**: Forgetting `% n` when accessing array.
-   **Pivot Logic**: Assuming pivot is always `arr[i] > arr[i+1]`. If array is not rotated (sorted), pivot is 0.
-   **Loop Condition**: `l < r` ensures we don't use the same element twice (unless `n=1` which loop skips).
