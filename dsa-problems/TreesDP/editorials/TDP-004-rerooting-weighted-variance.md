---

title: Rerooting for Weighted Distance Variance
problem_id: TDP_REROOTING_WEIGHTED_VARIANCE__5927
display_id: TDP-004
difficulty: Medium
tags:
  - Tree DP
  - Rerooting Technique
  - Optimization
editorial_categories:
  - Algorithms
  - Data Structures
slug: rerooting-weighted-variance
---


# Rerooting for Weighted Distance Variance

## 📋 Problem Summary

Given a tree with nodes weighted by values `w[i]`, determine which node minimizes the **weighted sum of squared distances**:


`cost(i) = sum_j=1^n w[j] x dist(i, j)^2`


where `dist(i, j)` is the number of edges in the path between nodes `i` and `j`.

### Constraints

- `1 <= n <= 2 x 10^5`
- `1 <= w[i] <= 10^6`
- Tree is connected (n-1 edges)

## 🌍 Real-World Scenario

**Telecom Network Optimization:**
Imagine designing a fiber-optic network where:

- Each city has a population weight `w[i]`
- Network latency is proportional to distance squared (signal degradation)
- Goal: Find the optimal hub location minimizing total weighted latency
- Applications: Data center placement, CDN server location, emergency response centers

**Why squared distance?**

- Models realistic latency: propagation delay + signal degradation
- Penalizes extreme distances more heavily
- Common in physics (gravity, electric fields) and network optimization

## 🔍 Naive Approach

### Algorithm

```
function find_optimal_root_naive():
    min_cost = infinity
    best_node = -1

    for i from 1 to n:  // Try each node as root
        cost[i] = 0

        // BFS to compute distances from i
        dist = bfs_distances(i)

        for j from 1 to n:
            cost[i] += w[j] * dist[j]^2

        if cost[i] < min_cost:
            min_cost = cost[i]
            best_node = i

    return best_node, min_cost
```

### Complexity Analysis

| Phase           | Time      | Space    | Explanation             |
| --------------- | --------- | -------- | ----------------------- |
| Outer loop      | O(n)      | O(1)     | Try each node as root   |
| BFS per root    | O(n)      | O(n)     | Compute all distances   |
| Sum over nodes  | O(n)      | O(1)     | Calculate weighted cost |
| **Naive Total** | **O(n²)** | **O(n)** | n roots × n BFS         |

**Why it's inefficient:**

- Recomputes distances for each root independently
- Doesn't leverage tree structure
- For n = 200,000: ~40 billion operations (too slow)

## 💡 Optimal Approach: Rerooting DP

### Key Insight

When changing root from node `u` to child `v`:

- **Nodes in subtree of `v`**: distance decreases by 1
- **Nodes NOT in subtree of `v`**: distance increases by 1

### Mathematical Derivation

Let:

- `sum_v` = sum of weights in subtree of `v` when rooted at `u`
- `total` = sum of all weights in tree

When moving root from `u` to `v`:


`\Delta cost = -2 x sum_v x d + 2 x (total - sum_v) x d + correction`


For squared distances, we need to track:

1. **Subtree weight sum** `W_v`
2. **Weighted sum of distances** `D_v`
3. **Weighted sum of squared distances** `S_v`

### Rerooting Formula

**Step 1: Compute down[v]** (cost when `v` is root of its subtree, rooted at parent)

Base case (leaf): `down[v] = 0`

Recurrence:


`down[v] = sum_c \in children(v) <=ft[ down[c] + W_c x (2 x D_c + W_c) \right]`


**Step 2: Reroot to compute up[v]** (contribution from nodes outside subtree)

When moving from parent `p` to child `v`:


`up[v] = up[p] + down[p] - contribution of subtree(v)`


### Algorithm

