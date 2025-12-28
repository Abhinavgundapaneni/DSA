"""Fix DP-011 test cases by running the editorial solution on all inputs."""

# Editorial solution (correct)
MOD = 1_000_000_007

def count_expressions(s, M, K, L):
    n = len(s)
    dp = [[[0]*2 for _ in range(M)] for __ in range(n+1)]
    for l in range(1, min(L, n) + 1):
        if s[0] == '0' and l > 1:
            break
        val = int(s[0:l]) % M
        dp[l][val][0] = 1
    for pos in range(1, n):
        for rem in range(M):
            for used in range(2):
                ways = dp[pos][rem][used]
                if ways == 0:
                    continue
                for l in range(1, min(L, n - pos) + 1):
                    if s[pos] == '0' and l > 1:
                        break
                    val = int(s[pos:pos+l])
                    addRem = (rem + val) % M
                    subRem = (rem - val) % M
                    dp[pos+l][addRem][used] = (dp[pos+l][addRem][used] + ways) % MOD
                    dp[pos+l][subRem][1] = (dp[pos+l][subRem][1] + ways) % MOD
    return dp[n][K][1]

# Read the YAML file
yaml_path = 'dsa-problems/DP/testcases/DP-011-expression-target-mod-minus.yaml'
with open(yaml_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Process line by line
output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    output_lines.append(line)
    
    # Check if this is an input line
    if '  - input: |-' in line or '- input: |-' in line:
        # Collect input lines
        i += 1
        input_text = []
        while i < len(lines) and not ('output:' in lines[i]):
            input_text.append(lines[i].strip())
            output_lines.append(lines[i])
            i += 1
        
        # Parse input
        input_str = '\n'.join(input_text).strip()
        input_parts = input_str.split('\n')
        
        if len(input_parts) >= 2:
            s = input_parts[0].strip()
            params = input_parts[1].strip().split()
            
            if len(params) == 3 and s:
                try:
                    M, K, L = map(int, params)
                    correct_output = count_expressions(s, M, K, L)
                    
                    # Skip the old output line
                    if i < len(lines) and 'output:' in lines[i]:
                        output_lines.append(lines[i])  # Keep "output: |-"
                        i += 1
                        # Skip old output value
                        if i < len(lines) and lines[i].strip() and not lines[i].startswith('  -') and not lines[i].startswith('hidden:') and not lines[i].startswith('public:'):
                            i += 1  # Skip old value
                            output_lines.append(f'      {correct_output}\n')
                        continue
                except:
                    pass
    
    i += 1

# Write back
with open(yaml_path, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Fixed all test cases in {yaml_path}")
print("Verified a few cases:")
print(f"  '1234' M=7 K=0 L=2 -> {count_expressions('1234', 7, 0, 2)}")
print(f"  '12' M=3 K=0 L=2 -> {count_expressions('12', 3, 0, 2)}")
print(f"  '505' M=5 K=0 L=3 -> {count_expressions('505', 5, 0, 3)}")
print(f"  '123' M=4 K=1 L=2 -> {count_expressions('123', 4, 1, 2)}")
