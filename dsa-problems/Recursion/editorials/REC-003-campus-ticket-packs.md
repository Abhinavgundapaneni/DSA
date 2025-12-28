---
title: Campus Ticket Packs
slug: campus-ticket-packs
difficulty: Medium
difficulty_score: 46
tags:
- Recursion
- Backtracking
- Combinations
problem_id: REC_CAMPUS_TICKET_PACKS__2187
display_id: REC-003
topics:
- Recursion
- Backtracking
- Combinations
---
# Campus Ticket Packs - Editorial

## Problem Summary

You are given `n` types of tickets. For the `i`-th type, the ticket has a value `v[i]` and comes in a fixed pack size of `p[i]`. This means for each ticket type, you can either take **0** tickets or exactly **`p[i]`** tickets. You cannot take a partial pack or multiple packs of the same type (unless multiple types have the same value, but they are treated as distinct options).

Your goal is to find all unique combinations of ticket values that sum up exactly to `target`. Each combination should be listed as individual ticket values. For example, if you take a pack of 2 tickets with value 5, your combination includes `5, 5`.


## Constraints

- `1 <= n <= 15`
- `1 <= target <= 200`
- `1 <= v[i] <= 50`
- `1 <= p[i] <= 10`
## Real-World Scenario

Imagine a **Vending Machine** that only dispenses items in bundles.
-   Chips cost \$2 and come in a twin-pack (2 bags).
-   Soda costs \$3 and comes in a single can.
-   Candy costs \$1 and comes in a 3-pack.

You have exactly \`7. What combinations of items can you buy to spend exactly`7? You can't buy just one bag of chips; you must buy the twin-pack or nothing.

## Problem Exploration

### 1. Decision Tree
For each ticket type `i` (from `0` to `n-1`), we have a binary choice:
1.  **Skip**: Take 0 tickets. Contribution to sum = 0.
2.  **Take**: Take `p[i]` tickets of value `v[i]`. Contribution to sum = `p[i] * v[i]`.

### 2. Output Format
The problem asks for the combination of *values*. If we take a pack of size 2 with value 5, we add `5, 5` to our current list of values. The final output requires these values to be sorted non-decreasingly.

### 3. Uniqueness and Ordering
Since the problem asks for "unique combinations", and the input might have duplicate `(value, pack)` pairs, or different pairs might produce the same set of values (e.g., Pack A: value 2, size 2 -> `2, 2`; Pack B: value 2, size 2 -> `2, 2`), we need to be careful. However, usually in such "subset sum" variations, unless specified otherwise, distinct items in input are treated as distinct choices. The problem says "List all unique combinations", implying if two different sets of choices lead to the same multiset of values, we might need to handle duplicates.
*Clarification based on example*: The example shows `2 2 3`. This comes from taking `v[0]=2, p[0]=2` (contributes `2, 2`, sum 4) and `v[1]=3, p[1]=1` (contributes `3`, sum 3). Total sum 7.
The simplest interpretation is standard backtracking: iterate through items, decide to include or exclude.

## Approaches

### Approach 1: Backtracking (Subset Sum Variation)

We can use a recursive function `solve(index, current_sum, current_list)`.
-   **Base Case**:
    -   If `current_sum == target`: Add `current_list` to results.
    -   If `current_sum > target` or `index == n`: Return.
-   **Recursive Step**:
    -   **Option 1 (Include)**: Add `p[index]` copies of `v[index]` to `current_list`. Recurse with `solve(index + 1, current_sum + total_value, new_list)`.
    -   **Option 2 (Exclude)**: Recurse with `solve(index + 1, current_sum, current_list)`.

To ensure the output is sorted and unique:
1.  We can collect all valid combinations.
2.  Sort each combination internally.
3.  Sort the list of combinations.
4.  Remove duplicates if necessary (though if input items are distinct indices, the combinations of indices are unique. If the *values* are what matters, we might generate duplicates if identical packs exist). Given the constraints and problem type, usually we just output valid subsets found via search.

