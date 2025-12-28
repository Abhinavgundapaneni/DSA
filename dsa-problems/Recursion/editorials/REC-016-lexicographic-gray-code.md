---
title: Lexicographic Gray Code
slug: lexicographic-gray-code
difficulty: Medium
difficulty_score: 45
tags:
- Recursion
- Bit Manipulation
- Gray Code
problem_id: REC_LEXICOGRAPHIC_GRAY_CODE__6685
display_id: REC-016
topics:
- Recursion
- Bit Manipulation
- Gray Code
---
# Lexicographic Gray Code - Editorial

## Problem Summary

You need to generate the **Binary Reflected Gray Code** sequence for `n` bits.
The sequence starts with `0...0` and has `2^n` elements.
Every adjacent pair of elements differs by exactly one bit.
The construction is defined recursively:
-   `G(1) = [0, 1]`
-   `G(n) = [0G(n-1)_0, 0G(n-1)_1, ..., 1G(n-1)_last, ..., 1G(n-1)_0]`
    (Prefix 0 to the sequence, then prefix 1 to the *reversed* sequence).


## Constraints

- `1 <= n <= 12`
## Real-World Scenario

**Rotary Encoders**: In hardware, Gray codes are used to prevent spurious output from electromechanical switches. If you use standard binary, moving from 3 (011) to 4 (100) changes 3 bits. If the bits don't change perfectly simultaneously, you might read 011 -> 001 -> 000 -> 100 (reading 1, 0, 4). With Gray code, only one bit changes at a time, eliminating this ambiguity.

## Problem Exploration

### 1. Recursive Definition
-   `n=1`: `0`, `1`
-   `n=2`:
    -   Prefix 0 to `0, 1` -> `00, 01`
    -   Prefix 1 to `1, 0` (reversed) -> `11, 10`
    -   Result: `00, 01, 11, 10`
-   `n=3`:
    -   Prefix 0 to `00, 01, 11, 10` -> `000, 001, 011, 010`
    -   Prefix 1 to `10, 11, 01, 00` -> `110, 111, 101, 100`
    -   Result: `000, 001, 011, 010, 110, 111, 101, 100`

### 2. Iterative Approach (Bitwise)
The `i`-th Gray code can be calculated directly as `i ^ (i >> 1)`.
-   `i=0`: `0 ^ 0 = 0` (00)
-   `i=1`: `1 ^ 0 = 1` (01)
-   `i=2`: `2 ^ 1 = 3` (11)
-   `i=3`: `3 ^ 1 = 2` (10)
This matches the recursive definition.

### 3. Constraints
-   `n <= 12`: `2^12 = 4096`. Very small.
-   We need to output binary strings, not integers.

## Approaches

### Approach 1: Recursion
Directly implement the recursive definition.
`solve(n)`:
-   If `n==1` return `["0", "1"]`.
-   `prev = solve(n-1)`.
-   `res = []`.
-   For `s` in `prev`: `res.add("0" + s)`.
-   For `s` in `prev` reversed: `res.add("1" + s)`.
-   Return `res`.

### Approach 2: Iterative (Bitwise)
Iterate `i` from `0` to `2^n - 1`.
Calculate `val = i ^ (i >> 1)`.
Convert `val` to binary string of length `n`.

Both are `O(2^n * n)`. Recursion is more "natural" for the problem statement's prompt ("standard recursive construction").

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public List<String> grayCode(int n) {
        if (n == 0) return new ArrayList<>(Arrays.asList("0")); // Edge case if n=0 allowed
        if (n == 1) return new ArrayList<>(Arrays.asList("0", "1"));
        
        List<String> prev = grayCode(n - 1);
        List<String> result = new ArrayList<>();
        
        // Prefix 0
        for (String s : prev) {
            result.add("0" + s);
        }
        
        // Prefix 1 to reversed
        for (int i = prev.size() - 1; i >= 0; i--) {
            result.add("1" + prev.get(i));
        }
        
        return result;
    }
}
```

### Python

```python
def gray_code(n: int) -> list[str]:
    if n == 1:
        return ["0", "1"]
    
    prev = gray_code(n - 1)
    result = []
    
    # Prefix 0
    for s in prev:
        result.append("0" + s)
        
    # Prefix 1 to reversed
    for s in reversed(prev):
        result.append("1" + s)
        
    return result

def main():
    n = int(input())
    result = gray_code(n)
    for code in result:
        print(code)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

class Solution {
public:
    vector<string> grayCode(int n) {
        if (n == 1) return {"0", "1"};
        
        vector<string> prev = grayCode(n - 1);
        vector<string> result;
        result.reserve(prev.size() * 2);
        
        for (const string& s : prev) {
            result.push_back("0" + s);
        }
        
        for (auto it = prev.rbegin(); it != prev.rend(); ++it) {
            result.push_back("1" + *it);
        }
        
        return result;
    }
};
```

### JavaScript

```javascript
class Solution {
  grayCode(n) {
    if (n === 1) return ["0", "1"];

    const prev = this.grayCode(n - 1);
    const result = [];

    for (const s of prev) {
      result.push("0" + s);
    }

    for (let i = prev.length - 1; i >= 0; i--) {
      result.push("1" + prev[i]);
    }

    return result;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:** `n=2`

1.  `grayCode(2)` calls `grayCode(1)`.
2.  `grayCode(1)` returns `["0", "1"]`.
3.  Back in `grayCode(2)`:
    -   Prefix 0: `0`+`0`=`00`, `0`+`1`=`01`. Result: `["00", "01"]`.
    -   Prefix 1 (reversed): `1`+`1`=`11`, `1`+`0`=`10`. Result: `["00", "01", "11", "10"]`.
4.  Output matches example.

## Proof of Correctness

-   **Base Case**: `n=1` is `0, 1`. Differs by 1 bit.
-   **Inductive Step**:
    -   First half `0` + `G(n-1)` preserves 1-bit diff property.
    -   Second half `1` + `G(n-1)^R` preserves 1-bit diff property.
    -   Boundary: Last of first half is `0` + `G(n-1)_last`. First of second half is `1` + `G(n-1)_last`. They differ only in the first bit. Correct.

## Interview Extensions

1.  **Iterative Formula?**
    -   `G(i) = i ^ (i >> 1)`.
2.  **Hamiltonian Cycle on Hypercube?**
    -   Gray code is exactly a Hamiltonian cycle on an `n`-dimensional hypercube graph.

### Common Mistakes

-   **Reversing**: Forgetting to reverse the second half. If you don't reverse, the boundary transition will differ by more than 1 bit.
-   **Output Format**: Problem asks for binary strings, not integers.
