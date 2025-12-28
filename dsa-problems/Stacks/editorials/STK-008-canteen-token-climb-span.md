---
title: Canteen Token Climb Span
slug: canteen-token-climb-span
difficulty: Medium
difficulty_score: 50
tags:
- Stack
- Monotonic Stack
- Spans
problem_id: STK_CANTEEN_TOKEN_CLIMB_SPAN__6180
display_id: STK-008
topics:
- Stack
- Monotonic Stack
- Spans
---
# Canteen Token Climb Span - Editorial

## Problem Summary

For each day `i`, calculate the "span" of demand. The span is defined as the number of consecutive days immediately preceding day `i` (excluding `i` itself) where the demand was **strictly less** than `demand[i]`. If any prior day has demand equal to `demand[i]`, the span stops there (resets to 0).


## Constraints

- `1 <= n <= 100000`
- `0 <= demand[i] <= 10^9`
## Real-World Scenario

Imagine you are analyzing **Canteen Popularity**.
-   Every day, you record how many tokens were sold.
-   You want to know, for today, how long the "winning streak" has been.
-   A "winning streak" means today's sales are strictly better than yesterday, and the day before, and so on.
-   However, if you find a past day where sales were equal to today, that breaks the streak completely (it's not a strict improvement over that day).
-   This metric helps identify if today is a local peak relative to recent history.

## Problem Exploration

### 1. Stock Span Variation
-   This is a classic **Stock Span Problem**.
-   Standard Stock Span: Count consecutive days `<= current`.
-   Our Problem: Count consecutive days `< current`.
-   Also, the problem statement says "If any prior day equals today's demand, the span resets to 0 at that day."
    -   This is slightly ambiguous. Does it mean the span *is* 0? Or does it mean the span stops counting *at* that day?
    -   Example: `3 1 2 2 5`.
    -   Day 2 (val 2): Prior is `1` (<2). Span 1.
    -   Day 3 (val 2): Prior is `2` (==2). Span 0? Or does it stop?
    -   The example output says `0 0 1 0 4`.
    -   Day 0 (3): 0.
    -   Day 1 (1): 0.
    -   Day 2 (2): Prior `1`. Span 1.
    -   Day 3 (2): Prior `2`. Span 0. (Because `2` is not `< 2`).
    -   Day 4 (5): Prior `2, 2, 1`.
    -   Check: `5 > 2`, `5 > 2`, `5 > 1`, `5 > 3`.
    -   All 4 prior days are `< 5`. Span 4.
    -   So the logic is: Find the nearest previous day `j` such that `demand[j] >= demand[i]`. The span is `i - j - 1`.
    -   If no such day exists, `j = -1`. Span `i - (-1) - 1 = i`.

### 2. Monotonic Stack Approach
-   We need to find the **Previous Greater or Equal Element** (PGEE).
-   We maintain a stack of indices `j` such that `demand[j]` is decreasing.
-   For current `demand[i]`:
    -   Pop elements from stack that are strictly smaller than `demand[i]`.
    -   Why strictly smaller? Because we want to find the first element `>=`.
    -   So if `top < current`, `top` cannot be the blocking element. Pop it.
    -   Stop when `stack` is empty or `top >= current`.
    -   If stack empty: No element `>= current` exists to the left. `j = -1`.
    -   If stack not empty: `top` is the nearest element `>= current`. `j = top`.
    -   Span = `i - j - 1`.
    -   Push `i` to stack.

### 3. Example Trace
-   `3 1 2 2 5`
-   `i=0 (3)`: Stack empty. `j=-1`. Span `0 - (-1) - 1 = 0`. Stack `[0]`.
-   `i=1 (1)`: `1 < 3`. Stop pop. `j=0`. Span `1 - 0 - 1 = 0`. Stack `[0, 1]`.
-   `i=2 (2)`: `2 > 1`. Pop 1. `2 < 3`. Stop. `j=0`. Span `2 - 0 - 1 = 1`. Stack `[0, 2]`.
-   `i=3 (2)`: `2` not `> 2`. Stop. `j=2`. Span `3 - 2 - 1 = 0`. Stack `[0, 2, 3]`.
-   `i=4 (5)`: `5 > 2` (pop 3). `5 > 2` (pop 2). `5 > 3` (pop 0). Stack empty. `j=-1`. Span `4 - (-1) - 1 = 4`. Stack `[4]`.
-   Result: `0 0 1 0 4`. Matches example!

## Approaches

### Approach 1: Monotonic Stack (Previous Greater or Equal)
-   Maintain a stack of indices.
-   Iterate `i` from `0` to `n-1`.
-   While `stack` not empty and `demand[stack.peek()] < demand[i]`:
    -   `stack.pop()`
-   `prev_index = stack.isEmpty() ? -1 : stack.peek()`
-   `span[i] = i - prev_index - 1`
-   `stack.push(i)`
-   Complexity: `O(N)` time, `O(N)` space.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public int[] spans(int[] demand) {
        int n = demand.length;
        int[] result = new int[n];
        Stack<Integer> stack = new Stack<>(); // Stores indices
        
        for (int i = 0; i < n; i++) {
            // Find nearest previous element >= current
            // Pop elements strictly smaller
            while (!stack.isEmpty() && demand[stack.peek()] < demand[i]) {
                stack.pop();
            }
            
            int prevIdx = stack.isEmpty() ? -1 : stack.peek();
            result[i] = i - prevIdx - 1;
            
            stack.push(i);
        }
        return result;
    }
}
```

### Python

```python
def spans(prices: list[int]) -> list[int]:
    n = len(prices)
    result = [1] * n
    stack = []
    
    for i in range(n):
        while stack and prices[stack[-1]] <= prices[i]:
            stack.pop()
        
        result[i] = i + 1 if not stack else i - stack[-1]
        stack.append(i)
    
    return result

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    
    result = spans(arr)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()

