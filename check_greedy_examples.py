import re
import os

# List of all Greedy problem files
problem_files = [
    "dsa-problems/Greedy/problems/GRD-001-campus-shuttle-driver-swaps.md",
    "dsa-problems/Greedy/problems/GRD-002-lab-kit-distribution.md",
    "dsa-problems/Greedy/problems/GRD-003-festival-stall-placement.md",
    "dsa-problems/Greedy/problems/GRD-004-library-power-backup.md",
    "dsa-problems/Greedy/problems/GRD-005-shuttle-overtime-minimizer.md",
    "dsa-problems/Greedy/problems/GRD-006-robotics-component-bundling-loss-quality.md",
    "dsa-problems/Greedy/problems/GRD-007-campus-wifi-expansion.md",
    "dsa-problems/Greedy/problems/GRD-008-exam-proctor-allocation.md",
    "dsa-problems/Greedy/problems/GRD-009-shuttle-refuel-with-refund.md",
    "dsa-problems/Greedy/problems/GRD-010-library-merge-queues.md",
    "dsa-problems/Greedy/problems/GRD-011-campus-event-ticket-caps.md",
    "dsa-problems/Greedy/problems/GRD-012-workshop-task-cooldown-priority.md",
    "dsa-problems/Greedy/problems/GRD-013-auditorium-seat-refunds.md",
    "dsa-problems/Greedy/problems/GRD-014-festival-bandwidth-split.md",
    "dsa-problems/Greedy/problems/GRD-015-robotics-median-after-batches-stale.md",
    "dsa-problems/Greedy/problems/GRD-016-shuttle-schedule-delay-minimizer.md",
]

def extract_example_info(filepath):
    """Extract Input, Output, and Explanation from problem file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the Example section
    example_match = re.search(r'## Example\s*\n\n\*\*Input:\*\*\s*\n```(.*?)```\s*\n\*\*Output:\*\*\s*\n```(.*?)```\s*\n\*\*Explanation:\*\*(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL)
    
    if not example_match:
        return None, None, None
    
    input_text = example_match.group(1).strip()
    output_text = example_match.group(2).strip()
    explanation = example_match.group(3).strip()
    
    return input_text, output_text, explanation

def check_output_vs_explanation(output_text, explanation):
    """Check if output matches any numbers in explanation"""
    try:
        expected_output = int(output_text)
    except:
        return None, None
    
    # Find all numbers in explanation
    numbers_in_explanation = re.findall(r'\d+', explanation)
    
    # Look for "Total" or "total" lines
    total_lines = re.findall(r'(?i)total[:\s]*.*?(\d+)', explanation)
    
    # Look for math expressions like "3 + 5 + 2 = 10"
    math_expr = re.findall(r'=\s*(\d+)', explanation)
    
    issues = []
    
    if total_lines:
        for total_val in total_lines:
            if int(total_val) != expected_output:
                issues.append(f"Output is {expected_output} but explanation shows total {total_val}")
    
    if math_expr:
        for val in math_expr:
            if int(val) != expected_output:
                issues.append(f"Output is {expected_output} but explanation calculation shows {val}")
    
    return issues if issues else None, total_lines or math_expr

# Check all problems
print("Checking Greedy Problem Examples...")
print("=" * 80)

problems_with_issues = []

for filepath in problem_files:
    problem_id = os.path.basename(filepath).replace('.md', '')
    
    if not os.path.exists(filepath):
        print(f"⚠️  {problem_id}: File not found")
        continue
    
    input_text, output_text, explanation = extract_example_info(filepath)
    
    if not output_text:
        print(f"⚠️  {problem_id}: Could not parse example section")
        continue
    
    issues, calculated_values = check_output_vs_explanation(output_text, explanation)
    
    if issues:
        problems_with_issues.append(problem_id)
        print(f"\n❌ {problem_id}:")
        print(f"   Output: {output_text}")
        for issue in issues:
            print(f"   Issue: {issue}")
        print(f"   Explanation snippet: {explanation[:200]}...")
    else:
        print(f"✅ {problem_id}: OK")

print("\n" + "=" * 80)
print(f"\nSummary: {len(problems_with_issues)} problems with potential issues")
if problems_with_issues:
    print(f"Problems to review: {', '.join(problems_with_issues)}")
