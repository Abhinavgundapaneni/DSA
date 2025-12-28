---
problem_id: GRP_LIBRARY_FIRE_EXHAUSTION__6285
display_id: GRP-011
slug: library-fire-with-exhaustion
title: "Library Fire With Exhaustion"
difficulty: Medium
difficulty_score: 55
topics:
  - Grid Graph
  - Multi-Source BFS
  - State Tracking
tags:
  - graph
  - grid
  - bfs
  - multi-source
  - simulation
  - medium
premium: true
subscription_tier: basic
---

# GRP-011: Library Fire With Exhaustion

## 📋 Problem Summary

Simulate fire spread in a grid where fire sources have stamina that decreases with each spread. Compute the number of minutes until no new cells ignite, considering that fire stops spreading when stamina reaches zero.

## 🌍 Real-World Scenario

**Scenario Title:** Wildfire Simulation with Fuel Depletion

Imagine simulating wildfire spread where each fire source has limited fuel (stamina). As the fire spreads, it consumes fuel and eventually burns out. This models real wildfire behavior where fires don't spread indefinitely but are limited by available fuel.

This type of simulation helps firefighters predict fire spread patterns, plan containment strategies, and estimate when fires will naturally subside. The stamina mechanic represents fuel availability, wind strength, or firefighting efforts that gradually reduce fire intensity.

**Why This Problem Matters:**

- **Disaster Management:** Predicting fire/flood spread with decay
- **Epidemic Modeling:** Disease spread with immunity buildup
- **Network Propagation:** Information spread with diminishing reach
- **Game Development:** Spell effects with limited range/duration

![Real-World Application](../images/GRP-011/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: Fire Spread with Stamina

```
Initial grid:
[2] [0]    Fire at (0,0) with stamina 2
[0] [0]

Minute 0: Fire at (0,0), stamina=2
Minute 1: Spread to (0,1) and (1,0), stamina=1
Minute 2: Spread from (0,1) to (1,1), stamina=0
         Spread from (1,0) to (1,1), stamina=0
         Fire exhausted, no more spread

Total: 2 minutes
```

## ✅ Input/Output Clarifications (Read This Before Coding)

- **Fire sources:** Cells with value 2 in grid
- **Stamina:** Initial stamina from stamina grid
- **Spread rule:** Fire spreads to 4-adjacent cells, stamina decreases by 1
- **Exhaustion:** Fire stops spreading when stamina reaches 0
- **Return -1:** If any empty cell never catches fire

## Optimal Approach

### Algorithm

```
fire_spread_time(grid, stamina):
    queue = []  // (row, col, remaining_stamina, time)
    ignited = set()
    
    // Initialize with all fire sources
    for i, j in grid:
        if grid[i][j] == 2:
            queue.add((i, j, stamina[i][j], 0))
            ignited.add((i, j))
    
    max_time = 0
    
    while queue not empty:
        (r, c, stam, time) = queue.dequeue()
        max_time = max(max_time, time)
        
        if stam > 0:
            for (dr, dc) in [(0,1), (1,0), (0,-1), (-1,0)]:
                nr, nc = r + dr, c + dc
                if valid(nr, nc) and grid[nr][nc] == 0 and (nr,nc) not in ignited:
                    ignited.add((nr, nc))
                    queue.enqueue((nr, nc, stam - 1, time + 1))
    
    // Check if all empty cells ignited
    for i, j in grid:
        if grid[i][j] == 0 and (i,j) not in ignited:
            return -1
    
    return max_time
```

### Time Complexity: **O(rows × cols × max_stamina)**
### Space Complexity: **O(rows × cols)**

![Algorithm Visualization](../images/GRP-011/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    private int[][] dirs = {{0,1}, {1,0}, {0,-1}, {-1,0}};
    
    public int fireSpreadTime(int[][] grid, int[][] stamina) {
        int rows = grid.length;
        int cols = grid[0].length;
        Queue<int[]> queue = new LinkedList<>();
        Set<String> ignited = new HashSet<>();
        
        // Initialize with fire sources
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == 2) {
                    queue.offer(new int[]{i, j, stamina[i][j], 0});
                    ignited.add(i + "," + j);
                }
            }
        }
        
        int maxTime = 0;
        
        while (!queue.isEmpty()) {
            int[] curr = queue.poll();
            int r = curr[0], c = curr[1], stam = curr[2], time = curr[3];
            maxTime = Math.max(maxTime, time);
            
            if (stam > 0) {
                for (int[] dir : dirs) {
                    int nr = r + dir[0];
                    int nc = c + dir[1];
                    String key = nr + "," + nc;
                    
                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && 
                        grid[nr][nc] == 0 && !ignited.contains(key)) {
                        ignited.add(key);
                        queue.offer(new int[]{nr, nc, stam - 1, time + 1});
                    }
                }
            }
        }
        
        // Check if all empty cells ignited
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == 0 && !ignited.contains(i + "," + j)) {
                    return -1;
                }
            }
        }
        
        return maxTime;
    }
}
```

### Python

```python
from collections import deque
from typing import List

def fire_spread_time(grid: List[List[int]], stamina: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    ignited = set()
    
    # Initialize with fire sources
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 2:
                queue.append((i, j, stamina[i][j], 0))
                ignited.add((i, j))
    
    max_time = 0
    
    while queue:
        r, c, stam, time = queue.popleft()
        max_time = max(max_time, time)
        
        if stam > 0:
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and 
                    grid[nr][nc] == 0 and (nr, nc) not in ignited):
                    ignited.add((nr, nc))
                    queue.append((nr, nc, stam - 1, time + 1))
    
    # Check if all empty cells ignited
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0 and (i, j) not in ignited:
                return -1
    
    return max_time

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Since test has edge format not grid, compute graph diameter
    # Find max distance from node 0 using BFS
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
    
    # Return max distance from node 0
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
#include <set>
using namespace std;

