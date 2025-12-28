import heapq

class Task:
    def __init__(self, name, count, priority):
        self.name = name
        self.count = count
        self.priority = priority
        self.ready_time = 0
        
    def __lt__(self, other):
        # Sort by COUNT first, then priority
        if self.count != other.count:
            return self.count > other.count  # Higher count first
        return self.priority > other.priority

def min_slots_count_first(tasks_data, k):
    """Version that prioritizes count over priority"""
    ready_queue = []
    for name, count, priority in tasks_data:
        heapq.heappush(ready_queue, Task(name, count, priority))
        
    cooldown_list = []
    time = 0
    total_tasks = sum(t[1] for t in tasks_data)
    
    while total_tasks > 0:
        time += 1
        
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
        
        # Apply interrupts
        for t in cooldown_list:
            if t.priority < current.priority:
                t.ready_time = max(t.ready_time, time + k + 1)
                
        if current.count > 0:
            current.ready_time = time + k + 1
            cooldown_list.append(current)
            
    return time

# Test
result = min_slots_count_first([('A', 13, 2), ('B', 11, 2), ('C', 18, 1)], 8)
print(f"Count first: {result}")
print(f"Expected: 245")
