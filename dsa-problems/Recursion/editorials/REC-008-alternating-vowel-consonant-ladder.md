---
title: Alternating Vowel-Consonant Ladder
slug: alternating-vowel-consonant-ladder
difficulty: Medium
difficulty_score: 54
tags:
- Recursion
- Backtracking
- Graphs
- BFS
problem_id: REC_ALTERNATING_VOWEL_CONSONANT_LADDER__6073
display_id: REC-008
topics:
- Recursion
- Backtracking
- Graphs
---
# Alternating Vowel-Consonant Ladder - Editorial

## Problem Summary

You need to find all **shortest** transformation sequences (word ladders) from a `start` word to an `end` word.
Rules for transformation:
1.  Change exactly one letter at a time.
2.  Each intermediate word must exist in the given dictionary.
3.  **Constraint**: The starting letter of consecutive words must alternate between a vowel and a consonant. For example, if word `i` starts with a vowel, word `i+1` must start with a consonant, and vice versa.


## Constraints

- `1 <= |word| <= 6`
- `1 <= m <= 3000`
- All words are lowercase and of equal length
## Real-World Scenario

This is a variation of the classic **Word Ladder** game (invented by Lewis Carroll). It models finding the shortest path in a graph where nodes are words and edges represent single-letter modifications. The additional constraint adds a "parity" check to the edges, similar to alternating traffic rules or bipartite matching constraints.

## Problem Exploration

### 1. Vowels and Consonants
-   Vowels: `a, e, i, o, u`.
-   Consonants: All other lowercase English letters.
-   Helper function `isVowel(char c)` is essential.

### 2. Graph Construction
-   Nodes: Words in the dictionary (plus start word).
-   Edges: Two words are connected if they differ by exactly 1 character AND their starting letters have different types (one vowel, one consonant).
    -   The constraint requires successive words in the path to alternate between vowel-start and consonant-start.
    -   If `start` begins with a vowel, the next word must begin with a consonant, and vice versa.

### 3. Shortest Path + All Paths
-   **BFS**: To find the shortest distance.
-   **DFS/Backtracking**: To reconstruct all paths of that shortest distance.
-   Since we need *all* shortest paths, standard BFS storing `parent` pointers is good, but since a node can have multiple parents (multiple shortest paths reaching it), we store `List<String> parents` for each node.

## Approaches

### Approach 1: BFS + Backtracking (Standard Word Ladder II)

1.  **Preprocessing**: Identify Vowel/Consonant status for all words. Build an adjacency list where edges only exist between words differing by 1 char AND having different start-letter types.
2.  **BFS**:
    -   Start from `start`.
    -   Track `distance` to each word.
    -   Track `parents` map: `word -> list of previous words`.
    -   Standard level-order traversal. If we reach `end`, we stop adding new levels but finish the current level to find all parents.
3.  **Backtracking (DFS)**:
    -   Reconstruct paths from `end` back to `start` using the `parents` map.
    -   Reverse the paths for output.

