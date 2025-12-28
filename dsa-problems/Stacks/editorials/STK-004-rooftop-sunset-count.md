---
title: Rooftop Sunset Count
slug: rooftop-sunset-count
difficulty: Easy
difficulty_score: 32
tags:
- Stack
- Monotonic Stack
- Arrays
problem_id: STK_ROOFTOP_SUNSET_COUNT__2974
display_id: STK-004
topics:
- Stack
- Monotonic Stack
- Arrays
---
# Rooftop Sunset Count - Editorial

## Problem Summary

You are given an array of building heights listed from West to East. A building can see the sunset (West) if there are no taller (or equal height) buildings to its left. Count the number of buildings that have a clear view of the sunset.

*Note: The problem statement says "no taller building", which technically implies `h[left] > h[i]` blocks. However, in standard visibility problems, a building of equal height also blocks the view. We will assume the standard interpretation: a building is visible if it is strictly taller than all buildings to its left.*


## Constraints

- `1 <= n <= 200000`
- `0 <= h[i] <= 10^9`
## Real-World Scenario

Imagine you are an **Architect** designing a row of beach houses.
-   The beach and sunset are to the West (left side of the row).
-   Every house wants a sunset view.
-   If you build a 2-story house, and there is a 5-story hotel to its left, the house gets no view.
-   If you build a 6-story tower, it can see over the 5-story hotel.
-   You want to calculate how many of your proposed designs actually get the premium "Sunset View" label.

## Problem Exploration

### 1. Visibility Condition
-   A building at index `i` can see the sunset if `h[i] > h[j]` for all `j < i`.
-   This is equivalent to saying `h[i] > max(h[0], h[1], ..., h[i-1])`.

### 2. Running Maximum
-   We can iterate through the buildings from West to East (Left to Right).
-   Maintain a variable `current_max` representing the height of the tallest building seen so far.
-   For each building `h[i]`:
    -   If `h[i] > current_max`, it is visible. Increment count. Update `current_max = h[i]`.
    -   Else, it is blocked.
-   This approach is intuitive and efficient.

### 3. Stack Approach (Alternative)
-   While a simple linear scan works for "Sunset (West)", a **Monotonic Stack** is often used for more complex visibility problems (e.g., "Which building does this one look at?").
-   If we wanted to find buildings visible from the **East**, we could use a Monotonic Stack processing Left-to-Right:
    -   Maintain a stack of buildings that are candidates for East-view.
    -   When a new building comes, it blocks smaller buildings to its left from seeing the East.
    -   Pop elements from stack that are `<= current_height`.
    -   Push current building.
    -   The stack at the end contains buildings visible from the East.
-   However, for "Sunset (West)", the Running Max is sufficient and optimal.

## Approaches

### Approach 1: Running Maximum (Greedy)
-   Initialize `count = 0` and `max_height = -1` (or 0).
-   Iterate `h` in `heights`:
    -   If `h > max_height`:
        -   `count++`
        -   `max_height = h`
-   Complexity: `O(N)` time, `O(1)` space.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public int countVisible(int[] h) {
        int count = 0;
        int maxH = -1; // Assuming heights are non-negative
        
        for (int height : h) {
            if (height > maxH) {
                count++;
                maxH = height;
            }
        }
        return count;
    }
}
```

### Python

```python
def count_visible(h: list[int]) -> int:
    """Count buildings that can see sunset (no taller building to the right)"""
    count = 0
    max_height = -1
    
    # Process from right to left
    for height in reversed(h):
        if height > max_height:
            count += 1
            max_height = height
    
    return count

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    heights = list(map(int, lines[1].split()))
    
    print(count_visible(heights))

if __name__ == "__main__":
    main()

```

### C++

```cpp
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    int countVisible(const vector<int>& h) {
        int count = 0;
        int maxH = -1;
        
        for (int height : h) {
            if (height > maxH) {
                count++;
                maxH = height;
            }
        }
        return count;
    }
};
```

### JavaScript

```javascript
class Solution {
  countVisible(h) {
    let count = 0;
    let maxH = -1;
    
    for (const height of h) {
      if (height > maxH) {
        count++;
        maxH = height;
      }
    }
    return count;
  }
}
```

### Python

```python

def rooftop_sunset_count(heights):
    stack = []
    count = 0
    
    for h in heights:
        while stack and stack[-1] <= h:
            stack.pop()
        stack.append(h)
    
    return len(stack)

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    heights = list(map(int, lines[1].split()))
    
    print(rooftop_sunset_count(heights))

if __name__ == "__main__":
    main()

```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:** `2 5 2 6 1`

1.  `h=2`: `2 > -1`. Count=1. `maxH=2`. (Visible)
2.  `h=5`: `5 > 2`. Count=2. `maxH=5`. (Visible)
3.  `h=2`: `2 <= 5`. Blocked.
4.  `h=6`: `6 > 5`. Count=3. `maxH=6`. (Visible)
5.  `h=1`: `1 <= 6`. Blocked.

**Result:** 3.

## Proof of Correctness

-   **Necessary Condition**: A building must be taller than *all* preceding buildings to see over them.
-   **Sufficient Condition**: If a building is taller than the *maximum* of all preceding buildings, it is taller than *all* of them.
-   **Greedy Update**: By updating `maxH` only when we find a new tallest building, we correctly maintain the blocking threshold.

## Interview Extensions

1.  **List Indices**: Return the indices of visible buildings instead of count.
    -   *Solution*: Store indices in a list whenever `count` increments.
2.  **Visible from East**: Count buildings visible from the East (Sunrise).
    -   *Solution*: Scan Right-to-Left with Running Max, or Left-to-Right with Monotonic Stack.
3.  **Tallest Visible**: Find the tallest building that is visible.
    -   *Solution*: Just `max(h)`. The global maximum is always visible (unless blocked by an earlier global max of equal height).

### Common Mistakes

-   **Strict Inequality**: Using `>=` instead of `>`. Usually, equal height blocks the view.
-   **Direction**: Confusing West (Left) and East (Right).
-   **Initialization**: Setting `maxH = 0` is fine if heights are positive, but `-1` or `-infinity` is safer for general inputs.