```

### C++

```cpp
#include <vector>
#include <stack>

using namespace std;

class Solution {
public:
    vector<int> spans(const vector<int>& demand) {
        int n = demand.size();
        vector<int> result(n);
        stack<int> s; // Stores indices
        
        for (int i = 0; i < n; i++) {
            while (!s.empty() && demand[s.top()] < demand[i]) {
                s.pop();
            }
            
            int prevIdx = s.empty() ? -1 : s.top();
            result[i] = i - prevIdx - 1;
            
            s.push(i);
        }
        return result;
    }
};
```

### JavaScript

```javascript
class Solution {
  spans(demand) {
    const n = demand.length;
    const result = new Int32Array(n);
    const stack = []; // Stores indices
    
    for (let i = 0; i < n; i++) {
      while (stack.length > 0 && demand[stack[stack.length - 1]] < demand[i]) {
        stack.pop();
      }
      
      const prevIdx = stack.length === 0 ? -1 : stack[stack.length - 1];
      result[i] = i - prevIdx - 1;
      
      stack.push(i);
    }
    
    return Array.from(result);
  }
}
```

### Python

```python

def token_climb_span(arr):
    n = len(arr)
    result = [1] * n
    stack = []
    
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        
        if stack:
            result[i] = i - stack[-1]
        else:
            result[i] = i + 1
        
        stack.append(i)
    
    return result

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    
    result = token_climb_span(arr)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()

```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:** `3 1 2 2 5`

1.  `i=0 (3)`: Stack empty. `prev=-1`. `res=0`. Push 0. Stack `[0]`.
2.  `i=1 (1)`: `1 < 3`. `prev=0`. `res=1-0-1=0`. Push 1. Stack `[0, 1]`.
3.  `i=2 (2)`: `2 > 1` (pop 1). `2 < 3`. `prev=0`. `res=2-0-1=1`. Push 2. Stack `[0, 2]`.
4.  `i=3 (2)`: `2` not `< 2`. `prev=2`. `res=3-2-1=0`. Push 3. Stack `[0, 2, 3]`.
5.  `i=4 (5)`: `5 > 2` (pop 3). `5 > 2` (pop 2). `5 > 3` (pop 0). Stack empty. `prev=-1`. `res=4-(-1)-1=4`. Push 4. Stack `[4]`.

**Result:** `0 0 1 0 4`.

## Proof of Correctness

-   **Invariant**: The stack contains indices `j` such that `demand[j]` is decreasing (or non-increasing).
-   **Nearest Greater or Equal**: By popping all smaller elements, the top of the stack becomes the nearest element to the left that is `>=` current. This is exactly the boundary of the span of strictly smaller elements.
-   **Complexity**: Each element is pushed once and popped at most once. `O(N)`.

## Interview Extensions

1.  **Include Equals**: What if span includes days with equal demand?
    -   *Hint*: Pop elements `<= demand[i]`.
2.  **Online Version**: Implement a class `StockSpanner` with `next(price)`.
    -   *Hint*: Same logic, but process one by one. Store `(price, span)` pairs in stack to skip over already-counted ranges.

### Common Mistakes

-   **Strict vs Non-Strict**: Confusing `<` with `<=`. The problem says "strictly lower", so we stop at `>=`.
-   **Index Arithmetic**: `i - prev - 1` is the correct formula for count of items *between* `prev` and `i`.
