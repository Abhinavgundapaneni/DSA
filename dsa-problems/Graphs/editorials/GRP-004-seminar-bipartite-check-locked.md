---
problem_id: GRP_SEMINAR_BIPARTITE_LOCKED__6927
display_id: GRP-004
slug: seminar-bipartite-check-locked
title: "Seminar Bipartite Check with Locked Nodes"
difficulty: Medium
difficulty_score: 50
topics:
  - Graph Coloring
  - Bipartite Graphs
  - BFS
  - DFS
tags:
  - graph
  - bipartite
  - coloring
  - bfs
  - dfs
  - medium
premium: true
subscription_tier: basic
---

# GRP-004: Seminar Bipartite Check with Locked Nodes

## 📋 Problem Summary

Determine if an undirected graph can be 2-colored (bipartite) while respecting pre-colored (locked) nodes. Some nodes are locked to specific colors (group A or B), and we must check if a valid bipartite coloring exists that satisfies all constraints.

## 🌍 Real-World Scenario

**Scenario Title:** Seminar Room Assignment with VIP Seating

Imagine organizing a university seminar where students must be divided into two discussion groups (A and B). Some students have conflicts and cannot be in the same group (represented by edges). Additionally, certain VIP students or faculty are pre-assigned to specific groups and cannot be moved.

The challenge is to assign remaining students to groups such that no two connected students are in the same group, while respecting the locked assignments. This is a constrained bipartite checking problem - we need to verify if such an assignment is possible.

For example, if two VIP students who have a conflict are both locked to group A, no valid assignment exists. However, if they're locked to different groups or if there's flexibility in other assignments, a solution might be possible.

**Why This Problem Matters:**

- **Scheduling with Constraints:** Assigning shifts/tasks with pre-existing commitments
- **Resource Allocation:** Distributing resources with fixed assignments
- **Conflict Resolution:** Managing incompatible requirements with locked constraints
- **Seating Arrangements:** Event planning with VIP or reserved seating

