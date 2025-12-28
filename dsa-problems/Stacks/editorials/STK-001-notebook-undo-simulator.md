---
title: Notebook Undo Simulator
slug: notebook-undo-simulator
difficulty: Easy
difficulty_score: 20
tags:
- Stack
- Simulation
- LIFO
problem_id: STK_NOTEBOOK_UNDO_SIMULATOR__4827
display_id: STK-001
topics:
- Stack
- Simulation
- Data Structures
---
# Notebook Undo Simulator - Editorial

## Problem Summary

You need to implement a basic undo buffer using a stack. The system supports three operations:
1.  `PUSH x`: Add an action (represented by `x`) to the history.
2.  `POP`: Undo the most recent action and output it.
3.  `TOP`: Peek at the most recent action without removing it.

If the stack is empty during `POP` or `TOP`, output `EMPTY`.


## Constraints

- `1 <= m <= 100000`
- `-10^9 <= x <= 10^9`
## Real-World Scenario

Think of a **Text Editor** like Microsoft Word or Google Docs.
-   Every time you type a word, delete a sentence, or format text, the editor saves this action in a history buffer.
-   When you press `Ctrl+Z` (Undo), the editor looks at the *most recent* action you performed and reverses it.
-   If you press Undo again, it reverses the action before that.
-   This "Last-In, First-Out" (LIFO) behavior is exactly what a Stack data structure provides. The most recently added item is the first one to be removed.

## Problem Exploration

### 1. Understanding LIFO
-   The core requirement is to access elements in the reverse order of their insertion.
-   A **Stack** is the perfect data structure for this. It supports `push` (add to top) and `pop` (remove from top) in `O(1)` time.

### 2. Handling Empty States
-   A common edge case in stack problems is trying to access or remove an element when the stack is empty.
-   The problem explicitly states to output `EMPTY` in these cases.
-   We must check `stack.isEmpty()` before performing `pop` or `top` operations.

### 3. Data Types
-   The input values `x` can be large (`-10^9` to `10^9`).
-   Standard integer types in most languages (like `int` in Java/C++, `number` in JS) can handle this range. In C++, `long long` is safer if values exceed 2 billion, but `int` usually covers up to `2*10^9`. Given the constraint `10^9`, a standard 32-bit signed integer is sufficient.

## Approaches

### Approach 1: Standard Stack Simulation
-   Use the built-in Stack class or a dynamic array (List/Vector) to simulate the stack.
-   **PUSH**: Append the value to the list.
-   **POP**: Check if empty. If not, remove the last element and print it. Else print `EMPTY`.
-   **TOP**: Check if empty. If not, print the last element. Else print `EMPTY`.
-   Complexity: `O(1)` per operation. Total Time: `O(M)`. Space: `O(M)` to store history.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public List<String> process(List<String[]> ops) {
        List<String> result = new ArrayList<>();
        Stack<String> stack = new Stack<>();
        
        for (String[] op : ops) {
            String command = op[0];
            
            if (command.equals("PUSH")) {
                stack.push(op[1]);
            } else if (command.equals("POP")) {
                if (stack.isEmpty()) {
                    result.add("EMPTY");
                } else {
                    result.add(stack.pop());
                }
            } else if (command.equals("TOP")) {
                if (stack.isEmpty()) {
                    result.add("EMPTY");
                } else {
                    result.add(stack.peek());
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
    stack = []
    result = []
    
    for op in ops:
        command = op[0]
        
        if command == "PUSH":
            stack.append(op[1])
        elif command == "POP":
            if not stack:
                result.append("EMPTY")
            else:
                result.append(stack.pop())
        elif command == "TOP":
            if not stack:
                result.append("EMPTY")
            else:
                result.append(stack[-1])
                
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
        stack<string> s;
        
        for (const auto& op : ops) {
            string command = op[0];
            
            if (command == "PUSH") {
                s.push(op[1]);
            } else if (command == "POP") {
                if (s.empty()) {
                    result.push_back("EMPTY");
                } else {
                    result.push_back(s.top());
                    s.pop();
                }
            } else if (command == "TOP") {
                if (s.empty()) {
                    result.push_back("EMPTY");
                } else {
                    result.push_back(s.top());
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
    const stack = [];
    
    for (const op of ops) {
      const command = op[0];
      
      if (command === "PUSH") {
        stack.push(op[1]);
      } else if (command === "POP") {
        if (stack.length === 0) {
          result.push("EMPTY");
        } else {
          result.push(stack.pop());
        }
      } else if (command === "TOP") {
        if (stack.length === 0) {
          result.push("EMPTY");
        } else {
          result.push(stack[stack.length - 1]);
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
5
PUSH 10
PUSH -1
TOP
POP
TOP
```

1.  `PUSH 10`: Stack is `[10]`.
2.  `PUSH -1`: Stack is `[10, -1]`.
3.  `TOP`: Stack is `[10, -1]`. Top is `-1`. Output `-1`.
4.  `POP`: Stack is `[10, -1]`. Pop `-1`. Stack becomes `[10]`. Output `-1`.
5.  `TOP`: Stack is `[10]`. Top is `10`. Output `10`.

**Output:**
```
-1
-1
10
```

### Python

```python

def process(ops):
    result = []
    stack = []
    
    for op in ops:
        command = op[0]
        
        if command == "PUSH":
            stack.append(op[1])
        elif command == "POP":
            if len(stack) == 0:
                result.append("EMPTY")
            else:
                result.append(stack.pop())
        elif command == "TOP":
            if len(stack) == 0:
                result.append("EMPTY")
            else:
                result.append(stack[-1])
    
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

## Proof of Correctness

-   **LIFO Property**: The `Stack` data structure (or `list` with `append`/`pop`) inherently maintains the LIFO order required by the problem.
-   **Empty Checks**: Explicit checks for `isEmpty` ensure we never crash or return incorrect values for empty stack operations.
-   **Efficiency**: All operations are `O(1)`, ensuring the solution runs well within the time limit for `M=100,000`.

## Interview Extensions

1.  **Min-Stack**: Can you also support a `getMin()` operation in `O(1)`?
    -   *Hint*: Use an auxiliary stack to keep track of the minimum element at each state.
2.  **Fixed Size**: What if the undo buffer has a maximum size `K`?
    -   *Hint*: Use a Deque (Double Ended Queue). When pushing to a full stack, remove the oldest element from the bottom.

### Common Mistakes

-   **Forgetting Empty Check**: Calling `pop()` on an empty stack usually throws an exception.
-   **Output Format**: Printing `Empty` instead of `EMPTY` (case sensitivity).
-   **String vs Int**: Treating inputs as numbers is fine, but since we just output them, treating them as strings avoids parsing overhead and potential overflow issues (though constraints here are safe).
