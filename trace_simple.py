import heapq

def trace_sample1():
    """Trace A:4, k=1 expecting 7"""
    print("Tracing: A has 4 tasks, priority 2, k=1")
    print("Expected: 7\n")
    
    # Without interrupts (standard scheduling):
    # A _ A _ A _ A = 7 time slots
    
    # With my algorithm:
    time = 0
    remaining = 4
    ready_time_A = 0
    
    while remaining > 0:
        time += 1
        print(f"Time {time}:")
        
        if ready_time_A <= time:
            print(f"  Execute A (remaining={remaining})")
            remaining -= 1
            if remaining > 0:
                ready_time_A = time + 1 + 1  # time + k + 1
                print(f"    A will be ready at {ready_time_A}")
        else:
            print(f"  IDLE (A ready at {ready_time_A})")
        print()
    
    print(f"Total time: {time}")
    print(f"Expected: 7")

trace_sample1()
