---

title: Max Path Sum with Length Limit
problem_id: TDP_MAX_PATH_SUM_LENGTH_LIMIT__6382
display_id: TDP-005
difficulty: Medium
tags:
  - Tree DP
  - Path Algorithms
  - Constrained Optimization
editorial_categories:
  - Algorithms
  - Data Structures
slug: max-path-sum-length-limit
---


# Max Path Sum with Length Limit

## 📋 Problem Summary

Given a tree with `n` nodes where each node has a value (possibly negative), find the maximum path sum where the path uses **at most `L` edges**.

A path is a sequence of distinct nodes where consecutive nodes are connected by an edge. The path sum is the sum of values of all nodes in the path.

### Constraints

- `1 <= n <= 2 x 10^5`
- `1 <= L <= n-1`
- `-10^9 <= values[i] <= 10^9`
- The graph forms a valid tree

## 🌍 Real-World Scenario

**Supply Chain Optimization:**
Imagine a distribution network where:

- Each warehouse has a profit/loss value (inventory value - operating cost)
- You want to establish a distribution route with maximum profit
- Route length is limited by delivery time constraints (max `L` stops)
- Negative values represent warehouses with high costs but strategic locations

**Applications:**

- Maximum profit route within delivery time window
- Investment portfolio with limited number of assets
- Network resource allocation with hop constraints

## 🔍 Naive Approach

### Algorithm

```
function max_path_naive():
    max_sum = -infinity

    // Step 1: Enumerate all node pairs
    for u from 1 to n:
        for v from u to n:
            // Step 2: Find path from u to v
            path = find_path(u, v)

            // Step 3: Check length constraint
            if path.length <= L:
                sum = calculate_sum(path)
                max_sum = max(max_sum, sum)

    return max_sum

function find_path(u, v):
    // BFS or DFS to find unique path in tree
    parent = bfs_parent_tracking(u)
    path = reconstruct_path(v, parent)
    return path
```

### Complexity Analysis

| Phase           | Time      | Space    | Explanation         |
| --------------- | --------- | -------- | ------------------- |
| Node pairs      | O(n²)     | O(1)     | n(n+1)/2 pairs      |
| Path finding    | O(n)      | O(n)     | BFS per pair        |
| Sum calculation | O(L)      | O(1)     | Iterate path        |
| **Naive Total** | **O(n³)** | **O(n)** | n² pairs × O(n) BFS |

**Why This Complexity:**

- For each of n² pairs, run O(n) BFS
- For n = 200,000: ~8 trillion operations (infeasible)
- Redundant: Many paths computed multiple times

**Limitations:**

- Enumerates all possible paths redundantly
- Doesn't leverage tree structure
- For n = 200,000: ~8 trillion operations

## 💡 Optimal Approach: DP with Length Tracking

### Key Insight

For each node `u`, maintain DP state:

- `dp[u][len]` = maximum sum of downward path from `u` using exactly `len` edges

To find maximum path passing through node `u`:

- Combine two best downward paths from different children
- Ensure total length ≤ L

### Algorithm

**Phase 1: Compute Downward DP**

```
function compute_downward_dp():
    function dfs(u, parent):
        // Base case: path of length 0 is just the node
        dp[u][0] = value[u]

        for child in adj[u]:
            if child != parent:
                dfs(child, u)

                // Extend paths from child
                for k from 0 to L-1:
                    dp[u][k+1] = max(dp[u][k+1],
                                     dp[child][k] + value[u])

    dfs(root, -1)
```

**Phase 2: Combine Paths Through Each Node**

```
function combine_paths():
    max_sum = -infinity

    for u from 1 to n:
        // Path entirely in one subtree
        for len from 0 to L:
            max_sum = max(max_sum, dp[u][len])

        // Path through u (two branches)
        for each pair of children (c1, c2):
            for len1 from 0 to L:
                for len2 from 0 to L-len1:
                    if len1 + len2 <= L:
                        path_sum = dp[c1][len1] + dp[c2][len2] + value[u]
                        max_sum = max(max_sum, path_sum)

    return max_sum
```

