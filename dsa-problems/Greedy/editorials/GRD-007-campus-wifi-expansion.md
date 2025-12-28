---
problem_id: GRD_CAMPUS_WIFI_EXPANSION__4892
display_id: GRD-007
slug: campus-wifi-expansion
title: "Campus Wi-Fi Expansion"
difficulty: Medium
difficulty_score: 55
topics:
  - Greedy Algorithms
  - Minimum Spanning Tree
  - Kruskal's Algorithm
tags:
  - greedy
  - mst
  - kruskal
  - graph
  - medium
premium: true
subscription_tier: basic
---

# GRD-007: Campus Wi-Fi Expansion

## 📋 Problem Summary

You need to connect `n` buildings into a single network. You are given the heights of all buildings.
- Existing connections between some buildings are free.
- New connections between any two buildings `i` and `j` cost `|height[i] - height[j]|`.
Find the minimum cost to connect all buildings.

## 🌍 Real-World Scenario

**Scenario Title:** Connecting Mountain Villages

Imagine a series of villages located at different altitudes on a mountain range. The government wants to build a road network connecting all of them.
- Some dirt paths already exist (free to use).
- Building a new road between two villages is expensive, and the cost depends on the elevation difference (slope). Steeper roads are harder to build. The cost is proportional to the absolute difference in altitude.

To save taxpayer money, the engineers want to design a network (a set of roads) that connects every village while minimizing the total elevation difference covered by new construction.

**Why This Problem Matters:**

- **Infrastructure Planning:** Minimizing construction costs in utility networks (water, electricity, internet).
- **Clustering:** In data science, connecting data points with similar properties (small "distance") is key to hierarchical clustering.

