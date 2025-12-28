---
problem_id: GRP_COURSE_PLAN_MANDATORY__5183
display_id: GRP-007
slug: course-plan-mandatory-pairs
title: "Course Plan with Mandatory Pairs"
difficulty: Medium
difficulty_score: 55
topics:
  - Topological Sort
  - Directed Acyclic Graph
  - Graph Contraction
tags:
  - graph
  - topological-sort
  - dag
  - scheduling
  - medium
premium: true
subscription_tier: basic
---

# GRP-007: Course Plan with Mandatory Pairs

## 📋 Problem Summary

Produce a topological ordering of courses that respects both prerequisite constraints and mandatory adjacency pairs. This combines standard topological sort with the constraint that certain course pairs must appear adjacent in the final schedule.

## 🌍 Real-World Scenario

**Scenario Title:** University Course Scheduling with Lab Pairs

Imagine scheduling university courses where some courses have prerequisites (must be taken before others) and some courses have mandatory lab components that must be scheduled in consecutive time slots. For example, "Chemistry Theory" and "Chemistry Lab" must be adjacent, and "Physics 1" must come before "Physics 2".

The challenge is to create a valid semester schedule that satisfies both types of constraints. This is common in academic planning where theory-lab pairs, lecture-tutorial pairs, or related courses need to be consecutive for pedagogical or logistical reasons.

**Why This Problem Matters:**

- **Academic Scheduling:** Course timetabling with paired sessions
- **Task Scheduling:** Jobs with setup/cleanup phases that must be adjacent
- **Manufacturing:** Processes with mandatory consecutive steps
- **Project Planning:** Tasks with hard adjacency requirements

