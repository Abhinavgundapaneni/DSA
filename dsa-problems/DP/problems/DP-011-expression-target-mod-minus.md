---
problem_id: DP_EXPR_MOD_MINUS__8104
display_id: DP-011
slug: expression-target-mod-minus
title: "Expression Target Modulo With Required Minus"
difficulty: Medium
difficulty_score: 60
topics:
  - Dynamic Programming
  - String
  - Modulo Arithmetic
tags:
  - dp
  - strings
  - modulo
  - medium
premium: true
subscription_tier: basic
time_limit: 2000
memory_limit: 256
---

# DP-011: Expression Target Modulo With Required Minus

## Problem Statement

You are given:

- a digit string `s` (length up to 12)
- an integer modulus `M`
- a target remainder `K`
- a maximum chunk length `Lmax`

You must split `s` into chunks of length `1..Lmax` (from left to right, no reordering) and insert `+` or `-` between chunks to form an expression.

Rules:

- No chunk may have leading zeros unless the chunk is exactly `"0"`.
- You must use **at least one `-` operator** in the entire expression.
- Evaluate the expression normally; let `val % M` be its remainder (negative values are taken modulo `M` as usual).

Count the number of valid expressions whose value modulo `M` equals `K`. Output the count.

![Problem Illustration](../images/DP-011/problem-illustration.png)

## Input Format

- First line: digit string `s`
- Second line: three integers `M`, `K`, `Lmax`

## Output Format

Print one integer: the number of valid expressions modulo `1_000_000_007`.

## Constraints

- `1 <= |s| <= 12`
- `1 <= M <= 50`
- `0 <= K < M`
- `1 <= Lmax <= |s|`

## Example

**Input:**
```
1234
7 0 2
```

**Output:**
```
2
```

**Explanation:**

With chunk length up to 2 and at least one minus, there are 2 valid expressions whose value is congruent to 0 modulo 7: `1-2-3+4 = 0` and `1-2-34 = -35 ≡ 0 (mod 7)`.

![Example Visualization](../images/DP-011/example-1.png)

## Notes

- Negative intermediate results are allowed; apply modulo normally (e.g., `(-1) % 7 = 6`).
- At least one minus is mandatory; expressions with only `+` are invalid.

## Related Topics

Dynamic Programming, Modulo Arithmetic, String Parsing

---

## Solution Template

### Java

```java
import java.util.*;

class Solution {
    private static final int MOD = 1_000_000_007;

    public int countExpressions(String s, int M, int K, int L) {
        // Your implementation here
        return 0;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();
        int M = sc.nextInt(), K = sc.nextInt(), L = sc.nextInt();
        System.out.println(new Solution().countExpressions(s, M, K, L));
        sc.close();
    }
}
```

### Python

```python
def count_expressions(s: str, M: int, K: int, L: int) -> int:
    # Your implementation here
    return 0

def main():
    s = input().strip()
    M, K, L = map(int, input().split())
    print(count_expressions(s, M, K, L))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
using namespace std;

class Solution {
public:
    int countExpressions(const string& s, int M, int K, int L) {
        // Your implementation here
        return 0;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    getline(cin, s);
    int M, K, L;
    cin >> M >> K >> L;
    Solution sol;
    cout << sol.countExpressions(s, M, K, L) << "\\n";
    return 0;
}
```

### JavaScript

```javascript
const readline = require("readline");
const MOD = 1000000007n;

class Solution {
  countExpressions(s, M, K, L) {
    // Your implementation here
    return 0;
  }
}

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const lines = [];
rl.on("line", (line) => lines.push(line.trim()));
rl.on("close", () => {
  const s = (lines[0] ?? "").trim();
  const [M, K, L] = lines[1].split(" ").map(Number);
  const sol = new Solution();
  console.log(sol.countExpressions(s, M, K, L));
});
```

