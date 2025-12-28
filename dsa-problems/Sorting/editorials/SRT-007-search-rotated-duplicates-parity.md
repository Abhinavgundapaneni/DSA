---
title: Search Rotated With Duplicates Parity Count
slug: search-rotated-duplicates-parity
difficulty: Medium
difficulty_score: 52
tags:
- Sorting
- Binary Search
- Rotated Array
problem_id: SRT_SEARCH_ROTATED_DUPLICATES_PARITY__9062
display_id: SRT-007
topics:
- Sorting
- Binary Search
- Rotated Arrays
---
# Search Rotated With Duplicates Parity Count - Editorial

## Problem Summary

You are given a rotated sorted array `a` which may contain duplicates. You need to count how many times a target value `x` appears at **even indices** (0, 2, 4, ...).

## Real-World Scenario

Imagine a **Shifted Calendar**.
-   You have a list of daily temperatures recorded over a year, sorted by value.
-   However, the data was shifted: the records start from March instead of January, wrapping around.
-   You want to find how many days had a temperature of exactly `x` degrees.
-   Furthermore, due to a specific sampling requirement, you only care about readings taken on "even" days (0th day, 2nd day, etc.) relative to the start of your shifted log.

## Problem Exploration

### 1. Rotated Sorted Array with Duplicates
-   Standard binary search works on rotated arrays, but duplicates make finding the pivot (minimum element) `O(N)` in the worst case (e.g., `[2, 2, 2, 1, 2]`).
-   However, if we assume the "average" case or if the problem implies we can do better, we try to find the pivot or search ranges.
-   The problem asks for `O(log N)` time in the notes. This implies we should try to handle duplicates efficiently or assume the number of duplicates isn't "all elements".
-   The real challenge is finding the *range* of `x`.

