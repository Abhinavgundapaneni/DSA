---
id: STR-014
title: Shortest Covering Window for Set
sidebar_label: STR-014 - Shortest Covering Window for Set
tags:
- strings
- sliding-window
- hashmap
- medium
difficulty: Medium
difficulty_score: 41
problem_id: STR_SHORTEST_COVERING_WINDOW_SET__1014
display_id: STR-014
slug: shortest-covering-window-set
topics:
- String Array
- Sliding Window
- Hashing
---
# STR-014: Shortest Covering Window for Set

## 📋 Problem Summary

**Input**: Array of strings `arr`, set of required strings `T`  
**Output**: Length and one shortest contiguous subarray covering all strings in `T`  
**Constraints**: `1 <= |arr| <= 10^5`, `|T| <= 10^3`

## 🌍 Real-World Scenario

Document search needs to find the smallest text window containing all query keywords. Minimizing window size helps extract concise, relevant excerpts for search results.

## Detailed Explanation

**Covering Window**: Contiguous subarray of `arr` whose set of elements ⊇ T

**Goal**: Find shortest such window

**Example**: `arr=["db","aa","cc","db","aa","cc"]`, `T={"aa","cc"}`

- Window [1:3] = ["aa","cc"] → length 2, covers all ✓
- Window [4:6] = ["aa","cc"] → length 2, covers all ✓
- Shortest: length 2

## Naive Approach

```
1. For each starting position i:
   a. For each ending position j >= i:
      - Check if arr[i:j+1] covers T
      - Track minimum length
```

### Time Complexity: **O(n³)**

- n² windows
- O(n) to check coverage

### Space Complexity: **O(n)**

- Set for coverage check

## Optimal Approach

**Sliding Window with Frequency Map**:

1. Expand window until all elements of T are covered
2. Contract window while maintaining coverage
3. Track minimum window

**Algorithm**:

```
1. required = Counter(T)  # T elements with count (all 1 for set)
2. window_counts = {}
3. left = 0, right = 0
4. formed = 0  # Number of unique T elements fully covered
5. min_len = infinity, result_window = None
6. While right < n:
   a. char = arr[right]
   b. window_counts[char]++
   c. If char in required and window_counts[char] == 1:
      formed++
   d. While formed == |T| (all covered):
      - Update min_len and result if better
      - Remove arr[left] from window
      - If removed element in required and count becomes 0:
         formed--
      - left++
   e. right++
7. Return (min_len, result_window)
```

### Time Complexity

| Phase             | Operations                 | Cost     |
| ----------------- | -------------------------- | -------- |
| Expand window     | Right pointer scans n      | O(n)     |
| Contract window   | Left pointer scans n total | O(n)     |
| Frequency updates | O(1) per operation         | O(1)     |
| **Total**         |                            | **O(n)** |

### Space Complexity

| Component     | Space | Justification |
| ------------- | ----- | ------------- | --- | ------- | --- | ----------------- |
| required map  | O(    | T             | )   | At most | T   | unique elements   |
| window_counts | O(    | T             | )   | At most | T   | relevant elements |
| **Total**     |       | \*\*O(        | T   | )\*\*   |

## 💻 Implementation

### Python

```python
def shortest_covering_window(arr: list[str], T: set[str]) -> tuple[int, list[str]]:
    if not arr or not T:
        return (0, [])

    required = {s: 1 for s in T}
    window_counts = {}

    left = 0
    formed = 0  # Unique T elements covered
    min_len = float('inf')
    result_left, result_right = 0, 0

    for right in range(len(arr)):
        char = arr[right]
        window_counts[char] = window_counts.get(char, 0) + 1

        # Check if this char is in T and newly covered
        if char in required and window_counts[char] == 1:
            formed += 1

        # Contract window while all elements covered
        while formed == len(T) and left <= right:
            # Update result if better
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result_left, result_right = left, right

            # Remove leftmost element
            left_char = arr[left]
            window_counts[left_char] -= 1
            if left_char in required and window_counts[left_char] == 0:
                formed -= 1

            left += 1

    if min_len == float('inf'):
        return (0, [])

    return (min_len, arr[result_left:result_right + 1])

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    arr = lines[1:n+1]
    k = int(lines[n+1])
    T = set(lines[n+2:n+2+k])
    count, window = shortest_covering_window(arr, T)
    print(count)
    for item in window:
        print(item)

if __name__ == "__main__":
    main()

```

### Java

```java
class Solution {
    public Object[] shortestCoveringWindow(String[] arr, Set<String> T) {
        if (arr == null || arr.length == 0 || T == null || T.isEmpty()) {
            return new Object[]{0, new String[]{}};
        }

        Map<String, Integer> required = new HashMap<>();
        for (String s : T) {
            required.put(s, 1);
        }

        Map<String, Integer> windowCounts = new HashMap<>();
        int left = 0, formed = 0;
        int minLen = Integer.MAX_VALUE;
        int resultLeft = 0, resultRight = 0;

        for (int right = 0; right < arr.length; right++) {
            String s = arr[right];
            windowCounts.put(s, windowCounts.getOrDefault(s, 0) + 1);

            if (required.containsKey(s) && windowCounts.get(s) == 1) {
                formed++;
            }

            while (formed == T.size() && left <= right) {
                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    resultLeft = left;
                    resultRight = right;
                }

                String leftS = arr[left];
                windowCounts.put(leftS, windowCounts.get(leftS) - 1);
                if (required.containsKey(leftS) && windowCounts.get(leftS) == 0) {
                    formed--;
                }

                left++;
            }
        }

        if (minLen == Integer.MAX_VALUE) {
            return new Object[]{0, new String[]{}};
        }

        String[] resultWindow = new String[minLen];
        System.arraycopy(arr, resultLeft, resultWindow, 0, minLen);
        return new Object[]{minLen, resultWindow};
    }
}
```