![Real-World Application](../images/GRD-007/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: The Cost of Height

Buildings: A(10m), B(15m), C(12m).
Existing: None.

Possible Edges:
- A-B: Cost |10-15| = 5
- A-C: Cost |10-12| = 2
- B-C: Cost |15-12| = 3

MST Strategy:
1. Pick cheapest: A-C (Cost 2). Connected: {A, C}, {B}.
2. Pick next cheapest: B-C (Cost 3). Connected: {A, B, C}.
Total Cost: 2 + 3 = 5.

(Note: A-B cost 5 was skipped because A and B were already connected via C).

```text
   15m [ B ]
         | (3)
   12m [ C ]
         | (2)
   10m [ A ]
```

## ✅ Input/Output Clarifications (Read This Before Coding)

- **Graph Type:** This is a Minimum Spanning Tree (MST) problem.
- **Dense Graph:** If we consider *every* pair of buildings, there are `O(N^2)` edges. With `N=10^5`, this is too many (`10^10`). We need a smarter way to pick candidate edges.
- **Existing Edges:** These have weight 0. They should be processed first (or effectively merged before starting).

## Naive Approach

### Intuition

Generate all possible pairs `(i, j)`, calculate costs, and run Kruskal's Algorithm.

### Algorithm

1. Create edges for all pairs `(i, j)`. Cost = `|h[i] - h[j]|`.
2. Add existing edges with Cost = 0.
3. Sort all edges.
4. Use Union-Find to select edges until all connected.

### Time Complexity

- **O(N^2 log N)**: Generating and sorting `N^2` edges.
- **Space:** `O(N^2)`.
- **Failure:** TLE and Memory Limit Exceeded for `N > 5000`.

## Optimal Approach

### Key Insight

We only care about the *smallest* costs. The cost is `|h[i] - h[j]|`.
For any building with height `h`, its "cheapest" potential neighbors are the buildings with heights *closest* to `h`.
If we sort the buildings by height, the closest neighbors for building `i` (in the sorted list) are `i-1` and `i+1`.
**Property:** In a graph where edge weights are differences between values on a line, the MST is formed by edges between adjacent elements in the sorted sequence.
(Plus the existing zero-cost edges).

### Algorithm

1. **Handle Existing Edges:** Initialize Union-Find. Union all pairs given in `existingCables`. Count how many merges occurred.
2. **Sort Buildings:** Create a list of pairs `(height, original_index)`. Sort this list based on height.
3. **Generate Candidate Edges:**
   - Iterate through the sorted list from `i = 0` to `n-2`.
   - Create an edge between `sorted[i]` and `sorted[i+1]`.
   - Cost = `sorted[i+1].height - sorted[i].height`.
   - Store these `N-1` edges.
4. **Run Kruskal's:**
   - Sort the `N-1` candidate edges by cost.
   - Iterate and apply Union-Find. Add cost if merge is successful.
   - Stop when we have `N-1` total edges (including existing ones) or just process all candidates.

### Time Complexity

- **O(N log N)**: Sorting buildings takes `O(N log N)`. Sorting `N-1` edges takes `O(N log N)`. Union-Find is nearly linear.

### Space Complexity

- **O(N)**: Storing buildings and `N-1` edges.

### Why This Is Optimal

Consider three buildings with heights `a < b < c`.
Edges: `(a,b)` cost `b-a`, `(b,c)` cost `c-b`, `(a,c)` cost `c-a`.
Note that `(c-a) = (c-b) + (b-a)`.
The edge `(a,c)` is the most expensive and is "redundant" because `a` and `c` can be connected via `b` with the same total cost (in a path) or cheaper individual edges. Kruskal's will always prefer the smaller components `(a,b)` and `(b,c)`.
Thus, we only need to consider adjacent pairs in the sorted order.

![Algorithm Visualization](../images/GRD-007/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    static class Edge implements Comparable<Edge> {
        int u, v, cost;
        public Edge(int u, int v, int cost) {
            this.u = u;
            this.v = v;
            this.cost = cost;
        }
        @Override
        public int compareTo(Edge other) {
            return Integer.compare(this.cost, other.cost);
        }
    }

    static class DSU {
        int[] parent;
        public DSU(int n) {
            parent = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }
        public int find(int x) {
            if (parent[x] != x) parent[x] = find(parent[x]);
            return parent[x];
        }
        public boolean union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);
            if (rootX == rootY) return false;
            parent[rootX] = rootY;
            return true;
        }
    }

    public long minCost(int n, int[] heights, int[][] existingCables) {
        DSU dsu = new DSU(n);
        int edgesCount = 0;
        
        // Process existing cables (cost 0)
        for (int[] cable : existingCables) {
            if (dsu.union(cable[0], cable[1])) {
                edgesCount++;
            }
        }
        
        // Prepare for sorting
        int[][] sortedBuildings = new int[n][2];
        for (int i = 0; i < n; i++) {
            sortedBuildings[i][0] = heights[i];
            sortedBuildings[i][1] = i; // Original index
        }
        
        Arrays.sort(sortedBuildings, (a, b) -> Integer.compare(a[0], b[0]));
        
        List<Edge> edges = new ArrayList<>();
        for (int i = 0; i < n - 1; i++) {
            int u = sortedBuildings[i][1];
            int v = sortedBuildings[i+1][1];
            int cost = sortedBuildings[i+1][0] - sortedBuildings[i][0];
            edges.add(new Edge(u, v, cost));
        }
        
        Collections.sort(edges);
        
        long totalCost = 0;
        for (Edge edge : edges) {
            if (dsu.union(edge.u, edge.v)) {
                totalCost += edge.cost;
                edgesCount++;
            }
        }
        
        return totalCost;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        
        int n = sc.nextInt();
        int[] heights = new int[n];
        for (int i = 0; i < n; i++) heights[i] = sc.nextInt();
        
        int m = sc.nextInt();
        int[][] existingCables = new int[m][2];
        for (int i = 0; i < m; i++) {
            existingCables[i][0] = sc.nextInt();
            existingCables[i][1] = sc.nextInt();
        }
        
        Solution solution = new Solution();
        System.out.println(solution.minCost(n, heights, existingCables));
        sc.close();
    }
}
```

### Python

```python
import sys

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            self.parent[rootX] = rootY
            return True
        return False

