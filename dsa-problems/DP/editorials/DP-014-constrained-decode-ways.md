---
problem_id: DP_CONSTRAINED_DECODE__3012
display_id: DP-014
slug: constrained-decode-ways
title: "Constrained Decode Ways"
difficulty: Medium
difficulty_score: 50
topics:
  - Dynamic Programming
  - Strings
  - Combinatorics
tags:
  - dp
  - decoding
  - strings
  - medium
premium: true
subscription_tier: basic
---

# DP-014: Constrained Decode Ways

## 📋 Problem Summary

You are given a digit string `s`. Codes map `1 -> A` through `26 -> Z`. A special rule restricts zeros: any `0` is valid **only** when it forms the pair `20`. Count the number of valid decodings modulo `1_000_000_007`; if the string cannot be decoded, the answer is `0`.

## 🌍 Real-World Scenario

**Scenario Title:** Even-Guarded One-Time Passwords

An IoT company uses numeric one-time passwords where digits are grouped into codes `1..26`. For resilience against optical character recognition errors, zeros are only allowed after an even digit two (`20`) to serve as a checksum. Any other placement of `0` indicates tampering.

Developers need to compute how many valid interpretations a received password string could have:

- A lone zero means the device rejects the password.
- Two-digit codes like `10` or `30` are forbidden; only `20` is permitted.
- All other two-digit codes `11..26` remain valid.

**Why This Problem Matters:**

- Strengthens **linear DP on strings** with custom validity checks.
- Shows how small rule tweaks (“only `20` is valid with zero”) change transition logic.
- Reinforces **modular arithmetic** for large counts.

![Real-World Application](../images/DP-014/real-world-scenario.png)

## Detailed Explanation

Classic “decode ways” DP states: `dp[i] = number of ways to decode prefix ending at i`. Here we only need the last two states, because each step depends on at most two previous characters.

Let:

- `prev1 = dp[i-1]` (ways up to previous character)
- `prev2 = dp[i-2]` (ways up to two characters before)

For position `i` (`1`-indexed):

1. **Single-digit code:** Allowed if `s[i] != '0'`. Add `prev1`.
2. **Two-digit code:** Form value `pair = 10 * s[i-1] + s[i]`.
   - Valid if `pair == 20` (special zero rule) **or** `11..26` (excluding `10`).
   - Add `prev2` for these.
3. If `s[i] == '0'`, only `pair == 20` works; otherwise the string is invalid and contributes 0.

Initialization:

- If `s[0] == '0'`, answer is 0.
- Otherwise `prev1 = prev2 = 1`.

Update `prev2 <- prev1`, `prev1 <- cur` each step. The result is `prev1` at the end.

## Naive Approach

**Intuition:**
Generate all splits recursively and count valid codes.

**Algorithm:**

1. DFS from index 0.
2. At each step, try a single digit; if non-zero, recurse.
3. Try two digits; if `20` or between `11` and `26`, recurse.
4. Count leaves reaching the end.

**Time Complexity:** Exponential in `|s|`.  
**Space Complexity:** Recursion depth `O(n)`.

**Why This Works:**
Enumerates every partition, filtering invalid ones.

**Limitations:**

- Exponential blowup (`2^n` splits).
- TLE for `|s| = 1e5`.

## Optimal Approach

**Key Insight:**
Each position only depends on the previous one or two characters, so we need just two running DP values.

**Algorithm:**

1. If `s` is empty or starts with `0`, return 0.
2. Set `prev2 = 1`, `prev1 = 1`.
3. For `i` from 1 to `n-1`:
   - `pair = int(s[i-1..i])`
   - `cur = 0`
   - If `s[i] != '0'`, add `prev1` to `cur`.
   - If `pair == 20` or (`pair > 10 && pair <= 26`), add `prev2` to `cur`.
   - Take `cur %= MOD`.
   - Shift: `prev2 = prev1`, `prev1 = cur`.
4. Return `prev1`.

**Time Complexity:** `O(n)`  
**Space Complexity:** `O(1)`  
**Why This Is Optimal:**
Only two previous states are needed; every character is processed once.

![Algorithm Visualization](../images/DP-014/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    static final long MOD = 1_000_000_007L;

    public long decodeWays(String s) {
        int n = s.length();
        if (n == 0 || s.charAt(0) == '0') return 0;
        long prev2 = 1, prev1 = 1;
        for (int i = 1; i < n; i++) {
            char c = s.charAt(i);
            int pair = (s.charAt(i - 1) - '0') * 10 + (c - '0');
            long cur = 0;
            if (c != '0') {
                cur = (cur + prev1) % MOD;
                if (pair == 20 || (pair > 10 && pair <= 26)) cur = (cur + prev2) % MOD;
            } else {
                if (pair == 20) cur = (cur + prev2) % MOD;
            }
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1 % MOD;
    }
}
```

### Python

```python
MOD = 1_000_000_007

def decode_ways(s: str) -> int:
    n = len(s)
    if n == 0 or s[0] == "0":
        return 0
    prev2 = prev1 = 1
    for i in range(1, n):
        c = s[i]
        pair = int(s[i-1:i+1])
        cur = 0
        if c != "0":
            cur = (cur + prev1) % MOD
            if pair == 20 or (10 < pair <= 26):
                cur = (cur + prev2) % MOD
        else:
            if pair == 20:
                cur = (cur + prev2) % MOD
        prev2, prev1 = prev1, cur
    return prev1 % MOD

def main():
    s = input().strip()
    print(decode_ways(s))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1'000'000'007LL;

long long decodeWays(const string& s) {
    int n = s.size();
    if (n == 0 || s[0] == '0') return 0;
    long long prev2 = 1, prev1 = 1;
    for (int i = 1; i < n; ++i) {
        int pair = (s[i - 1] - '0') * 10 + (s[i] - '0');
        long long cur = 0;
        if (s[i] != '0') {
            cur = (cur + prev1) % MOD;
            if (pair == 20 || (pair > 10 && pair <= 26)) cur = (cur + prev2) % MOD;
        } else {
            if (pair == 20) cur = (cur + prev2) % MOD;
        }
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1 % MOD;
}
```

### JavaScript

```javascript
const MOD = 1_000_000_007n;

function decodeWays(s) {
  if (s.length === 0 || s[0] === "0") return 0;
  let prev2 = 1n, prev1 = 1n;
  for (let i = 1; i < s.length; i++) {
    const pair = Number(s[i - 1]) * 10 + Number(s[i]);
    let cur = 0n;
    if (s[i] !== "0") {
      cur = (cur + prev1) % MOD;
      if (pair === 20 || (pair > 10 && pair <= 26)) cur = (cur + prev2) % MOD;
    } else {
      if (pair === 20) cur = (cur + prev2) % MOD;
    }
    prev2 = prev1;
    prev1 = cur;
  }
  return Number(prev1 % MOD);
}
```

### Common Mistakes to Avoid

1. **Treating `10` as valid.**
   - ❌ Counting `10` violates the rule (“only `20` pairs with zero”).
   - ✅ Allow two-digit codes only if `pair == 20` or `11..26`.

2. **Allowing leading zero.**
   - ❌ Starting DP with `dp[0] = 1` even when `s[0] == '0'`.
   - ✅ Return `0` immediately if the first character is `0`.

3. **Overflow without modulus.**
   - ❌ Accumulating counts in 32-bit integers.
   - ✅ Use 64-bit (or BigInt) and reduce modulo `1_000_000_007` every step.



## Related Concepts

- Linear DP on strings
- State rolling (two variables)
- Modulo arithmetic in counting DPs
