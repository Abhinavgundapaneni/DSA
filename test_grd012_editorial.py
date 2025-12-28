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
        
        for t in cooldown_list:
            if t.priority < current.priority:
                t.ready_time = max(t.ready_time, time + k + 1)
                
        if current.count > 0:
            current.ready_time = time + k + 1
            cooldown_list.append(current)
            
    return time

# Test case: public[1]
tasks = [('A', 13, 2), ('B', 11, 2), ('C', 18, 1)]
k = 8
result = min_slots(tasks, k)
print(f"Result: {result}")
print(f"Expected: 245")
