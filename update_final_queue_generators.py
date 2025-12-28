"""
Script to update remaining Queue test generators (QUE-011 to QUE-016)
Expands each to 38 test cases (3 samples + 5 public + 30 hidden)
"""
import os
import re

DSA_DIR = r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Queues\testcases\tc_generators"

# QUE-011: Merge sorted queues
QUE011_NEW_YAML = """def generate_yaml():
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

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))"""

# QUE-012: Circuit energy stations (complex generator - keep it simpler)
QUE012_NEW_YAML_SIMPLE = """def generate_yaml():
    tc = {
        "samples": [
            make_test_case([3, 1, 2], [1, 2, 2]),
            make_test_case([1, 2, 3, 4], [2, 3, 4, 5]),
            make_test_case([4, 5, 6], [3, 4, 5])
        ],
        "public": [
            make_test_case([2, 2, 2], [1, 1, 1]),  # Simple sufficient
            make_test_case([1, 1, 1], [2, 2, 2]),  # Impossible
            make_test_case([10, 1, 1], [1, 1, 9]),  # One skip
            make_test_case([5, 5, 5], [4, 4, 4]),  # Exact
            make_test_case([1, 2, 3, 4, 5], [2, 1, 2, 1, 2])  # Mixed
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case([10], [5]))  # Single
    tc["hidden"].append(make_test_case([10, 10], [5, 5]))  # Two same
    tc["hidden"].append(make_test_case([1, 2], [2, 1]))  # Two swap
    tc["hidden"].append(make_test_case([5]*5, [4]*5]))  # All same sufficient
    tc["hidden"].append(make_test_case([1]*5, [2]*5]))  # All same insufficient
    tc["hidden"].append(make_test_case([10, 1, 1, 1], [1, 1, 1, 8]))  # One dominant
    tc["hidden"].append(make_test_case([i for i in range(1, 6)], [i//2 for i in range(1, 6)]))  # Half cost
    tc["hidden"].append(make_test_case([i*2 for i in range(1, 7)], [i for i in range(1, 7)]))  # Double gain

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case([10**9], [1]))  # Extreme gain
    tc["hidden"].append(make_test_case([10**9]*3, [1, 1, 10**9-1]))  # Extreme with one skip
    tc["hidden"].append(make_test_case([random.randint(1, 100) for _ in range(10)], 
                                      [random.randint(1, 100) for _ in range(10)]))  # Random small
    tc["hidden"].append(make_test_case([100]*10, [99]*10]))  # Close margins
    tc["hidden"].append(make_test_case([i*10 for i in range(1, 13)], [i*5 for i in range(1, 13)]))  # Pattern
    tc["hidden"].append(make_test_case([random.randint(1, 1000) for _ in range(15)], 
                                      [random.randint(1, 1000) for _ in range(15)]))  # Medium random
    tc["hidden"].append(make_test_case([10**6]*5, [10**6-1]*5]))  # Large values
    tc["hidden"].append(make_test_case([i for i in range(1, 21)], [i//2 for i in range(1, 21)]))  # Larger pattern

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case([random.randint(1, 50) for _ in range(8)], 
                                      [random.randint(1, 50) for _ in range(8)]))  # Small random
    tc["hidden"].append(make_test_case([i*5 for i in range(1, 11)], [i*3 for i in range(1, 11)]))  # Pattern
    tc["hidden"].append(make_test_case([random.randint(1, 200) for _ in range(12)], 
                                      [random.randint(1, 200) for _ in range(12)]))  # Medium random
    tc["hidden"].append(make_test_case([i*10 for i in range(1, 16)], [i*7 for i in range(1, 16)]))  # Pattern medium
    tc["hidden"].append(make_test_case([random.randint(1, 500) for _ in range(18)], 
                                      [random.randint(1, 500) for _ in range(18)]))  # Larger random
    tc["hidden"].append(make_test_case([i*20 for i in range(1, 21)], [i*15 for i in range(1, 21)]))  # Pattern large
    tc["hidden"].append(make_test_case([random.randint(1, 1000) for _ in range(25)], 
                                      [random.randint(1, 1000) for _ in range(25)]))  # Large random
    tc["hidden"].append(make_test_case([i*50 for i in range(1, 26)], [i*40 for i in range(1, 26)]))  # Pattern larger
    tc["hidden"].append(make_test_case([random.randint(1, 2000) for _ in range(30)], 
                                      [random.randint(1, 2000) for _ in range(30)]))  # Very large random
    tc["hidden"].append(make_test_case([i*100 for i in range(1, 31)], [i*80 for i in range(1, 31)]))  # Pattern max
    tc["hidden"].append(make_test_case([random.randint(1, 5000) for _ in range(35)], 
                                      [random.randint(1, 5000) for _ in range(35)]))  # Max random
    tc["hidden"].append(make_test_case([i*200 for i in range(1, 36)], [i*150 for i in range(1, 36)]))  # Max pattern

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))"""

# QUE-013: Rate limiter
QUE013_NEW_YAML = """def generate_yaml():
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
    tc["hidden"].append(make_test_case(1, 10, [1]*10)))  # Small window, high k
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

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))"""

