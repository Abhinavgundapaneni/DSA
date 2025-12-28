---
problem_id: GRP_LAB_DIRECTED_CYCLE__2647
display_id: GRP-006
slug: lab-directed-cycle-check
title: "Lab Directed Cycle Check"
difficulty: Medium
difficulty_score: 50
topics:
  - Directed Graph
  - Cycle Detection
  - DFS
  - Topological Sort
tags:
  - graph
  - directed-graph
  - cycle-detection
  - dfs
  - topological-sort
  - medium
premium: true
subscription_tier: basic
---

# GRP-006: Lab Directed Cycle Check

## 📋 Problem Summary

Detect if a directed graph contains a cycle using DFS with a recursion stack. Unlike undirected graphs, directed graphs require tracking nodes currently in the DFS path to identify back edges.

## 🌍 Real-World Scenario

**Scenario Title:** Software Build Dependency Validation

Imagine a software build system where packages have dependencies. Package A depending on Package B is represented as a directed edge A→B. Before building, the system must verify there are no circular dependencies - if A depends on B, B depends on C, and C depends on A, the build is impossible.

Detecting cycles in the dependency graph is crucial. A cycle means the build order cannot be determined (no topological sort exists). Modern build tools like Maven, Gradle, and npm all perform cycle detection before attempting to build. Finding cycles early prevents build failures and helps developers fix dependency issues.

For example, if module "auth" depends on "database", "database" depends on "logging", and "logging" depends on "auth", we have a cycle that must be broken by refactoring the code structure.

**Why This Problem Matters:**

- **Build Systems:** Detecting circular dependencies in software projects
- **Task Scheduling:** Validating prerequisite relationships
- **Deadlock Detection:** Finding circular wait conditions in operating systems
- **Course Prerequisites:** Ensuring valid course ordering in academic programs

