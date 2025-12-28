---
id: STR-002
title: Lab Code Palindrome Rotate
sidebar_label: STR-002 - Palindrome Rotate
tags:
- strings
- palindrome
- frequency
- easy
difficulty: Easy
difficulty_score: 28
problem_id: STR_LAB_CODE_PALINDROME_ROTATE__1002
display_id: STR-002
slug: lab-code-palindrome-rotate
topics:
- String Manipulation
- Palindromes
- Frequency Analysis
---
# STR-002: Lab Code Palindrome Rotate

## 📋 Problem Summary

**Input**: String `s` of lowercase letters  
**Output**: Boolean - whether some rotation of `s` can form a palindrome  
**Constraints**: `1 <= |s| <= 10^5`

## 🌍 Real-World Scenario

Laboratory equipment codes are circularly printed on rotating labels. A scanner needs to detect if any rotation creates a valid palindromic code for verification.

## Detailed Explanation

**Key Insight**: Rotation doesn't change character frequencies. A string can form a palindrome if and only if at most one character has an odd frequency.

**Why?**: In a palindrome of length n:

- If n is even: all characters must pair up (even frequencies)
- If n is odd: all except one character (the middle) must pair up

Rotation merely rearranges characters—it cannot change how many times each character appears.

## Naive Approach

```
1. Generate all n rotations of string s
2. For each rotation, check if it's a palindrome
3. Return true if any rotation is palindromic
```

### Time Complexity

| Phase              | Operations              | Cost      |
| ------------------ | ----------------------- | --------- |
| Generate rotations | n rotations             | O(n²)     |
| Check palindrome   | n checks × n comparison | O(n²)     |
| **Total**          |                         | **O(n³)** |

### Space Complexity: O(n) for storing rotations

## 🧪 Test Case Walkthrough (Dry Run)

### Example: "aab"

**Step 1: Generate all rotations**

```
Original: "aab"

Rotation 0: "aab"  →  a │ a │ b
Rotation 1: "aba"  →  a │ b │ a  ← PALINDROME! ✓
Rotation 2: "baa"  →  b │ a │ a
```

**Visual Check:**

```
"aba" reversed: "aba" → Same! It's a palindrome.
```

**Result:** `true` (rotation 1 is a palindrome)

---

### Example: "aabbcc"

**Step 1: Generate all rotations**

```
Rotation 0: "aabbcc"  →  not palindrome
Rotation 1: "abbcca"  →  not palindrome
Rotation 2: "bbccaa"  →  not palindrome
Rotation 3: "bccaab"  →  not palindrome
Rotation 4: "ccaabb"  →  not palindrome
Rotation 5: "caabbc"  →  not palindrome
```

**Visualization of rotation process:**

```
Step 0:  [a][a][b][b][c][c]  ← start
Step 1:  [a][b][b][c][c][a]  ← move first to end
Step 2:  [b][b][c][c][a][a]  ← move first to end
Step 3:  [b][c][c][a][a][b]  ← move first to end
...
None form palindromes!
```

**Result:** `false` (no rotation is a palindrome)

---

## Optimal Approach

**Direct Rotation Checking**:

1. Generate all n rotations of string s
2. For each rotation, check if it's a palindrome
3. Return true if any rotation is palindromic

**Algorithm**:

```
1. freq = HashMap<Character, Integer>()
2. For each char c in s:
   freq[c]++
3. oddCount = 0
4. For each count in freq.values():
   if count % 2 == 1:
      oddCount++
5. Return oddCount <= 1
```

### Time Complexity

| Phase                 | Operations        | Cost     |
| --------------------- | ----------------- | -------- |
| Count frequencies     | n chars           | O(n)     |
| Count odd frequencies | ≤ 26 unique chars | O(1)     |
| **Total**             |                   | **O(n)** |

**Why This Complexity?**: Single pass for counting, constant iteration over alphabet.

### Space Complexity

