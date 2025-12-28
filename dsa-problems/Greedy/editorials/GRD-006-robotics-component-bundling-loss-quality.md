---
problem_id: GRD_ROBOTICS_COMPONENT_BUNDLING__7259
display_id: GRD-006
slug: robotics-component-bundling-loss-quality
title: "Robotics Component Bundling with Loss and Quality Score"
difficulty: Medium
difficulty_score: 60
topics:
  - Greedy Algorithms
  - Heap
  - Priority Queue
  - Simulation
tags:
  - greedy
  - heap
  - priority-queue
  - simulation
  - medium
premium: true
subscription_tier: basic
---

# GRD-006: Robotics Component Bundling with Loss and Quality Score

## 📋 Problem Summary

You have a collection of parts, each with a weight and a quality score. You need to merge them all into a single component. Merging two parts combines their weights (with some loss) and degrades their quality. Specifically:
- New Weight = `W_1 + W_2 - lfloor 0.1 x min(W_1, W_2) rfloor`
- New Quality = `min(Q_1, Q_2) - 1`

You must ensure that every intermediate bundle maintains a quality of at least `T`. Find the maximum final weight possible, or return -1 if impossible.

## 🌍 Real-World Scenario

**Scenario Title:** The Clay Sculpting Class

Imagine a class of art students working with clay. They all start with small lumps of clay of varying "freshness" (quality). To make a large statue, they must combine their lumps.

- **Weight:** The amount of clay.
- **Loss:** Every time you squish two lumps together, a little bit of clay sticks to your hands or the table and is lost (10% of the smaller lump).
- **Quality:** The freshness/malleability of the clay.
- **Degradation:** Mixing clay dries it out slightly (-1 quality). Also, if you mix fresh clay with dry clay, the whole batch becomes limited by the dry clay (`min(Q_1, Q_2)`).

The teacher demands that the final statue (and every intermediate blob) must be moist enough to mold (Quality `>= T`). To get the biggest statue possible, the students should smartly combine the freshest lumps first to maintain workability as long as possible.

**Why This Problem Matters:**

- **Manufacturing:** combining materials often involves yield loss and quality degradation.
- **Signal Processing:** Merging signals can introduce noise (lower quality); maintaining a signal-to-noise ratio is critical.

