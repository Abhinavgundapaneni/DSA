---
problem_id: QUE_CIRCULAR_SHUTTLE_BUFFER_OVERWRITE__7314
display_id: QUE-002
slug: circular-shuttle-buffer-overwrite
title: "Circular Shuttle Buffer with Overwrite"
difficulty: Easy
difficulty_score: 28
topics:
  - Queue
  - Circular Buffer
  - Simulation
tags:
  - queue
  - circular-buffer
  - simulation
  - easy
premium: true
subscription_tier: basic
---

# QUE-002: Circular Shuttle Buffer with Overwrite

## 📋 Problem Summary

We need to implement a fixed-size circular buffer (capacity `k`) that supports standard queue operations plus a special overwrite mode.
- **ENQ x:** Add `x` to the rear. Fails if full.
- **ENQ_OVR x:** Add `x` to the rear. If full, overwrite the oldest element (front) and succeed.
- **DEQ:** Remove from front.
- **FRONT / REAR:** Peek at front/rear.
- **ISEMPTY / ISFULL:** Check status.

## 🌍 Real-World Scenario

**Scenario Title:** Dashcam Recording

Imagine a dashboard camera in a car.
- It records video in 1-minute chunks.
- The memory card has limited space (e.g., can hold 60 minutes).
- When the card is full, it doesn't stop recording.
- Instead, it **overwrites** the oldest footage to make room for the new minute.
- This ensures you always have the latest hour of driving footage.
- Standard file copying would be slow; a **Circular Buffer** allows this overwrite in `O(1)` time by just moving pointers.

**Why This Problem Matters:**

- **Log Rotation:** Servers keeping the last N lines of logs.
- **Audio Buffering:** Ring buffers in sound cards.
- **Network Switches:** Dropping old packets when the buffer is full (Tail Drop vs. Head Drop).

![Real-World Application](../images/QUE-002/real-world-scenario.png)

## Detailed Explanation

### ASCII Diagram: Circular Buffer Logic

Capacity `k=3`. Array `arr` of size 3.
Pointers: `head` (start), `tail` (end), `count` (size).

1. `ENQ 1`: `arr=[1, _, _]`, head=0, tail=1, count=1.
2. `ENQ 2`: `arr=[1, 2, _]`, head=0, tail=2, count=2.
3. `ENQ 3`: `arr=[1, 2, 3]`, head=0, tail=0 (wrap), count=3 (FULL).
4. `ENQ 4`: Fails (Full).
5. `ENQ_OVR 4`:
   - Full, so "remove" head (1). `head` moves to 1.
   - Insert 4 at `tail` (0). `arr=[4, 2, 3]`.
   - `tail` moves to 1.
   - `count` remains 3.
   - Queue logical order: `2 -> 3 -> 4`.

### ✅ Input/Output Clarifications (Read This Before Coding)

- **Input:** Capacity `k`, then `m` commands.
- **Output:** Boolean for success/status, or values for peek/pop.
- **ENQ_OVR:** If not full, acts like normal `ENQ`. If full, reports "overwritten".

## Naive Approach

### Intuition

Use a standard list/array and shift elements.
- `ENQ`: Append.
- `DEQ`: Remove index 0 (shift all).
- `ENQ_OVR`: If full, remove index 0, then append.

### Limitations

- `DEQ` and `ENQ_OVR` (when full) are `O(k)` due to shifting.
- With `m` operations, total time `O(m x k)`, which is too slow if `k` is large.

## Optimal Approach

### Key Insight

Use a fixed-size array with `head` and `tail` indices and modulo arithmetic.
- **Index:** `(index + 1) % k`.
- **Size:** Track `count` explicitly to distinguish empty vs full (or use `(tail + 1) % k == head` rule, but explicit count is easier).

### Algorithm

1. `arr` of size `k`. `head = 0`, `tail = 0`, `count = 0`.
2. `ENQ x`:
   - If `count == k`: return `false`.
   - `arr[tail] = x`.
   - `tail = (tail + 1) % k`.
   - `count++`.
   - Return `true`.
