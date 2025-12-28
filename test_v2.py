import heapq

def solve_grd012_v2(tasks, k):
    """Version 2: Don't interrupt the task just added to cooldown."""
    
    # Ready queue: max-heap by (-priority, -count)
    ready_queue = []
    for task, count, priority in tasks:
        heapq.heappush(ready_queue, (-priority, -count, task, count))
    
    # Cooldown list: (ready_time, priority, count, task)
    cooldown_list = []
    
    time = 0
    total_tasks = sum(count for _, count, _ in tasks)
    
    while total_tasks > 0:
        time += 1
        
        # Move tasks from cooldown to ready if ready_time <= time
        new_cooldown = []
        for ready_time, priority, count, task in cooldown_list:
            if ready_time <= time:
                heapq.heappush(ready_queue, (-priority, -count, task, count))
            else:
                new_cooldown.append((ready_time, priority, count, task))
        cooldown_list = new_cooldown
        
        if not ready_queue:
            continue
        
        # Execute highest priority task
        neg_pri, neg_cnt, task, count = heapq.heappop(ready_queue)
        priority = -neg_pri
        
        total_tasks -= 1
        count -= 1
        
        if count > 0:
            # First apply interrupts to existing tasks in cooldown
            new_cooldown2 = []
            for rt, p, c, t in cooldown_list:
                if p < priority:
                    rt = max(rt, time + k + 1)
                new_cooldown2.append((rt, p, c, t))
            cooldown_list = new_cooldown2
            
            # Then add current task to cooldown (NOT interrupted by itself)
            ready_time = time + k + 1
            cooldown_list.append((ready_time, priority, count, task))
    
    return time

# Test
tasks = [('A', 13, 2), ('B', 11, 2), ('C', 18, 1)]
k = 8
result = solve_grd012_v2(tasks, k)
print(f"Version 2: {result}")
print(f"Expected: 245")
