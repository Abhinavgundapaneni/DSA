from collections import deque
import random
import yaml

def solve(n, k, values):
    queue = deque()
    results = []
    
    for i in range(n):
        if values[i] < 0:
            queue.append(i)
        
        if i >= k - 1:
            while queue and queue[0] <= i - k:
                queue.popleft()
            
            if queue:
                results.append(values[queue[0]])
            else:
                results.append(0)
    return results

def make_test_case(n, k, values):
    res = solve(n, k, values)
    input_str = f"{n} {k}\n" + " ".join(map(str, values))
    output_str = " ".join(map(str, res))
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case(5, 2, [5, -2, -7, 3, 4]),
            make_test_case(3, 1, [1, -1, 1]),
            make_test_case(4, 3, [1, 2, 3, 4])
        ],
        "public": [
            make_test_case(6, 3, [-1, -2, -3, -4, -5, -6]),  # All negative
            make_test_case(5, 2, [10, 5, -3, 7, -2]),  # Mixed
            make_test_case(6, 4, [1, 2, 3, -4, 5, 6]),  # One negative
            make_test_case(7, 3, [5, -1, 10, -2, 15, -3, 20]),  # Alternating
            make_test_case(8, 5, [1, 2, 3, 4, 5, 6, 7, 8])  # All positive
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case(10, 1, [random.randint(-100, 100) for _ in range(10)]))  # k=1
    tc["hidden"].append(make_test_case(10, 10, [random.randint(-100, 100) for _ in range(10)]))  # k=n
    tc["hidden"].append(make_test_case(5, 2, [1, 2, 3, 4, 5]))  # No negatives
    tc["hidden"].append(make_test_case(6, 3, [-1, -2, -3, -4, -5, -6]))  # All negative
    tc["hidden"].append(make_test_case(7, 3, [1, -1, 1, -1, 1, -1, 1]))  # Alternating
    tc["hidden"].append(make_test_case(8, 4, [10, 5, -1, 20, 15, -2, 25, 30]))  # Sparse negatives
    tc["hidden"].append(make_test_case(5, 5, [-5, -4, -3, -2, -1]))  # k=n all negative
    tc["hidden"].append(make_test_case(9, 3, [0, 0, 0, 0, 0, 0, 0, 0, 0]))  # All zeros

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case(6, 3, [10**9, -10**9, 10**9, -10**9, 10**9, -10**9]))  # Extreme alternating
    tc["hidden"].append(make_test_case(5, 3, [0, 0, -1, 0, 0]))  # Single negative
    tc["hidden"].append(make_test_case(10, 5, [random.randint(-1000, 1000) for _ in range(10)]))  # Large range random
    tc["hidden"].append(make_test_case(8, 4, [-10**9] * 8))  # All extreme negative
    tc["hidden"].append(make_test_case(12, 6, [i if i % 2 == 0 else -i for i in range(12)]))  # Pattern pos/neg
    tc["hidden"].append(make_test_case(15, 7, [i for i in range(1, 16)]))  # All positive sequential
    tc["hidden"].append(make_test_case(10, 5, [-i for i in range(1, 11)]))  # All negative sequential
    tc["hidden"].append(make_test_case(20, 10, [random.randint(-50, 50) for _ in range(20)]))  # Medium random

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case(12, 4, [random.randint(-100, 100) for _ in range(12)]))  # Small-medium
    tc["hidden"].append(make_test_case(15, 5, [i if i % 3 != 0 else -i for i in range(15)]))  # Pattern
    tc["hidden"].append(make_test_case(18, 6, [random.randint(-200, 200) for _ in range(18)]))  # Random medium
    tc["hidden"].append(make_test_case(20, 8, [i if i % 2 == 0 else -i for i in range(20)]))  # Alternating pattern
    tc["hidden"].append(make_test_case(25, 10, [random.randint(-150, 150) for _ in range(25)]))  # Larger random
    tc["hidden"].append(make_test_case(22, 9, [i*3 if i % 2 == 0 else -i*3 for i in range(22)]))  # Pattern larger
    tc["hidden"].append(make_test_case(30, 12, [random.randint(-100, 100) for _ in range(30)]))  # Large random
    tc["hidden"].append(make_test_case(28, 11, [i*2 if i % 4 != 0 else -i*2 for i in range(28)]))  # Complex pattern
    tc["hidden"].append(make_test_case(35, 15, [random.randint(-95, 95) for _ in range(35)]))  # Larger
    tc["hidden"].append(make_test_case(40, 18, [i if i % 5 != 0 else -i for i in range(40)]))  # Large pattern
    tc["hidden"].append(make_test_case(32, 13, [random.randint(-90, 90) for _ in range(32)]))  # Large varied
    tc["hidden"].append(make_test_case(38, 16, [i if i % 3 != 0 else -i*2 for i in range(38)]))  # Pattern max

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
