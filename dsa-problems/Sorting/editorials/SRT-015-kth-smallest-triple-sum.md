---
title: Kth Smallest Triple Sum
slug: kth-smallest-triple-sum
difficulty: Medium
difficulty_score: 59
tags:
- Sorting
- Binary Search
- Two Pointers
problem_id: SRT_KTH_SMALLEST_TRIPLE_SUM__7904
display_id: SRT-015
topics:
- Sorting
- Binary Search
- Two Pointers
---
# Kth Smallest Triple Sum - Editorial

## Problem Summary

Given an array of `n` integers, find the `k`-th smallest sum of a triplet `(a[i], a[j], a[k])` where `i < j < k`.

## Real-World Scenario

Imagine you are a **Logistics Manager** planning shipments.
-   You have a warehouse full of items with different weights.
-   Each shipment must consist of exactly three items.
-   Shipping costs are proportional to the total weight of the three items.
-   You want to offer a "Budget Shipping" option, which corresponds to the cheapest possible combinations.
-   Specifically, you want to find the weight of the `k`-th cheapest shipment option available to advertise "Shipping starting from X...".

## Problem Exploration

### 1. Brute Force
-   Generate all `N choose 3` triplets.
-   Sort their sums. Pick the `k`-th.
-   Complexity: `O(N^3)` to generate, `O(N^3 log(N^3))` to sort.
-   With `N=100,000`, this is impossible. Even `N=1000` is `10^9` ops.
-   The notes indicate `O(N^2 log R)` complexity.
-   For large `N`, the intended approach uses Binary Search on Answer.
    -   "Time complexity: O(n^2 log R)"
    -   The standard approach uses Binary Search on Answer.
    -   We binary search for a value `S` and count how many triples have sum `<= S`.
    -   Counting triples `<= S`:
        -   Sort `A`.
        -   Iterate `i` from `0` to `n-3`.
        -   Target for pair `(j, k)` is `S - A[i]`.
        -   Count pairs in `A[i+1...n-1]` with sum `<= Target`.
        -   This pair counting can be done in `O(N)` using two pointers.
        -   Total count complexity: `O(N^2)`.
    -   Total complexity: `O(N^2 * log(Range))`.
    -   We implement the Binary Search on Answer approach with optimizations.

### 2. Binary Search on Answer
-   Range `[3*min, 3*max]`.
-   `check(val)`: Count triples with sum `<= val`.
-   Sort `arr`.
-   For each `i`:
    -   `target = val - arr[i]`.
    -   `left = i + 1`, `right = n - 1`.
    -   While `left < right`:
        -   If `arr[left] + arr[right] <= target`:
            -   All pairs `(left, left+1...right)` are valid.
            -   Count += `right - left`.
            -   `left++`.
        -   Else: `right--`.
-   If `count >= k`, `ans = val`, `high = val - 1`.
-   Else `low = val + 1`.

### 3. Optimization
-   If `arr[i] * 3 > val`, we can stop early (since array is sorted).
-   If `arr[i] + arr[i+1] + arr[i+2] > val`, break.
-   If `arr[i] + arr[n-2] + arr[n-1] <= val`, add all combinations `(n-1-i)*(n-2-i)/2` and continue? Yes.

## Approaches

### Approach 1: Binary Search on Answer
-   Binary search for the sum value `S`.
-   Count triples `<= S` in `O(N^2)`.
-   Complexity: `O(N^2 log(Range))`.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public long kthTripleSum(int[] arr, long k) {
        int n = arr.length;
        Arrays.sort(arr);
        
        long low = (long)arr[0] + arr[1] + arr[2];
        long high = (long)arr[n-1] + arr[n-2] + arr[n-3];
        long ans = high;
        
        while (low <= high) {
            long mid = low + (high - low) / 2;
            if (countLessEqual(arr, mid) >= k) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return ans;
    }
    
    private long countLessEqual(int[] arr, long target) {
        long count = 0;
        int n = arr.length;
        for (int i = 0; i < n - 2; i++) {
            // Optimization: If smallest sum starting with arr[i] > target, break
            if ((long)arr[i] + arr[i+1] + arr[i+2] > target) break;
            
            // Optimization: If largest sum starting with arr[i] <= target, add all
            if ((long)arr[i] + arr[n-2] + arr[n-1] <= target) {
                long remaining = n - 1 - i;
                count += remaining * (remaining - 1) / 2;
                continue;
            }
            
            long rem = target - arr[i];
            int l = i + 1;
            int r = n - 1;
            while (l < r) {
                if (arr[l] + arr[r] <= rem) {
                    count += (r - l);
                    l++;
                } else {
                    r--;
                }
            }
        }
        return count;
    }
}
```

### Python

```python
def kth_triple_sum(arr: list[int], k: int) -> int:
    n = len(arr)
    arr.sort()
    
    def count_less_equal(target):
        count = 0
        for i in range(n - 2):
            # Optimizations
            if arr[i] + arr[i+1] + arr[i+2] > target:
                break
            if arr[i] + arr[n-2] + arr[n-1] <= target:
                rem_len = n - 1 - i
                count += rem_len * (rem_len - 1) // 2
                continue
                
            rem = target - arr[i]
            l, r = i + 1, n - 1
            while l < r:
                if arr[l] + arr[r] <= rem:
                    count += (r - l)
                    l += 1
                else:
                    r -= 1
        return count

    low = arr[0] + arr[1] + arr[2]
    high = arr[n-1] + arr[n-2] + arr[n-3]
    ans = high
    
    while low <= high:
        mid = (low + high) // 2
        if count_less_equal(mid) >= k:
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
            
    return ans

