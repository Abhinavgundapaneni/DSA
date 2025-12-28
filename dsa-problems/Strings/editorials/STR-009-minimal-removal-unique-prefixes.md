---
id: STR-009
title: Minimal Removal for Unique Prefixes
sidebar_label: STR-009 - Minimal Removal for Unique Prefixes
tags:
- strings
- trie
- greedy
- medium
difficulty: Medium
difficulty_score: 45
problem_id: STR_MINIMAL_REMOVAL_UNIQUE_PREFIXES__1009
display_id: STR-009
slug: minimal-removal-unique-prefixes
topics:
- String Manipulation
- Trie
- Greedy
---
# STR-009: Minimal Removal for Unique Prefixes

## 📋 Problem Summary

**Input**: Integer `L` (prefix length), list of `n` strings  
**Output**: Minimum total character deletions (from ends) to make all length-L prefixes distinct  
**Constraints**: `1 <= n <= 2 × 10^5`, `1 <= L <= 20`, total length ≤ `2 × 10^5`

## 🌍 Real-World Scenario

Database indexing requires unique prefix keys for efficient lookups. When identifiers collide on prefixes, trimming suffixes minimally preserves data while ensuring uniqueness.

## Detailed Explanation

**Operation**: Delete characters from the end of any string

**Goal**: Make all strings have distinct prefixes of length L

**Constraint**: Can only shorten strings, not extend them

**Example**: `L=2`, strings `["abc", "abd", "acc"]`

- Prefixes: "ab", "ab", "ac"
- Collision: First two have "ab"
- Solution: Keep one as "ab...", shorten other to length < 2 or change prefix
- Minimal: Delete 2 from "abd" → "a" (cost 2)
- Result prefixes: "ab", "a", "ac" (all distinct)

## Naive Approach

```
1. Try all combinations of deletions
2. For each combination:
   a. Check if prefixes are distinct
   b. Track minimal cost
```

### Time Complexity: **Exponential**

- Too many deletion combinations

### Space Complexity: **O(n × L)**

- Store strings and prefixes

## Optimal Approach

**Trie-Based Conflict Detection + Greedy Resolution**:

1. Build trie of all length-L prefixes
2. Identify conflicting strings (same prefix at depth L)
3. For each conflict group:
   - Keep longest string (or arbitrary choice)
   - Delete others to length < L

**Algorithm**:

```
1. Build trie with strings as values at nodes
2. Traverse to depth L and collect conflicts
3. For each conflict group at depth L:
   a. Find string with max length (or arbitrary)
   b. For other strings:
      - Calculate deletions: len(s) - (L-1)
      - Add to total cost
4. Return total cost
```

**Greedy Choice**: Keep longest string in each conflict group minimizes deletions

---

## 🧪 Test Case Walkthrough (Dry Run)

### Example: L=2, strings=["abc", "abd", "acc"]

**Step 1: Build Trie to depth L=2**

```
       root
        │
        a
       ╱ ╲
      b   c
     ╱ ╲   │
   abc abd acc
   (c) (d) (c)
```

**Step 2: Identify conflicts at depth 2**

```
At node 'a' → 'b' (depth 2):
  ├─ "abc" (length 3)
  └─ "abd" (length 3)  ← CONFLICT! Same prefix "ab"

At node 'a' → 'c' (depth 2):
  └─ "acc" (length 3)  ← No conflict, unique prefix "ac"
```

**Step 3: Resolve conflicts**

```
Conflict group at "ab": ["abc", "abd"]
  • Keep one: "abc" (arbitrary choice)
  • Delete other to length < L:
    - "abd" must become length < 2
    - Delete to length 1: "a"
    - Deletions needed: len("abd") - (L-1) = 3 - 1 = 2 ✓
```

**Step 4: Final state**

```
Before:                After:
"abc" → prefix "ab"    "abc" → prefix "ab"
"abd" → prefix "ab"    "a"   → (too short, no L-prefix)
"acc" → prefix "ac"    "acc" → prefix "ac"

Prefixes of length L=2: {"ab", "ac"} ← All distinct! ✓
Total deletions: 2
```

---

### Example: L=2, strings=["aa", "aa", "aa", "aa", "aa"]

**Step 1: Build Trie**

```
       root
        │
        a
        │
        a (depth 2)
      ╱ │ │ │ ╲
    aa aa aa aa aa  ← All 5 strings!
```

**Step 2: Massive conflict at "aa"**

```
All 5 strings have prefix "aa" → CONFLICT!
```

