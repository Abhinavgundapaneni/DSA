import random
import yaml

def solve(n, values, k):
    if n == 0:
        return []
    k = k % n
    return values[k:] + values[:k]

def make_test_case(values, k):
    n = len(values)
    res = solve(n, values, k)
    input_str = f"{n}\n" + " ".join(map(str, values)) + f"\n{k}"
    output_str = " ".join(map(str, res))
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case([4, 9, 1, 7], 3),
            make_test_case([1, 2, 3, 4, 5], 0),
            make_test_case([1, 2, 3, 4, 5], 5)
        ],
        "public": [
            make_test_case([1, 2, 3, 4, 5], 11),  # k > n
            make_test_case([100], 10**9),  # Single element, large k
            make_test_case([i for i in range(10)], 9),  # k = n-1
            make_test_case([1, 2], 1),  # Two elements
            make_test_case([10, 20, 30], 3)  # k = n (no rotation)
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case([1], 0))  # Single, k=0
    tc["hidden"].append(make_test_case([1], 1))  # Single, k=1
    tc["hidden"].append(make_test_case([1, 2], 0))  # Two, k=0
    tc["hidden"].append(make_test_case([1, 2], 2))  # Two, k=n
    tc["hidden"].append(make_test_case([5, 10, 15], 0))  # No rotation
    tc["hidden"].append(make_test_case([5, 10, 15], 3))  # Full rotation
    tc["hidden"].append(make_test_case([1, 2, 3, 4], 1))  # Rotate by 1
    tc["hidden"].append(make_test_case([1, 2, 3, 4, 5, 6], 6))  # k = n exactly

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case([10**9], 10**9))  # Extreme value, extreme k
    tc["hidden"].append(make_test_case([-10**9, 0, 10**9], 2))  # Extreme values
    tc["hidden"].append(make_test_case([0, 0, 0, 0], 2))  # All zeros
    tc["hidden"].append(make_test_case([1, 2, 3, 4, 5], 10**9))  # Large k
    tc["hidden"].append(make_test_case([-1, -2, -3, -4], 3))  # Negative values
    tc["hidden"].append(make_test_case([100, 100, 100], 1))  # Duplicate values
    tc["hidden"].append(make_test_case([i for i in range(50)], 49))  # k = n-1, medium
    tc["hidden"].append(make_test_case([i for i in range(20)], 20))  # k = n, medium

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case([1, 2, 3, 4, 5], 2))  # Small rotation
    tc["hidden"].append(make_test_case([10, 20, 30, 40, 50, 60], 3))  # Medium rotation
    tc["hidden"].append(make_test_case([i for i in range(10)], 5))  # Half rotation
    tc["hidden"].append(make_test_case([i*10 for i in range(8)], 3))  # Pattern values
    tc["hidden"].append(make_test_case([5, 4, 3, 2, 1], 2))  # Reverse order
    tc["hidden"].append(make_test_case([i for i in range(15)], 7))  # Medium array
    tc["hidden"].append(make_test_case([random.randint(-100, 100) for _ in range(12)], 4))  # Random small
    tc["hidden"].append(make_test_case([i for i in range(20)], 13))  # Larger rotation
    tc["hidden"].append(make_test_case([i*5 for i in range(18)], 9))  # Medium-large
    tc["hidden"].append(make_test_case([random.randint(-1000, 1000) for _ in range(25)], 15))  # Random medium
    tc["hidden"].append(make_test_case([i for i in range(30)], 17))  # Larger array
    tc["hidden"].append(make_test_case([i*2 for i in range(16)], 8))  # Even pattern
    tc["hidden"].append(make_test_case([i for i in range(10, 30)], 12))  # Range values
    tc["hidden"].append(make_test_case([random.randint(-50, 50) for _ in range(20)], 11))  # Random mix

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
