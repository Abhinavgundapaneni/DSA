#!/usr/bin/env python3
"""
Batch test all DSA topic folders and generate comprehensive report.
"""
import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Import after encoding setup
import subprocess

def test_folder(folder_name, base_path):
    """Test a single folder and return results."""
    print(f"\n{'='*80}")
    print(f"Testing {folder_name}...")
    print(f"{'='*80}")
    
    try:
        result = subprocess.run(
            [sys.executable, 'test_topic_editorials.py', folder_name],
            capture_output=True,
            text=True,
            timeout=300,
            encoding='utf-8',
            errors='replace'
        )
        
        # Parse results from output
        output = result.stdout
        
        # Extract key metrics
        total_tests = 0
        passed = 0
        failed = 0
        perfect_count = 0
        
        for line in output.split('\n'):
            if 'Total Test Cases Executed:' in line:
                total_tests = int(line.split(':')[1].strip())
            elif 'Passed:' in line and '(' in line:
                passed = int(line.split(':')[1].split('(')[0].strip())
            elif 'Failed:' in line and '(' in line:
                failed = int(line.split(':')[1].split('(')[0].strip())
            elif 'Perfect Score (' in line:
                perfect_count = int(line.split('(')[1].split(' ')[0])
        
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        return {
            'folder': folder_name,
            'total_tests': total_tests,
            'passed': passed,
            'failed': failed,
            'success_rate': success_rate,
            'perfect_count': perfect_count,
            'status': 'OK' if total_tests > 0 else 'NO_TESTS'
        }
    
    except subprocess.TimeoutExpired:
        return {
            'folder': folder_name,
            'status': 'TIMEOUT',
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'success_rate': 0,
            'perfect_count': 0
        }
    except Exception as e:
        return {
            'folder': folder_name,
            'status': 'ERROR',
            'error': str(e),
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'success_rate': 0,
            'perfect_count': 0
        }


def main():
    base_path = Path(__file__).parent / 'dsa-problems'
    
    # List of all topic folders to test
    folders_to_test = [
        'AdvancedGraphs',
        'Arrays',
        'Bitwise',
        'DP',
        'Graphs',
        'GraphsBasics',
        'Greedy',
        'Hashing',
        'Heaps',
        'LinkedLists',
        'MathAdvanced',
        'NumberTheory',
        'Queues',
        'Recursion',
        'Sorting',
        'Stacks',
        'Strings',
        'StringsClassic',
        'Trees',
        'TreesDP',
        'Tries'
    ]
    
    print("="*80)
    print("COMPREHENSIVE DSA EDITORIAL SOLUTIONS TEST - ALL TOPICS")
    print("="*80)
    
    all_results = []
    
    for folder in folders_to_test:
        folder_path = base_path / folder
        if not folder_path.exists() or not (folder_path / 'editorials').exists():
            print(f"\nSkipping {folder} (folder not found or no editorials)")
            continue
        
        results = test_folder(folder, base_path)
        all_results.append(results)
    
    # Generate comprehensive summary
    print("\n\n" + "="*80)
    print("COMPREHENSIVE SUMMARY - ALL TOPICS")
    print("="*80)
    
    grand_total_tests = sum(r['total_tests'] for r in all_results)
    grand_total_passed = sum(r['passed'] for r in all_results)
    grand_total_failed = sum(r['failed'] for r in all_results)
    
    print(f"\nGRAND TOTAL ACROSS ALL TOPICS:")
    print(f"  Total Test Cases: {grand_total_tests}")
    print(f"  Passed: {grand_total_passed} ({100*grand_total_passed/grand_total_tests:.1f}%)" if grand_total_tests > 0 else "  Passed: 0")
    print(f"  Failed: {grand_total_failed} ({100*grand_total_failed/grand_total_tests:.1f}%)" if grand_total_tests > 0 else "  Failed: 0")
    
    # Summary by topic
    print(f"\n{'='*80}")
    print("RESULTS BY TOPIC")
    print(f"{'='*80}\n")
    
    perfect_topics = []
    good_topics = []  # >90%
    moderate_topics = []  # 50-90%
    poor_topics = []  # <50%
    
    for r in sorted(all_results, key=lambda x: x['success_rate'], reverse=True):
        if r['total_tests'] == 0:
            continue
        
        status_symbol = "PASS" if r['success_rate'] == 100 else "FAIL" if r['success_rate'] < 50 else "WARN"
        
        print(f"{r['folder']:20} | Tests: {r['total_tests']:4} | "
              f"Passed: {r['passed']:4} ({r['success_rate']:5.1f}%) | "
              f"Perfect: {r['perfect_count']:2} | {status_symbol}")
        
        if r['success_rate'] == 100:
            perfect_topics.append(r['folder'])
        elif r['success_rate'] >= 90:
            good_topics.append(r['folder'])
        elif r['success_rate'] >= 50:
            moderate_topics.append(r['folder'])
        else:
            poor_topics.append(r['folder'])
    
    # Category summary
    print(f"\n{'='*80}")
    print("TOPICS BY PERFORMANCE")
    print(f"{'='*80}")
    
    if perfect_topics:
        print(f"\nPERFECT (100%): {len(perfect_topics)} topics")
        for topic in perfect_topics:
            print(f"  - {topic}")
    
    if good_topics:
        print(f"\nGOOD (90-99%): {len(good_topics)} topics")
        for topic in good_topics:
            print(f"  - {topic}")
    
    if moderate_topics:
        print(f"\nMODERATE (50-89%): {len(moderate_topics)} topics")
        for topic in moderate_topics:
            print(f"  - {topic}")
    
    if poor_topics:
        print(f"\nPOOR (<50%): {len(poor_topics)} topics")
        for topic in poor_topics:
            print(f"  - {topic}")
    
    print(f"\n{'='*80}")
    print("TEST COMPLETE")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
