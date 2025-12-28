import random
import yaml

def solve(n, q1, q2):
    return [q2, q1]

def make_test_case(q1, q2):
    n = len(q1)
    res = solve(n, q1, q2)
    input_str = f"{n}\n" + " ".join(map(str, q1)) + "\n" + " ".join(map(str, q2))
    output_str = " ".join(map(str, res[0])) + "\n" + " ".join(map(str, res[1]))
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case([4, 5], [7, 8]),
            make_test_case([1], [2]),
            make_test_case([1, 2, 3], [4, 5, 6])
        ],
        "public": [
            make_test_case([10, 20], [30, 40]),  # Two each
            make_test_case([100], [200]),  # Single each
            make_test_case([i for i in range(5)], [i*10 for i in range(5)]),  # Five each
            make_test_case([1, 1, 1], [2, 2, 2]),  # Duplicates
            make_test_case([10, 20, 30, 40], [50, 60, 70, 80])  # Four each
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case([1], [2]))  # Minimum
    tc["hidden"].append(make_test_case([5, 10], [15, 20]))  # Two each
    tc["hidden"].append(make_test_case([1, 2, 3], [4, 5, 6]))  # Three each
    tc["hidden"].append(make_test_case([0]*5, [1]*5))  # Same values
    tc["hidden"].append(make_test_case([i for i in range(6)], [i*2 for i in range(6)]))  # Pattern
    tc["hidden"].append(make_test_case([10]*7, [20]*7))  # All duplicates
    tc["hidden"].append(make_test_case([i for i in range(8)], [i+10 for i in range(8)]))  # Offset
    tc["hidden"].append(make_test_case([5, 4, 3, 2, 1], [10, 9, 8, 7, 6]))  # Descending

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case([10**9], [-10**9]))  # Extremes
    tc["hidden"].append(make_test_case([-10**9]*3, [10**9]*3))  # Extreme duplicates
    tc["hidden"].append(make_test_case([random.randint(-10**9, 10**9) for _ in range(10)], 
                                      [random.randint(-10**9, 10**9) for _ in range(10)]))  # Random extremes
    tc["hidden"].append(make_test_case([0]*10, [0]*10))  # All zeros
    tc["hidden"].append(make_test_case([-i for i in range(1, 13)], [i for i in range(1, 13)]))  # Neg/pos
    tc["hidden"].append(make_test_case([random.randint(-1000, 1000) for _ in range(15)], 
                                      [random.randint(-1000, 1000) for _ in range(15)]))  # Random medium
    tc["hidden"].append(make_test_case([10**6]*5, [-10**6]*5))  # Large values
    tc["hidden"].append(make_test_case([i*10**5 for i in range(20)], [-i*10**5 for i in range(20)]))  # Large pattern

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case([random.randint(1, 100) for _ in range(8)], 
                                      [random.randint(1, 100) for _ in range(8)]))  # Small random
    tc["hidden"].append(make_test_case([i*5 for i in range(10)], [i*10 for i in range(10)]))  # Pattern
    tc["hidden"].append(make_test_case([random.randint(1, 200) for _ in range(12)], 
                                      [random.randint(1, 200) for _ in range(12)]))  # Medium random
    tc["hidden"].append(make_test_case([i*10 for i in range(15)], [i*20 for i in range(15)]))  # Pattern medium
    tc["hidden"].append(make_test_case([random.randint(1, 500) for _ in range(18)], 
                                      [random.randint(1, 500) for _ in range(18)]))  # Larger random
    tc["hidden"].append(make_test_case([i*20 for i in range(20)], [i*30 for i in range(20)]))  # Pattern large
    tc["hidden"].append(make_test_case([random.randint(1, 1000) for _ in range(25)], 
                                      [random.randint(1, 1000) for _ in range(25)]))  # Large random
    tc["hidden"].append(make_test_case([i*50 for i in range(28)], [i*60 for i in range(28)]))  # Pattern larger
    tc["hidden"].append(make_test_case([random.randint(1, 2000) for _ in range(30)], 
                                      [random.randint(1, 2000) for _ in range(30)]))  # Very large random
    tc["hidden"].append(make_test_case([i*100 for i in range(35)], [i*110 for i in range(35)]))  # Pattern max
    tc["hidden"].append(make_test_case([random.randint(1, 5000) for _ in range(40)], 
                                      [random.randint(1, 5000) for _ in range(40)]))  # Max random
    tc["hidden"].append(make_test_case([i*200 for i in range(45)], [i*210 for i in range(45)]))  # Max pattern

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