| Component     | Space | Justification                |
| ------------- | ----- | ---------------------------- |
| Frequency map | O(1)  | At most 26 lowercase letters |
| **Total**     |       | **O(1)**                     |

## 💻 Implementation

### Java

```java
class Solution {
    public boolean canRotateToPalindrome(String s) {
        if (s == null || s.length() <= 1) return true;

        // Count character frequencies
        Map<Character, Integer> freq = new HashMap<>();
        for (char c : s.toCharArray()) {
            freq.put(c, freq.getOrDefault(c, 0) + 1);
        }

        // Count characters with odd frequency
        int oddCount = 0;
        for (int count : freq.values()) {
            if (count % 2 == 1) {
                oddCount++;
            }
        }

        return oddCount <= 1;
    }
}
```

### Python

```python
def can_rotate_to_palindrome(s: str) -> bool:
    if not s or len(s) <= 1:
        return True

    # Check all rotations
    n = len(s)
    for i in range(n):
        rotation = s[i:] + s[:i]
        if rotation == rotation[::-1]:
            return True

    return False

def main():
    import sys
    s = sys.stdin.read().strip()
    result = can_rotate_to_palindrome(s)
    print("true" if result else "false")

if __name__ == "__main__":
    main()

```

### C++

```cpp
class Solution {
public:
    bool canRotateToPalindrome(string s) {
        if (s.empty() || s.size() <= 1) return true;

        // Count character frequencies
        unordered_map<char, int> freq;
        for (char c : s) {
            freq[c]++;
        }

        // Count characters with odd frequency
        int oddCount = 0;
        for (auto& [c, count] : freq) {
            if (count % 2 == 1) {
                oddCount++;
            }
        }

        return oddCount <= 1;
    }
};
```

### JavaScript

```javascript
function canRotateToPalindrome(s) {
  if (!s || s.length <= 1) return true;

  // Count character frequencies
  const freq = new Map();
  for (let c of s) {
    freq.set(c, (freq.get(c) || 0) + 1);
  }

  // Count characters with odd frequency
  let oddCount = 0;
  for (let count of freq.values()) {
    if (count % 2 === 1) {
      oddCount++;
    }
  }

  return oddCount <= 1;
}
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input**: `s = "aab"`

**Step 1: Count Frequencies**

```
char | frequency
-----|----------
'a'  | 2
'b'  | 1
```

**Step 2: Count Odd Frequencies**

```
'a': 2 is even → skip
'b': 1 is odd → oddCount = 1
```

**Step 3: Check Condition**

```
oddCount = 1
1 <= 1 → true
```

**Verification**:

- Original: "aab" → not palindrome
- Rotation "aba" → palindrome ✓

**Output**: `true`

## ⚠️ Common Mistakes to Avoid

1. **Generating Rotations**: Unnecessary—use frequency check instead
2. **Forgetting Empty/Single Char**: These are always valid palindromes
3. **Wrong Odd Count Threshold**: Must be `<= 1`, not `== 0`
4. **Case Sensitivity**: Problem specifies lowercase, but be aware in variants
5. **Not Handling Duplicates**: Use frequency map, not just unique chars

## ⏱️ Complexity Analysis

### Time Complexity: **O(n)**

- Counting frequencies: O(n)
- Checking odd counts: O(26) = O(1) for lowercase letters

### Space Complexity: **O(1)**

- Frequency map: at most 26 entries for lowercase letters

## 💡 Key Takeaways

1. **Rotation Invariance**: Character frequencies remain constant across rotations
2. **Palindrome Property**: At most one character can have odd frequency
3. **Frequency Analysis**: Often more efficient than generating permutations/rotations
4. **Early Termination**: Could stop counting odds after finding 2
5. **Mathematical Insight**: Understanding properties avoids brute-force


## Constraints

- `1 ≤ |s| ≤ 2 × 10^5`
- `s` contains only lowercase English letters