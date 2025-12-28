---
title: Campus Seating KenKen Mini
slug: campus-seating-kenken-mini
difficulty: Medium
difficulty_score: 59
tags:
- Recursion
- Backtracking
- Constraint Satisfaction
problem_id: REC_CAMPUS_SEATING_KENKEN_MINI__1579
display_id: REC-015
topics:
- Recursion
- Backtracking
- Constraint Satisfaction
---
# Campus Seating KenKen Mini - Editorial

## Problem Summary

You need to fill a `4 x 4` grid with digits `1` to `4` such that:
1.  Each row contains unique digits.
2.  Each column contains unique digits.
3.  The grid is partitioned into "cages". Each cage has a target value and an operator (`+`, `-`, `*`, `/`, `=`). The numbers in the cage must satisfy the operation to produce the target.


## Constraints

- Grid size is fixed at 4x4
- `1 <= c <= 16`
- All cage cells are within the grid
## Real-World Scenario

This is literally the logic puzzle **KenKen** (or Calcudoku). It combines the Latin Square property of Sudoku with arithmetic constraints. Imagine assigning 4 different tasks to 4 people across 4 days, where certain groups of tasks must sum up to a specific workload value.

## Problem Exploration

### 1. Latin Square Constraints
-   Standard backtracking: Fill cell `(0,0)` to `(3,3)`.
-   At each cell, try digits `1..4`.
-   Check `row_used[r][d]` and `col_used[c][d]`.

### 2. Cage Constraints
-   A cage is a set of cells.
-   **Validation**: We can only validate a cage fully when *all* its cells are filled.
-   **Pruning**: If a cage is partially filled, can we prune?
    -   For `+` and `*`: Yes. If current sum/product already exceeds target, prune.
    -   For `-` and `/`: Harder to prune early because order matters (e.g., `target=1`, `op=-`. If we have `5`, we might add `4` later. But digits are small `1..4`, so bounds checking is possible).
    -   Given grid size `4 x 4`, we can just check the cage constraint *after* filling the last cell of that cage.

### 3. Cage Operations
-   `+`: Sum of all cells = target.
-   `*`: Product of all cells = target.
-   `-`: Difference of two cells = target. (Cage size always 2). `|a - b| = target`.
-   `/`: Quotient of two cells = target. (Cage size always 2). `a / b = target` or `b / a = target`.
-   `=`: Value of single cell = target. (Cage size always 1).

## Approaches

### Approach 1: Cell-by-Cell Backtracking
We iterate cells `(0,0)` to `(3,3)`.
At `(r, c)`:
1.  Try `v` in `1..4`.
2.  Check Row/Col uniqueness.
3.  Check Cage validity:
    -   Identify which cage `(r, c)` belongs to.
    -   If `(r, c)` is the *last* empty cell in that cage, validate the cage fully.
    -   If valid, recurse.

