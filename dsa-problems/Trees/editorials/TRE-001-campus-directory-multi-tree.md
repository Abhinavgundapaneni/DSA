---
problem_id: TRE_CAMPUS_DIRECTORY_MULTI_TREE__4813
display_id: TRE-001
slug: campus-directory-multi-tree
title: "Campus Directory Multi-Tree Comparison"
difficulty: Easy
difficulty_score: 28
topics:
  - Trees
  - Traversal
  - Comparison
tags:
  - trees
  - traversal
  - comparison
  - easy
premium: true
subscription_tier: basic
---

# TRE-001: Campus Directory Multi-Tree Comparison

## 📋 Problem Summary

You are given two binary trees. For each tree, you need to generate its **preorder**, **inorder**, and **postorder** traversals. Additionally, you must determine if the two trees are **structurally identical** (having the exact same shape, regardless of node values) and identify which traversal sequences are exactly the same between the two trees.

## 🌍 Real-World Scenario

**Scenario Title:** Organizational Chart Merger

Imagine two companies are merging, and their HR departments need to compare their organizational structures. Each employee is a node in a tree.
1.  **Traversals:** Listing employees in different orders (e.g., by rank, by department) helps in generating different types of reports.
2.  **Structural Identity:** HR wants to know if the *hierarchy* of roles is the same in both companies (e.g., does every Manager have exactly two Team Leads?), even if the people (values) filling those roles are different.
3.  **Matching Traversals:** If the list of employee IDs matches exactly in a specific order, it might indicate that one department was copied from another or that there's a data duplication issue.

