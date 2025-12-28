---
title: Shuttle Validation with Time Windows
slug: shuttle-validation-time-windows
difficulty: Medium
difficulty_score: 61
tags:
- Stack
- Simulation
- Validation
problem_id: STK_SHUTTLE_VALIDATION_TIME_WINDOWS__2743
display_id: STK-014
topics:
- Stack
- Simulation
- Constraints
---
# Shuttle Validation with Time Windows - Editorial

## Problem Summary

Validate a stack push/pop sequence with two additional constraints:
1.  **Time Windows**: Certain elements must be popped within `W` time units of being pushed.
2.  **Priority Constraint**: Each priority element must be popped before any larger non-priority element. When popping a non-priority element `X`, there must be no priority element `P` currently in the stack such that `X > P`. Priority elements block larger non-priority elements from being popped.


## Constraints

- `1 <= n <= 100000`
- `0 <= times <= 10^9`
- All values are integers and unique in the push sequence
## Real-World Scenario

Imagine a **Space Shuttle Cargo Bay**.
-   **Stack**: Cargo is loaded (pushed) and unloaded (popped) in LIFO order.
-   **Time Windows**: Some perishable items (e.g., food, biological samples) must be unloaded within `W` hours of loading, or they spoil.
-   **Priority**: Some items are "High Priority" (e.g., emergency medical supplies).
-   **Rule**: You cannot unload a large, low-priority crate if there's a smaller, high-priority box still waiting in the stack. The validation checks whether the loading/unloading plan respects these constraints.

## Problem Exploration

### 1. Stack Simulation
-   Standard "Validate Stack Sequences" logic:
    -   Iterate through `pushed` array.
    -   Push `pushed[i]`.
    -   While `stack.top() == popped[j]`:
        -   Pop from stack.
        -   `j++`.
-   If stack is empty at the end, the sequence is valid (structurally).

### 2. Time Window Constraint
-   We are given `pushTimes` and `popTimes`.
-   When we push `x` at `pushT`, we store `(x, pushT)`.
-   When we pop `x` at `popT`, we check if `x` has a window `W`.
-   Condition: `popT - pushT <= W`.
-   If not, return `false`.

### 3. Priority Constraint
-   When popping a non-priority element `X`, there must be no priority element `P` currently in the stack such that `P < X`.
-   We need to efficiently track the **minimum priority element** currently in the stack.
-   Use an auxiliary **Min-Stack** to track the minimum priority value at each stack level.
-   When pushing `val`:
    -   If `val` is Priority: `new_min = min(val, current_min)`.
    -   If `val` is Non-Priority: `new_min = current_min`.
    -   Push `new_min` to the auxiliary stack.
-   When popping a non-priority element `X`:
    -   Check if `X > min_priority_in_stack`.
    -   If true, the constraint is violated.
    -   Pop from the auxiliary stack.

## Approaches

