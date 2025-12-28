#!/usr/bin/env python3
"""
Fix TreesDP test cases by regenerating outputs using correct brute-force solutions.
"""
import sys
import yaml
from collections import defaultdict, deque
from pathlib import Path

BASE = Path(r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\TreesDP")

sys.setrecursionlimit(300000)

# ============= CORRECT SOLVERS =============

def solve_tdp004(inp: str) -> str:
    """TDP-004: Rerooting for Weighted Distance Variance"""
    lines = inp.strip().split('\n')
    n = int(lines[0])
    w = [0] + list(map(int, lines[1].split()))
    
    adj = defaultdict(list)
    for i in range(2, n + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    def compute_cost(root):
        dist = [-1] * (n + 1)
        dist[root] = 0
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for neighbor in adj[node]:
                if dist[neighbor] == -1:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        return sum(w[j] * dist[j] * dist[j] for j in range(1, n + 1))
    
    min_cost = float('inf')
    best_node = 1
    for node in range(1, n + 1):
        cost = compute_cost(node)
        if cost < min_cost:
            min_cost = cost
            best_node = node
    
    return str(best_node)


def solve_tdp005(inp: str) -> str:
    """TDP-005: Max Path Sum with Length Limit k"""
    lines = inp.strip().split('\n')
    parts = lines[0].split()
    n = int(parts[0])
    k = int(parts[1])
    w = [0] + list(map(int, lines[1].split()))
    
    if n == 1:
        return str(w[1])
    
    adj = defaultdict(list)
    for i in range(2, n + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    max_sum = max(w[1:n+1])
    
    # DFS from each node exploring all paths up to k edges
    def dfs(node, parent, depth, path_sum):
        nonlocal max_sum
        max_sum = max(max_sum, path_sum)
        if depth < k:
            for child in adj[node]:
                if child != parent:
                    dfs(child, node, depth + 1, path_sum + w[child])
    
    for start in range(1, n + 1):
        dfs(start, -1, 0, w[start])
    
    return str(max_sum)


def solve_tdp006(inp: str) -> str:
    """TDP-006: Minimum Vertex Cover"""
    lines = inp.strip().split('\n')
    n = int(lines[0])
    
    if n == 1:
        return "0"
    
    adj = defaultdict(list)
    for i in range(1, n):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    dp = [[0, 0] for _ in range(n + 1)]
    
    def dfs(node, parent):
        dp[node][0] = 0  # Not in cover
        dp[node][1] = 1  # In cover
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
                dp[node][0] += dp[child][1]
                dp[node][1] += min(dp[child][0], dp[child][1])
    
    dfs(1, -1)
    return str(min(dp[1][0], dp[1][1]))


def solve_tdp007(inp: str) -> str:
    """TDP-007: Maximum Weight Independent Set"""
    lines = inp.strip().split('\n')
    n = int(lines[0])
    w = [0] + list(map(int, lines[1].split()))
    
    if n == 1:
        return str(w[1])
    
    adj = defaultdict(list)
    for i in range(2, n + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    dp = [[0, 0] for _ in range(n + 1)]
    
    def dfs(node, parent):
        dp[node][0] = 0  # Not selected
        dp[node][1] = w[node]  # Selected
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
                dp[node][0] += max(dp[child][0], dp[child][1])
                dp[node][1] += dp[child][0]
    
    dfs(1, -1)
    return str(max(dp[1][0], dp[1][1]))


def solve_tdp008(inp: str) -> str:
    """TDP-008: Path Sum Queries"""
    lines = inp.strip().split('\n')
    parts = lines[0].split()
    n = int(parts[0])
    q = int(parts[1])
    w = [0] + list(map(int, lines[1].split()))
    
    adj = defaultdict(list)
    for i in range(2, n + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Build parent array via BFS from node 1
    parent = [-1] * (n + 1)
    depth = [0] * (n + 1)
    queue = deque([1])
    visited = {1}
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                depth[neighbor] = depth[node] + 1
                queue.append(neighbor)
    
    def path_sum(u, v):
        path = []
        # Bring u and v to same depth
        while depth[u] > depth[v]:
            path.append(u)
            u = parent[u]
        while depth[v] > depth[u]:
            path.append(v)
            v = parent[v]
        # Move both up until they meet
        while u != v:
            path.append(u)
            path.append(v)
            u = parent[u]
            v = parent[v]
        path.append(u)  # LCA
        return sum(w[node] for node in set(path))
    
    results = []
    for i in range(n + 1, n + 1 + q):
        u, v = map(int, lines[i].split())
        results.append(str(path_sum(u, v)))
    
    return '\n'.join(results)


def solve_tdp009(inp: str) -> str:
    """TDP-009: Sum of Distances from Each Node"""
    lines = inp.strip().split('\n')
    n = int(lines[0])
    
    adj = defaultdict(list)
    for i in range(1, n):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    def compute_dist_sum(root):
        dist = {root: 0}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for neighbor in adj[node]:
                if neighbor not in dist:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        return sum(dist.values())
    
    results = [str(compute_dist_sum(i)) for i in range(1, n + 1)]
    return '\n'.join(results)


def solve_tdp010(inp: str) -> str:
    """TDP-010: Count Subtrees with Sum K"""
    lines = inp.strip().split('\n')
    parts = lines[0].split()
    n = int(parts[0])
    k = int(parts[1])
    w = [0] + list(map(int, lines[1].split()))
    
    adj = defaultdict(list)
    for i in range(2, n + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    count = 0
    subtree_sum = [0] * (n + 1)
    
    def dfs(node, parent):
        nonlocal count
        subtree_sum[node] = w[node]
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
                subtree_sum[node] += subtree_sum[child]
        if subtree_sum[node] == k:
            count += 1
    
    dfs(1, -1)
    return str(count)


def solve_tdp011(inp: str) -> str:
    """TDP-011: Eccentricity of Each Node"""
    lines = inp.strip().split('\n')
    n = int(lines[0])
    
    adj = defaultdict(list)
    for i in range(1, n):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    def compute_eccentricity(root):
        dist = {root: 0}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for neighbor in adj[node]:
                if neighbor not in dist:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        return max(dist.values()) if dist else 0
    
    results = [str(compute_eccentricity(i)) for i in range(1, n + 1)]
    return '\n'.join(results)


def solve_tdp012(inp: str) -> str:
    """TDP-012: K-th Ancestor Queries"""
    lines = inp.strip().split('\n')
    parts = lines[0].split()
    n = int(parts[0])
    q = int(parts[1])
    
    adj = defaultdict(list)
    for i in range(1, n):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    parent = {1: -1}
    depth = {1: 0}
    queue = deque([1])
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                depth[neighbor] = depth[node] + 1
                queue.append(neighbor)
    
    def get_kth_ancestor(node, k):
        if k > depth[node]:
            return -1
        curr = node
        for _ in range(k):
            curr = parent[curr]
            if curr == -1:
                return -1
        return curr
    
    results = []
    for i in range(n, n + q):
        node, k = map(int, lines[i].split())
        results.append(str(get_kth_ancestor(node, k)))
    
    return '\n'.join(results)


def solve_tdp013(inp: str) -> str:
    """TDP-013: Maximum Depth of Tree"""
    lines = inp.strip().split('\n')
    n = int(lines[0])
    
    if n == 1:
        return "0"
    
    adj = defaultdict(list)
    for i in range(1, n):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Find diameter using two BFS
    def bfs_farthest(start):
        dist = {start: 0}
        queue = deque([start])
        farthest = start
        max_dist = 0
        while queue:
            node = queue.popleft()
            if dist[node] > max_dist:
                max_dist = dist[node]
                farthest = node
            for neighbor in adj[node]:
                if neighbor not in dist:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        return farthest, max_dist
    
    far1, _ = bfs_farthest(1)
    _, diameter = bfs_farthest(far1)
    
    return str(diameter)


def solve_tdp015(inp: str) -> str:
    """TDP-015: Centroid Decomposition Level"""
    lines = inp.strip().split('\n')
    n = int(lines[0])
    
    adj = defaultdict(list)
    for i in range(1, n):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    removed = [False] * (n + 1)
    level = [0] * (n + 1)
    
    def get_subtree_size(node, parent):
        size = 1
        for neighbor in adj[node]:
            if neighbor != parent and not removed[neighbor]:
                size += get_subtree_size(neighbor, node)
        return size
    
    def get_centroid(node, parent, tree_size):
        subtree_size = 1
        is_centroid = True
        for neighbor in adj[node]:
            if neighbor != parent and not removed[neighbor]:
                child_size = get_subtree_size(neighbor, node)
                subtree_size += child_size
                if child_size > tree_size // 2:
                    is_centroid = False
        if tree_size - subtree_size > tree_size // 2:
            is_centroid = False
        
        if is_centroid:
            return node
        
        for neighbor in adj[node]:
            if neighbor != parent and not removed[neighbor]:
                result = get_centroid(neighbor, node, tree_size)
                if result != -1:
                    return result
        return -1
    
    def decompose(node, current_level):
        tree_size = get_subtree_size(node, -1)
        centroid = get_centroid(node, -1, tree_size)
        
        if centroid == -1:
            centroid = node
        
        level[centroid] = current_level
        removed[centroid] = True
        
        for neighbor in adj[centroid]:
            if not removed[neighbor]:
                decompose(neighbor, current_level + 1)
    
    decompose(1, 1)
    return ' '.join(str(level[i]) for i in range(1, n + 1))


def solve_tdp016(inp: str) -> str:
    """TDP-016: Weighted Distance Sum with Edge Weights"""
    lines = inp.strip().split('\n')
    n = int(lines[0])
    node_weights = [0] + list(map(int, lines[1].split()))
    
    adj = defaultdict(list)
    for i in range(2, n + 1):
        parts = lines[i].split()
        u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    def compute_weighted_sum(root):
        dist = {root: 0}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for neighbor, weight in adj[node]:
                if neighbor not in dist:
                    dist[neighbor] = dist[node] + weight
                    queue.append(neighbor)
        # Sum of (node_weight[j] * distance[j]) for all j
        return sum(node_weights[j] * dist[j] for j in range(1, n + 1))
    
    results = [str(compute_weighted_sum(i)) for i in range(1, n + 1)]
    return '\n'.join(results)


SOLVERS = {
    'TDP-004': solve_tdp004,
    'TDP-005': solve_tdp005,
    'TDP-006': solve_tdp006,
    'TDP-007': solve_tdp007,
    'TDP-008': solve_tdp008,
    'TDP-009': solve_tdp009,
    'TDP-010': solve_tdp010,
    'TDP-011': solve_tdp011,
    'TDP-012': solve_tdp012,
    'TDP-013': solve_tdp013,
    'TDP-015': solve_tdp015,
    'TDP-016': solve_tdp016,
}


def fix_problem(prob_id: str, dry_run: bool = True):
    """Fix test cases for a single problem."""
    if prob_id not in SOLVERS:
        print(f"No solver for {prob_id}")
        return 0
    
    solver = SOLVERS[prob_id]
    
    # Find testcase file
    tc_files = list(BASE.glob(f"testcases/{prob_id}*.yaml"))
    if not tc_files:
        print(f"No testcase file for {prob_id}")
        return 0
    
    tc_file = tc_files[0]
    with open(tc_file, 'r', encoding='utf-8') as f:
        content = f.read()
        data = yaml.safe_load(content)
    
    fixed_count = 0
    
    for category in ['samples', 'public', 'hidden']:
        testcases = data.get(category, [])
        for i, tc in enumerate(testcases):
            inp = tc['input']
            expected = tc['output'].strip()
            
            try:
                actual = solver(inp)
                if actual != expected:
                    fixed_count += 1
                    if not dry_run:
                        tc['output'] = actual
                    print(f"  {category}[{i}]: FIXED")
                    if dry_run:
                        print(f"    Was: {expected[:60]}...")
                        print(f"    Now: {actual[:60]}...")
            except Exception as e:
                print(f"  {category}[{i}]: ERROR - {e}")
    
    if not dry_run and fixed_count > 0:
        with open(tc_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=1000)
        print(f"  Saved {fixed_count} fixes to {tc_file.name}")
    
    return fixed_count


def main():
    dry_run = '--apply' not in sys.argv
    probs = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    
    if not probs:
        probs = sorted(SOLVERS.keys())
    
    total_fixed = 0
    for prob_id in probs:
        print(f"\n{prob_id}:")
        fixed = fix_problem(prob_id, dry_run)
        total_fixed += fixed
    
    print(f"\n{'Would fix' if dry_run else 'Fixed'}: {total_fixed} test cases")
    if dry_run:
        print("Run with --apply to actually fix the files")


if __name__ == "__main__":
    main()
