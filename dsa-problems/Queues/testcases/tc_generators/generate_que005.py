import random
import yaml

def solve(values, k):
    res = values[:k][::-1] + values[k:]
    return res

def make_test_case(values, k):
    n = len(values)
    res = solve(values, k)
    input_str = f"{n}\n" + " ".join(map(str, values)) + f"\n{k}"
    output_str = " ".join(map(str, res))
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case([2, 4, 6, 8, 10], 4),
            make_test_case([1, 2, 3], 1),
            make_test_case([1, 2, 3], 3)
        ],
        "public": [
            make_test_case([10, 20, 30, 40], 2),  # Four elements, k=2
            make_test_case([i for i in range(10)], 1),  # k=1
            make_test_case([i for i in range(10)], 10),  # k=n
            make_test_case([5, 10, 15], 2),  # Three elements
            make_test_case([1, 2, 3, 4, 5], 5)  # k=n
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case([1], 1))  # Single element
    tc["hidden"].append(make_test_case([1, 2], 1))  # Two, k=1
    tc["hidden"].append(make_test_case([1, 2], 2))  # Two, k=2
    tc["hidden"].append(make_test_case([1, 2, 3], 2))  # Three, k=2
    tc["hidden"].append(make_test_case([5, 10, 15, 20], 1))  # k=1, larger
    tc["hidden"].append(make_test_case([1, 2, 3, 4], 4))  # k=n exact
    tc["hidden"].append(make_test_case([10, 20, 30, 40, 50], 3))  # Middle k
    tc["hidden"].append(make_test_case([i for i in range(6)], 1))  # Six, k=1

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case([10**9], 1))  # Extreme value single
    tc["hidden"].append(make_test_case([-10**9, 0, 10**9], 3))  # Extremes all
    tc["hidden"].append(make_test_case([0, 0, 0, 0], 2))  # All zeros
    tc["hidden"].append(make_test_case([-1, -2, -3, -4, -5], 4))  # Negative
    tc["hidden"].append(make_test_case([10**9, 10**9, 10**9], 2))  # Extreme duplicates
    tc["hidden"].append(make_test_case([i for i in range(50)], 50))  # Medium, k=n
    tc["hidden"].append(make_test_case([-i for i in range(10)], 5))  # Negative sequence
    tc["hidden"].append(make_test_case([random.randint(-10**9, 10**9) for _ in range(15)], 10))  # Random extremes

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case([i for i in range(10)], 5))  # Half
    tc["hidden"].append(make_test_case([i*10 for i in range(8)], 4))  # Pattern
    tc["hidden"].append(make_test_case([5, 4, 3, 2, 1], 3))  # Reverse order
    tc["hidden"].append(make_test_case([i for i in range(12)], 7))  # Medium array
    tc["hidden"].append(make_test_case([random.randint(-100, 100) for _ in range(15)], 9))  # Random small
    tc["hidden"].append(make_test_case([i for i in range(20)], 12))  # Larger
    tc["hidden"].append(make_test_case([i*5 for i in range(16)], 8))  # Pattern medium
    tc["hidden"].append(make_test_case([i for i in range(5, 25)], 15))  # Range
    tc["hidden"].append(make_test_case([random.randint(-1000, 1000) for _ in range(18)], 10))  # Random medium
    tc["hidden"].append(make_test_case([i for i in range(25)], 20))  # Larger k
    tc["hidden"].append(make_test_case([i*2 for i in range(22)], 11))  # Even pattern
    tc["hidden"].append(make_test_case([i for i in range(30)], 18))  # Large array
    tc["hidden"].append(make_test_case([random.randint(-50, 50) for _ in range(20)], 13))  # Random mix
    tc["hidden"].append(make_test_case([i*3 for i in range(24)], 16))  # Triple pattern

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
