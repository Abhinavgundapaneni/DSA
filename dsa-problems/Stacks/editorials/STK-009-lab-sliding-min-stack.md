---
title: Lab Sliding-Min Stack
slug: lab-sliding-min-stack
difficulty: Medium
difficulty_score: 52
tags:
- Stack
- Min Stack
- Range Queries
problem_id: STK_LAB_SLIDING_MIN_STACK__5027
display_id: STK-009
topics:
- Stack
- Range Minimum
- Data Structures
---
# Lab Sliding-Min Stack - Editorial

## Problem Summary

You need to implement a stack that supports `PUSH x`, `POP`, and a special query `MIN k`.
-   `MIN k`: Returns the minimum value among the top `k` elements of the stack.
-   Standard error handling for empty stack or insufficient elements.


## Constraints

- `1 <= m <= 100000`
- `-10^9 <= x <= 10^9`
- `1 <= k <= 100000`
## Real-World Scenario

Imagine you are a **Lab Technician** recording temperature readings in a logbook.
-   You write down readings one by one (Push).
-   Sometimes you realize a mistake and cross out the last entry (Pop).
-   Occasionally, your supervisor asks: "What was the lowest temperature recorded in the last 5 readings?" (Min k).
-   You need a way to answer this quickly without scanning through the last 5 pages every time.

## Problem Exploration

### 1. Standard Min-Stack
-   A standard Min-Stack stores pairs `(val, current_min)`.
-   `current_min` is the minimum of *all* elements currently in the stack.
-   This answers `MIN k` where `k == stack.size()`.
-   But we need `MIN k` for *any* `k`.

### 2. Naive Approach
-   For `MIN k`, iterate through the top `k` elements.
-   Complexity: `O(k)` per query. In worst case `O(N)`.
-   Total time `O(M * N)` is too slow for `M=100,000`.

### 3. Sliding Window Minimum?
-   The "top k" elements form a window.
-   As we push, the window slides/expands.
-   But `k` is not fixed. One query might be `MIN 2`, next `MIN 10`.
-   This suggests we need to query the minimum in the range `[size - k, size - 1]`.
-   This is a **Range Minimum Query (RMQ)** on a dynamic array.
-   We can use a Segment Tree or Fenwick Tree over the stack indices.
-   Complexity: `O(log N)` per operation.
-   Can we do `O(1)`?

### 4. Auxiliary Monotonic Stack?
-   What if we store "candidates" for minimums?
-   Consider stack: `[5, 1, 3, 2, 4]` (Top is right).
-   Top 1: `4`. Min 4.
-   Top 2: `2, 4`. Min 2.
-   Top 3: `3, 2, 4`. Min 2.
-   Top 4: `1, 3, 2, 4`. Min 1.
-   Top 5: `5, 1, 3, 2, 4`. Min 1.
-   Notice the minimums for `k=1..5` are `4, 2, 2, 1, 1`.
-   This sequence is non-increasing.
-   We need to find the minimum in a suffix of the stack.
-   We use a **Segment Tree** approach which provides efficient range minimum queries.
-   Operations:
    -   `PUSH`: Update position `size` with value. `size++`.
    -   `POP`: `size--`. (Value at old size is effectively removed).
    -   `MIN k`: Query range `[size - k, size - 1]`.
-   This is `O(log N)` per operation, which is efficient for the given constraints.

## Approaches

