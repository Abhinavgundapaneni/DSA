---
id: STR-006
title: Minimal Unique Rotation
sidebar_label: STR-006 - Minimal Unique Rotation
tags:
- strings
- rotation
- booth-algorithm
- medium
difficulty: Medium
difficulty_score: 42
problem_id: STR_MINIMAL_UNIQUE_ROTATION__1006
display_id: STR-006
slug: minimal-unique-rotation
topics:
- String Manipulation
- Booth Algorithm
- Rotation
---
# STR-006: Minimal Unique Rotation

## 📋 Problem Summary

**Input**: String `s` (lowercase letters)  
**Output**: Lexicographically smallest rotation that differs from original, or original if all rotations equal  
**Constraints**: `1 <= |s| <= 10^5`

## 🌍 Real-World Scenario

Circular data structures (like DNA sequences or circular shift registers) need canonical representations. Finding the minimal rotation ensures consistent identification across different starting positions.

## Detailed Explanation

**Rotation**: Shift characters cyclically. For "abc", rotations are "abc", "bca", "cab"

**Goal**: Among all rotations ≠ original, find the lexicographically smallest

**Special Case**: If all characters identical (e.g., "aaa"), all rotations equal → return original

**Example**: "bba"

- Rotations: "bba" (original), "bab", "abb"
- Excluding original: "bab", "abb"
- Smallest: "abb"

## Naive Approach

```
1. Generate all n rotations
2. Filter out the original
3. Find the lexicographically smallest
```

### Time Complexity: **O(n²)**

- Generating n rotations: O(n²)
- Comparing strings: O(n) per comparison

### Space Complexity: **O(n²)**

- Storing all rotations

## Optimal Approach

**Use Booth's Algorithm + Filter Original**:

Booth's algorithm finds the minimal rotation in O(n) time by analyzing the doubled string.

**Algorithm**:

```
1. Use Booth's algorithm to find minimal rotation index
2. Generate minimal rotation
3. If it equals original:
   - All rotations identical
   - Return original
4. Else:
   - Return minimal rotation
```

**Booth's Algorithm Core**:

```
1. doubled = s + s
2. failure = array of size 2n, initialized to -1
3. k = 0  # minimal rotation start index
4. For j from 1 to 2n-1:
   i = failure[j - k - 1]
   While i != -1 and doubled[j] != doubled[k + i + 1]:
      If doubled[j] < doubled[k + i + 1]:
         k = j - i - 1
      i = failure[i]

   If doubled[j] != doubled[k + i + 1]:
      If doubled[j] < doubled[k + i + 1]:
         k = j
      failure[j - k] = -1
   Else:
      failure[j - k] = i + 1
5. Return k
```

### Time Complexity

| Phase                 | Operations                    | Cost     |
| --------------------- | ----------------------------- | -------- |
| Booth's algorithm     | Linear scan of doubled string | O(n)     |
| Generate rotation     | Substring + concatenation     | O(n)     |
| Compare with original | String equality               | O(n)     |
| **Total**             |                               | **O(n)** |

### Space Complexity

| Component      | Space | Justification   |
| -------------- | ----- | --------------- |
| doubled string | O(n)  | 2n characters   |
| failure array  | O(n)  | 2n integers     |
| Result string  | O(n)  | At most n chars |
| **Total**      |       | **O(n)**        |

## 💻 Implementation

### Python

```python
def minimal_unique_rotation(s: str) -> str:
    n = len(s)

    # Booth's algorithm to find minimal rotation
    def booth_minimal_rotation_index(s):
        s_doubled = s + s
        n = len(s)
        failure = [-1] * (2 * n)
        k = 0  # minimal rotation start index

        for j in range(1, 2 * n):
            i = failure[j - k - 1]
            while i != -1 and s_doubled[j] != s_doubled[k + i + 1]:
                if s_doubled[j] < s_doubled[k + i + 1]:
                    k = j - i - 1
                i = failure[i]

            if s_doubled[j] != s_doubled[k + i + 1]:
                if s_doubled[j] < s_doubled[k + i + 1]:
                    k = j
                failure[j - k] = -1
            else:
                failure[j - k] = i + 1

        return k

    # Find minimal rotation index
    min_idx = booth_minimal_rotation_index(s)
    min_rotation = s[min_idx:] + s[:min_idx]

    # If minimal rotation equals original, all rotations identical
    if min_rotation == s:
        return s
    else:
        return min_rotation

def main():
    import sys
    s = sys.stdin.read().strip()
    result = minimal_unique_rotation(s)
    print(result)

if __name__ == "__main__":
    main()

```

### Java

