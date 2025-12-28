---
problem_id: TDP_LCA_BINARY_LIFTING__7291
display_id: TDP-001
slug: lca-binary-lifting
title: "Lowest Common Ancestor (Binary Lifting)"
difficulty: Medium
difficulty_score: 45
topics:
  - Tree DP
  - Binary Lifting
  - LCA
tags:
  - preprocessing
  - tree-traversal
  - ancestors
premium: true
subscription_tier: basic
---

# TDP-001: Lowest Common Ancestor (Binary Lifting)

## 📋 Problem Summary

Given a rooted tree with n nodes, preprocess it to answer queries for the Lowest Common Ancestor (LCA) of any two nodes in O(log n) time using binary lifting technique.

## 🌍 Real-World Scenario

**Scenario Title:** Corporate Organizational Hierarchy Analysis

In a large multinational corporation with thousands of employees, the organizational structure forms a tree where the CEO is the root, and each employee reports to exactly one manager. The HR department needs to efficiently answer questions like: "Who is the lowest-level manager that oversees both the Sales Director of Region A and the Marketing Manager of Region B?" This is essentially finding the LCA of two nodes in the organizational tree.

Traditional methods of traversing from each employee up to the root would be too slow when handling hundreds of thousands of queries per day. Binary lifting allows the system to preprocess the organizational chart once (whenever there's a restructuring) and then answer any managerial relationship query in logarithmic time, making real-time organizational analysis feasible.

This technique is also used in version control systems like Git to find the common ancestor of two commits, in file system hierarchies to determine the closest common parent directory, and in biological taxonomy to find the most recent common ancestor of two species.

**Why This Problem Matters:**

- **Efficient Query Processing:** Reduces query time from O(n) to O(log n), crucial for real-time systems
- **Preprocessing Investment:** One-time O(n log n) preprocessing enables unlimited fast queries
- **Versatile Applications:** Used in databases, compilers, bioinformatics, and network routing

![Real-World Application](../images/TDP-001/real-world-scenario.png)

## Detailed Explanation

The Lowest Common Ancestor (LCA) of two nodes u and v in a rooted tree is the deepest node that is an ancestor of both u and v. Binary lifting is a preprocessing technique that allows us to answer LCA queries efficiently.

**Key Insight:** Instead of storing just the immediate parent of each node, we store the ancestor at distances 2^0, 2^1, 2^2, ..., 2^k where k = log₂(n). This allows us to "jump" exponentially up the tree.

The preprocessing involves:

1. Computing the depth of each node via DFS
2. Building a 2D array `up[node][j]` where `up[node][j]` is the 2^j-th ancestor of node
3. Using dynamic programming: `up[node][j] = up[up[node][j-1]][j-1]`

For LCA queries:

1. First, bring both nodes to the same depth using binary jumps
2. Then, simultaneously lift both nodes upward, ensuring they don't meet, until their parents are the same
3. The parent is the LCA

## Naive Approach

**Intuition:**
For each LCA query, traverse from both nodes upward toward the root until they meet at a common ancestor.

### Algorithm

```
function lca_naive(u, v):
    ancestors_u = empty set

    // Step 1: Collect all ancestors of u
    current = u
    while current != null:
        ancestors_u.add(current)
        current = parent[current]

    // Step 2: Traverse from v upward until hitting an ancestor of u
    current = v
    while current not in ancestors_u:
        current = parent[current]

    return current  // This is the LCA
```

### Complexity Analysis

| Phase                  | Time       | Space    | Explanation                           |
| ---------------------- | ---------- | -------- | ------------------------------------- |
| Collect ancestors of u | O(h)       | O(h)     | Traverse from u to root, store in set |
| Find LCA from v        | O(h)       | O(1)     | Traverse from v until match found     |
| **Per Query**          | **O(h)**   | **O(h)** | h = height of tree                    |
| **Total (q queries)**  | **O(q·h)** | **O(h)** | Worst case h = n (skewed tree)        |

**Why This Complexity:**

- In a balanced tree: h = O(log n), so O(q log n) per query
- In a skewed tree (linked list): h = O(n), so O(qn) total
- No preprocessing benefit - each query starts fresh

**Limitations:**

- Too slow for large trees with many queries
- Each query requires potentially scanning the entire path to root
- No benefit from preprocessing

## Optimal Approach

**Key Insight:**
By preprocessing ancestors at exponential distances (2^0, 2^1, 2^2, ...), we can jump to any ancestor in O(log n) jumps using binary representation of distances.

### Algorithm

**Phase 1: Preprocessing (Build Jump Table)**

```
function preprocess(root):
    // Step 1: DFS to compute depths and immediate parents
    dfs(root, null, depth=0)

    // Step 2: Build binary lifting table
    // up[node][j] = ancestor at distance 2^j
    for j from 1 to LOG:
        for each node:
            if up[node][j-1] exists:
                up[node][j] = up[up[node][j-1]][j-1]
            // Jump 2^j = jump 2^(j-1) twice
```

**Phase 2: LCA Query**

```
function lca(u, v):
    // Step 1: Ensure u is deeper
    if depth[u] < depth[v]: swap(u, v)

    // Step 2: Lift u to same depth as v
    diff = depth[u] - depth[v]
    for j from LOG-1 down to 0:
        if (diff >> j) & 1:  // If j-th bit is set
            u = up[u][j]

    // Step 3: If same node, v was ancestor of u
    if u == v: return u

    // Step 4: Binary search for LCA
    for j from LOG-1 down to 0:
        if up[u][j] != up[v][j]:
            u = up[u][j]
            v = up[v][j]

    return up[u][0]  // Parent is LCA
```

### Complexity Analysis

| Phase                   | Time                     | Space          | Explanation                       |
| ----------------------- | ------------------------ | -------------- | --------------------------------- |
| DFS traversal           | O(n)                     | O(n)           | Visit each node once, store depth |
| Build jump table        | O(n log n)               | O(n log n)     | n nodes × log n ancestors each    |
| **Preprocessing Total** | **O(n log n)**           | **O(n log n)** | One-time cost                     |
| Equalize depths         | O(log n)                 | O(1)           | At most log n jumps               |
| Binary search LCA       | O(log n)                 | O(1)           | At most log n iterations          |
| **Per Query**           | **O(log n)**             | **O(1)**       | Constant per query                |
| **Total (q queries)**   | **O(n log n + q log n)** | **O(n log n)** | Amortized                         |

**Why This Is Optimal:**

- Each query requires at most log₂(n) jumps
- Preprocessing is done once and amortized over many queries
- Binary representation allows reaching any distance efficiently
- For n = 200,000 and q = 200,000: ~7M operations vs ~40B naive

![Algorithm Visualization](../images/TDP-001/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    private int LOG = 20; // log2(200000) ≈ 18
    private List<Integer>[] tree;
    private int[][] up;
    private int[] depth;
    private int n;

    public void preprocess(int root, int n, int[][] edges) {
        this.n = n;
        tree = new ArrayList[n + 1];
        up = new int[n + 1][LOG];
        depth = new int[n + 1];

        for (int i = 0; i <= n; i++) {
            tree[i] = new ArrayList<>();
            Arrays.fill(up[i], -1);
        }

        // Build adjacency list
        for (int[] edge : edges) {
            tree[edge[0]].add(edge[1]);
            tree[edge[1]].add(edge[0]);
        }

        // DFS to compute depths and immediate parents
        dfs(root, -1, 0);

        // Binary lifting preprocessing
        for (int j = 1; j < LOG; j++) {
            for (int i = 1; i <= n; i++) {
                if (up[i][j - 1] != -1) {
                    up[i][j] = up[up[i][j - 1]][j - 1];
                }
            }
        }
    }

    private void dfs(int node, int parent, int d) {
        up[node][0] = parent;
        depth[node] = d;
        for (int child : tree[node]) {
            if (child != parent) {
                dfs(child, node, d + 1);
            }
        }
    }

    public int lca(int u, int v) {
        // Make u deeper
        if (depth[u] < depth[v]) {
            int temp = u;
            u = v;
            v = temp;
        }

        // Lift u to same level as v
        int diff = depth[u] - depth[v];
        for (int j = 0; j < LOG; j++) {
            if ((diff & (1 << j)) != 0) {
                u = up[u][j];
            }
        }

        if (u == v) return u;

        // Lift both simultaneously
        for (int j = LOG - 1; j >= 0; j--) {
            if (up[u][j] != -1 && up[u][j] != up[v][j]) {
                u = up[u][j];
                v = up[v][j];
            }
        }

        return up[u][0];
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int q = sc.nextInt();

        int[][] edges = new int[n - 1][2];
        for (int i = 0; i < n - 1; i++) {
            edges[i][0] = sc.nextInt();
            edges[i][1] = sc.nextInt();
        }

        Solution solution = new Solution();
        solution.preprocess(1, n, edges);

        for (int i = 0; i < q; i++) {
            int u = sc.nextInt();
            int v = sc.nextInt();
            System.out.println(solution.lca(u, v));
        }

        sc.close();
    }
}
```

### Python

```python
from typing import List
import sys
sys.setrecursionlimit(300000)

class Solution:
    def __init__(self):
        self.LOG = 20
        self.tree = []
        self.up = []
        self.depth = []
        self.n = 0

    def preprocess(self, root: int, n: int, edges: List[List[int]]) -> None:
        self.n = n
        self.tree = [[] for _ in range(n + 1)]
        self.up = [[-1] * self.LOG for _ in range(n + 1)]
        self.depth = [0] * (n + 1)

        # Build adjacency list
        for u, v in edges:
            self.tree[u].append(v)
            self.tree[v].append(u)

        # DFS to compute depths and immediate parents
        self._dfs(root, -1, 0)

        # Binary lifting preprocessing
        for j in range(1, self.LOG):
            for i in range(1, n + 1):
                if self.up[i][j - 1] != -1:
                    self.up[i][j] = self.up[self.up[i][j - 1]][j - 1]

    def _dfs(self, node: int, parent: int, d: int) -> None:
        self.up[node][0] = parent
        self.depth[node] = d
        for child in self.tree[node]:
            if child != parent:
                self._dfs(child, node, d + 1)

    def lca(self, u: int, v: int) -> int:
        # Make u deeper
        if self.depth[u] < self.depth[v]:
            u, v = v, u

        # Lift u to same level as v
        diff = self.depth[u] - self.depth[v]
        for j in range(self.LOG):
            if (diff >> j) & 1:
                u = self.up[u][j]

        if u == v:
            return u

        # Lift both simultaneously
        for j in range(self.LOG - 1, -1, -1):
            if self.up[u][j] != -1 and self.up[u][j] != self.up[v][j]:
                u = self.up[u][j]
                v = self.up[v][j]

        return self.up[u][0]

def main():
    input_lines = sys.stdin.read().strip().split('\n')
    n, q = map(int, input_lines[0].split())

    edges = []
    for i in range(1, n):
        u, v = map(int, input_lines[i].split())
        edges.append([u, v])

    solution = Solution()
    solution.preprocess(1, n, edges)

    results = []
    for i in range(n, n + q):
        u, v = map(int, input_lines[i].split())
        results.append(str(solution.lca(u, v)))

    print('\n'.join(results))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

class Solution {
private:
    static const int LOG = 20;
    vector<vector<int>> tree;
    int up[200005][LOG];
    int depth[200005];
    int n;

    void dfs(int node, int parent, int d) {
        up[node][0] = parent;
        depth[node] = d;
        for (int child : tree[node]) {
            if (child != parent) {
                dfs(child, node, d + 1);
            }
        }
    }

public:
    void preprocess(int root, int n, vector<pair<int, int>>& edges) {
        this->n = n;
        tree.resize(n + 1);
        memset(up, -1, sizeof(up));
        memset(depth, 0, sizeof(depth));

        // Build adjacency list
        for (auto& edge : edges) {
            tree[edge.first].push_back(edge.second);
            tree[edge.second].push_back(edge.first);
        }

        // DFS to compute depths and immediate parents
        dfs(root, -1, 0);

        // Binary lifting preprocessing
        for (int j = 1; j < LOG; j++) {
            for (int i = 1; i <= n; i++) {
                if (up[i][j - 1] != -1) {
                    up[i][j] = up[up[i][j - 1]][j - 1];
                }
            }
        }
    }

    int lca(int u, int v) {
        // Make u deeper
        if (depth[u] < depth[v]) {
            swap(u, v);
        }

        // Lift u to same level as v
        int diff = depth[u] - depth[v];
        for (int j = 0; j < LOG; j++) {
            if ((diff >> j) & 1) {
                u = up[u][j];
            }
        }

        if (u == v) return u;

        // Lift both simultaneously
        for (int j = LOG - 1; j >= 0; j--) {
            if (up[u][j] != -1 && up[u][j] != up[v][j]) {
                u = up[u][j];
                v = up[v][j];
            }
        }

        return up[u][0];
    }
};

int main() {
    int n, q;
    cin >> n >> q;

    vector<pair<int, int>> edges;
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        edges.push_back({u, v});
    }

    Solution solution;
    solution.preprocess(1, n, edges);

    for (int i = 0; i < q; i++) {
        int u, v;
        cin >> u >> v;
        cout << solution.lca(u, v) << endl;
    }

    return 0;
}
```

### JavaScript

```javascript
const readline = require("readline");

