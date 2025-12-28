import sys
sys.path.insert(0, r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA')

# Import just the function (not main)
import heapq

class Task:
    def __init__(self, name, count, priority):
        self.name = name
        self.count = count
        self.priority = priority
        self.ready_time = 0
        
    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority > other.priority
        return self.count > other.count

def min_slots(tasks_data, k):
    ready_queue = []
    for name, count, priority in tasks_data:
        heapq.heappush(ready_queue, Task(name, count, priority))
        
    cooldown_list = []
    time = 0
    total_tasks = sum(t[1] for t in tasks_data)
    
    iteration = 0
    while total_tasks > 0:
        time += 1
        iteration += 1
        
        if iteration <= 25:  # Only trace first 25 iterations
            print(f"\nTime {time}:")
        
        next_cooldown = []
        for t in cooldown_list:
            if t.ready_time <= time:
                if iteration <= 25:
                    print(f"  {t.name}(P{t.priority}) ready")
                heapq.heappush(ready_queue, t)
            else:
                next_cooldown.append(t)
        cooldown_list = next_cooldown
        
        if not ready_queue:
            if iteration <= 25:
                print(f"  IDLE")
            continue
            
        current = heapq.heappop(ready_queue)
        if iteration <= 25:
            print(f"  Execute {current.name}(P{current.priority}, count={current.count})")
        current.count -= 1
        total_tasks -= 1
        
        # Apply Interrupts
        for t in cooldown_list:
            if t.priority < current.priority:
                old_rt = t.ready_time
                t.ready_time = max(t.ready_time, time + k + 1)
                if iteration <= 25 and old_rt != t.ready_time:
                    print(f"    Interrupt {t.name}(P{t.priority}): {old_rt} -> {t.ready_time}")
                
        if current.count > 0:
            current.ready_time = time + k + 1
            cooldown_list.append(current)
            if iteration <= 25:
                print(f"    Added {current.name} to cooldown, ready at {current.ready_time}")
            
    return time

# Test
result = min_slots([('A', 13, 2), ('B', 11, 2), ('C', 18, 1)], 8)
print(f"Editorial code result: {result}, expected: 245")