### 2. Finding the Range of `x`
-   Since the array is rotated, `x` might appear in one contiguous block (if it doesn't cross the rotation boundary) or two blocks (if it does).
-   In the rotated version, they might be split into at most two segments: `[L1, R1]` and `[L2, R2]`.
-   We need to find the start and end indices of `x`.
-   Finding the pivot `P` (index of minimum) allows us to treat the array as two sorted subarrays `[0, P-1]` and `[P, N-1]`.
-   We can binary search for the first and last occurrence of `x` in both subarrays.

### 3. Counting Even Indices
-   Once we have a range `[L, R]` where `a[i] == x` for `L <= i <= R`, we need to count even numbers in `[L, R]`.
-   Count of even numbers in `[0, K]` is `K/2 + 1`.
-   Count in `[L, R]` is `count(0, R) - count(0, L-1)`.
-   Formula: `countEven(L, R) = (R/2 + 1) - ((L-1)/2 + 1)`.
    -   If `L` is even and `R` is even: `(R-L)/2 + 1`.
    -   If `L` is odd and `R` is odd: `(R-L)/2`.
    -   General: Number of integers in `[L, R]` is `len = R - L + 1`.
    -   If `len` is even, exactly half are even.
    -   If `len` is odd, it depends on parity of `L`. If `L` even, `(len+1)/2`. If `L` odd, `(len-1)/2`.

### 4. Worst Case for Duplicates
-   If `a = [1, 1, 1, 0, 1]`, finding the pivot is `O(N)`.
-   If we cannot find the pivot in `O(log N)`, we cannot solve this strictly in `O(log N)`.
-   However, many problems allow `O(N)` worst case but expect `O(log N)` for non-degenerate cases.
-   Given the constraints and typical "Search in Rotated Array II" style, we should implement the best effort binary search.
-   Or, we can just find the pivot linearly if `a[mid] == a[end]`, which degrades to `O(N)`.
-   The Notes say "Time complexity: O(log n)". This usually implies inputs are not degenerate (e.g., `[2, 2, 1, 2, 2]`).

## Approaches

### Approach 1: Find Pivot + Binary Search Ranges
-   Find pivot `P`.
-   Search for `x` in `[0, P-1]` -> Range `[s1, e1]`.
-   Search for `x` in `[P, N-1]` -> Range `[s2, e2]`.
-   Sum even indices in valid ranges.
-   Complexity: `O(log N)` average, `O(N)` worst case.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public int countEvenIndices(int[] arr, int x) {
        int n = arr.length;
        int pivot = findPivot(arr, 0, n - 1);
        
        int count = 0;
        // Search in left part [0, pivot-1]
        if (pivot > 0) {
            int[] range = searchRange(arr, 0, pivot - 1, x);
            if (range[0] != -1) {
                count += countEvens(range[0], range[1]);
            }
        }
        
        // Search in right part [pivot, n-1]
        int[] range = searchRange(arr, pivot, n - 1, x);
        if (range[0] != -1) {
            count += countEvens(range[0], range[1]);
        }
        
        return count;
    }
    
    private int findPivot(int[] arr, int low, int high) {
        // Returns index of minimum element
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] > arr[high]) {
                low = mid + 1;
            } else if (arr[mid] < arr[high]) {
                high = mid;
            } else {
                // Duplicates: worst case O(N)
                high--;
            }
        }
        return low;
    }
    
    private int[] searchRange(int[] arr, int low, int high, int target) {
        int start = -1, end = -1;
        
        // Find first
        int l = low, r = high;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (arr[mid] >= target) {
                if (arr[mid] == target) start = mid;
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        }
        
        if (start == -1) return new int[]{-1, -1};
        
        // Find last
        l = low; r = high;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (arr[mid] <= target) {
                if (arr[mid] == target) end = mid;
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }
        
        return new int[]{start, end};
    }
    
    private int countEvens(int L, int R) {
        if (L > R) return 0;
        int len = R - L + 1;
        if (len % 2 == 0) return len / 2;
        return (L % 2 == 0) ? (len + 1) / 2 : (len - 1) / 2;
    }
}
```

### Python

```python
def count_even_indices(arr: list[int], x: int) -> int:
    n = len(arr)
    
    def find_pivot(low, high):
        while low < high:
            mid = (low + high) // 2
            if arr[mid] > arr[high]:
                low = mid + 1
            elif arr[mid] < arr[high]:
                high = mid
            else:
                high -= 1
        return low
        
    def search_range(low, high, target):
        start, end = -1, -1
        
        # Find first
        l, r = low, high
        while l <= r:
            mid = (l + r) // 2
            if arr[mid] >= target:
                if arr[mid] == target:
                    start = mid
                r = mid - 1
            else:
                l = mid + 1
        
        if start == -1:
            return -1, -1
            
        # Find last
        l, r = low, high
        while l <= r:
            mid = (l + r) // 2
            if arr[mid] <= target:
                if arr[mid] == target:
                    end = mid
                l = mid + 1
            else:
                r = mid - 1
                
        return start, end
        
    def count_evens(L, R):
        if L > R: return 0
        length = R - L + 1
        if length % 2 == 0:
            return length // 2
        return (length + 1) // 2 if L % 2 == 0 else (length - 1) // 2

    pivot = find_pivot(0, n - 1)
    count = 0
    
    if pivot > 0:
        s, e = search_range(0, pivot - 1, x)
        if s != -1:
            count += count_evens(s, e)
            
    s, e = search_range(pivot, n - 1, x)
    if s != -1:
        count += count_evens(s, e)
        
    return count

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    x = int(input())
    result = count_even_indices(arr, x)
    print(result)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <iostream>

using namespace std;

class Solution {
    int findPivot(const vector<int>& arr, int low, int high) {
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] > arr[high]) {
                low = mid + 1;
            } else if (arr[mid] < arr[high]) {
                high = mid;
            } else {
                high--;
            }
        }
        return low;
    }

    pair<int, int> searchRange(const vector<int>& arr, int low, int high, int target) {
        int start = -1, end = -1;
        
        int l = low, r = high;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (arr[mid] >= target) {
                if (arr[mid] == target) start = mid;
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        }
        
        if (start == -1) return {-1, -1};
        
        l = low; r = high;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (arr[mid] <= target) {
                if (arr[mid] == target) end = mid;
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }
        return {start, end};
    }

    int countEvens(int L, int R) {
        if (L > R) return 0;
        int len = R - L + 1;
        if (len % 2 == 0) return len / 2;
        return (L % 2 == 0) ? (len + 1) / 2 : (len - 1) / 2;
    }

