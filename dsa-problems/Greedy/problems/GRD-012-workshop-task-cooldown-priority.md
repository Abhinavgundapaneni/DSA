---
problem_id: GRD_WORKSHOP_TASK_COOLDOWN_PRIORITY__7539
display_id: GRD-012
slug: workshop-task-cooldown-priority
title: "Workshop Task Cooldown with Priority Interrupts"
difficulty: Medium
difficulty_score: 60
topics:
  - Greedy Algorithms
  - Heap
  - Priority Queue
  - Scheduling
tags:
  - greedy
  - heap
  - priority-queue
  - scheduling
  - hard
premium: true
subscription_tier: basic
time_limit: 2000
memory_limit: 256
---

# GRD-012: Workshop Task Cooldown with Priority Interrupts

## Problem Statement

You have tasks labeled A-Z with counts `c[i]` and priority levels `p[i]` in {1, 2, 3} where higher numbers indicate higher priority.

**Cooldown rule**: Between two identical tasks, at least `k` different tasks must be executed.

**Priority interrupt rule**: When a higher-priority task is scheduled, it resets the cooldown counter for all lower-priority tasks currently in cooldown. This means lower-priority tasks must wait an additional `k` slots from when the high-priority task runs.

**Idle slots**: If no task can be scheduled (all available tasks are in cooldown), insert an idle slot (costs 1 time unit).

Your goal is to minimize the total time slots (including idle slots) needed to complete all tasks.

![Problem Illustration](../images/GRD-012/problem-illustration.png)

## Input Format

- First line: two integers `n k` (number of task types and cooldown period)
- Next `n` lines: character `task`, integer `count`, integer `priority` representing each task type

## Output Format

- Single integer: minimum total time slots needed

## Constraints

- `1 <= n <= 26`
- `1 <= total tasks <= 10^5`
- `0 <= k <= 10^5`
- `1 <= priority <= 3`
- Tasks are uppercase letters A-Z

## Example

**Input:**

```
2 1
A 3 2
B 2 1
```

**Output:**

```
7
```

**Explanation:**

Tasks:

- Task A: count=3, priority=2 (higher priority)
- Task B: count=2, priority=1 (lower priority)

Cooldown k=1 (after executing a task, it becomes ready again at time + k + 1)

Schedule:

- Slot 1: Execute A (2 remaining) → A ready at slot 3
- Slot 2: Execute B (1 remaining) → B ready at slot 4
- Slot 3: Execute A (1 remaining) → Interrupt: B's ready time reset to max(4, 3+1+1) = 5 → A ready at slot 5
- Slot 4: IDLE (B not ready until slot 5)
- Slot 5: Execute A (0 remaining) → Interrupt: B's ready time reset to max(5, 5+1+1) = 7
- Slot 6: IDLE (B not ready until slot 7)
- Slot 7: Execute B (0 remaining) → Done

Total: 5 tasks completed in 7 time slots.

![Example Visualization](../images/GRD-012/example-1.png)

## Notes

- Use a max-heap ordered by (priority, remaining count)
- Maintain a cooldown queue with (task, ready_time, priority)
- When scheduling a high-priority task, increment ready_time for all lower-priority tasks in cooldown
- Time complexity: O(T log n) where T is total time slots

## Related Topics

Greedy Algorithms, Heap, Priority Queue, Task Scheduling, Cooldown Management

---

## Solution Template

### Java

```java
import java.util.*;

class Solution {
    public int minSlots(List<Task> tasks, int k) {
        // Task has: char name, int count, int priority
        // Your implementation here
        return 0;
    }
}

class Task {
    char name;
    int count;
    int priority;

    Task(char name, int count, int priority) {
        this.name = name;
        this.count = count;
        this.priority = priority;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int k = sc.nextInt();

        List<Task> tasks = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            char name = sc.next().charAt(0);
            int count = sc.nextInt();
            int priority = sc.nextInt();
            tasks.add(new Task(name, count, priority));
        }

        Solution solution = new Solution();
        System.out.println(solution.minSlots(tasks, k));
        sc.close();
    }
}
```

### Python

```python
from typing import List, Tuple
import heapq

def min_slots(tasks: List[Tuple[str, int, int]], k: int) -> int:
    # tasks[i] = (name, count, priority)
    # Your implementation here
    return 0

def main():
    n, k = map(int, input().split())
    tasks = []
    for _ in range(n):
        parts = input().split()
        name = parts[0]
        count = int(parts[1])
        priority = int(parts[2])
        tasks.append((name, count, priority))

    result = min_slots(tasks, k)
    print(result)

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

struct Task {
    char name;
    int count;
    int priority;
};

class Solution {
public:
    int minSlots(vector<Task>& tasks, int k) {
        // Your implementation here
        return 0;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    vector<Task> tasks(n);
    for (int i = 0; i < n; i++) {
        cin >> tasks[i].name >> tasks[i].count >> tasks[i].priority;
    }

    Solution solution;
    cout << solution.minSlots(tasks, k) << "\n";

    return 0;
}
```

### JavaScript

```javascript
const readline = require("readline");

class Solution {
  minSlots(tasks, k) {
    // tasks[i] = {name, count, priority}
    // Your implementation here
    return 0;
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

let data = [];
rl.on("line", (line) => data.push(line.trim()));
rl.on("close", () => {
  let ptr = 0;
  const [n, k] = data[ptr++].split(" ").map(Number);

  const tasks = [];
  for (let i = 0; i < n; i++) {
    const parts = data[ptr++].split(" ");
    const name = parts[0];
    const count = parseInt(parts[1]);
    const priority = parseInt(parts[2]);
    tasks.push({ name, count, priority });
  }

  const solution = new Solution();
  console.log(solution.minSlots(tasks, k));
});
```
