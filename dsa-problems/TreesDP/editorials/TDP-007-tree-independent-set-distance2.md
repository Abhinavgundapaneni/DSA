---

title: Distance-2 Independent Set on Tree
problem_id: TDP_DISTANCE2_INDEPENDENT_SET__8395
display_id: TDP-007
difficulty: Medium
tags:
  - Tree DP
  - Independent Set
  - Optimization
editorial_categories:
  - Algorithms
  - Data Structures
slug: tree-independent-set-distance2
---


# Distance-2 Independent Set on Tree

## 📋 Problem Summary

Given a tree with `n` nodes where each node has a weight, find the **maximum total weight** of a subset of nodes such that any two chosen nodes are at distance **at least 3** (no adjacency and no common neighbor).

### Constraints

- `1 <= n <= 2 x 10^5`
- `1 <= w[i] <= 10^9`

## 🌍 Real-World Scenario

**Cell Tower Placement:**

- Each location has a value (population coverage potential)
- Towers must be placed far apart to avoid interference
- Distance-2 constraint: no adjacent towers, no towers sharing a common junction
- Goal: Maximize total population coverage

## 🔍 Naive Approach

### Algorithm

```
function max_independent_set_d2_naive():
    max_value = 0

    // Step 1: Try all subsets
    for subset in all_subsets(vertices):
        // Step 2: Check distance-2 constraint
        valid = true
        for u in subset:
            for v in subset:
                if u != v and distance(u, v) <= 2:
                    valid = false
                    break

        // Step 3: Calculate value
        if valid:
            value = sum of weights in subset
            max_value = max(max_value, value)

    return max_value
```

### Complexity Analysis

| Phase            | Time             | Space    | Explanation         |
| ---------------- | ---------------- | -------- | ------------------- |
| Generate subsets | O(2^n)           | O(n)     | All 2^n subsets     |
| Distance check   | O(n²) per subset | O(n)     | All pairs in subset |
| **Naive Total**  | **O(2^n · n²)**  | **O(n)** | Exponential         |

**Why This Complexity:**

- 2^n subsets, each requires O(n²) distance checks
- For n = 20: billions of operations
- Completely infeasible for n = 200K

## 💡 Optimal Approach: Extended State DP

### DP States

For each node `u`, track three states based on its relationship to selected nodes:

- `dp[u][0]` = u NOT selected, and no child is selected
- `dp[u][1]` = u NOT selected, but at least one child is selected
- `dp[u][2]` = u IS selected

### Recurrence

**dp[u][2] (u selected):**

- All children must be in state 0 (not selected, no grandchild selected)

```
dp[u][2] = w[u] + Σ dp[child][0]
```

**dp[u][0] (u not selected, no child selected):**

- All children in state 0 or 1, but none in state 2

```
dp[u][0] = Σ max(dp[child][0], dp[child][1])
```

**dp[u][1] (u not selected, at least one child selected):**

- At least one child must be in state 2
- Others can be in state 0, 1, or 2

```
dp[u][1] = max over configurations where at least one child is in state 2
```

### Algorithm

```
function max_independent_set_d2_dp():
    function dfs(u, parent):
        dp[u][0] = 0  // u not selected, no child selected
        dp[u][1] = 0  // u not selected, ≥1 child selected
        dp[u][2] = w[u]  // u selected

        sum_no_child = 0
        max_with_child = 0

        for child in adj[u]:
            if child != parent:
                dfs(child, u)

                dp[u][2] += dp[child][0]  // u selected → child state 0
                sum_no_child += max(dp[child][0], dp[child][1])
                max_with_child = max(max_with_child,
                                     dp[child][2] - max(dp[child][0], dp[child][1]))

        dp[u][0] = sum_no_child
        dp[u][1] = sum_no_child + max_with_child

    dfs(1, -1)
    return max(dp[1][0], dp[1][1], dp[1][2])
```

### Complexity Analysis

