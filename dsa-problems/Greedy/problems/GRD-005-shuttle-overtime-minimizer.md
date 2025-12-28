---
problem_id: GRD_SHUTTLE_OVERTIME_MINIMIZER__6381
display_id: GRD-005
slug: shuttle-overtime-minimizer
title: "Shuttle Overtime Minimizer"
difficulty: Medium
difficulty_score: 50
topics:
  - Greedy Algorithms
  - Heap
  - Priority Queue
tags:
  - greedy
  - heap
  - priority-queue
  - optimization
  - medium
premium: true
subscription_tier: basic
time_limit: 2000
memory_limit: 256
---

# GRD-005: Shuttle Overtime Minimizer

## Problem Statement

You manage shuttle driver shifts where each shift `i` has:

- A standard length `l[i]` hours (no overtime cost for these hours)
- An overtime cost `p[i]` per hour beyond the standard length

You must cover a total of `H` hours using these shifts. Shifts can be partially used, but any hours beyond the standard length incur overtime costs at rate `p[i]`.

Your goal is to minimize the total overtime cost while covering all `H` hours.

![Problem Illustration](../images/GRD-005/problem-illustration.png)

## Input Format

- First line: two integers `n H` (number of shifts and total hours needed)
- Next `n` lines: two integers `l p` representing standard length and overtime cost per hour for each shift

## Output Format

- Single integer: minimum total overtime cost

## Constraints

- `1 <= n <= 10^5`
- `0 <= l[i], p[i] <= 10^9`
- `1 <= H <= 10^12`
- Total standard hours (sum of all `l[i]`) may be less than, equal to, or greater than `H`

## Example

**Input:**

```
2 8
4 3
2 1
```

**Output:**

```
2
```

**Explanation:**

Shifts:

- Shift 1: 4 standard hours, overtime costs 3 per hour
- Shift 2: 2 standard hours, overtime costs 1 per hour

Total hours needed: 8

Strategy:

Strategy to minimize cost:

1. Use all standard hours first: 4 + 2 = 6 hours (no overtime cost)
2. Need 2 more hours (8 - 6 = 2)
3. For overtime, choose the cheaper rate (shift 2 at cost 1 per hour)
4. Overtime cost: 2 × 1 = 2

Total minimum cost: 2

![Example Visualization](../images/GRD-005/example-1.png)

## Notes

- First use all standard hours from all shifts (these are free)
- For remaining hours, use overtime from shifts with lowest overtime costs
- Use a min-heap to track available overtime costs
- If total standard hours >= H, answer is 0
- Time complexity: O(n log n) for sorting by overtime cost

## Related Topics

Greedy Algorithms, Heap, Priority Queue, Cost Optimization, Resource Allocation

---

## Solution Template

### Java

```java
import java.util.*;

class Solution {
    public long minOvertimeCost(int n, long H, int[][] shifts) {
        // shifts[i] = [length, overtimeCost]
        // Your implementation here
        return 0;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        long H = sc.nextLong();

        int[][] shifts = new int[n][2];
        for (int i = 0; i < n; i++) {
            shifts[i][0] = sc.nextInt(); // length
            shifts[i][1] = sc.nextInt(); // overtime cost
        }

        Solution solution = new Solution();
        System.out.println(solution.minOvertimeCost(n, H, shifts));
        sc.close();
    }
}
```

### Python

```python
from typing import List

def min_overtime_cost(n: int, H: int, shifts: List[List[int]]) -> int:
    # shifts[i] = [length, overtime_cost]
    # Your implementation here
    return 0

def main():
    n, H = map(int, input().split())
    shifts = []
    for _ in range(n):
        l, p = map(int, input().split())
        shifts.append([l, p])

    result = min_overtime_cost(n, H, shifts)
    print(result)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    long long minOvertimeCost(int n, long long H, vector<pair<int,int>>& shifts) {
        // shifts[i] = {length, overtimeCost}
        // Your implementation here
        return 0;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long H;
    cin >> n >> H;

    vector<pair<int,int>> shifts(n);
    for (int i = 0; i < n; i++) {
        cin >> shifts[i].first >> shifts[i].second;
    }

    Solution solution;
    cout << solution.minOvertimeCost(n, H, shifts) << "\n";

    return 0;
}
```

### JavaScript

```javascript
const readline = require("readline");

class Solution {
  minOvertimeCost(n, H, shifts) {
    // shifts[i] = [length, overtimeCost]
    // Your implementation here
    return 0;
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

let data = [];
rl.on("line", (line) => data.push(line.trim()));
rl.on("close", () => {
  let ptr = 0;
  const [n, H] = data[ptr++].split(" ").map(Number);

  const shifts = [];
  for (let i = 0; i < n; i++) {
    const [l, p] = data[ptr++].split(" ").map(Number);
    shifts.push([l, p]);
  }

  const solution = new Solution();
  console.log(solution.minOvertimeCost(n, H, shifts));
});
```
