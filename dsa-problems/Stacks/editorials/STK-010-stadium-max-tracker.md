---
title: Stadium Max Tracker
slug: stadium-max-tracker
difficulty: Medium
difficulty_score: 40
tags:
- Stack
- Max Stack
- Design
problem_id: STK_STADIUM_MAX_TRACKER__3658
display_id: STK-010
topics:
- Stack
- Data Structures
- Design
---
# Stadium Max Tracker - Editorial

## Problem Summary

Design a stack that supports `PUSH`, `POP`, `TOP`, and `GETMAX` operations. All operations should be efficient (ideally `O(1)`). `GETMAX` returns the maximum element currently in the stack.


## Constraints

- `1 <= m <= 100000`
- `-10^9 <= x <= 10^9`
## Real-World Scenario

Imagine you are managing a **Stadium Crowd**.
-   People enter the stadium one by one (Push).
-   Sometimes people leave (Pop).
-   You want to know the **loudest person** currently in the stadium (GetMax).
-   If the loudest person leaves, you need to instantly know who the *next* loudest person is.
-   You can't ask everyone to shout again every time someone leaves. You need to keep track of the "maximums" history.

## Problem Exploration

### 1. Naive Approach
-   `PUSH`, `POP`, `TOP` are standard `O(1)`.
-   `GETMAX`: Iterate through the entire stack to find the max. `O(N)`.
-   This is too slow if we have many `GETMAX` queries.

### 2. Auxiliary Max Stack
-   We can maintain a second stack, let's call it `maxStack`.
-   `maxStack` will store the maximum value encountered *so far* up to the current height of the main stack.
-   **PUSH x**:
    -   Push `x` to `mainStack`.
    -   If `maxStack` is empty or `x >= maxStack.top()`, push `x` to `maxStack`.
    -   Else, push `maxStack.top()` again to `maxStack`. (This duplicates the current max, ensuring `maxStack` size matches `mainStack` size).
    -   *Optimization*: We don't strictly need `maxStack` to be the same size. We can just push to `maxStack` if `x >= currentMax`. When popping, if `poppedValue == currentMax`, we pop from `maxStack` too.
-   **POP**:
    -   Pop from `mainStack`.
    -   If we use the "same size" approach: Pop from `maxStack` too.
    -   If we use the "optimized" approach: If the popped value equals `maxStack.top()`, pop from `maxStack`.
-   **GETMAX**:
    -   Return `maxStack.top()`.

### 3. Optimized Space
-   The "same size" approach uses `2N` space.
-   The "optimized" approach uses `N + M` space (where `M` is number of new maximums). In worst case (sorted ascending), `M=N`.
-   Both are `O(N)` space.
-   The "same size" logic is slightly simpler to implement because we don't need to check values on POP.
-   However, the "optimized" logic is more standard for "Min Stack" / "Max Stack" problems.
-   Let's use the optimized logic:
    -   `PUSH x`: `main.push(x)`. If `maxStack.empty() || x >= maxStack.peek()`, `maxStack.push(x)`.
    -   `POP`: `val = main.pop()`. If `val == maxStack.peek()`, `maxStack.pop()`.
    -   `GETMAX`: `maxStack.peek()`.

## Approaches

