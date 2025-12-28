---
title: Robot Route With Turns
slug: robot-route-turns
difficulty: Medium
difficulty_score: 52
tags:
- Recursion
- Backtracking
- Grid
problem_id: REC_ROBOT_ROUTE_TURNS__7405
display_id: REC-005
topics:
- Recursion
- Backtracking
- Grid
---
# Robot Route With Turns - Editorial

## Problem Summary

You need to find a path from the top-left `(0, 0)` to the bottom-right `(r-1, c-1)` of a grid containing obstacles (`1`) and open spaces (`0`). The robot can move in 4 directions. The catch is that the robot can make at most `T` turns. A turn is defined as changing the direction of movement (e.g., moving Right then Down counts as 1 turn).


## Constraints

- `1 <= r, c <= 8`
- `0 <= T <= 6`
- Grid values are `0` or `1`
## Real-World Scenario

Imagine a **Self-Driving Car** navigating a parking lot. Steering is expensive or slow, so the car prefers to drive in straight lines. It wants to reach the exit with minimal steering adjustments (turns).

Another example is **Piping Layout**. When laying pipes, every bend (elbow joint) adds cost and reduces flow pressure. You want to connect the source to the sink with a limited number of bends.

## Problem Exploration

### 1. State Definition
To solve this using recursion/backtracking, we need to track:
-   Current position `(r, c)`.
-   Current number of turns made `k`.
-   The direction we arrived from `last_dir`.

### 2. Transitions
From `(r, c)`, we can move to 4 neighbors.
-   If we move in the *same* direction as `last_dir`, the turn count `k` remains the same.
-   If we move in a *different* direction, the turn count becomes `k + 1`.
-   If `k` exceeds `T`, we prune this branch.

### 3. Visited Array
Standard DFS needs a `visited` array to prevent cycles. However, simply marking `(r, c)` as visited is not enough because we might reach the same cell with fewer turns or a different direction later.
Given the constraints (`R, C <= 8`), simple backtracking with a `visited` set for the current path is sufficient.

## Approaches

### Approach 1: Backtracking (DFS)
We explore paths recursively.
`dfs(r, c, turns, last_dir, path)`
-   **Base Case**: Reached `(R-1, C-1)`. Return `true`.
-   **Pruning**: If `turns > T`, return `false`.
-   **Recursive Step**: Try all 4 directions. Update `turns` accordingly. Mark current cell visited before recursing and unmark after (backtracking).

### Approach 2: BFS (Shortest Path in Weighted Graph)
This problem can be modeled as a shortest path problem on a graph where nodes are `(r, c, dir)` and edge weights are 0 (same dir) or 1 (turn). We want to reach `(R-1, C-1, any_dir)` with distance `<= T`. BFS/Dijkstra is optimal for finding the *minimum* turns, but the problem asks for *any* valid path. DFS is easier to implement for path reconstruction.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    private int rows, cols;
    private int[][] directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}}; // U, D, L, R

    public List<int[]> findPath(int[][] grid, int T) {
        rows = grid.length;
        cols = grid[0].length;
        boolean[][] visited = new boolean[rows][cols];
        List<int[]> path = new ArrayList<>();
        
        path.add(new int[]{0, 0});
        visited[0][0] = true;
        
        // Start DFS. Initial direction is -1 (none)
        if (dfs(0, 0, -1, 0, T, grid, visited, path)) {
            return path;
        }
        
        return new ArrayList<>();
    }

    private boolean dfs(int r, int c, int lastDir, int turns, int maxTurns, 
                       int[][] grid, boolean[][] visited, List<int[]> path) {
        if (r == rows - 1 && c == cols - 1) {
            return true;
        }

        for (int i = 0; i < 4; i++) {
            int nr = r + directions[i][0];
            int nc = c + directions[i][1];

            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !visited[nr][nc] && grid[nr][nc] == 0) {
                int newTurns = turns;
                if (lastDir != -1 && i != lastDir) {
                    newTurns++;
                }

                if (newTurns <= maxTurns) {
                    visited[nr][nc] = true;
                    path.add(new int[]{nr, nc});
                    if (dfs(nr, nc, i, newTurns, maxTurns, grid, visited, path)) {
                        return true;
                    }
                    path.remove(path.size() - 1);
                    visited[nr][nc] = false;
                }
            }
        }
        return false;
    }
}
```

### Python

```python
def count_paths_with_turns(r, c, max_turns):
    """
    Count paths from (0,0) to (r-1,c-1) with at most max_turns turns.
    A turn occurs when changing direction (R to D or D to R).
    """
    memo = {}
    
    def dp(row, col, direction, turns):
        # Base case: reached destination (check this FIRST)
        if row == r - 1 and col == c - 1:
            return 1
        
        # Pruning: out of bounds or too many turns
        if row >= r or col >= c or turns > max_turns:
            return 0
        
        key = (row, col, direction, turns)
        if key in memo:
            return memo[key]
        
        result = 0
        
        # Move right: turn occurs if previous direction was Down
        new_turns = turns + (1 if direction == 'D' else 0)
        result += dp(row, col + 1, 'R', new_turns)
        
        # Move down: turn occurs if previous direction was Right
        new_turns = turns + (1 if direction == 'R' else 0)
        result += dp(row + 1, col, 'D', new_turns)
        
        memo[key] = result
        return result
    
    return dp(0, 0, '', 0)