def min_cost(n: int, heights: list, existing_cables: list) -> int:
    dsu = DSU(n)
    
    # Union existing cables
    for u, v in existing_cables:
        dsu.union(u, v)
        
    # Create sorted list of (height, original_index)
    buildings = []
    for i in range(n):
        buildings.append((heights[i], i))
    
    buildings.sort()
    
    # Generate edges between adjacent sorted buildings
    edges = []
    for i in range(n - 1):
        h1, idx1 = buildings[i]
        h2, idx2 = buildings[i+1]
        cost = h2 - h1
        edges.append((cost, idx1, idx2))
        
    edges.sort()
    
    total_cost = 0
    for cost, u, v in edges:
        if dsu.union(u, v):
            total_cost += cost
            
    return total_cost

def main():
    data = sys.stdin.read()
    data = data.split()
    if not data:
        return
        
    idx = 0
    n = int(data[idx])
    idx += 1
    
    heights = []
    for _ in range(n):
        heights.append(int(data[idx]))
        idx += 1
        
    m = int(data[idx])
    idx += 1
    existing_cables = []
    for _ in range(m):
        u = int(data[idx])
        idx += 1
        v = int(data[idx])
        idx += 1
        existing_cables.append([u, v])
        
    print(min_cost(n, heights, existing_cables))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

using namespace std;

struct Edge {
    int u, v, cost;
    bool operator<(const Edge& other) const {
        return cost < other.cost;
    }
};

struct DSU {
    vector<int> parent;
    DSU(int n) {
        parent.resize(n);
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    bool unite(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        if (rootX != rootY) {
            parent[rootX] = rootY;
            return true;
        }
        return false;
    }
};

class Solution {
public:
    long long minCost(int n, vector<int>& heights, vector<pair<int,int>>& existingCables) {
        DSU dsu(n);
        
        for (auto& cable : existingCables) {
            dsu.unite(cable.first, cable.second);
        }
        
        vector<pair<int,int>> sortedBuildings(n);
        for (int i = 0; i < n; i++) {
            sortedBuildings[i] = {heights[i], i};
        }
        
        sort(sortedBuildings.begin(), sortedBuildings.end());
        
        vector<Edge> edges;
        for (int i = 0; i < n - 1; i++) {
            int u = sortedBuildings[i].second;
            int v = sortedBuildings[i+1].second;
            int cost = sortedBuildings[i+1].first - sortedBuildings[i].first;
            edges.push_back({u, v, cost});
        }
        
        sort(edges.begin(), edges.end());
        
        long long totalCost = 0;
        for (const auto& edge : edges) {
            if (dsu.unite(edge.u, edge.v)) {
                totalCost += edge.cost;
            }
        }
        
        return totalCost;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> heights(n);
    for (int i = 0; i < n; i++) cin >> heights[i];

    int m;
    if (!(cin >> m)) return 0; // Should not happen based on constraints but safe check

    vector<pair<int,int>> existingCables(m);
    for (int i = 0; i < m; i++) {
        cin >> existingCables[i].first >> existingCables[i].second;
    }

    Solution solution;
    cout << solution.minCost(n, heights, existingCables) << "\n";

    return 0;
}
```

### JavaScript

```javascript
const readline = require("readline");

class DSU {
  constructor(n) {
    this.parent = Array.from({ length: n }, (_, i) => i);
  }
  find(x) {
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]);
    }
    return this.parent[x];
  }
  union(x, y) {
    const rootX = this.find(x);
    const rootY = this.find(y);
    if (rootX !== rootY) {
      this.parent[rootX] = rootY;
      return true;
    }
    return false;
  }
}

