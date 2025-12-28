---
id: STR-005
title: Equal Distinct Split
sidebar_label: STR-005 - Equal Distinct Split
tags:
- strings
- prefix-suffix
- hashmap
- medium
difficulty: Medium
difficulty_score: 38
problem_id: STR_EQUAL_DISTINCT_SPLIT__1005
display_id: STR-005
slug: equal-distinct-split
topics:
- String Manipulation
- Prefix-Suffix
- Hashing
---
# STR-005: Equal Distinct Split

## 📋 Problem Summary

**Input**: String `s` (lowercase letters)  
**Output**: Count of split points where left and right substrings have equal distinct character counts  
**Constraints**: `1 <= |s| <= 2 × 10^5`

## 🌍 Real-World Scenario

Data partitioning systems need to split datasets evenly based on diversity metrics. Finding balanced split points ensures both partitions have similar variety for testing/training separation.

## Detailed Explanation

**Split Point**: Position after index i (0-indexed), creating:

- Left: s[0..i]
- Right: s[i+1..n-1]

**Goal**: Count positions where distinct_chars(left) == distinct_chars(right)

**Example**: "ababa"

- After index 1: left="ab" (2 distinct), right="aba" (2 distinct) ✓
- After index 3: left="abab" (2 distinct), right="a" (1 distinct) ✗

## Naive Approach

```
1. For each split position i (0 to n-2):
   a. Count distinct chars in s[0..i]
   b. Count distinct chars in s[i+1..n-1]
   c. If equal, increment counter
```

### Time Complexity: **O(n²)**

- n split points × O(n) to count distinct each time

### Space Complexity: **O(1)**

- Using fixed-size (26) character arrays

## Optimal Approach

**Precompute Suffix Distinct Counts**:

1. Build array `suffixDistinct[i]` = distinct chars in s[i..n-1]
2. Scan left-to-right maintaining `leftDistinct` count
3. At each position, compare `leftDistinct` vs `suffixDistinct[i+1]`

**Algorithm**:

```
1. n = len(s)
2. suffixDistinct = array of size n+1
3. charSet = set()
4. For i from n-1 down to 0:
   charSet.add(s[i])
   suffixDistinct[i] = len(charSet)
5. leftSet = set()
6. count = 0
7. For i from 0 to n-2:
   leftSet.add(s[i])
   if len(leftSet) == suffixDistinct[i+1]:
      count++
8. Return count
```

### Time Complexity

| Phase              | Operations   | Cost           |
| ------------------ | ------------ | -------------- |
| Build suffix array | n iterations | O(n)           |
| Left scan          | n iterations | O(n)           |
| Set operations     | add/size     | O(1) amortized |
| **Total**          |              | **O(n)**       |

### Space Complexity

| Component            | Space        | Justification                |
| -------------------- | ------------ | ---------------------------- |
| suffixDistinct array | O(n)         | Stores n+1 integers          |
| leftSet              | O(26) = O(1) | At most 26 lowercase letters |
| charSet              | O(26) = O(1) | Temporary for suffix build   |
| **Total**            |              | **O(n)**                     |

---

## 🧪 Test Case Walkthrough (Dry Run)

### Example: "ababa"

**Step 1: Build suffix distinct array**

```
String:  a  b  a  b  a
Index:   0  1  2  3  4

Building from right to left:

Index 4: charSet = {a}
  suffixDistinct[4] = 1

Index 3: charSet = {a, b}
  suffixDistinct[3] = 2

Index 2: charSet = {a, b}
  suffixDistinct[2] = 2

Index 1: charSet = {a, b}
  suffixDistinct[1] = 2

Index 0: charSet = {a, b}
  suffixDistinct[0] = 2

suffixDistinct = [2, 2, 2, 2, 1, 0]
                  0  1  2  3  4  5
```

**Visual representation:**

```
Index:    0  1  2  3  4
String:   a  b  a  b  a
Suffix:  [2][2][2][2][1][0]
          │  │  │  │  │  └─ (empty)
          │  │  │  │  └──── "a" → 1 distinct
          │  │  │  └─────── "ba" → 2 distinct
          │  │  └────────── "aba" → 2 distinct
          │  └───────────── "baba" → 2 distinct
          └──────────────── "ababa" → 2 distinct
```

