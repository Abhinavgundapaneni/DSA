---

title: Tree DP for Vertex Cover
problem_id: TDP_TREE_VERTEX_COVER__7514
display_id: TDP-006
difficulty: Medium
tags:
  - Tree DP
  - Graph Theory
  - Optimization
editorial_categories:
  - Algorithms
  - Data Structures
slug: tree-vertex-cover
---


# Tree DP for Vertex Cover

## 📋 Problem Summary

Given a tree with `n` nodes, find the **minimum vertex cover** - the smallest set of vertices such that every edge has at least one endpoint in the set.

### Constraints

- `1 <= n <= 2 x 10^5`
- Tree is connected (n-1 edges)

## 🌍 Real-World Scenario

**Security Camera Placement:**
Imagine a building with hallways forming a tree structure:

- Each intersection is a node
- Each hallway is an edge
- Need to place minimum cameras such that every hallway is monitored
- A camera at an intersection covers all connected hallways

**Applications:**

- Network monitoring (routers covering links)
- Security systems (cameras covering corridors)
- Facility management (sensors covering zones)

## 🔍 Naive Approach

### Algorithm

```
function vertex_cover_naive():
    min_size = infinity

    // Step 1: Generate all subsets
    for subset in all_subsets(vertices):
        // Step 2: Check if subset covers all edges
        covers_all = true
        for edge (u, v) in edges:
            if u not in subset and v not in subset:
                covers_all = false
                break

        // Step 3: Update minimum
        if covers_all:
            min_size = min(min_size, subset.size())

    return min_size
```

### Complexity Analysis

| Phase            | Time            | Space    | Explanation     |
| ---------------- | --------------- | -------- | --------------- |
| Generate subsets | O(2^n)          | O(n)     | All 2^n subsets |
| Check coverage   | O(m) per subset | O(1)     | m = n-1 edges   |
| **Naive Total**  | **O(2^n · n)**  | **O(n)** | Exponential     |

**Why This Complexity:**

- 2^n subsets to check
- For n = 20: ~20M operations
- For n = 100: ~10^32 operations (impossible)

**Limitations:**

- For n = 20: over 1 million subsets
- For n = 100: computationally infeasible

## 💡 Optimal Approach: Include/Exclude DP

### Key Insight

For each node in the tree (rooted arbitrarily), we have two choices:

1. **Include** the node in vertex cover
2. **Exclude** the node from vertex cover

**DP State:**

- `dp[u][0]` = minimum vertices to cover subtree of `u` when `u` is **NOT included**
- `dp[u][1]` = minimum vertices to cover subtree of `u` when `u` is **included**

### Recurrence Relations

**Base Case (Leaf node):**

```
dp[leaf][0] = 0  // Don't include leaf
dp[leaf][1] = 1  // Include leaf
```

**Recursive Case:**

**When u is NOT included (`dp[u][0]`):**

- All children MUST be included (to cover edges u-child)

```
dp[u][0] = sum of dp[child][1] for all children
```

**When u is included (`dp[u][1]`):**

- Children can be included or not (edge u-child is already covered)
- Choose minimum for each child

```
dp[u][1] = 1 + sum of min(dp[child][0], dp[child][1]) for all children
```

**Final Answer:**

```
min(dp[root][0], dp[root][1])
```

### Algorithm

```
function vertex_cover_dp():
    function dfs(u, parent):
        // Base case handled implicitly
        dp[u][0] = 0  // u not included
        dp[u][1] = 1  // u included

        for child in adj[u]:
            if child != parent:
                dfs(child, u)

                // u not in cover → child must be
                dp[u][0] += dp[child][1]

                // u in cover → child can be either
                dp[u][1] += min(dp[child][0], dp[child][1])

    dfs(1, -1)
    return min(dp[1][0], dp[1][1])
```

### Complexity Analysis

| Phase             | Time               | Space    | Explanation          |
| ----------------- | ------------------ | -------- | -------------------- |
| DFS traversal     | O(n)               | O(h)     | Visit each node once |
| Process children  | O(degree) per node | O(1)     | Sum children's DP    |
| DP storage        | -                  | O(n)     | 2 states × n nodes   |
| **Optimal Total** | **O(n)**           | **O(n)** | Linear               |

**Why This Is Optimal:**

- Each edge visited exactly once
- Bottom-up DP: no redundant computation
- For n = 200K: ~400K operations vs ~10^60K naive

- **Space Complexity:** O(n)
  - DP arrays: 2n
  - Recursion stack: O(n)

## 💻 Implementation

### Java

