---
problem_id: GRP_CITY_TOLL_DIJKSTRA__7561
display_id: GRP-009
slug: city-toll-dijkstra
title: City Toll Dijkstra
difficulty: Medium
difficulty_score: 55
topics:
- Shortest Path
- Dijkstra's Algorithm
- Priority Queue
tags:
- graph
- dijkstra
- shortest-path
- weighted-graph
- priority-queue
- medium
premium: true
subscription_tier: basic
---
# GRP-009: City Toll Dijkstra

## 📋 Problem Summary

Compute shortest path distances from a source node to all other nodes in a weighted directed graph with non-negative edge weights using Dijkstra's algorithm.

## 🌍 Real-World Scenario

**Scenario Title:** City Navigation with Toll Roads

Imagine a GPS navigation system where roads have different toll costs (edge weights). The system needs to find the cheapest route from your location to all possible destinations, considering toll costs.

Dijkstra's algorithm greedily selects the next closest unvisited node, ensuring we always find the minimum cost path. This is how modern GPS systems calculate optimal routes considering factors like tolls, distance, or time.

**Why This Problem Matters:**

- **GPS Navigation:** Finding shortest/cheapest routes
- **Network Routing:** Packet routing in computer networks
- **Logistics:** Optimizing delivery routes
- **Game AI:** Pathfinding with terrain costs

