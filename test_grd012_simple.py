import heapq

def solve_grd012(tasks, k):
    """Min time with cooldown and priority interrupts - Simulation."""
    
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
            # Idle slot
            continue
        
        # Execute highest priority task
        neg_pri, neg_cnt, task, count = heapq.heappop(ready_queue)
        priority = -neg_pri
        
        total_tasks -= 1
        count -= 1
        
        if count > 0:
            # Add to cooldown
            ready_time = time + k + 1
            cooldown_list.append((ready_time, priority, count, task))
            
            # Apply interrupts to lower priority tasks
            new_cooldown2 = []
            for rt, p, c, t in cooldown_list:
                if p < priority:
                    rt = max(rt, time + k + 1)
                new_cooldown2.append((rt, p, c, t))
            cooldown_list = new_cooldown2
    
    return time

# Test sample from problem
tasks = [('A', 3, 2), ('B', 2, 1)]
k = 1
result = solve_grd012(tasks, k)
print(f"Sample test: tasks={tasks}, k={k}")
print(f"Result: {result}")
print(f"Expected: 7")
print()

# Test the failing case
tasks = [('A', 13, 2), ('B', 11, 2), ('C', 18, 1)]
k = 8
result = solve_grd012(tasks, k)
print(f"Failing test: k={k}, A(13,P2), B(11,P2), C(18,P1)")
print(f"Result: {result}")
print(f"Expected: 245")
