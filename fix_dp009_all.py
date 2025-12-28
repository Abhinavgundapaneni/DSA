"""Fix ALL DP-009 test case outputs by running editorial solution."""

import re

def min_cost_with_free_cells(cost, f):
    INF = 4 * 10**18
    m, n = len(cost), len(cost[0])
    dp = [[[INF] * (f + 1) for _ in range(n)] for __ in range(m)]
    dp[0][0][0] = cost[0][0]
    if f > 0:
        dp[0][0][1] = 0

    for r in range(m):
        for c in range(n):
            for k in range(f + 1):
                cur = dp[r][c][k]
                if cur >= INF:
                    continue
                if c + 1 < n:
                    dp[r][c + 1][k] = min(dp[r][c + 1][k], cur + cost[r][c + 1])
                    if k + 1 <= f:
                        dp[r][c + 1][k + 1] = min(dp[r][c + 1][k + 1], cur)
                if r + 1 < m:
                    dp[r + 1][c][k] = min(dp[r + 1][c][k], cur + cost[r + 1][c])
                    if k + 1 <= f:
                        dp[r + 1][c][k + 1] = min(dp[r + 1][c][k + 1], cur)

    return min(dp[-1][-1])

yaml_path = 'dsa-problems/DP/testcases/DP-009-flooded-campus-min-cost-free.yaml'

with open(yaml_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
i = 0
fixed_count = 0

while i < len(lines):
    line = lines[i]
    
    if '  - input: |-' in line or '- input: |-' in line:
        output.append(line)
        i += 1
        
        # Read input lines
        input_lines = []
        while i < len(lines) and not 'output:' in lines[i]:
            input_lines.append(lines[i].strip())
            output.append(lines[i])
            i += 1
        
        # Parse input
        try:
            m, n = map(int, input_lines[0].split())
            grid = []
            for j in range(1, m + 1):
                if j < len(input_lines):
                    row = list(map(int, input_lines[j].split()))
                    grid.append(row)
            
            if m + 1 < len(input_lines):
                f = int(input_lines[m + 1])
                
                # Compute correct output
                correct_output = min_cost_with_free_cells(grid, f)
                
                # Handle output line
                if i < len(lines) and 'output:' in lines[i]:
                    output.append(lines[i])
                    i += 1
                    
                    if i < len(lines):
                        old_value = lines[i].strip()
                        indent = len(lines[i]) - len(lines[i].lstrip())
                        output.append(' ' * indent + str(correct_output) + '\n')
                        if old_value != str(correct_output):
                            fixed_count += 1
                            print(f'Fixed: {m}x{n} grid, f={f}: {old_value} -> {correct_output}')
                        i += 1
                    continue
        except:
            pass
    
    output.append(line)
    i += 1

with open(yaml_path, 'w', encoding='utf-8') as f:
    f.writelines(output)

print(f'\nFixed {fixed_count} test cases in DP-009')