### Approach 1: Two Stacks (Optimized)
-   `mainStack`: Stores all elements.
-   `maxStack`: Stores the sequence of maximums.
-   Complexity: `O(1)` time for all ops. `O(N)` space.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public List<String> process(List<String[]> ops) {
        List<String> result = new ArrayList<>();
        Stack<Integer> mainStack = new Stack<>();
        Stack<Integer> maxStack = new Stack<>();
        
        for (String[] op : ops) {
            String cmd = op[0];
            
            if (cmd.equals("PUSH")) {
                int val = Integer.parseInt(op[1]);
                mainStack.push(val);
                if (maxStack.isEmpty() || val >= maxStack.peek()) {
                    maxStack.push(val);
                }
            } else if (cmd.equals("POP")) {
                if (mainStack.isEmpty()) {
                    result.add("EMPTY");
                } else {
                    int val = mainStack.pop();
                    result.add(String.valueOf(val));
                    if (val == maxStack.peek()) {
                        maxStack.pop();
                    }
                }
            } else if (cmd.equals("TOP")) {
                if (mainStack.isEmpty()) {
                    result.add("EMPTY");
                } else {
                    result.add(String.valueOf(mainStack.peek()));
                }
            } else if (cmd.equals("GETMAX")) {
                if (mainStack.isEmpty()) {
                    result.add("EMPTY");
                } else {
                    result.add(String.valueOf(maxStack.peek()));
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
    result = []
    main_stack = []
    max_stack = []
    
    for op in ops:
        cmd = op[0]
        
        if cmd == "PUSH":
            val = int(op[1])
            main_stack.append(val)
            if not max_stack or val >= max_stack[-1]:
                max_stack.append(val)
        elif cmd == "POP":
            if main_stack:
                val = main_stack.pop()
                if val == max_stack[-1]:
                    max_stack.pop()
        elif cmd == "MAX":
            if not main_stack:
                result.append("EMPTY")
            else:
                result.append(str(max_stack[-1]))
                
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
#include <stack>

using namespace std;

class Solution {
public:
    vector<string> process(const vector<vector<string>>& ops) {
        vector<string> result;
        stack<int> mainStack;
        stack<int> maxStack;
        
        for (const auto& op : ops) {
            string cmd = op[0];
            
            if (cmd == "PUSH") {
                int val = stoi(op[1]);
                mainStack.push(val);
                if (maxStack.empty() || val >= maxStack.top()) {
                    maxStack.push(val);
                }
            } else if (cmd == "POP") {
                if (mainStack.empty()) {
                    result.push_back("EMPTY");
                } else {
                    int val = mainStack.top();
                    mainStack.pop();
                    result.push_back(to_string(val));
                    if (val == maxStack.top()) {
                        maxStack.pop();
                    }
                }
            } else if (cmd == "TOP") {
                if (mainStack.empty()) {
                    result.push_back("EMPTY");
                } else {
                    result.push_back(to_string(mainStack.top()));
                }
            } else if (cmd == "GETMAX") {
                if (mainStack.empty()) {
                    result.push_back("EMPTY");
                } else {
                    result.push_back(to_string(maxStack.top()));
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
    const mainStack = [];
    const maxStack = [];
    
    for (const op of ops) {
      const cmd = op[0];
      
      if (cmd === "PUSH") {
        const val = parseInt(op[1], 10);
        mainStack.push(val);
        if (maxStack.length === 0 || val >= maxStack[maxStack.length - 1]) {
          maxStack.push(val);
        }
      } else if (cmd === "POP") {
        if (mainStack.length === 0) {
          result.push("EMPTY");
        } else {
          const val = mainStack.pop();
          result.push(val.toString());
          if (val === maxStack[maxStack.length - 1]) {
            maxStack.pop();
          }
        }
      } else if (cmd === "TOP") {
        if (mainStack.length === 0) {
          result.push("EMPTY");
        } else {
          result.push(mainStack[mainStack.length - 1].toString());
        }
      } else if (cmd === "GETMAX") {
        if (mainStack.length === 0) {
          result.push("EMPTY");
        } else {
          result.push(maxStack[maxStack.length - 1].toString());
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
PUSH 2
PUSH 9
PUSH 5
GETMAX
POP
GETMAX
```

### Python

```python

def max_tracker(ops):
    stack = []
    max_stack = []
    result = []
    
    for op in ops:
        cmd = op[0]
        
        if cmd == "PUSH":
            val = int(op[1])
            stack.append(val)
            if not max_stack or val >= max_stack[-1]:
                max_stack.append(val)
            else:
                max_stack.append(max_stack[-1])
        
        elif cmd == "POP":
            if stack:
                stack.pop()
                max_stack.pop()
        
        elif cmd == "MAX":
            if max_stack:
                result.append(max_stack[-1])
            else:
                result.append("EMPTY")
    
    return result

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    m = int(lines[0])
    ops = []
    for i in range(1, m + 1):
        parts = lines[i].split()
        ops.append(parts)
    
    result = max_tracker(ops)
    for r in result:
        print(r)

if __name__ == "__main__":
    main()

```

1.  `PUSH 2`: Main `[2]`. Max `[2]`.
2.  `PUSH 9`: Main `[2, 9]`. `9 >= 2`. Max `[2, 9]`.
3.  `PUSH 5`: Main `[2, 9, 5]`. `5 < 9`. Max `[2, 9]`.
4.  `GETMAX`: Max top is `9`. Output `9`.
5.  `POP`: Main pop `5`. `5 != 9`. Max stays `[2, 9]`. Output `5`.
6.  `GETMAX`: Max top is `9`. Output `9`.

**Output:** `9`, `5`, `9`. Matches example.

## Proof of Correctness

-   **Invariant**: `maxStack` contains a non-decreasing subsequence of `mainStack` elements. The top of `maxStack` is always the maximum of `mainStack`.
-   **Push**: If new element is `>=` current max, it becomes the new max. We push it.
-   **Pop**: If we remove the current max (value matches), we pop from `maxStack` to reveal the previous max.
-   **Efficiency**: All ops `O(1)`.

## Interview Extensions

1.  **Pop Max**: Support `popMax()` which removes the maximum element (even if deep in stack).
    -   *Hint*: Use a Doubly Linked List + TreeMap, or just two stacks with lazy deletion (complex). `O(log N)` or `O(N)` usually.
2.  **Min Stack**: Same logic, just `>=` becomes `<=`.

### Common Mistakes

-   **Strict Inequality**: Using `>` instead of `>=` when pushing to `maxStack`. If we have `[9, 9]`, we need `maxStack` to have `[9, 9]` so that popping one `9` leaves the other.
-   **Empty Checks**: Crashing on `GETMAX` or `POP` when empty.
