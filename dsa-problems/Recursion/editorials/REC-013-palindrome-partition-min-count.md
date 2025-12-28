---
title: Palindrome Partition with Minimum Count
slug: palindrome-partition-min-count
difficulty: Medium
difficulty_score: 53
tags:
- Recursion
- Backtracking
- Strings
problem_id: REC_PALINDROME_PARTITION_MIN_COUNT__3491
display_id: REC-013
topics:
- Recursion
- Backtracking
- Strings
---
# Palindrome Partition with Minimum Count - Editorial

## Problem Summary

You need to partition a string `s` into substrings such that:
1.  Every substring is a **palindrome**.
2.  The length of every substring is at most `L`.
3.  The **number of substrings** in the partition is minimized.

Return all such minimum partitions.


## Constraints

- `1 <= |s| <= 12`
- `1 <= L <= |s|`
- `s` contains lowercase English letters
## Real-World Scenario

Think of **Data Compression**. You want to split a long message into the fewest possible chunks, but each chunk must satisfy a specific property (like being a palindrome, which might represent a reversible signal) and fit within a buffer size `L`. Minimizing the number of chunks reduces header overhead.

## Problem Exploration

### 1. Palindrome Check
A substring `s[i...j]` is a palindrome if it reads the same forwards and backwards. We can precompute this for all pairs `(i, j)` in `O(N^2)` using Dynamic Programming.
`isPal[i][j] = (s[i] == s[j]) && (j - i < 2 || isPal[i+1][j-1])`.

### 2. Minimum Cuts (DP vs BFS)
To find the *minimum number* of partitions, we can use BFS or DP.
-   **BFS**: Treat indices `0` to `N` as nodes. Edge from `i` to `j` exists if `s[i...j-1]` is a valid palindrome of length `<= L`. Find shortest path from `0` to `N`.
-   **DP**: `dp[i]` = min partitions for suffix `s[i...]`.
    `dp[i] = 1 + min(dp[j+1])` for all valid `j` where `s[i...j]` is palindrome and length `<= L`.

### 3. All Solutions
Since we need *all* partitions achieving the minimum count, we can:
1.  Compute `min_cuts` using BFS/DP.
2.  Use Backtracking (DFS) to reconstruct paths that match this `min_cuts`.

Given `N <= 12`, we can just use pure backtracking with a global minimum tracker, or iterative deepening. But BFS is cleanest for "shortest path" structure.

## Approaches

### Approach 1: BFS for Min Count + DFS for Reconstruction
1.  **BFS**: Compute `dist[i]`: minimum number of palindromes needed to cover prefix `s[0...i-1]`. Or better, `dist[i]` = min partitions for suffix `s[i...]`. Let's do suffix.
    -   `dist[N] = 0`.
    -   Work backwards or use BFS from `N` to `0` in the reversed graph?
2.  **DFS**: Reconstruct paths.
    -   `dfs(index, current_path)`
    -   If `index == N`: Add to results if `current_path.size() == min_k`.
    -   Iterate `j` from `index` to `N-1`.
    -   If `s[index...j]` is valid (palindrome & length `<= L`) AND `dist[j+1] == dist[index] - 1` (optimal substructure):
        -   Add substring to path.
        -   Recurse.
        -   Backtrack.

Then in DFS from `0`: move to `j+1` only if `dist[j+1] == dist[index] + 1`.

### Approach 2: Pure Backtracking (Small N)
With `N=12`, pure recursion is fine.
`solve(index, current_path)`
-   Track `global_min`.
-   If `current_path.size() > global_min`, prune.
-   If `index == N`:
    -   If `size < global_min`: Clear results, update `global_min`, add path.
    -   If `size == global_min`: Add path.

This is simpler to implement and sufficient for `N=12`.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public List<List<String>> minPalindromePartitions(String s, int L) {
        int n = s.length();
        // Precompute palindromes
        boolean[][] isPal = new boolean[n][n];
        for (int len = 1; len <= n; len++) {
            for (int i = 0; i <= n - len; i++) {
                int j = i + len - 1;
                if (s.charAt(i) == s.charAt(j)) {
                    if (len <= 2 || isPal[i + 1][j - 1]) {
                        isPal[i][j] = true;
                    }
                }
            }
        }

        List<List<String>> results = new ArrayList<>();
        int[] minCount = {Integer.MAX_VALUE};
        
        backtrack(0, s, L, isPal, new ArrayList<>(), results, minCount);
        return results;
    }

    private void backtrack(int start, String s, int L, boolean[][] isPal, 
                           List<String> current, List<List<String>> results, int[] minCount) {
        if (start == s.length()) {
            if (current.size() < minCount[0]) {
                minCount[0] = current.size();
                results.clear();
                results.add(new ArrayList<>(current));
            } else if (current.size() == minCount[0]) {
                results.add(new ArrayList<>(current));
            }
            return;
        }

        // Pruning: if current size already exceeds min found, stop
        if (current.size() >= minCount[0]) return;

        for (int end = start; end < s.length(); end++) {
            if (end - start + 1 > L) break; // Length constraint
            if (isPal[start][end]) {
                current.add(s.substring(start, end + 1));
                backtrack(end + 1, s, L, isPal, current, results, minCount);
                current.remove(current.size() - 1);
            }
        }
    }
}
```

### Python

```python
def is_palindrome(s):
    """Check if string is a palindrome."""
    return s == s[::-1]