To implement this efficiently:
-   Precompute a map `cell -> cage_index`.
-   Track `cage_filled_count[cage_index]`.
-   When `cage_filled_count == cage_size`, check math.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    private int[][] grid;
    private int[][] cageMap; // cell (r*4+c) -> cage index
    private List<int[]> cagesList;
    
    public int[][] solveKenKen(List<int[]> cages) {
        grid = new int[4][4];
        cageMap = new int[4][4];
        cagesList = cages;
        
        // Map each cell to its cage index
        for (int i = 0; i < cages.size(); i++) {
            int[] data = cages.get(i);
            int len = data[2];
            for (int j = 0; j < len; j++) {
                int r = data[3 + 2 * j];
                int c = data[4 + 2 * j];
                cageMap[r][c] = i;
            }
        }
        
        if (backtrack(0, 0)) {
            return grid;
        }
        return new int[0][0];
    }

    private boolean backtrack(int r, int c) {
        if (r == 4) return true;
        
        int nextR = (c == 3) ? r + 1 : r;
        int nextC = (c == 3) ? 0 : c + 1;
        
        for (int v = 1; v <= 4; v++) {
            if (isValid(r, c, v)) {
                grid[r][c] = v;
                // Check cage constraint if this is the last cell in the cage
                if (checkCage(r, c)) {
                    if (backtrack(nextR, nextC)) return true;
                }
                grid[r][c] = 0;
            }
        }
        return false;
    }

    private boolean isValid(int r, int c, int v) {
        // Check if value v exists in row r
        for (int j = 0; j < 4; j++) if (grid[r][j] == v) return false;
        // Check if value v exists in column c
        for (int i = 0; i < 4; i++) if (grid[i][c] == v) return false;
        return true;
    }

    private boolean checkCage(int r, int c) {
        int cageIdx = cageMap[r][c];
        int[] data = cagesList.get(cageIdx);
        int target = data[0];
        char op = (char) data[1];
        int len = data[2];
        
        List<Integer> values = new ArrayList<>();
        boolean full = true;
        
        for (int j = 0; j < len; j++) {
            int rr = data[3 + 2 * j];
            int cc = data[4 + 2 * j];
            if (grid[rr][cc] == 0) {
                full = false;
                break;
            }
            values.add(grid[rr][cc]);
        }
        
        if (!full) return true; // Not full yet, assume valid (or implement partial checks)

        // Full cage check
        if (op == '+') {
            int sum = 0;
            for (int x : values) sum += x;
            return sum == target;
        } else if (op == '*') {
            int prod = 1;
            for (int x : values) prod *= x;
            return prod == target;
        } else if (op == '-') {
            // len is 2
            return Math.abs(values.get(0) - values.get(1)) == target;
        } else if (op == '/') {
            // len is 2
            int a = values.get(0), b = values.get(1);
            return (a % b == 0 && a / b == target) || (b % a == 0 && b / a == target);
        } else if (op == '=') {
            return values.get(0) == target;
        }
        return false;
    }
}
```

### Python

```python
def solve_latin_square(n, grid):
    """
    Solve a Latin square puzzle - fill n×n grid with 1 to n such that 
    each row and column contains each number exactly once.
    
    For the standard empty grid (all 0s), use the cyclic construction:
    grid[i][j] = (i + j) % n + 1
    """
    # Check if grid is completely empty
    is_empty = all(grid[i][j] == 0 for i in range(n) for j in range(n))
    
    if is_empty:
        # Use cyclic construction for standard Latin square
        return [[(i + j) % n + 1 for j in range(n)] for i in range(n)]
    
    # Otherwise use backtracking for partially filled grids
    def is_valid(row, col, num):
        # Check row
        for j in range(n):
            if grid[row][j] == num:
                return False
        # Check column
        for i in range(n):
            if grid[i][col] == num:
                return False
        return True
    
    def solve(row, col):
        if row == n:
            return True
        
        next_row, next_col = (row, col + 1) if col < n - 1 else (row + 1, 0)
        
        if grid[row][col] != 0:
            return solve(next_row, next_col)
        
        for num in range(1, n + 1):
            if is_valid(row, col, num):
                grid[row][col] = num
                if solve(next_row, next_col):
                    return True
                grid[row][col] = 0
        
        return False
    
    if solve(0, 0):
        return grid
    return None

def main():
    n = int(input())
    grid = []
    for _ in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
    
    result = solve_latin_square(n, grid)
    
    if result:
        for row in result:
            print(' '.join(map(str, row)))
    else:
        print("IMPOSSIBLE")

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;

class Solution {
    int grid[4][4];
    struct Cage {
        int target;
        char op;
        vector<pair<int,int>> cells;
    };
    vector<Cage> cageList;
    int cageMap[4][4];

public:
    vector<vector<int>> solveKenKen(const vector<vector<int>>& cages) {
        // Parse cages
        cageList.clear();
        for (int i = 0; i < cages.size(); i++) {
            Cage c;
            c.target = cages[i][0];
            c.op = (char)cages[i][1];
            int len = cages[i][2];
            for (int j = 0; j < len; j++) {
                int r = cages[i][3 + 2 * j];
                int col = cages[i][4 + 2 * j];
                c.cells.push_back({r, col});
                cageMap[r][col] = i;
            }
            cageList.push_back(c);
        }

        for(int i=0; i<4; i++) fill(grid[i], grid[i]+4, 0);

        if (backtrack(0, 0)) {
            vector<vector<int>> res(4, vector<int>(4));
            for(int i=0; i<4; i++)
                for(int j=0; j<4; j++) res[i][j] = grid[i][j];
            return res;
        }
        return {};
    }

    bool backtrack(int r, int c) {
        if (r == 4) return true;

        int nextR = (c == 3) ? r + 1 : r;
        int nextC = (c == 3) ? 0 : c + 1;

        for (int v = 1; v <= 4; v++) {
            if (isValid(r, c, v)) {
                grid[r][c] = v;
                if (checkCage(r, c)) {
                    if (backtrack(nextR, nextC)) return true;
                }
                grid[r][c] = 0;
            }
        }
        return false;
    }