```java
import java.util.*;

public class TreeVertexCover {
    static class Edge {
        int to;
        Edge(int to) {
            this.to = to;
        }
    }

    static List<Edge>[] graph;
    static int[][] dp;
    static int n;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();

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

        dp = new int[n + 1][2];

        dfs(1, -1);

        int result = Math.min(dp[1][0], dp[1][1]);
        System.out.println(result);

        sc.close();
    }

    static void dfs(int u, int parent) {
        dp[u][0] = 0;  // Not including u
        dp[u][1] = 1;  // Including u

        for (Edge e : graph[u]) {
            int v = e.to;
            if (v == parent) continue;

            dfs(v, u);

            // If u is not included, all children must be included
            dp[u][0] += dp[v][1];

            // If u is included, children can be included or not
            dp[u][1] += Math.min(dp[v][0], dp[v][1]);
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

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    dp = [[0, 0] for _ in range(n + 1)]

    def dfs(u, parent):
        dp[u][0] = 0  # Not including u
        dp[u][1] = 1  # Including u

        for v in graph[u]:
            if v == parent:
                continue

            dfs(v, u)

            # If u not included, all children must be included
            dp[u][0] += dp[v][1]

            # If u included, take minimum for each child
            dp[u][1] += min(dp[v][0], dp[v][1])

    dfs(1, -1)

    result = min(dp[1][0], dp[1][1])
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
int dp[MAXN][2];
int n;

void dfs(int u, int parent) {
    dp[u][0] = 0;  // Not including u
    dp[u][1] = 1;  // Including u

    for (int v : graph[u]) {
        if (v == parent) continue;

        dfs(v, u);

        // If u not included, all children must be included
        dp[u][0] += dp[v][1];

        // If u included, take minimum for each child
        dp[u][1] += min(dp[v][0], dp[v][1]);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> n;

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    dfs(1, -1);

    int result = min(dp[1][0], dp[1][1]);
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

  const graph = Array.from({ length: n + 1 }, () => []);

  for (let i = 0; i < n - 1; i++) {
    const [u, v] = lines[idx++].split(" ").map(Number);
    graph[u].push(v);
    graph[v].push(u);
  }

  const dp = Array.from({ length: n + 1 }, () => [0, 0]);

  function dfs(u, parent) {
    dp[u][0] = 0; // Not including u
    dp[u][1] = 1; // Including u

    for (const v of graph[u]) {
      if (v === parent) continue;

      dfs(v, u);

      // If u not included, all children must be included
      dp[u][0] += dp[v][1];

      // If u included, take minimum for each child
      dp[u][1] += Math.min(dp[v][0], dp[v][1]);
    }
  }

  dfs(1, -1);

  const result = Math.min(dp[1][0], dp[1][1]);
  console.log(result);
}
```

---

## 🧪 Test Case Walkthrough (Dry Run)

### Input

```
6
1 2
1 3
2 4
2 5
3 6
```

### Visual Representation

```
Tree Structure:
        1
       / \
      2   3
     / \   \
    4   5   6

Edges: (1,2), (1,3), (2,4), (2,5), (3,6)
Need: At least one endpoint of each edge in cover
```

### DP Walkthrough (post-order)

| Node | dp[0] (exclude)     | dp[1] (include)       | Explanation                     |
| ---- | ------------------- | --------------------- | ------------------------------- |
| 4    | 0                   | 1                     | Leaf: exclude=0, include=1      |
| 5    | 0                   | 1                     | Leaf: exclude=0, include=1      |
| 2    | dp[4][1]+dp[5][1]=2 | 1+min(0,1)+min(0,1)=1 | Children must be in if excluded |
| 6    | 0                   | 1                     | Leaf                            |
| 3    | dp[6][1]=1          | 1+min(0,1)=1          |                                 |
| 1    | dp[2][1]+dp[3][1]=2 | 1+min(2,1)+min(1,1)=3 |                                 |

**Answer: min(dp[1][0], dp[1][1]) = min(2, 3) = 2**

Optimal cover: {2, 3} covers all edges

**Output:** `2`

---

## ⚠️ Common Mistakes to Avoid

| #   | Mistake                  | ❌ Wrong                              | ✅ Correct                                  |
| --- | ------------------------ | ------------------------------------- | ------------------------------------------- |
| 1   | **Use min for dp[u][0]** | `dp[u][0] += min(dp[v][0], dp[v][1])` | `dp[u][0] += dp[v][1]` (MUST include child) |
| 2   | **Forget +1**            | `dp[u][1] = sum of children`          | `dp[u][1] = 1 + sum` (count node u)         |
| 3   | **Empty tree**           | Return 1                              | Return 0 (no edges to cover)                |
| 4   | **Greedy approach**      | Pick high-degree nodes                | Greedy fails; use DP                        |

### Detailed Example:

**Mistake 1: Using min() for dp[u][0]**

```python
# ❌ Wrong: When u excluded, child might be excluded too
dp[u][0] = 0
for v in children[u]:
    dp[u][0] += min(dp[v][0], dp[v][1])  # WRONG!
# Edge (u, v) not covered if both excluded!

# ✅ Correct: Child MUST be included when u excluded
dp[u][0] = 0
for v in children[u]:
    dp[u][0] += dp[v][1]  # Child must be in cover
```

---

## 🔗 Related Concepts

- **Independent Set**: Complement problem (nodes with no edges between them)
- **Dominating Set**: Every node is in set or adjacent to set
- **Edge Cover**: Every vertex is incident to at least one edge in set
- **Bipartite Matching**: Related via König's theorem
