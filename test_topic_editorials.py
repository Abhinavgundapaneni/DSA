#!/usr/bin/env python3
"""
Universal test script for testing editorial solutions in any DSA topic folder.
Tests all problems in a specified folder against their hidden test cases.
"""
import os
import re
import sys
import yaml
import subprocess
import tempfile
from pathlib import Path
from collections import defaultdict

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def extract_python_solution(editorial_file):
    """Extract Python solution from editorial markdown."""
    try:
        with open(editorial_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None
    
    # Find Python code block in editorial - multiple patterns
    patterns = [
        r'### Python.*?```python\n(.*?)```',
        r'## Python Solution.*?```python\n(.*?)```',
        r'##\s*Python.*?```python\n(.*?)```',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1)
    
    return None


def run_test_case(solution_code, test_input, timeout=10):
    """Run a single test case through the solution."""
    # Create temporary file with solution
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(solution_code)
        temp_file = f.name
    
    try:
        # Run the solution with test input
        result = subprocess.run(
            [sys.executable, temp_file],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return result.stdout.strip(), result.stderr.strip() if result.stderr else None, result.returncode
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT", -1
    except Exception as e:
        return None, str(e), -1
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass


def normalize_output(output):
    """Normalize output for comparison."""
    if output is None:
        return ""
    # Convert to string if it's not already
    if not isinstance(output, str):
        output = str(output)
    return output.strip()


def test_problem(prob_prefix, base_path):
    """Test all test cases for a single problem."""
    editorial_path = base_path / 'editorials'
    testcase_path = base_path / 'testcases'
    
    if not editorial_path.exists() or not testcase_path.exists():
        return {'status': 'FOLDER_NOT_FOUND', 'passed': 0, 'failed': 0, 'errors': [], 'total': 0}
    
    # Find files
    editorial_files = list(editorial_path.glob(f'{prob_prefix}*.md'))
    testcase_files = list(testcase_path.glob(f'{prob_prefix}*.yaml'))
    
    if not editorial_files:
        return {'status': 'EDITORIAL_NOT_FOUND', 'passed': 0, 'failed': 0, 'errors': [], 'total': 0}
    
    if not testcase_files:
        return {'status': 'TESTCASES_NOT_FOUND', 'passed': 0, 'failed': 0, 'errors': [], 'total': 0}
    
    editorial_file = editorial_files[0]
    testcase_file = testcase_files[0]
    
    # Extract solution
    solution_code = extract_python_solution(editorial_file)
    if not solution_code:
        return {'status': 'NO_SOLUTION', 'passed': 0, 'failed': 0, 'errors': [], 'total': 0}
    
    # Load test cases
    try:
        with open(testcase_file, 'r', encoding='utf-8') as f:
            tc_data = yaml.safe_load(f)
    except Exception as e:
        return {'status': 'YAML_ERROR', 'passed': 0, 'failed': 0, 'errors': [str(e)], 'total': 0}
    
    # Run all test cases
    results = {
        'status': 'OK', 
        'passed': 0, 
        'failed': 0, 
        'errors': [],
        'total': 0,
        'by_category': {
            'samples': {'passed': 0, 'failed': 0, 'total': 0},
            'public': {'passed': 0, 'failed': 0, 'total': 0},
            'hidden': {'passed': 0, 'failed': 0, 'total': 0}
        }
    }
    
    for category in ['samples', 'public', 'hidden']:
        if category not in tc_data or not tc_data[category]:
            continue
        
        for idx, tc in enumerate(tc_data[category]):
            tc_id = f"{category}[{idx}]"
            test_input = tc['input']
            expected_output = normalize_output(tc['output'])
            
            results['total'] += 1
            results['by_category'][category]['total'] += 1
            
            actual_output, error, returncode = run_test_case(solution_code, test_input)
            actual_output = normalize_output(actual_output)
            
            if error:
                results['failed'] += 1
                results['by_category'][category]['failed'] += 1
                results['errors'].append({
                    'tc_id': tc_id,
                    'error': error[:500],
                    'type': 'RUNTIME_ERROR',
                    'returncode': returncode
                })
            elif actual_output != expected_output:
                results['failed'] += 1
                results['by_category'][category]['failed'] += 1
                results['errors'].append({
                    'tc_id': tc_id,
                    'expected': expected_output[:200],
                    'actual': actual_output[:200] if actual_output else 'None',
                    'type': 'WRONG_ANSWER'
                })
            else:
                results['passed'] += 1
                results['by_category'][category]['passed'] += 1
    
    return results


def get_problem_prefixes(folder_path):
    """Get all problem prefixes from a folder."""
    editorial_path = folder_path / 'editorials'
    if not editorial_path.exists():
        return []
    
    # Get all editorial files and extract prefixes
    prefixes = set()
    for file in editorial_path.glob('*.md'):
        # Extract prefix like ARR-001, BIT-001, etc.
        match = re.match(r'([A-Z]+-\d+)', file.stem)
        if match:
            prefixes.add(match.group(1))
    
    return sorted(prefixes)


def print_detailed_results(prob_id, results):
    """Print detailed results for a problem."""
    if results['status'] == 'EDITORIAL_NOT_FOUND':
        print(f"  ⚠️  Editorial file not found")
        return
    
    if results['status'] == 'TESTCASES_NOT_FOUND':
        print(f"  ⚠️  Test case file not found")
        return
    
    if results['status'] == 'NO_SOLUTION':
        print(f"  ⚠️  No Python solution found in editorial")
        return
    
    if results['status'] == 'YAML_ERROR':
        print(f"  ❌ YAML parsing error")
        return
    
    total = results['total']
    passed = results['passed']
    failed = results['failed']
    
    # Status emoji
    if failed == 0:
        status = "✅"
    else:
        status = "❌"
    
    print(f"  {status} Total: {passed}/{total} passed")
    
    # Breakdown by category
    for category in ['samples', 'public', 'hidden']:
        cat_data = results['by_category'][category]
        if cat_data['total'] > 0:
            cat_passed = cat_data['passed']
            cat_total = cat_data['total']
            cat_status = "✅" if cat_data['failed'] == 0 else "❌"
            print(f"     {cat_status} {category.capitalize()}: {cat_passed}/{cat_total}")
    
    # Show first few errors
    if results['errors']:
        print(f"\n     First errors:")
        for error in results['errors'][:3]:
            print(f"       • {error['tc_id']}: {error['type']}")
            if error['type'] == 'WRONG_ANSWER':
                print(f"         Expected: {error['expected'][:80]}")
                print(f"         Actual:   {error['actual'][:80]}")
            elif error['type'] == 'RUNTIME_ERROR':
                print(f"         Error: {error['error'][:150]}")


def test_topic_folder(topic_name, base_path):
    """Test all problems in a topic folder."""
    folder_path = base_path / topic_name
    
    if not folder_path.exists():
        print(f"❌ Folder not found: {folder_path}")
        return None
    
    print("="*80)
    print(f"{topic_name.upper()} - EDITORIAL SOLUTIONS TEST")
    print("Testing against ALL test cases (samples, public, AND hidden)")
    print("="*80)
    
    # Get all problem prefixes
    problem_prefixes = get_problem_prefixes(folder_path)
    
    if not problem_prefixes:
        print(f"\n⚠️  No problems found in {topic_name}/editorials/")
        return None
    
    print(f"\nFound {len(problem_prefixes)} problems to test\n")
    
    all_results = {}
    total_passed = 0
    total_failed = 0
    total_tests = 0
    
    # Test each problem
    for prob_id in problem_prefixes:
        print(f"{prob_id}: Testing...")
        
        try:
            results = test_problem(prob_id, folder_path)
            all_results[prob_id] = results
            
            total_passed += results['passed']
            total_failed += results['failed']
            total_tests += results['total']
            
            print_detailed_results(prob_id, results)
        
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            all_results[prob_id] = {'status': 'ERROR', 'error': str(e), 'passed': 0, 'failed': 0, 'total': 0}
    
    # Summary
    print(f"\n\n{'='*80}")
    print(f"{topic_name.upper()} - FINAL SUMMARY")
    print(f"{'='*80}")
    print(f"\nTotal Test Cases Executed: {total_tests}")
    if total_tests > 0:
        print(f"✅ Passed: {total_passed} ({100*total_passed/total_tests:.1f}%)")
        print(f"❌ Failed: {total_failed} ({100*total_failed/total_tests:.1f}%)")
    else:
        print("⚠️  No tests executed")
    
    # Summary by problem
    print(f"\n{'='*80}")
    print("SUMMARY BY PROBLEM")
    print(f"{'='*80}")
    
    perfect_problems = []
    failed_problems = []
    no_solution_problems = []
    
    for prob_id, results in sorted(all_results.items()):
        if results['status'] == 'NO_SOLUTION':
            no_solution_problems.append(prob_id)
        elif results['failed'] == 0 and results['total'] > 0:
            perfect_problems.append(prob_id)
        elif results['failed'] > 0:
            failed_problems.append((prob_id, results['failed'], results['total']))
    
    if perfect_problems:
        print(f"\n✅ Perfect Score ({len(perfect_problems)} problems):")
        for prob_id in perfect_problems:
            r = all_results[prob_id]
            print(f"   {prob_id}: {r['passed']}/{r['total']} (all hidden tests passed)")
    
    if failed_problems:
        print(f"\n❌ Problems with Failures ({len(failed_problems)} problems):")
        for prob_id, failed, total in failed_problems:
            r = all_results[prob_id]
            print(f"   {prob_id}: {r['passed']}/{total} passed ({failed} failed)")
            hidden_failed = r['by_category']['hidden']['failed']
            if hidden_failed > 0:
                print(f"      └─ Hidden tests: {hidden_failed}/{r['by_category']['hidden']['total']} failed")
    
    if no_solution_problems:
        print(f"\n⚠️  No Solution Found ({len(no_solution_problems)} problems):")
        for prob_id in no_solution_problems:
            print(f"   {prob_id}")
    
    # Final verdict
    print(f"\n{'='*80}")
    if total_failed == 0 and total_tests > 0:
        print(f"🎉 ALL {total_tests} TEST CASES PASSED! Editorial solutions are 100% correct!")
    elif total_tests == 0:
        print("⚠️  No tests were executed")
    else:
        print(f"⚠️  {total_failed}/{total_tests} test cases failed")
        print(f"   Success rate: {100*total_passed/total_tests:.1f}%")
    print(f"{'='*80}\n")
    
    return {
        'topic': topic_name,
        'total_tests': total_tests,
        'passed': total_passed,
        'failed': total_failed,
        'perfect_count': len(perfect_problems),
        'failed_count': len(failed_problems),
        'no_solution_count': len(no_solution_problems),
        'problem_count': len(problem_prefixes)
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_topic_editorials.py <topic_folder_name>")
        print("\nExample: python test_topic_editorials.py Arrays")
        print("         python test_topic_editorials.py Bitwise")
        print("         python test_topic_editorials.py DP")
        sys.exit(1)
    
    topic_name = sys.argv[1]
    base_path = Path(__file__).parent / 'dsa-problems'
    
    if not base_path.exists():
        print(f"❌ Error: Path does not exist: {base_path}")
        sys.exit(1)
    
    test_topic_folder(topic_name, base_path)


if __name__ == '__main__':
    main()