class Solution {
  minCost(n, heights, existingCables) {
    const dsu = new DSU(n);
    
    for (const [u, v] of existingCables) {
      dsu.union(u, v);
    }
    
    const buildings = heights.map((h, i) => ({ h, i }));
    buildings.sort((a, b) => a.h - b.h);
    
    const edges = [];
    for (let i = 0; i < n - 1; i++) {
      const u = buildings[i].i;
      const v = buildings[i + 1].i;
      const cost = buildings[i + 1].h - buildings[i].h;
      edges.push({ u, v, cost });
    }
    
    edges.sort((a, b) => a.cost - b.cost);
    
    let totalCost = 0;
    for (const { u, v, cost } of edges) {
      if (dsu.union(u, v)) {
        totalCost += cost;
      }
    }
    
    return totalCost;
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

let data = [];
rl.on("line", (line) => data.push(line.trim()));
rl.on("close", () => {
  if (data.length === 0) return;
  
  let ptr = 0;
  const n = parseInt(data[ptr++]);
  const heights = data[ptr++].split(" ").map(Number);
  const m = parseInt(data[ptr++]);
  
  const existingCables = [];
  for (let i = 0; i < m; i++) {
    const [u, v] = data[ptr++].split(" ").map(Number);
    existingCables.push([u, v]);
  }

  const solution = new Solution();
  console.log(solution.minCost(n, heights, existingCables));
});
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input:**
```
3
5 1 9
0
```

**Step 1: Sort Buildings**
- (1, idx 1)
- (5, idx 0)
- (9, idx 2)

**Step 2: Generate Edges**
- Between (1, idx 1) and (5, idx 0): Cost `5-1=4`. Edge (1, 0).
- Between (5, idx 0) and (9, idx 2): Cost `9-5=4`. Edge (0, 2).

**Step 3: Kruskal's**
- Edge (1, 0), Cost 4. Union(1, 0). Cost += 4.
- Edge (0, 2), Cost 4. Union(0, 2). Cost += 4.

**Result:** 8.

![Example Visualization](../images/GRD-007/example-1.png)

## ✅ Proof of Correctness

### Invariant
The set of edges formed by adjacent elements in the sorted list contains a Minimum Spanning Tree for the 1D line metric.

### Why the approach is correct
As argued in the Optimal Approach section, any edge between non-adjacent sorted elements `(u, w)` with `h_u < h_v < h_w` has cost `(h_w - h_u) = (h_w - h_v) + (h_v - h_u)`.
The path `u -> v -> w` uses strictly smaller (or equal) edges.
Kruskal's algorithm will always pick the smaller edges `u-v` and `v-w` before considering `u-w`. Once `u-v` and `v-w` are picked, `u` and `w` are connected, so `u-w` is discarded.
Therefore, we never need to consider "jump" edges.

## 💡 Interview Extensions

- **Extension 1:** What if new cables have a fixed installation cost `C` plus the height difference?
- **Extension 2:** What if we are in 2D (coordinates x, y) and cost is Manhattan distance?
  - *Answer:* This is much harder. We need to consider neighbors in 4 quadrants. A sweep-line algorithm or checking nearest neighbors in sorted X and Y lists is needed (approx `4N` edges).
- **Extension 3:** What if we can add "hub" nodes at any height?
  - *Answer:* This becomes a Steiner Tree problem, which is NP-hard in general graphs, but on a 1D line, it's trivial (range min/max).

### Common Mistakes to Avoid

1. **Generating All Edges**
   - ❌ Wrong: `O(N^2)` edges will TLE.
   - ✅ Correct: Only generate `N-1` adjacent edges.

2. **Ignoring Existing Cables**
   - ❌ Wrong: Running MST on just new edges and adding their cost.
   - ⚠️ Issue: Existing cables might connect distant buildings for free, making some intermediate edges redundant.
   - ✅ Correct: Add existing cables to DSU first (or as 0-weight edges).

3. **Index Confusion**
   - ❌ Wrong: Sorting heights and losing track of original indices.
   - ✅ Correct: Store pairs `(height, original_index)`.

## Related Concepts

- **Minimum Spanning Tree:** The core problem.
- **Kruskal's Algorithm:** Greedy edge selection.
- **Coordinate Compression / Sorting:** Reducing search space in geometric graphs.
