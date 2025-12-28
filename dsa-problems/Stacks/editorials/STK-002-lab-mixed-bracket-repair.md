---
title: Lab Mixed Bracket Repair
slug: lab-mixed-bracket-repair
difficulty: Easy
difficulty_score: 34
tags:
- Stack
- Bracket Matching
- Greedy
problem_id: STK_LAB_MIXED_BRACKET_REPAIR__7391
display_id: STK-002
topics:
- Stack
- Brackets
- Greedy
---
# Lab Mixed Bracket Repair - Editorial

## Problem Summary

You are given a string containing brackets `()[]{}` and wildcards `?`. Each `?` can be replaced by any single bracket character. Determine if it is possible to replace all `?`s such that the resulting string is balanced and well-nested.


## Constraints

- `1 <= |s| <= 100000`
- `s` contains only `()[]{}` and `?`
## Real-World Scenario

Imagine you are a **Code Linter** analyzing a corrupted source code file.
-   Some characters have been corrupted and appear as `?`.
-   You know the code relies heavily on nested structures (functions `{}`, arrays `[]`, expressions `()`).
-   You want to check if there is *any* way to interpret the corrupted characters so that the code's structure remains valid.
-   If no such interpretation exists, you flag the file as "Irreparably Broken".

## Problem Exploration

### 1. The Power of Wildcards
-   A `?` is extremely flexible. It can become any opener `(`, `[`, `{` or any closer `)`, `]`, `}`.
-   This flexibility suggests a greedy approach. We should use `?` to fix immediate problems if possible, but save it for later if not needed immediately.

### 2. Constraints
-   The string length `N` is up to `100,000`.
-   We need an `O(N)` solution. Trying all replacements (`6^count(?)`) is impossible.

### 3. Two-Pass Greedy Strategy
-   With multiple types, we must ensure specific openers match specific closers (e.g., `(` must match `)`).
-   **Key Insight**: We should prioritize matching actual brackets with each other. If a specific opener (like `(`) matches a specific closer (like `)`), we should pair them up. If they mismatch (like `[` and `)`), we *must* use a `?` to resolve the conflict (by turning `?` into the required opener).

## Approaches

### Approach 1: Two-Stack Greedy
-   We use two stacks:
    1.  `LeftStack`: Stores indices of open brackets `(`, `[`, `{`.
    2.  `StarStack`: Stores indices of wildcards `?`.
-   **Pass 1 (Left to Right)**: Handle Closers.
    -   Iterate through the string.
    -   If char is `(`, `[`, `{`: Push index to `LeftStack`.
    -   If char is `?`: Push index to `StarStack`.
    -   If char is `)`, `]`, `}`:
        -   Check `LeftStack`. If the top matches (e.g., `(` for `)`), pop `LeftStack`. (Prioritize exact match).
        -   If `LeftStack` top mismatches or is empty, check `StarStack`. If available, pop `StarStack`. (Use `?` as the matching opener).
        -   If neither is available/valid, return `false`.
-   **Pass 2 (Cleanup)**: Handle Remaining Openers.
    -   After Pass 1, we might have unmatched openers in `LeftStack` and unused `?` in `StarStack`.
    -   We need to pair each remaining opener with a `?` that appears *after* it (to act as a closer).
    -   Iterate while `LeftStack` is not empty:
        -   If `StarStack` is empty, return `false`.
        -   If `LeftStack.top() < StarStack.top()`: Pop both. (Valid pair).
        -   Else: Return `false` (Wildcard is before opener, cannot close it).
-   **Final Check**:
    -   The remaining `?`s in `StarStack` must be paired with each other. Since `?` can be anything, any even number of `?`s can form valid pairs (e.g., `()`, `[]`).
    -   Return `StarStack.size() % 2 == 0`.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public boolean canRepair(String s) {
        int n = s.length();
        if (n % 2 != 0) return false;
        
        Stack<Integer> leftStack = new Stack<>();
        Stack<Integer> starStack = new Stack<>();
        
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            
            if (c == '(' || c == '[' || c == '{') {
                leftStack.push(i);
            } else if (c == '?') {
                starStack.push(i);
            } else {
                // Closer
                if (!leftStack.isEmpty() && isMatch(s.charAt(leftStack.peek()), c)) {
                    leftStack.pop();
                } else if (!starStack.isEmpty()) {
                    starStack.pop();
                } else {
                    return false;
                }
            }
        }
        
        while (!leftStack.isEmpty()) {
            if (starStack.isEmpty()) return false;
            if (leftStack.peek() < starStack.peek()) {
                leftStack.pop();
                starStack.pop();
            } else {
                return false;
            }
        }
        
        return starStack.size() % 2 == 0;
    }
    
    private boolean isMatch(char open, char close) {
        return (open == '(' && close == ')') ||
               (open == '[' && close == ']') ||
               (open == '{' && close == '}');
    }
}
```

### Python

```python
def can_repair(s: str) -> bool:
    """Check if wildcards can make brackets balanced"""
    stack = []
    stars = []
    
    pairs = {')': '(', ']': '[', '}': '{'}
    
    for i, c in enumerate(s):
        if c in '([{':
            stack.append((c, i))
        elif c == '?':
            stars.append(i)
        else:
            if stack and stack[-1][0] == pairs[c]:
                stack.pop()
            elif stars:
                stars.pop()
            else:
                return False
    
    while stack and stars:
        if stack[-1][1] < stars[-1]:
            stack.pop()
            stars.pop()
        else:
            break
    
    return not stack

