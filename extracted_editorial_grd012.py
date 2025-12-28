import heapq
import sys

class Task:
    def __init__(self, name, count, priority):
        self.name = name
        self.count = count
        self.priority = priority
        self.ready_time = 0
        
    # For heap: High priority first, then High count
    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority > other.priority
        return self.count > other.count

def min_slots(tasks_data: list, k: int) -> int:
    ready_queue = []
    for name, count, priority in tasks_data:
        heapq.heappush(ready_queue, Task(name, count, priority))
        
    cooldown_list = []
    time = 0
    total_tasks = sum(t[1] for t in tasks_data)
    
    while total_tasks > 0:
        time += 1
        
        # Move ready tasks
        # We must iterate a copy or build a new list because we modify cooldown_list
        next_cooldown = []
        for t in cooldown_list:
            if t.ready_time <= time:
                heapq.heappush(ready_queue, t)
            else:
                next_cooldown.append(t)
        cooldown_list = next_cooldown
        
        if not ready_queue:
            continue
            
        current = heapq.heappop(ready_queue)
        current.count -= 1
        total_tasks -= 1
        
        # Apply Interrupts
        for t in cooldown_list:
            if t.priority < current.priority:
                t.ready_time = max(t.ready_time, time + k + 1)
                
        if current.count > 0:
            current.ready_time = time + k + 1
            cooldown_list.append(current)
            
    return time

def main():
    data = sys.stdin.read()
    data = data.split()
    if not data:
        return
        
    idx = 0
    n = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1
    
    tasks = []
    for _ in range(n):
        name = data[idx]; idx += 1
        count = int(data[idx])
        idx += 1
        priority = int(data[idx])
        idx += 1
        tasks.append((name, count, priority))

    result = min_slots(tasks, k)
    print(result)

if __name__ == "__main__":
    main()