### Approach 1: Simulation with Auxiliary Min-Stack
-   Use a main stack for simulation.
-   Use an auxiliary stack to track the minimum priority element currently in the stack.
-   Check time constraints on pop.
-   Check priority constraints on pop.
-   Complexity: `O(N)` time, `O(N)` space.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public boolean validate(int[] push, long[] pushT, int[] pop, long[] popT, Map<Integer, Long> windows, Set<Integer> priority) {
        int n = push.length;
        Stack<Integer> stack = new Stack<>();
        Stack<Long> timeStack = new Stack<>();
        Stack<Integer> minPriorityStack = new Stack<>();
        
        int j = 0;
        for (int i = 0; i < n; i++) {
            int val = push[i];
            long time = pushT[i];
            
            stack.push(val);
            timeStack.push(time);
            
            int currentMin = minPriorityStack.isEmpty() ? Integer.MAX_VALUE : minPriorityStack.peek();
            if (priority.contains(val)) {
                currentMin = Math.min(currentMin, val);
            }
            minPriorityStack.push(currentMin);
            
            while (!stack.isEmpty() && j < n && stack.peek() == pop[j]) {
                int poppedVal = stack.pop();
                long pushedTime = timeStack.pop();
                minPriorityStack.pop(); // Remove current state
                
                long poppedTime = popT[j];
                
                // Check 1: Time Window
                if (windows.containsKey(poppedVal)) {
                    if (poppedTime - pushedTime > windows.get(poppedVal)) {
                        return false;
                    }
                }
                
                // Check 2: Priority
                // If poppedVal is Non-Priority, it must not be larger than any existing Priority
                if (!priority.contains(poppedVal)) {
                    int minP = minPriorityStack.isEmpty() ? Integer.MAX_VALUE : minPriorityStack.peek();
                    if (poppedVal > minP) {
                        return false;
                    }
                }
                
                j++;
            }
        }
        
        return stack.isEmpty();
    }
}
```

### Python

```python
def validate_time_windows(intervals):
    """
    Validate time windows using a stack-based approach.
    Windows are valid if they can be properly nested (like parentheses).
    Two intervals can overlap only if one fully contains the other.
    """
    # Create events: (time, type, index, end_time_for_starts)
    # type: 0 = end, 1 = start (so ends are processed before starts at same time)
    events = []
    for i, (start, end) in enumerate(intervals):
        events.append((start, 1, i, end))  # start event (type 1)
        events.append((end, 0, i, start))   # end event (type 0)
    
    # Sort by time, with ends before starts at same time
    events.sort(key=lambda x: (x[0], x[1]))
    
    stack = []  # stack of (interval_index, end_time)
    
    for time, event_type, idx, other_time in events:
        if event_type == 1:  # start
            stack.append((idx, other_time))  # other_time is end_time for starts
        else:  # end
            if not stack:
                return False
            # The end must match the most recent start (proper nesting)
            top_idx, top_end = stack[-1]
            if top_idx != idx:
                return False
            stack.pop()
    
    return len(stack) == 0

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    intervals = []
    for i in range(1, n + 1):
        parts = lines[i].split()
        start, end = int(parts[0]), int(parts[1])
        intervals.append((start, end))
    
    if validate_time_windows(intervals):
        print("VALID")
    else:
        print("INVALID")

if __name__ == "__main__":
    main()

```

### C++

```cpp
#include <vector>
#include <stack>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <climits>

using namespace std;

class Solution {
public:
    bool validate(const vector<int>& push, const vector<long long>& pushT, const vector<int>& pop, const vector<long long>& popT,
                  const unordered_map<int,long long>& windows, const unordered_set<int>& priority) {
        int n = push.size();
        stack<int> s;
        stack<long long> timeStack;
        stack<int> minPriorityStack;
        
        int j = 0;
        for (int i = 0; i < n; i++) {
            int val = push[i];
            long long time = pushT[i];
            
            s.push(val);
            timeStack.push(time);
            
            int currentMin = minPriorityStack.empty() ? INT_MAX : minPriorityStack.top();
            if (priority.count(val)) {
                currentMin = min(currentMin, val);
            }
            minPriorityStack.push(currentMin);
            
            while (!s.empty() && j < n && s.top() == pop[j]) {
                int poppedVal = s.top(); s.pop();
                long long pushedTime = timeStack.top(); timeStack.pop();
                minPriorityStack.pop();
                
                long long poppedTime = popT[j];
                
                // Check Time
                if (windows.count(poppedVal)) {
                    if (poppedTime - pushedTime > windows.at(poppedVal)) {
                        return false;
                    }
                }
                
                // Check Priority
                if (!priority.count(poppedVal)) {
                    int minP = minPriorityStack.empty() ? INT_MAX : minPriorityStack.top();
                    if (poppedVal > minP) {
                        return false;
                    }
                }
                
                j++;
            }
        }
        
        return s.empty();
    }
};
```

### JavaScript

```javascript
class Solution {
  validate(push, pushT, pop, popT, windows, priority) {
    const n = push.length;
    const stack = [];
    const timeStack = [];
    const minPriorityStack = [];
    
    let j = 0;
    
    for (let i = 0; i < n; i++) {
      const val = push[i];
      const time = pushT[i];
      
      stack.push(val);
      timeStack.push(time);
      
      let currentMin = minPriorityStack.length === 0 ? Infinity : minPriorityStack[minPriorityStack.length - 1];
      if (priority.has(val)) {
        currentMin = Math.min(currentMin, val);
      }
      minPriorityStack.push(currentMin);
      
      while (stack.length > 0 && j < n && stack[stack.length - 1] === pop[j]) {
        const poppedVal = stack.pop();
        const pushedTime = timeStack.pop();
        minPriorityStack.pop();
        
        const poppedTime = popT[j];
        
        // Check Time
        if (windows.has(poppedVal)) {
          if (poppedTime - pushedTime > windows.get(poppedVal)) {
            return false;
          }
        }
        
        // Check Priority
        if (!priority.has(poppedVal)) {
          const minP = minPriorityStack.length === 0 ? Infinity : minPriorityStack[minPriorityStack.length - 1];
          if (poppedVal > minP) {
            return false;
          }
        }
        
        j++;
      }
    }
    
    return stack.length === 0;
  }
}
```

### Python

```python

