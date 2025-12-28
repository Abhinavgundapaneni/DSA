"""
Fix broken Greedy editorials by replacing buggy main() with working implementations.
"""

import re
from pathlib import Path

def fix_grd003():
    """GRD-003: Festival Stall Placement - Fix iterator issue"""
    file_path = Path("dsa-problems/Greedy/editorials/GRD-003-festival-stall-placement.md")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the broken main() function
    old_main = '''def main():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
        
    iterator = iter(data)
    n = int(next(iterator))
    d = int(next(iterator))
    
    stalls = []
    for _ in range(n):
        start = int(next(iterator))
        end = int(next(iterator))
        stalls.append([start, end])

    result = max_stalls(stalls, d)
    print(result)'''
    
    new_main = '''def main():
    data = sys.stdin.read().split()
    if not data:
        return
        
    idx = 0
    n = int(data[idx])
    idx += 1
    d = int(data[idx])
    idx += 1
    
    stalls = []
    for _ in range(n):
        start = int(data[idx])
        idx += 1
        end = int(data[idx])
        idx += 1
        stalls.append([start, end])

    result = max_stalls(stalls, d)
    print(result)'''
    
    content = content.replace(old_main, new_main)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Fixed GRD-003")


def fix_grd005():
    """GRD-005: Shuttle Overtime Minimizer - Fix iterator issue"""
    file_path = Path("dsa-problems/Greedy/editorials/GRD-005-shuttle-overtime-minimizer.md")
    
    # Read and check if file exists
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"⚠️  GRD-005 file not found")
        return
    
    # Find and fix the main() function with iterator pattern
    pattern = r'(def main\(\):.*?)(input = sys\.stdin\.read\s+data = input\(\)\.split\(\).*?iterator = iter\(data\).*?)(if __name__)'
    
    def replacement(match):
        prefix = match.group(1)
        return prefix + '''data = sys.stdin.read().split()
    if not data:
        return
        
    idx = 0
    n = int(data[idx])
    idx += 1
    
    arrivals = []
    departures = []
    for _ in range(n):
        arrivals.append(int(data[idx]))
        idx += 1
        departures.append(int(data[idx]))
        idx += 1

    result = min_platforms(arrivals, departures)
    print(result)

''' + match.group(3)
    
    if 'iterator = iter' in content:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed GRD-005")
    else:
        print(f"⚠️  GRD-005 doesn't have expected pattern")


def fix_all_broken_editorials():
    """Fix all broken Greedy editorials."""
    print("="*60)
    print("FIXING BROKEN GREEDY EDITORIALS")
    print("="*60)
    
    # List of broken editorials (from testing)
    broken = [
        "GRD-003", "GRD-005", "GRD-006", "GRD-007", "GRD-008",
        "GRD-010", "GRD-011", "GRD-012", "GRD-013", "GRD-014", "GRD-015"
    ]
    
    # Try to fix known patterns
    fix_grd003()
    fix_grd005()
    
    # For the rest, let's use a generic fix
    for prob_id in broken:
        if prob_id in ["GRD-003", "GRD-005"]:
            continue  # Already fixed
        
        # Find the editorial file
        files = list(Path("dsa-problems/Greedy/editorials").glob(f"{prob_id}-*.md"))
        if not files:
            print(f"⚠️  {prob_id} file not found")
            continue
        
        file_path = files[0]
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it has the iterator bug
        if 'input = sys.stdin.read' in content and 'iterator = iter' in content:
            # Generic fix: replace iterator pattern with index-based parsing
            content = content.replace('input = sys.stdin.read', 'data = sys.stdin.read()')
            content = content.replace('data = input().split()', 'data = data.split()')
            content = content.replace('iterator = iter(data)', 'idx = 0')
            content = re.sub(r'int\(next\(iterator\)\)', 'int(data[idx]); idx += 1', content)
            content = re.sub(r'next\(iterator\)', 'data[idx]; idx += 1', content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed {prob_id} (generic fix)")
        else:
            print(f"⚠️  {prob_id} has unknown issue")
    
    print("="*60)
    print("DONE")
    print("="*60)


if __name__ == "__main__":
    fix_all_broken_editorials()