![Real-World Application](../images/TRE-001/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: Concept Visualization

**Tree 1:**
```
    1
   / \
  2   3
```
Traversals:
- Pre: 1 2 3
- In: 2 1 3
- Post: 2 3 1

**Tree 2:**
```
    1
   / \
  3   2
```
Traversals:
- Pre: 1 3 2
- In: 3 1 2
- Post: 3 2 1

**Comparison:**
- **Structure:** Both have a root with left and right children. **Identical**.
- **Traversals:** None match.

### Algorithm Steps

1.  **Traversals:**
    *   **Preorder:** Visit Root -> Left -> Right.
    *   **Inorder:** Visit Left -> Root -> Right.
    *   **Postorder:** Visit Left -> Right -> Root.
    *   Store these sequences for both trees.
2.  **Structural Identity:**
    *   Traverse both trees simultaneously.
    *   At each step, check:
        *   If both nodes are null: Match.
        *   If one is null and the other isn't: Mismatch.
        *   If both exist: Recursively check left children AND right children.
    *   Note: We do **not** compare node values for structural identity.
3.  **Matching Traversals:**
    *   Compare the lists generated in step 1.
    *   If `pre1 == pre2`, add "preorder".
    *   If `in1 == in2`, add "inorder".
    *   If `post1 == post2`, add "postorder".

## ✅ Input/Output Clarifications (Read This Before Coding)

-   **Input Format:** Trees are given as an array of nodes. Node `0` is always the root. Children are indices into this array. `-1` means no child.
-   **Empty Tree:** If `n=0`, the tree is empty. Traversals are empty lists. Structural identity with another empty tree is `true`.
-   **Output:** Print lists space-separated. Structural identity is `true`/`false`. Matches are space-separated names or `NONE`.

## Naive Approach

### Intuition

The problem asks for standard traversals and a comparison. Since we have to visit every node to generate traversals, we can't do better than linear time. The "naive" approach is simply the direct implementation of the requirements.

### Algorithm

1.  Implement recursive functions for `preorder`, `inorder`, `postorder`.
2.  Implement a recursive function `isStructurallySame(node1, node2)`.
3.  Run these on the input trees and compare the results.

### Time Complexity

-   **O(N1 + N2)**: We visit every node a constant number of times.

### Space Complexity

-   **O(H1 + H2)**: Recursion stack depth, where H is the height of the tree. In worst case (skewed tree), H=N.

## Optimal Approach

The naive approach is already optimal in terms of time complexity because we must process every node. We can optimize space slightly by using iterative traversals, but recursion is cleaner and standard for this problem.

### Key Insight

For structural identity, ensure you check the *existence* of children, not their values.
`if (node1.left == null && node2.left != null)` -> Different structure.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    static class Node {
        int val;
        int left = -1;
        int right = -1;
    }

    public List<List<Integer>> traverseAll(int n, int[][] nodes) {
        List<List<Integer>> results = new ArrayList<>();
        if (n == 0) {
            results.add(new ArrayList<>());
            results.add(new ArrayList<>());
            results.add(new ArrayList<>());
            return results;
        }

        Node[] tree = new Node[n];
        for (int i = 0; i < n; i++) {
            tree[i] = new Node();
            tree[i].val = nodes[i][0];
            tree[i].left = nodes[i][1];
            tree[i].right = nodes[i][2];
        }

        List<Integer> pre = new ArrayList<>();
        List<Integer> in = new ArrayList<>();
        List<Integer> post = new ArrayList<>();

        preorder(tree, 0, pre);
        inorder(tree, 0, in);
        postorder(tree, 0, post);

        results.add(pre);
        results.add(in);
        results.add(post);
        return results;
    }

    private void preorder(Node[] tree, int u, List<Integer> list) {
        if (u == -1) return;
        list.add(tree[u].val);
        preorder(tree, tree[u].left, list);
        preorder(tree, tree[u].right, list);
    }

    private void inorder(Node[] tree, int u, List<Integer> list) {
        if (u == -1) return;
        inorder(tree, tree[u].left, list);
        list.add(tree[u].val);
        inorder(tree, tree[u].right, list);
    }

    private void postorder(Node[] tree, int u, List<Integer> list) {
        if (u == -1) return;
        postorder(tree, tree[u].left, list);
        postorder(tree, tree[u].right, list);
        list.add(tree[u].val);
    }

    public boolean structuralIdentical(int n1, int[][] t1, int n2, int[][] t2) {
        if (n1 == 0 && n2 == 0) return true;
        if (n1 == 0 || n2 == 0) return false;
        return checkStructure(t1, 0, t2, 0);
    }

    private boolean checkStructure(int[][] t1, int u1, int[][] t2, int u2) {
        if (u1 == -1 && u2 == -1) return true;
        if (u1 == -1 || u2 == -1) return false;

        // Check left child existence
        boolean l1 = t1[u1][1] != -1;
        boolean l2 = t2[u2][1] != -1;
        if (l1 != l2) return false;

        // Check right child existence
        boolean r1 = t1[u1][2] != -1;
        boolean r2 = t2[u2][2] != -1;
        if (r1 != r2) return false;

        return checkStructure(t1, t1[u1][1], t2, t2[u2][1]) &&
               checkStructure(t1, t1[u1][2], t2, t2[u2][2]);
    }

    public List<String> matchingTraversals(List<List<Integer>> t1, List<List<Integer>> t2) {
        List<String> matches = new ArrayList<>();
        if (t1.get(0).equals(t2.get(0))) matches.add("preorder");
        if (t1.get(1).equals(t2.get(1))) matches.add("inorder");
        if (t1.get(2).equals(t2.get(2))) matches.add("postorder");
        return matches;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int n1 = sc.nextInt();
        int[][] t1 = new int[n1][3];
        for (int i = 0; i < n1; i++) {
            t1[i][0] = sc.nextInt();
            t1[i][1] = sc.nextInt();
            t1[i][2] = sc.nextInt();
        }
        int n2 = sc.nextInt();
        int[][] t2 = new int[n2][3];
        for (int i = 0; i < n2; i++) {
            t2[i][0] = sc.nextInt();
            t2[i][1] = sc.nextInt();
            t2[i][2] = sc.nextInt();
        }

        Solution solution = new Solution();
        List<List<Integer>> trav1 = solution.traverseAll(n1, t1);
        List<List<Integer>> trav2 = solution.traverseAll(n2, t2);
        boolean same = solution.structuralIdentical(n1, t1, n2, t2);
        List<String> matches = solution.matchingTraversals(trav1, trav2);

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 3; i++) {
            sb.append(join(trav1.get(i))).append('\n');
        }
        for (int i = 0; i < 3; i++) {
            sb.append(join(trav2.get(i))).append('\n');
        }
        sb.append(same ? "true" : "false").append('\n');
        if (matches.isEmpty()) {
            sb.append("NONE");
        } else {
            sb.append(String.join(" ", matches));
        }
        System.out.print(sb.toString());
        sc.close();
    }

    private static String join(List<Integer> list) {
        if (list.isEmpty()) return "";
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < list.size(); i++) {
            sb.append(list.get(i));
            if (i + 1 < list.size()) sb.append(' ');
        }
        return sb.toString();
    }
}
```

### Python

```python
import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(200000)