def main():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    result = kth_triple_sum(arr, k)
    print(result)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <algorithm>
#include <iostream>

using namespace std;

class Solution {
    long long countLessEqual(const vector<int>& arr, long long target) {
        long long count = 0;
        int n = arr.size();
        for (int i = 0; i < n - 2; i++) {
            if ((long long)arr[i] + arr[i+1] + arr[i+2] > target) break;
            
            if ((long long)arr[i] + arr[n-2] + arr[n-1] <= target) {
                long long remaining = n - 1 - i;
                count += remaining * (remaining - 1) / 2;
                continue;
            }
            
            long long rem = target - arr[i];
            int l = i + 1;
            int r = n - 1;
            while (l < r) {
                if (arr[l] + arr[r] <= rem) {
                    count += (r - l);
                    l++;
                } else {
                    r--;
                }
            }
        }
        return count;
    }

public:
    long long kthTripleSum(vector<int>& arr, long long k) {
        int n = arr.size();
        sort(arr.begin(), arr.end());
        
        long long low = (long long)arr[0] + arr[1] + arr[2];
        long long high = (long long)arr[n-1] + arr[n-2] + arr[n-3];
        long long ans = high;
        
        while (low <= high) {
            long long mid = low + (high - low) / 2;
            if (countLessEqual(arr, mid) >= k) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return ans;
    }
};
```

### JavaScript

```javascript
class Solution {
  kthTripleSum(arr, k) {
    const n = arr.length;
    // Use numeric sort
    arr.sort((a, b) => a - b);
    
    // Use BigInt for sums to avoid overflow
    const bigK = BigInt(k);
    
    const countLessEqual = (target) => {
      let count = 0n;
      for (let i = 0; i < n - 2; i++) {
        const valI = BigInt(arr[i]);
        const valI1 = BigInt(arr[i+1]);
        const valI2 = BigInt(arr[i+2]);
        
        if (valI + valI1 + valI2 > target) break;
        
        const valN2 = BigInt(arr[n-2]);
        const valN1 = BigInt(arr[n-1]);
        
        if (valI + valN2 + valN1 <= target) {
          const remaining = BigInt(n - 1 - i);
          count += remaining * (remaining - 1n) / 2n;
          continue;
        }
        
        const rem = target - valI;
        let l = i + 1;
        let r = n - 1;
        while (l < r) {
          if (BigInt(arr[l]) + BigInt(arr[r]) <= rem) {
            count += BigInt(r - l);
            l++;
          } else {
            r--;
          }
        }
      }
      return count;
    };
    
    let low = BigInt(arr[0]) + BigInt(arr[1]) + BigInt(arr[2]);
    let high = BigInt(arr[n-1]) + BigInt(arr[n-2]) + BigInt(arr[n-3]);
    let ans = high;
    
    while (low <= high) {
      const mid = (low + high) / 2n;
      if (countLessEqual(mid) >= bigK) {
        ans = mid;
        high = mid - 1n;
      } else {
        low = mid + 1n;
      }
    }
    return ans.toString();
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
`4 2`
`1 2 4 7`

1.  **Sorted**: `1, 2, 4, 7`.
2.  **Range**: `1+2+4=7` to `2+4+7=13`.
3.  **Try mid=10**:
    -   `i=0 (1)`. Target `9`.
        -   `l=1 (2), r=3 (7)`. `2+7=9 <= 9`. Count += `3-1=2`. Pairs `(2,7), (2,4)`. `l=2`.
        -   `l=2 (4), r=3 (7)`. `4+7=11 > 9`. `r=2`.
        -   Loop end. Count = 2.
    -   `i=1 (2)`. Target `8`.
        -   `l=2 (4), r=3 (7)`. `4+7=11 > 8`. `r=2`.
        -   Loop end.
    -   Total count = 2.
    -   `2 >= 2`. `ans=10`. `high=9`.
4.  **Try mid=8**:
    -   `i=0 (1)`. Target `7`.
        -   `l=1 (2), r=3 (7)`. `9 > 7`. `r=2`.
        -   `l=1 (2), r=2 (4)`. `6 <= 7`. Count += `1`. Pair `(2,4)`.
    -   Total count = 1.
    -   `1 < 2`. `low=9`.
5.  **Try mid=9**:
    -   Count will be 1 (since 10 gave 2 and next smallest is 10).
    -   Counts: `<=7`: 1. `<=8`: 1. `<=9`: 1. `<=10`: 2.
    -   So for 9, count is 1. `low=10`.
6.  **Loop End**: `low=10, high=9`.
7.  **Result**: 10.

## Proof of Correctness

-   **Monotonicity**: The number of triples with sum `<= S` increases as `S` increases.
-   **Binary Search**: Finds the smallest `S` such that count is `>= k`.
-   **Counting**: The two-pointer approach correctly counts pairs in sorted array in `O(N)`.

## Interview Extensions

1.  **4Sum?**
    -   `O(N^3 log Range)`.
2.  **Count Triples with Sum < Target?**
    -   Just the counting part of this solution. `O(N^2)`.

### Common Mistakes

-   **Overflow**: Sum of three integers can exceed `2^31 - 1`. Use `long` / `BigInt`.
-   **Loop Bounds**: `i` goes up to `n-3`. `l` starts at `i+1`.
-   **Optimization**: Forgetting to break early can lead to TLE on large inputs with small answers.
