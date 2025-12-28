"""
Check all Queue problems for common issues
"""
import os
import subprocess
import yaml

QUEUE_NUMS = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015", "016"]

def check_problem(num):
    """Check a single Queue problem"""
    problem_file = f"dsa-problems/Queues/problems/QUE-{num}-*.md"
    editorial_file = f"dsa-problems/Queues/editorials/QUE-{num}-*.md"
    
    # Find actual filename
    import glob
    problem_files = glob.glob(problem_file.replace("*", "*"))
    editorial_files = glob.glob(editorial_file.replace("*", "*"))
    
    if not problem_files or not editorial_files:
        return {"status": "missing_files", "problem": problem_files, "editorial": editorial_files}
    
    problem_path = problem_files[0]
    editorial_path = editorial_files[0]
    
    # Read problem to find example
    with open(problem_path, 'r', encoding='utf-8') as f:
        problem_content = f.read()
    
    # Extract example input/output
    import re
    example_match = re.search(r'\*\*Input:\*\*\s*```(.*?)```\s*\*\*Output:\*\*\s*```(.*?)```', problem_content, re.DOTALL)
    
    if not example_match:
        return {"status": "no_example", "file": problem_path}
    
    example_input = example_match.group(1).strip()
    example_output = example_match.group(2).strip()
    
    # Read YAML test case
    yaml_files = glob.glob(f"dsa-problems/Queues/testcases/QUE-{num}-*.yaml")
    if not yaml_files:
        return {"status": "no_yaml", "file": problem_path}
    
    with open(yaml_files[0], 'r', encoding='utf-8') as f:
        test_data = yaml.safe_load(f)
    
    if not test_data or 'samples' not in test_data or len(test_data['samples']) == 0:
        return {"status": "no_samples", "file": yaml_files[0]}
    
    yaml_sample_input = test_data['samples'][0]['input'].strip()
    yaml_sample_output = test_data['samples'][0]['output'].strip()
    
    # Compare
    input_match = (example_input == yaml_sample_input)
    output_match = (example_output == yaml_sample_output)
    
    return {
        "status": "ok" if (input_match and output_match) else "mismatch",
        "input_match": input_match,
        "output_match": output_match,
        "example_input": example_input[:100],
        "yaml_input": yaml_sample_input[:100],
        "example_output": example_output[:100],
        "yaml_output": yaml_sample_output[:100]
    }

print("Checking Queue Problems...")
print("=" * 80)

issues = []
for num in QUEUE_NUMS:
    result = check_problem(num)
    status_icon = "✅" if result.get("status") == "ok" else "❌"
    print(f"{status_icon} QUE-{num}: {result['status']}")
    
    if result['status'] not in ['ok', 'missing_files']:
        issues.append((num, result))
        if result['status'] == 'mismatch':
            if not result.get('input_match'):
                print(f"   Input mismatch!")
            if not result.get('output_match'):
                print(f"   Output mismatch!")

print("\n" + "=" * 80)
print(f"Found {len(issues)} problems with issues")