![Real-World Application](../images/GRD-006/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: The Quality Decay

Threshold `T = 5`.
Parts: A(Q=10), B(Q=8), C(Q=6).

**Strategy: Merge Highest Quality First**

```text
Step 1: Merge A(10) and B(8)
   [ A ]      [ B ]
   (10)       (8)
     \        /
      \      /
       [ AB ]
    Q = min(10, 8) - 1 = 7
    (7 is >= 5, OK)

Step 2: Merge AB(7) and C(6)
       [ AB ]      [ C ]
        (7)        (6)
          \        /
           \      /
           [ ABC ]
      Q = min(7, 6) - 1 = 5
      (5 is >= 5, OK)
      
Success!
```

**Strategy: Merge Lowest Quality First (Bad)**

```text
Step 1: Merge B(8) and C(6)
   [ B ]      [ C ]
    (8)        (6)
      \        /
      [ BC ]
   Q = min(8, 6) - 1 = 5

Step 2: Merge A(10) and BC(5)
   [ A ]      [ BC ]
   (10)        (5)
      \        /
      [ ABC ]
   Q = min(10, 5) - 1 = 4
   (4 < 5, FAIL!)
```

## ✅ Input/Output Clarifications (Read This Before Coding)

- **Single Component:** You must merge *all* parts into one.
- **Impossible Case:** If at any step you cannot find two parts to merge that result in `Q >= T`, then the task is impossible. Return -1.
- **Loss Calculation:** The 10% loss is calculated on the *smaller* weight of the pair. `floor(0.1 * min_weight)`.

## Naive Approach

### Intuition

Try all possible orders of merging the `N` parts. This is equivalent to generating all possible binary merge trees.

### Algorithm

1. Permute the parts.
2. Simulate the merge process.
3. Check validity and track max weight.

### Time Complexity

- **Factorial:** `O(N!)` or worse (Catalan number for tree structures). Impossible for `N=200,000`.

## Optimal Approach

### Key Insight

We are fighting against **Quality Decay**. Every merge operation reduces the quality score. To keep the quality above the threshold `T` for as long as possible, we should always merge the **highest quality** parts available.

By merging the two best parts, we maximize the resulting quality: `min(high, high) - 1` is better than `min(high, low) - 1`. This "greedy for quality" strategy gives us the best buffer against the threshold.

Since the problem asks to maximize weight *if possible*, and the feasibility is strictly determined by quality, we prioritize feasibility. The weight calculation is deterministic based on the merge tree, but since we are constrained by `T`, the "Highest Quality First" tree is often the *only* valid tree (or one of the few).

### Algorithm

1. Store all parts in a **Max-Heap** ordered by **Quality**.
2. While the heap has more than 1 item:
   - Extract the two parts with the highest qualities: `P_1` and `P_2`.
   - Calculate new quality: `Q_new = min(P_1.q, P_2.q) - 1`.
   - **Check Constraint:** If `Q_new < T`, return -1 (impossible).
   - Calculate new weight: `W_new = P_1.w + P_2.w - lfloor 0.1 x min(P_1.w, P_2.w) rfloor`.
   - Insert new part `(W_new, Q_new)` back into the heap.
3. Return the weight of the single remaining part.

### Time Complexity

- **O(N log N)**: We perform `N-1` merges. Each merge involves heap operations (`O(log N)`).

### Space Complexity

- **O(N)**: To store the heap.

### Why This Is Optimal

If the two parts with the *highest* qualities cannot be merged to satisfy `T`, then *no* pair of parts can be merged to satisfy `T` (because any other pair would have equal or lower qualities). Thus, this greedy choice is necessary for feasibility.

![Algorithm Visualization](../images/GRD-006/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    static class Part implements Comparable<Part> {
        long w;
        int q;

        public Part(long w, int q) {
            this.w = w;
            this.q = q;
        }

        @Override
        public int compareTo(Part other) {
            // Max-heap based on quality
            return Integer.compare(other.q, this.q);
        }
    }

    public long maxBundleWeight(int n, int T, int[] weights, int[] qualities) {
        PriorityQueue<Part> pq = new PriorityQueue<>();
        
        for (int i = 0; i < n; i++) {
            pq.offer(new Part(weights[i], qualities[i]));
        }
        
        while (pq.size() > 1) {
            Part p1 = pq.poll();
            Part p2 = pq.poll();
            
            int newQ = Math.min(p1.q, p2.q) - 1;
            
            if (newQ < T) {
                return -1;
            }
            
            long minW = Math.min(p1.w, p2.w);
            long loss = (long) Math.floor(0.1 * minW);
            long newW = p1.w + p2.w - loss;
            
            pq.offer(new Part(newW, newQ));
        }
        
        return pq.isEmpty() ? -1 : pq.poll().w;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        
        int n = sc.nextInt();
        int T = sc.nextInt();

        int[] weights = new int[n];
        for (int i = 0; i < n; i++) {
            weights[i] = sc.nextInt();
        }

        int[] qualities = new int[n];
        for (int i = 0; i < n; i++) {
            qualities[i] = sc.nextInt();
        }

        Solution solution = new Solution();
        System.out.println(solution.maxBundleWeight(n, T, weights, qualities));
        sc.close();
    }
}
```

### Python

```python
import heapq
import math
import sys

def max_bundle_weight(n: int, T: int, weights: list, qualities: list) -> int:
    # Max-heap: store (-quality, weight)
    pq = []
    for w, q in zip(weights, qualities):
        heapq.heappush(pq, (-q, w))
        
    while len(pq) > 1:
        # Pop two highest qualities
        neg_q1, w1 = heapq.heappop(pq)
        neg_q2, w2 = heapq.heappop(pq)
        
        q1, q2 = -neg_q1, -neg_q2
        
        new_q = min(q1, q2) - 1
        
        if new_q < T:
            return -1
            
        loss = math.floor(0.1 * min(w1, w2))
        new_w = w1 + w2 - loss
        
        heapq.heappush(pq, (-new_q, new_w))
        
    return pq[0][1] if pq else -1

def main():
    data = sys.stdin.read()
    data = data.split()
    if not data:
        return
        
    idx = 0
    n = int(data[idx])
    idx += 1
    T = int(data[idx])
    idx += 1
    
    weights = []
    for _ in range(n):
        weights.append(int(data[idx]))
        idx += 1
        
    qualities = []
    for _ in range(n):
        qualities.append(int(data[idx]))
        idx += 1

    result = max_bundle_weight(n, T, weights, qualities)
    print(result)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <cmath>
#include <algorithm>

using namespace std;

struct Part {
    long long w;
    int q;
    
    // For priority_queue, we want max quality at top.
    // Default is max-heap, so operator< should return true if 'this' is smaller than 'other'.
    bool operator<(const Part& other) const {
        return q < other.q;
    }
};

class Solution {
public:
    long long maxBundleWeight(int n, int T, vector<int>& weights, vector<int>& qualities) {
        priority_queue<Part> pq;
        
        for (int i = 0; i < n; i++) {
            pq.push({(long long)weights[i], qualities[i]});
        }
        
        while (pq.size() > 1) {
            Part p1 = pq.top(); pq.pop();
            Part p2 = pq.top(); pq.pop();
            
            int newQ = min(p1.q, p2.q) - 1;
            
            if (newQ < T) {
                return -1;
            }
            
            long long minW = min(p1.w, p2.w);
            long long loss = floor(0.1 * minW);
            long long newW = p1.w + p2.w - loss;
            
            pq.push({newW, newQ});
        }
        
        return pq.empty() ? -1 : pq.top().w;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, T;
    if (!(cin >> n >> T)) return 0;

    vector<int> weights(n), qualities(n);
    for (int i = 0; i < n; i++) {
        cin >> weights[i];
    }
    for (int i = 0; i < n; i++) {
        cin >> qualities[i];
    }

    Solution solution;
    cout << solution.maxBundleWeight(n, T, weights, qualities) << "\n";

    return 0;
}
```

### JavaScript

```javascript
const readline = require("readline");

class MaxHeap {
  constructor() {
    this.heap = [];
  }
  push(val) {
    this.heap.push(val);
    this._siftUp();
  }
  pop() {
    if (this.size() === 0) return null;
    if (this.size() === 1) return this.heap.pop();
    const max = this.heap[0];
    this.heap[0] = this.heap.pop();
    this._siftDown();
    return max;
  }
  size() {
    return this.heap.length;
  }
  _siftUp() {
    let idx = this.heap.length - 1;
    while (idx > 0) {
      const parentIdx = Math.floor((idx - 1) / 2);
      if (this.heap[idx].q <= this.heap[parentIdx].q) break;
      [this.heap[idx], this.heap[parentIdx]] = [this.heap[parentIdx], this.heap[idx]];
      idx = parentIdx;
    }
  }
  _siftDown() {
    let idx = 0;
    while (idx < this.heap.length) {
      let maxChildIdx = null;
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;
      if (left < this.heap.length) maxChildIdx = left;
      if (right < this.heap.length && this.heap[right].q > this.heap[left].q) {
        maxChildIdx = right;
      }
      if (maxChildIdx === null || this.heap[idx].q >= this.heap[maxChildIdx].q) break;
      [this.heap[idx], this.heap[maxChildIdx]] = [this.heap[maxChildIdx], this.heap[idx]];
      idx = maxChildIdx;
    }
  }
}

class Solution {
  maxBundleWeight(n, T, weights, qualities) {
    const pq = new MaxHeap();
    
    for (let i = 0; i < n; i++) {
      pq.push({ w: weights[i], q: qualities[i] });
    }
    
    while (pq.size() > 1) {
      const p1 = pq.pop();
      const p2 = pq.pop();
      
      const newQ = Math.min(p1.q, p2.q) - 1;
      
      if (newQ < T) {
        return -1;
      }
      
      const minW = Math.min(p1.w, p2.w);
      const loss = Math.floor(0.1 * minW);
      const newW = p1.w + p2.w - loss;
      
      pq.push({ w: newW, q: newQ });
    }
    
    return pq.size() === 1 ? pq.pop().w : -1;
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

let data = [];
rl.on("line", (line) => data.push(line.trim()));
rl.on("close", () => {
  if (data.length === 0) return;
  
  let ptr = 0;
  const [n, T] = data[ptr++].split(" ").map(Number);
  const weights = data[ptr++].split(" ").map(Number);
  const qualities = data[ptr++].split(" ").map(Number);

  const solution = new Solution();
  console.log(solution.maxBundleWeight(n, T, weights, qualities));
});
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input:**
```
3 5
4 3 2
10 8 6
```

**Initialization:**
Heap: `[(Q10, W4), (Q8, W3), (Q6, W2)]`

**Iteration 1:**
- Pop `(Q10, W4)` and `(Q8, W3)`.
- New Q: `min(10, 8) - 1 = 7`. (`7 >= 5`, OK).
- New W: `4 + 3 - floor(0.1 * 3) = 7 - 0 = 7`.
- Push `(Q7, W7)`.
- Heap: `[(Q7, W7), (Q6, W2)]`.

**Iteration 2:**
- Pop `(Q7, W7)` and `(Q6, W2)`.
- New Q: `min(7, 6) - 1 = 5`. (`5 >= 5`, OK).
- New W: `7 + 2 - floor(0.1 * 2) = 9 - 0 = 9`.
- Push `(Q5, W9)`.
- Heap: `[(Q5, W9)]`.

**Result:** `9`.

![Example Visualization](../images/GRD-006/example-1.png)

## ✅ Proof of Correctness

### Invariant
At any step, the heap contains the set of components that maximizes the potential to satisfy the quality constraint for future merges.

### Why the approach is correct
Let `S` be the set of available parts. To merge all parts, we must perform a sequence of merges.
If we merge two parts with qualities `q_a, q_b`, the result has quality `min(q_a, q_b) - 1`.
This operation is monotonic: lower inputs yield lower outputs.
To maximize the minimum quality in the final tree (or to keep intermediate values as high as possible), we should always combine the largest available values.
This is analogous to Huffman coding but maximizing the "bottleneck" capacity (quality) rather than minimizing path length.

## 💡 Interview Extensions

- **Extension 1:** What if we want to *maximize* the final quality instead of weight?
  - *Answer:* The same greedy strategy works! It maximizes the bottleneck at every step.
- **Extension 2:** What if the loss percentage varies per item?
  - *Answer:* If quality is still the constraint, the strategy doesn't change. If we need to optimize weight primarily (and quality is easy), we might merge small weights first (Huffman).
- **Extension 3:** What if we can discard some parts?
  - *Answer:* Then we would discard low-quality parts that drag down the average, or low-weight parts that aren't worth the loss. This becomes a subset selection problem.

### Common Mistakes to Avoid

1. **Merging by Weight**
   - ❌ Wrong: Merging small weights first (like Huffman) ignores the quality constraint and will likely fail the threshold check early.
   - ✅ Correct: Merge by Quality.

2. **Incorrect Loss Calculation**
   - ❌ Wrong: `0.1 * sum`.
   - ✅ Correct: `0.1 * min(w1, w2)`.

3. **Floating Point Issues**
   - ❌ Wrong: Using floats for final weight if precise integer arithmetic is required.
   - ✅ Correct: Use `floor` and keep weights as integers/longs.

## Related Concepts

- **Huffman Coding:** Merging based on values (though min/max logic is reversed here).
- **Minimax / Bottleneck Paths:** Optimization problems involving `min` or `max` constraints.
- **Greedy Choice Property:** Local optimal leads to global optimal.