def is_valid_sequence(s):
    stack = []
    matching = {'(': ')', '[': ']', '{': '}'}
    
    for char in s:
        if char in matching:
            stack.append(char)
        else:
            if not stack or matching[stack[-1]] != char:
                return "INVALID"
            stack.pop()
    
    return "VALID" if not stack else "INVALID"

def main():
    import sys
    s = sys.stdin.read().strip()
    print(is_valid_sequence(s))

if __name__ == "__main__":
    main()

```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
-   Push: `4 5 6`, Times: `0 2 4`
-   Pop: `6 5 4`, Times: `5 6 10`
-   Window: `5` -> `2`
-   Priority: `4`

1.  Push `4` (t=0). Priority. MinP=`4`. Stack `[4]`.
2.  Push `5` (t=2). Non-P. MinP=`4`. Stack `[4, 5]`.
3.  Push `6` (t=4). Non-P. MinP=`4`. Stack `[4, 5, 6]`.
4.  Pop `6` (t=5).
    -   Window: None.
    -   Priority: `6` is Non-P. Check `MinP` below. Stack below has `[4, 5]`. MinP is `4`.
    -   `6 > 4`. **Violation!**
    -   Return `false`.

The example output returns `false` due to the **Time Window** violation: "Value 5 must be popped within 2 time units... popped at time 6".

Note that this test case also violates the priority constraint (element `6` is non-priority and popped while priority element `4` with smaller value is still in the stack). The implementation may detect either constraint violation first depending on the order of checks. Both are valid reasons for returning `false`.

## Proof of Correctness

-   **Structure**: Standard simulation ensures LIFO validity.
-   **Time**: Direct check `pop - push <= W`.
-   **Priority**: The Min-Stack invariant correctly tracks the minimum priority value *currently waiting* in the stack. If we pop a larger non-priority value, we confirm a priority value is still waiting, which violates the ordering rule.

## Interview Extensions

1.  **Multiple Priority Levels**: What if priority is 1-10?
    -   *Hint*: "Higher priority popped before lower priority". Similar logic, check `max_priority_below > current_priority`.
2.  **Online Validation**: Stream of operations.
    -   *Hint*: Same logic works online.

### Common Mistakes

-   **Min Stack Update**: Forgetting to pop from `minPriorityStack` when popping from main stack.
-   **Priority Logic**: Checking `val > minP` for *priority* elements too (only non-priority are restricted).
-   **Time Units**: Mixing up push/pop times.
