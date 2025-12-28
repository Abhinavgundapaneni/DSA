import heapq

class Task:
    def __init__(self, name, count, priority):
        self.name = name
        self.count = count
        self.priority = priority
        self.ready_time = 0
        self.interrupted = False  # Track if already interrupted
        
    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority > other.priority
        return self.count > other.count

def min_slots_no_stack(tasks_data, k):
    """Version where interrupts don't stack"""
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
                t.interrupted = False  # Reset when it becomes ready
                heapq.heappush(ready_queue, t)
            else:
                next_cooldown.append(t)
        cooldown_list = next_cooldown
        
        if not ready_queue:
            continue
            
        current = heapq.heappop(ready_queue)
        current.count -= 1
        total_tasks -= 1
        
        # Apply interrupts only to non-interrupted tasks
        for t in cooldown_list:
            if t.priority < current.priority and not t.interrupted:
                t.ready_time = max(t.ready_time, time + k + 1)
                t.interrupted = True  # Mark as interrupted
                
        if current.count > 0:
            current.ready_time = time + k + 1
            current.interrupted = False
            cooldown_list.append(current)
            
    return time

# Test
result = min_slots_no_stack([('A', 13, 2), ('B', 11, 2), ('C', 18, 1)], 8)
print(f"No stacking interrupts: {result}")
print(f"Expected: 245")
