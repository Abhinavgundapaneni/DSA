---
title: Minimum Operations to Make Array Alternating
slug: min-ops-make-alternating
difficulty: Medium
difficulty_score: 51
tags:
- Greedy
- Counting
- Arrays
problem_id: SRT_MIN_OPS_MAKE_ALTERNATING__4621
display_id: SRT-014
topics:
- Sorting
- Counting
- Greedy
---
# Minimum Operations to Make Array Alternating - Editorial

## Problem Summary

You are given an array `a`. You want to make it alternating, meaning `a[0] == a[2] == a[4]...` and `a[1] == a[3] == a[5]...`, with the condition that `a[0] != a[1]`. You can change any element to any value. Find the minimum number of changes required.

## Real-World Scenario

Imagine you are a **Tiler** laying a floor.
-   The design requires a checkerboard-like pattern in 1D: Black, White, Black, White...
-   You have a row of tiles already laid out, but they are a mix of colors.
-   You want to paint over the minimum number of tiles to achieve the alternating pattern.
-   However, you are not restricted to Black and White; you can pick any two distinct colors (e.g., Red and Blue) that maximize the number of tiles you *don't* have to paint.

## Problem Exploration

### 1. Even and Odd Indices
-   The problem requires all even indices `0, 2, 4...` to have the same value `X`.
-   It requires all odd indices `1, 3, 5...` to have the same value `Y`.
-   Constraint: `X != Y`.
-   To minimize changes, we want to maximize the number of elements that are *already* `X` at even positions and `Y` at odd positions.
-   Total Changes = `(Total Evens - Count of X at Evens) + (Total Odds - Count of Y at Odds)`.
-   This simplifies to: `Total Elements - (Count of X at Evens + Count of Y at Odds)`.
-   So we need to maximize `Count(X, Even) + Count(Y, Odd)` subject to `X != Y`.

### 2. Frequency Analysis
-   Count frequencies of all numbers at even indices. Let the top two most frequent be `(E1_val, E1_count)` and `(E2_val, E2_count)`.
-   Count frequencies of all numbers at odd indices. Let top two be `(O1_val, O1_count)` and `(O2_val, O2_count)`.
-   Why top two? Because if the best even value `E1_val` is the same as the best odd value `O1_val`, we can't use both. We must pick the second best for one of them.

### 3. Cases
-   **Case 1**: `E1_val != O1_val`.
    -   Best combo is simply `E1` and `O1`.
    -   Kept elements = `E1_count + O1_count`.
-   **Case 2**: `E1_val == O1_val`.
    -   We have a conflict. We can't use `E1` and `O1` together.
    -   Option A: Use `E1` and `O2`. Kept = `E1_count + O2_count`.
    -   Option B: Use `E2` and `O1`. Kept = `E2_count + O1_count`.
    -   Take the max of Option A and Option B.
-   Note: If a position (even or odd) has all distinct elements appearing once, or is empty, counts are small. We should handle cases where `E2` or `O2` doesn't exist (count 0).

### 4. Edge Cases
-   `n=1`: 0 changes.
-   Array with all same elements: `[2, 2, 2]`. Even: `2` (count 2). Odd: `2` (count 1). `E1=2`, `O1=2`. Conflict.
    -   Option A: Keep even `2`s. Change odds to something else. Kept `2 + 0`. Changes `1`.
    -   Option B: Keep odd `2`s. Change evens. Kept `1 + 0`. Changes `2`.
    -   Best is 1 change.

## Approaches

### Approach 1: Frequency Counting
-   Count frequencies for even/odd positions.
-   Find top 2 frequent elements for both.
-   Check conflict and compute max kept.
-   Result = `N - max_kept`.
-   Complexity: `O(N)`.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public int minChanges(int[] arr) {
        int n = arr.length;
        if (n <= 1) return 0;
        
        Map<Integer, Integer> evenCounts = new HashMap<>();
        Map<Integer, Integer> oddCounts = new HashMap<>();
        
        for (int i = 0; i < n; i++) {
            if (i % 2 == 0) {
                evenCounts.put(arr[i], evenCounts.getOrDefault(arr[i], 0) + 1);
            } else {
                oddCounts.put(arr[i], oddCounts.getOrDefault(arr[i], 0) + 1);
            }
        }
        
        int[] topEven = getTopTwo(evenCounts);
        int[] topOdd = getTopTwo(oddCounts);
        
        int e1Val = topEven[0], e1Count = topEven[1];
        int e2Val = topEven[2], e2Count = topEven[3];
        int o1Val = topOdd[0], o1Count = topOdd[1];
        int o2Val = topOdd[2], o2Count = topOdd[3];
        
        if (e1Val != o1Val) {
            return n - (e1Count + o1Count);
        } else {
            int option1 = n - (e1Count + o2Count);
            int option2 = n - (e2Count + o1Count);
            return Math.min(option1, option2);
        }
    }
    
    private int[] getTopTwo(Map<Integer, Integer> counts) {
        int firstVal = -1, firstCount = 0;
        int secondVal = -1, secondCount = 0;
        
        for (Map.Entry<Integer, Integer> entry : counts.entrySet()) {
            int val = entry.getKey();
            int count = entry.getValue();
            
            if (count > firstCount) {
                secondCount = firstCount;
                secondVal = firstVal;
                firstCount = count;
                firstVal = val;
            } else if (count > secondCount) {
                secondCount = count;
                secondVal = val;
            }
        }
        return new int[]{firstVal, firstCount, secondVal, secondCount};
    }
}
```

### Python

```python
from collections import Counter