def main():
    import sys
    s = sys.stdin.read().strip()
    result = can_repair(s)
    print("true" if result else "false")

if __name__ == "__main__":
    main()

```

### C++

```cpp
#include <string>
#include <stack>
#include <vector>

using namespace std;

class Solution {
    bool isMatch(char open, char close) {
        return (open == '(' && close == ')') ||
               (open == '[' && close == ']') ||
               (open == '{' && close == '}');
    }

public:
    bool canRepair(const string& s) {
        int n = s.length();
        if (n % 2 != 0) return false;
        
        vector<int> leftStack;
        vector<int> starStack;
        
        for (int i = 0; i < n; i++) {
            char c = s[i];
            if (c == '(' || c == '[' || c == '{') {
                leftStack.push_back(i);
            } else if (c == '?') {
                starStack.push_back(i);
            } else {
                // Closer
                if (!leftStack.empty() && isMatch(s[leftStack.back()], c)) {
                    leftStack.pop_back();
                } else if (!starStack.empty()) {
                    starStack.pop_back();
                } else {
                    return false;
                }
            }
        }
        
        while (!leftStack.empty()) {
            if (starStack.empty()) return false;
            if (leftStack.back() < starStack.back()) {
                leftStack.pop_back();
                starStack.pop_back();
            } else {
                return false;
            }
        }
        
        return starStack.size() % 2 == 0;
    }
};
```

### JavaScript

```javascript
class Solution {
  canRepair(s) {
    const n = s.length;
    if (n % 2 !== 0) return false;
    
    const leftStack = [];
    const starStack = [];
    
    const isMatch = (open, close) => {
      return (open === '(' && close === ')') ||
             (open === '[' && close === ']') ||
             (open === '{' && close === '}');
    };
    
    for (let i = 0; i < n; i++) {
      const c = s[i];
      if (c === '(' || c === '[' || c === '{') {
        leftStack.push(i);
      } else if (c === '?') {
        starStack.push(i);
      } else {
        // Closer
        if (leftStack.length > 0 && isMatch(s[leftStack[leftStack.length - 1]], c)) {
          leftStack.pop();
        } else if (starStack.length > 0) {
          starStack.pop();
        } else {
          return false;
        }
      }
    }
    
    while (leftStack.length > 0) {
      if (starStack.length === 0) return false;
      if (leftStack[leftStack.length - 1] < starStack[starStack.length - 1]) {
        leftStack.pop();
        starStack.pop();
      } else {
        return false;
      }
    }
    
    return starStack.length % 2 === 0;
  }
}
```

### Python

```python

def min_deletions(s):
    stack = []
    deletions = 0
    
    for char in s:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if stack:
                stack.pop()
            else:
                deletions += 1
    
    deletions += len(stack)
    return deletions

def main():
    import sys
    s = sys.stdin.read().strip()
    print(min_deletions(s))

if __name__ == "__main__":
    main()

```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:** `(?[?])??`

1.  **Pass 1**:
    -   `(` (0) -> `LeftStack: [0]`
    -   `?` (1) -> `StarStack: [1]`
    -   `[` (2) -> `LeftStack: [0, 2]`
    -   `?` (3) -> `StarStack: [1, 3]`
    -   `]` (4) -> Matches `[` (2). Pop `LeftStack`. `LeftStack: [0]`.
    -   `)` (5) -> Matches `(` (0). Pop `LeftStack`. `LeftStack: []`.
    -   `?` (6) -> `StarStack: [1, 3, 6]`
    -   `?` (7) -> `StarStack: [1, 3, 6, 7]`
2.  **Pass 2**:
    -   `LeftStack` is empty. No matching needed.
3.  **Final Check**:
    -   `StarStack` size is 4. Even.
    -   Return `true`.

## Proof of Correctness

-   **Priority**: By prioritizing exact matches in Pass 1, we ensure that specific constraints are met whenever possible. Using a `?` to match a closer is a fallback that consumes a wildcard (making it an opener).
-   **Flexibility**: In Pass 2, we use remaining `?`s as closers. The index check `left < star` ensures the `?` appears after the opener, preserving valid nesting order.
-   **Parity**: The final check ensures remaining `?`s can form pairs among themselves.

## Interview Extensions

1.  **Min/Max Depth**: Can you calculate the minimum and maximum possible nesting depth?
2.  **Construct String**: Can you output *one* valid string instead of just boolean?
    -   *Hint*: Track which `?` was used as opener/closer and fill accordingly.

### Common Mistakes

-   **Ignoring Types**: Treating `(` and `]` as a match because "one is open, one is close".
-   **Greedy Mismatch**: Using a `?` to match a closer when a matching opener was available. This wastes the `?` and might leave the opener unmatched.
-   **Order in Pass 2**: Forgetting to check indices. A `?` before an opener cannot close it.
