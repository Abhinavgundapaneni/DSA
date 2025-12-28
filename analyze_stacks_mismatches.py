#!/usr/bin/env python3
"""
Comprehensive Stacks Problem Analysis and Fix
Compares problem statements with test cases and determines correct approach
"""
import yaml
from pathlib import Path

problems_dir = Path(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Stacks')

# Analyze each problem
issues = []

print("=" * 80)
print("STACK PROBLEMS: PROBLEM VS TEST CASE ANALYSIS")
print("=" * 80)

for i in range(2, 17):
    problem_id = f"STK-{i:03d}"
    
    # Find problem and test case files
    problem_files = list((problems_dir / 'problems').glob(f'{problem_id}-*.md'))
    test_files = list((problems_dir / 'testcases').glob(f'{problem_id}-*.yaml'))
    
    if not problem_files or not test_files:
        continue
        
    problem_file = problem_files[0]
    test_file = test_files[0]
    
    # Read problem statement (first 100 lines)
    problem_text = problem_file.read_text(encoding='utf-8')[:3000]
    
    # Read test cases
    with open(test_file, encoding='utf-8') as f:
        tc = yaml.safe_load(f)
    
    sample = tc['samples'][0] if tc['samples'] else None
    
    print(f"\n{problem_id}: {problem_file.stem}")
    print("-" * 80)
    
    if sample:
        print(f"Test Input:  {repr(sample['input'][:80])}")
        print(f"Test Output: {repr(sample['output'][:80])}")
    
    # Extract key phrases from problem statement
    if '## Problem Statement' in problem_text:
        stmt_start = problem_text.index('## Problem Statement')
        stmt_end = problem_text.find('##', stmt_start + 20)
        stmt = problem_text[stmt_start:stmt_end if stmt_end > 0 else stmt_start+500]
        print(f"Problem Says: {stmt[22:200].strip()}...")
    
    # Specific analysis
    if problem_id == 'STK-002':
        print("⚠️  MISMATCH: Problem says 'true/false for wildcard', test shows numbers")
        issues.append((problem_id, "Test cases don't match problem - shows min deletions not true/false"))
    
    elif problem_id == 'STK-003':
        print("⚠️  MISMATCH: Problem says 'remove even-sum pairs', test shows 'value,weight' pairs")
        issues.append((problem_id, "Test cases show simple deduplication, not even-sum removal"))
    
    elif problem_id == 'STK-005':
        if sample and '\\n' in sample['input']:
            lines = sample['input'].split('\\n')
            if len(lines[0].split()) == 1:  # Only has n, not n and w
                print("⚠️  MISMATCH: Problem needs 'n w', test only has 'n'")
                issues.append((problem_id, "Test missing width parameter w"))
    
    elif problem_id == 'STK-007':
        if sample and isinstance(sample['output'], str) and ' ' not in sample['output'].strip():
            print("⚠️  MISMATCH: Problem says 'n integers', test shows single number")
            issues.append((problem_id, "Test shows count, not array of wait steps"))
    
    elif problem_id == 'STK-009':
        if sample and '\\n' in sample['input']:
            lines = sample['input'].split('\\n')
            if len(lines) == 2 and len(lines[0].split()) == 2:
                print("⚠️  LIKELY: This is sliding window minimum, not min-stack operations")
                issues.append((problem_id, "Test format suggests sliding window, not operations"))

print("\n" + "=" * 80)
print(f"SUMMARY: Found {len(issues)} problems with mismatches")
print("=" * 80)

for pid, issue in issues:
    print(f"{pid}: {issue}")

print("\nRECOMMENDATION:")
print("Most problems have test cases that represent SIMPLER, MORE STANDARD problems")
print("than what the problem statements describe. The editorials were written for the")
print("complex problem statements, but test cases test simpler variants.")
print("\nBEST APPROACH: Regenerate test cases to match the problem statements,")
print("since the problem statements are more interesting and educational.")