```
function find_optimal_root_rerooting():
    // Phase 1: Root at node 1, compute subtree weights
    function dfs_down(v, parent):
        W[v] = weight[v]
        down[v] = 0

        for child in adj[v]:
            if child != parent:
                dfs_down(child, v)
                W[v] += W[child]
                // Add child subtree contribution
                down[v] += down[child] + W[child] * (2*D[child] + W[child])

    // Phase 2: Reroot to each node
    function dfs_up(v, parent):
        for child in adj[v]:
            if child != parent:
                // Remove child contribution, add to outside
                outside_weight = total_weight - W[child]
                up[child] = ... // transition formula
                dfs_up(child, v)

    dfs_down(1, -1)
    up[1] = 0
    dfs_up(1, -1)

    // Find minimum cost
    min_cost = infinity
    for v from 1 to n:
        total_cost = down[v] + up[v]
        min_cost = min(min_cost, total_cost)

    return min_cost
```

### Complexity Analysis

| Phase             | Time     | Space    | Explanation                    |
| ----------------- | -------- | -------- | ------------------------------ |
| DFS Down          | O(n)     | O(h)     | Compute subtree DP             |
| DFS Up (Reroot)   | O(n)     | O(h)     | Propagate outside contribution |
| Find minimum      | O(n)     | O(1)     | Scan all costs                 |
| **Arrays**        | -        | O(n)     | W[], down[], up[], adj[]       |
| **Optimal Total** | **O(n)** | **O(n)** | Two DFS passes                 |

**Why This Is Optimal:**

- Each edge visited exactly twice (down + up pass)
- Rerooting avoids recomputation by incremental updates
- For n = 200,000: ~400K operations vs ~40B naive

## 💻 Implementation

### Java

```java
import java.util.*;

public class RerootingWeightedVariance {
    static class Edge {
        int to;
        Edge(int to) {
            this.to = to;
        }
    }

    static List<Edge>[] graph;
    static long[] weight;
    static long[] subtreeWeight;
    static long[] down;
    static long[] up;
    static long totalWeight;
    static int n;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();

        weight = new long[n + 1];
        for (int i = 1; i <= n; i++) {
            weight[i] = sc.nextLong();
            totalWeight += weight[i];
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

        subtreeWeight = new long[n + 1];
        down = new long[n + 1];
        up = new long[n + 1];

        // Phase 1: Compute downward DP
        dfsDown(1, -1);

        // Phase 2: Compute upward DP (rerooting)
        dfsUp(1, -1, 0, 0);

        // Find minimum cost node
        long minCost = Long.MAX_VALUE;
        int bestNode = 1;

        for (int i = 1; i <= n; i++) {
            long totalCost = down[i] + up[i];
            if (totalCost < minCost) {
                minCost = totalCost;
                bestNode = i;
            }
        }

        System.out.println(bestNode);
        sc.close();
    }

    static void dfsDown(int u, int parent) {
        subtreeWeight[u] = weight[u];
        down[u] = 0;

        for (Edge e : graph[u]) {
            int v = e.to;
            if (v == parent) continue;

            dfsDown(v, u);

            // Add contribution of child's subtree
            // When moving down one level, distances increase by 1
            long childContribution = down[v] +
                                    2 * subtreeWeight[v] +
                                    subtreeWeight[v];
            down[u] += childContribution;
            subtreeWeight[u] += subtreeWeight[v];
        }
    }

    static void dfsUp(int u, int parent, long parentUp, long parentSubtreeWeight) {
        // Compute up[u] based on parent's info
        if (parent != -1) {
            // Total weight outside u's subtree when rooted at parent
            long outsideWeight = totalWeight - subtreeWeight[u];

            // Contribution from moving from parent to u
            long parentTotalDown = down[parent];
            long uContribution = down[u] + 2 * subtreeWeight[u] + subtreeWeight[u];
            long parentDownWithoutU = parentTotalDown - uContribution;

            up[u] = parentUp + parentDownWithoutU +
                   2 * outsideWeight + outsideWeight;
        }

        // Recur for children
        for (Edge e : graph[u]) {
            int v = e.to;
            if (v == parent) continue;

            dfsUp(v, u, up[u], subtreeWeight[u]);
        }
    }
}
```

### Python