![Real-World Application](../images/GRP-009/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: Dijkstra's Algorithm

```
Weighted graph:
    0 --2--> 1 --4--> 3
    |        |
    5        1
    |        |
    v        v
    2 --1--> 3

Source: 0

Dijkstra's process:
1. dist[0]=0, others=∞
2. Process 0: update dist[1]=2, dist[2]=5
3. Process 1 (min): update dist[3]=6, dist[2]=3
4. Process 2 (min): update dist[3]=4
5. Process 3 (min): done

Final distances: [0, 2, 3, 4]
```

## ✅ Input/Output Clarifications (Read This Before Coding)

- **Non-negative weights:** Dijkstra requires all weights ≥ 0
- **Directed edges:** Edge u→v only allows traversal from u to v
- **Unreachable nodes:** Return very large value (10^18) or -1
- **Priority queue:** Min-heap for efficient minimum extraction

## Optimal Approach

### Algorithm

```
dijkstra(n, adj, source):
    dist = [∞] * n
    dist[source] = 0
    pq = MinHeap()
    pq.add((0, source))  // (distance, node)
    
    while pq not empty:
        (d, node) = pq.extract_min()
        
        if d > dist[node]:
            continue  // Skip outdated entry
        
        for (neighbor, weight) in adj[node]:
            new_dist = dist[node] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                pq.add((new_dist, neighbor))
    
    return dist
```

### Time Complexity: **O((V + E) log V)** with binary heap
### Space Complexity: **O(V)**

![Algorithm Visualization](../images/GRP-009/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public long[] dijkstra(int n, List<List<int[]>> adj, int source) {
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[source] = 0;
        
        PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        pq.offer(new long[]{0, source});
        
        while (!pq.isEmpty()) {
            long[] curr = pq.poll();
            long d = curr[0];
            int node = (int)curr[1];
            
            if (d > dist[node]) continue;
            
            for (int[] edge : adj.get(node)) {
                int neighbor = edge[0];
                long weight = edge[1];
                long newDist = dist[node] + weight;
                
                if (newDist < dist[neighbor]) {
                    dist[neighbor] = newDist;
                    pq.offer(new long[]{newDist, neighbor});
                }
            }
        }
        
        return dist;
    }
}
```

### Python

```python
import heapq
from typing import List

def dijkstra(n: int, adj: List[List[tuple]], source: int) -> List[int]:
    dist = [float('inf')] * n
    dist[source] = 0
    pq = [(0, source)]  # (distance, node)
    
    while pq:
        d, node = heapq.heappop(pq)
        
        if d > dist[node]:
            continue
        
        for neighbor, weight in adj[node]:
            new_dist = dist[node] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    
    return dist

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    # Dijkstra from node 0
    import heapq
    dist = [float('inf')] * n
    dist[0] = 0
    pq = [(0, 0)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    
    # Return sum of all finite distances
    result = sum(d for d in dist if d != float('inf'))
    print(result)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <climits>
using namespace std;

class Solution {
public:
    vector<long long> dijkstra(int n, vector<vector<pair<int,int>>>& adj, int source) {
        vector<long long> dist(n, LLONG_MAX);
        dist[source] = 0;
        
        priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
        pq.push({0, source});
        
        while (!pq.empty()) {
            auto [d, node] = pq.top();
            pq.pop();
            
            if (d > dist[node]) continue;
            
            for (auto [neighbor, weight] : adj[node]) {
                long long newDist = dist[node] + weight;
                if (newDist < dist[neighbor]) {
                    dist[neighbor] = newDist;
                    pq.push({newDist, neighbor});
                }
            }
        }
        
        return dist;
    }
};
```

### JavaScript

```javascript
class MinHeap {
  constructor() {
    this.heap = [];
  }
  
  push(val) {
    this.heap.push(val);
    this.bubbleUp(this.heap.length - 1);
  }
  
  pop() {
    if (this.heap.length === 0) return null;
    const min = this.heap[0];
    const end = this.heap.pop();
    if (this.heap.length > 0) {
      this.heap[0] = end;
      this.bubbleDown(0);
    }
    return min;
  }
  
  bubbleUp(idx) {
    while (idx > 0) {
      const parent = Math.floor((idx - 1) / 2);
      if (this.heap[parent][0] <= this.heap[idx][0]) break;
      [this.heap[parent], this.heap[idx]] = [this.heap[idx], this.heap[parent]];
      idx = parent;
    }
  }
  
  bubbleDown(idx) {
    while (true) {
      let smallest = idx;
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;
      
      if (left < this.heap.length && this.heap[left][0] < this.heap[smallest][0]) {
        smallest = left;
      }
      if (right < this.heap.length && this.heap[right][0] < this.heap[smallest][0]) {
        smallest = right;
      }
      if (smallest === idx) break;
      
      [this.heap[idx], this.heap[smallest]] = [this.heap[smallest], this.heap[idx]];
      idx = smallest;
    }
  }
  
  isEmpty() {
    return this.heap.length === 0;
  }
}

class Solution {
  dijkstra(n, adj, source) {
    const dist = new Array(n).fill(Infinity);
    dist[source] = 0;
    const pq = new MinHeap();
    pq.push([0, source]);
    
    while (!pq.isEmpty()) {
      const [d, node] = pq.pop();
      
      if (d > dist[node]) continue;
      
      for (const [neighbor, weight] of adj[node]) {
        const newDist = dist[node] + weight;
        if (newDist < dist[neighbor]) {
          dist[neighbor] = newDist;
          pq.push([newDist, neighbor]);
        }
      }
    }
    
    return dist;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)

Graph: 0→1(2), 0→2(5), 1→3(4), 2→3(1), 1→2(1)

| Step | PQ | Node | dist[0] | dist[1] | dist[2] | dist[3] |
|-----:|:--:|:----:|:-------:|:-------:|:-------:|:-------:|
| 0 | [(0,0)] | - | 0 | ∞ | ∞ | ∞ |
| 1 | [(2,1),(5,2)] | 0 | 0 | 2 | 5 | ∞ |
| 2 | [(3,2),(5,2),(6,3)] | 1 | 0 | 2 | 3 | 6 |
| 3 | [(4,3),(5,2),(6,3)] | 2 | 0 | 2 | 3 | 4 |
| 4 | [(5,2),(6,3)] | 3 | 0 | 2 | 3 | 4 |

Final: `[0, 2, 3, 4]`

![Example Visualization](../images/GRP-009/example-1.png)

## ✅ Proof of Correctness

**Theorem:** Dijkstra's algorithm finds shortest paths in graphs with non-negative weights.

**Proof (Greedy Choice):** When we extract a node from the priority queue, we've found its shortest path. Any other path would go through an unprocessed node with higher distance.

## 💡 Interview Extensions (High-Value Add-ons)

- **Extension 1:** Return the actual shortest paths, not just distances
- **Extension 2:** Handle negative weights (use Bellman-Ford)
- **Extension 3:** A* search (Dijkstra with heuristic)
- **Extension 4:** Bidirectional Dijkstra for single-pair shortest path

### Common Mistakes to Avoid

1. **Using Dijkstra with Negative Weights**
   - ❌ Wrong: Applying Dijkstra to graphs with negative edges
   - ✅ Correct: Use Bellman-Ford for negative weights
   - **Impact:** Incorrect results

2. **Not Skipping Outdated Entries**
   - ❌ Wrong: Processing all priority queue entries
   - ✅ Correct: Skip if `d > dist[node]`
   - **Description:** Efficiency issue, may cause incorrect updates

3. **Wrong Priority Queue Comparison**
   - ❌ Wrong: Max-heap instead of min-heap
   - ✅ Correct: Min-heap (smallest distance first)
   - **Prevention:** Ensure correct comparator

4. **Forgetting to Initialize Distances**
   - ❌ Wrong: Starting with 0 or random values
   - ✅ Correct: Initialize all to ∞ except source
   - **Description:** Causes incorrect distance calculations

5. **Not Handling Integer Overflow**
   - ❌ Wrong: Using int for large weights
   - ✅ Correct: Use long/long long for distances
   - **Description:** Overflow causes incorrect results

## Related Concepts

- **Bellman-Ford:** Handles negative weights
- **Floyd-Warshall:** All-pairs shortest paths
- **A* Search:** Heuristic-guided Dijkstra
- **Prim's MST:** Similar greedy approach
- **BFS:** Special case for unweighted graphs
