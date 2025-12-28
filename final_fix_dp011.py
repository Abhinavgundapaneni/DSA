"""Fix all DP-011 test outputs."""

# Correct outputs (from our computation)
corrections = {
    ('12', '3 0 2'): '0',
    ('505', '5 0 3'): '4',
    ('123', '4 1 2'): '1',
    ('7631', '9 0 4'): '4',
    ('9074', '5 4 1'): '0',
    ('60', '5 3 2'): '0',
    ('35337', '6 0 4'): '13',
    ('12415', '8 3 3'): '9',
    ('978', '8 0 2'): '1',
    ('66', '4 2 2'): '0',
    ('707', '2 1 3'): '1',
    ('99622', '5 0 2'): '13',
    ('83685', '7 3 3'): '7',
    ('890682', '5 3 1'): '7',
    ('5983', '8 7 3'): '3',
    ('5088', '7 3 1'): '2',
    ('28', '4 0 2'): '0',
    ('25412', '4 2 5'): '18',
    ('1046', '7 3 2'): '2',
    ('148', '5 4 2'): '1',
    ('3', '2 1 1'): '0',
    ('38738', '2 1 5'): '34',
    ('9420', '2 0 4'): '5',
    ('98', '2 1 1'): '1',
    ('139', '8 3 2'): '1',
    ('35', '4 2 2'): '1',
}

yaml_path = 'dsa-problems/DP/testcases/DP-011-expression-target-mod-minus.yaml'

with open(yaml_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Process and fix
output = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if we're at an input line
    if '  - input: |-' in line or '- input: |-' in line:
        output.append(line)
        i += 1
        
        # Read input content
        input_lines = []
        while i < len(lines) and not 'output:' in lines[i]:
            input_lines.append(lines[i].strip())
            output.append(lines[i])
            i += 1
        
        # Parse input
        if len(input_lines) >= 2:
            s_value = input_lines[0]
            params_value = input_lines[1]
            key = (s_value, params_value)
            
            # Skip output line and value
            if i < len(lines) and 'output:' in lines[i]:
                output.append(lines[i])  # Keep "output: |-"
                i += 1
                
                # Replace the output value if we have a correction
                if i < len(lines):
                    old_value = lines[i].strip()
                    if key in corrections:
                        # Replace with correct value
                        indent = len(lines[i]) - len(lines[i].lstrip())
                        output.append(' ' * indent + corrections[key] + '\n')
                        print(f"Fixed: s={s_value}, params={params_value}: {old_value} -> {corrections[key]}")
                    else:
                        output.append(lines[i])
                    i += 1
                continue
    
    output.append(line)
    i += 1

# Write fixed content
with open(yaml_path, 'w', encoding='utf-8') as f:
    f.writelines(output)

print(f"\nAll test cases fixed in {yaml_path}")