### Approach 2: Bidirectional BFS
For very large dictionaries, Bidirectional BFS is faster. However, with `M <= 3000`, standard BFS is sufficient and easier to implement for "all paths".

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public List<List<String>> ladders(String start, String end, List<String> dict) {
        Set<String> dictSet = new HashSet<>(dict);
        dictSet.add(start);
        dictSet.add(end); // Ensure end is in dict for graph building
        
        // Build adjacency list with constraints
        Map<String, List<String>> adj = new HashMap<>();
        for (String w : dictSet) {
            adj.put(w, new ArrayList<>());
        }
        
        List<String> words = new ArrayList<>(dictSet);
        for (int i = 0; i < words.size(); i++) {
            for (int j = i + 1; j < words.size(); j++) {
                String w1 = words.get(i);
                String w2 = words.get(j);
                if (isOneDiff(w1, w2) && isAlternating(w1, w2)) {
                    adj.get(w1).add(w2);
                    adj.get(w2).add(w1);
                }
            }
        }
        
        // BFS
        Map<String, Integer> dist = new HashMap<>();
        Map<String, List<String>> parents = new HashMap<>();
        Queue<String> q = new LinkedList<>();
        
        q.offer(start);
        dist.put(start, 0);
        
        boolean found = false;
        
        while (!q.isEmpty()) {
            int size = q.size();
            Set<String> currentLevelVisited = new HashSet<>();
            
            for (int i = 0; i < size; i++) {
                String curr = q.poll();
                if (curr.equals(end)) found = true;
                
                int curDist = dist.get(curr);
                
                for (String neighbor : adj.getOrDefault(curr, new ArrayList<>())) {
                    if (!dist.containsKey(neighbor)) {
                        // Not visited yet
                        if (currentLevelVisited.add(neighbor)) {
                            dist.put(neighbor, curDist + 1);
                            q.offer(neighbor);
                        }
                        parents.computeIfAbsent(neighbor, k -> new ArrayList<>()).add(curr);
                    } else if (dist.get(neighbor) == curDist + 1) {
                        // Visited in this level (another shortest path)
                        parents.computeIfAbsent(neighbor, k -> new ArrayList<>()).add(curr);
                    }
                }
            }
            if (found) break;
        }
        
        List<List<String>> results = new ArrayList<>();
        if (found) {
            List<String> path = new ArrayList<>();
            path.add(end);
            backtrack(end, start, parents, path, results);
        }
        
        // Sort results for consistent output if needed (problem doesn't specify order, but usually lexicographical or any)
        // The problem output example shows sorted paths.
        results.sort((a, b) -> {
            for(int i=0; i<a.size(); i++) {
                if(!a.get(i).equals(b.get(i))) return a.get(i).compareTo(b.get(i));
            }
            return 0;
        });
        
        return results;
    }
    
    private void backtrack(String curr, String start, Map<String, List<String>> parents, List<String> path, List<List<String>> results) {
        if (curr.equals(start)) {
            List<String> fullPath = new ArrayList<>(path);
            Collections.reverse(fullPath);
            results.add(fullPath);
            return;
        }
        
        for (String p : parents.getOrDefault(curr, new ArrayList<>())) {
            path.add(p);
            backtrack(p, start, parents, path, results);
            path.remove(path.size() - 1);
        }
    }
    
    private boolean isOneDiff(String a, String b) {
        if (a.length() != b.length()) return false;
        int diff = 0;
        for (int i = 0; i < a.length(); i++) {
            if (a.charAt(i) != b.charAt(i)) diff++;
            if (diff > 1) return false;
        }
        return diff == 1;
    }
    
    private boolean isAlternating(String a, String b) {
        return isVowel(a.charAt(0)) != isVowel(b.charAt(0));
    }
    
    private boolean isVowel(char c) {
        return "aeiou".indexOf(c) != -1;
    }
}
```

### Python

```python
def is_vowel(c):
    """Check if character is a vowel."""
    return c in 'aeiou'

def generate_alternating_strings(s):
    """
    Generate all permutations of string s that alternate 
    between vowels and consonants.
    """
    results = []
    chars = sorted(s)  # Sort for lexicographic ordering
    
    def backtrack(path, remaining):
        if not remaining:
            results.append(''.join(path))
            return
        
        seen = set()  # Avoid duplicates at same position
        for i in range(len(remaining)):
            if remaining[i] in seen:
                continue
            seen.add(remaining[i])
            
            # Check alternation constraint
            if len(path) > 0:
                last_is_vowel = is_vowel(path[-1])
                curr_is_vowel = is_vowel(remaining[i])
                if last_is_vowel == curr_is_vowel:
                    continue
            
            # Recurse with remaining characters
            backtrack(path + [remaining[i]], remaining[:i] + remaining[i+1:])
    
    backtrack([], chars)
    return results if results else ["NONE"]

def main():
    s = input().strip()
    result = generate_alternating_strings(s)
    for r in result:
        print(r)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <queue>
#include <algorithm>

using namespace std;