### Approach 1: Segment Tree on Stack Indices
-   Maintain a global array `arr` and a variable `size`.
-   Build a Segment Tree over `[0, MAX_M]`.
-   `PUSH x`: `update(size, x)`, `size++`.
-   `POP`: `size--`.
-   `MIN k`: `query(size - k, size - 1)`.
-   Complexity: `O(log M)` per op.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    int[] tree;
    int n = 100005; // Max operations
    int currentSize = 0;
    
    void update(int node, int start, int end, int idx, int val) {
        if (start == end) {
            tree[node] = val;
            return;
        }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, val);
        else update(2 * node + 1, mid + 1, end, idx, val);
        tree[node] = Math.min(tree[2 * node], tree[2 * node + 1]);
    }
    
    int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return Integer.MAX_VALUE;
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return Math.min(query(2 * node, start, mid, l, r), query(2 * node + 1, mid + 1, end, l, r));
    }

    public List<String> process(List<String[]> ops) {
        List<String> result = new ArrayList<>();
        tree = new int[4 * n];
        Arrays.fill(tree, Integer.MAX_VALUE);
        currentSize = 0;
        
        for (String[] op : ops) {
            String cmd = op[0];
            if (cmd.equals("PUSH")) {
                int val = Integer.parseInt(op[1]);
                update(1, 0, n - 1, currentSize, val);
                currentSize++;
            } else if (cmd.equals("POP")) {
                if (currentSize == 0) {
                    result.add("EMPTY");
                } else {
                    // To output the popped value, we need to store it or query it.
                    // Querying point is O(log N). Storing in array is O(1).
                    // Let's query.
                    int val = query(1, 0, n - 1, currentSize - 1, currentSize - 1);
                    result.add(String.valueOf(val));
                    currentSize--;
                }
            } else if (cmd.equals("MIN")) {
                int k = Integer.parseInt(op[1]);
                if (currentSize < k) {
                    result.add("NA");
                } else {
                    int minVal = query(1, 0, n - 1, currentSize - k, currentSize - 1);
                    result.add(String.valueOf(minVal));
                }
            }
        }
        return result;
    }
}
```

### Python

```python
def process(ops: list[list[str]]) -> list[str]:
    """Process stack operations with MIN k support"""
    result = []
    stack = []  # Main stack storing values
    
    for op in ops:
        cmd = op[0]
        if cmd == "PUSH":
            val = int(op[1])
            stack.append(val)
        elif cmd == "POP":
            if not stack:
                result.append("EMPTY")
            else:
                result.append(str(stack.pop()))
        elif cmd == "MIN":
            k = int(op[1])
            if len(stack) == 0:
                result.append("EMPTY")
            elif len(stack) < k:
                result.append("NA")
            else:
                # Get minimum of top k elements
                top_k = stack[-k:]
                result.append(str(min(top_k)))
                
    return result

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    m = int(lines[0])
    ops = []
    for i in range(1, m + 1):
        parts = lines[i].split()
        ops.append(parts)
    
    result = process(ops)
    for r in result:
        print(r)

if __name__ == "__main__":
    main()

```

### C++

```cpp
#include <vector>
#include <string>
#include <algorithm>
#include <climits>

using namespace std;

class Solution {
    vector<int> tree;
    int n = 100005;
    int currentSize = 0;
    vector<int> stackVals;

    void update(int node, int start, int end, int idx, int val) {
        if (start == end) {
            tree[node] = val;
            return;
        }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, val);
        else update(2 * node + 1, mid + 1, end, idx, val);
        tree[node] = min(tree[2 * node], tree[2 * node + 1]);
    }

    int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return INT_MAX;
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return min(query(2 * node, start, mid, l, r), query(2 * node + 1, mid + 1, end, l, r));
    }