### Complexity Analysis

| Phase             | Time              | Space      | Explanation                   |
| ----------------- | ----------------- | ---------- | ----------------------------- |
| DFS traversal     | O(n)              | O(h)       | Visit each node once          |
| Extend paths      | O(L) per child    | -          | Update dp[u][0..L]            |
| **Phase 1 Total** | **O(n·L)**        | **O(n·L)** | n nodes × L lengths           |
| Combine paths     | O(L²·d²) per node | O(1)       | d = degree, pairs of children |
| **Phase 2 Total** | **O(n·L²)**       | **O(1)**   | Worst case all pairs          |
| **Overall**       | **O(n·L²)**       | **O(n·L)** | Dominated by Phase 2          |

**Why This Is Optimal:**

- Each edge visited once in DFS
- Path combination is O(L²) per node (amortized)
- For n = 200K, L = 10: ~200M operations vs ~8T naive

## 💻 Implementation

### Java

```java
import java.util.*;

public class MaxPathSumLengthLimit {
    static class Edge {
        int to;
        Edge(int to) {
            this.to = to;
        }
    }

    static List<Edge>[] graph;
    static long[] value;
    static long[][] dp;
    static long maxSum;
    static int n, L;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();
        L = sc.nextInt();

        value = new long[n + 1];
        for (int i = 1; i <= n; i++) {
            value[i] = sc.nextLong();
        }

        graph = new ArrayList[n + 1];
        for (int i = 0; i <= n; i++) {
            graph[i] = new ArrayList<>();
        }

        for (int i = 0; i < n - 1; i++) {
            int u = sc.nextInt();
            int v = sc.nextInt();
            graph[u].add(new Edge(v));
            graph[v].add(new Edge(u));
        }

        dp = new long[n + 1][L + 1];
        for (int i = 0; i <= n; i++) {
            Arrays.fill(dp[i], Long.MIN_VALUE / 2);
        }

        maxSum = Long.MIN_VALUE;

        dfs(1, -1);

        // Also consider single node paths
        for (int i = 1; i <= n; i++) {
            maxSum = Math.max(maxSum, value[i]);
        }

        System.out.println(maxSum);
        sc.close();
    }

    static void dfs(int u, int parent) {
        dp[u][0] = value[u];
        maxSum = Math.max(maxSum, value[u]);

        List<long[]> childPaths = new ArrayList<>();

        for (Edge e : graph[u]) {
            int v = e.to;
            if (v == parent) continue;

            dfs(v, u);

            // Extend paths from child
            long[] childBest = new long[L + 1];
            Arrays.fill(childBest, Long.MIN_VALUE / 2);

            for (int len = 0; len < L; len++) {
                if (dp[v][len] > Long.MIN_VALUE / 2) {
                    long extended = dp[v][len] + value[u];
                    dp[u][len + 1] = Math.max(dp[u][len + 1], extended);
                    childBest[len] = dp[v][len];
                }
            }

            childPaths.add(childBest);
        }

        // Update max with single downward path
        for (int len = 0; len <= L; len++) {
            maxSum = Math.max(maxSum, dp[u][len]);
        }

        // Combine two paths through this node
        for (int i = 0; i < childPaths.size(); i++) {
            for (int j = i + 1; j < childPaths.size(); j++) {
                long[] path1 = childPaths.get(i);
                long[] path2 = childPaths.get(j);

                for (int len1 = 0; len1 <= L; len1++) {
                    for (int len2 = 0; len2 <= L; len2++) {
                        // Total edges: len1 + 1 (to u) + 1 (from u) + len2
                        if (len1 + len2 + 2 > L) continue;
                        if (path1[len1] > Long.MIN_VALUE / 2 &&
                            path2[len2] > Long.MIN_VALUE / 2) {
                            long combined = path1[len1] + path2[len2] + value[u];
                            maxSum = Math.max(maxSum, combined);
                        }
                    }
                }
            }
        }
    }
}
```

### Python

