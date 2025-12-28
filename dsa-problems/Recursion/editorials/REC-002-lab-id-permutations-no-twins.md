---
title: Lab ID Permutations With No Adjacent Twins
slug: lab-id-permutations-no-twins
difficulty: Easy
difficulty_score: 30
tags:
- Recursion
- Backtracking
- Permutations
problem_id: REC_LAB_ID_PERMUTATIONS_NO_TWINS__9064
display_id: REC-002
topics:
- Recursion
- Backtracking
- Strings
---
# Lab ID Permutations With No Adjacent Twins - Editorial

## Problem Summary

You are given a string `s` which may contain duplicate characters. Your task is to generate all unique permutations of `s` such that no two adjacent characters are identical. The permutations must be output in lexicographical order. If no such permutation exists, output `NONE`.


## Constraints

- `1 <= |s| <= 8`
- `s` contains lowercase English letters
## Real-World Scenario

Imagine you are organizing a **Seating Chart** for a dinner party. You have guests from different families (represented by characters 'a', 'b', etc.). You want to arrange them in a line such that no two members of the same family sit next to each other to encourage mingling.

Another example is **Task Scheduling**. You have tasks of type 'A', 'B', 'C'. You want to schedule them sequentially but you cannot run two tasks of the same type back-to-back due to resource locking constraints.

## Problem Exploration

### 1. Generating Permutations
The core of the problem is generating permutations. Since the input string can have duplicates (e.g., "aab"), we must ensure we generate *unique* permutations. A standard way to handle duplicates is to sort the input string first and skip identical adjacent characters during the recursion if the previous one hasn't been used in the current depth.

### 2. The Constraint
The additional constraint is "no adjacent twins". This means if we just placed character 'a', the next character we place cannot be 'a'.

### 3. Lexicographical Order
To ensure the output is sorted, we should iterate through the available characters in alphabetical order. Sorting the input string initially helps with this.

## Approaches

### Approach 1: Generate All and Filter
Generate all unique permutations of the string, store them, and then filter out those that violate the condition. Finally, sort them.
-   **Pros**: Simple to implement if you have a library function for permutations.
-   **Cons**: Very inefficient. For `s="aaaaaaaab"`, there are many permutations, but almost all are invalid. Generating them all is wasteful.

### Approach 2: Backtracking with Pruning (Optimal)
We build the permutation character by character.
-   Maintain a frequency count of available characters (or use a boolean `used` array on the sorted string).
-   At each step, try to append a character.
-   **Pruning Condition 1 (Duplicates)**: If `s[i] == s[i-1]` and `s[i-1]` was not used in the current context (standard permutation logic), skip to avoid duplicate permutations.
-   **Pruning Condition 2 (Adjacency)**: If the character we are about to pick is the same as the *last* character we added to the current permutation, skip it.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public List<String> generatePermutations(String s) {
        List<String> result = new ArrayList<>();
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        boolean[] used = new boolean[chars.length];
        backtrack(chars, used, new StringBuilder(), result);
        return result;
    }

    private void backtrack(char[] chars, boolean[] used, StringBuilder current, List<String> result) {
        if (current.length() == chars.length) {
            result.add(current.toString());
            return;
        }

        for (int i = 0; i < chars.length; i++) {
            // Skip used characters
            if (used[i]) continue;

            // Skip duplicates: if current is same as previous and previous was not used,
            // it means we are in a new branch for the same character value, which leads to duplicates.
            if (i > 0 && chars[i] == chars[i - 1] && !used[i - 1]) continue;

            // Constraint: No adjacent twins
            if (current.length() > 0 && current.charAt(current.length() - 1) == chars[i]) continue;

            used[i] = true;
            current.append(chars[i]);
            backtrack(chars, used, current, result);
            current.deleteCharAt(current.length() - 1);
            used[i] = false;
        }
    }
}
```

### Python

```python
def generate_permutations(s: str) -> list[str]:
    chars = sorted(list(s))
    n = len(chars)
    used = [False] * n
    result = []

    def backtrack(current):
        if len(current) == n:
            result.append("".join(current))
            return

        for i in range(n):
            if used[i]:
                continue
            
            # Skip duplicates
            if i > 0 and chars[i] == chars[i-1] and not used[i-1]:
                continue
            
            # Constraint: No adjacent twins
            if current and current[-1] == chars[i]:
                continue
            
            used[i] = True
            current.append(chars[i])
            backtrack(current)
            current.pop()
            used[i] = False

    backtrack([])
    return result

def main():
    s = input().strip()
    result = generate_permutations(s)
    if result:
        for perm in result:
            print(perm)
    else:
        print("NONE")

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
    vector<string> generatePermutations(string s) {
        vector<string> result;
        sort(s.begin(), s.end());
        string current;
        vector<bool> used(s.length(), false);
        backtrack(s, used, current, result);
        return result;
    }