### Optimization: Pruning
-   Sort the input items by value or some heuristic? Not strictly necessary for correctness but helps with duplicate detection if needed.
-   If `current_sum + (p[i] * v[i]) > target`, we can't take item `i`.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public List<List<Integer>> packCombinations(int[] values, int[] packs, int target) {
        List<List<Integer>> result = new ArrayList<>();
        // We need to pass index, current sum, and current list of values
        backtrack(0, 0, new ArrayList<>(), values, packs, target, result);
        
        // The problem asks for "unique combinations". 
        // If the problem implies set uniqueness based on content (multiset of values),
        // we should deduplicate. Given "List all unique combinations", let's use a Set to be safe
        // or ensure we generate them in a specific order.
        // However, usually distinct indices constitute distinct solutions. 
        // Let's stick to simple backtracking first.
        // Sorting the internal lists is required for the output format "nondecreasing order".
        
        for (List<Integer> list : result) {
            Collections.sort(list);
        }
        
        // Deduplicate based on content
        Set<List<Integer>> uniqueResults = new HashSet<>(result);
        List<List<Integer>> finalResult = new ArrayList<>(uniqueResults);
        
        // Sort the list of lists for consistent output
        finalResult.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) {
                if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            }
            return a.size() - b.size();
        });
        
        return finalResult;
    }

    private void backtrack(int index, int currentSum, List<Integer> currentList, 
                          int[] values, int[] packs, int target, List<List<Integer>> result) {
        if (currentSum == target) {
            result.add(new ArrayList<>(currentList));
            return;
        }
        if (currentSum > target || index == values.length) {
            return;
        }

        // Option 1: Include current pack
        int packVal = values[index];
        int packSize = packs[index];
        int totalVal = packVal * packSize;

        if (currentSum + totalVal <= target) {
            for (int k = 0; k < packSize; k++) currentList.add(packVal);
            backtrack(index + 1, currentSum + totalVal, currentList, values, packs, target, result);
            for (int k = 0; k < packSize; k++) currentList.remove(currentList.size() - 1);
        }

        // Option 2: Exclude current pack
        backtrack(index + 1, currentSum, currentList, values, packs, target, result);
    }
}
```

### Python

```python
def count_combinations(coins: list[int], target: int) -> int:
    """Count ways to make target using coins (unlimited supply)."""
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for coin in coins:
        for i in range(coin, target + 1):
            dp[i] += dp[i - coin]
    
    return dp[target]

def main():
    line1 = input().split()
    n, target = int(line1[0]), int(line1[1])
    coins = list(map(int, input().split()))
    print(count_combinations(coins, target))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <algorithm>
#include <set>

using namespace std;

