---
problem_id: GRD_CAMPUS_EVENT_TICKET_CAPS__5864
display_id: GRD-011
slug: campus-event-ticket-caps
title: "Campus Event Ticket Caps"
difficulty: Medium
difficulty_score: 50
topics:
  - Greedy Algorithms
  - Heap
  - Scheduling
tags:
  - greedy
  - heap
  - priority-queue
  - scheduling
  - medium
premium: true
subscription_tier: basic
---

# GRD-011: Campus Event Ticket Caps

## 📋 Problem Summary

You have `n` requests to process. Each request has a **value** (quantity of tickets) and a **deadline**. You can process at most one request per day. Your goal is to select a set of requests to process such that each is completed by its deadline, maximizing the total value (tickets sold).

## 🌍 Real-World Scenario

**Scenario Title:** Freelance Project Management

You are a freelancer with a list of potential gigs.
- Each gig pays a certain amount (`q`).
- Each gig has a strict deadline (`d`).
- Each gig takes exactly 1 day to complete.

You want to pick the most profitable set of gigs to work on. You can't do everything because some deadlines clash. For example, if you have 3 gigs due on Day 1, you can only pick one. If you have a high-paying gig due on Day 10, you can do it on Day 1, 2, ..., or 10.

**Why This Problem Matters:**

- **Revenue Maximization:** Choosing the most valuable tasks under time constraints.
- **Scheduling:** Standard single-machine scheduling with deadlines and profits.

