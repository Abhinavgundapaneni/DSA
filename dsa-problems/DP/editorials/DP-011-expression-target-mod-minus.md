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
---

# DP-011: Expression Target Modulo With Required Minus

## 📋 Problem Summary

Given a digit string `s`, modulus `M`, target remainder `K`, and max chunk length `Lmax`, split `s` into chunks of length `1..Lmax` (left to right, no reordering). Insert `+` or `-` between chunks.

Constraints:

- No leading zeros inside a chunk (unless the chunk is exactly `"0"`).
- At least one `-` must appear in the expression.
- Evaluate the expression; count how many expressions satisfy `value % M == K`.

Return the count modulo `1_000_000_007`.

## 🌍 Real-World Scenario

**Scenario Title:** Checksum Variations With Required Debit

You’re building alternate checksum formulas from a fixed digit string. Each chunk can be added or subtracted, but every formula must include at least one subtraction (debit). You only care about the result modulo `M` (like a hash bucket).

This maps to counting all valid expressions under chunk-size and “must-subtract” rules.

**Why This Problem Matters:**

- String-to-expression DP (classic interview pattern)
- Demonstrates modulo arithmetic handling with negative values
- Shows how to enforce a “must use operator X at least once” constraint via DP state

![Real-World Application](../images/DP-011/real-world-scenario.png)

## ✅ Clarifications

- The first chunk has no operator before it.
- At least one `-` anywhere in the expression.
- Negative intermediate results are fine; always reduce modulo `M`.
- `1 <= |s| <= 12`, so exponential brute force is possible but DP is cleaner and less error-prone.

## Detailed Explanation

### State definition

Let:

`dp[pos][rem][usedMinus] = number of ways to parse prefix s[0..pos-1]`
such that:

- we have consumed exactly `pos` characters,
- current expression value ≡ `rem (mod M)`,
- `usedMinus` is 0/1 indicating whether we have used at least one minus so far.

Answer:

`sum of dp[n][K][1]` (actually just dp[n][K][1], since rem must be K).

### Transitions

From `pos`, pick a chunk `s[pos..end-1]` of length `1..Lmax` (end ≤ n):

- skip if chunk has leading zero (`s[pos]=='0'` and length>1).
- let `val = int(chunk)`

If this is the **first chunk** (`pos == 0`):

- newRem = `val % M`
- `dp[end][newRem][0] += 1`

Else, you can add or subtract the chunk:

- Add: `newRem = (rem + val) % M`, `usedMinus` unchanged
- Sub: `newRem = (rem - val) % M`, `usedMinus` becomes 1

All updates are modulo `MOD = 1e9+7`.

### Why this enforces “at least one minus”

`usedMinus` starts at 0 and only flips to 1 when you choose a `-` transition. We count only states with `usedMinus = 1` at the end.

### Complexity

- `n <= 12`, `M <= 50`, `Lmax <= n`
- States: `O(n * M * 2)`
- For each state, try up to `Lmax` chunks: `O(n * M * Lmax)`
- With small limits, this is extremely fast.

![Algorithm Visualization](../images/DP-011/algorithm-visualization.png)
![Algorithm Steps](../images/DP-011/algorithm-steps.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    private static final int MOD = 1_000_000_007;

    public int countExpressions(String s, int M, int K, int L) {
        int n = s.length();
        int[][][] dp = new int[n + 1][M][2];

        for (int len = 1; len <= L && len <= n; len++) {
            if (s.charAt(0) == '0' && len > 1) break;
            int val = Integer.parseInt(s.substring(0, len)) % M;
            dp[len][val][0] = (dp[len][val][0] + 1) % MOD;
        }

        for (int pos = 1; pos < n; pos++) {
            for (int rem = 0; rem < M; rem++) {
                for (int used = 0; used <= 1; used++) {
                    int ways = dp[pos][rem][used];
                    if (ways == 0) continue;
                    for (int len = 1; len <= L && pos + len <= n; len++) {
                        if (s.charAt(pos) == '0' && len > 1) break;
                        int val = Integer.parseInt(s.substring(pos, pos + len));
                        int addRem = (int)(((rem + val) % M + M) % M);
                        int subRem = (int)(((rem - val) % M + M) % M);

                        dp[pos + len][addRem][used] = (int)((dp[pos + len][addRem][used] + (long)ways) % MOD);
                        dp[pos + len][subRem][1] = (int)((dp[pos + len][subRem][1] + (long)ways) % MOD);
                    }
                }
            }
        }

        return dp[n][K][1];
    }
}
```

### Python

```python
MOD = 1_000_000_007