3. `ENQ_OVR x`:
   - If `count < k`: Call `ENQ x`. Return `true` (or whatever success msg).
   - If `count == k`:
     - `head = (head + 1) % k` (Drop oldest).
     - `arr[tail] = x`.
     - `tail = (tail + 1) % k`.
     - Return "overwritten".
4. `DEQ`:
   - If `count == 0`: return "EMPTY".
   - Val = `arr[head]`.
   - `head = (head + 1) % k`.
   - `count--`.
   - Return Val.

### Time Complexity

- **O(1)** for all operations.

### Space Complexity

- **O(k)** for the array.

![Algorithm Visualization](../images/QUE-002/algorithm-visualization.png)
![Algorithm Steps](../images/QUE-002/algorithm-steps.png)

## Implementations

### Java

```java
import java.util.*;

class Solution {
    public List<String> processOperations(int k, List<String[]> operations) {
        List<String> result = new ArrayList<>();
        int[] buffer = new int[k];
        int head = 0;
        int tail = 0;
        int count = 0;

        for (String[] op : operations) {
            String cmd = op[0];
            if (cmd.equals("ENQ")) {
                if (count == k) {
                    result.add("false");
                } else {
                    buffer[tail] = Integer.parseInt(op[1]);
                    tail = (tail + 1) % k;
                    count++;
                    result.add("true");
                }
            } else if (cmd.equals("ENQ_OVR")) {
                int val = Integer.parseInt(op[1]);
                if (count == k) {
                    int overwrittenVal = buffer[head];
                    head = (head + 1) % k; // Drop oldest
                    buffer[tail] = val;
                    tail = (tail + 1) % k;
                    result.add(String.valueOf(overwrittenVal));
                } else {
                    buffer[tail] = val;
                    tail = (tail + 1) % k;
                    count++;
                    result.add("NONE");
                }
            } else if (cmd.equals("DEQ")) {
                if (count == 0) {
                    result.add("EMPTY");
                } else {
                    result.add(String.valueOf(buffer[head]));
                    head = (head + 1) % k;
                    count--;
                }
            } else if (cmd.equals("FRONT")) {
                if (count == 0) result.add("EMPTY");
                else result.add(String.valueOf(buffer[head]));
            } else if (cmd.equals("REAR")) {
                if (count == 0) result.add("EMPTY");
                else {
                    int idx = (tail - 1 + k) % k;
                    result.add(String.valueOf(buffer[idx]));
                }
            } else if (cmd.equals("ISEMPTY")) {
                result.add(count == 0 ? "true" : "false");
            } else if (cmd.equals("ISFULL")) {
                result.add(count == k ? "true" : "false");
            }
        }
        return result;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int k = sc.nextInt();
            int m = sc.nextInt();
            List<String[]> operations = new ArrayList<>();
    
            for (int i = 0; i < m; i++) {
                String op = sc.next();
                if (op.equals("ENQ") || op.equals("ENQ_OVR")) {
                    String x = sc.next();
                    operations.add(new String[]{op, x});
                } else {
                    operations.add(new String[]{op});
                }
            }
    
            Solution solution = new Solution();
            List<String> result = solution.processOperations(k, operations);
            for (String line : result) {
                System.out.println(line);
            }
        }
        sc.close();
    }
}
```

### Python