private:
    void backtrack(const string& s, vector<bool>& used, string& current, vector<string>& result) {
        if (current.length() == s.length()) {
            result.push_back(current);
            return;
        }

        for (int i = 0; i < s.length(); ++i) {
            if (used[i]) continue;

            // Skip duplicates
            if (i > 0 && s[i] == s[i - 1] && !used[i - 1]) continue;

            // Constraint: No adjacent twins
            if (!current.empty() && current.back() == s[i]) continue;

            used[i] = true;
            current.push_back(s[i]);
            backtrack(s, used, current, result);
            current.pop_back();
            used[i] = false;
        }
    }
};
```

### JavaScript

```javascript
class Solution {
  generatePermutations(s) {
    const chars = s.split("").sort();
    const n = chars.length;
    const used = new Array(n).fill(false);
    const result = [];

    const backtrack = (current) => {
      if (current.length === n) {
        result.push(current.join(""));
        return;
      }

      for (let i = 0; i < n; i++) {
        if (used[i]) continue;

        // Skip duplicates
        if (i > 0 && chars[i] === chars[i - 1] && !used[i - 1]) continue;

        // Constraint: No adjacent twins
        if (current.length > 0 && current[current.length - 1] === chars[i]) continue;

        used[i] = true;
        current.push(chars[i]);
        backtrack(current);
        current.pop();
        used[i] = false;
      }
    };

    backtrack([]);
    return result;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:** `aab`

1.  Sort `s`: `['a', 'a', 'b']`.
2.  **Step 1**: Try placing `chars[0]` ('a').
    -   `current` = "a". `used` = `[T, F, F]`.
    -   **Recurse**:
        -   Try `chars[0]` ('a'): Used. Skip.
        -   Try `chars[1]` ('a'): Not used. But `chars[1] == current.back()`. Skip (Constraint).
        -   Try `chars[2]` ('b'): Not used. `b != a`. OK.
            -   `current` = "ab". `used` = `[T, F, T]`.
            -   **Recurse**:
                -   Try `chars[1]` ('a'): Not used. `a != b`. OK.
                    -   `current` = "aba". `used` = `[T, T, T]`.
                    -   Length == 3. Add "aba" to result.
                    -   Backtrack.
3.  **Step 1 Backtrack**: Remove 'a'.
4.  **Step 1**: Try `chars[1]` ('a').
    -   `chars[1] == chars[0]` and `used[0]` is false. Skip (Duplicate pruning).
5.  **Step 1**: Try `chars[2]` ('b').
    -   `current` = "b". `used` = `[F, F, T]`.
    -   **Recurse**:
        -   Try `chars[0]` ('a'): OK.
            -   `current` = "ba".
            -   **Recurse**:
                -   Try `chars[1]` ('a'): `a == a`. Skip (Constraint).
        -   Try `chars[1]` ('a'): Skip (Duplicate pruning).

**Result:** `["aba"]`.

## Proof of Correctness

The algorithm explores the state space of all permutations.
1.  **Completeness**: It tries every character at every position.
2.  **Uniqueness**: The condition `if (i > 0 && chars[i] == chars[i-1] && !used[i-1]) continue` ensures that we only use the first available instance of a duplicate character for a specific position, preventing duplicate permutations.
3.  **Constraint Satisfaction**: The condition `if (!current.empty() && current.back() == s[i]) continue` explicitly prevents adjacent identical characters.
4.  **Order**: By sorting `chars` initially and iterating `i` from 0 to `n-1`, we generate permutations in lexicographical order.

## Interview Extensions

1.  **Can we do this without sorting?**
    -   Yes, using a HashMap to count frequencies. Iterate through keys (sorted keys for lexicographical order). Decrement count when using a char, increment when backtracking. This naturally handles duplicates.

2.  **What is the time complexity?**
    -   Worst case is still factorial `O(N!)`, but pruning significantly reduces the actual number of calls.

3.  **What if we want the K-th valid permutation?**
    -   We would need a more mathematical approach or a counter in the backtracking to stop early.

### Common Mistakes

-   **Missing Duplicate Pruning**: Forgetting the `!used[i-1]` check leads to duplicate outputs like `aba` and `aba`.
-   **Incorrect Constraint Check**: Checking `chars[i] == chars[i-1]` inside the loop without checking `current.back()` is wrong. `chars[i-1]` is just the previous character in the *sorted list*, not necessarily the neighbor in the *permutation*.
-   **String Concatenation**: Using `s + c` in recursion is `O(N)` per step. Using `StringBuilder` or `vector` (push/pop) is `O(1)` amortized.

## Related Concepts

-   **Backtracking**: The fundamental technique.
-   **Permutations**: Standard combinatorial problem.
-   **Pruning**: Optimization technique.
