import random
import yaml

def solve(values):
    n = len(values)
    l, r = 0, n - 1
    res = []
    turn = 0
    while l <= r:
        if turn % 2 == 0:
            res.append(values[l])
            l += 1
        else:
            res.append(values[r])
            r -= 1
        turn += 1
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
            make_test_case([2, 4, 6, 8]),
            make_test_case([1]),
            make_test_case([1, 2, 3])
        ],
        "public": [
            make_test_case([10, 20, 30, 40, 50]),  # Five elements
            make_test_case([1, 2]),  # Two elements
            make_test_case([i for i in range(10)]),  # Ten sequential
            make_test_case([5, 10, 15, 20]),  # Four elements
            make_test_case([100, 200, 300])  # Three large
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case([1]))  # Single
    tc["hidden"].append(make_test_case([1, 2]))  # Two
    tc["hidden"].append(make_test_case([1, 2, 3]))  # Three
    tc["hidden"].append(make_test_case([i for i in range(4)]))  # Four
    tc["hidden"].append(make_test_case([10]*5))  # All same
    tc["hidden"].append(make_test_case([i for i in range(6)]))  # Six sequential
    tc["hidden"].append(make_test_case([1, 2, 3, 4, 5, 6, 7]))  # Seven
    tc["hidden"].append(make_test_case([5, 4, 3, 2, 1]))  # Reverse

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case([10**9, -10**9]))  # Extremes
    tc["hidden"].append(make_test_case([-10**9, 0, 10**9]))  # Extremes with zero
    tc["hidden"].append(make_test_case([0]*10))  # All zeros
    tc["hidden"].append(make_test_case([-i for i in range(1, 11)]))  # Negative sequence
    tc["hidden"].append(make_test_case([random.randint(-10**9, 10**9) for _ in range(15)]))  # Random extremes
    tc["hidden"].append(make_test_case([10**9]*8))  # All extreme same
    tc["hidden"].append(make_test_case([i if i % 2 == 0 else -i for i in range(20)]))  # Alternating sign
    tc["hidden"].append(make_test_case([random.randint(-1000, 1000) for _ in range(18)]))  # Random medium

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case([i for i in range(12)]))  # Sequential small
    tc["hidden"].append(make_test_case([random.randint(1, 100) for _ in range(15)]))  # Random small
    tc["hidden"].append(make_test_case([i*5 for i in range(18)]))  # Pattern medium
    tc["hidden"].append(make_test_case([random.randint(1, 200) for _ in range(20)]))  # Random medium
    tc["hidden"].append(make_test_case([i*10 for i in range(25)]))  # Pattern large
    tc["hidden"].append(make_test_case([random.randint(1, 500) for _ in range(28)]))  # Random large
    tc["hidden"].append(make_test_case([i*20 for i in range(30)]))  # Pattern larger
    tc["hidden"].append(make_test_case([random.randint(1, 1000) for _ in range(35)]))  # Random larger
    tc["hidden"].append(make_test_case([i*50 for i in range(40)]))  # Pattern very large
    tc["hidden"].append(make_test_case([random.randint(1, 2000) for _ in range(45)]))  # Random very large
    tc["hidden"].append(make_test_case([i*100 for i in range(50)]))  # Pattern max
    tc["hidden"].append(make_test_case([random.randint(1, 5000) for _ in range(55)]))  # Random max

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
