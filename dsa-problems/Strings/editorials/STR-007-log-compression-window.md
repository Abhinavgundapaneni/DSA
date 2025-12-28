---
id: STR-007
title: Log Compression With Window
sidebar_label: STR-007 - Log Compression With Window
tags:
- strings
- compression
- run-length-encoding
- medium
difficulty: Medium
difficulty_score: 35
problem_id: STR_LOG_COMPRESSION_WINDOW__1007
display_id: STR-007
slug: log-compression-window
topics:
- String Manipulation
- Run-Length Encoding
---
# STR-007: Log Compression With Window

## 📋 Problem Summary

**Input**: String `s`, integer `w` (window threshold)  
**Output**: Compressed string where runs of length ≥ `w` are replaced with char + count  
**Constraints**: `1 <= |s| <= 2 × 10^5`, `1 <= w <= 10^5`

## 🌍 Real-World Scenario

Log file compression needs adaptive encoding - only compress runs above a threshold to avoid overhead for short runs. This balances compression ratio with encoding efficiency.

## Detailed Explanation

**Run-Length Encoding**: Replace consecutive identical characters with char + count

**Threshold-Based**: Only compress runs of length ≥ `w`

**Example**: `s="aaabbbbcc"`, `w=3`

- "aaa" (length 3) → "a3" ✓
- "bbbb" (length 4) → "b4" ✓
- "cc" (length 2 < 3) → "cc" ✗ (keep as-is)
- Output: "a3b4cc"

## Naive Approach

```
1. For each position i:
   a. Scan forward to find run length
   b. If >= w, append char + count
   c. Else, append characters individually
   d. Skip processed characters
```

### Time Complexity: **O(n)**

- Single pass through string
- Each character processed once

### Space Complexity: **O(n)**

- Result string

**Note**: Naive approach is actually optimal here!

## Optimal Approach

**Single-Pass Run Detection**:

```
1. i = 0
2. result = []
3. While i < n:
   a. start = i
   b. char = s[i]
   c. While i < n and s[i] == char:
      i++
   d. run_length = i - start
   e. If run_length >= w:
      result.append(char + str(run_length))
   f. Else:
      result.append(char * run_length)
4. Return join(result)
```

### Time Complexity

| Phase            | Operations                  | Cost             |
| ---------------- | --------------------------- | ---------------- |
| Single pass      | Iterate each character once | O(n)             |
| Count conversion | Integer to string           | O(log n) per run |
| String building  | Concatenation               | O(n) total       |
| **Total**        |                             | **O(n)**         |

### Space Complexity

| Component    | Space    | Justification                |
| ------------ | -------- | ---------------------------- |
| Result list  | O(n)     | Worst case: all uncompressed |
| Temp strings | O(log n) | Count strings                |
| **Total**    |          | **O(n)**                     |

## 💻 Implementation

### Python

```python
def compress_with_window(s: str, w: int) -> str:
    if not s:
        return ""

    result = []
    i = 0
    n = len(s)

    while i < n:
        start = i
        char = s[i]

        # Count consecutive occurrences
        while i < n and s[i] == char:
            i += 1

        run_length = i - start

        # Compress if >= threshold AND it actually saves space
        if run_length >= w:
            compressed = char + str(run_length)
            original = char * run_length
            if len(compressed) < len(original):
                result.append(compressed)
            else:
                result.append(original)
        else:
            result.append(char * run_length)

    return ''.join(result)

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    s = lines[0]
    w = int(lines[1])
    result = compress_with_window(s, w)
    print(result)

if __name__ == "__main__":
    main()

```

### Java

```java
class Solution {
    public String compressWithWindow(String s, int w) {
        if (s == null || s.isEmpty()) {
            return "";
        }

        StringBuilder result = new StringBuilder();
        int i = 0;
        int n = s.length();

        while (i < n) {
            int start = i;
            char ch = s.charAt(i);

            // Count consecutive occurrences
            while (i < n && s.charAt(i) == ch) {
                i++;
            }

            int runLength = i - start;

            // Compress if >= threshold
            if (runLength >= w) {
                result.append(ch).append(runLength);
            } else {
                for (int j = 0; j < runLength; j++) {
                    result.append(ch);
                }
            }
        }

        return result.toString();
    }
}
```

### C++

```cpp
class Solution {
public:
    string compressWithWindow(string s, int w) {
        if (s.empty()) {
            return "";
        }

        string result;
        int i = 0;
        int n = s.size();

        while (i < n) {
            int start = i;
            char ch = s[i];

            // Count consecutive occurrences
            while (i < n && s[i] == ch) {
                i++;
            }

            int runLength = i - start;

            // Compress if >= threshold
            if (runLength >= w) {
                result += ch;
                result += to_string(runLength);
            } else {
                result.append(runLength, ch);
            }
        }

        return result;
    }
};
```

### JavaScript

```javascript
function compressWithWindow(s, w) {
  if (!s) {
    return "";
  }

  const result = [];
  let i = 0;
  const n = s.length;

  while (i < n) {
    const start = i;
    const char = s[i];

    // Count consecutive occurrences
    while (i < n && s[i] === char) {
      i++;
    }

    const runLength = i - start;

    // Compress if >= threshold
    if (runLength >= w) {
      result.push(char + runLength);
    } else {
      result.push(char.repeat(runLength));
    }
  }

  return result.join("");
}
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input**: `s = "aaabbbbcc"`, `w = 3`

**Execution**:

```
i=0: start=0, char='a'
     Scan: i=0,1,2 → i=3
     runLength = 3 - 0 = 3
     3 >= 3 → compress → result=["a3"]

i=3: start=3, char='b'
     Scan: i=3,4,5,6 → i=7
     runLength = 7 - 3 = 4
     4 >= 3 → compress → result=["a3", "b4"]

i=7: start=7, char='c'
     Scan: i=7,8 → i=9
     runLength = 9 - 7 = 2
     2 < 3 → keep as-is → result=["a3", "b4", "cc"]

i=9: exit loop

Final: join(result) = "a3b4cc"
```

**Output**: `"a3b4cc"`

## 🧪 Walkthrough: Edge Case

**Input**: `s = "abc"`, `w = 2`

```
i=0: char='a', runLength=1 < 2 → "a"
i=1: char='b', runLength=1 < 2 → "b"
i=2: char='c', runLength=1 < 2 → "c"

Result: "abc" (no compression)
```

**Input**: `s = "aaaaaa"`, `w = 1`

```
i=0: char='a', runLength=6 >= 1 → "a6"

Result: "a6" (all compressed)
```

## ⚠️ Common Mistakes to Avoid

1. **Off-By-One in Run Length**: Ensure `i - start` calculation is correct
2. **Not Handling w=1**: All runs compress when w=1
3. **String Concatenation**: Use StringBuilder/list for efficiency
4. **Empty String**: Check for null/empty input
5. **Large Numbers**: Count strings can be multiple digits

## 💡 Key Takeaways

1. **Single-Pass Efficiency**: Process each character exactly once
2. **Threshold-Based Compression**: Balance compression vs overhead
3. **Run-Length Encoding**: Classic string compression technique
4. **String Building**: Use efficient builders (StringBuilder, list)
5. **Edge Cases**: Handle w=1, single chars, empty strings


## Constraints

- `1 ≤ |s| ≤ 2 × 10^5`
- `1 ≤ w ≤ 10^5`
- `s` contains only lowercase English letters