def min_changes(arr: list[int]) -> int:
    n = len(arr)
    if n <= 1:
        return 0
        
    even_counts = Counter(arr[i] for i in range(0, n, 2))
    odd_counts = Counter(arr[i] for i in range(1, n, 2))
    
    def get_top_two(counts):
        # Returns [(val, count), (val, count)]
        # Add dummy values to ensure at least 2 elements
        most = counts.most_common(2)
        if not most:
            return [(-1, 0), (-1, 0)]
        if len(most) == 1:
            return [most[0], (-1, 0)]
        return most
        
    e_top = get_top_two(even_counts)
    o_top = get_top_two(odd_counts)
    
    e1_val, e1_count = e_top[0]
    e2_val, e2_count = e_top[1]
    o1_val, o1_count = o_top[0]
    o2_val, o2_count = o_top[1]
    
    if e1_val != o1_val:
        return n - (e1_count + o1_count)
    else:
        opt1 = n - (e1_count + o2_count)
        opt2 = n - (e2_count + o1_count)
        return min(opt1, opt2)

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    result = min_changes(arr)
    print(result)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <map>
#include <algorithm>

using namespace std;

class Solution {
    struct Top {
        int val = -1;
        int count = 0;
    };
    
    pair<Top, Top> getTopTwo(const map<int, int>& counts) {
        Top first, second;
        for (auto const& [val, count] : counts) {
            if (count > first.count) {
                second = first;
                first = {val, count};
            } else if (count > second.count) {
                second = {val, count};
            }
        }
        return {first, second};
    }

public:
    int minChanges(const vector<int>& arr) {
        int n = arr.size();
        if (n <= 1) return 0;
        
        map<int, int> evenCounts;
        map<int, int> oddCounts;
        
        for (int i = 0; i < n; i++) {
            if (i % 2 == 0) evenCounts[arr[i]]++;
            else oddCounts[arr[i]]++;
        }
        
        auto [e1, e2] = getTopTwo(evenCounts);
        auto [o1, o2] = getTopTwo(oddCounts);
        
        if (e1.val != o1.val) {
            return n - (e1.count + o1.count);
        } else {
            int opt1 = n - (e1.count + o2.count);
            int opt2 = n - (e2.count + o1.count);
            return min(opt1, opt2);
        }
    }
};
```

### JavaScript

```javascript
class Solution {
  minChanges(arr) {
    const n = arr.length;
    if (n <= 1) return 0;
    
    const evenCounts = new Map();
    const oddCounts = new Map();
    
    for (let i = 0; i < n; i++) {
      if (i % 2 === 0) {
        evenCounts.set(arr[i], (evenCounts.get(arr[i]) || 0) + 1);
      } else {
        oddCounts.set(arr[i], (oddCounts.get(arr[i]) || 0) + 1);
      }
    }
    
    const getTopTwo = (counts) => {
      let firstVal = -1, firstCount = 0;
      let secondVal = -1, secondCount = 0;
      
      for (const [val, count] of counts.entries()) {
        if (count > firstCount) {
          secondCount = firstCount;
          secondVal = firstVal;
          firstCount = count;
          firstVal = val;
        } else if (count > secondCount) {
          secondCount = count;
          secondVal = val;
        }
      }
      return [{val: firstVal, count: firstCount}, {val: secondVal, count: secondCount}];
    };
    
    const [e1, e2] = getTopTwo(evenCounts);
    const [o1, o2] = getTopTwo(oddCounts);
    
    if (e1.val !== o1.val) {
      return n - (e1.count + o1.count);
    } else {
      const opt1 = n - (e1.count + o2.count);
      const opt2 = n - (e2.count + o1.count);
      return Math.min(opt1, opt2);
    }
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
`4`
`1 1 1 2`

1.  **Indices**:
    -   Even (0, 2): `[1, 1]`. Counts: `{1: 2}`.
    -   Odd (1, 3): `[1, 2]`. Counts: `{1: 1, 2: 1}`.
2.  **Top Two**:
    -   Even: `E1=(1, 2)`, `E2=(-1, 0)`.
    -   Odd: `O1=(1, 1)`, `O2=(2, 1)`. (Order of 1 and 2 in odd doesn't strictly matter for O1, but let's say 1 is O1).
3.  **Check**:
    -   `E1.val (1) == O1.val (1)`. Conflict.
    -   Option 1: Use `E1` and `O2`. Kept = `2 + 1 = 3`. Changes = `4 - 3 = 1`.
    -   Option 2: Use `E2` and `O1`. Kept = `0 + 1 = 1`. Changes = `4 - 1 = 3`.
    -   Min changes: 1.
4.  **Result**: 1. (Change odd index 1 from 1 to 2 -> `1 2 1 2`).

## Proof of Correctness

-   **Greedy**: We want to maximize the number of unchanged elements.
-   **Cases**: Since we only need to pick one value for evens and one for odds, checking the top 2 candidates covers all optimal scenarios. If the best choices conflict, the next best choice for one of them combined with the best of the other is guaranteed to be optimal.

## Interview Extensions

1.  **Alternating Period K?**
    -   `a[i] == a[i+K]`. Count frequencies modulo K. Solve K independent problems? No, distinct values constraint might apply between adjacent groups?
    -   Usually "alternating" implies period 2.
2.  **Cost to change values?**
    -   If changing `x` to `y` has cost `C(x, y)`, this becomes a min-cost matching or flow problem.

### Common Mistakes

-   **Empty Maps**: Handling cases where all elements are at even indices (not possible if n > 1) or only 1 distinct element exists.
-   **Tie Breaking**: The order of top 2 doesn't matter as long as we check both cross combinations.