def traverse_all(n, nodes):
    if n == 0:
        return [[], [], []]
    
    pre_order = []
    in_order = []
    post_order = []
    
    def dfs(u):
        if u == -1:
            return
        val, left, right = nodes[u]
        
        pre_order.append(val)
        dfs(left)
        in_order.append(val)
        dfs(right)
        post_order.append(val)
        
    dfs(0)
    return [pre_order, in_order, post_order]

def structural_identical(n1, t1, n2, t2):
    # Different number of nodes means not identical
    if n1 != n2:
        return False
    if n1 == 0 and n2 == 0:
        return True
    if n1 == 0 or n2 == 0:
        return False
        
    def check(u1, u2):
        if u1 == -1 and u2 == -1:
            return True
        if u1 == -1 or u2 == -1:
            return False
            
        # Check existence of children
        l1 = t1[u1][1]
        r1 = t1[u1][2]
        l2 = t2[u2][1]
        r2 = t2[u2][2]
        
        # Structure check: if one has child and other doesn't -> False
        if (l1 != -1) != (l2 != -1): return False
        if (r1 != -1) != (r2 != -1): return False
        
        return check(l1, l2) and check(r1, r2)
        
    return check(0, 0)

def matching_traversals(n1, n2, t1, t2):
    matches = []
    # Only compare traversals if both trees are non-empty
    if n1 > 0 and n2 > 0:
        if t1[0] == t2[0]: matches.append("preorder")
        if t1[1] == t2[1]: matches.append("inorder")
        if t1[2] == t2[2]: matches.append("postorder")
    return matches

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    idx = 0
    
    if idx < len(data):
        n1 = int(data[idx]); idx += 1
        t1 = []
        for _ in range(n1):
            v = int(data[idx]); l = int(data[idx + 1]); r = int(data[idx + 2])
            t1.append((v, l, r))
            idx += 3
    else:
        n1 = 0
        t1 = []

    if idx < len(data):
        n2 = int(data[idx]); idx += 1
        t2 = []
        for _ in range(n2):
            v = int(data[idx]); l = int(data[idx + 1]); r = int(data[idx + 2])
            t2.append((v, l, r))
            idx += 3
    else:
        n2 = 0
        t2 = []

    trav1 = traverse_all(n1, t1)
    trav2 = traverse_all(n2, t2)
    same = structural_identical(n1, t1, n2, t2)
    matches = matching_traversals(n1, n2, trav1, trav2)

    out = []
    for i in range(3):
        out.append(" ".join(str(x) for x in trav1[i]))
    for i in range(3):
        out.append(" ".join(str(x) for x in trav2[i]))
    out.append("true" if same else "false")
    out.append("NONE" if not matches else " ".join(matches))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <array>
#include <algorithm>

using namespace std;

class Solution {
    void dfs(int u, const vector<array<int, 3>>& nodes, 
             vector<int>& pre, vector<int>& in, vector<int>& post) {
        if (u == -1) return;
        
        pre.push_back(nodes[u][0]);
        dfs(nodes[u][1], nodes, pre, in, post);
        in.push_back(nodes[u][0]);
        dfs(nodes[u][2], nodes, pre, in, post);
        post.push_back(nodes[u][0]);
    }

    bool checkStruct(int u1, const vector<array<int, 3>>& t1,
                     int u2, const vector<array<int, 3>>& t2) {
        if (u1 == -1 && u2 == -1) return true;
        if (u1 == -1 || u2 == -1) return false;
        
        // Check children existence
        bool l1 = t1[u1][1] != -1;
        bool l2 = t2[u2][1] != -1;
        if (l1 != l2) return false;
        
        bool r1 = t1[u1][2] != -1;
        bool r2 = t2[u2][2] != -1;
        if (r1 != r2) return false;
        
        return checkStruct(t1[u1][1], t1, t2[u2][1], t2) &&
               checkStruct(t1[u1][2], t1, t2[u2][2], t2);
    }

public:
    vector<vector<int>> traverseAll(int n, const vector<array<int, 3>>& nodes) {
        vector<vector<int>> res(3);
        if (n == 0) return res;
        dfs(0, nodes, res[0], res[1], res[2]);
        return res;
    }

