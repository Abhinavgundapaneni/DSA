"""Regenerate outputs for GRP-004, GRP-011, GRP-017."""
import yaml
import sys
from io import StringIO
import re

def extract_python_solution(editorial_path):
    """Extract Python solution from editorial markdown."""
    with open(editorial_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'```python\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        if 'def main():' in match:
            return match
    
    return None

def run_solution(solution_code, input_str):
    """Run solution code with given input and return output."""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    
    try:
        sys.stdin = StringIO(input_str)
        sys.stdout = StringIO()
        
        exec(solution_code, {'__name__': '__main__'})
        
        output = sys.stdout.getvalue().strip()
        return output
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return None
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def regenerate_problem(problem_id, slug):
    """Regenerate test outputs for a problem."""
    editorial_path = f"dsa-problems/Graphs/editorials/{problem_id}-{slug}.md"
    test_path = f"dsa-problems/Graphs/testcases/{problem_id}-{slug}.yaml"
    
    print(f"\nProcessing {problem_id}...")
    
    # Extract solution
    solution = extract_python_solution(editorial_path)
    if not solution:
        print(f"ERROR: No solution with main() found")
        return 0
    
    # Load tests
    with open(test_path, 'r', encoding='utf-8') as f:
        test_data = yaml.safe_load(f)
    
    # Regenerate outputs
    total = 0
    for category in ['samples', 'public', 'hidden']:
        for test in test_data[category]:
            output = run_solution(solution, test['input'])
            if output is not None:
                test['output'] = output
                total += 1
    
    # Save updated tests
    with open(test_path, 'w', encoding='utf-8') as f:
        yaml.dump(test_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"SUCCESS: Regenerated {total} test outputs")
    return total

if __name__ == "__main__":
    problems = [
        ("GRP-004", "seminar-bipartite-check-locked"),
        ("GRP-011", "library-fire-with-exhaustion"),
        ("GRP-017", "festival-maze-shortest-path"),
    ]
    
    for problem_id, slug in problems:
        regenerate_problem(problem_id, slug)