```python
from typing import List
import sys

def process_operations(k: int, operations: List[List[str]]) -> List[str]:
    buffer = [0] * k
    head = 0
    tail = 0
    count = 0
    result = []
    
    for op_data in operations:
        cmd = op_data[0]
        
        if cmd == "ENQ":
            if count == k:
                result.append("false")
            else:
                buffer[tail] = int(op_data[1])
                tail = (tail + 1) % k
                count += 1
                result.append("true")
                
        elif cmd == "ENQ_OVR":
            val = int(op_data[1])
            if count == k:
                overwritten_val = buffer[head]
                head = (head + 1) % k
                buffer[tail] = val
                tail = (tail + 1) % k
                result.append(str(overwritten_val))
            else:
                buffer[tail] = val
                tail = (tail + 1) % k
                count += 1
                result.append("NONE")
                
        elif cmd == "DEQ":
            if count == 0:
                result.append("EMPTY")
            else:
                result.append(str(buffer[head]))
                head = (head + 1) % k
                count -= 1
                
        elif cmd == "FRONT":
            if count == 0:
                result.append("EMPTY")
            else:
                result.append(str(buffer[head]))
                
        elif cmd == "REAR":
            if count == 0:
                result.append("EMPTY")
            else:
                idx = (tail - 1 + k) % k
                result.append(str(buffer[idx]))
                
        elif cmd == "ISEMPTY":
            result.append("true" if count == 0 else "false")
            
        elif cmd == "ISFULL":
            result.append("true" if count == k else "false")
            
    return result

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        k = int(next(iterator))
        m = int(next(iterator))
        operations = []
        for _ in range(m):
            op = next(iterator)
            if op in ("ENQ", "ENQ_OVR"):
                val = next(iterator)
                operations.append([op, val])
            else:
                operations.append([op])
        
        result = process_operations(k, operations)
        print("\n".join(result))
    except StopIteration:
        pass

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <string>

using namespace std;

class Solution {
public:
    vector<string> processOperations(int k, const vector<vector<string>>& operations) {
        vector<int> buffer(k);
        int head = 0;
        int tail = 0;
        int count = 0;
        vector<string> result;
        
        for (const auto& op_data : operations) {
            const string& cmd = op_data[0];
            
            if (cmd == "ENQ") {
                if (count == k) {
                    result.push_back("false");
                } else {
                    buffer[tail] = stoi(op_data[1]);
                    tail = (tail + 1) % k;
                    count++;
                    result.push_back("true");
                }
            } else if (cmd == "ENQ_OVR") {
                int val = stoi(op_data[1]);
                if (count == k) {
                    int overwrittenVal = buffer[head];
                    head = (head + 1) % k;
                    buffer[tail] = val;
                    tail = (tail + 1) % k;
                    result.push_back(to_string(overwrittenVal));
                } else {
                    buffer[tail] = val;
                    tail = (tail + 1) % k;
                    count++;
                    result.push_back("NONE");
                }
            } else if (cmd == "DEQ") {
                if (count == 0) {
                    result.push_back("EMPTY");
                } else {
                    result.push_back(to_string(buffer[head]));
                    head = (head + 1) % k;
                    count--;
                }
            } else if (cmd == "FRONT") {
                if (count == 0) result.push_back("EMPTY");
                else result.push_back(to_string(buffer[head]));
            } else if (cmd == "REAR") {
                if (count == 0) result.push_back("EMPTY");
                else {
                    int idx = (tail - 1 + k) % k;
                    result.push_back(to_string(buffer[idx]));
                }
            } else if (cmd == "ISEMPTY") {
                result.push_back(count == 0 ? "true" : "false");
            } else if (cmd == "ISFULL") {
                result.push_back(count == k ? "true" : "false");
            }
        }
        return result;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int k, m;
    if (cin >> k >> m) {
        vector<vector<string>> operations;
        operations.reserve(m);
        for (int i = 0; i < m; i++) {
            string op;
            cin >> op;
            if (op == "ENQ" || op == "ENQ_OVR") {
                string val;
                cin >> val;
                operations.push_back({op, val});
            } else {
                operations.push_back({op});
            }
        }
    
        Solution solution;
        vector<string> result = solution.processOperations(k, operations);
        for (const string& line : result) {
            cout << line << "\n";
        }
    }
    return 0;
}
```

### JavaScript