![Real-World Application](../images/GRP-004/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: Bipartite with Locked Nodes

```
Graph (cycle of 4 nodes):

    0 --- 1
    |     |
    3 --- 2

Locked array: [1, 0, 0, 2]
- Node 0: Locked to group A (1)
- Node 1: Unlocked (0)
- Node 2: Unlocked (0)
- Node 3: Locked to group B (2)

Valid coloring:
Node 0: A (locked)
Node 1: B (must differ from 0)
Node 2: A (must differ from 1)
Node 3: B (locked, must differ from 2) ✓

This is valid because:
- 0-1 edge: A-B ✓
- 1-2 edge: B-A ✓
- 2-3 edge: A-B ✓
- 3-0 edge: B-A ✓

Legend:
A = Group A (color 1)
B = Group B (color 2)
0 = Unlocked (can be either)
```

## ✅ Input/Output Clarifications (Read This Before Coding)

- **Locked values:** 0 = unlocked, 1 = locked to group A, 2 = locked to group B
- **Bipartite property:** No two adjacent nodes can have the same color
- **Conflict detection:** If a locked node's required color conflicts with its forced color, return false
- **Disconnected components:** Handle each component separately
- **Color assignment:** Unlocked nodes get colored based on their neighbors

Common interpretation mistake:

- ❌ **Wrong:** Ignoring locked constraints and just checking standard bipartite
- ✅ **Correct:** Respecting locked nodes and checking if coloring is still possible

### Core Concept

Use BFS/DFS for graph coloring. When visiting a node:
1. If it's locked, check if the required color matches the locked color
2. If unlocked, assign the opposite color of its parent
3. If there's a conflict, return false

## Naive Approach

### Intuition

Perform standard bipartite checking but add validation for locked nodes at each step.

### Algorithm

1. Create color array initialized to -1 (uncolored)
2. For locked nodes, set color[i] = locked[i]
3. For each unvisited node:
   - Start BFS/DFS with appropriate color
   - For each neighbor:
     - If uncolored: assign opposite color
     - If colored: check if it's the opposite color
     - If locked: verify the assignment matches the lock
4. Return true if no conflicts, false otherwise

### Time Complexity

- **O(V + E)** - Visit each node and edge once

### Space Complexity

- **O(V)** - For color array and BFS queue

### Why This Works

Standard bipartite checking with additional locked node validation ensures we respect pre-existing constraints while maintaining the bipartite property.

## Optimal Approach

### Key Insight

The naive approach is optimal. The key is to handle locked nodes carefully during BFS/DFS traversal.

### Algorithm

```
can_color_bipartite(n, adj, locked):
    color = [-1] * n
    
    # Pre-color locked nodes
    for i in 0 to n-1:
        if locked[i] != 0:
            color[i] = locked[i]
    
    for i in 0 to n-1:
        if color[i] == -1:
            if not bfs(i, adj, color, locked):
                return false
    
    return true

bfs(start, adj, color, locked):
    queue = [start]
    color[start] = 1 if locked[start] == 0 else locked[start]
    
    while queue not empty:
        node = queue.dequeue()
        required_neighbor_color = 3 - color[node]  // Toggle between 1 and 2
        
        for neighbor in adj[node]:
            if color[neighbor] == -1:
                color[neighbor] = required_neighbor_color
                queue.enqueue(neighbor)
            elif color[neighbor] != required_neighbor_color:
                return false  // Conflict detected
    
    return true
```

### Time Complexity

- **O(V + E)** - Optimal for graph traversal

### Space Complexity

- **O(V)** - For color array and queue

![Algorithm Visualization](../images/GRP-004/algorithm-visualization.png)
![Algorithm Steps](../images/GRP-004/algorithm-steps.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public boolean canColorBipartite(int n, List<List<Integer>> adj, int[] locked) {
        int[] color = new int[n];
        Arrays.fill(color, -1);
        
        // Pre-color locked nodes
        for (int i = 0; i < n; i++) {
            if (locked[i] != 0) {
                color[i] = locked[i];
            }
        }
        
        // Check each component
        for (int i = 0; i < n; i++) {
            if (color[i] == -1) {
                if (!bfs(i, adj, color, locked)) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    private boolean bfs(int start, List<List<Integer>> adj, int[] color, int[] locked) {
        Queue<Integer> queue = new LinkedList<>();
        queue.offer(start);
        color[start] = (locked[start] == 0) ? 1 : locked[start];
        
        while (!queue.isEmpty()) {
            int node = queue.poll();
            int requiredNeighborColor = 3 - color[node]; // Toggle between 1 and 2
            
            for (int neighbor : adj.get(node)) {
                if (color[neighbor] == -1) {
                    // Uncolored neighbor
                    if (locked[neighbor] != 0 && locked[neighbor] != requiredNeighborColor) {
                        return false; // Locked to wrong color
                    }
                    color[neighbor] = requiredNeighborColor;
                    queue.offer(neighbor);
                } else if (color[neighbor] != requiredNeighborColor) {
                    return false; // Color conflict
                }
            }
        }
        
        return true;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int m = sc.nextInt();
        
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        
        for (int i = 0; i < m; i++) {
            int u = sc.nextInt();
            int v = sc.nextInt();
            adj.get(u).add(v);
            adj.get(v).add(u);
        }
        
        int[] locked = new int[n];
        for (int i = 0; i < n; i++) {
            locked[i] = sc.nextInt();
        }
        
        Solution solution = new Solution();
        System.out.println(solution.canColorBipartite(n, adj, locked));
        sc.close();
    }
}
```

### Python

```python
from collections import deque
from typing import List

def can_color_bipartite(n: int, adj: List[List[int]], locked: List[int]) -> bool:
    """
    Check if graph can be 2-colored respecting locked nodes.
    
    Args:
        n: Number of nodes
        adj: Adjacency list
        locked: Locked colors (0=unlocked, 1=group A, 2=group B)
    
    Returns:
        True if valid bipartite coloring exists
    """
    color = [-1] * n
    
    # Pre-color locked nodes
    for i in range(n):
        if locked[i] != 0:
            color[i] = locked[i]
    
    def bfs(start):
        queue = deque([start])
        if color[start] == -1:
            color[start] = 1 if locked[start] == 0 else locked[start]
        
        while queue:
            node = queue.popleft()
            required_neighbor_color = 3 - color[node]  # Toggle between 1 and 2
            
            for neighbor in adj[node]:
                if color[neighbor] == -1:
                    # Check if locked to wrong color
                    if locked[neighbor] != 0 and locked[neighbor] != required_neighbor_color:
                        return False
                    color[neighbor] = required_neighbor_color
                    queue.append(neighbor)
                elif color[neighbor] != required_neighbor_color:
                    return False  # Color conflict
        
        return True
    
    # Check each component
    for i in range(n):
        if color[i] == -1:
            if not bfs(i):
                return False
    
    return True

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Sort adjacency lists for deterministic output
    for i in range(n):
        adj[i].sort()
    
    # Problem: Count nodes in larger bipartite partition
    # Use BFS to color graph, return size of larger partition
    color = [-1] * n
    count = [0, 0]  # count[0] = color 0, count[1] = color 1
    
    from collections import deque
    for start in range(n):
        if color[start] == -1:
            queue = deque([start])
            color[start] = 0
            count[0] += 1
            
            while queue:
                u = queue.popleft()
                for v in adj[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]
                        count[color[v]] += 1
                        queue.append(v)
    
    print(max(count))

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
private:
    bool bfs(int start, vector<vector<int>>& adj, vector<int>& color, vector<int>& locked) {
        queue<int> q;
        q.push(start);
        if (color[start] == -1) {
            color[start] = (locked[start] == 0) ? 1 : locked[start];
        }
        
        while (!q.empty()) {
            int node = q.front();
            q.pop();
            int requiredNeighborColor = 3 - color[node];
            
            for (int neighbor : adj[node]) {
                if (color[neighbor] == -1) {
                    if (locked[neighbor] != 0 && locked[neighbor] != requiredNeighborColor) {
                        return false;
                    }
                    color[neighbor] = requiredNeighborColor;
                    q.push(neighbor);
                } else if (color[neighbor] != requiredNeighborColor) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
public:
    bool canColorBipartite(int n, vector<vector<int>>& adj, vector<int>& locked) {
        vector<int> color(n, -1);
        
        // Pre-color locked nodes
        for (int i = 0; i < n; i++) {
            if (locked[i] != 0) {
                color[i] = locked[i];
            }
        }
        
        // Check each component
        for (int i = 0; i < n; i++) {
            if (color[i] == -1) {
                if (!bfs(i, adj, color, locked)) {
                    return false;
                }
            }
        }
        
        return true;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> adj(n);
    
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    
    vector<int> locked(n);
    for (int i = 0; i < n; i++) {
        cin >> locked[i];
    }
    
    Solution solution;
    cout << (solution.canColorBipartite(n, adj, locked) ? "true" : "false") << "\n";
    
    return 0;
}
```

### JavaScript

```javascript
const readline = require("readline");

class Solution {
  canColorBipartite(n, adj, locked) {
    const color = new Array(n).fill(-1);
    
    // Pre-color locked nodes
    for (let i = 0; i < n; i++) {
      if (locked[i] !== 0) {
        color[i] = locked[i];
      }
    }
    
    const bfs = (start) => {
      const queue = [start];
      if (color[start] === -1) {
        color[start] = locked[start] === 0 ? 1 : locked[start];
      }
      
      while (queue.length > 0) {
        const node = queue.shift();
        const requiredNeighborColor = 3 - color[node];
        
        for (const neighbor of adj[node]) {
          if (color[neighbor] === -1) {
            if (locked[neighbor] !== 0 && locked[neighbor] !== requiredNeighborColor) {
              return false;
            }
            color[neighbor] = requiredNeighborColor;
            queue.push(neighbor);
          } else if (color[neighbor] !== requiredNeighborColor) {
            return false;
          }
        }
      }
      
      return true;
    };
    
    // Check each component
    for (let i = 0; i < n; i++) {
      if (color[i] === -1) {
        if (!bfs(i)) {
          return false;
        }
      }
    }
    
    return true;
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

let data = [];
rl.on("line", (line) => data.push(line.trim()));
rl.on("close", () => {
  let ptr = 0;
  const n = parseInt(data[ptr++]);
  const m = parseInt(data[ptr++]);
  
  const adj = Array.from({ length: n }, () => []);
  
  for (let i = 0; i < m; i++) {
    const [u, v] = data[ptr++].split(" ").map(Number);
    adj[u].push(v);
    adj[v].push(u);
  }
  
  const locked = data[ptr++].split(" ").map(Number);
  
  const solution = new Solution();
  console.log(solution.canColorBipartite(n, adj, locked) ? "true" : "false");
});
```

## 🧪 Test Case Walkthrough (Dry Run)

Use the sample:
- n = 4, m = 4
- Edges: (0,1), (1,2), (2,3), (3,0)
- Locked: [1, 0, 0, 2]

Graph forms a cycle: 0-1-2-3-0

Initialize locked colors:
- color = [1, -1, -1, 2]

Start BFS from locked node 0:
- Node 1 must be 2 (opposite of 0)
- Node 2 must be 1 (opposite of 1)
- Node 3 must be 2 (opposite of 2), and it matches the lock ✓

Answer: `true`

![Example Visualization](../images/GRP-004/example-1.png)

## ✅ Proof of Correctness

### Invariant

At any point, all colored nodes satisfy: (1) bipartite property with neighbors, (2) locked constraints.

### Why the approach is correct

**Bipartite checking:** Standard BFS 2-coloring ensures no adjacent nodes have the same color.

**Locked validation:** Before coloring a node, we verify it's not locked to a conflicting color.

**Completeness:** We check all components, ensuring no part of the graph is missed.

## 💡 Interview Extensions (High-Value Add-ons)

- **Extension 1:** Return a valid coloring if one exists, not just true/false
- **Extension 2:** Find the minimum number of locked nodes to change to make bipartite coloring possible
- **Extension 3:** Handle 3-coloring with locked nodes
- **Extension 4:** Count the number of valid colorings respecting locks

### Common Mistakes to Avoid

1. **Ignoring Locked Constraints**

   - ❌ Wrong: Standard bipartite check without validating locked nodes
   - ✅ Correct: Check locked constraints at every coloring step
   - **Impact:** Incorrect results when locks conflict with bipartite property

2. **Wrong Color Toggle Logic**

   - ❌ Wrong: Using `1 - color[node]` for toggling between 1 and 2
   - ✅ Correct: Using `3 - color[node]` to toggle between 1 and 2
   - **Description:** Math error in color calculation

3. **Not Pre-Coloring Locked Nodes**

   - ❌ Wrong: Coloring locked nodes during BFS
   - ✅ Correct: Pre-color all locked nodes before starting BFS
   - **Prevention:** Ensures locked constraints are respected from the start

4. **Forgetting Disconnected Components**

   - ❌ Wrong: Only checking from node 0
   - ✅ Correct: Check all unvisited nodes to handle disconnected components
   - **Description:** Missing components leads to incomplete validation

5. **Incorrect Conflict Detection**

   - ❌ Wrong: Only checking color conflicts, not locked conflicts
   - ✅ Correct: Check both: (1) color[neighbor] matches required, (2) locked[neighbor] allows required color
   - **Description:** Missing one type of conflict gives wrong answer

## Related Concepts

- **Standard Bipartite Checking:** Without locked constraints
- **Graph Coloring:** General k-coloring problem (NP-complete for k≥3)
- **Constraint Satisfaction:** CSP with pre-assigned variables
- **2-SAT:** Boolean satisfiability with 2 literals per clause
- **Matching in Bipartite Graphs:** Maximum matching, Hall's theorem