class Solution {
public:
    vector<vector<int>> packCombinations(const vector<int>& values, const vector<int>& packs, int target) {
        set<vector<int>> unique_results;
        vector<int> current;
        backtrack(0, 0, current, values, packs, target, unique_results);
        
        vector<vector<int>> result(unique_results.begin(), unique_results.end());
        return result;
    }

private:
    void backtrack(int idx, int currentSum, vector<int>& current, 
                   const vector<int>& values, const vector<int>& packs, int target, 
                   set<vector<int>>& results) {
        if (currentSum == target) {
            vector<int> temp = current;
            sort(temp.begin(), temp.end());
            results.insert(temp);
            return;
        }
        if (idx == values.size() || currentSum > target) {
            return;
        }

        // Option 1: Include
        int packVal = values[idx];
        int packSize = packs[idx];
        int totalVal = packVal * packSize;

        if (currentSum + totalVal <= target) {
            for(int k=0; k<packSize; ++k) current.push_back(packVal);
            backtrack(idx + 1, currentSum + totalVal, current, values, packs, target, results);
            for(int k=0; k<packSize; ++k) current.pop_back();
        }

        // Option 2: Exclude
        backtrack(idx + 1, currentSum, current, values, packs, target, results);
    }
};
```

### JavaScript

```javascript
class Solution {
  packCombinations(values, packs, target) {
    const results = [];
    const n = values.length;

    const backtrack = (idx, currentSum, currentItems) => {
      if (currentSum === target) {
        // Create a copy and sort it
        results.push([...currentItems].sort((a, b) => a - b));
        return;
      }
      if (idx === n || currentSum > target) {
        return;
      }

      // Option 1: Include
      const packVal = values[idx];
      const packSize = packs[idx];
      const totalVal = packVal * packSize;

      if (currentSum + totalVal <= target) {
        const nextItems = [...currentItems];
        for (let k = 0; k < packSize; k++) nextItems.push(packVal);
        backtrack(idx + 1, currentSum + totalVal, nextItems);
      }

      // Option 2: Exclude
      backtrack(idx + 1, currentSum, currentItems);
    };

    backtrack(0, 0, []);

    // Deduplicate
    const uniqueSet = new Set();
    const uniqueResults = [];
    
    for (const res of results) {
      const key = res.join(",");
      if (!uniqueSet.has(key)) {
        uniqueSet.add(key);
        uniqueResults.push(res);
      }
    }

    // Sort results lexicographically
    uniqueResults.sort((a, b) => {
      for (let i = 0; i < Math.min(a.length, b.length); i++) {
        if (a[i] !== b[i]) return a[i] - b[i];
      }
      return a.length - b.length;
    });

    return uniqueResults;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
`n=2`
`values=[2, 3]`
`packs=[2, 1]`
`target=7`

1.  **Index 0 (Val 2, Pack 2)**:
    -   **Include**: Adds `2, 2`. Sum = 4.
        -   Recurse to Index 1.
        -   **Index 1 (Val 3, Pack 1)**:
            -   **Include**: Adds `3`. Sum = 4 + 3 = 7.
                -   Target reached! Add `[2, 2, 3]` to results.
            -   **Exclude**: Sum = 4.
                -   End of list. Return.
    -   **Exclude**: Sum = 0.
        -   Recurse to Index 1.
        -   **Index 1 (Val 3, Pack 1)**:
            -   **Include**: Adds `3`. Sum = 3.
                -   End of list. Return.
            -   **Exclude**: Sum = 0.
                -   End of list. Return.

**Result**: `[[2, 2, 3]]`.

## Proof of Correctness

The algorithm explores the binary decision tree of including or excluding each ticket pack.
-   **Completeness**: Since we try both options for every item, we cover all possible subsets.
-   **Correctness**: We only add to the result if the sum exactly matches the target.
-   **Uniqueness**: By using a Set (or manual deduplication) on the sorted contents of valid combinations, we ensure no duplicate combinations are output.

## Interview Extensions

1.  **What if `n` is large (e.g., 100)?**
    -   This is the Subset Sum problem, which is NP-Complete. Standard backtracking won't work. If `target` is small, we can use Dynamic Programming (Knapsack-style).

2.  **What if we can take partial packs?**
    -   The problem changes to the standard Knapsack problem (or Change Making problem), where we can take `0 dots p[i]` items.

3.  **Can we optimize space?**
    -   We are storing all solutions. If we only needed the *count* of solutions, we could use DP. Since we need to list them, we can't avoid storing them, but we can avoid creating new list objects at every step by backtracking on a single list.

### Common Mistakes

-   **Incorrect Sum Calculation**: Adding `v[i]` instead of `v[i] * p[i]` to the sum.
-   **Output Format**: Forgetting to split the pack into individual values (e.g., outputting `4` instead of `2 2`).
-   **Sorting**: The problem requires the output values to be sorted.

## Related Concepts

-   **Subset Sum Problem**: The underlying algorithmic challenge.
-   **Knapsack Problem**: Similar structure (items with weights/values).
-   **Backtracking**: The solution technique.
