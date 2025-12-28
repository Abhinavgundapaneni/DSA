import random
import yaml
import bisect

def solve(n, k, values):
    if n == 0 or k == 0:
        return []
    
    results = []
    window = sorted(values[:k])
    
    #定义获取第二小值的辅助函数
    def get_second_min():
        if k == 1:
            return window[0]
        return window[1]

    results.append(get_second_min())
    
    for i in range(k, n):
        # Remove values[i-k]
        old_val = values[i-k]
        idx_to_remove = bisect.bisect_left(window, old_val)
        window.pop(idx_to_remove)
        # Add values[i]
        bisect.insort(window, values[i])
        results.append(get_second_min())
                
    return results

def make_test_case(n, k, values):
    res = solve(n, k, values)
    input_str = f"{n} {k}\n" + " ".join(map(str, values))
    output_str = " ".join(map(str, res))
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case(5, 3, [6, 2, 5, 1, 7]),
            make_test_case(3, 1, [10, 20, 30]),
            make_test_case(4, 2, [1, 1, 2, 2])
        ],
        "public": [
            make_test_case(6, 3, [5, 4, 3, 2, 1, 0]),  # Decreasing
            make_test_case(5, 2, [10, 5, 20, 15, 25]),  # Alternating
            make_test_case(5, 3, [7, 7, 7, 7, 7]),  # All same
            make_test_case(6, 4, [1, 2, 3, 4, 5, 6]),  # Increasing
            make_test_case(8, 5, [3, 1, 4, 1, 5, 9, 2, 6])  # Mixed
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case(10, 1, [random.randint(1, 100) for _ in range(10)]))  # k=1
    tc["hidden"].append(make_test_case(10, 10, [random.randint(1, 100) for _ in range(10)]))  # k=n
    tc["hidden"].append(make_test_case(5, 2, [1, 2, 3, 4, 5]))  # Small window
    tc["hidden"].append(make_test_case(6, 3, [10, 10, 10, 10, 10, 10]))  # All duplicates
    tc["hidden"].append(make_test_case(7, 4, [1, 1, 2, 2, 3, 3, 4]))  # Pairs
    tc["hidden"].append(make_test_case(8, 3, [5, 4, 3, 2, 1, 2, 3, 4]))  # V-shape
    tc["hidden"].append(make_test_case(5, 5, [9, 8, 7, 6, 5]))  # k=n decreasing
    tc["hidden"].append(make_test_case(9, 4, [1, 2, 1, 2, 1, 2, 1, 2, 1]))  # Alternating pattern

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case(6, 3, [10**9, -10**9, 10**9, -10**9, 10**9, -10**9]))  # Extremes
    tc["hidden"].append(make_test_case(5, 3, [0, 0, 0, 0, 0]))  # All zeros
    tc["hidden"].append(make_test_case(10, 5, [random.randint(-100, 100) for _ in range(10)]))  # With negatives
    tc["hidden"].append(make_test_case(8, 4, [-1, -2, -3, -4, -5, -6, -7, -8]))  # Negative decreasing
    tc["hidden"].append(make_test_case(12, 6, [random.randint(-10**9, 10**9) for _ in range(12)]))  # Extreme random
    tc["hidden"].append(make_test_case(15, 7, [i for i in range(15)]))  # Sequential larger
    tc["hidden"].append(make_test_case(10, 5, [100] * 10))  # All same large value
    tc["hidden"].append(make_test_case(20, 10, [random.randint(1, 50) for _ in range(20)]))  # Medium random

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case(12, 4, [random.randint(1, 100) for _ in range(12)]))  # Small-medium
    tc["hidden"].append(make_test_case(15, 5, [i*5 for i in range(15)]))  # Pattern
    tc["hidden"].append(make_test_case(18, 6, [random.randint(1, 200) for _ in range(18)]))  # Random medium
    tc["hidden"].append(make_test_case(20, 8, [i for i in range(20)]))  # Medium array
    tc["hidden"].append(make_test_case(25, 10, [random.randint(1, 150) for _ in range(25)]))  # Larger random
    tc["hidden"].append(make_test_case(22, 9, [i*3 for i in range(22)]))  # Pattern larger
    tc["hidden"].append(make_test_case(30, 12, [random.randint(1, 100) for _ in range(30)]))  # Large random
    tc["hidden"].append(make_test_case(28, 11, [i*2 for i in range(28)]))  # Even pattern
    tc["hidden"].append(make_test_case(35, 15, [random.randint(5, 95) for _ in range(35)]))  # Larger
    tc["hidden"].append(make_test_case(40, 18, [i for i in range(40)]))  # Large sequential
    tc["hidden"].append(make_test_case(32, 13, [random.randint(10, 90) for _ in range(32)]))  # Large varied
    tc["hidden"].append(make_test_case(38, 16, [i*4 for i in range(38)]))  # Pattern max

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