def count_expressions(s: str, M: int, K: int, L: int) -> int:
    n = len(s)
    dp = [[[0]*2 for _ in range(M)] for __ in range(n+1)]

    for l in range(1, min(L, n) + 1):
        if s[0] == '0' and l > 1:
            break
        val = int(s[0:l]) % M
        dp[l][val][0] = 1

    for pos in range(1, n):
        for rem in range(M):
            for used in range(2):
                ways = dp[pos][rem][used]
                if ways == 0:
                    continue
                for l in range(1, min(L, n - pos) + 1):
                    if s[pos] == '0' and l > 1:
                        break
                    val = int(s[pos:pos+l])
                    addRem = (rem + val) % M
                    subRem = (rem - val) % M
                    dp[pos+l][addRem][used] = (dp[pos+l][addRem][used] + ways) % MOD
                    dp[pos+l][subRem][1] = (dp[pos+l][subRem][1] + ways) % MOD

    return dp[n][K][1]

def main():
    s = input().strip()
    M, K, L = map(int, input().split())
    print(count_expressions(s, M, K, L))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

class Solution {
    static const int MOD = 1'000'000'007;
public:
    int countExpressions(const string& s, int M, int K, int L) {
        int n = (int)s.size();
        vector<vector<array<int,2>>> dp(n+1, vector<array<int,2>>(M, {0,0}));

        for (int len=1; len<=L && len<=n; len++) {
            if (s[0]=='0' && len>1) break;
            int val = stoi(s.substr(0,len)) % M;
            dp[len][val][0] = (dp[len][val][0] + 1) % MOD;
        }

        for (int pos=1; pos<n; pos++) {
            for (int rem=0; rem<M; rem++) {
                for (int used=0; used<=1; used++) {
                    int ways = dp[pos][rem][used];
                    if (!ways) continue;
                    for (int len=1; len<=L && pos+len<=n; len++) {
                        if (s[pos]=='0' && len>1) break;
                        int val = stoi(s.substr(pos,len));
                        int addRem = ((rem + val)%M + M)%M;
                        int subRem = ((rem - val)%M + M)%M;
                        dp[pos+len][addRem][used] = (dp[pos+len][addRem][used] + ways) % MOD;
                        dp[pos+len][subRem][1] = (dp[pos+len][subRem][1] + ways) % MOD;
                    }
                }
            }
        }
        return dp[n][K][1];
    }
};
```

### JavaScript

```javascript
const MOD = 1000000007n;

class Solution {
  countExpressions(s, M, K, L) {
    const n = s.length;
    const dp = Array.from({ length: n + 1 }, () =>
      Array.from({ length: M }, () => [0n, 0n])
    );

    for (let len = 1; len <= L && len <= n; len++) {
      if (s[0] === '0' && len > 1) break;
      const val = BigInt(parseInt(s.substring(0, len))) % BigInt(M);
      dp[len][Number(val)][0] = (dp[len][Number(val)][0] + 1n) % MOD;
    }

    for (let pos = 1; pos < n; pos++) {
      for (let rem = 0; rem < M; rem++) {
        for (let used = 0; used <= 1; used++) {
          const ways = dp[pos][rem][used];
          if (ways === 0n) continue;
          for (let len = 1; len <= L && pos + len <= n; len++) {
            if (s[pos] === '0' && len > 1) break;
            const val = BigInt(parseInt(s.substring(pos, pos + len)));
            const addRem = Number((BigInt(rem) + val) % BigInt(M));
            const subRem = Number((BigInt(rem) - val) % BigInt(M) + BigInt(M)) % M;
            dp[pos + len][addRem][used] = (dp[pos + len][addRem][used] + ways) % MOD;
            dp[pos + len][subRem][1] = (dp[pos + len][subRem][1] + ways) % MOD;
          }
        }
      }
    }

    return Number(dp[n][K][1] % MOD);
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
Sample:

`s=1234, M=7, K=0, Lmax=2`

Enumerating valid chunkings with at least one minus yields 5 expressions congruent to 0 mod 7.

![Example Visualization](../images/DP-011/example-1.png)

## ✅ Proof of Correctness

We enumerate all valid chunk splits (length 1..Lmax, no leading zeros) and all operator choices (+/-) while tracking:

- current position in `s`,
- current remainder mod `M`,
- whether a minus has been used.

The recurrence adds the next chunk either as `+` (remainder update `+ val`) or `-` (remainder update `- val`, flipping `usedMinus=1`). Because every valid expression corresponds to exactly one sequence of such choices, and we count only states with `usedMinus=1` at the end and remainder `K`, the DP counts exactly the desired expressions.

Modulo arithmetic on remainders ensures correctness even with negative partial sums.

### Common Mistakes to Avoid

1. **Allowing leading zeros inside a chunk** (invalid)
2. **Counting expressions with no minus**
3. **Forgetting to mod after subtraction** (negative remainders)
4. **Integer overflow on counts** (use 64-bit / BigInt and mod 1e9+7)
5. **Not limiting chunk length to Lmax**


## Related Concepts

- String parsing with DP
- Modulo DP
- State tracking for “at least one occurrence” constraints