```java
class Solution {
    public String minimalUniqueRotation(String s) {
        int n = s.length();

        // Booth's algorithm
        int minIdx = boothMinimalRotationIndex(s);
        String minRotation = s.substring(minIdx) + s.substring(0, minIdx);

        // Check if same as original
        if (minRotation.equals(s)) {
            return s;
        } else {
            return minRotation;
        }
    }

    private int boothMinimalRotationIndex(String s) {
        String doubled = s + s;
        int n = s.length();
        int[] failure = new int[2 * n];
        Arrays.fill(failure, -1);
        int k = 0;

        for (int j = 1; j < 2 * n; j++) {
            int i = failure[j - k - 1];
            while (i != -1 && doubled.charAt(j) != doubled.charAt(k + i + 1)) {
                if (doubled.charAt(j) < doubled.charAt(k + i + 1)) {
                    k = j - i - 1;
                }
                i = failure[i];
            }

            if (doubled.charAt(j) != doubled.charAt(k + i + 1)) {
                if (doubled.charAt(j) < doubled.charAt(k + i + 1)) {
                    k = j;
                }
                failure[j - k] = -1;
            } else {
                failure[j - k] = i + 1;
            }
        }

        return k;
    }
}
```

### C++

```cpp
class Solution {
public:
    string minimalUniqueRotation(string s) {
        int n = s.size();

        // Booth's algorithm
        int minIdx = boothMinimalRotationIndex(s);
        string minRotation = s.substr(minIdx) + s.substr(0, minIdx);

        // Check if same as original
        if (minRotation == s) {
            return s;
        } else {
            return minRotation;
        }
    }

private:
    int boothMinimalRotationIndex(const string& s) {
        string doubled = s + s;
        int n = s.size();
        vector<int> failure(2 * n, -1);
        int k = 0;

        for (int j = 1; j < 2 * n; j++) {
            int i = failure[j - k - 1];
            while (i != -1 && doubled[j] != doubled[k + i + 1]) {
                if (doubled[j] < doubled[k + i + 1]) {
                    k = j - i - 1;
                }
                i = failure[i];
            }

            if (doubled[j] != doubled[k + i + 1]) {
                if (doubled[j] < doubled[k + i + 1]) {
                    k = j;
                }
                failure[j - k] = -1;
            } else {
                failure[j - k] = i + 1;
            }
        }

        return k;
    }
};
```

### JavaScript

```javascript
function minimalUniqueRotation(s) {
  const n = s.length;

  // Booth's algorithm
  function boothMinimalRotationIndex(s) {
    const doubled = s + s;
    const n = s.length;
    const failure = new Array(2 * n).fill(-1);
    let k = 0;

    for (let j = 1; j < 2 * n; j++) {
      let i = failure[j - k - 1];
      while (i !== -1 && doubled[j] !== doubled[k + i + 1]) {
        if (doubled[j] < doubled[k + i + 1]) {
          k = j - i - 1;
        }
        i = failure[i];
      }

      if (doubled[j] !== doubled[k + i + 1]) {
        if (doubled[j] < doubled[k + i + 1]) {
          k = j;
        }
        failure[j - k] = -1;
      } else {
        failure[j - k] = i + 1;
      }
    }

    return k;
  }

  const minIdx = boothMinimalRotationIndex(s);
  const minRotation = s.slice(minIdx) + s.slice(0, minIdx);

  // Check if same as original
  if (minRotation === s) {
    return s;
  } else {
    return minRotation;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input**: `s = "bba"`

**Step 1: Apply Booth's Algorithm**

```
doubled = "bbabba"
n = 3
failure = [-1, -1, -1, -1, -1, -1]
k = 0 (minimal rotation start index)

j=1: doubled[1]='b', doubled[k+i+1]=doubled[0]='b' → equal
     failure[1-0]=failure[1]=0

j=2: doubled[2]='a', doubled[k+i+1]=doubled[1]='b' → 'a'<'b'
     k = 2
     failure[2-2]=failure[0]=-1

j=3: doubled[3]='b', k=2, doubled[k+i+1]=doubled[2]='a' → 'b'>'a', no update
     i = failure[0] = -1
     failure[3-2]=failure[1]=-1

j=4: doubled[4]='b', k=2, doubled[k+i+1]=doubled[2]='a' → 'b'>'a'
     i = -1
     failure[4-2]=failure[2]=-1

j=5: doubled[5]='a', k=2, doubled[k+i+1]=doubled[2]='a' → equal
     failure[5-2]=failure[3]=0

Result: k = 2
```

**Step 2: Generate Minimal Rotation**

```
minIdx = 2
minRotation = s[2:] + s[:2] = "a" + "bb" = "abb"
```

**Step 3: Compare with Original**

```
minRotation = "abb"
original = "bba"
"abb" ≠ "bba" → return "abb"
```

**Output**: `"abb"`

## ⚠️ Common Mistakes to Avoid

1. **Generating All Rotations**: O(n²) approach when O(n) exists
2. **Not Handling Identical Chars**: Forgetting special case where all chars same
3. **Wrong Booth Implementation**: Failure array logic is subtle
4. **String Comparison Overhead**: Using multiple comparisons instead of single check
5. **Off-By-One Errors**: Index calculations in Booth's algorithm

## 💡 Key Takeaways

1. **Booth's Algorithm**: Elegant O(n) solution for minimal rotation
2. **Doubled String Trick**: s+s contains all rotations as substrings
3. **Failure Function**: Adapted from KMP for rotation finding
4. **Special Case Handling**: All-identical characters need explicit check
5. **Linear Time String Algorithms**: Often exist for circular/rotation problems


## Constraints

- `1 ≤ |s| ≤ 10^5`
- `s` contains only lowercase English letters