### C++

```cpp
class Solution {
public:
    pair<int, vector<string>> shortestCoveringWindow(vector<string>& arr, unordered_set<string>& T) {
        if (arr.empty() || T.empty()) {
            return {0, {}};
        }

        unordered_map<string, int> required;
        for (const string& s : T) {
            required[s] = 1;
        }

        unordered_map<string, int> windowCounts;
        int left = 0, formed = 0;
        int minLen = INT_MAX;
        int resultLeft = 0, resultRight = 0;

        for (int right = 0; right < arr.size(); right++) {
            string s = arr[right];
            windowCounts[s]++;

            if (required.count(s) && windowCounts[s] == 1) {
                formed++;
            }

            while (formed == (int)T.size() && left <= right) {
                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    resultLeft = left;
                    resultRight = right;
                }

                string leftS = arr[left];
                windowCounts[leftS]--;
                if (required.count(leftS) && windowCounts[leftS] == 0) {
                    formed--;
                }

                left++;
            }
        }

        if (minLen == INT_MAX) {
            return {0, {}};
        }

        vector<string> resultWindow(arr.begin() + resultLeft, arr.begin() + resultRight + 1);
        return {minLen, resultWindow};
    }
};
```

### JavaScript

```javascript
function shortestCoveringWindow(arr, T) {
  if (!arr || arr.length === 0 || !T || T.size === 0) {
    return [0, []];
  }

  const required = new Map();
  for (let s of T) {
    required.set(s, 1);
  }

  const windowCounts = new Map();
  let left = 0,
    formed = 0;
  let minLen = Infinity;
  let resultLeft = 0,
    resultRight = 0;

  for (let right = 0; right < arr.length; right++) {
    const s = arr[right];
    windowCounts.set(s, (windowCounts.get(s) || 0) + 1);

    if (required.has(s) && windowCounts.get(s) === 1) {
      formed++;
    }

    while (formed === T.size && left <= right) {
      if (right - left + 1 < minLen) {
        minLen = right - left + 1;
        resultLeft = left;
        resultRight = right;
      }

      const leftS = arr[left];
      windowCounts.set(leftS, windowCounts.get(leftS) - 1);
      if (required.has(leftS) && windowCounts.get(leftS) === 0) {
        formed--;
      }

      left++;
    }
  }

  if (minLen === Infinity) {
    return [0, []];
  }

  return [minLen, arr.slice(resultLeft, resultRight + 1)];
}
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input**: `arr=["db","aa","cc","db","aa","cc"]`, `T={"aa","cc"}`

**Execution**:

```
required = {aa:1, cc:1}

right=0: arr[0]="db", windowCounts={db:1}, formed=0

right=1: arr[1]="aa", windowCounts={db:1,aa:1}, formed=1

right=2: arr[2]="cc", windowCounts={db:1,aa:1,cc:1}, formed=2
  formed==2 (all covered):
    Window [0:2] length=3, update minLen=3, result=[0,2]
    Remove arr[0]="db": windowCounts={db:0,aa:1,cc:1}, formed=2, left=1
    Window [1:2] length=2, update minLen=2, result=[1,2]
    Remove arr[1]="aa": windowCounts={db:0,aa:0,cc:1}, formed=1, left=2

right=3: arr[3]="db", windowCounts={db:1,aa:0,cc:1}, formed=1

right=4: arr[4]="aa", windowCounts={db:1,aa:1,cc:1}, formed=2
  formed==2:
    Window [2:4] length=3, minLen=2 (no update)
    Remove arr[2]="cc": formed=1, left=3

right=5: arr[5]="cc", windowCounts={db:1,aa:1,cc:1}, formed=2
  formed==2:
    Window [3:5] length=3, minLen=2 (no update)
    Remove arr[3]="db": formed=2, left=4
    Window [4:5] length=2, minLen=2 (no update, could update)
    Remove arr[4]="aa": formed=1, left=5

Final: minLen=2, window=arr[1:3]=["aa","cc"]
```

**Output**: `(2, ["aa","cc"])`

## ⚠️ Common Mistakes to Avoid

1. **Not Using Set for T**: Store T elements for O(1) lookup
2. **Wrong Formed Count**: Track unique T elements covered, not total
3. **Infinite Loop**: Ensure left pointer advances
4. **Window Extraction**: Include both left and right indices
5. **Empty Result**: Handle case where no covering window exists

## 💡 Key Takeaways

1. **Sliding Window Pattern**: Expand-contract for substring problems
2. **Two Pointers**: Efficient O(n) solution
3. **Frequency Tracking**: Map for required and window counts
4. **Formed Count**: Optimization to avoid checking full coverage each time
5. **Edge Cases**: Empty array, T not in array, multiple minimum windows


## Constraints

- `1 ≤ |arr| ≤ 10^5`
- `|T| ≤ 10^3`