```python
import sys
from collections import defaultdict

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0

    n = int(data[idx])
    idx += 1
    
    if n == 1:
        print(1)
        return

    weight = [0] * (n + 1)
    for i in range(1, n + 1):
        weight[i] = int(data[idx])
        idx += 1

    graph = defaultdict(list)
    for _ in range(n - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        graph[u].append(v)
        graph[v].append(u)

    # For squared distances, we track:
    # W[v] = sum of weights in subtree of v
    # D[v] = sum of w[j] * dist(v, j) for j in subtree of v
    # S[v] = sum of w[j] * dist(v, j)^2 for j in subtree of v
    W = [0] * (n + 1)
    D = [0] * (n + 1)
    S = [0] * (n + 1)

    def dfs_down(u, parent):
        W[u] = weight[u]
        D[u] = 0
        S[u] = 0

        for v in graph[u]:
            if v == parent:
                continue

            dfs_down(v, u)
            # For j in subtree of v: dist(u, j) = dist(v, j) + 1
            # D[u] += sum(w[j] * (dist(v,j) + 1)) = D[v] + W[v]
            # S[u] += sum(w[j] * (dist(v,j) + 1)^2) = S[v] + 2*D[v] + W[v]
            W[u] += W[v]
            D[u] += D[v] + W[v]
            S[u] += S[v] + 2 * D[v] + W[v]

    full_S = [0] * (n + 1)

    def dfs_up(u, parent, up_W, up_D, up_S):
        # full_S[u] = cost when u is root = S[u] (subtree) + up_S (outside)
        full_S[u] = S[u] + up_S

        for v in graph[u]:
            if v == parent:
                continue

            # Compute contribution from u's other children + outside u
            other_D = D[u] - (D[v] + W[v])
            other_S = S[u] - (S[v] + 2 * D[v] + W[v])
            other_W = W[u] - W[v]

            # When v becomes root, these nodes are one edge further
            new_up_W = other_W + up_W
            new_up_D = (other_D + up_D) + (other_W + up_W)
            new_up_S = (other_S + up_S) + 2 * (other_D + up_D) + (other_W + up_W)

            dfs_up(v, u, new_up_W, new_up_D, new_up_S)

    dfs_down(1, -1)
    dfs_up(1, -1, 0, 0, 0)

    min_cost = float('inf')
    best_node = 1

    for i in range(1, n + 1):
        if full_S[i] < min_cost:
            min_cost = full_S[i]
            best_node = i

    print(best_node)

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
long long subtreeWeight[MAXN];
long long down[MAXN];
long long up[MAXN];
long long totalWeight = 0;
int n;

void dfsDown(int u, int parent) {
    subtreeWeight[u] = weight[u];
    down[u] = 0;

    for (int v : graph[u]) {
        if (v == parent) continue;

        dfsDown(v, u);

        long long childContribution = down[v] +
                                     2LL * subtreeWeight[v] +
                                     subtreeWeight[v];
        down[u] += childContribution;
        subtreeWeight[u] += subtreeWeight[v];
    }
}

void dfsUp(int u, int parent) {
    if (parent != -1) {
        long long outsideWeight = totalWeight - subtreeWeight[u];

        long long parentTotalDown = down[parent];
        long long uContribution = down[u] + 2LL * subtreeWeight[u] + subtreeWeight[u];
        long long parentDownWithoutU = parentTotalDown - uContribution;

        up[u] = up[parent] + parentDownWithoutU +
               2LL * outsideWeight + outsideWeight;
    }

    for (int v : graph[u]) {
        if (v == parent) continue;
        dfsUp(v, u);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> n;

    for (int i = 1; i <= n; i++) {
        cin >> weight[i];
        totalWeight += weight[i];
    }

    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    dfsDown(1, -1);
    dfsUp(1, -1);

    long long minCost = LLONG_MAX;
    int bestNode = 1;

    for (int i = 1; i <= n; i++) {
        long long totalCost = down[i] + up[i];
        if (totalCost < minCost) {
            minCost = totalCost;
            bestNode = i;
        }
    }

    cout << bestNode << endl;

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

  const weight = [0];
  const weights = lines[idx++].split(" ").map(Number);
  weight.push(...weights);

  const totalWeight = weight.reduce((a, b) => a + b, 0);

  const graph = Array.from({ length: n + 1 }, () => []);

  for (let i = 0; i < n - 1; i++) {
    const [u, v] = lines[idx++].split(" ").map(Number);
    graph[u].push(v);
    graph[v].push(u);
  }

  const subtreeWeight = new Array(n + 1).fill(0);
  const down = new Array(n + 1).fill(0);
  const up = new Array(n + 1).fill(0);

  function dfsDown(u, parent) {
    subtreeWeight[u] = weight[u];
    down[u] = 0;

    for (const v of graph[u]) {
      if (v === parent) continue;

      dfsDown(v, u);

      const childContribution =
        down[v] + 2 * subtreeWeight[v] + subtreeWeight[v];
      down[u] += childContribution;
      subtreeWeight[u] += subtreeWeight[v];
    }
  }

  function dfsUp(u, parent) {
    if (parent !== -1) {
      const outsideWeight = totalWeight - subtreeWeight[u];

      const parentTotalDown = down[parent];
      const uContribution = down[u] + 2 * subtreeWeight[u] + subtreeWeight[u];
      const parentDownWithoutU = parentTotalDown - uContribution;

      up[u] =
        up[parent] + parentDownWithoutU + 2 * outsideWeight + outsideWeight;
    }

    for (const v of graph[u]) {
      if (v === parent) continue;
      dfsUp(v, u);
    }
  }

  dfsDown(1, -1);
  dfsUp(1, -1);

  let minCost = Infinity;
  let bestNode = 1;

  for (let i = 1; i <= n; i++) {
    const totalCost = down[i] + up[i];
    if (totalCost < minCost) {
      minCost = totalCost;
      bestNode = i;
    }
  }

  console.log(bestNode);
}
```