| Phase             | Time          | Space    | Explanation          |
| ----------------- | ------------- | -------- | -------------------- |
| DFS traversal     | O(n)          | O(h)     | Visit each node once |
| Process children  | O(d) per node | O(1)     | d = degree           |
| DP storage        | -             | O(n)     | 3 states × n nodes   |
| **Optimal Total** | **O(n)**      | **O(n)** | Linear               |

**Why This Is Optimal:**

- Each node visited once in post-order DFS
- 3 states sufficient to capture all constraints
- For n = 200K: ~600K operations vs ~10^60K naive

## 💻 Implementation

### Java

```java
import java.util.*;

public class Distance2IndependentSet {
    static List<Integer>[] graph;
    static long[] weight;
    static long[][] dp;
    static int n;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();

        weight = new long[n + 1];
        for (int i = 1; i <= n; i++) {
            weight[i] = sc.nextLong();
        }

        graph = new ArrayList[n + 1];
        for (int i = 0; i <= n; i++) {
            graph[i] = new ArrayList<>();
        }

        for (int i = 0; i < n - 1; i++) {
            int u = sc.nextInt();
            int v = sc.nextInt();
            graph[u].add(v);
            graph[v].add(u);
        }

        dp = new long[n + 1][3];

        dfs(1, -1);

        long result = Math.max(dp[1][0], Math.max(dp[1][1], dp[1][2]));
        System.out.println(result);

        sc.close();
    }

    static void dfs(int u, int parent) {
        dp[u][0] = 0;
        dp[u][1] = 0;
        dp[u][2] = weight[u];

        long sumWithoutSelected = 0;
        long maxGain = Long.MIN_VALUE;

        for (int v : graph[u]) {
            if (v == parent) continue;

            dfs(v, u);

            long bestNotSelected = Math.max(dp[v][0], dp[v][1]);
            sumWithoutSelected += bestNotSelected;

            long gain = dp[v][2] - bestNotSelected;
            maxGain = Math.max(maxGain, gain);

            dp[u][2] += dp[v][0];
        }

        dp[u][0] = sumWithoutSelected;

        if (maxGain > Long.MIN_VALUE) {
            dp[u][1] = sumWithoutSelected + maxGain;
        }
    }
}
```

### Python

```python
import sys
sys.setrecursionlimit(300000)

def solve():
    n = int(input())
    weight = [0] + list(map(int, input().split()))

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    dp = [[0, 0, 0] for _ in range(n + 1)]

    def dfs(u, parent):
        dp[u][0] = 0
        dp[u][1] = 0
        dp[u][2] = weight[u]

        sum_without_selected = 0
        max_gain = float('-inf')

        for v in graph[u]:
            if v == parent:
                continue

            dfs(v, u)

            best_not_selected = max(dp[v][0], dp[v][1])
            sum_without_selected += best_not_selected

            gain = dp[v][2] - best_not_selected
            max_gain = max(max_gain, gain)

            dp[u][2] += dp[v][0]

        dp[u][0] = sum_without_selected

        if max_gain > float('-inf'):
            dp[u][1] = sum_without_selected + max_gain

    dfs(1, -1)

    result = max(dp[1][0], dp[1][1], dp[1][2])
    print(result)

def main():
    solve()

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
vector<int> graph[MAXN];
long long weight[MAXN];
long long dp[MAXN][3];
int n;

void dfs(int u, int parent) {
    dp[u][0] = 0;
    dp[u][1] = 0;
    dp[u][2] = weight[u];

    long long sumWithoutSelected = 0;
    long long maxGain = LLONG_MIN;

    for (int v : graph[u]) {
        if (v == parent) continue;

        dfs(v, u);

        long long bestNotSelected = max(dp[v][0], dp[v][1]);
        sumWithoutSelected += bestNotSelected;

        long long gain = dp[v][2] - bestNotSelected;
        maxGain = max(maxGain, gain);

        dp[u][2] += dp[v][0];
    }

    dp[u][0] = sumWithoutSelected;

    if (maxGain > LLONG_MIN) {
        dp[u][1] = sumWithoutSelected + maxGain;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> n;

    for (int i = 1; i <= n; i++) {
        cin >> weight[i];
    }

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    dfs(1, -1);

    long long result = max({dp[1][0], dp[1][1], dp[1][2]});
    cout << result << endl;

    return 0;
}
```