public:
    int countEvenIndices(const vector<int>& arr, int x) {
        int n = arr.size();
        int pivot = findPivot(arr, 0, n - 1);
        
        int count = 0;
        if (pivot > 0) {
            pair<int, int> range = searchRange(arr, 0, pivot - 1, x);
            if (range.first != -1) {
                count += countEvens(range.first, range.second);
            }
        }
        
        pair<int, int> range = searchRange(arr, pivot, n - 1, x);
        if (range.first != -1) {
            count += countEvens(range.first, range.second);
        }
        
        return count;
    }
};
```

### JavaScript

```javascript
class Solution {
  countEvenIndices(arr, x) {
    const n = arr.length;
    
    const findPivot = (low, high) => {
      while (low < high) {
        const mid = Math.floor((low + high) / 2);
        if (arr[mid] > arr[high]) {
          low = mid + 1;
        } else if (arr[mid] < arr[high]) {
          high = mid;
        } else {
          high--;
        }
      }
      return low;
    };
    
    const searchRange = (low, high, target) => {
      let start = -1, end = -1;
      
      let l = low, r = high;
      while (l <= r) {
        const mid = Math.floor((l + r) / 2);
        if (arr[mid] >= target) {
          if (arr[mid] === target) start = mid;
          r = mid - 1;
        } else {
          l = mid + 1;
        }
      }
      
      if (start === -1) return [-1, -1];
      
      l = low; r = high;
      while (l <= r) {
        const mid = Math.floor((l + r) / 2);
        if (arr[mid] <= target) {
          if (arr[mid] === target) end = mid;
          l = mid + 1;
        } else {
          r = mid - 1;
        }
      }
      return [start, end];
    };
    
    const countEvens = (L, R) => {
      if (L > R) return 0;
      const len = R - L + 1;
      if (len % 2 === 0) return len / 2;
      return (L % 2 === 0) ? (len + 1) / 2 : (len - 1) / 2;
    };
    
    const pivot = findPivot(0, n - 1);
    let count = 0;
    
    if (pivot > 0) {
      const [s, e] = searchRange(0, pivot - 1, x);
      if (s !== -1) count += countEvens(s, e);
    }
    
    const [s, e] = searchRange(pivot, n - 1, x);
    if (s !== -1) count += countEvens(s, e);
    
    return count;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
`6`
`4 5 5 1 2 3`
`5`

1.  **Find Pivot**:
    -   `low=0, high=5`. `mid=2 (5) > arr[5] (3)`. `low=3`.
    -   `low=3, high=5`. `mid=4 (2) < arr[5] (3)`. `high=4`.
    -   `low=3, high=4`. `mid=3 (1) < arr[4] (2)`. `high=3`.
    -   Pivot at index 3 (value 1).
2.  **Search Left [0, 2]**:
    -   Array `[4, 5, 5]`. Target `5`.
    -   First occurrence: Index 1.
    -   Last occurrence: Index 2.
    -   Range `[1, 2]`.
    -   Evens in `[1, 2]`: Length 2. `2/2 = 1`. (Index 2 is even).
3.  **Search Right [3, 5]**:
    -   Array `[1, 2, 3]`. Target `5`.
    -   Not found.
4.  **Total**: `1 + 0 = 1`.

## Proof of Correctness

-   **Pivot**: Correctly identifies the rotation point, splitting array into two sorted sequences.
-   **Binary Search**: Correctly finds the start and end of the target value in sorted sequences.
-   **Parity Counting**: The formula `(len + (L%2==0 ? 1 : 0))/2` for odd length correctly counts evens.

## Interview Extensions

1.  **Search in Rotated Sorted Array II?**
    -   Just return boolean exists. Same worst case `O(N)`.
2.  **Find Minimum in Rotated Sorted Array II?**
    -   Same logic as `findPivot`.

### Common Mistakes

-   **Pivot Finding**: Handling `arr[mid] == arr[high]` incorrectly. Must decrement `high` safely.
-   **Range Counting**: Off-by-one errors in `countEvens`.
-   **Split Logic**: Forgetting to search both left and right of pivot.
