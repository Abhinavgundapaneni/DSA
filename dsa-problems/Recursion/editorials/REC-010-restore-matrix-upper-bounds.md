---
title: Restore Matrix With Upper Bounds
slug: restore-matrix-upper-bounds
difficulty: Medium
difficulty_score: 56
tags:
- Recursion
- Backtracking
- Matrix
problem_id: REC_RESTORE_MATRIX_UPPER_BOUNDS__2607
display_id: REC-010
topics:
- Recursion
- Backtracking
- Matrices
---
# Restore Matrix With Upper Bounds - Editorial

## Problem Summary

You need to construct an `R x C` matrix of non-negative integers such that:
1.  The sum of the `i`-th row equals `rowSums[i]`.
2.  The sum of the `j`-th column equals `colSums[j]`.
3.  Each cell `matrix[i][j]` is between `0` and `bounds[i][j]` inclusive.

If multiple solutions exist, any one is acceptable. If none exist, output `NONE`.


## Constraints

- `1 <= r, c <= 6`
- `0 <= rowSum[i], colSum[j] <= 20`
- `0 <= u[i][j] <= 20`
## Real-World Scenario

Imagine **Supply Chain Management**. You have `R` factories and `C` warehouses.
-   Factory `i` produces exactly `rowSums[i]` units.
-   Warehouse `j` demands exactly `colSums[j]` units.
-   The shipping route from Factory `i` to Warehouse `j` has a capacity limit of `bounds[i][j]`.
You need to determine how much to ship on each route to satisfy all supply and demand within capacity limits.

## Problem Exploration

### 1. Constraints
-   `R, C <= 6`: Very small dimensions. Total cells `<= 36`.
-   Sums and bounds `<= 20`: Small values.
-   This suggests backtracking is feasible, but we need to be smart about pruning.

### 2. Recursive Structure
We can fill the matrix cell by cell, say from `(0,0)` to `(R-1, C-1)`.
At cell `(r, c)`, we need to decide a value `v`.
-   **Lower Bound**: `0`.
-   **Upper Bound**: `bounds[r][c]`.
-   **Row Constraint**: `v` cannot exceed the remaining sum needed for row `r`.
-   **Column Constraint**: `v` cannot exceed the remaining sum needed for column `c`.

So, `v` can range from `0` to `min(bounds[r][c], remaining_row_sum[r], remaining_col_sum[c])`.

### 3. Pruning
-   **Lookahead**: After picking `v` for `(r, c)`, is it possible to satisfy the rest?
    -   If we are at the end of a row (column `C-1`), the value is fixed: it *must* be exactly `remaining_row_sum[r]`. If this value is invalid (negative or > bound or > remaining_col_sum), backtrack.
    -   Similarly, if at the end of a column (row `R-1`), value is fixed by column sum.
-   **Feasibility Check**: At any point, if `remaining_row_sum[i]` > sum of bounds of remaining cells in row `i`, it's impossible. (This might be too expensive to check every step, but simple checks help).

## Approaches