class Solution {
public:
    vector<vector<string>> ladders(string start, string end, const vector<string>& dict) {
        unordered_set<string> wordSet(dict.begin(), dict.end());
        wordSet.insert(start);
        wordSet.insert(end);
        
        unordered_map<string, vector<string>> parents;
        unordered_map<string, int> dist;
        queue<string> q;
        
        q.push(start);
        dist[start] = 0;
        
        bool found = false;
        
        while (!q.empty() && !found) {
            int size = q.size();
            unordered_set<string> levelVisited;
            
            for (int i = 0; i < size; i++) {
                string curr = q.front();
                q.pop();
                
                if (curr == end) found = true;
                
                string temp = curr;
                for (int j = 0; j < temp.length(); j++) {
                    char original = temp[j];
                    for (char c = 'a'; c <= 'z'; c++) {
                        if (c == original) continue;
                        temp[j] = c;
                        if (wordSet.count(temp) && isAlternating(curr, temp)) {
                            if (dist.find(temp) == dist.end()) {
                                if (levelVisited.find(temp) == levelVisited.end()) {
                                    dist[temp] = dist[curr] + 1;
                                    q.push(temp);
                                    levelVisited.insert(temp);
                                }
                                parents[temp].push_back(curr);
                            } else if (dist[temp] == dist[curr] + 1) {
                                parents[temp].push_back(curr);
                            }
                        }
                    }
                    temp[j] = original;
                }
            }
        }
        
        vector<vector<string>> results;
        if (found) {
            vector<string> path;
            path.push_back(end);
            backtrack(end, start, parents, path, results);
        }
        
        // Sort for deterministic output
        sort(results.begin(), results.end());
        
        return results;
    }

private:
    void backtrack(string curr, string start, unordered_map<string, vector<string>>& parents, vector<string>& path, vector<vector<string>>& results) {
        if (curr == start) {
            vector<string> fullPath = path;
            reverse(fullPath.begin(), fullPath.end());
            results.push_back(fullPath);
            return;
        }
        
        for (const string& p : parents[curr]) {
            path.push_back(p);
            backtrack(p, start, parents, path, results);
            path.pop_back();
        }
    }

    bool isAlternating(const string& a, const string& b) {
        return isVowel(a[0]) != isVowel(b[0]);
    }