def main():
    parts = input().split()
    r, c, t = int(parts[0]), int(parts[1]), int(parts[2])
    print(count_paths_with_turns(r, c, t))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <utility>

using namespace std;

class Solution {
    int rows, cols;
    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, -1, 1};
    vector<pair<int, int>> path;
    vector<vector<bool>> visited;

public:
    vector<pair<int, int>> findPath(const vector<vector<int>>& grid, int T) {
        rows = grid.size();
        cols = grid[0].size();
        visited.assign(rows, vector<bool>(cols, false));
        path.clear();
        
        path.push_back({0, 0});
        visited[0][0] = true;
        
        if (dfs(0, 0, -1, 0, T, grid)) {
            return path;
        }
        return {};
    }

    bool dfs(int r, int c, int lastDir, int turns, int maxTurns, const vector<vector<int>>& grid) {
        if (r == rows - 1 && c == cols - 1) return true;

        for (int i = 0; i < 4; i++) {
            int nr = r + dr[i];
            int nc = c + dc[i];

            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !visited[nr][nc] && grid[nr][nc] == 0) {
                int newTurns = turns;
                if (lastDir != -1 && i != lastDir) newTurns++;

                if (newTurns <= maxTurns) {
                    visited[nr][nc] = true;
                    path.push_back({nr, nc});
                    if (dfs(nr, nc, i, newTurns, maxTurns, grid)) return true;
                    path.pop_back();
                    visited[nr][nc] = false;
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
  findPath(grid, T) {
    const rows = grid.length;
    const cols = grid[0].length;
    const visited = Array.from({ length: rows }, () => Array(cols).fill(false));
    const path = [[0, 0]];
    visited[0][0] = true;
    
    const dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]; // U, D, L, R

    const dfs = (r, c, lastDir, turns) => {
      if (r === rows - 1 && c === cols - 1) return true;

      for (let i = 0; i < 4; i++) {
        const [dr, dc] = dirs[i];
        const nr = r + dr;
        const nc = c + dc;

        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !visited[nr][nc] && grid[nr][nc] === 0) {
          let newTurns = turns;
          if (lastDir !== -1 && i !== lastDir) newTurns++;

          if (newTurns <= T) {
            visited[nr][nc] = true;
            path.push([nr, nc]);
            if (dfs(nr, nc, i, newTurns)) return true;
            path.pop();
            visited[nr][nc] = false;
          }
        }
      }
      return false;
    };

    if (dfs(0, 0, -1, 0)) return path;
    return [];
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
`3 3 2`
`0 0 0`
`1 1 0`
`0 0 0`

1.  Start `(0,0)`, turns=0.
2.  Move Right to `(0,1)`. Dir=Right. Turns=0.
3.  Move Right to `(0,2)`. Dir=Right. Turns=0.
4.  Move Down to `(1,2)`. Dir=Down. Turns=0 -> 1 (Right to Down).
5.  Move Down to `(2,2)`. Dir=Down. Turns=1.
6.  Reached `(2,2)`. Return path.

**Path:** `(0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2)`

## Proof of Correctness

The algorithm explores all valid paths using DFS.
-   **Validity**: It checks grid boundaries, obstacles, and the visited array to ensure the path is valid and simple (no loops).
-   **Turn Constraint**: It explicitly tracks turns and prunes branches where `turns > T`.
-   **Completeness**: Since it backtracks, it explores alternate routes if one gets stuck or exceeds turns. With small constraints (`8 x 8`), this exhaustive search is feasible.

## Interview Extensions

1.  **Find the path with MINIMUM turns?**
    -   Use BFS (0-1 BFS or Dijkstra). State is `(r, c, dir)`. Edge weight is 0 if same dir, 1 if different.

2.  **What if T is large?**
    -   The constraint becomes irrelevant, and it reduces to standard pathfinding (DFS/BFS).

3.  **What if we can move diagonally?**
    -   Add 4 more directions to the `dirs` array. Logic remains the same.

### Common Mistakes

-   **Initial Direction**: The first move does *not* count as a turn. Initialize `lastDir` to -1 or handle the first step separately.
-   **Backtracking**: Forgetting to unmark `visited` (set to false) after returning from recursion prevents finding other valid paths.
-   **Turn Logic**: A turn happens only when `i != lastDir`. Moving straight keeps turns same.

## Related Concepts

-   **Backtracking**: Core concept.
-   **Grid Traversal**: Standard DFS/BFS on grids.
-   **State Space Search**: Including 'direction' and 'turns' in the state.
