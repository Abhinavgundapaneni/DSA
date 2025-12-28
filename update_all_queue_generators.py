"""
Script to systematically update all remaining Queue test generators (QUE-007 to QUE-016)
Expands each to 38 test cases (3 samples + 5 public + 30 hidden)
Removes large/stress tests, adds focused edge/corner/normal cases
"""
import os
import re

DSA_DIR = r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Queues\testcases\tc_generators"

# QUE-007: Sliding window instability
QUE007_NEW_YAML = """def generate_yaml():
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

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))"""

# QUE-008: Sliding window second minimum
QUE008_NEW_YAML = """def generate_yaml():
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

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))"""

# QUE-009: First negative in window
QUE009_NEW_YAML = """def generate_yaml():
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

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))"""

# QUE-010: Meeting rooms peak usage
QUE010_NEW_YAML = """def generate_yaml():
    tc = {
        "samples": [
            make_test_case([0, 4, 4], [5, 5, 9]),
            make_test_case([1, 2, 3], [2, 3, 4]),
            make_test_case([1, 1, 1], [2, 2, 2])
        ],
        "public": [
            make_test_case([0, 5, 10], [5, 10, 15]),  # No overlap
            make_test_case([0], [10**9]),  # Single meeting
            make_test_case([1] * 5, [10] * 5),  # All overlap
            make_test_case([i*10 for i in range(5)], [i*10+5 for i in range(5)]),  # No overlap pattern
            make_test_case([1, 2, 3, 4], [5, 6, 7, 8])  # Nested
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case([0], [1]))  # Single short
    tc["hidden"].append(make_test_case([1, 2], [3, 4]))  # Two no overlap
    tc["hidden"].append(make_test_case([1, 1], [5, 5]))  # Two full overlap
    tc["hidden"].append(make_test_case([1, 3, 5], [2, 4, 6]))  # Three no overlap
    tc["hidden"].append(make_test_case([1, 1, 1], [3, 3, 3]))  # Three all overlap
    tc["hidden"].append(make_test_case([0, 5], [10, 15]))  # Two separate ranges
    tc["hidden"].append(make_test_case([1, 5, 10], [4, 8, 12]))  # Partial overlap
    tc["hidden"].append(make_test_case([i for i in range(5)], [i+1 for i in range(5)]))  # Chain

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case([0, 0, 0], [10**9, 10**9, 10**9]))  # Extreme long overlapping
    tc["hidden"].append(make_test_case([i*10**6 for i in range(8)], [(i+1)*10**6 for i in range(8)]))  # Large times
    tc["hidden"].append(make_test_case([random.randint(0, 100) for _ in range(10)], 
                                      [random.randint(100, 200) for _ in range(10)]))  # Random non-overlap
    tc["hidden"].append(make_test_case([1]*10, [100]*10))  # Ten all overlap
    tc["hidden"].append(make_test_case([i*5 for i in range(12)], [i*5+2 for i in range(12)]))  # Partial chain
    tc["hidden"].append(make_test_case([0, 10, 20, 30], [40, 40, 40, 40]))  # Mixed overlap
    tc["hidden"].append(make_test_case([random.randint(0, 10**8) for _ in range(15)], 
                                      [random.randint(10**8, 2*10**8) for _ in range(15)]))  # Large random
    tc["hidden"].append(make_test_case([i for i in range(20)], [i+10 for i in range(20)]))  # Heavy overlap

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case([random.randint(0, 100) for _ in range(8)], 
                                      [random.randint(10, 120) for _ in range(8)]))  # Small random
    tc["hidden"].append(make_test_case([i*10 for i in range(10)], [i*10+15 for i in range(10)]))  # Pattern overlap
    tc["hidden"].append(make_test_case([random.randint(0, 200) for _ in range(12)], 
                                      [random.randint(50, 250) for _ in range(12)]))  # Medium random
    tc["hidden"].append(make_test_case([i*5 for i in range(15)], [i*5+7 for i in range(15)]))  # Pattern medium
    tc["hidden"].append(make_test_case([random.randint(0, 500) for _ in range(18)], 
                                      [random.randint(100, 600) for _ in range(18)]))  # Larger random
    tc["hidden"].append(make_test_case([i*3 for i in range(20)], [i*3+5 for i in range(20)]))  # Pattern large
    tc["hidden"].append(make_test_case([random.randint(0, 1000) for _ in range(25)], 
                                      [random.randint(500, 1500) for _ in range(25)]))  # Large random
    tc["hidden"].append(make_test_case([i*2 for i in range(28)], [i*2+4 for i in range(28)]))  # Even pattern
    tc["hidden"].append(make_test_case([random.randint(0, 2000) for _ in range(30)], 
                                      [random.randint(1000, 3000) for _ in range(30)]))  # Very large random
    tc["hidden"].append(make_test_case([i*4 for i in range(22)], [i*4+6 for i in range(22)]))  # Pattern varied
    tc["hidden"].append(make_test_case([random.randint(0, 5000) for _ in range(35)], 
                                      [random.randint(2500, 7500) for _ in range(35)]))  # Max random
    tc["hidden"].append(make_test_case([i for i in range(40)], [i+20 for i in range(40)]))  # Heavy sequential

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
    print("Updating Queue generators 007-010...\n")
    
    updates = [
        (7, QUE007_NEW_YAML),
        (8, QUE008_NEW_YAML),
        (9, QUE009_NEW_YAML),
        (10, QUE010_NEW_YAML)
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
    else:
        print(f"⚠️  {len(updates) - success_count} generators failed to update")

if __name__ == "__main__":
    main()
