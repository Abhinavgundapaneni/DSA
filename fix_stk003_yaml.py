import yaml

# Read the YAML file
with open('./dsa-problems/Stacks/testcases/STK-003-conveyor-weighted-deduplication.yaml', 'r') as f:
    data = yaml.safe_load(f)

# The data is already loaded, but the \n in the file are literal strings
# We need to rewrite the file with proper YAML multiline strings

def format_multiline(text):
    """Convert \\n to actual newlines and format as YAML literal block"""
    # Replace literal \n with actual newlines
    actual_newlines = text.replace('\\n', '\n')
    # Use literal block scalar with proper indentation
    lines = actual_newlines.split('\n')
    if len(lines) == 1:
        return f'"{lines[0]}"'
    else:
        result = '|\n'
        for line in lines:
            result += f'    {line}\n'
        return result.rstrip('\n')

# Fix all test cases
for category in ['samples', 'public', 'hidden']:
    if category in data:
        for tc in data[category]:
            # Check if input/output have \n in them
            if '\\n' in tc['input']:
                tc['input'] = tc['input'].replace('\\n', '\n')
            if '\\n' in tc['output']:
                tc['output'] = tc['output'].replace('\\n', '\n')

# Write back with proper formatting
with open('./dsa-problems/Stacks/testcases/STK-003-conveyor-weighted-deduplication.yaml', 'w') as f:
    # Write problem_id
    f.write(f"problem_id: {data['problem_id']}\n")
    
    for category in ['samples', 'public', 'hidden']:
        if category not in data:
            continue
        f.write(f"{category}:\n")
        for tc in data[category]:
            f.write("- input: |\n")
            for line in tc['input'].split('\n'):
                f.write(f"    {line}\n")
            f.write("  output: |\n")
            for line in tc['output'].split('\n'):
                f.write(f"    {line}\n")

print("Fixed STK-003 test cases with proper YAML multiline format")