**Step 2: Scan left and compare**

```
Split after index 0:
  Left: "a" → leftSet = {a} → 1 distinct
  Right: suffixDistinct[1] = 2 distinct
  1 ≠ 2 ✗

Split after index 1:
  Left: "ab" → leftSet = {a, b} → 2 distinct
  Right: suffixDistinct[2] = 2 distinct
  2 = 2 ✓ COUNT = 1

Split after index 2:
  Left: "aba" → leftSet = {a, b} → 2 distinct
  Right: suffixDistinct[3] = 2 distinct
  2 = 2 ✓ COUNT = 2

Split after index 3:
  Left: "abab" → leftSet = {a, b} → 2 distinct
  Right: suffixDistinct[4] = 1 distinct
  2 ≠ 1 ✗
```

**Final count: 2 ✓**

**Visual summary:**

```
Valid splits:

  a b | a b a
  └─┘   └───┘
   2      2    ✓

  a b a | b a
  └───┘   └─┘
    2      2   ✓
```

---

### Example: "aa"

**Step 1: Build suffix distinct**

```
String:  a  a
Index:   0  1

Index 1: charSet = {a}
  suffixDistinct[1] = 1

Index 0: charSet = {a}
  suffixDistinct[0] = 1

suffixDistinct = [1, 1, 0]
                  0  1  2
```

**Step 2: Scan left**

```
Split after index 0:
  Left: "a" → leftSet = {a} → 1 distinct
  Right: suffixDistinct[1] = 1 distinct
  1 = 1 ✓ COUNT = 1
```

**Final count: 1 ✓**

---

### Example: "abcdefghij"

**Step 1: Suffix distinct (partial)**

```
All characters unique!

Index 9: {j} → 1
Index 8: {i,j} → 2
Index 7: {h,i,j} → 3
Index 6: {g,h,i,j} → 4
...
Index 0: {a,b,c,d,e,f,g,h,i,j} → 10

suffixDistinct = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```

**Step 2: Scan left**

```
Split 0: left={a}=1, right=9 → 1≠9 ✗
Split 1: left={a,b}=2, right=8 → 2≠8 ✗
Split 2: left={a,b,c}=3, right=7 → 3≠7 ✗
Split 3: left={a,b,c,d}=4, right=6 → 4≠6 ✗
Split 4: left={a,b,c,d,e}=5, right=5 → 5=5 ✓
Split 5: left={a,b,c,d,e,f}=6, right=4 → 6≠4 ✗
...
```

**Valid split:**

```
  a b c d e | f g h i j
  └───────┘   └───────┘
      5           5      ✓
```

**Final count: 1 ✓**

---

## 💻 Implementation

### Python

```python
def count_equal_distinct_splits(s: str) -> int:
    n = len(s)
    if n < 2:
        return 0

    # Build suffix distinct counts
    suffix_distinct = [0] * (n + 1)
    char_set = set()
    for i in range(n - 1, -1, -1):
        char_set.add(s[i])
        suffix_distinct[i] = len(char_set)

    # Scan left and compare
    left_set = set()
    count = 0
    for i in range(n - 1):
        left_set.add(s[i])
        if len(left_set) == suffix_distinct[i + 1]:
            count += 1

    return count

def main():
    import sys
    s = sys.stdin.read().strip()
    result = count_equal_distinct_splits(s)
    print(result)

if __name__ == "__main__":
    main()

```

### Java

```java
class Solution {
    public int countEqualDistinctSplits(String s) {
        int n = s.length();
        if (n < 2) return 0;

        // Build suffix distinct counts
        int[] suffixDistinct = new int[n + 1];
        Set<Character> charSet = new HashSet<>();
        for (int i = n - 1; i >= 0; i--) {
            charSet.add(s.charAt(i));
            suffixDistinct[i] = charSet.size();
        }

        // Scan left and compare
        Set<Character> leftSet = new HashSet<>();
        int count = 0;
        for (int i = 0; i < n - 1; i++) {
            leftSet.add(s.charAt(i));
            if (leftSet.size() == suffixDistinct[i + 1]) {
                count++;
            }
        }

        return count;
    }
}
```

