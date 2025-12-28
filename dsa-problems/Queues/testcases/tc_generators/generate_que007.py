import random
import yaml
import bisect
from collections import deque

def solve(n, k, values):
    if n == 0 or k == 0:
        return []
        
    results = []
    
    # For max and min
    max_dq = deque()
    min_dq = deque()
    
    # For median (using sorted list for simplicity in generator)
    window = sorted(values[:k])
    
    def get_instability(idx):
        nonlocal max_dq, min_dq
        
        # Max/Min are handled by the sliding window loop
        # But we need them for the current window [idx-k+1, idx]
        # Actually it's easier to just calculate for each window in generator
        win = values[idx-k+1 : idx+1]
        v_max = max(win)
        v_min = min(win)
        
        # Median
        median = window[(k-1)//2]
        
        if median == 0:
            return 0
        return (v_max - v_min) // median

    for i in range(n):
        if i >= k:
            # Remove values[i-k] from sorted window
            old_val = values[i-k]
            idx_to_remove = bisect.bisect_left(window, old_val)
            window.pop(idx_to_remove)
            # Add values[i]
            bisect.insort(window, values[i])
        
        if i >= k - 1:
            win = values[i-k+1 : i+1]
            v_max = max(win)
            v_min = min(win)
            median = window[(k-1)//2]
            if median == 0:
                results.append(0)
            else:
                results.append((v_max - v_min) // median)
                
    return results

def make_test_case(n, k, values):
    res = solve(n, k, values)
    input_str = f"{n} {k}\n" + " ".join(map(str, values))
    output_str = " ".join(map(str, res))
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case(5, 3, [5, 1, 4, 6, 2]),
            make_test_case(3, 1, [10, 20, 30]),
            make_test_case(4, 2, [1, 2, 3, 4])
        ],
        "public": [
            make_test_case(6, 3, [0, 0, 0, 0, 0, 0]),  # All zeros
            make_test_case(5, 2, [1, 5, 3, 7, 2]),  # Small window
            make_test_case(6, 4, [2, 4, 6, 8, 10, 12]),  # Even sequence
            make_test_case(5, 5, [1, 2, 3, 4, 5]),  # k=n
            make_test_case(8, 3, [10, 5, 20, 15, 25, 30, 10, 5])  # Varying values
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case(10, 1, [random.randint(1, 100) for _ in range(10)]))  # k=1
    tc["hidden"].append(make_test_case(10, 10, [random.randint(1, 100) for _ in range(10)]))  # k=n
    tc["hidden"].append(make_test_case(5, 2, [0, 1, 0, 1, 0]))  # Zeros in median
    tc["hidden"].append(make_test_case(6, 3, [1, 1, 1, 1, 1, 1]))  # All same
    tc["hidden"].append(make_test_case(7, 3, [1, 2, 3, 4, 5, 6, 7]))  # Sequential
    tc["hidden"].append(make_test_case(8, 4, [10, 5, 10, 5, 10, 5, 10, 5]))  # Alternating
    tc["hidden"].append(make_test_case(5, 3, [0, 0, 1, 0, 0]))  # Zero median case
    tc["hidden"].append(make_test_case(9, 5, [1, 2, 3, 4, 5, 4, 3, 2, 1]))  # Peak pattern

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case(6, 3, [10**9, 1, 10**9, 1, 10**9, 1]))  # Extreme alternating
    tc["hidden"].append(make_test_case(5, 3, [-10**9, 0, 10**9, -10**9, 10**9]))  # Extremes with zero
    tc["hidden"].append(make_test_case(10, 5, [random.randint(-100, 100) for _ in range(10)]))  # Random with negatives
    tc["hidden"].append(make_test_case(8, 4, [0] * 8))  # All zeros
    tc["hidden"].append(make_test_case(12, 6, [i*10 for i in range(12)]))  # Large increments
    tc["hidden"].append(make_test_case(15, 7, [random.randint(1, 50) for _ in range(15)]))  # Medium random
    tc["hidden"].append(make_test_case(10, 5, [100, 1, 100, 1, 100, 1, 100, 1, 100, 1]))  # High variance
    tc["hidden"].append(make_test_case(20, 10, [i for i in range(20)]))  # Larger sequential

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case(12, 4, [random.randint(1, 100) for _ in range(12)]))  # Small-medium
    tc["hidden"].append(make_test_case(15, 5, [i*5 for i in range(15)]))  # Pattern medium
    tc["hidden"].append(make_test_case(18, 6, [random.randint(1, 200) for _ in range(18)]))  # Random medium
    tc["hidden"].append(make_test_case(20, 8, [i for i in range(20)]))  # Medium array
    tc["hidden"].append(make_test_case(25, 10, [random.randint(1, 150) for _ in range(25)]))  # Larger random
    tc["hidden"].append(make_test_case(22, 9, [i*3 for i in range(22)]))  # Pattern larger
    tc["hidden"].append(make_test_case(30, 12, [random.randint(1, 100) for _ in range(30)]))  # Large random
    tc["hidden"].append(make_test_case(28, 11, [i*2 for i in range(28)]))  # Even pattern large
    tc["hidden"].append(make_test_case(35, 15, [random.randint(5, 95) for _ in range(35)]))  # Larger array
    tc["hidden"].append(make_test_case(40, 18, [i for i in range(40)]))  # Large sequential
    tc["hidden"].append(make_test_case(32, 13, [random.randint(10, 90) for _ in range(32)]))  # Large random varied
    tc["hidden"].append(make_test_case(38, 16, [i*4 for i in range(38)]))  # Pattern max

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
