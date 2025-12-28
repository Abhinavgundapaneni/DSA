"""
Regenerate ALL Greedy test outputs using the editorial solutions.
This ensures tests match what the editorials actually produce.
"""

import yaml
import sys
import re
import subprocess
import tempfile
import os
from pathlib import Path

def extract_python_solution(editorial_file):
    """Extract Python solution from editorial markdown."""
    with open(editorial_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'### Python.*?```python\n(.*?)```'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1)
    return None

def run_solution(solution_code, test_input):
    """Run solution and return output."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(solution_code)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, temp_file],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return None, str(e)
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass

def regenerate_problem(problem_id, slug):
    """Regenerate test outputs for one problem."""
    print(f"\n{'='*60}")
    print(f"Processing {problem_id}")
    print(f"{'='*60}")
    
    editorial_path = Path(f"dsa-problems/Greedy/editorials/{problem_id}-{slug}.md")
    test_path = Path(f"dsa-problems/Greedy/testcases/{problem_id}-{slug}.yaml")
    
    if not editorial_path.exists():
        print(f"ERROR: Editorial not found")
        return 0
    
    if not test_path.exists():
        print(f"ERROR: Test file not found")
        return 0
    
    # Extract solution
    solution_code = extract_python_solution(editorial_path)
    if not solution_code:
        print(f"ERROR: No Python solution found")
        return 0
    
    # Load tests
    with open(test_path, 'r', encoding='utf-8') as f:
        test_data = yaml.safe_load(f)
    
    # Regenerate outputs
    total = 0
    failed = 0
    
    for category in ['samples', 'public', 'hidden']:
        if category not in test_data:
            continue
        
        for test in test_data[category]:
            output, error = run_solution(solution_code, test['input'])
            
            if error or output is None:
                print(f"  FAIL ({category}): {error[:100] if error else 'No output'}")
                failed += 1
            else:
                test['output'] = output
                total += 1
    
    # Save updated tests
    with open(test_path, 'w', encoding='utf-8') as f:
        yaml.dump(test_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"SUCCESS: Regenerated {total} outputs ({failed} failed)")
    return total

def main():
    """Regenerate all Greedy test outputs."""
    problems = [
        ("GRD-001", "campus-shuttle-driver-swaps"),
        ("GRD-002", "lab-kit-distribution"),
        ("GRD-003", "festival-stall-placement"),
        ("GRD-004", "library-power-backup"),
        ("GRD-005", "shuttle-overtime-minimizer"),
        ("GRD-006", "robotics-component-bundling-loss-quality"),
        ("GRD-007", "campus-wifi-expansion"),
        ("GRD-008", "exam-proctor-allocation"),
        ("GRD-009", "shuttle-refuel-with-refund"),
        ("GRD-010", "library-merge-queues"),
        ("GRD-011", "campus-event-ticket-caps"),
        ("GRD-012", "workshop-task-cooldown-priority"),
        ("GRD-013", "auditorium-seat-refunds"),
        ("GRD-014", "festival-bandwidth-split"),
        ("GRD-015", "robotics-median-after-batches-stale"),
        ("GRD-016", "shuttle-schedule-delay-minimizer"),
    ]
    
    total_success = 0
    for problem_id, slug in problems:
        count = regenerate_problem(problem_id, slug)
        if count > 0:
            total_success += 1
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {total_success}/{len(problems)} problems regenerated")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