### C++

```cpp
class Solution {
public:
    int countEqualDistinctSplits(string s) {
        int n = s.size();
        if (n < 2) return 0;

        // Build suffix distinct counts
        vector<int> suffixDistinct(n + 1, 0);
        unordered_set<char> charSet;
        for (int i = n - 1; i >= 0; i--) {
            charSet.insert(s[i]);
            suffixDistinct[i] = charSet.size();
        }

        // Scan left and compare
        unordered_set<char> leftSet;
        int count = 0;
        for (int i = 0; i < n - 1; i++) {
            leftSet.insert(s[i]);
            if ((int)leftSet.size() == suffixDistinct[i + 1]) {
                count++;
            }
        }

        return count;
    }
};
```

### JavaScript

```javascript
function countEqualDistinctSplits(s) {
  const n = s.length;
  if (n < 2) return 0;

  // Build suffix distinct counts
  const suffixDistinct = new Array(n + 1).fill(0);
  const charSet = new Set();
  for (let i = n - 1; i >= 0; i--) {
    charSet.add(s[i]);
    suffixDistinct[i] = charSet.size;
  }

  // Scan left and compare
  const leftSet = new Set();
  let count = 0;
  for (let i = 0; i < n - 1; i++) {
    leftSet.add(s[i]);
    if (leftSet.size === suffixDistinct[i + 1]) {
      count++;
    }
  }

  return count;
}
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input**: `s = "ababa"`

**Step 1: Build Suffix Distinct Array** (right-to-left)

```
i=4: char='a', set={a}, suffixDistinct[4]=1
i=3: char='b', set={a,b}, suffixDistinct[3]=2
i=2: char='a', set={a,b}, suffixDistinct[2]=2
i=1: char='b', set={a,b}, suffixDistinct[1]=2
i=0: char='a', set={a,b}, suffixDistinct[0]=2

suffixDistinct = [2, 2, 2, 2, 1, 0]
                  ^  ^  ^  ^  ^  ^
                  0  1  2  3  4  5
```

**Step 2: Scan Left and Compare**

```
i=0: s[0]='a', leftSet={a}, size=1, suffix[1]=2 → 1≠2 ✗
i=1: s[1]='b', leftSet={a,b}, size=2, suffix[2]=2 → 2==2 ✓ (count=1)
i=2: s[2]='a', leftSet={a,b}, size=2, suffix[3]=2 → 2==2 ✓ (count=2)
i=3: s[3]='b', leftSet={a,b}, size=2, suffix[4]=1 → 2≠1 ✗
```

**Output**: `2` (splits after indices 1 and 2)

**Verification with problem statement:**

- After index 1: "ab" (left) vs "aba" (right) → both have 2 distinct ✓
- After index 3: "abab" (left) vs "a" (right) → 2 vs 1 distinct ✗

The algorithm correctly identifies valid split points. For "ababa":

- Split after index 1: left=s[0:2]="ab", right=s[2:]="aba" ✓
- Split after index 2: left=s[0:3]="aba", right=s[3:]="ba" → both have 2 distinct ✓

The output is 2 based on indices 1 and 2 being valid split points.

**Output**: `2`

## ⚠️ Common Mistakes to Avoid

1. **Off-By-One in Split**: Ensure correct split point interpretation
2. **Not Precomputing Suffix**: Recomputing each time leads to O(n²)
3. **Wrong Array Size**: suffixDistinct needs size n+1
4. **Forgetting Empty Right**: Don't split at last position (no right part)
5. **Set Size Comparison**: Compare sizes, not set contents

## 💡 Key Takeaways

1. **Precomputation**: Build suffix array once, use many times
2. **Prefix-Suffix Pattern**: Common for split/partition problems
3. **Set for Distinct Counting**: Efficient O(1) add and size operations
4. **Two-Pass Algorithm**: First backward (suffix), then forward (prefix)
5. **Space-Time Tradeoff**: O(n) space saves from O(n²) to O(n) time


## Constraints

- `1 ≤ |s| ≤ 2 × 10^5`
- `s` contains only lowercase English letters