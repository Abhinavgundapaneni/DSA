import random
import yaml

def solve(values):
    n = len(values)
    half = n // 2
    first_half = values[:half]
    second_half = values[half:]
    res = []
    for i in range(half):
        res.append(first_half[i])
        res.append(second_half[i])
    return res

def make_test_case(values):
    n = len(values)
    res = solve(values)
    input_str = f"{n}\n" + " ".join(map(str, values))
    output_str = " ".join(map(str, res))
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case([11, 12, 13, 14]),
            make_test_case([1, 2]),
            make_test_case([1, 2, 3, 4, 5, 6])
        ],
        "public": [
            make_test_case([10, 20]),  # Minimum
            make_test_case([1, 2, 3, 4]),  # Four elements
            make_test_case([5, 10, 15, 20, 25, 30]),  # Six elements
            make_test_case([i for i in range(8)]),  # Eight sequential
            make_test_case([100, 200, 300, 400])  # Large values
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case([1, 2]))  # Minimum even
    tc["hidden"].append(make_test_case([0, 0]))  # Duplicate zeros
    tc["hidden"].append(make_test_case([10, 20]))  # Two different
    tc["hidden"].append(make_test_case([1, 2, 3, 4]))  # Four sequential
    tc["hidden"].append(make_test_case([5, 5, 10, 10]))  # Pairs
    tc["hidden"].append(make_test_case([i for i in range(6)]))  # Six sequential
    tc["hidden"].append(make_test_case([1, 1, 1, 1]))  # All same
    tc["hidden"].append(make_test_case([2, 4, 6, 8]))  # Even numbers

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case([10**9, -10**9]))  # Extremes
    tc["hidden"].append(make_test_case([-10**9, 0, 10**9, 0]))  # Mixed extremes
    tc["hidden"].append(make_test_case([0, 0, 0, 0, 0, 0]))  # All zeros
    tc["hidden"].append(make_test_case([-1, -2, -3, -4]))  # Negative
    tc["hidden"].append(make_test_case([10**9, 10**9, -10**9, -10**9]))  # Extreme pairs
    tc["hidden"].append(make_test_case([50]*10))  # Large duplicate
    tc["hidden"].append(make_test_case([-i for i in range(10)]))  # Negative sequence
    tc["hidden"].append(make_test_case([random.randint(-10**9, 10**9) for _ in range(20)]))  # Random extremes

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case([i for i in range(10)]))  # Ten sequential
    tc["hidden"].append(make_test_case([i*10 for i in range(12)]))  # Pattern
    tc["hidden"].append(make_test_case([i for i in range(14)]))  # Fourteen
    tc["hidden"].append(make_test_case([random.randint(-100, 100) for _ in range(16)]))  # Random small
    tc["hidden"].append(make_test_case([i for i in range(20)]))  # Twenty
    tc["hidden"].append(make_test_case([i*5 for i in range(18)]))  # Medium pattern
    tc["hidden"].append(make_test_case([i for i in range(5, 25)]))  # Range
    tc["hidden"].append(make_test_case([random.randint(-1000, 1000) for _ in range(24)]))  # Random medium
    tc["hidden"].append(make_test_case([i for i in range(30)]))  # Larger
    tc["hidden"].append(make_test_case([i*2 for i in range(26)]))  # Even pattern
    tc["hidden"].append(make_test_case([i for i in range(10, 32)]))  # Offset range
    tc["hidden"].append(make_test_case([random.randint(-50, 50) for _ in range(22)]))  # Random mix
    tc["hidden"].append(make_test_case([i*3 for i in range(28)]))  # Triple pattern
    tc["hidden"].append(make_test_case([i for i in range(40)]))  # Forty elements

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
