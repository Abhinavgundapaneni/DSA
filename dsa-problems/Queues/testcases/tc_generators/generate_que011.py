import random
import yaml

def solve(a, b):
    res = []
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    res.extend(a[i:])
    res.extend(b[j:])
    return res

def make_test_case(a, b):
    n, m = len(a), len(b)
    res = solve(a, b)
    input_str = f"{n}\n" + " ".join(map(str, a)) + f"\n{m}\n" + " ".join(map(str, b))
    output_str = " ".join(map(str, res))
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case([3, 5, 9], [1, 4, 10]),
            make_test_case([], [1, 2, 3]),
            make_test_case([1, 2, 3], [])
        ],
        "public": [
            make_test_case([1, 3, 5], [2, 4, 6]),  # Interleaved
            make_test_case([], []),  # Both empty
            make_test_case([10] * 5, [10] * 5),  # Duplicates
            make_test_case([1, 2], [10, 20]),  # Separated ranges
            make_test_case([i for i in range(5)], [i*2 for i in range(5)])  # Different patterns
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case([], []))  # Both empty
    tc["hidden"].append(make_test_case([1], []))  # One empty
    tc["hidden"].append(make_test_case([], [2]))  # Other empty
    tc["hidden"].append(make_test_case([1], [2]))  # Both single
    tc["hidden"].append(make_test_case([1, 1, 1], [1, 1, 1]))  # All same
    tc["hidden"].append(make_test_case([1, 2, 3], [4, 5, 6]))  # No overlap
    tc["hidden"].append(make_test_case([1, 3, 5, 7], [2, 4, 6, 8]))  # Perfect interleave
    tc["hidden"].append(make_test_case([10] * 10, [5] * 10))  # Duplicates

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case([-10**9], [10**9]))  # Extremes
    tc["hidden"].append(make_test_case([i for i in range(-10, 0)], [i for i in range(0, 10)]))  # Neg/pos
    tc["hidden"].append(make_test_case([random.randint(-10**9, 10**9) for _ in range(15)], 
                                      [random.randint(-10**9, 10**9) for _ in range(15)]))  # Random extremes
    tc["hidden"].append(make_test_case([0]*10, [0]*10))  # All zeros
    tc["hidden"].append(make_test_case([i*100 for i in range(20)], [i*100+50 for i in range(20)]))  # Large gaps
    tc["hidden"].append(make_test_case([-i for i in range(15, 0, -1)], [i for i in range(15)]))  # Neg sorted
    tc["hidden"].append(make_test_case([10**9]*5, [-10**9]*5))  # Extreme duplicates
    tc["hidden"].append(make_test_case([i for i in range(100)], [i*2 for i in range(50)]))  # Different lengths

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case([i for i in range(10)], [i for i in range(5, 15)]))  # Overlap
    tc["hidden"].append(make_test_case([random.randint(1, 100) for _ in range(12)], 
                                      [random.randint(1, 100) for _ in range(12)]))  # Small random
    tc["hidden"].append(make_test_case([i*5 for i in range(15)], [i*3 for i in range(20)]))  # Pattern mix
    tc["hidden"].append(make_test_case([random.randint(-200, 200) for _ in range(18)], 
                                      [random.randint(-200, 200) for _ in range(18)]))  # Medium random
    tc["hidden"].append(make_test_case([i for i in range(0, 40, 2)], [i for i in range(1, 40, 2)]))  # Even/odd
    tc["hidden"].append(make_test_case([random.randint(1, 500) for _ in range(25)], 
                                      [random.randint(1, 500) for _ in range(20)]))  # Varied lengths
    tc["hidden"].append(make_test_case([i*10 for i in range(30)], [i*10+5 for i in range(30)]))  # Interleaved pattern
    tc["hidden"].append(make_test_case([random.randint(-1000, 1000) for _ in range(35)], 
                                      [random.randint(-1000, 1000) for _ in range(35)]))  # Large random
    tc["hidden"].append(make_test_case([i for i in range(50)], [i for i in range(25, 75)]))  # Large overlap
    tc["hidden"].append(make_test_case([i*2 for i in range(40)], [i*3 for i in range(30)]))  # Pattern large
    tc["hidden"].append(make_test_case([random.randint(1, 2000) for _ in range(45)], 
                                      [random.randint(1, 2000) for _ in range(45)]))  # Very large random
    tc["hidden"].append(make_test_case([i for i in range(60)], [i for i in range(30, 90)]))  # Large overlap varied
    tc["hidden"].append(make_test_case([i*4 for i in range(50)], [i*5 for i in range(40)]))  # Pattern max

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
