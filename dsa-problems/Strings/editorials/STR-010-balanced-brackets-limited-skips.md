---
id: STR-010
title: Balanced Brackets With Limited Skips
sidebar_label: STR-010 - Balanced Brackets With Limited Skips
tags:
- strings
- stack
- greedy
- parentheses
- medium
difficulty: Medium
difficulty_score: 37
problem_id: STR_BALANCED_BRACKETS_LIMITED_SKIPS__1010
display_id: STR-010
slug: balanced-brackets-limited-skips
topics:
- String Manipulation
- Stack
- Greedy
---
# STR-010: Balanced Brackets With Limited Skips

## 📋 Problem Summary

**Input**: String `s` (contains '(' and ')'), integer `k` (skip tokens)  
**Output**: `true` if string can be balanced using ≤ `k` skips, `false` otherwise  
**Constraints**: `1 <= |s| <= 2 × 10^5`, `0 <= k <= |s|`

## 🌍 Real-World Scenario

Code parsers with error recovery can skip malformed tokens. Checking if code can be balanced within a skip budget determines if auto-correction is feasible.

## Detailed Explanation

**Balanced**: Every '(' has matching ')' after it, and vice versa

**Skip Token**: Can remove one parenthesis from consideration

**Goal**: Determine if using at most `k` skips makes string balanced

**Example**: `s="())("`, `k=2`

- Original: unbalanced (extra ')' at index 2, unmatched '(' at index 3)
- Skip ')' at index 2: "()(" still unbalanced
- Skip '(' at index 3: "()" balanced ✓
- Total skips: 2 <= 2 ✓

## Naive Approach

```
1. Try all combinations of skipping positions
2. For each combination:
   a. Remove skipped characters
   b. Check if balanced
```

### Time Complexity: **O(2^n × n)**

- Exponential combinations

### Space Complexity: **O(n)**

## Optimal Approach

**Greedy Balance Tracking**:

Track running balance:

- '(' → balance++
- ')' → balance--

**When balance < 0**: Need to skip a ')' to prevent underflow

**At end**: Remaining positive balance needs skips to remove unmatched '('

**Algorithm**:

```
1. balance = 0
2. skips_used = 0
3. For each char in s:
   a. If char == '(':
      balance++
   b. Else (char == ')'):
      balance--
      If balance < 0:
         skips_used++
         balance = 0  (skip this ')')
4. If skips_used + balance <= k:
   Return true
5. Else:
   Return false
```

**Key Insight**:

- Negative balance requires immediate skip
- Positive balance at end can be handled by skipping trailing '('

### Time Complexity

| Phase           | Operations     | Cost     |
| --------------- | -------------- | -------- |
| Single scan     | Iterate string | O(n)     |
| Balance updates | O(1) per char  | O(n)     |
| **Total**       |                | **O(n)** |

### Space Complexity

| Component | Space | Justification       |
| --------- | ----- | ------------------- |
| Variables | O(1)  | balance, skips_used |
| **Total** |       | **O(1)**            |

## 💻 Implementation

### Python

```python
def can_balance_with_skips(s: str, k: int) -> bool:
    balance = 0
    skips_used = 0

    for char in s:
        if char == '(':
            balance += 1
        else:  # char == ')'
            balance -= 1
            if balance < 0:
                # Need to skip this ')'
                skips_used += 1
                balance = 0

    # Remaining balance are unmatched '(' - need skips for them
    total_skips_needed = skips_used + balance
    return total_skips_needed <= k

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    s = lines[0]
    k = int(lines[1])
    result = can_balance_with_skips(s, k)
    print("true" if result else "false")

if __name__ == "__main__":
    main()

```

### Java

```java
class Solution {
    public boolean canBalanceWithSkips(String s, int k) {
        int balance = 0;
        int skipsUsed = 0;

        for (char c : s.toCharArray()) {
            if (c == '(') {
                balance++;
            } else {  // c == ')'
                balance--;
                if (balance < 0) {
                    // Need to skip this ')'
                    skipsUsed++;
                    balance = 0;
                }
            }
        }

        // Remaining balance are unmatched '('
        int totalSkipsNeeded = skipsUsed + balance;
        return totalSkipsNeeded <= k;
    }
}
```

### C++

```cpp
class Solution {
public:
    bool canBalanceWithSkips(string s, int k) {
        int balance = 0;
        int skipsUsed = 0;

        for (char c : s) {
            if (c == '(') {
                balance++;
            } else {  // c == ')'
                balance--;
                if (balance < 0) {
                    // Need to skip this ')'
                    skipsUsed++;
                    balance = 0;
                }
            }
        }

        // Remaining balance are unmatched '('
        int totalSkipsNeeded = skipsUsed + balance;
        return totalSkipsNeeded <= k;
    }
};
```

### JavaScript

```javascript
function canBalanceWithSkips(s, k) {
  let balance = 0;
  let skipsUsed = 0;

  for (let char of s) {
    if (char === "(") {
      balance++;
    } else {
      // char === ')'
      balance--;
      if (balance < 0) {
        // Need to skip this ')'
        skipsUsed++;
        balance = 0;
      }
    }
  }

  // Remaining balance are unmatched '('
  const totalSkipsNeeded = skipsUsed + balance;
  return totalSkipsNeeded <= k;
}
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input**: `s="())("`, `k=2`

**Execution**:

```
i=0: char='(', balance=1
i=1: char=')', balance=0
i=2: char=')', balance=-1 < 0 → skip, skipsUsed=1, balance=0
i=3: char='(', balance=1

End: balance=1, skipsUsed=1
totalSkipsNeeded = 1 + 1 = 2
2 <= 2 → true
```

**Output**: `true`

**Verification**:

- Skip ')' at index 2
- Skip '(' at index 3
- Remaining: "()" → balanced ✓

## 🧪 Walkthrough: Insufficient Skips

**Input**: `s="((("`, `k=1`

```
i=0: char='(', balance=1
i=1: char='(', balance=2
i=2: char='(', balance=3

End: balance=3, skipsUsed=0
totalSkipsNeeded = 0 + 3 = 3
3 > 1 → false
```

**Output**: `false`

**Reasoning**: Need to skip all 3 '(' but only have 1 skip token

## 🧪 Walkthrough: Exact Skips

**Input**: `s=")))(("`, `k=5`

```
i=0: char=')', balance=-1 → skip, skipsUsed=1, balance=0
i=1: char=')', balance=-1 → skip, skipsUsed=2, balance=0
i=2: char=')', balance=-1 → skip, skipsUsed=3, balance=0
i=3: char='(', balance=1
i=4: char='(', balance=2

End: balance=2, skipsUsed=3
totalSkipsNeeded = 3 + 2 = 5
5 <= 5 → true
```

**Output**: `true`

## ⚠️ Common Mistakes to Avoid

1. **Not Resetting Balance**: After skip, reset balance to 0, not -1
2. **Forgetting End Balance**: Unmatched '(' at end also need skips
3. **Using Stack**: Simple counter suffices, no need for stack
4. **Double Counting**: Don't skip same character twice
5. **Wrong Skip Count**: Total = immediate skips + remaining balance

## 💡 Key Takeaways

1. **Greedy Strategy**: Skip ')' immediately when balance goes negative
2. **Linear Time**: Single pass with O(1) space
3. **Balance Tracking**: Simple counter instead of stack
4. **Two Types of Skips**: Immediate (for ')') and deferred (for '(')
5. **No Backtracking**: Greedy choice is always optimal for this problem


## Constraints

- `1 ≤ |s| ≤ 2 × 10^5`
- `0 ≤ k ≤ |s|`
- `s` contains only '(' and ')'