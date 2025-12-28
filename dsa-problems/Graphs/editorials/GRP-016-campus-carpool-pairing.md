---
problem_id: GRP_CAMPUS_CARPOOL_PAIRING__2914
display_id: GRP-016
slug: campus-carpool-pairing
title: Campus Carpool Pairing
difficulty: Medium
difficulty_score: 45
topics:
- Union-Find
- Cycle Detection
- Forest
tags:
- graph
- union-find
- cycle-detection
- forest
- medium
premium: true
subscription_tier: basic
---
# GRP-016: Campus Carpool Pairing

## 📋 Problem Summary

Determine if adding a new edge creates a cycle in an undirected graph using Union-Find. A graph is a forest (acyclic) if no cycles exist. Return true if the graph remains a forest after adding the edge.

## 🌍 Real-World Scenario

**Scenario Title:** Network Connection Validation

Imagine building a computer network where you want to avoid redundant connections (cycles) to minimize cost while maintaining connectivity. Before adding a new cable, you need to verify it won't create a cycle.

Union-Find efficiently detects if two nodes are already connected. If they are, adding an edge between them creates a cycle. This is crucial for network design, spanning tree construction, and resource optimization.

**Why This Problem Matters:**

- **Network Design:** Avoiding redundant connections
- **Spanning Tree Construction:** Building minimal connected graphs
- **Resource Optimization:** Minimizing infrastructure costs
- **Kruskal's MST:** Core component of the algorithm

![Real-World Application](../images/GRP-016/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: Cycle Detection with Union-Find

```
Current graph (forest):
    0 --- 1
    
    2 --- 3

Adding edge (1, 2):
    0 --- 1
          |
    2 --- 3

Result: Still a forest (no cycle)

Adding edge (0, 3):
    0 --- 1
    |     |
    2 --- 3

Result: Cycle detected! (0-1-2-3-0)
```

## ✅ Input/Output Clarifications (Read This Before Coding)

- **Forest:** Graph with no cycles (collection of trees)
- **Cycle detection:** If find(u) == find(v), adding (u,v) creates cycle
- **Union-Find:** Efficiently tracks connected components
- **Return:** true if remains forest, false if cycle created

## Optimal Approach

### Algorithm

```
is_forest_after_adding(n, existing_edges, new_edge):
    uf = UnionFind(n)
    
    // Build current graph
    for (u, v) in existing_edges:
        if uf.find(u) == uf.find(v):
            return false  // Already has cycle
        uf.union(u, v)
    
    // Check new edge
    (u, v) = new_edge
    if uf.find(u) == uf.find(v):
        return false  // Would create cycle
    
    return true  // Remains a forest
```

### Time Complexity: **O(E × α(n))** where α is inverse Ackermann
### Space Complexity: **O(n)**

![Algorithm Visualization](../images/GRP-016/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class UnionFind {
    private int[] parent;
    private int[] rank;
    
    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
    }
    
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    public boolean union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX == rootY) {
            return false;  // Already in same set (would create cycle)
        }
        
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
        } else {
            parent[rootY] = rootX;
            rank[rootX]++;
        }
        
        return true;
    }
}

class Solution {
    public boolean isForestAfterAdding(int n, int[][] existingEdges, int[] newEdge) {
        UnionFind uf = new UnionFind(n);
        
        // Build current graph
        for (int[] edge : existingEdges) {
            if (!uf.union(edge[0], edge[1])) {
                return false;  // Already has cycle
            }
        }
        
        // Check new edge
        return uf.find(newEdge[0]) != uf.find(newEdge[1]);
    }
}
```

### Python

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same set (would create cycle)
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True

def is_forest_after_adding(n, existing_edges, new_edge):
    uf = UnionFind(n)
    
    # Build current graph
    for u, v in existing_edges:
        if not uf.union(u, v):
            return False  # Already has cycle
    
    # Check new edge
    return uf.find(new_edge[0]) != uf.find(new_edge[1])

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Count edges in graph
    edge_count = sum(len(adj[i]) for i in range(n)) // 2
    print(edge_count)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

class UnionFind {
private:
    vector<int> parent;
    vector<int> rank;
    
public:
    UnionFind(int n) : parent(n), rank(n, 0) {
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
    }
    
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    bool unite(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX == rootY) {
            return false;  // Already in same set (would create cycle)
        }
        
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
        } else {
            parent[rootY] = rootX;
            rank[rootX]++;
        }
        
        return true;
    }
};

class Solution {
public:
    bool isForestAfterAdding(int n, vector<vector<int>>& existingEdges, vector<int>& newEdge) {
        UnionFind uf(n);
        
        // Build current graph
        for (auto& edge : existingEdges) {
            if (!uf.unite(edge[0], edge[1])) {
                return false;  // Already has cycle
            }
        }
        
        // Check new edge
        return uf.find(newEdge[0]) != uf.find(newEdge[1]);
    }
};
```