```python
import sys
sys.setrecursionlimit(300000)

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0

    n = int(data[idx])
    L = int(data[idx + 1])
    idx += 2

    value = [0] * (n + 1)
    for i in range(1, n + 1):
        value[i] = int(data[idx])
        idx += 1

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        graph[u].append(v)
        graph[v].append(u)

    dp = [[float('-inf')] * (L + 1) for _ in range(n + 1)]
    max_sum = [float('-inf')]

    def dfs(u, parent):
        dp[u][0] = value[u]
        max_sum[0] = max(max_sum[0], value[u])

        child_paths = []

        for v in graph[u]:
            if v == parent:
                continue

            dfs(v, u)

            child_best = [float('-inf')] * (L + 1)

            for length in range(L):
                if dp[v][length] > float('-inf') / 2:
                    extended = dp[v][length] + value[u]
                    dp[u][length + 1] = max(dp[u][length + 1], extended)
                    child_best[length] = dp[v][length]

            child_paths.append(child_best)

        for length in range(L + 1):
            max_sum[0] = max(max_sum[0], dp[u][length])

        for i in range(len(child_paths)):
            for j in range(i + 1, len(child_paths)):
                path1 = child_paths[i]
                path2 = child_paths[j]

                for len1 in range(L + 1):
                    for len2 in range(L + 1):
                        # Total edges: len1 + 1 (to u) + 1 (from u) + len2
                        if len1 + len2 + 2 > L:
                            continue
                        if (path1[len1] > float('-inf') / 2 and
                            path2[len2] > float('-inf') / 2):
                            combined = path1[len1] + path2[len2] + value[u]
                            max_sum[0] = max(max_sum[0], combined)

    dfs(1, -1)
    print(max_sum[0])

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
const long long NEG_INF = LLONG_MIN / 2;

vector<int> graph[MAXN];
long long value[MAXN];
long long dp[MAXN][505];
long long maxSum;
int n, L;

void dfs(int u, int parent) {
    dp[u][0] = value[u];
    maxSum = max(maxSum, value[u]);

    vector<vector<long long>> childPaths;

    for (int v : graph[u]) {
        if (v == parent) continue;

        dfs(v, u);

        vector<long long> childBest(L + 1, NEG_INF);

        for (int len = 0; len < L; len++) {
            if (dp[v][len] > NEG_INF) {
                long long extended = dp[v][len] + value[u];
                dp[u][len + 1] = max(dp[u][len + 1], extended);
                childBest[len] = dp[v][len];
            }
        }

        childPaths.push_back(childBest);
    }

    for (int len = 0; len <= L; len++) {
        maxSum = max(maxSum, dp[u][len]);
    }

    for (int i = 0; i < (int)childPaths.size(); i++) {
        for (int j = i + 1; j < (int)childPaths.size(); j++) {
            auto& path1 = childPaths[i];
            auto& path2 = childPaths[j];

            for (int len1 = 0; len1 <= L; len1++) {
                for (int len2 = 0; len2 <= L; len2++) {
                    // Total edges: len1 + 1 (to u) + 1 (from u) + len2
                    if (len1 + len2 + 2 > L) continue;
                    if (path1[len1] > NEG_INF && path2[len2] > NEG_INF) {
                        long long combined = path1[len1] + path2[len2] + value[u];
                        maxSum = max(maxSum, combined);
                    }
                }
            }
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> n >> L;

    for (int i = 1; i <= n; i++) {
        cin >> value[i];
    }

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= L; j++) {
            dp[i][j] = NEG_INF;
        }
    }

    maxSum = NEG_INF;

    dfs(1, -1);

    cout << maxSum << endl;

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
  const [n, L] = lines[idx++].split(" ").map(Number);

  const value = [0];
  const values = lines[idx++].split(" ").map(Number);
  value.push(...values);

  const graph = Array.from({ length: n + 1 }, () => []);

  for (let i = 0; i < n - 1; i++) {
    const [u, v] = lines[idx++].split(" ").map(Number);
    graph[u].push(v);
    graph[v].push(u);
  }

  const NEG_INF = -1e18;
  const dp = Array.from({ length: n + 1 }, () => Array(L + 1).fill(NEG_INF));

  let maxSum = NEG_INF;

  function dfs(u, parent) {
    dp[u][0] = value[u];
    maxSum = Math.max(maxSum, value[u]);

    const childPaths = [];

    for (const v of graph[u]) {
      if (v === parent) continue;

      dfs(v, u);

      const childBest = Array(L + 1).fill(NEG_INF);

      for (let len = 0; len < L; len++) {
        if (dp[v][len] > NEG_INF) {
          const extended = dp[v][len] + value[u];
          dp[u][len + 1] = Math.max(dp[u][len + 1], extended);
          childBest[len] = dp[v][len];
        }
      }

      childPaths.push(childBest);
    }

    for (let len = 0; len <= L; len++) {
      maxSum = Math.max(maxSum, dp[u][len]);
    }

    for (let i = 0; i < childPaths.length; i++) {
      for (let j = i + 1; j < childPaths.length; j++) {
        const path1 = childPaths[i];
        const path2 = childPaths[j];

        for (let len1 = 0; len1 <= L; len1++) {
          for (let len2 = 0; len2 <= L; len2++) {
            // Total edges: len1 + 1 (to u) + 1 (from u) + len2
            if (len1 + len2 + 2 > L) continue;
            if (path1[len1] > NEG_INF && path2[len2] > NEG_INF) {
              const combined = path1[len1] + path2[len2] + value[u];
              maxSum = Math.max(maxSum, combined);
            }
          }
        }
      }
    }
  }

  dfs(1, -1);

  console.log(maxSum);
}
```

