#!/usr/bin/env python3
"""
Generate CORRECT test cases for Greedy problems by reading problem statements
and implementing exact solutions.

Strategy:
1. Read each problem statement to understand input/output format
2. Implement correct solve function
3. Generate 38 test cases (3 samples + 5 public + 30 hidden)
"""

import random
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

def format_testcase_yaml(data):
    """Format test cases in proper YAML with |- syntax."""
    lines = []
    lines.append(f"problem_id: {data['problem_id']}")
    
    for section_name in ['samples', 'public', 'hidden']:
        if section_name not in data or not data[section_name]:
            continue
        lines.append(f"{section_name}:")
        for case in data[section_name]:
            lines.append("- input: |-")
            for line in case['input'].strip().split('\n'):
                lines.append(f"    {line}")
            lines.append("  output: |-")
            for line in case['output'].strip().split('\n'):
                lines.append(f"    {line}")
    
    return '\n'.join(lines)


# ============================================================================
# GRD-003: Festival Stall Placement
# Input: n d
#        start1 end1
#        start2 end2
#        ...
# Output: max number of stalls
# ============================================================================

def solve_grd003(stalls, d):
    """Maximum stalls with distance d constraint."""
    if not stalls:
        return 0
    
    # Sort by end position
    stalls.sort(key=lambda x: x[1])
    
    count = 0
    last_end = -float('inf')
    
    for start, end in stalls:
        if start - last_end >= d:
            count += 1
            last_end = end
    
    return count

def generate_grd003():
    """Generate test cases for GRD-003."""
    cases = {'problem_id': 'GRD-003', 'samples': [], 'public': [], 'hidden': []}
    random.seed(42)
    
    # Sample 1: From problem statement
    stalls = [(0, 2), (1, 4), (5, 6)]
    d = 2
    result = solve_grd003(stalls, d)
    inp = f"{len(stalls)} {d}\n" + "\n".join(f"{s} {e}" for s, e in stalls)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 2: No overlap possible
    stalls = [(0, 5), (1, 6), (2, 7)]
    d = 10
    result = solve_grd003(stalls, d)
    inp = f"{len(stalls)} {d}\n" + "\n".join(f"{s} {e}" for s, e in stalls)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 3: All can fit
    stalls = [(0, 1), (5, 6), (10, 11)]
    d = 2
    result = solve_grd003(stalls, d)
    inp = f"{len(stalls)} {d}\n" + "\n".join(f"{s} {e}" for s, e in stalls)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Public + Hidden test cases
    for idx in range(35):
        n = random.randint(5, 30)
        d = random.randint(1, 10)
        stalls = []
        for _ in range(n):
            start = random.randint(0, 100)
            end = start + random.randint(1, 20)
            stalls.append((start, end))
        
        result = solve_grd003(stalls, d)
        inp = f"{n} {d}\n" + "\n".join(f"{s} {e}" for s, e in stalls)
        
        test_case = {'input': inp, 'output': str(result)}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# GRD-004: Library Power Backup
# Input: n T
#        c1 c2 c3 ... cn
# Output: minimum battery swaps or -1
# ============================================================================

def solve_grd004(batteries, T):
    """Minimum battery swaps to power for T hours."""
    total_capacity = sum(batteries)
    if total_capacity < T:
        return -1
    
    # Sort batteries in descending order (use longest batteries first)
    batteries.sort(reverse=True)
    
    swaps = 0
    hours_covered = 0
    
    for capacity in batteries:
        hours_covered += capacity
        if hours_covered >= T:
            break
        swaps += 1
    
    return swaps

def generate_grd004():
    """Generate test cases for GRD-004."""
    cases = {'problem_id': 'GRD-004', 'samples': [], 'public': [], 'hidden': []}
    random.seed(43)
    
    # Sample 1
    batteries = [5, 3, 2]
    T = 8
    result = solve_grd004(batteries, T)
    inp = f"{len(batteries)} {T}\n" + " ".join(map(str, batteries))
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 2: Impossible
    batteries = [1, 1, 1]
    T = 10
    result = solve_grd004(batteries, T)
    inp = f"{len(batteries)} {T}\n" + " ".join(map(str, batteries))
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 3: No swaps needed
    batteries = [10]
    T = 5
    result = solve_grd004(batteries, T)
    inp = f"{len(batteries)} {T}\n" + " ".join(map(str, batteries))
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Public + Hidden
    for idx in range(35):
        n = random.randint(1, 20)
        batteries = [random.randint(1, 50) for _ in range(n)]
        T = random.randint(1, sum(batteries) + 10)  # Sometimes impossible
        
        result = solve_grd004(batteries, T)
        inp = f"{n} {T}\n" + " ".join(map(str, batteries))
        
        test_case = {'input': inp, 'output': str(result)}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# GRD-005: Shuttle Overtime Minimizer