public:
    vector<string> process(const vector<vector<string>>& ops) {
        vector<string> result;
        tree.assign(4 * n, INT_MAX);
        currentSize = 0;
        stackVals.clear();
        
        for (const auto& op : ops) {
            string cmd = op[0];
            if (cmd == "PUSH") {
                int val = stoi(op[1]);
                stackVals.push_back(val);
                update(1, 0, n - 1, currentSize, val);
                currentSize++;
            } else if (cmd == "POP") {
                if (currentSize == 0) {
                    result.push_back("EMPTY");
                } else {
                    result.push_back(to_string(stackVals.back()));
                    stackVals.pop_back();
                    currentSize--;
                }
            } else if (cmd == "MIN") {
                int k = stoi(op[1]);
                if (currentSize < k) {
                    result.push_back("NA");
                } else {
                    int minVal = query(1, 0, n - 1, currentSize - k, currentSize - 1);
                    result.push_back(to_string(minVal));
                }
            }
        }
        return result;
    }
};
```

### JavaScript

```javascript
class Solution {
  process(ops) {
    const result = [];
    const n = 100005;
    const tree = new Int32Array(4 * n).fill(2147483647); // INT_MAX
    let currentSize = 0;
    const stackVals = [];
    
    const update = (node, start, end, idx, val) => {
      if (start === end) {
        tree[node] = val;
        return;
      }
      const mid = Math.floor((start + end) / 2);
      if (idx <= mid) update(2 * node, start, mid, idx, val);
      else update(2 * node + 1, mid + 1, end, idx, val);
      tree[node] = Math.min(tree[2 * node], tree[2 * node + 1]);
    };
    
    const query = (node, start, end, l, r) => {
      if (r < start || end < l) return 2147483647;
      if (l <= start && end <= r) return tree[node];
      const mid = Math.floor((start + end) / 2);
      return Math.min(query(2 * node, start, mid, l, r),
                      query(2 * node + 1, mid + 1, end, l, r));
    };
    
    for (const op of ops) {
      const cmd = op[0];
      if (cmd === "PUSH") {
        const val = parseInt(op[1], 10);
        stackVals.push(val);
        update(1, 0, n - 1, currentSize, val);
        currentSize++;
      } else if (cmd === "POP") {
        if (currentSize === 0) {
          result.push("EMPTY");
        } else {
          result.push(stackVals.pop().toString());
          currentSize--;
        }
      } else if (cmd === "MIN") {
        const k = parseInt(op[1], 10);
        if (currentSize < k) {
          result.push("NA");
        } else {
          const minVal = query(1, 0, n - 1, currentSize - k, currentSize - 1);
          result.push(minVal.toString());
        }
      }
    }
    return result;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
```
PUSH 5
PUSH 1
PUSH 3
MIN 2
POP
MIN 2
```

### Python

```python

def sliding_min_stack(ops):
    stack = []
    min_stack = []
    result = []
    
    for op in ops:
        cmd = op[0]
        
        if cmd == "PUSH":
            val = int(op[1])
            stack.append(val)
            if not min_stack or val <= min_stack[-1]:
                min_stack.append(val)
            else:
                min_stack.append(min_stack[-1])
        
        elif cmd == "POP":
            if stack:
                stack.pop()
                min_stack.pop()
        
        elif cmd == "MIN":
            if min_stack:
                result.append(min_stack[-1])
    
    return result

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    m = int(lines[0])
    ops = []
    for i in range(1, m + 1):
        parts = lines[i].split()
        ops.append(parts)
    
    result = sliding_min_stack(ops)
    for r in result:
        print(r)

if __name__ == "__main__":
    main()

```

1.  `PUSH 5`: Stack `[5]`. SegTree `[5, inf...]`. Size 1.
2.  `PUSH 1`: Stack `[5, 1]`. SegTree `[5, 1, inf...]`. Size 2.
3.  `PUSH 3`: Stack `[5, 1, 3]`. SegTree `[5, 1, 3, inf...]`. Size 3.
4.  `MIN 2`: Query `[3-2, 3-1] = [1, 2]`. Elements at indices 1 and 2 are `1` and `3`. Min is `1`. Output `1`.
5.  `POP`: Output `3`. Size 2. (SegTree effectively ignores index 2 now).
6.  `MIN 2`: Query `[2-2, 2-1] = [0, 1]`. Elements at indices 0 and 1 are `5` and `1`. Min is `1`. Output `1`.

**Output:** `1`, `3`, `1`. Matches example.

## Proof of Correctness

-   **Segment Tree**: Provides correct Range Minimum Query results for any valid range `[L, R]`.
-   **Dynamic Updates**: Pushing updates the tree at the new index. Popping just reduces the valid range size (future pushes overwrite).
-   **Complexity**: `O(log N)` per operation fits within limits.

## Interview Extensions

1.  **O(1) Approach**: Can you do this in `O(1)`?
    -   *Hint*: Since it's a stack, a "Min-Queue" structure using two stacks could work, but `k` is variable.
2.  **Max Query**: Support `MAX k` as well.
    -   *Hint*: Another Segment Tree or augment the existing one.

### Common Mistakes

-   **Index Bounds**: Querying `[size-k, size]` instead of `[size-k, size-1]`.
-   **Empty Checks**: Forgetting `NA` or `EMPTY`.
-   **Tree Size**: Making tree too small. `4 * MAX_OPS` is safe.
