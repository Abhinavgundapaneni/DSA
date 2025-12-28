---
id: STR-013
title: Run-Length Decode with Cap
sidebar_label: STR-013 - Run-Length Decode with Cap
tags:
- strings
- encoding
- parsing
- easy-medium
difficulty: Easy-Medium
difficulty_score: 30
problem_id: STR_RUN_LENGTH_DECODE_CAP__1013
display_id: STR-013
slug: run-length-decode-cap
topics:
- String Manipulation
- Encoding
- Parsing
---
# STR-013: Run-Length Decode with Cap

## 📋 Problem Summary

**Input**: Run-length encoded string (format: "char+count"), integer `cap`  
**Output**: Decoded string with any run > `cap` limited to exactly `cap` occurrences  
**Constraints**: `1 <= |s| <= 10^5`, `1 <= cap <= 10^4`

## 🌍 Real-World Scenario

Memory-constrained decompression needs to limit expansion. Capping decoded runs prevents buffer overflow while preserving encoding structure for pattern recognition.

## Detailed Explanation

**Run-Length Encoding**: "a3b2" means "aab"

**Capping**: If count > cap, output only `cap` occurrences

**Example**: `s="a10b2"`, `cap=3`

- "a10" → "aaa" (capped from 10 to 3)
- "b2" → "bb" (no cap needed)
- Output: "aaabb"

## Naive Approach

```
1. Parse character and its count
2. For each pair:
   a. If count > cap, append char × cap
   b. Else, append char × count
```

### Time Complexity: **O(n + output_size)**

- Parsing: O(n)
- Output generation: O(sum of min(count, cap))

### Space Complexity: **O(output_size)**

**Note**: This is actually optimal!

## Optimal Approach

**Single-Pass Parsing with Capping**:

```
1. result = []
2. i = 0
3. While i < len(s):
   a. char = s[i]
   b. i++
   c. count_str = ""
   d. While i < len(s) and s[i].isdigit():
      count_str += s[i]
      i++
   e. count = int(count_str)
   f. actual_count = min(count, cap)
   g. result.append(char × actual_count)
4. Return join(result)
```

### Time Complexity

| Phase                | Operations             | Cost                   |
| -------------------- | ---------------------- | ---------------------- |
| Parse encoded string | Iterate each character | O(n)                   |
| Extract numbers      | Digit parsing          | O(n)                   |
| Generate output      | Append characters      | O(output_size)         |
| **Total**            |                        | **O(n + output_size)** |

### Space Complexity

| Component      | Space          | Justification      |
| -------------- | -------------- | ------------------ |
| Result string  | O(output_size) | Decoded characters |
| Temp variables | O(1)           | char, count        |
| **Total**      |                | **O(output_size)** |

## 💻 Implementation

### Python

```python
def decode_with_cap(s: str, cap: int) -> str:
    result = []
    i = 0
    n = len(s)

    while i < n:
        # Read character
        char = s[i]
        i += 1

        # Read count (digits)
        count_str = ""
        while i < n and s[i].isdigit():
            count_str += s[i]
            i += 1

        # Decode with cap
        count = int(count_str) if count_str else 1
        actual_count = min(count, cap)
        result.append(char * actual_count)

    return ''.join(result)

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    s = lines[0]
    cap = int(lines[1])
    result = decode_with_cap(s, cap)
    print(result)

if __name__ == "__main__":
    main()

```

### Java

```java
class Solution {
    public String decodeWithCap(String s, int cap) {
        StringBuilder result = new StringBuilder();
        int i = 0;
        int n = s.length();

        while (i < n) {
            // Read character
            char ch = s.charAt(i);
            i++;

            // Read count
            StringBuilder countStr = new StringBuilder();
            while (i < n && Character.isDigit(s.charAt(i))) {
                countStr.append(s.charAt(i));
                i++;
            }

            // Decode with cap
            int count = countStr.length() > 0 ? Integer.parseInt(countStr.toString()) : 1;
            int actualCount = Math.min(count, cap);

            for (int j = 0; j < actualCount; j++) {
                result.append(ch);
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
    string decodeWithCap(string s, int cap) {
        string result;
        int i = 0;
        int n = s.size();

        while (i < n) {
            // Read character
            char ch = s[i];
            i++;

            // Read count
            string countStr;
            while (i < n && isdigit(s[i])) {
                countStr += s[i];
                i++;
            }

            // Decode with cap
            int count = countStr.empty() ? 1 : stoi(countStr);
            int actualCount = min(count, cap);

            result.append(actualCount, ch);
        }

        return result;
    }
};
```

### JavaScript

```javascript
function decodeWithCap(s, cap) {
  const result = [];
  let i = 0;
  const n = s.length;

  while (i < n) {
    // Read character
    const char = s[i];
    i++;

    // Read count
    let countStr = "";
    while (i < n && /\d/.test(s[i])) {
      countStr += s[i];
      i++;
    }

    // Decode with cap
    const count = countStr ? parseInt(countStr) : 1;
    const actualCount = Math.min(count, cap);

    result.push(char.repeat(actualCount));
  }

  return result.join("");
}
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input**: `s="a10b2"`, `cap=3`

**Execution**:

```
i=0: char='a', i=1
     countStr=""

     i=1: s[1]='1' (digit) → countStr="1", i=2
     i=2: s[2]='0' (digit) → countStr="10", i=3
     i=3: s[3]='b' (not digit) → stop

     count=10, actualCount=min(10,3)=3
     result=["aaa"]

i=3: char='b', i=4
     countStr=""

     i=4: s[4]='2' (digit) → countStr="2", i=5
     i=5: out of bounds → stop

     count=2, actualCount=min(2,3)=2
     result=["aaa", "bb"]

Final: join(result) = "aaabb"
```

**Output**: `"aaabb"`

## 🧪 Walkthrough: Edge Cases

**Input**: `s="x100y50"`, `cap=5`

```
Process 'x':
  count=100, actualCount=5
  result="xxxxx"

Process 'y':
  count=50, actualCount=5
  result="xxxxxyyyyy"
```

**Output**: `"xxxxxyyyyy"`

**Input**: `s="a1b1c1"`, `cap=10`

```
Process 'a': count=1, actualCount=1 → "a"
Process 'b': count=1, actualCount=1 → "ab"
Process 'c': count=1, actualCount=1 → "abc"
```

**Output**: `"abc"`

## ⚠️ Common Mistakes to Avoid

1. **Not Handling Multi-Digit Counts**: "a100" has count=100, not 1,0,0
2. **Forgetting to Advance Index**: Must increment i while reading digits
3. **Off-By-One in Loop**: Ensure proper bounds checking
4. **Empty Count String**: Handle cases where no digit follows character
5. **String Building Efficiency**: Use StringBuilder/list for efficiency

## 💡 Key Takeaways

1. **Parsing Pattern**: Character followed by optional digits
2. **Capping Logic**: `min(count, cap)` is simple and effective
3. **Digit Accumulation**: Build count string character by character
4. **Edge Cases**: No digits (count=1), very large numbers
5. **Efficient Building**: Use append operations, not repeated concatenation


## Constraints

- `1 ≤ |s| ≤ 10^5`
- `1 ≤ cap ≤ 10^4`
- Encoded format: character followed by count (digits)