---

## 🧪 Test Case Walkthrough (Dry Run)

### Input

```
5 2
10 -5 20 -3 15
1 2
1 3
2 4
2 5
```

### Visual Representation

```
Tree with values, L=2 (max 2 edges):
       1 (10)
      / \
   2(-5) 3(20)
   / \
4(-3) 5(15)

Valid paths (≤2 edges):
- Single nodes: 10, -5, 20, -3, 15
- 1 edge: 1-2(5), 1-3(30), 2-4(-8), 2-5(10)
- 2 edges: 4-2-5(7), 4-2-1(2), 5-2-1(20), 2-1-3(25)
```

### Path Analysis

| Path      | Edges | Sum             | Valid?  |
| --------- | ----- | --------------- | ------- |
| [3]       | 0     | 20              | ✓       |
| [1,3]     | 1     | 10+20=**30**    | ✓       |
| [5,2,1,3] | 3     | 15-5+10+20=40   | ❌ (>L) |
| [2,1,3]   | 2     | -5+10+20=**25** | ✓       |
| [5,2,1]   | 2     | 15-5+10=20      | ✓       |

**Answer: 30** (path 1→3)

**Output:** `30`

---

## ⚠️ Common Mistakes to Avoid

| #   | Mistake                   | ❌ Wrong                         | ✅ Correct                                  |
| --- | ------------------------- | -------------------------------- | ------------------------------------------- |
| 1   | **Skip negative paths**   | Ignore paths with neg values     | Check all - neg middle may connect pos ends |
| 2   | **Count nodes not edges** | `if (len > L)` where len = nodes | Path length = edges, not nodes              |
| 3   | **Same subtree combine**  | Combine paths from same child    | Only combine from different children        |
| 4   | **Initialize to 0**       | `maxSum = 0`                     | `maxSum = -INF` (all-negative case)         |

### Detailed Example:

**Mistake 3: Combining Paths from Same Subtree**

```python
# ❌ Wrong: Combines paths from same child
for i, path1 in enumerate(child_paths):
    for j, path2 in enumerate(child_paths):
        # This allows i == j, creating invalid paths!
        combine(path1, path2)

# ✅ Correct: Only different children
for i, path1 in enumerate(child_paths):
    for j in range(i + 1, len(child_paths)):
        path2 = child_paths[j]
        combine(path1, path2)
```