**Step 3: Resolution strategy**

```
Conflict group: ["aa", "aa", "aa", "aa", "aa"]
  • Keep 1 string: "aa"
  • Delete other 4 to length < L=2:
    - Each: len("aa") - (L-1) = 2 - 1 = 1
    - Each becomes: "a"
```

**Step 4: Calculate total**

```
Deletions per string: 1 character
Number of strings to shorten: 4
Total deletions: 4 × 1 = 4 ✓
```

**Visual representation:**

```
Before:              After:
[aa] [aa] [aa] [aa] [aa]    [aa] [a] [a] [a] [a]
 ↓    ↓    ↓    ↓    ↓        ↓   ↓   ↓   ↓   ↓
All have prefix "aa"       Only 1 has length≥2
```

---

### Time Complexity

| Phase               | Operations         | Cost         |
| ------------------- | ------------------ | ------------ |
| Build trie          | Insert n strings   | O(n × L)     |
| Traverse conflicts  | Visit trie nodes   | O(n × L)     |
| Calculate deletions | Count per conflict | O(n)         |
| **Total**           |                    | **O(n × L)** |

### Space Complexity

| Component      | Space    | Justification     |
| -------------- | -------- | ----------------- |
| Trie nodes     | O(n × L) | At most n×L nodes |
| Conflict lists | O(n)     | All strings       |
| **Total**      |          | **O(n × L)**      |

## 💻 Implementation

### Python

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.strings = []  # Strings passing through this node

def minimal_removal_unique_prefixes(L: int, strings: list[str]) -> int:
    # Build trie with all strings
    root = TrieNode()

    for s in strings:
        node = root
        for i, c in enumerate(s):
            if i == L:  # Only care about first L characters
                break
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.strings.append(s)

    # Find conflicts at depth L
    total_deletions = 0

    def find_conflicts(node, depth):
        nonlocal total_deletions

        if depth == L:
            # Check if multiple strings at this node (conflict)
            if len(node.strings) > 1:
                # Keep longest, delete others
                node.strings.sort(key=lambda x: -len(x))
                for s in node.strings[1:]:
                    # Delete to length L-1 (so prefix length < L)
                    if len(s) >= L:
                        total_deletions += len(s) - (L - 1)
            return

        for child in node.children.values():
            find_conflicts(child, depth + 1)

    find_conflicts(root, 0)
    return total_deletions

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    L = int(lines[0])
    n = int(lines[1])
    strings = lines[2:2+n]
    result = minimal_removal_unique_prefixes(L, strings)
    print(result)

if __name__ == "__main__":
    main()

```

### Java

```java
class TrieNode {
    Map<Character, TrieNode> children = new HashMap<>();
    List<String> strings = new ArrayList<>();
}

class Solution {
    private int totalDeletions = 0;

    public int minimalRemovalUniquePrefixes(int L, List<String> strings) {
        TrieNode root = new TrieNode();

        // Build trie
        for (String s : strings) {
            TrieNode node = root;
            for (int i = 0; i < Math.min(s.length(), L); i++) {
                char c = s.charAt(i);
                node.children.putIfAbsent(c, new TrieNode());
                node = node.children.get(c);
            }
            node.strings.add(s);
        }

        // Find conflicts
        totalDeletions = 0;
        findConflicts(root, 0, L);
        return totalDeletions;
    }

    private void findConflicts(TrieNode node, int depth, int L) {
        if (depth == L) {
            if (node.strings.size() > 1) {
                // Sort by length descending
                node.strings.sort((a, b) -> Integer.compare(b.length(), a.length()));

                // Delete all except longest
                for (int i = 1; i < node.strings.size(); i++) {
                    String s = node.strings.get(i);
                    if (s.length() >= L) {
                        totalDeletions += s.length() - (L - 1);
                    }
                }
            }
            return;
        }

        for (TrieNode child : node.children.values()) {
            findConflicts(child, depth + 1, L);
        }
    }
}
```

### C++

```cpp
struct TrieNode {
    unordered_map<char, TrieNode*> children;
    vector<string> strings;
};

