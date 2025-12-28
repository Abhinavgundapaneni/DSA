---
title: Campus Course Ordering
slug: campus-course-ordering
difficulty: Medium
difficulty_score: 55
tags:
- Recursion
- Backtracking
- Topological Sort
problem_id: REC_CAMPUS_COURSE_ORDERING__5184
display_id: REC-011
topics:
- Recursion
- Backtracking
- Graphs
---
# Campus Course Ordering - Editorial

## Problem Summary

You are given `n` courses and a list of prerequisites. If course `u` is a prerequisite for `v`, you must take `u` before `v`. You need to find **all possible valid sequences** (topological sorts) of taking all `n` courses.


## Constraints

- `1 <= n <= 8`
- `0 <= m <= 15`
- Course IDs are in `[0, n-1]`
## Real-World Scenario

Imagine **University Degree Planning**. You have a set of core courses. "Intro to CS" must be taken before "Data Structures", and "Calculus I" before "Calculus II". However, "History" and "Art" have no prerequisites relative to each other. You want to see every possible schedule that satisfies the rules so you can choose the one that fits your lifestyle best.

## Problem Exploration

### 1. Topological Sort
This is the classic definition of Topological Sort on a Directed Acyclic Graph (DAG).
-   Nodes: Courses.
-   Edges: Prerequisite `u -> v`.
-   A valid ordering is a linear arrangement of vertices such that for every edge `u -> v`, `u` comes before `v`.

### 2. Kahn's Algorithm (Modified)
Standard Kahn's algorithm finds *one* topological sort using indegrees.
-   Calculate indegree of all nodes.
-   Put all nodes with `indegree == 0` into a queue.
-   While queue not empty:
    -   Pop `u`. Add to result.
    -   Decrease indegree of neighbors. If neighbor becomes 0, add to queue.

To find **all** topological sorts, we can use backtracking with the same logic.
Instead of a queue, at each step of the recursion, we can pick **any** node that currently has `indegree == 0` and has not been visited yet.

### 3. Backtracking Strategy
`backtrack(current_path, current_indegrees)`
-   If `current_path` length is `n`: We found a valid sort. Add to results.
-   Iterate through all nodes `i` from `0` to `n-1`.
-   If `indegree[i] == 0` and `!visited[i]`:
    -   **Choose**: Add `i` to path. Mark visited. Decrease indegree of neighbors.
    -   **Recurse**: `backtrack(...)`
    -   **Unchoose (Backtrack)**: Remove `i`. Unmark visited. Increase indegree of neighbors (restore state).

## Approaches

### Approach 1: Backtracking with Indegree Array
We maintain the dynamic state of indegrees.
-   **Complexity**: `O(N! * (N+M))`. In the worst case (no edges), there are `N!` permutations. With `N <= 8`, `8! = 40,320`, which is small enough.
-   **Output Order**: To ensure lexicographical order of permutations, we should iterate nodes `0` to `n-1` at each step.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public List<List<Integer>> allOrderings(int n, int[][] edges) {
        List<List<Integer>> result = new ArrayList<>();
        int[] indegree = new int[n];
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        
        for (int[] edge : edges) {
            adj.get(edge[0]).add(edge[1]);
            indegree[edge[1]]++;
        }
        
        boolean[] visited = new boolean[n];
        backtrack(n, adj, indegree, visited, new ArrayList<>(), result);
        return result;
    }

    private void backtrack(int n, List<List<Integer>> adj, int[] indegree, boolean[] visited, 
                           List<Integer> path, List<List<Integer>> result) {
        if (path.size() == n) {
            result.add(new ArrayList<>(path));
            return;
        }

        for (int i = 0; i < n; i++) {
            if (!visited[i] && indegree[i] == 0) {
                // Choose i
                visited[i] = true;
                path.add(i);
                for (int neighbor : adj.get(i)) {
                    indegree[neighbor]--;
                }

                backtrack(n, adj, indegree, visited, path, result);

                // Backtrack
                for (int neighbor : adj.get(i)) {
                    indegree[neighbor]++;
                }
                path.remove(path.size() - 1);
                visited[i] = false;
            }
        }
    }
}
```

### Python

```python
from collections import deque

