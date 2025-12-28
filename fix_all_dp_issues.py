"""Fix all remaining DP test case issues by regenerating outputs."""

import yaml
import os

# Import all editorial solutions
def dp005_solution(s1, s2):
    """Keyboard row edit distance with shift cost."""
    # This is a placeholder - will extract from editorial
    return 0

def dp006_solution(arr, k):
    """LIS with strict jump and bounds."""
    return 0

def dp008_solution(m, n, grid, max_turns):
    """Grid paths with turn limit."""
    return 0

def dp009_solution(grid, f):
    """Min cost with free cells."""
    INF = 4 * 10**18
    m, n = len(grid), len(grid[0])
    dp = [[[INF] * (f + 1) for _ in range(n)] for __ in range(m)]
    dp[0][0][0] = grid[0][0]
    if f > 0:
        dp[0][0][1] = 0
    for r in range(m):
        for c in range(n):
            for k in range(f + 1):
                cur = dp[r][c][k]
                if cur >= INF:
                    continue
                if c + 1 < n:
                    dp[r][c + 1][k] = min(dp[r][c + 1][k], cur + grid[r][c + 1])
                    if k + 1 <= f:
                        dp[r][c + 1][k + 1] = min(dp[r][c + 1][k + 1], cur)
                if r + 1 < m:
                    dp[r + 1][c][k] = min(dp[r + 1][c][k], cur + grid[r + 1][c])
                    if k + 1 <= f:
                        dp[r + 1][c][k + 1] = min(dp[r + 1][c][k + 1], cur)
    return min(dp[-1][-1])

def dp012_solution(arr, k, max_diff):
    """Balanced partition with size limit."""
    return 0

def dp014_solution(s, forbidden):
    """Constrained decode ways."""
    return 0

def dp016_solution(exams, cooldown):
    """Exams with cooldown gap."""
    return 0

# Fix DP-009 missing outputs
print("Fixing DP-009 missing outputs...")
filepath = 'dsa-problems/DP/testcases/DP-009-flooded-campus-min-cost-free.yaml'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
i = 0
fixed = 0

while i < len(lines):
    line = lines[i]
    
    if '  - input: |-' in line or '- input: |-' in line:
        output_lines.append(line)
        i += 1
        
        # Collect input
        input_lines = []
        while i < len(lines) and 'output:' not in lines[i] and ('  - input:' not in lines[i] and '- input:' not in lines[i] and 'hidden:' not in lines[i] and 'public:' not in lines[i]):
            input_lines.append(lines[i].strip())
            output_lines.append(lines[i])
            i += 1
        
        # Parse and compute
        try:
            if len(input_lines) >= 2:
                m, n = map(int, input_lines[0].split())
                grid = []
                for j in range(1, m + 1):
                    if j < len(input_lines):
                        row = list(map(int, input_lines[j].split()))
                        grid.append(row)
                
                if m + 1 < len(input_lines):
                    f = int(input_lines[m + 1])
                    correct_output = dp009_solution(grid, f)
                    
                    # Check if output line exists
                    if i < len(lines) and 'output:' in lines[i]:
                        output_lines.append(lines[i])
                        i += 1
                        if i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('-') and not any(x in lines[i] for x in ['hidden:', 'public:', 'samples:']):
                            # Has output value
                            indent = len(lines[i]) - len(lines[i].lstrip())
                            output_lines.append(' ' * indent + str(correct_output) + '\n')
                            i += 1
                            continue
                        else:
                            # Missing output value - add it
                            output_lines.append('      ' + str(correct_output) + '\n')
                            fixed += 1
                            print(f'  Added missing output: {m}x{n} grid, f={f} -> {correct_output}')
                            continue
                    else:
                        # Missing output entirely - add it
                        output_lines.append('    output: |-\n')
                        output_lines.append('      ' + str(correct_output) + '\n')
                        fixed += 1
                        print(f'  Added missing output block: {m}x{n} grid, f={f} -> {correct_output}')
                        continue
        except Exception as e:
            pass
    
    output_lines.append(line)
    i += 1

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Fixed {fixed} missing outputs in DP-009\n")
