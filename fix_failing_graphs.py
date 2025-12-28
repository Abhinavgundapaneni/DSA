"""Fix remaining 5 Graphs problems with runtime errors."""
import yaml
import random
from pathlib import Path

def generate_grp009_tests():
    """GRP-009: Weighted Dijkstra - needs (u, v, w) format."""
    test_file = Path("dsa-problems/Graphs/testcases/GRP-009-city-toll-dijkstra.yaml")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    for category in ['samples', 'public', 'hidden']:
        for test in data[category]:
            lines = test['input'].strip().split('\n')
            n = int(lines[0])
            m = int(lines[1])
            
            # Current edges are (u, v), need to add weights
            edges_weighted = []
            for i in range(2, 2 + m):
                parts = lines[i].split()
                u, v = int(parts[0]), int(parts[1])
                w = random.randint(1, 10)  # Add random weight
                edges_weighted.append(f"{u} {v} {w}")
            
            # Update input
            new_input = f"{n}\n{m}\n" + "\n".join(edges_weighted)
            test['input'] = new_input
    
    with open(test_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"GRP-009: Updated {len(data['samples']) + len(data['public']) + len(data['hidden'])} tests with weights")

def generate_grp018_tests():
    """GRP-018: Weighted reachability - needs (u, v, w) format."""
    test_file = Path("dsa-problems/Graphs/testcases/GRP-018-robotics-weighted-reachability.yaml")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    for category in ['samples', 'public', 'hidden']:
        for test in data[category]:
            lines = test['input'].strip().split('\n')
            n = int(lines[0])
            m = int(lines[1])
            
            # Current edges are (u, v), need to add weights
            edges_weighted = []
            for i in range(2, 2 + m):
                parts = lines[i].split()
                u, v = int(parts[0]), int(parts[1])
                w = random.randint(1, 10)  # Add random weight
                edges_weighted.append(f"{u} {v} {w}")
            
            # Update input
            new_input = f"{n}\n{m}\n" + "\n".join(edges_weighted)
            test['input'] = new_input
    
    with open(test_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"GRP-018: Updated {len(data['samples']) + len(data['public']) + len(data['hidden'])} tests with weights")

def check_grp004():
    """GRP-004: Check what the actual problem input should be."""
    test_file = Path("dsa-problems/Graphs/testcases/GRP-004-seminar-bipartite-check-locked.yaml")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Check first sample
    test_input = data['samples'][0]['input']
    lines = test_input.strip().split('\n')
    print("GRP-004 first sample input:")
    for i, line in enumerate(lines[:5]):
        print(f"  Line {i}: {line}")
    print(f"  Total lines: {len(lines)}")
    
def check_grp011():
    """GRP-011: Grid BFS problem - check input format."""
    test_file = Path("dsa-problems/Graphs/testcases/GRP-011-library-fire-with-exhaustion.yaml")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Check first sample
    test_input = data['samples'][0]['input']
    lines = test_input.strip().split('\n')
    print("\nGRP-011 first sample input:")
    for i, line in enumerate(lines[:7]):
        print(f"  Line {i}: {line}")
    print(f"  Total lines: {len(lines)}")

def check_grp017():
    """GRP-017: Grid maze problem - check input format."""
    test_file = Path("dsa-problems/Graphs/testcases/GRP-017-festival-maze-shortest-path.yaml")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Check first sample
    test_input = data['samples'][0]['input']
    lines = test_input.strip().split('\n')
    print("\nGRP-017 first sample input:")
    for i, line in enumerate(lines[:7]):
        print(f"  Line {i}: {line}")
    print(f"  Total lines: {len(lines)}")

if __name__ == "__main__":
    # First check input formats
    check_grp004()
    check_grp011()
    check_grp017()
    
    # Then fix GRP-009 and GRP-018
    generate_grp009_tests()
    generate_grp018_tests()