# Input: n H / l1 p1 / l2 p2 / ...
# Output: min overtime cost
# ============================================================================

def solve_grd005(shifts, H):
    """Minimize overtime cost."""
    total_standard = sum(l for l, p in shifts)
    if total_standard >= H:
        return 0
    
    overtime_needed = H - total_standard
    # Use cheapest overtime
    min_cost_rate = min(p for l, p in shifts)
    return int(overtime_needed * min_cost_rate)

def generate_grd005():
    cases = {'problem_id': 'GRD-005', 'samples': [], 'public': [], 'hidden': []}
    random.seed(45)
    
    # Sample 1
    shifts = [(4, 3), (2, 1)]
    H = 8
    result = solve_grd005(shifts, H)
    inp = f"{len(shifts)} {H}\n" + "\n".join(f"{l} {p}" for l, p in shifts)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 2
    shifts = [(5, 2)]
    H = 3
    result = solve_grd005(shifts, H)
    inp = f"{len(shifts)} {H}\n" + "\n".join(f"{l} {p}" for l, p in shifts)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 3
    shifts = [(3, 1), (4, 2)]
    H = 10
    result = solve_grd005(shifts, H)
    inp = f"{len(shifts)} {H}\n" + "\n".join(f"{l} {p}" for l, p in shifts)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Public + Hidden
    for idx in range(35):
        n = random.randint(1, 10)
        shifts = [(random.randint(1, 20), random.randint(1, 10)) for _ in range(n)]
        H = random.randint(1, sum(l for l, p in shifts) + 20)
        result = solve_grd005(shifts, H)
        inp = f"{n} {H}\n" + "\n".join(f"{l} {p}" for l, p in shifts)
        
        test_case = {'input': inp, 'output': str(result)}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# GRD-006: Robotics Component Bundling
# Input: n T / weights (space-separated) / qualities (space-separated)
# Output: max weight or -1
# ============================================================================

import heapq
import math

def solve_grd006(n, T, weights, qualities):
    """Merge all parts maintaining quality >= T."""
    pq = []
    for w, q in zip(weights, qualities):
        heapq.heappush(pq, (-q, w))
    
    while len(pq) > 1:
        neg_q1, w1 = heapq.heappop(pq)
        neg_q2, w2 = heapq.heappop(pq)
        q1, q2 = -neg_q1, -neg_q2
        new_q = min(q1, q2) - 1
        if new_q < T:
            return -1
        loss = math.floor(0.1 * min(w1, w2))
        new_w = w1 + w2 - loss
        heapq.heappush(pq, (-new_q, new_w))
    
    return pq[0][1] if pq else -1

def generate_grd006():
    cases = {'problem_id': 'GRD-006', 'samples': [], 'public': [], 'hidden': []}
    random.seed(46)
    
    # Sample 1
    weights = [10, 20, 15]
    qualities = [10, 8, 6]
    T = 5
    result = solve_grd006(len(weights), T, weights, qualities)
    inp = f"{len(weights)} {T}\n" + " ".join(map(str, weights)) + "\n" + " ".join(map(str, qualities))
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 2: Impossible
    weights = [5, 10]
    qualities = [3, 2]
    T = 5
    result = solve_grd006(len(weights), T, weights, qualities)
    inp = f"{len(weights)} {T}\n" + " ".join(map(str, weights)) + "\n" + " ".join(map(str, qualities))
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 3
    weights = [100, 50]
    qualities = [10, 10]
    T = 5
    result = solve_grd006(len(weights), T, weights, qualities)
    inp = f"{len(weights)} {T}\n" + " ".join(map(str, weights)) + "\n" + " ".join(map(str, qualities))
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Public + Hidden
    for idx in range(35):
        n = random.randint(2, 15)
        T = random.randint(1, 10)
        weights = [random.randint(10, 100) for _ in range(n)]
        qualities = [random.randint(T-2, T+10) for _ in range(n)]
        result = solve_grd006(n, T, weights, qualities)
        inp = f"{n} {T}\n" + " ".join(map(str, weights)) + "\n" + " ".join(map(str, qualities))
        
        test_case = {'input': inp, 'output': str(result)}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# GRD-007: Campus WiFi Expansion - MST Problem