    bool structuralIdentical(int n1, const vector<array<int, 3>>& t1,
                             int n2, const vector<array<int, 3>>& t2) {
        if (n1 == 0 && n2 == 0) return true;
        if (n1 == 0 || n2 == 0) return false;
        return checkStruct(0, t1, 0, t2);
    }

    vector<string> matchingTraversals(const vector<vector<int>>& t1,
                                      const vector<vector<int>>& t2) {
        vector<string> matches;
        if (t1[0] == t2[0]) matches.push_back("preorder");
        if (t1[1] == t2[1]) matches.push_back("inorder");
        if (t1[2] == t2[2]) matches.push_back("postorder");
        return matches;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n1;
    if (!(cin >> n1)) return 0;
    vector<array<int, 3>> t1(n1);
    for (int i = 0; i < n1; i++) {
        cin >> t1[i][0] >> t1[i][1] >> t1[i][2];
    }
    int n2;
    cin >> n2;
    vector<array<int, 3>> t2(n2);
    for (int i = 0; i < n2; i++) {
        cin >> t2[i][0] >> t2[i][1] >> t2[i][2];
    }

    Solution solution;
    vector<vector<int>> trav1 = solution.traverseAll(n1, t1);
    vector<vector<int>> trav2 = solution.traverseAll(n2, t2);
    bool same = solution.structuralIdentical(n1, t1, n2, t2);
    vector<string> matches = solution.matchingTraversals(trav1, trav2);

    auto printList = [](const vector<int>& v) {
        for (int i = 0; i < (int)v.size(); i++) {
            if (i) cout << ' ';
            cout << v[i];
        }
        cout << "\n";
    };

    for (int i = 0; i < 3; i++) printList(trav1[i]);
    for (int i = 0; i < 3; i++) printList(trav2[i]);
    cout << (same ? "true" : "false") << "\n";
    if (matches.empty()) {
        cout << "NONE";
    } else {
        for (int i = 0; i < (int)matches.size(); i++) {
            if (i) cout << ' ';
            cout << matches[i];
        }
    }
    return 0;
}
```

### JavaScript

```javascript
const readline = require("readline");

class Solution {
  traverseAll(n, nodes) {
    if (n === 0) return [[], [], []];
    
    const pre = [];
    const inOrder = [];
    const post = [];
    
    const dfs = (u) => {
      if (u === -1) return;
      const [val, left, right] = nodes[u];
      
      pre.push(val);
      dfs(left);
      inOrder.push(val);
      dfs(right);
      post.push(val);
    };
    
    dfs(0);
    return [pre, inOrder, post];
  }

  structuralIdentical(n1, t1, n2, t2) {
    if (n1 === 0 && n2 === 0) return true;
    if (n1 === 0 || n2 === 0) return false;
    
    const check = (u1, u2) => {
      if (u1 === -1 && u2 === -1) return true;
      if (u1 === -1 || u2 === -1) return false;
      
      const l1 = t1[u1][1] !== -1;
      const l2 = t2[u2][1] !== -1;
      if (l1 !== l2) return false;
      
      const r1 = t1[u1][2] !== -1;
      const r2 = t2[u2][2] !== -1;
      if (r1 !== r2) return false;
      
      return check(t1[u1][1], t2[u2][1]) && check(t1[u1][2], t2[u2][2]);
    };
    
    return check(0, 0);
  }