### JavaScript

```javascript
const readline = require("readline");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

let lines = [];
rl.on("line", (line) => {
  lines.push(line);
}).on("close", () => {
  solve();
});

function solve() {
  let idx = 0;
  const n = parseInt(lines[idx++]);

  const weight = [0, ...lines[idx++].split(" ").map(Number)];

  const graph = Array.from({ length: n + 1 }, () => []);

  for (let i = 0; i < n - 1; i++) {
    const [u, v] = lines[idx++].split(" ").map(Number);
    graph[u].push(v);
    graph[v].push(u);
  }

  const dp = Array.from({ length: n + 1 }, () => [0, 0, 0]);

  function dfs(u, parent) {
    dp[u][0] = 0;
    dp[u][1] = 0;
    dp[u][2] = weight[u];

    let sumWithoutSelected = 0;
    let maxGain = -Infinity;

    for (const v of graph[u]) {
      if (v === parent) continue;

      dfs(v, u);

      const bestNotSelected = Math.max(dp[v][0], dp[v][1]);
      sumWithoutSelected += bestNotSelected;

      const gain = dp[v][2] - bestNotSelected;
      maxGain = Math.max(maxGain, gain);

      dp[u][2] += dp[v][0];
    }

    dp[u][0] = sumWithoutSelected;

    if (maxGain > -Infinity) {
      dp[u][1] = sumWithoutSelected + maxGain;
    }
  }

  dfs(1, -1);

  const result = Math.max(dp[1][0], dp[1][1], dp[1][2]);
  console.log(result);
}
```

---

## 🧪 Test Case Walkthrough (Dry Run)

### Input

```
7
10 20 30 40 50 60 70
1 2
1 3
2 4
2 5
3 6
3 7
```

### Visual Representation

```
Tree with weights:
        1 (10)
       / \
   2(20) 3(30)
   / \   / \
4(40)5(50)6(60)7(70)

Constraint: Selected nodes must be at distance ≥ 3
(at least 2 nodes between any two selected)
```

### Valid Selections

| Selection    | Distance Check | Total Weight  |
| ------------ | -------------- | ------------- |
| {4, 6}       | d(4,6)=4 ✓     | 40+60=100     |
| {4, 7}       | d(4,7)=4 ✓     | 40+70=110     |
| {5, 6}       | d(5,6)=4 ✓     | 50+60=110     |
| {5, 7}       | d(5,7)=4 ✓     | 50+70=**120** |
| {4, 5, 6, 7} | d(4,5)=2 ❌    | Invalid       |

**Answer: 120** (select nodes 5 and 7)

**Output:** `120`

---

## ⚠️ Common Mistakes to Avoid

| #   | Mistake            | ❌ Wrong                         | ✅ Correct                         |
| --- | ------------------ | -------------------------------- | ---------------------------------- |
| 1   | **Use 2 states**   | dp[u][0/1] like regular IS       | Need 3 states for dist-2           |
| 2   | **Wrong distance** | Adjacent = distance 2            | Adjacent = distance 1              |
| 3   | **Miss max gain**  | Don't track best child to select | Track `maxGain` over children      |
| 4   | **Init maxGain**   | `maxGain = 0`                    | `maxGain = -INF` (may be negative) |

### State Explanation:

```
dp[u][0] = u not selected, no child selected
dp[u][1] = u not selected, some child selected
dp[u][2] = u IS selected

When u is selected (dp[u][2]):
- All children must be in state 0 (not selected, no grandchild selected)
- Because distance(u, grandchild) = 2 < 3
```

---

## 🔗 Related Concepts

- **Maximum Independent Set:** Distance-1 constraint (no adjacent)
- **Dominating Set:** Every node covered or adjacent to selected
- **Tree Matching:** Pairing adjacent nodes