### JavaScript

```javascript
class UnionFind {
  constructor(n) {
    this.parent = Array.from({ length: n }, (_, i) => i);
    this.rank = Array(n).fill(0);
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
    
    if (rootX === rootY) {
      return false;  // Already in same set (would create cycle)
    }
    
    if (this.rank[rootX] < this.rank[rootY]) {
      this.parent[rootX] = rootY;
    } else if (this.rank[rootX] > this.rank[rootY]) {
      this.parent[rootY] = rootX;
    } else {
      this.parent[rootY] = rootX;
      this.rank[rootX]++;
    }
    
    return true;
  }
}

class Solution {
  isForestAfterAdding(n, existingEdges, newEdge) {
    const uf = new UnionFind(n);
    
    // Build current graph
    for (const [u, v] of existingEdges) {
      if (!uf.union(u, v)) {
        return false;  // Already has cycle
      }
    }
    
    // Check new edge
    return uf.find(newEdge[0]) !== uf.find(newEdge[1]);
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)

n=4, existing_edges=[(0,1), (2,3)], new_edge=(1,2)

1. Union(0,1): {0,1}, {2}, {3} ✓
2. Union(2,3): {0,1}, {2,3} ✓
3. Check new_edge(1,2): find(1)=0, find(2)=2, different roots ✓

Result: Remains a forest

![Example Visualization](../images/GRP-016/example-1.png)

## ✅ Proof of Correctness

**Theorem:** Union-Find correctly detects cycles in undirected graphs.

**Proof:** If find(u) == find(v), u and v are already connected. Adding edge (u,v) creates a cycle. Union-Find maintains disjoint sets, ensuring correct connectivity tracking.

## 💡 Interview Extensions (High-Value Add-ons)

- **Extension 1:** Return which edge to remove to break cycle
- **Extension 2:** Count number of trees in forest
- **Extension 3:** Find all edges that would create cycles
- **Extension 4:** Implement Kruskal's MST algorithm

### Common Mistakes to Avoid

1. **Not Checking Existing Edges**
   - ❌ Wrong: Only checking new edge
   - ✅ Correct: Build graph first, then check new edge
   - **Impact:** Misses existing cycles

2. **Using Union Return Value Incorrectly**
   - ❌ Wrong: Ignoring union's return value
   - ✅ Correct: Return false if union fails (cycle detected)
   - **Description:** Union returns false when roots are same

3. **Forgetting Path Compression**
   - ❌ Wrong: Simple find without optimization
   - ✅ Correct: Implement path compression
   - **Prevention:** Ensures O(α(n)) amortized time

4. **Not Using Rank/Size**
   - ❌ Wrong: Always attaching to first root
   - ✅ Correct: Union by rank or size
   - **Description:** Prevents tree degradation

5. **Directed vs Undirected Confusion**
   - ❌ Wrong: Treating edges as directed
   - ✅ Correct: Undirected edges (u,v) same as (v,u)
   - **Description:** Union-Find works for undirected graphs

## Related Concepts

- **Kruskal's MST:** Uses Union-Find for cycle detection
- **Cycle Detection in Undirected Graphs:** Core application
- **Minimum Spanning Tree:** Forest with minimum total weight
- **Dynamic Connectivity:** Online Union-Find queries
