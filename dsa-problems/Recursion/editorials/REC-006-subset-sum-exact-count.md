---
title: Subset Sum Exact Count
slug: subset-sum-exact-count
difficulty: Medium
difficulty_score: 43
tags:
- Recursion
- Backtracking
- Subset Sum
problem_id: REC_SUBSET_SUM_EXACT_COUNT__1854
display_id: REC-006
topics:
- Recursion
- Backtracking
- Subset Sum
---
# Subset Sum Exact Count - Editorial

## Problem Summary

You are given an array of integers `arr`, a target sum `target`, and an integer `k`. You need to find a subset of `arr` that contains exactly `k` elements and whose sum is exactly `target`. If multiple such subsets exist, any one is acceptable. If none exist, output `NONE`.


## Constraints

- `1 <= n <= 20`
- `0 <= k <= n`
- `|arr[i]| <= 10000`
- `|target| <= 10^9`
## Real-World Scenario

Imagine you are a **Cashier** and a customer needs to pay exactly \`50 using exactly 3 bills from their wallet. They have a mix of`10, \`20,`5, and \$1 bills. You need to check if there's a combination of 3 bills that sums to 50.

Another example is **Nutritional Planning**. You want to consume exactly 2000 calories using exactly 5 different food items from a provided menu.

## Problem Exploration

### 1. Constraints
-   `N <= 20`: This is small enough for an exponential solution `O(2^N)`.
-   `K <= N`: We need to pick exactly `K` items.
-   Target and values can be large or negative (though usually positive in subset sum, constraints say `|arr[i]| <= 10000`, so negative numbers are possible).

### 2. Recursive Structure
For each element `arr[i]`, we have two choices:
1.  **Include it**: We need to find `K-1` more elements summing to `target - arr[i]` from the remaining array.
2.  **Exclude it**: We need to find `K` elements summing to `target` from the remaining array.

### 3. Pruning
-   If we have already picked `k` elements and the sum is not `target`, backtrack.
-   If we have picked fewer than `k` elements but ran out of items in the array, backtrack.
-   If the remaining number of items in the array is less than the number of items we still need to pick, backtrack.

## Approaches

### Approach 1: Backtracking (DFS)
We define `solve(index, current_k, current_sum, current_list)`.
-   **Base Case**:
    -   If `current_k == k`: Check if `current_sum == target`. If yes, return `true`.
    -   If `index == n`: Return `false`.
-   **Recursive Step**:
    -   **Include**: Add `arr[index]` to list. Recurse. If returns true, propagate true.
    -   **Exclude**: Recurse without adding. If returns true, propagate true.

### Approach 2: Meet-in-the-middle (Optimization)
For `N=20`, simple backtracking is fast enough (`2^20 ~= 10^6`). If `N` were 40, we would split the array into two halves, generate all subset sums (with counts) for both halves, and try to match them. This is overkill here.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public List<Integer> findSubset(int[] arr, int k, int target) {
        List<Integer> result = new ArrayList<>();
        if (backtrack(0, 0, 0, arr, k, target, result)) {
            return result;
        }
        return new ArrayList<>();
    }

    private boolean backtrack(int index, int count, int currentSum, int[] arr, int k, int target, List<Integer> result) {
        if (count == k) {
            return currentSum == target;
        }
        if (index == arr.length) {
            return false;
        }
        
        // Pruning: if remaining elements are not enough to fill k
        if (arr.length - index < k - count) {
            return false;
        }

        // Option 1: Include arr[index]
        result.add(arr[index]);
        if (backtrack(index + 1, count + 1, currentSum + arr[index], arr, k, target, result)) {
            return true;
        }
        result.remove(result.size() - 1); // Backtrack

        // Option 2: Exclude arr[index]
        if (backtrack(index + 1, count, currentSum, arr, k, target, result)) {
            return true;
        }

        return false;
    }
}
```

### Python

```python
def find_subset(arr: list[int], k: int, target: int) -> list[int]:
    n = len(arr)
    result = []

    def backtrack(index, count, current_sum):
        if count == k:
            return current_sum == target
        
        if index == n:
            return False
        
        # Pruning
        if n - index < k - count:
            return False

        # Option 1: Include
        result.append(arr[index])
        if backtrack(index + 1, count + 1, current_sum + arr[index]):
            return True
        result.pop()

        # Option 2: Exclude
        if backtrack(index + 1, count, current_sum):
            return True
            
        return False

    if backtrack(0, 0, 0):
        return result
    return []

