---
title: Assembly Previous Greater with Parity
slug: assembly-previous-greater-parity
difficulty: Medium
difficulty_score: 46
tags:
- Stack
- Monotonic Stack
- Parity
problem_id: STK_ASSEMBLY_PREVIOUS_GREATER_PARITY__6802
display_id: STK-006
topics:
- Stack
- Monotonic Stack
- Parity
---
# Assembly Previous Greater with Parity - Editorial

## Problem Summary

For each element in an array, find the nearest element to its **left** that is **strictly greater** than the current element AND has the **opposite parity** (one is even, the other is odd). If no such element exists, return `-1`.


## Constraints

- `1 <= n <= 200000`
- `-10^9 <= a[i] <= 10^9`
## Real-World Scenario

Imagine an **Assembly Line** where components of two types (Type A: Even, Type B: Odd) are moving down a belt.
-   You are inspecting a component (say, Type A).
-   You need to find a "Supervisor Component" that came before it.
-   A valid Supervisor must be:
    1.  **Larger** (more complex/higher rank).
    2.  **Different Type** (Type B) to ensure cross-functional compatibility.
    3.  **Nearest** (most recent) to maintain locality.
-   You need to quickly tag each component with its Supervisor's ID.

## Problem Exploration

### 1. Previous Greater Element (PGE)
-   The standard "Previous Greater Element" problem is solved using a Monotonic Stack.
-   We maintain a stack of elements that are decreasing in value.
-   When a new element `x` comes, we pop elements `<= x` because `x` blocks them from being the "Previous Greater" for any future elements.
-   The element remaining on top is the nearest greater element.

### 2. Parity Constraint
-   Here, we have an extra condition: `parity(prev) != parity(curr)`.
-   If the current element is **Even**, we only care about previous **Odd** elements that are greater.
-   If the current element is **Odd**, we only care about previous **Even** elements that are greater.
-   A single stack might not work well because an Even element might pop a large Odd element that is needed by a future Even element.
-   **Example**: `[9, 2, 5]`
    -   `9` (Odd). Stack: `[9]`.
    -   `2` (Even). `9 > 2` and opposite parity. Answer `9`. Stack: `[9, 2]`.
    -   `5` (Odd). `2 < 5`, pop `2`. Top is `9`. `9 > 5` but same parity (Odd). `9` is not valid for `5`.
    -   But we can't pop `9` just because it has the same parity as `5`. A future Even number (e.g., `4`) might need `9`.
    -   However, `5` effectively "blocks" `9` for any future **Odd** numbers looking for an Odd PGE? No, we look for *Opposite* parity.
    -   Future Odd numbers look for Even PGEs. `9` is Odd, so it's irrelevant for future Odds anyway.
    -   If a future Even is `8`. It wants an Odd > 8. `5` is not > 8. `9` is > 8.
    -   So `5` does NOT fully block `9`. `9` is still needed.
    -   This implies we cannot simply pop `9` when processing `5`.
    -   This suggests we need **two separate stacks**:
        1.  Stack for **Even** numbers (candidates for future Odds).
        2.  Stack for **Odd** numbers (candidates for future Evens).

### 3. Dual Stack Strategy
-   **Even Stack**: Stores indices of Even numbers. Monotonic decreasing?
    -   If we have Even numbers `10, 4`.
    -   Future Odd `7` comes. It looks for Even > 7. `4` is not > 7. `10` is > 7.
    -   Should we pop `4`?
    -   If a future Odd `3` comes, `4` would be a valid candidate (closer than `10`).
    -   So `4` is useful for smaller Odds, `10` is useful for larger Odds.
    -   This looks like we just need to maintain the "Previous Greater" property within the Even numbers themselves?
    -   If a future Odd `x` needs an Even > `x`.
    -   If `x < 4`, `4` is the answer (closest).
    -   If `4 < x < 10`, `10` is the answer.
    -   If `x > 10`, neither.
    -   This implies we keep `10` and `4`.
    -   What if we have `4, 10`?
    -   `10` blocks `4` for *all* future queries because `10` is larger AND closer (or same distance if we consider indices).
    -   Yes! If `curr_even > prev_even`, `prev_even` is useless for any future Odd looking for a "Previous Greater Even". The `curr_even` is strictly better (larger and closer).
    -   So, for the **Even Stack**, we maintain a **Monotonic Decreasing** sequence of Even numbers.
    -   Same for the **Odd Stack**.