![Real-World Application](../images/GRP-006/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: Directed Cycle Detection

```
Directed graph with cycle:

    0 → 1 → 2
        ↑   ↓
        +---+

Edges: 0→1, 1→2, 2→1

DFS from 0:
Visit 0 (rec_stack: [0])
  → Visit 1 (rec_stack: [0,1])
    → Visit 2 (rec_stack: [0,1,2])
      → Try to visit 1
        1 is in rec_stack
        → CYCLE DETECTED!

States:
- White: Unvisited
- Gray: In recursion stack (currently exploring)
- Black: Completely processed

Legend:
→ = directed edge
rec_stack = nodes in current DFS path
```

## ✅ Input/Output Clarifications (Read This Before Coding)

- **Directed edges:** Edge u→v only allows traversal from u to v
- **Recursion stack:** Tracks nodes in current DFS path (gray nodes)
- **Back edge:** Edge to a node in recursion stack indicates cycle
- **Cross/Forward edges:** Edges to visited nodes NOT in stack are OK

Common interpretation mistake:

- ❌ **Wrong:** Using parent tracking (works for undirected, not directed)
- ✅ **Correct:** Using recursion stack to track current DFS path

### Core Concept

Maintain three states:
1. **Unvisited (white):** Not yet explored
2. **In recursion stack (gray):** Currently being explored
3. **Completely processed (black):** Finished exploring

A back edge (to a gray node) indicates a cycle.

## Optimal Approach

### Algorithm

```
has_cycle(n, adj):
    visited = [false] * n
    rec_stack = [false] * n
    
    for i in 0 to n-1:
        if not visited[i]:
            if dfs(i, adj, visited, rec_stack):
                return true
    
    return false

dfs(node, adj, visited, rec_stack):
    visited[node] = true
    rec_stack[node] = true  // Mark as gray
    
    for neighbor in adj[node]:
        if not visited[neighbor]:
            if dfs(neighbor, adj, visited, rec_stack):
                return true
        elif rec_stack[neighbor]:
            return true  // Back edge - cycle detected
    
    rec_stack[node] = false  // Mark as black
    return false
```

### Time Complexity

- **O(V + E)** - Visit each vertex once, examine each edge once

### Space Complexity

- **O(V)** - Recursion stack, visited array, rec_stack array

![Algorithm Visualization](../images/GRP-006/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public boolean hasCycle(int n, List<List<Integer>> adj) {
        boolean[] visited = new boolean[n];
        boolean[] recStack = new boolean[n];
        
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                if (dfs(i, adj, visited, recStack)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    private boolean dfs(int node, List<List<Integer>> adj, boolean[] visited, boolean[] recStack) {
        visited[node] = true;
        recStack[node] = true;
        
        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) {
                if (dfs(neighbor, adj, visited, recStack)) {
                    return true;
                }
            } else if (recStack[neighbor]) {
                return true; // Back edge - cycle detected
            }
        }
        
        recStack[node] = false;
        return false;
    }
}
```

### Python

```python
from typing import List

def has_cycle(n: int, adj: List[List[int]]) -> bool:
    visited = [False] * n
    rec_stack = [False] * n
    
    def dfs(node):
        visited[node] = True
        rec_stack[node] = True
        
        for neighbor in adj[node]:
            if not visited[neighbor]:
                if dfs(neighbor):
                    return True
            elif rec_stack[neighbor]:
                return True  # Back edge - cycle detected
        
        rec_stack[node] = False
        return False
    
    for i in range(n):
        if not visited[i]:
            if dfs(i):
                return True
    
    return False

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
    
    # Count back edges in directed graph (cycles)
    visited = [False] * n
    rec_stack = [False] * n
    cycle_count = 0
    
    def dfs(u):
        nonlocal cycle_count
        visited[u] = True
        rec_stack[u] = True
        
        for v in adj[u]:
            if not visited[v]:
                dfs(v)
            elif rec_stack[v]:
                cycle_count += 1
        
        rec_stack[u] = False
    
    for i in range(n):
        if not visited[i]:
            dfs(i)
    
    print(cycle_count)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

class Solution {
private:
    bool dfs(int node, vector<vector<int>>& adj, vector<bool>& visited, vector<bool>& recStack) {
        visited[node] = true;
        recStack[node] = true;
        
        for (int neighbor : adj[node]) {
            if (!visited[neighbor]) {
                if (dfs(neighbor, adj, visited, recStack)) {
                    return true;
                }
            } else if (recStack[neighbor]) {
                return true; // Back edge - cycle detected
            }
        }
        
        recStack[node] = false;
        return false;
    }
    
public:
    bool hasCycle(int n, vector<vector<int>>& adj) {
        vector<bool> visited(n, false);
        vector<bool> recStack(n, false);
        
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                if (dfs(i, adj, visited, recStack)) {
                    return true;
                }
            }
        }
        
        return false;
    }
};
```

### JavaScript

```javascript
class Solution {
  hasCycle(n, adj) {
    const visited = new Array(n).fill(false);
    const recStack = new Array(n).fill(false);
    
    const dfs = (node) => {
      visited[node] = true;
      recStack[node] = true;
      
      for (const neighbor of adj[node]) {
        if (!visited[neighbor]) {
          if (dfs(neighbor)) {
            return true;
          }
        } else if (recStack[neighbor]) {
          return true; // Back edge - cycle detected
        }
      }
      
      recStack[node] = false;
      return false;
    };
    
    for (let i = 0; i < n; i++) {
      if (!visited[i]) {
        if (dfs(i)) {
          return true;
        }
      }
    }
    
    return false;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)

Graph: 0→1, 1→2, 2→1

| Step | Node | Action | Visited | RecStack | Result |
|-----:|:----:|:-------|:--------|:---------|:-------|
| 1 | 0 | Visit | [T,F,F] | [T,F,F] | Explore neighbors |
| 2 | 1 | Visit from 0 | [T,T,F] | [T,T,F] | Explore neighbors |
| 3 | 2 | Visit from 1 | [T,T,T] | [T,T,T] | Explore neighbors |
| 4 | 1 | Check from 2 | [T,T,T] | [T,T,T] | visited[1]=T, recStack[1]=T → **CYCLE!** |

Answer: `true`

![Example Visualization](../images/GRP-006/example-1.png)

## ✅ Proof of Correctness

**Theorem:** A directed graph has a cycle iff DFS finds a back edge (edge to a node in recursion stack).

**Proof:**
- If cycle exists → DFS will eventually traverse the cycle → finds back edge to ancestor in current path
- If back edge exists → edge connects to node in current DFS path → forms cycle

## 💡 Interview Extensions (High-Value Add-ons)

- **Extension 1:** Return the actual cycle path
- **Extension 2:** Use Kahn's algorithm (topological sort) for cycle detection
- **Extension 3:** Find all cycles in the graph
- **Extension 4:** Detect the smallest cycle

### Common Mistakes to Avoid

1. **Using Parent Tracking (Undirected Approach)**
   - ❌ Wrong: Checking `neighbor != parent`
   - ✅ Correct: Checking `recStack[neighbor]`
   - **Impact:** Doesn't work for directed graphs

2. **Not Resetting Recursion Stack**
   - ❌ Wrong: Forgetting `recStack[node] = false` after DFS
   - ✅ Correct: Reset recStack when backtracking
   - **Description:** Causes false positives

3. **Confusing Visited with RecStack**
   - ❌ Wrong: Only using visited array
   - ✅ Correct: Using both visited and recStack
   - **Prevention:** Visited tracks all explored nodes, recStack tracks current path

4. **Checking Only Unvisited Neighbors**
   - ❌ Wrong: `if not visited[neighbor]: check cycle`
   - ✅ Correct: Check both unvisited AND recStack neighbors
   - **Description:** Misses back edges to visited nodes in current path

5. **Wrong Cycle Detection Condition**
   - ❌ Wrong: `if visited[neighbor]: return true`
   - ✅ Correct: `if visited[neighbor] and recStack[neighbor]: return true`
   - **Description:** Not all visited neighbors indicate cycles

## Related Concepts

- **Topological Sort:** Only possible in DAGs (no cycles)
- **Kahn's Algorithm:** Alternative cycle detection via in-degree
- **Strongly Connected Components:** Kosaraju's and Tarjan's algorithms
- **Undirected Cycle Detection:** Uses parent tracking instead
- **2-SAT:** Uses directed graph cycle detection