```javascript
const readline = require("readline");

class Solution {
  processOperations(k, operations) {
    const buffer = new Int32Array(k);
    let head = 0;
    let tail = 0;
    let count = 0;
    const result = [];
    
    for (const opData of operations) {
      const cmd = opData[0];
      
      if (cmd === "ENQ") {
        if (count === k) {
          result.push("false");
        } else {
          buffer[tail] = parseInt(opData[1], 10);
          tail = (tail + 1) % k;
          count++;
          result.push("true");
        }
      } else if (cmd === "ENQ_OVR") {
        const val = parseInt(opData[1], 10);
        if (count === k) {
          const overwrittenVal = buffer[head];
          head = (head + 1) % k;
          buffer[tail] = val;
          tail = (tail + 1) % k;
          result.push(String(overwrittenVal));
        } else {
          buffer[tail] = val;
          tail = (tail + 1) % k;
          count++;
          result.push("NONE");
        }
      } else if (cmd === "DEQ") {
        if (count === 0) {
          result.push("EMPTY");
        } else {
          result.push(String(buffer[head]));
          head = (head + 1) % k;
          count--;
        }
      } else if (cmd === "FRONT") {
        if (count === 0) result.push("EMPTY");
        else result.push(String(buffer[head]));
      } else if (cmd === "REAR") {
        if (count === 0) result.push("EMPTY");
        else {
          const idx = (tail - 1 + k) % k;
          result.push(String(buffer[idx]));
        }
      } else if (cmd === "ISEMPTY") {
        result.push(count === 0 ? "true" : "false");
      } else if (cmd === "ISFULL") {
        result.push(count === k ? "true" : "false");
      }
    }
    return result;
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

let data = [];
rl.on("line", (line) => data.push(...line.trim().split(/\s+/).filter(x => x !== "")));
rl.on("close", () => {
  if (data.length === 0) return;
  let idx = 0;
  const k = parseInt(data[idx++], 10);
  const m = parseInt(data[idx++], 10);
  const operations = [];

  for (let i = 0; i < m; i++) {
    const op = data[idx++];
    if (op === "ENQ" || op === "ENQ_OVR") {
      const x = data[idx++];
      operations.push([op, x]);
    } else {
      operations.push([op]);
    }
  }

  const solution = new Solution();
  const result = solution.processOperations(k, operations);
  console.log(result.join("\n"));
});
```

## 🧪 Test Case Walkthrough (Dry Run)

Input: `k=2`
1. `ENQ 5`: `[5, _]`, count=1. Output `true`.
2. `ENQ 6`: `[5, 6]`, count=2. Output `true`.
3. `ENQ 7`: Full. Output `false`.
4. `ENQ_OVR 8`: Full. Overwrite `5`. `head` moves to `6`. `[8, 6]`. `tail` moves to `5`'s old spot. Queue: `6 -> 8`. Output `overwritten`.
5. `FRONT`: Head is `6`. Output `6`.
6. `REAR`: Tail-1 is `8`. Output `8`.

Output matches example.

![Example Visualization](../images/QUE-002/example-1.png)

## ✅ Proof of Correctness

### Invariant
`count` always reflects the number of valid elements. `head` points to the oldest, `tail` to the next insertion slot. `ENQ_OVR` maintains capacity constraint by sacrificing `head`.

### Why the approach is correct
Modulo arithmetic correctly handles the circular wrapping of indices.

## 💡 Interview Extensions (High-Value Add-ons)

- **Extension 1:** Thread Safety?
  - *Hint:* Circular buffers are popular in producer-consumer problems. Use atomic indices or locks to make it thread-safe.
- **Extension 2:** Resizable Circular Buffer?
  - *Hint:* When full, allocate array of size `2k`, copy elements (unwrapping them), and reset head/tail.

### Common Mistakes to Avoid

1. **Tail Calculation**
   - ❌ Wrong: `tail - 1` without modulo for `REAR`.
   - ✅ Correct: `(tail - 1 + k) % k` to handle wrap-around when `tail` is 0.
2. **Full/Empty Confusion**
   - ❌ Wrong: `head == tail` means empty OR full.
   - ✅ Correct: Use `count` variable or keep one slot open to distinguish.

## Related Concepts

- **Ring Buffer:** Another name for this structure.
- **Deque:** Double-ended queue (can add/remove from both ends).