### 4. Algorithm
-   Initialize `evenStack` and `oddStack`.
-   Iterate `i` from `0` to `n-1`.
-   If `arr[i]` is Even:
    -   We need an Odd > `arr[i]`.
    -   Look at `oddStack`.
    -   We can't just pop from `oddStack` because `arr[i]` (Even) doesn't block Odds for future Evens.
    -   `arr[i]` is Even. It participates in `evenStack`. It has no effect on `oddStack` maintenance.
    -   So we just **search** `oddStack` for the nearest element > `arr[i]`.
    -   Since `oddStack` is monotonic decreasing (e.g., `9, 5`), we can binary search?
    -   Or do we just pop?
    -   Let's re-evaluate "blocking".
    -   Does an Even number block an Odd number? No.
    -   Does an Even number block an Even number? Yes (as established above).
    -   So `evenStack` is maintained purely by Even numbers. `oddStack` by Odd numbers.
    -   When we process `arr[i]` (Even):
        1.  Update `evenStack`: Pop elements <= `arr[i]`. Push `arr[i]`.
        2.  Query `oddStack`: Find the nearest element > `arr[i]`.
            -   `oddStack` contains `O1, O2, ... Ok` (decreasing values, increasing indices).
            -   We want the largest index `j` such that `oddStack[j] > arr[i]`.
            -   Since values are decreasing, we want the last element in the stack that is > `arr[i]`.
            -   This can be found via **Binary Search** on the stack.
    -   The problem constraints `N=200,000` allow `O(N log N)` complexity.

## Approaches

### Approach 1: Dual Monotonic Stacks with Binary Search
-   Maintain `evenStack` and `oddStack`. Both monotonic decreasing.
-   For each `x`:
    -   If `x` is Even:
        -   Binary search `oddStack` for the element closest to the top (largest index) that is `> x`.
        -   Update `evenStack` (pop `<= x`, push `x`).
    -   If `x` is Odd:
        -   Binary search `evenStack`.
        -   Update `oddStack`.
-   Complexity: `O(N log N)`.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public int[] prevGreaterOppositeParity(int[] arr) {
        int n = arr.length;
        int[] result = new int[n];
        Arrays.fill(result, -1);
        
        // Stacks store indices
        List<Integer> evenStack = new ArrayList<>();
        List<Integer> oddStack = new ArrayList<>();
        
        for (int i = 0; i < n; i++) {
            int val = arr[i];
            
            if (val % 2 == 0) {
                // Current is Even, look in Odd Stack
                int idx = findNearestGreater(oddStack, arr, val);
                if (idx != -1) result[i] = arr[idx];
                
                // Update Even Stack
                while (!evenStack.isEmpty() && arr[evenStack.get(evenStack.size() - 1)] <= val) {
                    evenStack.remove(evenStack.size() - 1);
                }
                evenStack.add(i);
            } else {
                // Current is Odd, look in Even Stack
                int idx = findNearestGreater(evenStack, arr, val);
                if (idx != -1) result[i] = arr[idx];
                
                // Update Odd Stack
                while (!oddStack.isEmpty() && arr[oddStack.get(oddStack.size() - 1)] <= val) {
                    oddStack.remove(oddStack.size() - 1);
                }
                oddStack.add(i);
            }
        }
        return result;
    }
    
    // Find the index in stack closest to the end (top) where arr[stack[k]] > val
    // Stack values are decreasing. We want the smallest stack value > val.
    // This corresponds to the rightmost valid element in the list.
    private int findNearestGreater(List<Integer> stack, int[] arr, int val) {
        if (stack.isEmpty()) return -1;
        
        int l = 0, r = stack.size() - 1;
        int ansIdx = -1;
        
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (arr[stack.get(mid)] > val) {
                ansIdx = stack.get(mid);
                l = mid + 1; // Try to find a closer one (further right in stack)
            } else {
                r = mid - 1; // Too small, go left (larger values)
            }
        }
        return ansIdx;
    }
}
```

### Python

```python
def prev_greater_same_parity(arr: list[int]) -> list[int]:
    """Find previous greater element with same parity (odd/even value)"""
    n = len(arr)
    result = [-1] * n
    stack = []  # Monotonic stack of indices with decreasing values
    
    for i in range(n):
        # Maintain monotonic decreasing stack
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        
        # Find previous greater with same parity (of VALUE)
        for j in range(len(stack) - 1, -1, -1):
            if arr[stack[j]] % 2 == arr[i] % 2:
                result[i] = stack[j]
                break
        
        stack.append(i)
    
    return result

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    
    result = prev_greater_same_parity(arr)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()

