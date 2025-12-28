"""
Comprehensive test generator for all empty Sorting problems (SRT-004 through SRT-016).
Generates test inputs based on problem constraints, then runs editorial solutions to get outputs.
"""

import yaml
import random
import sys
from io import StringIO
import re

def extract_python_solution(editorial_path):
    """Extract Python solution from editorial markdown."""
    with open(editorial_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find Python code block
    pattern = r'```python\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    if not matches:
        return None
    
    # Return the solution (usually the first or second code block)
    for match in matches:
        if 'def main():' in match:
            return match
    
    return matches[0] if matches else None

def run_solution(solution_code, input_str):
    """Run solution code with given input and return output."""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    
    try:
        sys.stdin = StringIO(input_str)
        sys.stdout = StringIO()
        
        # Execute the solution
        exec(solution_code, {'__name__': '__main__'})
        
        output = sys.stdout.getvalue().strip()
        return output
    except Exception as e:
        print(f"Error running solution: {e}", file=sys.stderr)
        return None
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def generate_srt004_tests():
    """SRT-004: Min Inversions One Swap
    Input: n, array of n integers
    Constraints: n <= 100,000, values <= 10^9
    """
    tests = []
    
    # Sample test
    tests.append("3\n3 1 2")
    
    # Public tests (5)
    for _ in range(5):
        n = random.randint(2, 100)
        arr = [random.randint(1, 1000) for _ in range(n)]
        tests.append(f"{n}\n{' '.join(map(str, arr))}")
    
    # Hidden tests (30)
    for i in range(30):
        if i < 10:
            n = random.randint(100, 1000)
        else:
            n = random.randint(1000, 100000)
        arr = [random.randint(1, 10**9) for _ in range(n)]
        tests.append(f"{n}\n{' '.join(map(str, arr))}")
    
    return tests

def generate_srt005_tests():
    """SRT-005: Two Pointer Closest Target
    Input: n, array, target
    Constraints: n <= 100,000
    """
    tests = []
    
    # Sample
    tests.append("4\n1 3 5 7\n8")
    
    # Public (5)
    for _ in range(5):
        n = random.randint(2, 50)
        arr = sorted([random.randint(1, 100) for _ in range(n)])
        target = random.randint(1, 200)
        tests.append(f"{n}\n{' '.join(map(str, arr))}\n{target}")
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            n = random.randint(50, 1000)
        else:
            n = random.randint(1000, 100000)
        arr = sorted([random.randint(-10**9, 10**9) for _ in range(n)])
        target = random.randint(-2*10**9, 2*10**9)
        tests.append(f"{n}\n{' '.join(map(str, arr))}\n{target}")
    
    return tests

def generate_srt006_tests():
    """SRT-006: K Sorted Array Min Swaps
    Input: n k, array
    Constraints: n <= 100,000
    """
    tests = []
    
    # Sample
    tests.append("5 2\n3 1 2 5 4")
    
    # Public (5)
    for _ in range(5):
        n = random.randint(2, 50)
        k = random.randint(1, min(n-1, 10))
        arr = list(range(1, n+1))
        random.shuffle(arr)
        tests.append(f"{n} {k}\n{' '.join(map(str, arr))}")
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            n = random.randint(50, 1000)
        else:
            n = random.randint(1000, 100000)
        k = random.randint(1, min(n-1, 100))
        arr = list(range(1, n+1))
        random.shuffle(arr)
        tests.append(f"{n} {k}\n{' '.join(map(str, arr))}")
    
    return tests

def generate_srt007_tests():
    """SRT-007: Search Rotated Duplicates Parity
    Input: n, rotated array, target x
    Constraints: n <= 100,000
    """
    tests = []
    
    # Sample
    tests.append("5\n4 5 1 2 3\n2")
    
    # Public (5)
    for _ in range(5):
        n = random.randint(3, 50)
        arr = sorted([random.randint(1, 20) for _ in range(n)])
        pivot = random.randint(1, n-1)
        arr = arr[pivot:] + arr[:pivot]
        x = random.choice(arr + [random.randint(1, 20)])
        tests.append(f"{n}\n{' '.join(map(str, arr))}\n{x}")
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            n = random.randint(50, 1000)
        else:
            n = random.randint(1000, 100000)
        arr = sorted([random.randint(1, 1000) for _ in range(n)])
        pivot = random.randint(1, n-1)
        arr = arr[pivot:] + arr[:pivot]
        x = random.choice(arr + [random.randint(1, 1000)])
        tests.append(f"{n}\n{' '.join(map(str, arr))}\n{x}")
    
    return tests

def generate_srt008_tests():
    """SRT-008: Balanced Range Covering K Lists
    Input: k, then k lists (each: m, then m values)
    Constraints: k <= 10, total elements <= 200,000
    """
    tests = []
    
    # Sample
    tests.append("3\n3\n1 3 5\n2\n2 4\n4\n1 2 3 4")
    
    # Public (5)
    for _ in range(5):
        k = random.randint(2, 5)
        lines = [str(k)]
        for _ in range(k):
            m = random.randint(1, 10)
            lst = sorted([random.randint(1, 50) for _ in range(m)])
            lines.append(str(m))
            lines.append(' '.join(map(str, lst)))
        tests.append('\n'.join(lines))
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            k = random.randint(2, 10)
            total_budget = 1000
        else:
            k = random.randint(5, 10)
            total_budget = 200000
        
        lines = [str(k)]
        for j in range(k):
            m = random.randint(1, total_budget // k)
            lst = sorted([random.randint(1, 10**9) for _ in range(m)])
            lines.append(str(m))
            lines.append(' '.join(map(str, lst)))
        tests.append('\n'.join(lines))
    
    return tests

def generate_srt009_tests():
    """SRT-009: Weighted Median Two Sorted
    Input: n m, array A, array B, wA wB
    Constraints: n, m <= 100,000
    """
    tests = []
    
    # Sample
    tests.append("2 3\n1 3\n2 4 5\n2 3")
    
    # Public (5)
    for _ in range(5):
        n = random.randint(1, 20)
        m = random.randint(1, 20)
        a = sorted([random.randint(1, 100) for _ in range(n)])
        b = sorted([random.randint(1, 100) for _ in range(m)])
        wa = random.randint(1, 10)
        wb = random.randint(1, 10)
        tests.append(f"{n} {m}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n{wa} {wb}")
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            n = random.randint(10, 1000)
            m = random.randint(10, 1000)
        else:
            n = random.randint(1000, 100000)
            m = random.randint(1000, 100000)
        a = sorted([random.randint(-10**9, 10**9) for _ in range(n)])
        b = sorted([random.randint(-10**9, 10**9) for _ in range(m)])
        wa = random.randint(1, 1000)
        wb = random.randint(1, 1000)
        tests.append(f"{n} {m}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n{wa} {wb}")
    
    return tests

def generate_srt010_tests():
    """SRT-010: Sort Colors Limited Swaps
    Input: n, array of 0/1/2, max swaps S
    Constraints: n <= 200,000
    """
    tests = []
    
    # Sample
    tests.append("5\n2 1 0 2 1\n3")
    
    # Public (5)
    for _ in range(5):
        n = random.randint(3, 50)
        arr = [random.choice([0, 1, 2]) for _ in range(n)]
        s = random.randint(0, n * (n-1) // 2)
        tests.append(f"{n}\n{' '.join(map(str, arr))}\n{s}")
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            n = random.randint(50, 1000)
        else:
            n = random.randint(1000, 200000)
        arr = [random.choice([0, 1, 2]) for _ in range(n)]
        s = random.randint(0, min(n * n, 10**18))
        tests.append(f"{n}\n{' '.join(map(str, arr))}\n{s}")
    
    return tests

def generate_srt011_tests():
    """SRT-011: Longest Consecutive One Change
    Input: n, array
    Constraints: n <= 100,000
    """
    tests = []
    
    # Sample
    tests.append("5\n1 2 4 5 6")
    
    # Public (5)
    for _ in range(5):
        n = random.randint(2, 50)
        arr = [random.randint(1, 100) for _ in range(n)]
        tests.append(f"{n}\n{' '.join(map(str, arr))}")
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            n = random.randint(50, 1000)
        else:
            n = random.randint(1000, 100000)
        arr = [random.randint(1, 10**9) for _ in range(n)]
        tests.append(f"{n}\n{' '.join(map(str, arr))}")
    
    return tests

def generate_srt012_tests():
    """SRT-012: Count Within Threshold After Self
    Input: n t, array
    Constraints: n <= 200,000
    """
    tests = []
    
    # Sample
    tests.append("4 5\n10 3 8 15")
    
    # Public (5)
    for _ in range(5):
        n = random.randint(2, 50)
        t = random.randint(1, 100)
        arr = [random.randint(1, 100) for _ in range(n)]
        tests.append(f"{n} {t}\n{' '.join(map(str, arr))}")
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            n = random.randint(50, 1000)
        else:
            n = random.randint(1000, 200000)
        t = random.randint(1, 10**9)
        arr = [random.randint(-10**9, 10**9) for _ in range(n)]
        tests.append(f"{n} {t}\n{' '.join(map(str, arr))}")
    
    return tests

def generate_srt013_tests():
    """SRT-013: Closest Pair Sorted Circular
    Input: n, rotated sorted array, target
    Constraints: n <= 100,000
    """
    tests = []
    
    # Sample
    tests.append("4\n1 3 6 10\n7")
    
    # Public (5)
    for _ in range(5):
        n = random.randint(2, 50)
        arr = sorted([random.randint(1, 100) for _ in range(n)])
        pivot = random.randint(0, n-1)
        arr = arr[pivot:] + arr[:pivot]
        target = random.randint(1, 200)
        tests.append(f"{n}\n{' '.join(map(str, arr))}\n{target}")
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            n = random.randint(50, 1000)
        else:
            n = random.randint(1000, 100000)
        arr = sorted([random.randint(-10**9, 10**9) for _ in range(n)])
        pivot = random.randint(0, n-1)
        arr = arr[pivot:] + arr[:pivot]
        target = random.randint(-2*10**9, 2*10**9)
        tests.append(f"{n}\n{' '.join(map(str, arr))}\n{target}")
    
    return tests

def generate_srt014_tests():
    """SRT-014: Min Ops Make Alternating
    Input: n, array
    Constraints: n <= 100,000
    """
    tests = []
    
    # Sample
    tests.append("5\n1 2 3 4 5")
    
    # Public (5)
    for _ in range(5):
        n = random.randint(2, 50)
        arr = [random.randint(1, 100) for _ in range(n)]
        tests.append(f"{n}\n{' '.join(map(str, arr))}")
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            n = random.randint(50, 1000)
        else:
            n = random.randint(1000, 100000)
        arr = [random.randint(1, 10**9) for _ in range(n)]
        tests.append(f"{n}\n{' '.join(map(str, arr))}")
    
    return tests

def generate_srt015_tests():
    """SRT-015: Kth Smallest Triple Sum
    Input: n k, array
    Constraints: n <= 100,000, k <= n choose 3
    """
    tests = []
    
    # Sample
    tests.append("4 2\n1 2 3 4")
    
    # Public (5)
    for _ in range(5):
        n = random.randint(3, 20)
        k = random.randint(1, min(100, n*(n-1)*(n-2)//6))
        arr = [random.randint(1, 100) for _ in range(n)]
        tests.append(f"{n} {k}\n{' '.join(map(str, arr))}")
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            n = random.randint(20, 200)
            k = random.randint(1, min(10000, n*(n-1)*(n-2)//6))
        else:
            n = random.randint(200, 1000)
            k = random.randint(1, min(10**9, n*(n-1)*(n-2)//6))
        arr = [random.randint(-10**9, 10**9) for _ in range(n)]
        tests.append(f"{n} {k}\n{' '.join(map(str, arr))}")
    
    return tests

def generate_srt016_tests():
    """SRT-016: Locate Peak Limited Queries
    Input: n q, array
    Constraints: n <= 100,000, q <= 20
    """
    tests = []
    
    # Sample
    tests.append("5 20\n1 3 2 5 4")
    
    # Public (5)
    for _ in range(5):
        n = random.randint(3, 50)
        q = 20
        arr = [random.randint(1, 100) for _ in range(n)]
        tests.append(f"{n} {q}\n{' '.join(map(str, arr))}")
    
    # Hidden (30)
    for i in range(30):
        if i < 15:
            n = random.randint(50, 1000)
        else:
            n = random.randint(1000, 100000)
        q = 20
        arr = [random.randint(1, 10**9) for _ in range(n)]
        tests.append(f"{n} {q}\n{' '.join(map(str, arr))}")
    
    return tests

def generate_and_save_tests(problem_id, problem_slug, test_generator):
    """Generate tests and save to YAML file."""
    editorial_path = f"dsa-problems/Sorting/editorials/{problem_id}-{problem_slug}.md"
    test_path = f"dsa-problems/Sorting/testcases/{problem_id}-{problem_slug}.yaml"
    
    print(f"\n{'='*60}")
    print(f"Processing {problem_id}")
    print(f"{'='*60}")
    
    # Extract solution
    solution = extract_python_solution(editorial_path)
    if not solution:
        print(f"ERROR: Could not extract Python solution from {editorial_path}")
        return 0
    
    # Generate test inputs
    print(f"Generating test inputs...")
    test_inputs = test_generator()
    
    if len(test_inputs) < 36:  # 1 sample + 5 public + 30 hidden
        print(f"WARNING: Only generated {len(test_inputs)} tests, expected 36")
    
    # Generate test outputs
    print(f"Running editorial solution on {len(test_inputs)} test inputs...")
    test_cases = []
    
    for i, input_str in enumerate(test_inputs):
        try:
            output = run_solution(solution, input_str)
            if output is None:
                print(f"  WARNING: Test {i+1} failed to run")
                continue
            
            test_cases.append({'input': input_str, 'output': output})
            
            if (i+1) % 10 == 0:
                print(f"  OK: Completed {i+1}/{len(test_inputs)} tests")
        except Exception as e:
            print(f"  ERROR on test {i+1}: {e}")
    
    if not test_cases:
        print(f"ERROR: No test cases generated")
        return 0
    
    # Read existing YAML to get problem_id
    with open(test_path, 'r', encoding='utf-8') as f:
        existing = yaml.safe_load(f)
    
    # Create YAML structure
    yaml_data = {
        'problem_id': existing['problem_id'],
        'samples': test_cases[:1],
        'public': test_cases[1:6],
        'hidden': test_cases[6:36]
    }
    
    # Write to file
    with open(test_path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    total_tests = len(test_cases)
    print(f"SUCCESS: Generated {total_tests} tests: {len(yaml_data['samples'])} samples, {len(yaml_data['public'])} public, {len(yaml_data['hidden'])} hidden")
    
    return total_tests

def main():
    random.seed(42)  # For reproducibility
    
    problems = [
        ("SRT-004", "min-inversions-one-swap", generate_srt004_tests),
        ("SRT-005", "two-pointer-closest-target", generate_srt005_tests),
        ("SRT-006", "k-sorted-array-min-swaps", generate_srt006_tests),
        ("SRT-007", "search-rotated-duplicates-parity", generate_srt007_tests),
        ("SRT-008", "balanced-range-covering-k-lists", generate_srt008_tests),
        ("SRT-009", "weighted-median-two-sorted", generate_srt009_tests),
        ("SRT-010", "sort-colors-limited-swaps", generate_srt010_tests),
        ("SRT-011", "longest-consecutive-one-change", generate_srt011_tests),
        ("SRT-012", "count-within-threshold-after-self", generate_srt012_tests),
        ("SRT-013", "closest-pair-sorted-circular", generate_srt013_tests),
        ("SRT-014", "min-ops-make-alternating", generate_srt014_tests),
        ("SRT-015", "kth-smallest-triple-sum", generate_srt015_tests),
        ("SRT-016", "locate-peak-limited-queries", generate_srt016_tests),
    ]
    
    total = 0
    successful = 0
    
    for problem_id, slug, generator in problems:
        try:
            count = generate_and_save_tests(problem_id, slug, generator)
            total += 1
            if count > 0:
                successful += 1
        except Exception as e:
            print(f"ERROR: Failed to process {problem_id}: {e}")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total problems processed: {total}")
    print(f"Successfully generated: {successful}")
    print(f"Failed: {total - successful}")

if __name__ == "__main__":
    main()
