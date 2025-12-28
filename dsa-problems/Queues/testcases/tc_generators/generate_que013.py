from collections import deque
import random
import yaml

def solve(n, t, k, times):
    queue = deque()
    results = []
    for time in times:
        while queue and queue[0] < time - t:
            queue.popleft()
        
        if len(queue) < k:
            results.append("true")
            queue.append(time)
        else:
            results.append("false")
    return results

def make_test_case(t, k, times):
    n = len(times)
    res = solve(n, t, k, times)
    input_str = f"{n} {t} {k}\n" + " ".join(map(str, times))
    output_str = " ".join(res)
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case(4, 1, [2, 4, 6, 9]),
            make_test_case(1, 1, [1, 1, 1, 2, 2]),
            make_test_case(10, 10, [i for i in range(10)])
        ],
        "public": [
            make_test_case(5, 2, [0, 1, 2, 3, 4, 10, 11, 12]),  # Two bursts
            make_test_case(1, 100, [0] * 10),  # High k, same time
            make_test_case(10**9, 1, [1, 10**8, 10**9]),  # Large window
            make_test_case(1, 1, [i*2 for i in range(10)]),  # Spaced out
            make_test_case(3, 3, [1, 2, 3, 10, 11, 12])  # Two groups
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case(1, 1, [1]))  # Single request
    tc["hidden"].append(make_test_case(1, 1, [1, 1]))  # Two same time
    tc["hidden"].append(make_test_case(10, 1, [1, 2, 3]))  # Large window, k=1
    tc["hidden"].append(make_test_case(1, 10, [1]*10))  # Small window, high k
    tc["hidden"].append(make_test_case(5, 2, [0, 1, 10, 11]))  # Two bursts
    tc["hidden"].append(make_test_case(100, 5, [i*10 for i in range(20)]))  # Spaced, medium k
    tc["hidden"].append(make_test_case(1, 1, [i for i in range(100)]))  # Sequential
    tc["hidden"].append(make_test_case(10**9, 10, [i*10**8 for i in range(15)]))  # Huge window

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case(10**9, 1, [0, 10**9]))  # Extremes
    tc["hidden"].append(make_test_case(1, 1000, [0]*100))  # High k
    tc["hidden"].append(make_test_case(10**6, 10, [random.randint(0, 10**9) for _ in range(20)]))  # Random large
    tc["hidden"].append(make_test_case(1, 5, [1, 1, 1, 1, 1, 2, 2, 2]))  # Burst limit
    tc["hidden"].append(make_test_case(100, 20, [i for i in range(50)]))  # High k sequential
    tc["hidden"].append(make_test_case(10**8, 5, [i*10**7 for i in range(25)]))  # Large times
    tc["hidden"].append(make_test_case(50, 10, [random.randint(0, 1000) for _ in range(30)]))  # Random medium
    tc["hidden"].append(make_test_case(1000, 50, [i*10 for i in range(40)]))  # Large window, high k

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case(5, 2, [random.randint(0, 50) for _ in range(15)]))  # Small random
    tc["hidden"].append(make_test_case(10, 3, [i*2 for i in range(20)]))  # Pattern
    tc["hidden"].append(make_test_case(20, 5, [random.randint(0, 200) for _ in range(25)]))  # Medium random
    tc["hidden"].append(make_test_case(15, 4, [i*3 for i in range(30)]))  # Pattern medium
    tc["hidden"].append(make_test_case(50, 10, [random.randint(0, 500) for _ in range(35)]))  # Larger random
    tc["hidden"].append(make_test_case(30, 6, [i*5 for i in range(40)]))  # Pattern large
    tc["hidden"].append(make_test_case(100, 15, [random.randint(0, 1000) for _ in range(45)]))  # Large random
    tc["hidden"].append(make_test_case(40, 8, [i*4 for i in range(50)]))  # Pattern larger
    tc["hidden"].append(make_test_case(200, 20, [random.randint(0, 2000) for _ in range(55)]))  # Very large random
    tc["hidden"].append(make_test_case(60, 12, [i*6 for i in range(60)]))  # Pattern max
    tc["hidden"].append(make_test_case(500, 25, [random.randint(0, 5000) for _ in range(65)]))  # Max random
    tc["hidden"].append(make_test_case(80, 15, [i*8 for i in range(70)]))  # Max pattern

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