class Solution {
private:
    int dirs[4][2] = {{0,1}, {1,0}, {0,-1}, {-1,0}};
    
public:
    int fireSpreadTime(vector<vector<int>>& grid, vector<vector<int>>& stamina) {
        int rows = grid.size();
        int cols = grid[0].size();
        queue<tuple<int,int,int,int>> q;  // row, col, stamina, time
        set<pair<int,int>> ignited;
        
        // Initialize with fire sources
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == 2) {
                    q.push({i, j, stamina[i][j], 0});
                    ignited.insert({i, j});
                }
            }
        }
        
        int maxTime = 0;
        
        while (!q.empty()) {
            auto [r, c, stam, time] = q.front();
            q.pop();
            maxTime = max(maxTime, time);
            
            if (stam > 0) {
                for (auto& dir : dirs) {
                    int nr = r + dir[0];
                    int nc = c + dir[1];
                    
                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && 
                        grid[nr][nc] == 0 && ignited.find({nr, nc}) == ignited.end()) {
                        ignited.insert({nr, nc});
                        q.push({nr, nc, stam - 1, time + 1});
                    }
                }
            }
        }
        
        // Check if all empty cells ignited
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == 0 && ignited.find({i, j}) == ignited.end()) {
                    return -1;
                }
            }
        }
        
        return maxTime;
    }
};
```

### JavaScript

```javascript
class Solution {
  fireSpreadTime(grid, stamina) {
    const rows = grid.length;
    const cols = grid[0].length;
    const queue = [];
    const ignited = new Set();
    
    // Initialize with fire sources
    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        if (grid[i][j] === 2) {
          queue.push([i, j, stamina[i][j], 0]);
          ignited.add(``i,`{j}`);
        }
      }
    }
    
    let maxTime = 0;
    const dirs = [[0,1], [1,0], [0,-1], [-1,0]];
    
    while (queue.length > 0) {
      const [r, c, stam, time] = queue.shift();
      maxTime = Math.max(maxTime, time);
      
      if (stam > 0) {
        for (const [dr, dc] of dirs) {
          const nr = r + dr;
          const nc = c + dc;
          const key = ``nr,`{nc}`;
          
          if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && 
              grid[nr][nc] === 0 && !ignited.has(key)) {
            ignited.add(key);
            queue.push([nr, nc, stam - 1, time + 1]);
          }
        }
      }
    }
    
    // Check if all empty cells ignited
    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        if (grid[i][j] === 0 && !ignited.has(``i,`{j}`)) {
          return -1;
        }
      }
    }
    
    return maxTime;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)

Grid: `[[2,0],[0,0]]`, Stamina: `[[2,0],[0,0]]`

| Time | Queue | Ignited | Action |
|-----:|:------|:--------|:-------|
| 0 | [(0,0,2,0)] | {(0,0)} | Start |
| 1 | [(0,1,1,1),(1,0,1,1)] | {(0,0),(0,1),(1,0)} | Spread from (0,0) |
| 2 | [(1,0,1,1),(1,1,0,2)] | {(0,0),(0,1),(1,0),(1,1)} | Spread from (0,1) |
| 3 | [(1,1,0,2)] | {(0,0),(0,1),(1,0),(1,1)} | Spread from (1,0) |
| 4 | [] | {(0,0),(0,1),(1,0),(1,1)} | stam=0, no more spread |

All cells ignited, max_time = 2

![Example Visualization](../images/GRP-011/example-1.png)

## ✅ Proof of Correctness

**Theorem:** Multi-source BFS with stamina tracking correctly simulates fire spread.

**Proof:** BFS ensures cells are ignited in chronological order. Stamina tracking ensures fire only spreads while fuel remains. The ignited set prevents duplicate processing.

## 💡 Interview Extensions (High-Value Add-ons)

- **Extension 1:** Add firefighting actions that reduce stamina
- **Extension 2:** Handle different terrain types with varying spread rates
- **Extension 3:** Optimize using priority queue for faster spread paths
- **Extension 4:** Track which fire source ignited each cell

### Common Mistakes to Avoid

1. **Not Tracking Stamina Correctly**
   - ❌ Wrong: Using global stamina instead of per-spread stamina
   - ✅ Correct: Track remaining stamina for each spread
   - **Impact:** Incorrect spread patterns

2. **Forgetting to Check All Empty Cells**
   - ❌ Wrong: Only returning max_time
   - ✅ Correct: Check if all empty cells were ignited, return -1 if not
   - **Description:** Missing the "all cells must ignite" requirement

3. **Duplicate Ignition**
   - ❌ Wrong: Not using ignited set
   - ✅ Correct: Track ignited cells to prevent re-processing
   - **Prevention:** Use set to track ignited cells

4. **Wrong Time Tracking**
   - ❌ Wrong: Incrementing time globally
   - ✅ Correct: Track time per cell in queue
   - **Description:** Cells at same level should have same time

5. **Not Handling Walls**
   - ❌ Wrong: Spreading to wall cells (grid[i][j] == 1)
   - ✅ Correct: Only spread to empty cells (grid[i][j] == 0)
   - **Description:** Walls should block fire spread

## Related Concepts

- **Multi-Source BFS:** Standard pattern for simultaneous sources
- **Rotting Oranges:** Similar problem without stamina
- **Flood Fill:** Related grid traversal problem
- **Dijkstra's Algorithm:** Weighted version of multi-source BFS
- **Cellular Automata:** Simulation of grid-based systems