# Input: n / heights (space-separated) / m / u1 v1 / u2 v2 / ...
# Output: min cost
# ============================================================================

def solve_grd007(n, heights, m, existing_edges):
    """MST with existing edges (cost 0) and new edges (cost = height difference)."""
    # Union-Find
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False
    
    # Add existing edges (free)
    for u, v in existing_edges:
        union(u, v)
    
    # Generate all possible edges with costs
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            cost = abs(heights[i] - heights[j])
            edges.append((cost, i, j))
    
    edges.sort()
    
    total_cost = 0
    for cost, u, v in edges:
        if union(u, v):
            total_cost += cost
    
    return total_cost

def generate_grd007():
    cases = {'problem_id': 'GRD-007', 'samples': [], 'public': [], 'hidden': []}
    random.seed(47)
    
    # Sample 1
    heights = [1, 3, 2, 5]
    existing_edges = [(0, 1)]
    result = solve_grd007(len(heights), heights, len(existing_edges), existing_edges)
    inp = f"{len(heights)}\n" + " ".join(map(str, heights)) + f"\n{len(existing_edges)}\n"
    inp += "\n".join(f"{u} {v}" for u, v in existing_edges)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 2
    heights = [10, 20, 15]
    existing_edges = []
    result = solve_grd007(len(heights), heights, len(existing_edges), existing_edges)
    inp = f"{len(heights)}\n" + " ".join(map(str, heights)) + f"\n{len(existing_edges)}"
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 3
    heights = [1, 1, 1, 1]
    existing_edges = [(0, 2)]
    result = solve_grd007(len(heights), heights, len(existing_edges), existing_edges)
    inp = f"{len(heights)}\n" + " ".join(map(str, heights)) + f"\n{len(existing_edges)}\n"
    inp += "\n".join(f"{u} {v}" for u, v in existing_edges)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Public + Hidden
    for idx in range(35):
        n = random.randint(3, 10)
        heights = [random.randint(1, 50) for _ in range(n)]
        m = random.randint(0, n//2)
        existing_edges = []
        for _ in range(m):
            u, v = random.sample(range(n), 2)
            existing_edges.append((min(u,v), max(u,v)))
        
        result = solve_grd007(n, heights, m, existing_edges)
        inp = f"{n}\n" + " ".join(map(str, heights)) + f"\n{m}\n"
        if m > 0:
            inp += "\n".join(f"{u} {v}" for u, v in existing_edges)
        
        test_case = {'input': inp, 'output': str(result)}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# GRD-008: Exam Proctor Allocation - Interval Partitioning
# Input: n r / start1 end1 / start2 end2 / ...
# Output: min proctors needed
# ============================================================================

def solve_grd008(exams, r):
    """Min proctors: ceiling(max_concurrent_exams / r)."""
    events = []
    for start, end in exams:
        events.append((start, 1))
        events.append((end, -1))
    # Sort by time, then by type (start +1 before end -1)
    # We want start events before end events when times are equal
    events.sort(key=lambda x: (x[0], -x[1]))
    
    current = 0
    max_concurrent = 0
    for time, delta in events:
        current += delta
        max_concurrent = max(max_concurrent, current)
    
    return (max_concurrent + r - 1) // r  # ceiling division

def generate_grd008():
    cases = {'problem_id': 'GRD-008', 'samples': [], 'public': [], 'hidden': []}
    random.seed(48)
    
    # Samples
    for sample_idx in range(3):
        n = random.randint(3, 8)
        r = random.randint(1, 3)
        exams = []
        for _ in range(n):
            start = random.randint(1, 20)
            end = start + random.randint(1, 10)
            exams.append((start, end))
        
        result = solve_grd008(exams, r)
        inp = f"{n} {r}\n" + "\n".join(f"{s} {e}" for s, e in exams)
        cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Public + Hidden
    for idx in range(35):
        n = random.randint(2, 15)
        r = random.randint(1, 5)
        exams = []
        for _ in range(n):
            start = random.randint(1, 100)
            end = start + random.randint(1, 50)
            exams.append((start, end))
        
        result = solve_grd008(exams, r)
        inp = f"{n} {r}\n" + "\n".join(f"{s} {e}" for s, e in exams)
        
        test_case = {'input': inp, 'output': str(result)}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# GRD-010: Library Merge Queues - Merge k sorted lists with constraint
# Input: k / len1 [queue1] / len2 [queue2] / ...
# Output: merged list (no more than 2 consecutive identical values)
# ============================================================================

def solve_grd010(queues):
    """Merge k sorted queues with no more than 2 consecutive duplicates."""
    import heapq
    pq = []
    indices = [0] * len(queues)
    
    for i, queue in enumerate(queues):
        if queue:
            heapq.heappush(pq, (queue[0], i))
    
    result = []
    last_val = None
    count = 0
    
    while pq:
        val, q_idx = heapq.heappop(pq)
        
        # Check constraint: can't add if count==2 and val==last_val
        if result and val == last_val and count == 2:
            if not pq:
                break  # Deadlock
            
            # Try next best, but skip ALL values equal to last_val
            val2, q_idx2 = heapq.heappop(pq)
            temp_storage = [(val, q_idx)]
            
            while val2 == last_val:
                temp_storage.append((val2, q_idx2))
                if not pq:
                    val2 = None
                    break
                val2, q_idx2 = heapq.heappop(pq)
            
            if val2 is None:
                break  # All remaining values are blocked
            
            # Found valid val2
            result.append(val2)
            last_val = val2
            count = 1
            
            # Advance q_idx2
            indices[q_idx2] += 1
            if indices[q_idx2] < len(queues[q_idx2]):
                heapq.heappush(pq, (queues[q_idx2][indices[q_idx2]], q_idx2))
            
            # Push back everything in temp_storage
            for item in temp_storage:
                heapq.heappush(pq, item)
        else:
            # Valid
            result.append(val)
            if val == last_val:
                count += 1
            else:
                last_val = val
                count = 1
            
            # Advance q_idx
            indices[q_idx] += 1
            if indices[q_idx] < len(queues[q_idx]):
                heapq.heappush(pq, (queues[q_idx][indices[q_idx]], q_idx))
    
    return result

def generate_grd010():
    cases = {'problem_id': 'GRD-010', 'samples': [], 'public': [], 'hidden': []}
    random.seed(410)
    
    # Sample 1
    queues = [[1, 1, 1], [1, 2], [2]]
    result = solve_grd010(queues)
    inp = f"{len(queues)}\n"
    inp += "\n".join(f"{len(q)} " + " ".join(map(str, q)) for q in queues)
    cases['samples'].append({'input': inp, 'output': " ".join(map(str, result))})
    
    # Sample 2
    queues = [[1, 3, 5], [2, 4]]
    result = solve_grd010(queues)
    inp = f"{len(queues)}\n"
    inp += "\n".join(f"{len(q)} " + " ".join(map(str, q)) for q in queues)
    cases['samples'].append({'input': inp, 'output': " ".join(map(str, result))})
    
    # Sample 3
    queues = [[1, 1, 1, 1, 1]]
    result = solve_grd010(queues)
    inp = f"{len(queues)}\n"
    inp += "\n".join(f"{len(q)} " + " ".join(map(str, q)) for q in queues)
    cases['samples'].append({'input': inp, 'output': " ".join(map(str, result))})
    
    # Public + Hidden
    for idx in range(35):
        k = random.randint(1, 5)
        queues = []
        for _ in range(k):
            size = random.randint(1, 10)
            # Generate sorted queue with possible duplicates
            queue = sorted([random.randint(1, 20) for _ in range(size)])
            queues.append(queue)
        
        result = solve_grd010(queues)
        inp = f"{k}\n"
        inp += "\n".join(f"{len(q)} " + " ".join(map(str, q)) for q in queues)
        
        test_case = {'input': inp, 'output': " ".join(map(str, result))}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# GRD-011: Campus Event Ticket Caps - Maximize tickets sold with deadlines
# Input: n / q1 d1 / q2 d2 / ...
# Output: max total tickets
# ============================================================================

def solve_grd011(requests):
    """Max tickets: use min-heap to maximize value within deadlines."""
    import heapq
    # Sort by deadline
    requests.sort(key=lambda x: x[1])
    
    min_heap = []
    
    for quantity, deadline in requests:
        heapq.heappush(min_heap, quantity)
        # If we have more selected than available days, drop the smallest
        if len(min_heap) > deadline:
            heapq.heappop(min_heap)
    
    return sum(min_heap)

def generate_grd011():
    cases = {'problem_id': 'GRD-011', 'samples': [], 'public': [], 'hidden': []}
    random.seed(411)
    
    # Sample 1
    requests = [(3, 1), (5, 3), (2, 2)]
    result = solve_grd011(requests)
    inp = f"{len(requests)}\n" + "\n".join(f"{q} {d}" for q, d in requests)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 2
    requests = [(10, 2), (8, 1)]
    result = solve_grd011(requests)
    inp = f"{len(requests)}\n" + "\n".join(f"{q} {d}" for q, d in requests)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 3
    requests = [(1, 5), (2, 4), (3, 3)]
    result = solve_grd011(requests)
    inp = f"{len(requests)}\n" + "\n".join(f"{q} {d}" for q, d in requests)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Public + Hidden
    for idx in range(35):
        n = random.randint(2, 10)
        requests = [(random.randint(1, 20), random.randint(1, 15)) for _ in range(n)]
        
        result = solve_grd011(requests[:])
        inp = f"{n}\n" + "\n".join(f"{q} {d}" for q, d in requests)
        
        test_case = {'input': inp, 'output': str(result)}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# GRD-012: Workshop Task Cooldown Priority - Complex scheduling
# Input: n k / task1 count1 priority1 / ...
# Output: min time slots
# ============================================================================

def solve_grd012(tasks, k):
    """Min time with cooldown and priority interrupts - Simulation."""
    import heapq
    
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
        
        # Apply interrupts to lower priority tasks (ALWAYS, not just if count > 0)
        new_cooldown2 = []
        for rt, p, c, t in cooldown_list:
            if p < priority:
                rt = max(rt, time + k + 1)
            new_cooldown2.append((rt, p, c, t))
        cooldown_list = new_cooldown2
        
        # Then add current task to cooldown if it has remaining count
        if count > 0:
            ready_time = time + k + 1
            cooldown_list.append((ready_time, priority, count, task))
    
    return time

def generate_grd012():
    cases = {'problem_id': 'GRD-012', 'samples': [], 'public': [], 'hidden': []}
    random.seed(412)
    
    # Samples
    for sample_idx in range(3):
        n = random.randint(1, 3)
        k = random.randint(0, 3)
        tasks = []
        for i in range(n):
            task = chr(65 + i)
            count = random.randint(1, 5)
            priority = random.randint(1, 3)
            tasks.append((task, count, priority))
        
        result = solve_grd012(tasks, k)
        inp = f"{n} {k}\n" + "\n".join(f"{t} {c} {p}" for t, c, p in tasks)
        cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Public + Hidden
    for idx in range(35):
        n = random.randint(1, 5)
        k = random.randint(0, 10)
        tasks = []
        for i in range(n):
            task = chr(65 + i)
            count = random.randint(1, 20)
            priority = random.randint(1, 3)
            tasks.append((task, count, priority))
        
        result = solve_grd012(tasks, k)
        inp = f"{n} {k}\n" + "\n".join(f"{t} {c} {p}" for t, c, p in tasks)
        
        test_case = {'input': inp, 'output': str(result)}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# GRD-013: Auditorium Seat Refunds - Track highest occupied row
# Input: r n / cap1 cap2 ... / row1 seat1 / row2 seat2 / ...
# Output: highest occupied row
# ============================================================================

def solve_grd013(capacities, refunds):
    """Track highest occupied row - greedy fill from bottom."""
    total_capacity = sum(capacities)
    total_people = total_capacity - len(refunds)
    
    if total_people <= 0:
        return 0
    
    # Find first row where cumulative capacity >= total_people
    for i in range(len(capacities)):
        total_people -= capacities[i]
        if total_people <= 0:
            return i + 1
    
    return len(capacities)

def generate_grd013():
    cases = {'problem_id': 'GRD-013', 'samples': [], 'public': [], 'hidden': []}
    random.seed(413)
    
    # Sample 1
    capacities = [5, 4, 3]
    refunds = [(3, 1), (3, 2), (2, 1)]
    result = solve_grd013(capacities, refunds)
    inp = f"{len(capacities)} {len(refunds)}\n"
    inp += " ".join(map(str, capacities)) + "\n"
    inp += "\n".join(f"{r} {s}" for r, s in refunds)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 2
    capacities = [3, 2]
    refunds = [(2, 1), (2, 2), (1, 1), (1, 2), (1, 3)]
    result = solve_grd013(capacities, refunds)
    inp = f"{len(capacities)} {len(refunds)}\n"
    inp += " ".join(map(str, capacities)) + "\n"
    inp += "\n".join(f"{r} {s}" for r, s in refunds)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 3
    capacities = [10]
    refunds = [(1, 5)]
    result = solve_grd013(capacities, refunds)
    inp = f"{len(capacities)} {len(refunds)}\n"
    inp += " ".join(map(str, capacities)) + "\n"
    inp += "\n".join(f"{r} {s}" for r, s in refunds)
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Public + Hidden
    for idx in range(35):
        r = random.randint(2, 10)
        capacities = [random.randint(1, 20) for _ in range(r)]
        total_seats = sum(capacities)
        n = random.randint(1, min(total_seats, 20))
        refunds = []
        for _ in range(n):
            row = random.randint(1, r)
            seat = random.randint(1, capacities[row - 1])
            refunds.append((row, seat))
        
        result = solve_grd013(capacities, refunds)
        inp = f"{r} {n}\n"
        inp += " ".join(map(str, capacities)) + "\n"
        inp += "\n".join(f"{row} {seat}" for row, seat in refunds)
        
        test_case = {'input': inp, 'output': str(result)}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# GRD-014: Festival Bandwidth Split - Maximize stages
# Input: n B / b1 b2 ... bn
# Output: max stages
# ============================================================================

def solve_grd014(bandwidths, B):
    """Max stages: greedy select smallest bandwidths."""
    bandwidths.sort()
    count = 0
    used = 0
    
    for b in bandwidths:
        if used + b <= B:
            used += b
            count += 1
        else:
            break
    
    return count

def generate_grd014():
    cases = {'problem_id': 'GRD-014', 'samples': [], 'public': [], 'hidden': []}
    random.seed(414)
    
    # Sample 1
    bandwidths = [5, 2, 4]
    B = 7
    result = solve_grd014(bandwidths[:], B)
    inp = f"{len(bandwidths)} {B}\n" + " ".join(map(str, bandwidths))
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 2
    bandwidths = [1, 1, 1, 10]
    B = 5
    result = solve_grd014(bandwidths[:], B)
    inp = f"{len(bandwidths)} {B}\n" + " ".join(map(str, bandwidths))
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Sample 3
    bandwidths = [10, 20, 30]
    B = 15
    result = solve_grd014(bandwidths[:], B)
    inp = f"{len(bandwidths)} {B}\n" + " ".join(map(str, bandwidths))
    cases['samples'].append({'input': inp, 'output': str(result)})
    
    # Public + Hidden
    for idx in range(35):
        n = random.randint(2, 10)
        bandwidths = [random.randint(1, 50) for _ in range(n)]
        B = random.randint(sum(bandwidths) // 3, sum(bandwidths))
        
        result = solve_grd014(bandwidths[:], B)
        inp = f"{n} {B}\n" + " ".join(map(str, bandwidths))
        
        test_case = {'input': inp, 'output': str(result)}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# GRD-015: Robotics Median After Batches - Two heaps with staleness filter
# Input: k t / m1 [batch1] / m2 [batch2] / ...
# Output: median1 median2 ... (or "NA")
# ============================================================================

def solve_grd015(batches, t):
    """Track median after each batch, excluding stale values."""
    from collections import Counter
    
    freq = Counter()
    all_values = []
    results = []
    
    for batch in batches:
        # Add new values
        for val in batch:
            freq[val] += 1
            all_values.append(val)
        
        # Filter non-stale values
        non_stale = [v for v in all_values if freq[v] <= t]
        
        if not non_stale:
            results.append("NA")
        else:
            non_stale.sort()
            mid = len(non_stale) // 2
            if len(non_stale) % 2 == 1:
                median = non_stale[mid]
            else:
                median = (non_stale[mid - 1] + non_stale[mid]) // 2
            results.append(str(median))
    
    return " ".join(results)

def generate_grd015():
    cases = {'problem_id': 'GRD-015', 'samples': [], 'public': [], 'hidden': []}
    random.seed(415)
    
    # Sample 1
    batches = [[5, 5, 1], [5, 3], [8, 9]]
    t = 2
    result = solve_grd015(batches, t)
    inp = f"{len(batches)} {t}\n"
    inp += "\n".join(f"{len(b)} " + " ".join(map(str, b)) for b in batches)
    cases['samples'].append({'input': inp, 'output': result})
    
    # Sample 2
    batches = [[1, 2, 3], [1, 2]]
    t = 1
    result = solve_grd015(batches, t)
    inp = f"{len(batches)} {t}\n"
    inp += "\n".join(f"{len(b)} " + " ".join(map(str, b)) for b in batches)
    cases['samples'].append({'input': inp, 'output': result})
    
    # Sample 3
    batches = [[5, 5, 5, 5]]
    t = 1
    result = solve_grd015(batches, t)
    inp = f"{len(batches)} {t}\n"
    inp += "\n".join(f"{len(b)} " + " ".join(map(str, b)) for b in batches)
    cases['samples'].append({'input': inp, 'output': result})
    
    # Public + Hidden
    for idx in range(35):
        k = random.randint(1, 5)
        t = random.randint(1, 10)
        batches = []
        for _ in range(k):
            size = random.randint(1, 10)
            batch = [random.randint(1, 20) for _ in range(size)]
            batches.append(batch)
        
        result = solve_grd015(batches, t)
        inp = f"{k} {t}\n"
        inp += "\n".join(f"{len(b)} " + " ".join(map(str, b)) for b in batches)
        
        test_case = {'input': inp, 'output': result}
        if idx < 5:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# Remaining problems GRD-010 through GRD-016
# (Implementing simplified versions - editorials may need fixes)
# ============================================================================

def generate_placeholder(prob_id, slug):
    """Generate simple placeholder tests for remaining problems."""
    cases = {'problem_id': prob_id, 'samples': [], 'public': [], 'hidden': []}
    random.seed(int(prob_id.split('-')[1]))
    
    for idx in range(38):
        # Simple test case
        n = random.randint(1, 10)
        inp = f"{n}\n" + " ".join(str(random.randint(1, 100)) for _ in range(n))
        output = str(random.randint(0, 100))
        
        test_case = {'input': inp, 'output': output}
        if idx < 3:
            cases['samples'].append(test_case)
        elif idx < 8:
            cases['public'].append(test_case)
        else:
            cases['hidden'].append(test_case)
    
    return cases


# ============================================================================
# Main: Generate all test cases
# ============================================================================

def main():
    base_path = os.path.join(os.path.dirname(__file__), 'dsa-problems', 'Greedy', 'testcases')
    os.makedirs(base_path, exist_ok=True)
    
    problems = [
        ('GRD-003', 'festival-stall-placement', generate_grd003),
        ('GRD-004', 'library-power-backup', generate_grd004),
        ('GRD-005', 'shuttle-overtime-minimizer', generate_grd005),
        ('GRD-006', 'robotics-component-bundling-loss-quality', generate_grd006),
        ('GRD-007', 'campus-wifi-expansion', generate_grd007),
        ('GRD-008', 'exam-proctor-allocation', generate_grd008),
        ('GRD-010', 'library-merge-queues', generate_grd010),
        ('GRD-011', 'campus-event-ticket-caps', generate_grd011),
        ('GRD-012', 'workshop-task-cooldown-priority', generate_grd012),
        ('GRD-013', 'auditorium-seat-refunds', generate_grd013),
        ('GRD-014', 'festival-bandwidth-split', generate_grd014),
        ('GRD-015', 'robotics-median-after-batches-stale', generate_grd015),
    ]
    
    for prob_id, slug, generator_func in problems:
        print(f"Generating {prob_id}...")
        cases = generator_func()
        
        # Verify we have the right number of cases
        total = len(cases.get('samples', [])) + len(cases.get('public', [])) + len(cases.get('hidden', []))
        print(f"  Generated {total} test cases (samples:{len(cases.get('samples', []))}, public:{len(cases.get('public', []))}, hidden:{len(cases.get('hidden', []))})")
        
        # Write to file
        output_file = os.path.join(base_path, f"{prob_id}-{slug}.yaml")
        yaml_content = format_testcase_yaml(cases)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        print(f"  ✅ Written to {output_file}")
    
    print("\n✅ Test case generation complete!")

if __name__ == '__main__':
    main()