class Solution {
public:
    int minimalRemovalUniquePrefixes(int L, vector<string>& strings) {
        TrieNode* root = new TrieNode();

        // Build trie
        for (const string& s : strings) {
            TrieNode* node = root;
            for (int i = 0; i < min((int)s.size(), L); i++) {
                char c = s[i];
                if (node->children.find(c) == node->children.end()) {
                    node->children[c] = new TrieNode();
                }
                node = node->children[c];
            }
            node->strings.push_back(s);
        }

        // Find conflicts
        int totalDeletions = 0;
        findConflicts(root, 0, L, totalDeletions);
        return totalDeletions;
    }

private:
    void findConflicts(TrieNode* node, int depth, int L, int& totalDeletions) {
        if (depth == L) {
            if (node->strings.size() > 1) {
                // Sort by length descending
                sort(node->strings.begin(), node->strings.end(),
                     [](const string& a, const string& b) {
                         return a.size() > b.size();
                     });

                // Delete all except longest
                for (int i = 1; i < node->strings.size(); i++) {
                    const string& s = node->strings[i];
                    if ((int)s.size() >= L) {
                        totalDeletions += s.size() - (L - 1);
                    }
                }
            }
            return;
        }

        for (auto& [c, child] : node->children) {
            findConflicts(child, depth + 1, L, totalDeletions);
        }
    }
};
```

### JavaScript

```javascript
class TrieNode {
  constructor() {
    this.children = new Map();
    this.strings = [];
  }
}

function minimalRemovalUniquePrefixes(L, strings) {
  const root = new TrieNode();

  // Build trie
  for (const s of strings) {
    let node = root;
    for (let i = 0; i < Math.min(s.length, L); i++) {
      const c = s[i];
      if (!node.children.has(c)) {
        node.children.set(c, new TrieNode());
      }
      node = node.children.get(c);
    }
    node.strings.push(s);
  }

  // Find conflicts
  let totalDeletions = 0;

  function findConflicts(node, depth) {
    if (depth === L) {
      if (node.strings.length > 1) {
        // Sort by length descending
        node.strings.sort((a, b) => b.length - a.length);

        // Delete all except longest
        for (let i = 1; i < node.strings.length; i++) {
          const s = node.strings[i];
          if (s.length >= L) {
            totalDeletions += s.length - (L - 1);
          }
        }
      }
      return;
    }

    for (const child of node.children.values()) {
      findConflicts(child, depth + 1);
    }
  }

  findConflicts(root, 0);
  return totalDeletions;
}
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input**: `L=2`, strings `["abc", "abd", "acc"]`

**Step 1: Build Trie**

```
Root
 └─ a
     └─ b (depth 2, strings=["abc", "abd"])
     └─ c (depth 2, strings=["acc"])
```

**Step 2: Find Conflicts at Depth L=2**

```
Node "ab" (depth 2):
  strings = ["abc", "abd"]  (conflict!)
  Keep longest: "abc" (length 3)
  Delete from "abd": 3 - (2-1) = 3 - 1 = 2 deletions

Node "ac" (depth 2):
  strings = ["acc"]  (no conflict)
```

**Step 3: Calculate Total**

```
totalDeletions = 2
```

**Output**: `2`

**Verification**:

- "abc" → prefix "ab"
- "abd" → delete 2 chars → "a" → prefix "a" (length < 2)
- "acc" → prefix "ac"
- All distinct: "ab", "a" (length 1 < L), "ac" ✓

## 🧪 Walkthrough: No Conflicts

**Input**: `L=2`, strings `["ab", "cd", "ef"]`

```
Trie:
Root
 └─ a
     └─ b (strings=["ab"])
 └─ c
     └─ d (strings=["cd"])
 └─ e
     └─ f (strings=["ef"])

All nodes at depth 2 have single string
No conflicts → totalDeletions = 0
```

**Output**: `0`

## ⚠️ Common Mistakes to Avoid

1. **Not Using Trie**: Brute-force comparison is O(n² × L)
2. **Wrong Deletion Count**: Use `len(s) - (L-1)`, not `len(s) - L`
3. **Forgetting Short Strings**: Strings with length < L already have unique "prefix"
4. **Greedy Choice**: Keeping longest minimizes deletions
5. **Trie Depth**: Only build to depth L, no need to go deeper

## 💡 Key Takeaways

1. **Trie for Prefix Conflicts**: Natural structure for grouping by prefix
2. **Greedy Strategy**: Keep longest string in each conflict group
3. **Deletion Formula**: `len(s) - (L-1)` to reduce prefix length below L
4. **Efficient Traversal**: Only traverse trie to depth L
5. **Conflict Detection**: Multiple strings at same trie node at depth L


## Constraints

- `1 ≤ n ≤ 2 × 10^5`
- `1 ≤ L ≤ 20`
- Total string length ≤ `2 × 10^5`