class Solution {
  constructor() {
    this.LOG = 20;
    this.tree = [];
    this.up = [];
    this.depth = [];
    this.n = 0;
  }

  preprocess(root, n, edges) {
    this.n = n;
    this.tree = Array.from({ length: n + 1 }, () => []);
    this.up = Array.from({ length: n + 1 }, () => Array(this.LOG).fill(-1));
    this.depth = Array(n + 1).fill(0);

    // Build adjacency list
    for (const [u, v] of edges) {
      this.tree[u].push(v);
      this.tree[v].push(u);
    }

    // DFS to compute depths and immediate parents
    this.dfs(root, -1, 0);

    // Binary lifting preprocessing
    for (let j = 1; j < this.LOG; j++) {
      for (let i = 1; i <= n; i++) {
        if (this.up[i][j - 1] !== -1) {
          this.up[i][j] = this.up[this.up[i][j - 1]][j - 1];
        }
      }
    }
  }

  dfs(node, parent, d) {
    this.up[node][0] = parent;
    this.depth[node] = d;
    for (const child of this.tree[node]) {
      if (child !== parent) {
        this.dfs(child, node, d + 1);
      }
    }
  }

  lca(u, v) {
    // Make u deeper
    if (this.depth[u] < this.depth[v]) {
      [u, v] = [v, u];
    }

    // Lift u to same level as v
    let diff = this.depth[u] - this.depth[v];
    for (let j = 0; j < this.LOG; j++) {
      if ((diff >> j) & 1) {
        u = this.up[u][j];
      }
    }

    if (u === v) return u;

    // Lift both simultaneously
    for (let j = this.LOG - 1; j >= 0; j--) {
      if (this.up[u][j] !== -1 && this.up[u][j] !== this.up[v][j]) {
        u = this.up[u][j];
        v = this.up[v][j];
      }
    }

    return this.up[u][0];
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const lines = [];
rl.on("line", (line) => {
  lines.push(line);
});

rl.on("close", () => {
  const [n, q] = lines[0].split(" ").map(Number);

  const edges = [];
  for (let i = 1; i < n; i++) {
    const [u, v] = lines[i].split(" ").map(Number);
    edges.push([u, v]);
  }

  const solution = new Solution();
  solution.preprocess(1, n, edges);

  const results = [];
  for (let i = n; i < n + q; i++) {
    const [u, v] = lines[i].split(" ").map(Number);
    results.push(solution.lca(u, v));
  }

  console.log(results.join("\n"));
});
```

---

## 🧪 Test Case Walkthrough (Dry Run)

### Input

```
7 3
1 2
1 3
2 4
2 5
3 6
3 7
4 5
4 7
6 7
```

### Visual Representation

```
Tree Structure:
        1
       / \
      2   3
     / \ / \
    4  5 6  7

Depths: 1→0, 2→1, 3→1, 4→2, 5→2, 6→2, 7→2
```

### Query Walkthrough

| Query | u   | v   | Process                            | LCA   |
| ----- | --- | --- | ---------------------------------- | ----- |
| 1     | 4   | 5   | Same parent (2), depth equal       | **2** |
| 2     | 4   | 7   | Lift to same depth, then lift both | **1** |
| 3     | 6   | 7   | Same parent (3), depth equal       | **3** |

### Step-by-Step for Query (4, 7):

1. `depth[4]=2, depth[7]=2` → same depth
2. `up[4][0]=2, up[7][0]=3` → different, don't jump
3. Since `up[4][0] != up[7][0]`, answer is `up[up[4][0]][0] = up[2][0] = 1`

**Output:** `2 1 3`

---

## ⚠️ Common Mistakes to Avoid

| #   | Mistake                   | ❌ Wrong                              | ✅ Correct                                          |
| --- | ------------------------- | ------------------------------------- | --------------------------------------------------- |
| 1   | **LOG too small**         | `LOG = (int)(log(n)/log(2))`          | `LOG = 20` (safe upper bound)                       |
| 2   | **Skip same-level check** | Always run lifting loop               | Check `if (u == v) return u` after equalizing depth |
| 3   | **Wrong comparison**      | `if (up[u][j] == up[v][j])` then jump | `if (up[u][j] != up[v][j])` then jump               |
| 4   | **Return wrong node**     | `return u` after lifting              | `return up[u][0]` (parent is LCA)                   |
| 5   | **Forget -1 check**       | Access `up[up[u][j]][...]`            | Check `up[u][j] != -1` first                        |

### Detailed Examples:

**Mistake 1: LOG Calculation**

```java
// ❌ Might overflow for n = 200000
int LOG = (int)(Math.log(n) / Math.log(2));  // Returns 17

// ✅ Safe approach
int LOG = 20;  // Handles up to 2^20 = 1M nodes
```

**Mistake 3: Wrong Comparison Direction**

```java
// ❌ This overshoots - you end up at LCA's ancestor
for (int j = LOG - 1; j >= 0; j--) {
    if (up[u][j] == up[v][j]) {  // WRONG!
        u = up[u][j];
        v = up[v][j];
    }
}
return u;  // Wrong: returns ancestor of LCA

// ✅ Correct: stop just before meeting
for (int j = LOG - 1; j >= 0; j--) {
    if (up[u][j] != -1 && up[u][j] != up[v][j]) {
        u = up[u][j];
        v = up[v][j];
    }
}
return up[u][0];  // Correct: parent is LCA
```

---

## Related Concepts

- **Sparse Table:** Similar preprocessing for range queries
- **Euler Tour + RMQ:** Alternative LCA approach with different trade-offs
- **Heavy-Light Decomposition:** Advanced tree path queries
- **Link-Cut Trees:** Dynamic tree structures with path queries


## Constraints

- `1 ≤ n ≤ 2 × 10^5`
- `1 ≤ q ≤ 2 × 10^5`
- `1 ≤ u, v ≤ n`
- The given edges form a valid tree
- All queries are independent