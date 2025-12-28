---
problem_id: GRP_SHUTTLE_SHORTEST_STOPS__9247
display_id: GRP-008
slug: shuttle-shortest-stops
title: "Shuttle Shortest Stops"
difficulty: Easy-Medium
difficulty_score: 35
topics:
  - Graph Traversal
  - BFS
  - Shortest Path
tags:
  - graph
  - bfs
  - shortest-path
  - unweighted
  - medium
premium: true
subscription_tier: basic
---

# GRP-008: Shuttle Shortest Stops

## 📋 Problem Summary

Find the shortest distance from a source node to all other nodes in an unweighted undirected graph using BFS. Return distances for all nodes, with -1 for unreachable nodes.

## 🌍 Real-World Scenario

**Scenario Title:** Campus Shuttle Route Optimization

Imagine a university shuttle system where stops are nodes and direct shuttle routes are edges. Students want to know the minimum number of shuttle transfers needed to reach any destination from their starting stop.

BFS naturally computes this because it explores nodes level by level - all stops reachable in 1 transfer, then 2 transfers, etc. This information helps students plan their routes and the university optimize shuttle schedules.

**Why This Problem Matters:**

- **Transportation Networks:** Finding minimum transfers in public transit
- **Social Networks:** Degrees of separation between people
- **Network Routing:** Hop count in computer networks
- **Game AI:** Shortest path for NPCs in grid-based games

![Real-World Application](../images/GRP-008/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: BFS Shortest Path

```
Graph:
    0 --- 1 --- 2
    |           |
    3 --- 4 ----+

Source: 0

BFS levels:
Level 0: [0] (distance 0)
Level 1: [1, 3] (distance 1)
Level 2: [2, 4] (distance 2)

Distances: [0, 1, 2, 1, 2]
```

## ✅ Input/Output Clarifications (Read This Before Coding)

- **Distance definition:** Minimum number of edges from source to target
- **Unreachable nodes:** Return -1 for nodes not connected to source
- **Source distance:** Always 0 to itself
- **BFS guarantee:** First time a node is visited = shortest path

## Optimal Approach

### Algorithm

```
shortest_distances(n, adj, source):
    dist = [-1] * n
    dist[source] = 0
    queue = [source]
    
    while queue not empty:
        node = queue.dequeue()
        
        for neighbor in adj[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.enqueue(neighbor)
    
    return dist
```

### Time Complexity: **O(V + E)**
### Space Complexity: **O(V)**

![Algorithm Visualization](../images/GRP-008/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public int[] shortestDistances(int n, List<List<Integer>> adj, int source) {
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        dist[source] = 0;
        
        Queue<Integer> queue = new LinkedList<>();
        queue.offer(source);
        
        while (!queue.isEmpty()) {
            int node = queue.poll();
            
            for (int neighbor : adj.get(node)) {
                if (dist[neighbor] == -1) {
                    dist[neighbor] = dist[node] + 1;
                    queue.offer(neighbor);
                }
            }
        }
        
        return dist;
    }
}
```

### Python

```python
from collections import deque
from typing import List

def shortest_distances(n: int, adj: List[List[int]], source: int) -> List[int]:
    dist = [-1] * n
    dist[source] = 0
    queue = deque([source])
    
    while queue:
        node = queue.popleft()
        
        for neighbor in adj[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    
    return dist

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # BFS from node 0, return max distance
    from collections import deque
    dist = [-1] * n
    dist[0] = 0
    queue = deque([0])
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    
    max_dist = max(d for d in dist if d != -1)
    print(max_dist)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    vector<int> shortestDistances(int n, vector<vector<int>>& adj, int source) {
        vector<int> dist(n, -1);
        dist[source] = 0;
        
        queue<int> q;
        q.push(source);
        
        while (!q.empty()) {
            int node = q.front();
            q.pop();
            
            for (int neighbor : adj[node]) {
                if (dist[neighbor] == -1) {
                    dist[neighbor] = dist[node] + 1;
                    q.push(neighbor);
                }
            }
        }
        
        return dist;
    }
};
```

### JavaScript

```javascript
class Solution {
  shortestDistances(n, adj, source) {
    const dist = new Array(n).fill(-1);
    dist[source] = 0;
    const queue = [source];
    
    while (queue.length > 0) {
      const node = queue.shift();
      
      for (const neighbor of adj[node]) {
        if (dist[neighbor] === -1) {
          dist[neighbor] = dist[node] + 1;
          queue.push(neighbor);
        }
      }
    }
    
    return dist;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)

Graph: 0-1, 1-2, 0-3, 3-4, Source: 0

| Step | Queue | Node | Neighbors | Distances |
|-----:|:-----:|:----:|:---------:|:----------|
| 0 | [0] | - | - | [0,-1,-1,-1,-1] |
| 1 | [1,3] | 0 | 1,3 | [0,1,-1,1,-1] |
| 2 | [3,2] | 1 | 0,2 | [0,1,2,1,-1] |
| 3 | [2,4] | 3 | 0,4 | [0,1,2,1,2] |
| 4 | [4] | 2 | 1 | [0,1,2,1,2] |
| 5 | [] | 4 | 3 | [0,1,2,1,2] |

Answer: `[0, 1, 2, 1, 2]`

![Example Visualization](../images/GRP-008/example-1.png)

## ✅ Proof of Correctness

**Theorem:** BFS finds shortest paths in unweighted graphs.

**Proof:** BFS explores nodes in increasing order of distance. When a node is first visited, it's via the shortest path (no shorter path exists, as BFS would have found it earlier).

## 💡 Interview Extensions (High-Value Add-ons)

- **Extension 1:** Return the actual shortest paths, not just distances
- **Extension 2:** Find shortest path between two specific nodes (bidirectional BFS)
- **Extension 3:** Handle weighted graphs (use Dijkstra instead)
- **Extension 4:** Find all shortest paths (not just one)

### Common Mistakes to Avoid

1. **Using DFS Instead of BFS**
   - ❌ Wrong: DFS doesn't guarantee shortest path
   - ✅ Correct: BFS explores level by level
   - **Impact:** Incorrect distances

2. **Not Initializing Distances**
   - ❌ Wrong: Using 0 or random values
   - ✅ Correct: Initialize all to -1 except source
   - **Description:** Causes incorrect distance calculations

3. **Updating Distance Multiple Times**
   - ❌ Wrong: Updating dist[neighbor] even if already visited
   - ✅ Correct: Only update if dist[neighbor] == -1
   - **Prevention:** First visit = shortest path in BFS

4. **Forgetting to Enqueue**
   - ❌ Wrong: Updating distance but not adding to queue
   - ✅ Correct: Update distance AND enqueue
   - **Description:** Incomplete traversal

5. **Wrong Distance Calculation**
   - ❌ Wrong: `dist[neighbor] = dist[node]`
   - ✅ Correct: `dist[neighbor] = dist[node] + 1`
   - **Description:** Off-by-one error

## Related Concepts

- **Dijkstra's Algorithm:** Shortest path in weighted graphs
- **Bellman-Ford:** Handles negative weights
- **Floyd-Warshall:** All-pairs shortest paths
- **A* Search:** Heuristic-guided shortest path
- **Bidirectional BFS:** Optimization for single-pair shortest path