def min_palindrome_partition(s, L):
    """
    Find minimum palindrome partition with max substring length L.
    Uses DP to find one valid minimum partition.
    """
    n = len(s)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    partition = [None] * (n + 1)
    
    for i in range(1, n + 1):
        for j in range(max(0, i - L), i):
            substr = s[j:i]
            if is_palindrome(substr) and dp[j] + 1 < dp[i]:
                dp[i] = dp[j] + 1
                partition[i] = j
    
    if dp[n] == float('inf'):
        return None
    
    # Reconstruct one valid partition
    result = []
    i = n
    while i > 0:
        j = partition[i]
        result.append(s[j:i])
        i = j
    
    return ' '.join(reversed(result))

def main():
    s = input().strip()
    L = int(input())
    result = min_palindrome_partition(s, L)
    if result is None:
        print("NONE")
    else:
        print(result)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <string>
#include <climits>

using namespace std;

class Solution {
public:
    vector<vector<string>> minPalindromePartitions(const string& s, int L) {
        int n = s.length();
        vector<vector<bool>> isPal(n, vector<bool>(n, false));
        for (int len = 1; len <= n; len++) {
            for (int i = 0; i <= n - len; i++) {
                int j = i + len - 1;
                if (s[i] == s[j]) {
                    if (len <= 2 || isPal[i + 1][j - 1]) {
                        isPal[i][j] = true;
                    }
                }
            }
        }

        vector<vector<string>> results;
        int minCount = INT_MAX;
        vector<string> current;
        
        backtrack(0, s, L, isPal, current, results, minCount);
        return results;
    }

private:
    void backtrack(int start, const string& s, int L, const vector<vector<bool>>& isPal, 
                   vector<string>& current, vector<vector<string>>& results, int& minCount) {
        if (start == s.length()) {
            if ((int)current.size() < minCount) {
                minCount = current.size();
                results.clear();
                results.push_back(current);
            } else if ((int)current.size() == minCount) {
                results.push_back(current);
            }
            return;
        }

        if ((int)current.size() >= minCount) return;

        for (int end = start; end < s.length(); end++) {
            if (end - start + 1 > L) break;
            if (isPal[start][end]) {
                current.push_back(s.substr(start, end - start + 1));
                backtrack(end + 1, s, L, isPal, current, results, minCount);
                current.pop_back();
            }
        }
    }
};
```

### JavaScript

```javascript
class Solution {
  minPalindromePartitions(s, L) {
    const n = s.length;
    const isPal = Array.from({ length: n }, () => Array(n).fill(false));
    for (let len = 1; len <= n; len++) {
      for (let i = 0; i <= n - len; i++) {
        const j = i + len - 1;
        if (s[i] === s[j]) {
          if (len <= 2 || isPal[i + 1][j - 1]) {
            isPal[i][j] = true;
          }
        }
      }
    }

    let results = [];
    let minCount = Infinity;

    const backtrack = (start, current) => {
      if (start === n) {
        if (current.length < minCount) {
          minCount = current.length;
          results = [[...current]];
        } else if (current.length === minCount) {
          results.push([...current]);
        }
        return;
      }

      if (current.length >= minCount) return;

      for (let end = start; end < n; end++) {
        if (end - start + 1 > L) break;
        if (isPal[start][end]) {
          current.push(s.substring(start, end + 1));
          backtrack(end + 1, current);
          current.pop();
        }
      }
    };

    backtrack(0, []);
    return results;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:** `aab`, `L=2`

1.  **Precompute Palindromes**:
    -   `a` (0,0), `a` (1,1), `b` (2,2) -> True.
    -   `aa` (0,1) -> True.
    -   `ab` (1,2) -> False.
    -   `aab` (0,2) -> False.
2.  `backtrack(0)`:
    -   Try `a` (0,0): Path `["a"]`.
        -   `backtrack(1)`:
            -   Try `a` (1,1): Path `["a", "a"]`.
                -   `backtrack(2)`:
                    -   Try `b` (2,2): Path `["a", "a", "b"]`.
                        -   Found len 3. `minCount = 3`. Results `[["a", "a", "b"]]`.
            -   Try `ab` (1,2): Invalid.
    -   Try `aa` (0,1): Path `["aa"]`.
        -   `backtrack(2)`:
            -   Try `b` (2,2): Path `["aa", "b"]`.
                -   Found len 2. `2 < 3`. `minCount = 2`. Results `[["aa", "b"]]`.
    -   Try `aab` (0,2): Length 3 > L=2. Break.

**Result:** `aa b`.

## Proof of Correctness

-   **Validity**: We only pick substrings that are palindromes and satisfy length constraint `L`.
-   **Optimality**: We track `minCount` and only keep solutions that match this minimum.
-   **Completeness**: Backtracking explores all valid partitions.

## Interview Extensions

1.  **Just the count?**
    -   Use DP: `dp[i] = 1 + min(dp[j+1])`. `O(N^2)`.
2.  **Large N?**
    -   Manacher's Algorithm for palindrome finding (`O(N)`), then DP.

### Common Mistakes

-   **Length Constraint**: Forgetting to check `end - start + 1 <= L`.
-   **Pruning**: Not pruning when `current.size() >= minCount` can lead to TLE on slightly larger inputs (though `N=12` is very forgiving).
