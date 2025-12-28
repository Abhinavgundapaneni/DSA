---
problem_id: GRP_ROBOTICS_BRIDGES__4172
display_id: GRP-013
slug: robotics-bridges
title: Robotics Bridges
difficulty: Medium
difficulty_score: 60
topics:
- Graph Theory
- Tarjan's Algorithm
- Bridges
tags:
- graph
- tarjan
- bridges
- critical-edges
- hard
premium: true
subscription_tier: premium
---
# GRP-013: Robotics Bridges

## 📋 Problem Summary

Find all bridges (critical edges) in an undirected graph using Tarjan's algorithm. A bridge is an edge whose removal increases the number of connected components.

## 🌍 Real-World Scenario

**Scenario Title:** Critical Infrastructure Identification

Imagine analyzing a transportation network where roads connect cities. A bridge road is critical - if it's closed for maintenance, some cities become unreachable from others. Identifying these critical roads helps prioritize maintenance and plan redundant routes.

Tarjan's algorithm efficiently finds all such critical edges in a single DFS traversal, making it ideal for large networks. This is crucial for infrastructure planning, network reliability analysis, and disaster preparedness.

**Why This Problem Matters:**

- **Network Reliability:** Identifying single points of failure
- **Infrastructure Planning:** Prioritizing redundancy for critical connections
- **Social Network Analysis:** Finding key relationships
- **Circuit Design:** Identifying critical connections

![Real-World Application](../images/GRP-013/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: Bridges in a Graph

```
Graph:
    0 --- 1 --- 2
          |     |
          3 --- 4

Bridges: (0,1), (1,3)

Why?
- Removing (0,1): {0} and {1,2,3,4} become disconnected
- Removing (1,3): {0,1,2,4} and {3} become disconnected
- Removing (1,2), (2,4), or (3,4): Graph stays connected (cycle exists)
```

## ✅ Input/Output Clarifications (Read This Before Coding)

- **Bridge definition:** Edge whose removal increases component count
- **Discovery time:** Time when node is first visited in DFS
- **Low value:** Minimum discovery time reachable from subtree
- **Bridge condition:** `low[v] > disc[u]` for edge (u,v)

## Optimal Approach

### Algorithm (Tarjan's Bridges)

```
find_bridges(n, adj):
    disc = [-1] * n  // Discovery time
    low = [-1] * n   // Low value
    parent = [-1] * n
    bridges = []
    time = [0]  // Mutable counter
    
    def dfs(u):
        disc[u] = low[u] = time[0]
        time[0] += 1
        
        for v in adj[u]:
            if disc[v] == -1:  // Unvisited
                parent[v] = u
                dfs(v)
                
                low[u] = min(low[u], low[v])
                
                // Bridge condition
                if low[v] > disc[u]:
                    bridges.append((u, v))
            
            elif v != parent[u]:  // Back edge
                low[u] = min(low[u], disc[v])
    
    for i in 0 to n-1:
        if disc[i] == -1:
            dfs(i)
    
    return bridges
```

### Time Complexity: **O(V + E)**
### Space Complexity: **O(V)**

![Algorithm Visualization](../images/GRP-013/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    private int time = 0;
    private List<int[]> bridges;
    
    public List<int[]> findBridges(int n, List<List<Integer>> adj) {
        int[] disc = new int[n];
        int[] low = new int[n];
        int[] parent = new int[n];
        Arrays.fill(disc, -1);
        Arrays.fill(parent, -1);
        bridges = new ArrayList<>();
        
        for (int i = 0; i < n; i++) {
            if (disc[i] == -1) {
                dfs(i, adj, disc, low, parent);
            }
        }
        
        return bridges;
    }
    
    private void dfs(int u, List<List<Integer>> adj, int[] disc, int[] low, int[] parent) {
        disc[u] = low[u] = time++;
        
        for (int v : adj.get(u)) {
            if (disc[v] == -1) {
                parent[v] = u;
                dfs(v, adj, disc, low, parent);
                
                low[u] = Math.min(low[u], low[v]);
                
                if (low[v] > disc[u]) {
                    bridges.add(new int[]{u, v});
                }
            } else if (v != parent[u]) {
                low[u] = Math.min(low[u], disc[v]);
            }
        }
    }
}
```

### Python

```python
from typing import List

def find_bridges(n: int, adj: List[List[int]]) -> List[tuple]:
    disc = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    bridges = []
    time = [0]
    
    def dfs(u):
        disc[u] = low[u] = time[0]
        time[0] += 1
        
        for v in adj[u]:
            if disc[v] == -1:
                parent[v] = u
                dfs(v)
                
                low[u] = min(low[u], low[v])
                
                if low[v] > disc[u]:
                    bridges.append((u, v))
            
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])
    
    for i in range(n):
        if disc[i] == -1:
            dfs(i)
    
    return bridges

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Find bridges using Tarjan's algorithm
    visited = [False] * n
    disc = [0] * n
    low = [0] * n
    parent = [-1] * n
    bridges = []
    timer = [0]
    
    def dfs(u):
        visited[u] = True
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        
        for v in adj[u]:
            if not visited[v]:
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                
                if low[v] > disc[u]:
                    bridges.append((min(u,v), max(u,v)))
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])
    
    for i in range(n):
        if not visited[i]:
            dfs(i)
    
    print(len(bridges))

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
private:
    int timer = 0;
    vector<pair<int,int>> bridges;
    
    void dfs(int u, vector<vector<int>>& adj, vector<int>& disc, 
             vector<int>& low, vector<int>& parent) {
        disc[u] = low[u] = timer++;
        
        for (int v : adj[u]) {
            if (disc[v] == -1) {
                parent[v] = u;
                dfs(v, adj, disc, low, parent);
                
                low[u] = min(low[u], low[v]);
                
                if (low[v] > disc[u]) {
                    bridges.push_back({u, v});
                }
            } else if (v != parent[u]) {
                low[u] = min(low[u], disc[v]);
            }
        }
    }
    
