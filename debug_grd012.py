import heapq

def solve_grd012_debug(tasks, k):
    """Min time with cooldown and priority interrupts - Simulation with debug."""
    
    # Ready queue: max-heap by (-priority, -count)
    ready_queue = []
    for task, count, priority in tasks:
        heapq.heappush(ready_queue, (-priority, -count, task, count))
    
    # Cooldown list: (ready_time, priority, count, task)
    cooldown_list = []
    
    time = 0
    total_tasks = sum(count for _, count, _ in tasks)
    
    print(f"\n=== STARTING SIMULATION ===")
    print(f"Tasks: {tasks}, k={k}")
    print(f"Total tasks to complete: {total_tasks}\n")
    
    while total_tasks > 0:
        time += 1
        
        print(f"\n--- Time {time} ---")
        
        # Move tasks from cooldown to ready if ready_time <= time
        new_cooldown = []
        for ready_time, priority, count, task in cooldown_list:
            if ready_time <= time:
                print(f"  Moving {task}(P{priority}, count={count}) from cooldown to ready")
                heapq.heappush(ready_queue, (-priority, -count, task, count))
            else:
                new_cooldown.append((ready_time, priority, count, task))
        cooldown_list = new_cooldown
        
        print(f"  Ready queue: {ready_queue}")
        print(f"  Cooldown list: {cooldown_list}")
        
        if not ready_queue:
            print(f"  IDLE (no tasks ready)")
            continue
        
        # Execute highest priority task
        neg_pri, neg_cnt, task, count = heapq.heappop(ready_queue)
        priority = -neg_pri
        
        print(f"  EXEC {task}(P{priority}, count={count})")
        
        total_tasks -= 1
        count -= 1
        
        if count > 0:
            # Add to cooldown
            ready_time = time + k + 1
            print(f"    {task} has {count} left, will be ready at time {ready_time}")
            cooldown_list.append((ready_time, priority, count, task))
            
            # Apply interrupts to lower priority tasks
            print(f"    Applying interrupts to lower priority tasks...")
            new_cooldown2 = []
            for rt, p, c, t in cooldown_list:
                old_rt = rt
                if p < priority:
                    rt = max(rt, time + k + 1)
                    if rt != old_rt:
                        print(f"      {t}(P{p}): ready time {old_rt} -> {rt} (interrupted)")
                else:
                    print(f"      {t}(P{p}): ready time {rt} (no interrupt, P{p} >= P{priority})")
                new_cooldown2.append((rt, p, c, t))
            cooldown_list = new_cooldown2
        
        print(f"  Tasks remaining: {total_tasks}")
    
    print(f"\n=== SIMULATION COMPLETE ===")
    print(f"Total time: {time}\n")
    return time

# Test the failing case
tasks = [('A', 13, 2), ('B', 11, 2), ('C', 18, 1)]
k = 8
result = solve_grd012_debug(tasks, k)
print(f"Result: {result}")
print(f"Expected: 245")