### Approach 1: Backtracking with Pruning
We iterate through cells `(0,0) -> (0,1) -> ... -> (0, C-1) -> (1,0) -> ...`.
At each cell `(r, c)`:
1.  Determine valid range for `val`: `[0, min(bounds[r][c], rowSums[r], colSums[c])]`.
2.  Iterate `val` in this range (try largest first? or smallest? Greedy approach works for simple "Restore Matrix" without bounds, but with bounds, we might need specific values. Trying largest first often satisfies sums quicker but might violate future bounds. Let's try descending).
3.  Update `rowSums[r]` and `colSums[c]`.
4.  Recurse to next cell.
5.  Backtrack (restore sums).

**Optimization**:
-   If `c == C-1`: We *must* pick `val = rowSums[r]`. Check if valid. If so, recurse.
-   If `r == R-1`: We *must* pick `val = colSums[c]`. Check if valid. If so, recurse.

### Approach 2: Max Flow (Network Flow)
This problem can be modeled as a Max Flow problem with demands and capacity constraints.
-   Source -> Rows (capacity `rowSum`).
-   Rows -> Cols (capacity `bound`).
-   Cols -> Sink (capacity `colSum`).
-   Check if max flow equals total row sum (and total col sum).
Given the constraints (`N <= 6`), backtracking is easier to implement during an interview than a full Max Flow algorithm (Dinic/Edmonds-Karp).

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public int[][] restoreMatrix(int[] rowSums, int[] colSums, int[][] bounds) {
        int r = rowSums.length;
        int c = colSums.length;
        int[][] matrix = new int[r][c];
        
        if (backtrack(0, 0, rowSums, colSums, bounds, matrix)) {
            return matrix;
        }
        return new int[0][0];
    }

    private boolean backtrack(int i, int j, int[] rowSums, int[] colSums, int[][] bounds, int[][] matrix) {
        int R = rowSums.length;
        int C = colSums.length;

        if (i == R) {
            // Check if all colSums are 0 (should be guaranteed if logic is correct)
            for (int val : colSums) if (val != 0) return false;
            return true;
        }

        int nextI = (j == C - 1) ? i + 1 : i;
        int nextJ = (j == C - 1) ? 0 : j + 1;

        // Determine range for matrix[i][j]
        // Must be <= bounds[i][j]
        // Must be <= rowSums[i]
        // Must be <= colSums[j]
        int maxVal = Math.min(bounds[i][j], Math.min(rowSums[i], colSums[j]));
        
        // Optimization: If last column, value is fixed
        if (j == C - 1) {
            int val = rowSums[i]; // Must use all remaining row sum
            if (val > maxVal || val < 0) return false; // Invalid
            
            matrix[i][j] = val;
            rowSums[i] -= val;
            colSums[j] -= val;
            
            if (backtrack(nextI, nextJ, rowSums, colSums, bounds, matrix)) return true;
            
            rowSums[i] += val;
            colSums[j] += val;
            return false;
        }

        // Try values from maxVal down to 0
        for (int val = maxVal; val >= 0; val--) {
            matrix[i][j] = val;
            rowSums[i] -= val;
            colSums[j] -= val;

            if (backtrack(nextI, nextJ, rowSums, colSums, bounds, matrix)) return true;

            rowSums[i] += val;
            colSums[j] += val;
        }

        return false;
    }
}
```

### Python

```python
def restore_matrix(row_sums, col_sums):
    """
    Restore a matrix given row and column sums.
    Uses greedy approach: for each cell, assign min(remaining_row_sum, remaining_col_sum).
    """
    r = len(row_sums)
    c = len(col_sums)
    
    # Check if solution is possible
    if sum(row_sums) != sum(col_sums):
        return None
    
    # Make copies to avoid modifying inputs
    row_sums = row_sums[:]
    col_sums = col_sums[:]
    
    matrix = [[0] * c for _ in range(r)]
    
    for i in range(r):
        for j in range(c):
            val = min(row_sums[i], col_sums[j])
            matrix[i][j] = val
            row_sums[i] -= val
            col_sums[j] -= val
    
    return matrix

def main():
    r, c = map(int, input().split())
    row_sums = list(map(int, input().split()))
    col_sums = list(map(int, input().split()))
    
    result = restore_matrix(row_sums, col_sums)
    
    if result is None:
        print("IMPOSSIBLE")
    else:
        for row in result:
            print(' '.join(map(str, row)))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <vector>
#include <algorithm>
#include <numeric>

using namespace std;