public:
    vector<pair<int,int>> findBridges(int n, vector<vector<int>>& adj) {
        vector<int> disc(n, -1);
        vector<int> low(n, -1);
        vector<int> parent(n, -1);
        
        for (int i = 0; i < n; i++) {
            if (disc[i] == -1) {
                dfs(i, adj, disc, low, parent);
            }
        }
        
        return bridges;
    }
};
```

### JavaScript

```javascript
class Solution {
  findBridges(n, adj) {
    const disc = Array(n).fill(-1);
    const low = Array(n).fill(-1);
    const parent = Array(n).fill(-1);
    const bridges = [];
    let time = 0;
    
    const dfs = (u) => {
      disc[u] = low[u] = time++;
      
      for (const v of adj[u]) {
        if (disc[v] === -1) {
          parent[v] = u;
          dfs(v);
          
          low[u] = Math.min(low[u], low[v]);
          
          if (low[v] > disc[u]) {
            bridges.push([u, v]);
          }
        } else if (v !== parent[u]) {
          low[u] = Math.min(low[u], disc[v]);
        }
      }
    };
    
    for (let i = 0; i < n; i++) {
      if (disc[i] === -1) {
        dfs(i);
      }
    }
    
    return bridges;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)

Graph: 0-1, 1-2, 2-1 (cycle), 1-3

| Node | disc | low | Parent | Action | Bridges Found |
|-----:|:----:|:---:|:------:|:-------|:--------------|
| 0 | 0 | 0 | -1 | Start DFS | - |
| 1 | 1 | 0 | 0 | Visit from 0, low[1]=min(low[1],low[0])=0 | (0,1) is bridge (low[1]=0 > disc[0]=0? No, wait...) |
| 2 | 2 | 1 | 1 | Visit from 1 | - |
| 1 | 1 | 1 | 0 | Back edge 2→1, low[2]=min(2,1)=1, then low[1]=min(1,1)=1 | - |
| 3 | 3 | 3 | 1 | Visit from 1, low[3]=3 > disc[1]=1 | (1,3) is bridge |

Bridges: [(0,1), (1,3)]

![Example Visualization](../images/GRP-013/example-1.png)

## ✅ Proof of Correctness

**Theorem:** Tarjan's algorithm correctly identifies all bridges.

**Proof:** An edge (u,v) is a bridge iff there's no back edge from v's subtree to u or above. This is captured by `low[v] > disc[u]`.

## 💡 Interview Extensions (High-Value Add-ons)

- **Extension 1:** Find articulation points (vertices whose removal disconnects graph)
- **Extension 2:** Count components after removing each bridge
- **Extension 3:** Find all edge-disjoint paths
- **Extension 4:** Handle directed graphs (find strongly connected components)

### Common Mistakes to Avoid

1. **Wrong Bridge Condition**
   - ❌ Wrong: `low[v] >= disc[u]`
   - ✅ Correct: `low[v] > disc[u]`
   - **Impact:** Incorrectly identifies non-bridges as bridges

2. **Not Handling Parent Edge**
   - ❌ Wrong: Updating low[u] with parent's disc
   - ✅ Correct: Skip parent edge (`v != parent[u]`)
   - **Description:** Incorrectly treats tree edge as back edge

3. **Using Global Time Variable Incorrectly**
   - ❌ Wrong: Not incrementing time or using local variable
   - ✅ Correct: Use mutable counter (list in Python, class variable in Java)
   - **Prevention:** Ensure time is shared across all DFS calls

4. **Forgetting Multiple Components**
   - ❌ Wrong: Only starting DFS from node 0
   - ✅ Correct: Start DFS from all unvisited nodes
   - **Description:** Misses bridges in disconnected components

5. **Updating low[u] After Finding Bridge**
   - ❌ Wrong: Not updating low[u] with low[v]
   - ✅ Correct: Always update `low[u] = min(low[u], low[v])`
   - **Description:** Affects detection of other bridges

## Related Concepts

- **Articulation Points:** Vertices whose removal disconnects graph
- **Strongly Connected Components:** Tarjan's SCC algorithm
- **Biconnected Components:** Maximal subgraphs with no bridges
- **Cut Vertices:** Similar to articulation points
- **Network Reliability:** Identifying critical infrastructure
