import random
import yaml
import heapq

def solve(n, arrivals, departures):
    if n == 0:
        return 0
    
    intervals = sorted(zip(arrivals, departures))
    heap = []
    max_seats = 0
    
    for arr, dep in intervals:
        while heap and heap[0] <= arr:
            heapq.heappop(heap)
        heapq.heappush(heap, dep)
        max_seats = max(max_seats, len(heap))
    
    return max_seats

def make_test_case(arrivals, departures):
    n = len(arrivals)
    res = solve(n, arrivals, departures)
    input_str = f"{n}\n" + " ".join(map(str, arrivals)) + "\n" + " ".join(map(str, departures))
    output_str = str(res)
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case([0, 4, 4], [5, 5, 9]),
            make_test_case([1, 2, 3], [2, 3, 4]),
            make_test_case([1, 1, 1], [2, 2, 2])
        ],
        "public": [
            make_test_case([0, 5, 10], [5, 10, 15]),  # No overlap
            make_test_case([0], [10**9]),  # Single meeting
            make_test_case([1] * 5, [10] * 5),  # All overlap
            make_test_case([i*10 for i in range(5)], [i*10+5 for i in range(5)]),  # No overlap pattern
            make_test_case([1, 2, 3, 4], [5, 6, 7, 8])  # Nested
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case([0], [1]))  # Single short
    tc["hidden"].append(make_test_case([1, 2], [3, 4]))  # Two no overlap
    tc["hidden"].append(make_test_case([1, 1], [5, 5]))  # Two full overlap
    tc["hidden"].append(make_test_case([1, 3, 5], [2, 4, 6]))  # Three no overlap
    tc["hidden"].append(make_test_case([1, 1, 1], [3, 3, 3]))  # Three all overlap
    tc["hidden"].append(make_test_case([0, 5], [10, 15]))  # Two separate ranges
    tc["hidden"].append(make_test_case([1, 5, 10], [4, 8, 12]))  # Partial overlap
    tc["hidden"].append(make_test_case([i for i in range(5)], [i+1 for i in range(5)]))  # Chain

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case([0, 0, 0], [10**9, 10**9, 10**9]))  # Extreme long overlapping
    tc["hidden"].append(make_test_case([i*10**6 for i in range(8)], [(i+1)*10**6 for i in range(8)]))  # Large times
    tc["hidden"].append(make_test_case([random.randint(0, 100) for _ in range(10)], 
                                      [random.randint(100, 200) for _ in range(10)]))  # Random non-overlap
    tc["hidden"].append(make_test_case([1]*10, [100]*10))  # Ten all overlap
    tc["hidden"].append(make_test_case([i*5 for i in range(12)], [i*5+2 for i in range(12)]))  # Partial chain
    tc["hidden"].append(make_test_case([0, 10, 20, 30], [40, 40, 40, 40]))  # Mixed overlap
    tc["hidden"].append(make_test_case([random.randint(0, 10**8) for _ in range(15)], 
                                      [random.randint(10**8, 2*10**8) for _ in range(15)]))  # Large random
    tc["hidden"].append(make_test_case([i for i in range(20)], [i+10 for i in range(20)]))  # Heavy overlap

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case([random.randint(0, 100) for _ in range(8)], 
                                      [random.randint(10, 120) for _ in range(8)]))  # Small random
    tc["hidden"].append(make_test_case([i*10 for i in range(10)], [i*10+15 for i in range(10)]))  # Pattern overlap
    tc["hidden"].append(make_test_case([random.randint(0, 200) for _ in range(12)], 
                                      [random.randint(50, 250) for _ in range(12)]))  # Medium random
    tc["hidden"].append(make_test_case([i*5 for i in range(15)], [i*5+7 for i in range(15)]))  # Pattern medium
    tc["hidden"].append(make_test_case([random.randint(0, 500) for _ in range(18)], 
                                      [random.randint(100, 600) for _ in range(18)]))  # Larger random
    tc["hidden"].append(make_test_case([i*3 for i in range(20)], [i*3+5 for i in range(20)]))  # Pattern large
    tc["hidden"].append(make_test_case([random.randint(0, 1000) for _ in range(25)], 
                                      [random.randint(500, 1500) for _ in range(25)]))  # Large random
    tc["hidden"].append(make_test_case([i*2 for i in range(28)], [i*2+4 for i in range(28)]))  # Even pattern
    tc["hidden"].append(make_test_case([random.randint(0, 2000) for _ in range(30)], 
                                      [random.randint(1000, 3000) for _ in range(30)]))  # Very large random
    tc["hidden"].append(make_test_case([i*4 for i in range(22)], [i*4+6 for i in range(22)]))  # Pattern varied
    tc["hidden"].append(make_test_case([random.randint(0, 5000) for _ in range(35)], 
                                      [random.randint(2500, 7500) for _ in range(35)]))  # Max random
    tc["hidden"].append(make_test_case([i for i in range(40)], [i+20 for i in range(40)]))  # Heavy sequential

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