class Solution {
public:
    vector<vector<int>> restoreMatrix(vector<int> rowSums, vector<int> colSums, const vector<vector<int>>& bounds) {
        int R = rowSums.size();
        int C = colSums.size();
        vector<vector<int>> matrix(R, vector<int>(C));
        
        if (backtrack(0, 0, rowSums, colSums, bounds, matrix)) {
            return matrix;
        }
        return {};
    }

private:
    bool backtrack(int r, int c, vector<int>& rowSums, vector<int>& colSums, const vector<vector<int>>& bounds, vector<vector<int>>& matrix) {
        int R = rowSums.size();
        int C = colSums.size();

        if (r == R) {
            for (int x : colSums) if (x != 0) return false;
            return true;
        }

        int nextR = (c == C - 1) ? r + 1 : r;
        int nextC = (c == C - 1) ? 0 : c + 1;

        if (c == C - 1) {
            int val = rowSums[r];
            if (val >= 0 && val <= bounds[r][c] && val <= colSums[c]) {
                matrix[r][c] = val;
                rowSums[r] -= val;
                colSums[c] -= val;
                if (backtrack(nextR, nextC, rowSums, colSums, bounds, matrix)) return true;
                rowSums[r] += val;
                colSums[c] += val;
            }
            return false;
        }

        int maxVal = min({bounds[r][c], rowSums[r], colSums[c]});

        for (int val = maxVal; val >= 0; val--) {
            matrix[r][c] = val;
            rowSums[r] -= val;
            colSums[c] -= val;
            if (backtrack(nextR, nextC, rowSums, colSums, bounds, matrix)) return true;
            rowSums[r] += val;
            colSums[c] += val;
        }

        return false;
    }
};
```

### JavaScript

```javascript
class Solution {
  restoreMatrix(rowSums, colSums, bounds) {
    const R = rowSums.length;
    const C = colSums.length;
    const matrix = Array.from({ length: R }, () => Array(C).fill(0));

    // Clone sums to avoid mutation if we wanted to reuse input, 
    // but here we can mutate copies passed to recursion or just mutate input if allowed.
    // Let's use copies for safety in recursion logic.
    const rSums = [...rowSums];
    const cSums = [...colSums];

    const backtrack = (r, c) => {
      if (r === R) {
        return cSums.every((x) => x === 0);
      }

      const nextR = c === C - 1 ? r + 1 : r;
      const nextC = c === C - 1 ? 0 : c + 1;

      if (c === C - 1) {
        const val = rSums[r];
        if (val >= 0 && val <= bounds[r][c] && val <= cSums[c]) {
          matrix[r][c] = val;
          rSums[r] -= val;
          cSums[c] -= val;
          if (backtrack(nextR, nextC)) return true;
          rSums[r] += val;
          cSums[c] += val;
        }
        return false;
      }

      const maxVal = Math.min(bounds[r][c], Math.min(rSums[r], cSums[c]));

      for (let val = maxVal; val >= 0; val--) {
        matrix[r][c] = val;
        rSums[r] -= val;
        cSums[c] -= val;
        if (backtrack(nextR, nextC)) return true;
        rSums[r] += val;
        cSums[c] += val;
      }
      return false;
    };

    if (backtrack(0, 0)) return matrix;
    return [];
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
RowSums: `[3, 4]`
ColSums: `[4, 3]`
Bounds:
`2 3`
`3 4`

1.  `backtrack(0, 0)`:
    -   `maxVal = min(2, 3, 4) = 2`.
    -   Try `val = 2`.
    -   `matrix[0][0] = 2`. `rSums[0]=1`, `cSums[0]=2`.
    -   Recurse `backtrack(0, 1)`.
2.  `backtrack(0, 1)` (Last col):
    -   `val = rSums[0] = 1`.
    -   Check: `1 <= bounds[0][1]=3` (OK), `1 <= cSums[1]=3` (OK).
    -   `matrix[0][1] = 1`. `rSums[0]=0`, `cSums[1]=2`.
    -   Recurse `backtrack(1, 0)`.
3.  `backtrack(1, 0)`:
    -   `maxVal = min(3, 4, 2) = 2`. (Note: `cSums[0]` is now 2).
    -   Try `val = 2`.
    -   `matrix[1][0] = 2`. `rSums[1]=2`, `cSums[0]=0`.
    -   Recurse `backtrack(1, 1)`.
4.  `backtrack(1, 1)` (Last col):
    -   `val = rSums[1] = 2`.
    -   Check: `2 <= bounds[1][1]=4` (OK), `2 <= cSums[1]=2` (OK).
    -   `matrix[1][1] = 2`. `rSums[1]=0`, `cSums[1]=0`.
    -   Recurse `backtrack(2, 0)`.
5.  `backtrack(2, 0)`:
    -   `r == R`. Check `cSums`: `[0, 0]`. All zero.
    -   Return `true`.

**Result:**
`2 1`
`2 2`

## Proof of Correctness

The backtracking algorithm fills the matrix cell by cell.
-   **Validity**: At each step, we ensure the chosen value respects the cell's upper bound and does not exceed the remaining required sum for the current row or column.
-   **Completeness**: By iterating from `maxVal` down to `0`, we explore possible assignments. The optimization for the last column ensures we exactly meet the row sum requirement, pruning invalid branches early.
-   **Termination**: The recursion depth is `R x C`, which is small.

## Interview Extensions

1.  **Minimize the maximum value in the matrix?**
    -   Binary search on the answer `K`. For a fixed `K`, check if a valid matrix exists where `bounds[i][j]` is effectively `min(bounds[i][j], K)`.

2.  **Large R, C?**
    -   Use Max Flow. Create a source connected to rows, columns connected to sink. Edges between row `i` and col `j` have capacity `bounds[i][j]`. Check if max flow saturates source edges.

### Common Mistakes

-   **Greedy Failure**: Simply picking `min(rowSum, colSum)` works for unbounded matrices but fails here because it might consume too much capacity needed for other cells.
-   **Bound Checking**: Forgetting to check `val <= bounds[i][j]`.