    bool isVowel(char c) {
        return string("aeiou").find(c) != string::npos;
    }
};
```

### JavaScript

```javascript
class Solution {
  ladders(start, end, dict) {
    const wordSet = new Set(dict);
    wordSet.add(start);
    wordSet.add(end);

    const isVowel = (c) => "aeiou".includes(c);
    const isAlternating = (a, b) => isVowel(a[0]) !== isVowel(b[0]);

    const parents = new Map();
    const dist = new Map();
    const queue = [start];
    dist.set(start, 0);

    let found = false;
    let head = 0;

    while (head < queue.length) {
      if (found) break; // Finish processing current level then stop
      // We need to be careful not to process next level if found.
      
      // Collect current level nodes
      const levelSize = queue.length - head;
      const currentLevelNodes = [];
      for(let i=0; i<levelSize; i++) currentLevelNodes.push(queue[head+i]);
      
      // Check if end is in this level
      if (currentLevelNodes.includes(end)) found = true;
      
      const levelVisited = new Set();
      
      for (let i = 0; i < levelSize; i++) {
        const curr = queue[head++];
        const curDist = dist.get(curr);
        
        // Generate neighbors
        const chars = curr.split("");
        for (let j = 0; j < chars.length; j++) {
          const original = chars[j];
          for (let k = 0; k < 26; k++) {
            const c = String.fromCharCode(97 + k);
            if (c === original) continue;
            chars[j] = c;
            const neighbor = chars.join("");
            
            if (wordSet.has(neighbor) && isAlternating(curr, neighbor)) {
               if (!dist.has(neighbor)) {
                 if (!levelVisited.has(neighbor)) {
                   dist.set(neighbor, curDist + 1);
                   queue.push(neighbor);
                   levelVisited.add(neighbor);
                 }
                 if (!parents.has(neighbor)) parents.set(neighbor, []);
                 parents.get(neighbor).push(curr);
               } else if (dist.get(neighbor) === curDist + 1) {
                 if (!parents.has(neighbor)) parents.set(neighbor, []);
                 parents.get(neighbor).push(curr);
               }
            }
          }
          chars[j] = original;
        }
      }
    }

    const results = [];
    if (found) {
      const backtrack = (curr, path) => {
        if (curr === start) {
          results.push([...path].reverse());
          return;
        }
        const pars = parents.get(curr) || [];
        for (const p of pars) {
          path.push(p);
          backtrack(p, path);
          path.pop();
        }
      };
      backtrack(end, [end]);
    }
    
    results.sort((a, b) => {
        const sa = a.join(" ");
        const sb = b.join(" ");
        return sa.localeCompare(sb);
    });

    return results;
  }
}
```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:**
Start: `eat` (Vowel)
End: `cot` (Consonant)
Dict: `eat, cat, cot, eot`

1.  **Level 0**: `eat` (Dist 0).
2.  **Level 1**:
    -   Neighbors of `eat` (V): Must be Consonant-start.
    -   `cat` (C): Differs by 'c'. Valid. Dist 1. Parent `eat`.
    -   `eot` (V): Starts with V. `isAlternating` false. **Skip**.
    -   `cot` (C): Differs by 2 chars. Skip.
    -   Queue: `[cat]`.
3.  **Level 2**:
    -   Neighbors of `cat` (C): Must be Vowel-start.
    -   `cot` (C): Starts with C. `isAlternating` false. **Skip**.
    -   `eat` (V): Visited.
    -   `eot` (V): Differs by 'e' vs 'c' and 'o' vs 'a'. 2 diffs. Skip.
    -   `eot` (V): Differs by 'e' vs 'c' and 'o' vs 'a'. 2 diffs. Skip.
    -   **Validation**: The First letter must alternate.
    -   `eat` (V) -> `cat` (C). OK.
    -   `cat` (C) -> `cot` (C). **Invalid** (C -> C).
    -   `eat` (V) -> `eot` (V). **Invalid** (V -> V).
    -   `eot` (V) -> `cot` (C). OK.
    -   The example output `eat cat cot` implies a C->C transition which violates the strict alternation rule described. The solution enforces the rule strictly.
    -   For `eat` -> `cat` -> `cot`: `eat` (V), `cat` (C), `cot` (C).
    -   The solution strictly follows the text constraint. If the example output is inconsistent with the rules, the implementation will output valid paths according to the specification.
    -   Transitions:
    -   `eat` -> `cat` (V -> C). Valid.
    -   `cat` -> `cot` (C -> C). Invalid.
    -   `eat` -> `eot` (V -> V). Invalid.
    -   `eot` -> `cot` (V -> C). Valid.
    -   The implementation follows the specification as stated: "first letter of successive words must alternate".
    -   The code will output `NONE` or valid paths that exist according to the constraint.

## Proof of Correctness

The algorithm uses BFS, which guarantees finding the shortest path in an unweighted graph. By storing all parents that lead to a node with the same optimal distance, and then backtracking, we recover all shortest paths. The "alternating" constraint is enforced during neighbor generation/validation, ensuring all edges in the graph are valid.

## Interview Extensions

1.  **Bidirectional BFS**: Start from both `start` and `end` to meet in the middle. Reduces search space significantly.
2.  **Wildcard Preprocessing**: Map `*at` -> `[bat, cat, rat]`. Speeds up neighbor finding.

### Common Mistakes

-   **Graph Construction**: Forgetting that the graph is directed if the constraint is asymmetric (though V<->C is symmetric).
-   **BFS Level Processing**: Not handling multiple parents correctly. A node can be reached by multiple nodes in the previous level.
-   **Constraint Checking**: Misidentifying vowels or checking the wrong character index.
