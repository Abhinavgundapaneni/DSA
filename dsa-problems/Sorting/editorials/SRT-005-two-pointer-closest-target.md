---
title: Two-Pointer Sum Closest to Target
slug: two-pointer-closest-target
difficulty: Easy
difficulty_score: 28
tags:
- Sorting
- Two Pointers
- Searching
problem_id: SRT_TWO_POINTER_CLOSEST_TARGET__2651
display_id: SRT-005
topics:
- Sorting
- Two Pointers
- Searching
---
# Two-Pointer Sum Closest to Target - Editorial

## Problem Summary

You are given a sorted array of integers `a` and a target integer `target`. You need to find a pair of elements `(a[i], a[j])` with `i != j` such that their sum `a[i] + a[j]` is as close to `target` as possible. If there are multiple pairs with the same minimum difference, return the one with the smaller first value `a[i]`.

## Real-World Scenario

Imagine you are a **Chemist** mixing a solution.
-   You have a shelf of chemical vials sorted by their pH level.
-   You need to mix two chemicals to achieve a target pH level of exactly `target`.
-   If you can't get exactly `target`, you want to get as close as possible to minimize the reaction error.
-   Since the vials are already sorted, you can efficiently find the best pair without testing every combination.

## Problem Exploration

### 1. Two-Pointer Technique
-   Since the array is sorted, we can use the **Two-Pointer** approach.
-   Initialize `left = 0` and `right = n - 1`.
-   Calculate `sum = a[left] + a[right]`.
-   If `sum == target`: We found an exact match. Since we want the smallest first value, and `left` starts at 0, this is likely the best candidate (or one of them). We can return immediately or continue to check if there are other pairs (though usually exact match is best).
-   If `sum < target`: We need a larger sum. Increment `left`.
-   If `sum > target`: We need a smaller sum. Decrement `right`.
-   In each step, update the "best pair" if the current `abs(sum - target)` is smaller than the best seen so far.

### 2. Handling Ties
-   The problem states: "return the pair with the smaller first value".
-   Our two-pointer approach starts with the smallest possible `left` and largest possible `right`.
-   As we iterate, `left` only increases.
-   So, the first time we find a pair with a specific difference `D`, it will have the smallest `left` among all pairs with difference `D` found *in that specific traversal logic*.
-   However, is it guaranteed?
    -   Suppose `target = 10`. Pairs `(2, 8)` and `(3, 7)`. Both sum to 10.
    -   If we start at `(1, 9)` (sum 10), we pick it.
    -   If we have `[2, 3, 7, 8]`. `L=0(2), R=3(8)`. Sum=10. Diff=0. Best=`(2, 8)`.
    -   If we continue, `sum == target`, what do we do?
    -   Usually, we stop or move pointers. If we move `left++` and `right--`, we might find `(3, 7)`.
    -   Since we want the *smaller first value*, `(2, 8)` is better than `(3, 7)`.
    -   So, if we find a new pair with the *same* difference, we should **not** update if the new `left` is larger.
    -   Since `left` increases monotonically, we simply update only if `new_diff < best_diff`. If `new_diff == best_diff`, we keep the old one (which had smaller `left`).

### 3. Edge Cases
-   `n=2`: Only one pair.
-   Array contains duplicates: Handled naturally by indices.
-   Large values: Sum can exceed 32-bit integer range? Constraints say `a[i], target <= 10^9`. Sum can be `2 * 10^9`, which fits in signed 32-bit integer (max `2.14 * 10^9`). But `abs(sum - target)` is safe. In languages like C++, `long long` is safer for sum to avoid overflow if constraints were slightly higher.

## Approaches