def topological_sort(n, edges):
    """
    Topological sort using Kahn's algorithm (BFS).
    Returns one valid ordering or None if cycle exists.
    """
    adj = [[] for _ in range(n)]
    indegree = [0] * n
    
    for u, v in edges:
        adj[u].append(v)
        indegree[v] += 1
    
    # Start with all nodes that have no prerequisites
    queue = deque([i for i in range(n) if indegree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in adj[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(result) != n:
        return None  # Cycle detected
    
    return result

def main():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u, v))
    
    result = topological_sort(n, edges)
    
    if result is None:
        print("IMPOSSIBLE")
    else:
        print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    vector<vector<int>> allOrderings(int n, const vector<pair<int,int>>& edges) {
        vector<vector<int>> adj(n);
        vector<int> indegree(n, 0);
        for (const auto& edge : edges) {
            adj[edge.first].push_back(edge.second);
            indegree[edge.second]++;
        }

        vector<vector<int>> result;
        vector<int> path;
        vector<bool> visited(n, false);
        
        backtrack(n, adj, indegree, visited, path, result);
        return result;
    }

private:
    void backtrack(int n, const vector<vector<int>>& adj, vector<int>& indegree, 
                   vector<bool>& visited, vector<int>& path, vector<vector<int>>& result) {
        if (path.size() == n) {
            result.push_back(path);
            return;
        }

        for (int i = 0; i < n; i++) {
            if (!visited[i] && indegree[i] == 0) {
                visited[i] = true;
                path.push_back(i);
                for (int neighbor : adj[i]) {
                    indegree[neighbor]--;
                }

                backtrack(n, adj, indegree, visited, path, result);

                for (int neighbor : adj[i]) {
                    indegree[neighbor]++;
                }
                path.pop_back();
                visited[i] = false;
            }
        }
    }
};
```

### JavaScript

```javascript
class Solution {
  allOrderings(n, edges) {
    const adj = Array.from({ length: n }, () => []);
    const indegree = Array(n).fill(0);
    
    for (const [u, v] of edges) {
      adj[u].push(v);
      indegree[v]++;
    }

    const results = [];
    const visited = Array(n).fill(false);

    const backtrack = (path) => {
      if (path.length === n) {
        results.push([...path]);
        return;
      }

      for (let i = 0; i < n; i++) {
        if (!visited[i] && indegree[i] === 0) {
          visited[i] = true;
          path.push(i);
          for (const neighbor of adj[i]) {
            indegree[neighbor]--;
          }

          backtrack(path);

          for (const neighbor of adj[i]) {
            indegree[neighbor]++;
          }
          path.pop();
          visited[i] = false;
        }
      }
    };

    backtrack([]);
    return results;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:** `3 2`, Edges `0->1`, `0->2`

1.  **Indegrees**: `0:0`, `1:1`, `2:1`.
2.  `backtrack([])`:
    -   Available (indegree 0): `0`.
    -   **Pick 0**: Path `[0]`.
        -   Update neighbors: `1` (indegree 1->0), `2` (indegree 1->0).
        -   `backtrack([0])`:
            -   Available: `1`, `2`.
            -   **Pick 1**: Path `[0, 1]`.
                -   `backtrack([0, 1])`:
                    -   Available: `2`.
                    -   **Pick 2**: Path `[0, 1, 2]`.
                        -   Found `[0, 1, 2]`.
            -   **Pick 2**: Path `[0, 2]`.
                -   `backtrack([0, 2])`:
                    -   Available: `1`.
                    -   **Pick 1**: Path `[0, 2, 1]`.
                        -   Found `[0, 2, 1]`.

**Result:**
`0 1 2`
`0 2 1`

## Proof of Correctness

The algorithm explores the state space of all valid topological sorts.
-   **Validity**: At each step, we only pick a node with `indegree == 0`, ensuring all its prerequisites have been satisfied (visited).
-   **Completeness**: We iterate through *all* currently available nodes, branching to find all possible valid sequences.
-   **Termination**: Each step adds a node. Stops at depth `n`.

## Interview Extensions

1.  **Detect Cycle?**
    -   If the recursion finishes but `path.size() < n`, a cycle exists (or simply if at some step `path.size() < n` but no node has `indegree == 0`).
2.  **Count only?**
    -   Use DP with bitmask `dp[mask]` = number of ways to order the subset `mask`. `O(2^n * n)`.

### Common Mistakes

-   **Modifying Indegree**: Forgetting to restore `indegree` values during backtracking.
-   **Visited Array**: Necessary to distinguish between "indegree 0 because processed" and "indegree 0 because available". Or just check if node is in current path.