![Real-World Application](../images/GRP-007/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: Topological Sort with Pairs

```
Prerequisites: 0→2, 1→2
Mandatory pair: (2,3) must be adjacent

Graph:
    0 ↘
         2 → 3
    1 ↗

Valid orderings:
[0, 1, 2, 3] ✓ (2 and 3 adjacent)
[1, 0, 2, 3] ✓ (2 and 3 adjacent)

Invalid:
[0, 2, 1, 3] ✗ (2 and 3 not adjacent)

Approach: Contract (2,3) into super-node,
run topological sort, then expand.
```

## ✅ Input/Output Clarifications (Read This Before Coding)

- **Prerequisite edges:** Directed edges representing "must come before"
- **Adjacency pairs:** Undirected pairs that must be consecutive in output
- **Valid ordering:** Satisfies all prerequisites AND all adjacency constraints
- **Multiple solutions:** Any valid ordering is acceptable

Common interpretation mistake:

- ❌ **Wrong:** Treating adjacency pairs as prerequisite edges
- ✅ **Correct:** Adjacency means consecutive in final ordering, not dependency

### Core Concept

**Graph Contraction:** Merge each adjacency pair into a single super-node, perform topological sort on the contracted graph, then expand super-nodes back to individual courses maintaining the pair adjacency.

## Optimal Approach

### Algorithm

```
course_schedule(n, prerequisites, pairs):
    # Step 1: Create super-nodes for adjacency pairs
    parent = [i for i in range(n)]  # Union-Find
    
    for (a, b) in pairs:
        union(a, b, parent)
    
    # Step 2: Build contracted graph
    contracted_adj = build_contracted_graph(prerequisites, parent)
    
    # Step 3: Topological sort on contracted graph
    topo_order = topological_sort(contracted_adj)
    
    if topo_order is empty:
        return []  # Cycle detected or impossible
    
    # Step 4: Expand super-nodes
    result = []
    for super_node in topo_order:
        members = get_members(super_node, parent)
        # Order members respecting internal prerequisites
        result.extend(order_members(members, prerequisites))
    
    return result
```

### Time Complexity

- **O(n + m + p)** where n=courses, m=prerequisites, p=pairs
- Union-Find: O(p × α(n))
- Topological sort: O(n + m)

### Space Complexity

- **O(n + m)** for graph and auxiliary structures

![Algorithm Visualization](../images/GRP-007/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    private int[] parent;
    
    public List<Integer> courseSchedule(int n, List<int[]> prerequisites, List<int[]> pairs) {
        parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        
        // Union pairs
        for (int[] pair : pairs) {
            union(pair[0], pair[1]);
        }
        
        // Build contracted graph
        Map<Integer, List<Integer>> contracted = new HashMap<>();
        Map<Integer, Integer> inDegree = new HashMap<>();
        
        for (int i = 0; i < n; i++) {
            int root = find(i);
            contracted.putIfAbsent(root, new ArrayList<>());
            inDegree.putIfAbsent(root, 0);
        }
        
        for (int[] pre : prerequisites) {
            int from = find(pre[0]);
            int to = find(pre[1]);
            if (from != to) {
                contracted.get(from).add(to);
                inDegree.put(to, inDegree.get(to) + 1);
            }
        }
        
        // Topological sort (Kahn's algorithm)
        Queue<Integer> queue = new LinkedList<>();
        for (int node : inDegree.keySet()) {
            if (inDegree.get(node) == 0) {
                queue.offer(node);
            }
        }
        
        List<Integer> topoOrder = new ArrayList<>();
        while (!queue.isEmpty()) {
            int node = queue.poll();
            topoOrder.add(node);
            
            for (int neighbor : contracted.get(node)) {
                inDegree.put(neighbor, inDegree.get(neighbor) - 1);
                if (inDegree.get(neighbor) == 0) {
                    queue.offer(neighbor);
                }
            }
        }
        
        if (topoOrder.size() != contracted.size()) {
            return new ArrayList<>(); // Cycle detected
        }
        
        // Expand super-nodes
        List<Integer> result = new ArrayList<>();
        for (int superNode : topoOrder) {
            for (int i = 0; i < n; i++) {
                if (find(i) == superNode) {
                    result.add(i);
                }
            }
        }
        
        return result;
    }
    
    private int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    private void union(int x, int y) {
        int px = find(x);
        int py = find(y);
        if (px != py) {
            parent[px] = py;
        }
    }
}
```

### Python

```python
from typing import List, Tuple
from collections import defaultdict, deque

def course_schedule(n: int, prerequisites: List[Tuple[int, int]], pairs: List[Tuple[int, int]]) -> List[int]:
    # Union-Find for pairs
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
    
    # Union pairs
    for a, b in pairs:
        union(a, b)
    
    # Build contracted graph
    contracted = defaultdict(list)
    in_degree = defaultdict(int)
    
    roots = set(find(i) for i in range(n))
    for root in roots:
        in_degree[root] = 0
    
    for u, v in prerequisites:
        from_root = find(u)
        to_root = find(v)
        if from_root != to_root:
            contracted[from_root].append(to_root)
            in_degree[to_root] += 1
    
    # Topological sort (Kahn's algorithm)
    queue = deque([node for node in roots if in_degree[node] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in contracted[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(topo_order) != len(roots):
        return []  # Cycle detected
    
    # Expand super-nodes
    result = []
    for super_node in topo_order:
        for i in range(n):
            if find(i) == super_node:
                result.append(i)
    
    return result

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    indegree = [0] * n
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        indegree[v] += 1
    
    # Topological sort using Kahn's algorithm
    from collections import deque
    queue = deque()
    
    for i in range(n):
        if indegree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        u = queue.popleft()
        result.append(u)
        
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    
    if len(result) == n:
        print(len(result))
    else:
        print(0)  # Has cycle

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <unordered_set>
using namespace std;

class Solution {
private:
    vector<int> parent;
    
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    void unionNodes(int x, int y) {
        int px = find(x);
        int py = find(y);
        if (px != py) {
            parent[px] = py;
        }
    }
    
public:
    vector<int> courseSchedule(int n, vector<pair<int,int>>& prerequisites, vector<pair<int,int>>& pairs) {
        parent.resize(n);
        for (int i = 0; i < n; i++) parent[i] = i;
        
        // Union pairs
        for (auto& [a, b] : pairs) {
            unionNodes(a, b);
        }
        
        // Build contracted graph
        unordered_map<int, vector<int>> contracted;
        unordered_map<int, int> inDegree;
        unordered_set<int> roots;
        
        for (int i = 0; i < n; i++) {
            roots.insert(find(i));
        }
        
        for (int root : roots) {
            inDegree[root] = 0;
        }
        
        for (auto& [u, v] : prerequisites) {
            int from = find(u);
            int to = find(v);
            if (from != to) {
                contracted[from].push_back(to);
                inDegree[to]++;
            }
        }
        
        // Topological sort
        queue<int> q;
        for (int root : roots) {
            if (inDegree[root] == 0) {
                q.push(root);
            }
        }
        
        vector<int> topoOrder;
        while (!q.empty()) {
            int node = q.front();
            q.pop();
            topoOrder.push_back(node);
            
            for (int neighbor : contracted[node]) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) {
                    q.push(neighbor);
                }
            }
        }
        
        if (topoOrder.size() != roots.size()) {
            return {}; // Cycle detected
        }
        
        // Expand super-nodes
        vector<int> result;
        for (int superNode : topoOrder) {
            for (int i = 0; i < n; i++) {
                if (find(i) == superNode) {
                    result.push_back(i);
                }
            }
        }
        
        return result;
    }
};
```

### JavaScript

```javascript
class Solution {
  courseSchedule(n, prerequisites, pairs) {
    const parent = Array.from({ length: n }, (_, i) => i);
    
    const find = (x) => {
      if (parent[x] !== x) {
        parent[x] = find(parent[x]);
      }
      return parent[x];
    };
    
    const union = (x, y) => {
      const px = find(x);
      const py = find(y);
      if (px !== py) {
        parent[px] = py;
      }
    };
    
    // Union pairs
    for (const [a, b] of pairs) {
      union(a, b);
    }
    
    // Build contracted graph
    const contracted = new Map();
    const inDegree = new Map();
    const roots = new Set();
    
    for (let i = 0; i < n; i++) {
      roots.add(find(i));
    }
    
    for (const root of roots) {
      contracted.set(root, []);
      inDegree.set(root, 0);
    }
    
    for (const [u, v] of prerequisites) {
      const from = find(u);
      const to = find(v);
      if (from !== to) {
        contracted.get(from).push(to);
        inDegree.set(to, inDegree.get(to) + 1);
      }
    }
    
    // Topological sort
    const queue = [];
    for (const root of roots) {
      if (inDegree.get(root) === 0) {
        queue.push(root);
      }
    }
    
    const topoOrder = [];
    while (queue.length > 0) {
      const node = queue.shift();
      topoOrder.push(node);
      
      for (const neighbor of contracted.get(node)) {
        inDegree.set(neighbor, inDegree.get(neighbor) - 1);
        if (inDegree.get(neighbor) === 0) {
          queue.push(neighbor);
        }
      }
    }
    
    if (topoOrder.length !== roots.size) {
      return []; // Cycle detected
    }
    
    // Expand super-nodes
    const result = [];
    for (const superNode of topoOrder) {
      for (let i = 0; i < n; i++) {
        if (find(i) === superNode) {
          result.push(i);
        }
      }
    }
    
    return result;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)

Input: n=4, prerequisites=[(0,2), (1,2)], pairs=[(2,3)]

1. Union pairs: {2,3} become super-node
2. Contracted graph: 0→{2,3}, 1→{2,3}
3. Topological sort: [0, 1, {2,3}] or [1, 0, {2,3}]
4. Expand: [0, 1, 2, 3] or [1, 0, 2, 3]

Both satisfy: 0 before 2, 1 before 2, and 2 adjacent to 3 ✓

![Example Visualization](../images/GRP-007/example-1.png)

## ✅ Proof of Correctness

**Theorem:** If a valid ordering exists, graph contraction + topological sort finds it.

**Proof:**
- Contraction preserves prerequisite relationships between super-nodes
- Topological sort ensures prerequisite order
- Expansion maintains adjacency within super-nodes

## 💡 Interview Extensions (High-Value Add-ons)

- **Extension 1:** Handle multiple adjacency pairs per course
- **Extension 2:** Minimize total schedule length with time constraints
- **Extension 3:** Find all valid orderings
- **Extension 4:** Handle conflicts (impossible to satisfy all constraints)

### Common Mistakes to Avoid

1. **Treating Pairs as Prerequisites**
   - ❌ Wrong: Adding directed edges for pairs
   - ✅ Correct: Using Union-Find to group pairs
   - **Impact:** Incorrect ordering

2. **Not Checking for Cycles**
   - ❌ Wrong: Assuming topological sort always succeeds
   - ✅ Correct: Validate topo_order.size() == num_super_nodes
   - **Description:** Prerequisites might form a cycle

3. **Incorrect Super-Node Expansion**
   - ❌ Wrong: Random order within super-nodes
   - ✅ Correct: Respect internal prerequisites when expanding
   - **Prevention:** Check prerequisites within super-nodes

4. **Forgetting Self-Loops**
   - ❌ Wrong: Not checking if from_root == to_root
   - ✅ Correct: Skip edges within same super-node
   - **Description:** Contracted edges to same node create issues

5. **Not Handling Disconnected Components**
   - ❌ Wrong: Only processing one component
   - ✅ Correct: Ensure all super-nodes are in topological order
   - **Description:** Missing courses in output

## Related Concepts

- **Standard Topological Sort:** Kahn's algorithm, DFS-based
- **Graph Contraction:** Merging nodes while preserving structure
- **Union-Find (DSU):** Efficient set operations for grouping
- **Constraint Satisfaction:** CSP with ordering constraints
- **Job Scheduling:** Real-world application of topological sort