### Approach 1: Two Pointers
-   Initialize `L=0`, `R=n-1`.
-   Track `bestDiff = infinity`, `bestPair = {-1, -1}`.
-   Loop while `L < R`.
-   Update best if current pair is closer.
-   Move pointers based on comparison with `target`.
-   Complexity: `O(N)`.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public int[] closestPair(int[] arr, int target) {
        int n = arr.length;
        int left = 0;
        int right = n - 1;
        
        long minDiff = Long.MAX_VALUE;
        int resLeft = -1;
        int resRight = -1;
        
        while (left < right) {
            long sum = (long) arr[left] + arr[right];
            long diff = Math.abs(sum - target);
            
            if (diff < minDiff) {
                minDiff = diff;
                resLeft = arr[left];
                resRight = arr[right];
            }
            // If diff is equal, we prefer smaller arr[left], which we already have
            // since left increases. So no update needed.
            
            if (sum < target) {
                left++;
            } else {
                right--;
            }
        }
        
        return new int[]{resLeft, resRight};
    }
}
```

### Python

```python
def closest_pair(arr: list[int], target: int) -> list[int]:
    n = len(arr)
    left = 0
    right = n - 1
    
    min_diff = float('inf')
    res_pair = []
    
    while left < right:
        current_sum = arr[left] + arr[right]
        diff = abs(current_sum - target)
        
        if diff < min_diff:
            min_diff = diff
            res_pair = [arr[left], arr[right]]
        
        if current_sum < target:
            left += 1
        else:
            right -= 1
            
    return res_pair

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    target = int(input())
    result = closest_pair(arr, target)
    print(result[0], result[1])

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <cmath>
#include <climits>
#include <cstdlib>

using namespace std;

class Solution {
public:
    vector<int> closestPair(const vector<int>& arr, int target) {
        int n = arr.size();
        int left = 0;
        int right = n - 1;
        
        long long minDiff = LLONG_MAX;
        int resLeft = -1;
        int resRight = -1;
        
        while (left < right) {
            long long sum = (long long)arr[left] + arr[right];
            long long diff = abs(sum - target);
            
            if (diff < minDiff) {
                minDiff = diff;
                resLeft = arr[left];
                resRight = arr[right];
            }
            
            if (sum < target) {
                left++;
            } else {
                right--;
            }
        }
        
        return {resLeft, resRight};
    }
};
```

### JavaScript

```javascript
class Solution {
  closestPair(arr, target) {
    let n = arr.length;
    let left = 0;
    let right = n - 1;
    
    let minDiff = Infinity;
    let resLeft = -1;
    let resRight = -1;
    
    while (left < right) {
      const sum = arr[left] + arr[right];
      const diff = Math.abs(sum - target);
      
      if (diff < minDiff) {
        minDiff = diff;
        resLeft = arr[left];
        resRight = arr[right];
      }
      
      if (sum < target) {
        left++;
      } else {
        right--;
      }
    }
    
    return [resLeft, resRight];
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
`4`
`1 4 6 8`
`10`

1.  **Init**: `L=0 (1)`, `R=3 (8)`. `Sum=9`. `Diff=1`. `Best=(1, 8)`.
2.  `Sum < 10`, so `L++`.
3.  **Step 2**: `L=1 (4)`, `R=3 (8)`. `Sum=12`. `Diff=2`. `2 > 1`, no update.
4.  `Sum > 10`, so `R--`.
5.  **Step 3**: `L=1 (4)`, `R=2 (6)`. `Sum=10`. `Diff=0`. `0 < 1`. `Best=(4, 6)`.
6.  `Sum == 10`. Logic says `R--` (since `else` branch).
7.  **Step 4**: `L=1`, `R=1`. Loop ends.
8.  **Result**: `4 6`.

## Proof of Correctness

-   **Monotonicity**: Since the array is sorted, if `a[L] + a[R] < target`, then for any `k < R`, `a[L] + a[k] < target` (even smaller). So we can safely discard `a[L]` as a candidate for the *current* `R` or any smaller `R` to reach `target`. We must increase sum, so `L++`.
-   Similarly, if `sum > target`, we must decrease sum, so `R--`.
-   This linear scan visits all "potential" best pairs.

## Interview Extensions

1.  **3Sum Closest?**
    -   Fix one element `a[i]`, then use 2-pointer on the rest. Complexity `O(N^2)`.
2.  **K Closest Pairs?**
    -   Use a Min-Heap to track candidates.

### Common Mistakes

-   **Overflow**: `a[i] + a[j]` can exceed integer limits. Use `long` or `long long`.
-   **Tie-breaking**: Ensure you don't overwrite a pair with equal difference if the new pair has a larger first element (which happens naturally if you only update on strict `<`).