def main():
    first_line = input().split()
    n, k, target = int(first_line[0]), int(first_line[1]), int(first_line[2])
    arr = list(map(int, input().split()))
    result = find_subset(arr, k, target)
    if result:
        print(' '.join(map(str, result)))
    else:
        print("NONE")

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <numeric>

using namespace std;

class Solution {
public:
    vector<int> findSubset(const vector<int>& arr, int k, int target) {
        vector<int> current;
        if (backtrack(0, 0, 0, arr, k, target, current)) {
            return current;
        }
        return {};
    }

private:
    bool backtrack(int index, int count, int currentSum, const vector<int>& arr, int k, int target, vector<int>& current) {
        if (count == k) {
            return currentSum == target;
        }
        if (index == arr.size()) {
            return false;
        }
        
        // Pruning
        if (arr.size() - index < k - count) {
            return false;
        }

        // Option 1: Include
        current.push_back(arr[index]);
        if (backtrack(index + 1, count + 1, currentSum + arr[index], arr, k, target, current)) {
            return true;
        }
        current.pop_back();

        // Option 2: Exclude
        if (backtrack(index + 1, count, currentSum, arr, k, target, current)) {
            return true;
        }

        return false;
    }
};
```

### JavaScript

```javascript
class Solution {
  findSubset(arr, k, target) {
    const result = [];
    const n = arr.length;

    const backtrack = (index, count, currentSum) => {
      if (count === k) {
        return currentSum === target;
      }
      if (index === n) {
        return false;
      }

      // Pruning
      if (n - index < k - count) {
        return false;
      }

      // Option 1: Include
      result.push(arr[index]);
      if (backtrack(index + 1, count + 1, currentSum + arr[index])) {
        return true;
      }
      result.pop();

      // Option 2: Exclude
      if (backtrack(index + 1, count, currentSum)) {
        return true;
      }

      return false;
    };

    if (backtrack(0, 0, 0)) {
      return result;
    }
    return [];
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
`4 2 7`
`4 1 6 2`

1.  `solve(0, 0, 0)` (Index 0, Count 0, Sum 0)
    -   **Include 4**: `solve(1, 1, 4)`
        -   **Include 1**: `solve(2, 2, 5)`. Count=2, Sum=5 != 7. Fail.
        -   **Exclude 1**: `solve(2, 1, 4)`
            -   **Include 6**: `solve(3, 2, 10)`. Count=2, Sum=10 != 7. Fail.
            -   **Exclude 6**: `solve(3, 1, 4)`
                -   **Include 2**: `solve(4, 2, 6)`. Count=2, Sum=6 != 7. Fail.
                -   **Exclude 2**: `solve(4, 1, 4)`. Index=4. Fail.
    -   **Exclude 4**: `solve(1, 0, 0)`
        -   **Include 1**: `solve(2, 1, 1)`
            -   **Include 6**: `solve(3, 2, 7)`. Count=2, Sum=7 == 7. **Success!**
            -   Return True.
        -   Return True.
    -   Return True.

**Result:** `[1, 6]`.

## Proof of Correctness

The algorithm explores the state space of all subsets of size `k`.
-   **Completeness**: The binary recursion tree covers all `2^N` subsets, but we stop deeper recursion once `count == k`.
-   **Correctness**: We only return `true` if we hit the base case `count == k` AND `sum == target`.
-   **Pruning**: The check `n - index < k - count` ensures we don't waste time on branches that can never reach `k` elements.

## Interview Extensions

1.  **What if we need ALL such subsets?**
    -   Instead of returning `true` on the first match, add the current list to a `results` list and continue searching (backtrack).

2.  **What if elements must be non-negative?**
    -   We can add another pruning step: if `currentSum > target`, stop (since adding more non-negative numbers won't help).

3.  **What if `k` is not fixed (any size subset)?**
    -   Remove the `count` parameter and check `sum == target` at every step.

### Common Mistakes

-   **Incorrect Base Case**: Checking `sum == target` without checking `count == k`.
-   **Pruning Logic**: `n - index` is remaining items. `k - count` is needed items. If `remaining < needed`, impossible.
-   **Backtracking**: Forgetting to `pop` after the recursive call returns `false`.