  matchingTraversals(t1, t2) {
    const matches = [];
    
    const eq = (a, b) => {
      if (a.length !== b.length) return false;
      for (let i = 0; i < a.length; i++) {
        if (a[i] !== b[i]) return false;
      }
      return true;
    };
    
    if (eq(t1[0], t2[0])) matches.push("preorder");
    if (eq(t1[1], t2[1])) matches.push("inorder");
    if (eq(t1[2], t2[2])) matches.push("postorder");
    
    return matches;
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

let data = [];
rl.on("line", (line) => {
  const parts = line.trim().split(/\s+/);
  for (const part of parts) {
    if (part) data.push(part);
  }
});

rl.on("close", () => {
  if (data.length === 0) return;
  let idx = 0;
  
  let n1 = 0, t1 = [];
  if (idx < data.length) {
      n1 = parseInt(data[idx++], 10);
      for (let i = 0; i < n1; i++) {
        const v = parseInt(data[idx++], 10);
        const l = parseInt(data[idx++], 10);
        const r = parseInt(data[idx++], 10);
        t1.push([v, l, r]);
      }
  }

  let n2 = 0, t2 = [];
  if (idx < data.length) {
      n2 = parseInt(data[idx++], 10);
      for (let i = 0; i < n2; i++) {
        const v = parseInt(data[idx++], 10);
        const l = parseInt(data[idx++], 10);
        const r = parseInt(data[idx++], 10);
        t2.push([v, l, r]);
      }
  }

  const solution = new Solution();
  const trav1 = solution.traverseAll(n1, t1);
  const trav2 = solution.traverseAll(n2, t2);
  const same = solution.structuralIdentical(n1, t1, n2, t2);
  const matches = solution.matchingTraversals(trav1, trav2);

  const out = [];
  for (let i = 0; i < 3; i++) out.push(trav1[i].join(" "));
  for (let i = 0; i < 3; i++) out.push(trav2[i].join(" "));
  out.push(same ? "true" : "false");
  out.push(matches.length === 0 ? "NONE" : matches.join(" "));
  console.log(out.join("\n"));
});
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input:**
```
3
2 1 2
1 -1 -1
3 -1 -1
3
1 -1 1
2 -1 2
3 -1 -1
```

**Tree 1:**
- Node 0: val 2, left 1, right 2
- Node 1: val 1, leaf
- Node 2: val 3, leaf
- Structure: Root(2) -> Left(1), Right(3)

**Tree 2:**
- Node 0: val 1, left -1, right 1
- Node 1: val 2, left -1, right 2
- Node 2: val 3, leaf
- Structure: Root(1) -> Right(2) -> Right(3) (Skewed right)

**Traversals T1:**
- Pre: 2 1 3
- In: 1 2 3
- Post: 1 3 2

**Traversals T2:**
- Pre: 1 2 3
- In: 1 2 3
- Post: 3 2 1

**Comparison:**
- **Structure:** T1 has left child, T2 does not. `structural_identity = false`.
- **Matches:**
  - Pre: `2 1 3` vs `1 2 3` (No)
  - In: `1 2 3` vs `1 2 3` (Yes)
  - Post: `1 3 2` vs `3 2 1` (No)
  - Result: `inorder`

**Output:**
```
2 1 3
1 2 3
1 3 2
1 2 3
1 2 3
3 2 1
false
inorder
```

## ✅ Proof of Correctness

### Correctness of Traversals
The recursive definitions (e.g., Preorder = Root, Left, Right) are standard and directly implemented. Since the input guarantees valid trees (no cycles, valid indices), the recursion will terminate and visit every node exactly once.

### Correctness of Structural Check
The function `checkStructure` returns true if and only if:
1.  Both current nodes are null (base case match).
2.  Both current nodes exist AND their left children have matching existence AND their right children have matching existence AND their subtrees recursively match.
This covers all conditions for structural identity.

## 💡 Interview Extensions (High-Value Add-ons)

-   **Extension 1: Symmetric Tree**
    -   Check if a tree is a mirror of itself. (Compare `left` of T1 with `right` of T1).
-   **Extension 2: Subtree Check**
    -   Check if T2 is a subtree of T1. (Requires matching structure and values starting from some node in T1).
-   **Extension 3: Serialize/Deserialize**
    -   How to store a tree in a file so it can be reconstructed? (Preorder + Inorder, or Preorder with null markers).

### Common Mistakes to Avoid

1.  **Comparing Values for Structure:**
    -   ❌ `if (t1[u].val != t2[u].val) return false;` inside `structuralIdentical`.
    -   ✅ Structural identity only cares about shape, not values.
2.  **Null Pointer Exceptions:**
    -   ❌ Accessing `t1[u]` when `u == -1`.
    -   ✅ Always check `u == -1` base case.
3.  **Empty Tree Handling:**
    -   ❌ Forgetting `n=0` case.
    -   ✅ Handle `n=0` explicitly or ensure recursion handles it gracefully.

## Related Concepts

-   **Graph Isomorphism:** A more general version of structural identity.
-   **Tree Serialization:** Converting tree to string.
