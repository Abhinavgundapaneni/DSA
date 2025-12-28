"""Quick diagnosis of Graphs editorial issues."""

import re
import sys
from io import StringIO

def extract_python_solution(editorial_path):
    """Extract Python solution from editorial markdown."""
    with open(editorial_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'```python\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        if 'def main():' in match:
            return match
    
    return matches[0] if matches else None

def run_solution(solution_code, input_str):
    """Run solution and return output."""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    
    try:
        sys.stdin = StringIO(input_str)
        sys.stdout = StringIO()
        exec(solution_code, {'__name__': '__main__'})
        output = sys.stdout.getvalue().strip()
        return output
    except Exception as e:
        return f"ERROR: {e}"
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Test GRP-004
print("GRP-004:")
code = extract_python_solution("dsa-problems/Graphs/editorials/GRP-004-seminar-bipartite-check-locked.md")
test_input = """7
20
3 4
4 6
0 2
0 5
1 6
2 5
1 3
4 5
5 6
3 6
0 1
2 4
1 2
0 4
1 5
3 5
0 3
1 4
2 3
2 6"""
result = run_solution(code, test_input)
print(f"  Output: {result}")
print(f"  Expected: 7")

# Test GRP-005
print("\nGRP-005:")
code = extract_python_solution("dsa-problems/Graphs/editorials/GRP-005-robotics-cycle-detector.md")
test_input = """5
7
0 1
1 2
2 3
3 4
4 1
1 3
0 4"""
result = run_solution(code, test_input)
print(f"  Output: {result}")
print(f"  Expected: 3")