# QUE-014: Deque alternating
QUE014_NEW_YAML = """def generate_yaml():
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

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))"""

# QUE-015: Light spread BFS (more complex - keep focused)
QUE015_NEW_YAML = """def generate_yaml():
    tc = {
        "samples": [
            make_test_case([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]]),
            make_test_case([[1, 1], [1, 1]]),
            make_test_case([[0, 0], [0, 0]])
        ],
        "public": [
            make_test_case([[1, 0], [0, 0]]),  # Single source
            make_test_case([[1, 0, 0], [0, 0, 0], [0, 0, 1]]),  # Two sources
            make_test_case([[1]*3 for _ in range(3)]),  # All lit
            make_test_case([[0]*3 for _ in range(3)]),  # None lit
            make_test_case([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # Diagonal
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case([[1]]))  # 1x1 lit
    tc["hidden"].append(make_test_case([[0]]))  # 1x1 unlit
    tc["hidden"].append(make_test_case([[1, 0]]))  # 1x2
    tc["hidden"].append(make_test_case([[1], [0]]))  # 2x1
    tc["hidden"].append(make_test_case([[1, 1], [1, 1]]))  # 2x2 all lit
    tc["hidden"].append(make_test_case([[0, 0], [0, 0]]))  # 2x2 none
    tc["hidden"].append(make_test_case([[1, 0], [0, 1]]))  # 2x2 diagonal
    tc["hidden"].append(make_test_case([[1, 0, 0], [0, 0, 0], [0, 0, 0]]))  # Corner only

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case([[1] + [0]*9]))  # 1x10 one source
    tc["hidden"].append(make_test_case([[1 if i == j else 0 for j in range(5)] for i in range(5)]))  # 5x5 diagonal
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(6)] for _ in range(6)]))  # 6x6 random
    tc["hidden"].append(make_test_case([[1]*8 for _ in range(8)]))  # 8x8 all lit
    tc["hidden"].append(make_test_case([[0]*8 for _ in range(8)]))  # 8x8 none
    tc["hidden"].append(make_test_case([[1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
                                       [0, 0, 0, 0, 0], [0, 0, 0, 0, 1]]))  # 5x5 corners
    tc["hidden"].append(make_test_case([[1 if (i+j) % 2 == 0 else 0 for j in range(7)] for i in range(7)]))  # Checkerboard
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(10)] for _ in range(10)]))  # 10x10 random

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case([[1, 0, 0], [0, 0, 0], [0, 0, 0]]))  # 3x3 one corner
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(4)] for _ in range(4)]))  # 4x4 random
    tc["hidden"].append(make_test_case([[1 if i == 0 else 0 for _ in range(5)] for i in range(5)]))  # 5x5 first row
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(5)] for _ in range(5)]))  # 5x5 random
    tc["hidden"].append(make_test_case([[1 if j == 0 else 0 for j in range(6)] for _ in range(6)]))  # 6x6 first col
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(7)] for _ in range(7)]))  # 7x7 random
    tc["hidden"].append(make_test_case([[1 if (i == 0 or j == 0) else 0 for j in range(8)] for i in range(8)]))  # 8x8 edges
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(8)] for _ in range(8)]))  # 8x8 random
    tc["hidden"].append(make_test_case([[1 if i < 3 else 0 for _ in range(9)] for i in range(9)]))  # 9x9 top rows
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(10)] for _ in range(10)]))  # 10x10 random
    tc["hidden"].append(make_test_case([[1 if (i+j) < 6 else 0 for j in range(12)] for i in range(12)]))  # 12x12 diagonal
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(12)] for _ in range(12)]))  # 12x12 random

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))"""

# QUE-016: Queue swap
QUE016_NEW_YAML = """def generate_yaml():
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

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))"""

def update_generator(problem_num, new_yaml_content):
    """Update a single generator file"""
    filepath = os.path.join(DSA_DIR, f"generate_que{problem_num:03d}.py")
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the generate_yaml function
    pattern = r'def generate_yaml\(\):.*?(?=\nif __name__|$)'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"❌ Could not find generate_yaml() in {filepath}")
        return False
    
    new_content = content[:match.start()] + new_yaml_content + "\n" + content[match.end():]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated generate_que{problem_num:03d}.py")
    return True

def main():
    print("Updating Queue generators 011-016...\n")
    
    updates = [
        (11, QUE011_NEW_YAML),
        (12, QUE012_NEW_YAML_SIMPLE),
        (13, QUE013_NEW_YAML),
        (14, QUE014_NEW_YAML),
        (15, QUE015_NEW_YAML),
        (16, QUE016_NEW_YAML)
    ]
    
    success_count = 0
    for prob_num, new_yaml in updates:
        if update_generator(prob_num, new_yaml):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Updated {success_count}/{len(updates)} generators successfully!")
    print(f"{'='*60}\n")
    
    if success_count == len(updates):
        print("✅ All updates complete!")
        print("\n🎯 Next steps:")
        print("1. Regenerate all Queue YAMLs: python regenerate_queues.py")
        print("2. Validate all tests: python test_topic_editorials.py QUEUES")
    else:
        print(f"⚠️  {len(updates) - success_count} generators failed to update")

if __name__ == "__main__":
    main()