![Real-World Application](../images/GRD-011/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: The Timeline

Requests: A(3, d=1), B(5, d=3), C(2, d=2).

Sort by deadline: A(d=1), C(d=2), B(d=3).

```text
Day 1:
Deadline 1 requests: [A(3)].
We must pick one. Pick A.
Total = 3.

Day 2:
Deadline 2 requests: [C(2)].
We can pick C.
Total = 3 + 2 = 5.

Day 3:
Deadline 3 requests: [B(5)].
We can pick B.
Total = 5 + 5 = 10.
```

What if we had D(10, d=1)?
Day 1: Options [A(3), D(10)].
Pick D (higher value). Drop A.
Total = 10.

## ✅ Input/Output Clarifications (Read This Before Coding)

- **One per day:** You consume 1 unit of time per request.
- **Deadline:** `d[i]` means the request must be processed on day `d[i]` or earlier.
- **Processing Time:** Implicitly 1 day.

## Naive Approach

### Intuition

Try all subsets of requests. For each subset, check if a valid schedule exists. Pick the max value subset.

### Algorithm

1. Generate subsets.
2. Sort subset by deadline.
3. Check if `subset[i]` can be done at time `i+1`.
4. Maximize sum.

### Time Complexity

- **O(2^N)**: Too slow.

## Optimal Approach

### Key Insight

We should process requests in order of their **deadlines**. Why? Because a request with an earlier deadline is more "urgent". A request with deadline 10 can be done on day 1, but a request with deadline 1 *must* be done on day 1.

However, just picking urgent tasks might force us to drop high-value tasks later.
Strategy:
1. Sort all requests by **deadline**.
2. Iterate through them.
3. Add the current request to our "selected" pile.
4. Check if the "selected" pile is valid (size `<=` current deadline).
   - If we have selected too many items (`k > D`), we must drop one.
   - Which one to drop? The one with the **smallest value**. This maximizes the total sum of the remaining set.

### Algorithm

1. Sort requests by deadline ascending.
2. Initialize a **Min-Heap** to store the values (quantities) of selected requests.
3. Iterate through sorted requests:
   - Push current request's value to heap.
   - If `heap.size() > current_request.deadline`:
     - Pop the minimum value from the heap (drop the least valuable request to make space).
4. Sum up elements in the heap.

### Time Complexity

- **O(N log N)**: Sorting takes `O(N log N)`. Heap operations take `O(N log N)`.

### Space Complexity

- **O(N)**: Heap storage.

### Why This Is Optimal

This is a classic greedy exchange argument.
At any point, if we have more tasks than time slots, we must discard one. Discarding the smallest value minimizes the loss, leaving the highest possible total value for the available slots. Since we process by deadline, we ensure that the tasks we *keep* can indeed be scheduled (Hall's Marriage Theorem condition or simple exchange argument).

![Algorithm Visualization](../images/GRD-011/algorithm-visualization.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public long maxTickets(int n, int[][] requests) {
        // Sort by deadline
        Arrays.sort(requests, (a, b) -> Integer.compare(a[1], b[1]));
        
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        long totalTickets = 0;
        
        for (int[] req : requests) {
            int quantity = req[0];
            int deadline = req[1];
            
            pq.offer(quantity);
            totalTickets += quantity;
            
            // If we have more tasks than the current deadline allows,
            // remove the one with the smallest quantity.
            // Note: Since we sorted by deadline, the current deadline is the max time available
            // for ALL tasks currently in the heap.
            if (pq.size() > deadline) {
                totalTickets -= pq.poll();
            }
        }
        
        return totalTickets;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        
        int n = sc.nextInt();
        int[][] requests = new int[n][2];
        for (int i = 0; i < n; i++) {
            requests[i][0] = sc.nextInt();
            requests[i][1] = sc.nextInt();
        }
        
        Solution solution = new Solution();
        System.out.println(solution.maxTickets(n, requests));
        sc.close();
    }
}
```

### Python

```python
import heapq
import sys

def max_tickets(n: int, requests: list) -> int:
    # Sort by deadline
    requests.sort(key=lambda x: x[1])
    
    pq = [] # Min-heap for quantities
    
    for q, d in requests:
        heapq.heappush(pq, q)
        
        if len(pq) > d:
            heapq.heappop(pq)
            
    return sum(pq)

def main():
    data = sys.stdin.read()
    data = data.split()
    if not data:
        return
        
    idx = 0
    n = int(data[idx])
    idx += 1
    
    requests = []
    for _ in range(n):
        q = int(data[idx])
        idx += 1
        d = int(data[idx])
        idx += 1
        requests.append([q, d])

    result = max_tickets(n, requests)
    print(result)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

class Solution {
public:
    long long maxTickets(int n, vector<pair<int,int>>& requests) {
        // Sort by deadline (second element)
        sort(requests.begin(), requests.end(), [](const pair<int,int>& a, const pair<int,int>& b) {
            return a.second < b.second;
        });
        
        priority_queue<int, vector<int>, greater<int>> pq;
        long long total = 0;
        
        for (const auto& req : requests) {
            int quantity = req.first;
            int deadline = req.second;
            
            pq.push(quantity);
            total += quantity;
            
            if (pq.size() > deadline) {
                total -= pq.top();
                pq.pop();
            }
        }
        
        return total;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<pair<int,int>> requests(n);
    for (int i = 0; i < n; i++) {
        cin >> requests[i].first >> requests[i].second;
    }

    Solution solution;
    cout << solution.maxTickets(n, requests) << "\n";

    return 0;
}
```

### JavaScript

```javascript
const readline = require("readline");

class MinHeap {
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
    const min = this.heap[0];
    this.heap[0] = this.heap.pop();
    this._siftDown();
    return min;
  }
  size() {
    return this.heap.length;
  }
  _siftUp() {
    let idx = this.heap.length - 1;
    while (idx > 0) {
      const parentIdx = Math.floor((idx - 1) / 2);
      if (this.heap[idx] >= this.heap[parentIdx]) break;
      [this.heap[idx], this.heap[parentIdx]] = [this.heap[parentIdx], this.heap[idx]];
      idx = parentIdx;
    }
  }
  _siftDown() {
    let idx = 0;
    while (idx < this.heap.length) {
      let minChildIdx = null;
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;
      if (left < this.heap.length) minChildIdx = left;
      if (right < this.heap.length && this.heap[right] < this.heap[left]) {
        minChildIdx = right;
      }
      if (minChildIdx === null || this.heap[idx] <= this.heap[minChildIdx]) break;
      [this.heap[idx], this.heap[minChildIdx]] = [this.heap[minChildIdx], this.heap[idx]];
      idx = minChildIdx;
    }
  }
}

class Solution {
  maxTickets(n, requests) {
    // Sort by deadline
    requests.sort((a, b) => a[1] - b[1]);
    
    const pq = new MinHeap();
    let total = 0;
    
    for (const [q, d] of requests) {
      pq.push(q);
      total += q;
      
      if (pq.size() > d) {
        total -= pq.pop();
      }
    }
    
    return total;
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
  const n = parseInt(data[ptr++]);
  
  const requests = [];
  for (let i = 0; i < n; i++) {
    const [q, d] = data[ptr++].split(" ").map(Number);
    requests.push([q, d]);
  }

  const solution = new Solution();
  console.log(solution.maxTickets(n, requests));
});
```

## 🧪 Test Case Walkthrough (Dry Run)

**Input:**
```
3
3 1
5 3
2 2
```

**Sorted Requests:**
1. (3, d=1)
2. (2, d=2)
3. (5, d=3)

**Execution:**
- **Req 1 (3, 1):** Push 3. Heap: `[3]`. Size 1 <= Deadline 1. OK.
- **Req 2 (2, 2):** Push 2. Heap: `[2, 3]`. Size 2 <= Deadline 2. OK.
- **Req 3 (5, 3):** Push 5. Heap: `[2, 3, 5]`. Size 3 <= Deadline 3. OK.

**Result:** Sum = 10.

**Another Case:**
Input: `(10, 1), (20, 1)`.
Sorted: `(10, 1), (20, 1)`.
- **Req 1:** Push 10. Heap `[10]`. Size 1 <= 1. OK.
- **Req 2:** Push 20. Heap `[10, 20]`. Size 2 > 1. Pop min (10). Heap `[20]`.
Result: 20. Correct.

![Example Visualization](../images/GRD-011/example-1.png)

## ✅ Proof of Correctness

### Invariant
The heap contains the `k` largest values encountered so far that can be scheduled within the current deadline `D`.

### Why the approach is correct
Suppose we are at deadline `D`. We have seen a set of tasks `S` with deadlines `<= D`.
We want to pick the largest subset of `S` with size `<= D`.
Our algorithm ensures `heap.size() <= current_deadline` at every step.
Since we process in increasing order of deadlines, this local check effectively maintains the global validity condition.
By always discarding the smallest element when capacity is exceeded, we ensure the sum of the remaining elements is maximized.

## 💡 Interview Extensions

- **Extension 1:** What if tasks take different amounts of time?
  - *Answer:* This becomes the **Knapsack Problem** or **Job Sequencing with Deadlines** (NP-hard if general, but solvable with DP if times are small integers).
- **Extension 2:** What if we want to minimize the number of late tasks?
  - *Answer:* Just count how many we dropped.
- **Extension 3:** What if we have multiple machines?
  - *Answer:* Capacity becomes `m * deadline`.

### Common Mistakes to Avoid

1. **Sorting by Value**
   - ❌ Wrong: Prioritizing high value first might miss tight deadlines.
   - ✅ Correct: Sort by Deadline.

2. **Heap Direction**
   - ❌ Wrong: Using Max-Heap.
   - ✅ Correct: Min-Heap (to eject the smallest).

3. **Index Confusion**
   - ❌ Wrong: Comparing heap size to `n`.
   - ✅ Correct: Compare heap size to `current_request.deadline`.

## Related Concepts

- **Job Sequencing Problem:** The classic version.
- **Greedy with Priority Queue:** Common pattern.
- **Matroid:** Theoretical framework for this type of greedy solution.