```### C++

```cpp
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
    int findNearestGreater(const vector<int>& stack, const vector<int>& arr, int val) {
        if (stack.empty()) return -1;
        
        int l = 0, r = stack.size() - 1;
        int ansIdx = -1;
        
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (arr[stack[mid]] > val) {
                ansIdx = stack[mid];
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }
        return ansIdx;
    }

public:
    vector<int> prevGreaterOppositeParity(const vector<int>& arr) {
        int n = arr.size();
        vector<int> result(n, -1);
        vector<int> evenStack;
        vector<int> oddStack;
        
        for (int i = 0; i < n; i++) {
            int val = arr[i];
            
            if (val % 2 == 0) {
                int idx = findNearestGreater(oddStack, arr, val);
                if (idx != -1) result[i] = arr[idx];
                
                while (!evenStack.empty() && arr[evenStack.back()] <= val) {
                    evenStack.pop_back();
                }
                evenStack.push_back(i);
            } else {
                int idx = findNearestGreater(evenStack, arr, val);
                if (idx != -1) result[i] = arr[idx];
                
                while (!oddStack.empty() && arr[oddStack.back()] <= val) {
                    oddStack.pop_back();
                }
                oddStack.push_back(i);
            }
        }
        return result;
    }
};
```

### JavaScript

```javascript
class Solution {
  prevGreaterOppositeParity(arr) {
    const n = arr.length;
    const result = new Int32Array(n).fill(-1);
    
    const evenStack = [];
    const oddStack = [];
    
    const findNearestGreater = (stack, val) => {
      if (stack.length === 0) return -1;
      
      let l = 0;
      let r = stack.length - 1;
      let ansIdx = -1;
      
      while (l <= r) {
        const mid = Math.floor((l + r) / 2);
        if (arr[stack[mid]] > val) {
          ansIdx = stack[mid];
          l = mid + 1;
        } else {
          r = mid - 1;
        }
      }
      return ansIdx;
    };
    
    for (let i = 0; i < n; i++) {
      const val = arr[i];
      
      if (val % 2 === 0) {
        const idx = findNearestGreater(oddStack, val);
        if (idx !== -1) result[i] = arr[idx];
        
        while (evenStack.length > 0 && arr[evenStack[evenStack.length - 1]] <= val) {
          evenStack.pop();
        }
        evenStack.push(i);
      } else {
        const idx = findNearestGreater(evenStack, val);
        if (idx !== -1) result[i] = arr[idx];
        
        while (oddStack.length > 0 && arr[oddStack[oddStack.length - 1]] <= val) {
          oddStack.pop();
        }
        oddStack.push(i);
      }
    }
    
    return Array.from(result);
  }
}
```

### Python

```python

def previous_greater_parity(arr):
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        
        if stack:
            result[i] = stack[-1]
        
        stack.append(i)
    
    return result

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    
    result = previous_greater_parity(arr)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()

```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:** `4 1 6 3 8`

1.  `4` (E): -1. StackE: `[4]`.
2.  `1` (O): Need E > 1. `4` > 1. Res `4`. StackO: `[1]`.
3.  `6` (E): Need O > 6. `1` not > 6. Res -1. StackE: `[6]` (4 popped).
4.  `3` (O): Need E > 3. `6` > 3. Res `6`. StackO: `[3]` (1 popped).
5.  `8` (E): Need O > 8. `3` not > 8. Res -1. StackE: `[8]` (6 popped).

Result: `-1 4 -1 6 -1`.

## Proof of Correctness

-   **Monotonicity**: We maintain stacks of potential "Previous Greater" candidates.
-   **Binary Search**: Since we cannot simply pop from the "other" stack (as it doesn't block), we use binary search to find the nearest valid candidate. The stack is naturally sorted, enabling this.
-   **Completeness**: We check the best possible candidate (nearest and largest) from the valid set.

## Interview Extensions

1.  **Next Greater Opposite Parity**: Same logic, iterate Right to Left.
2.  **Distance Constraint**: Add `j - i <= k`. Binary search makes this easy (check index).

### Common Mistakes

-   **Single Stack**: Trying to use one stack and skipping elements. This is `O(N^2)` in worst case.
-   **Popping from Wrong Stack**: Popping from `oddStack` when processing an Even number. Even numbers don't invalidate Odd candidates for future Evens.