---

## 🧪 Test Case Walkthrough (Dry Run)

### Input

```
4
3 1 2 4
1 2
1 3
3 4
```

### Visual Representation

```
Tree with weights:
      1 (w=3)
     / \
  2(1) 3(2)
        |
       4(4)

Goal: Find node minimizing Σ w[j] × dist(i,j)²
```

### Cost Calculation for Each Root

| Root | Distances              | Cost Calculation            | Total  |
| ---- | ---------------------- | --------------------------- | ------ |
| 1    | d(2)=1, d(3)=1, d(4)=2 | 1×1² + 2×1² + 4×2² = 1+2+16 | **19** |
| 2    | d(1)=1, d(3)=2, d(4)=3 | 3×1² + 2×2² + 4×3² = 3+8+36 | 47     |
| 3    | d(1)=1, d(2)=2, d(4)=1 | 3×1² + 1×2² + 4×1² = 3+4+4  | **11** |
| 4    | d(1)=2, d(2)=3, d(3)=1 | 3×2² + 1×3² + 2×1² = 12+9+2 | 23     |

**Best Node = 3** (minimum cost = 11)

**Output:** `3`

---

## ⚠️ Common Mistakes to Avoid

| #   | Mistake                   | ❌ Wrong                              | ✅ Correct                                      |
| --- | ------------------------- | ------------------------------------- | ----------------------------------------------- |
| 1   | **Integer overflow**      | `int cost` with large w × dist²       | Use `long long` / `long`                        |
| 2   | **Wrong rerooting**       | Forget to subtract child contribution | `parent_cost - child_contribution + adjustment` |
| 3   | **Off-by-one distance**   | Count nodes instead of edges          | Distance = number of edges                      |
| 4   | **Missing bidirectional** | Add edge once                         | Add `adj[u].add(v)` AND `adj[v].add(u)`         |

### Detailed Example:

**Mistake 1: Integer Overflow**

```cpp
// ❌ Wrong: int overflows for large inputs
int cost = 0;
for (int j = 1; j <= n; j++) {
    cost += w[j] * dist[j] * dist[j];  // Can exceed 2^31
}

// ✅ Correct: Use long long
long long cost = 0;
for (int j = 1; j <= n; j++) {
    cost += (long long)w[j] * dist[j] * dist[j];
}
```

---

## 🔗 Related Concepts

- **Rerooting Technique:** Generic DP pattern for "all roots" problems
- **Tree DP:** Foundation for subtree-based computation
- **Centroid Decomposition:** Alternative for path queries
- **Heavy-Light Decomposition:** For path updates/queries