    bool isValid(int r, int c, int v) {
        for (int j = 0; j < 4; j++) if (grid[r][j] == v) return false;
        for (int i = 0; i < 4; i++) if (grid[i][c] == v) return false;
        return true;
    }

    bool checkCage(int r, int c) {
        int idx = cageMap[r][c];
        const Cage& cage = cageList[idx];
        
        vector<int> vals;
        for (auto& p : cage.cells) {
            if (grid[p.first][p.second] == 0) return true; // Not full
            vals.push_back(grid[p.first][p.second]);
        }

        if (cage.op == '+') {
            int sum = 0;
            for (int x : vals) sum += x;
            return sum == cage.target;
        } else if (cage.op == '*') {
            int prod = 1;
            for (int x : vals) prod *= x;
            return prod == cage.target;
        } else if (cage.op == '-') {
            return abs(vals[0] - vals[1]) == cage.target;
        } else if (cage.op == '/') {
            int a = vals[0], b = vals[1];
            return (a % b == 0 && a / b == cage.target) || (b % a == 0 && b / a == cage.target);
        } else if (cage.op == '=') {
            return vals[0] == cage.target;
        }
        return false;
    }
};
```

### JavaScript

```javascript
class Solution {
  solveKenKen(cages) {
    const grid = Array.from({ length: 4 }, () => Array(4).fill(0));
    const cageMap = Array.from({ length: 4 }, () => Array(4).fill(null));
    
    // Process cages
    const processedCages = cages.map((data, idx) => {
      const target = data[0];
      const op = String.fromCharCode(data[1]);
      const len = data[2];
      const coords = [];
      for (let j = 0; j < len; j++) {
        const r = data[3 + 2 * j];
        const c = data[4 + 2 * j];
        coords.push([r, c]);
        cageMap[r][c] = idx;
      }
      return { target, op, coords };
    });

    const isValid = (r, c, v) => {
      for (let j = 0; j < 4; j++) if (grid[r][j] === v) return false;
      for (let i = 0; i < 4; i++) if (grid[i][c] === v) return false;
      return true;
    };

    const checkCage = (r, c) => {
      const cageIdx = cageMap[r][c];
      const { target, op, coords } = processedCages[cageIdx];
      
      const values = [];
      for (const [rr, cc] of coords) {
        if (grid[rr][cc] === 0) return true; // Not full
        values.push(grid[rr][cc]);
      }

      if (op === '+') {
        return values.reduce((a, b) => a + b, 0) === target;
      } else if (op === '*') {
        return values.reduce((a, b) => a * b, 1) === target;
      } else if (op === '-') {
        return Math.abs(values[0] - values[1]) === target;
      } else if (op === '/') {
        const [a, b] = values;
        return (a % b === 0 && a / b === target) || (b % a === 0 && b / a === target);
      } else if (op === '=') {
        return values[0] === target;
      }
      return false;
    };

    const backtrack = (r, c) => {
      if (r === 4) return true;

      const nextR = c === 3 ? r + 1 : r;
      const nextC = c === 3 ? 0 : c + 1;

      for (let v = 1; v <= 4; v++) {
        if (isValid(r, c, v)) {
          grid[r][c] = v;
          if (checkCage(r, c)) {
            if (backtrack(nextR, nextC)) return true;
          }
          grid[r][c] = 0;
        }
      }
      return false;
    };

    if (backtrack(0, 0)) return grid;
    return [];
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:** 16 cages, all `=`.
1.  `1 = 1 0 0`: `grid[0][0]` must be 1.
2.  `2 = 1 0 1`: `grid[0][1]` must be 2.
...
This forces a specific grid.
`backtrack(0,0)`: Try 1. Valid. Recurse.
...
Eventually fills the grid.

## Proof of Correctness

-   **Validity**: Row/Col constraints checked at every placement. Cage constraints checked when cage is full.
-   **Completeness**: Backtracking explores all valid Latin Squares.
-   **Termination**: Grid size fixed `4 x 4`.

## Interview Extensions

1.  **Larger Grid (6x6, 9x9)?**
    -   Same logic, but need better pruning (e.g., partial sum checks for cages).
2.  **Unique Solution?**
    -   Count solutions instead of returning first.

### Common Mistakes

-   **Division**: `a / b` can be `a/b` or `b/a`.
-   **Subtraction**: `|a - b|`.
-   **Cage Check**: Checking too early (when cage not full) might return false incorrectly if logic assumes full cage. Ensure partial cages return `true`.
