#!/usr/bin/env python3
"""
Fix TreesDP test cases with correct solvers for each problem.
"""
import sys
import yaml
from collections import defaultdict, deque
from pathlib import Path

BASE = Path(r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\TreesDP")
sys.setrecursionlimit(300000)

# ============= CORRECT SOLVERS =============

def solve_tdp004(inp: str) -> str:
    """Rerooting for Weighted Distance Variance - minimize sum(w[j]*dist^2)"""
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
    """Max Path Sum with Length Limit L (at most L edges)"""
    lines = inp.strip().split('\n')
    parts = lines[0].split()
    n = int(parts[0])
    L = int(parts[1])
    w = [0] + list(map(int, lines[1].split()))
    
    if n == 1:
        return str(w[1])
    
    adj = defaultdict(list)
    for i in range(2, n + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    max_sum = max(w[1:n+1])
    
    def dfs(node, parent, depth, path_sum):
        nonlocal max_sum
        max_sum = max(max_sum, path_sum)
        if depth < L:
            for child in adj[node]:
                if child != parent:
                    dfs(child, node, depth + 1, path_sum + w[child])
    
    for start in range(1, n + 1):
        dfs(start, -1, 0, w[start])
    
    return str(max_sum)


def solve_tdp006(inp: str) -> str:
    """Minimum Vertex Cover"""
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
        dp[node][0] = 0
        dp[node][1] = 1
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
                dp[node][0] += dp[child][1]
                dp[node][1] += min(dp[child][0], dp[child][1])
    
    dfs(1, -1)
    return str(min(dp[1][0], dp[1][1]))


def solve_tdp008(inp: str) -> str:
    """Tree Coloring with Color Costs - minimize total coloring cost"""
    lines = inp.strip().split('\n')
    first_line = lines[0].split()
    N = int(first_line[0])
    K = int(first_line[1])
    
    # Cost matrix: cost[node][color]
    cost = [[0] * (K + 1) for _ in range(N + 1)]
    for i in range(1, N + 1):
        row = list(map(int, lines[i].split()))
        for j in range(K):
            cost[i][j + 1] = row[j]
    
    # Build adjacency list
    adj = defaultdict(list)
    for i in range(N + 1, 2 * N):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    # DP: dp[node][color] = min cost to color subtree of node when node has color
    dp = [[float('inf')] * (K + 1) for _ in range(N + 1)]
    
    def dfs(node, parent):
        for c in range(1, K + 1):
            dp[node][c] = cost[node][c]
        
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
                for c in range(1, K + 1):
                    # Find minimum cost for child with different color
                    min_child = float('inf')
                    for cc in range(1, K + 1):
                        if cc != c:
                            min_child = min(min_child, dp[child][cc])
                    dp[node][c] += min_child
    
    dfs(1, -1)
    return str(min(dp[1][1:K+1]))


def solve_tdp009(inp: str) -> str:
    """Path Queries with weighted edges - distance queries"""
    lines = inp.strip().split('\n')
    N = int(lines[0])
    
    adj = defaultdict(list)
    for i in range(1, N):
        parts = lines[i].split()
        u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    Q = int(lines[N])
    
    # Build parent and dist from root using BFS
    parent = [-1] * (N + 1)
    dist_from_root = [0] * (N + 1)
    depth = [0] * (N + 1)
    queue = deque([1])
    visited = {1}
    while queue:
        node = queue.popleft()
        for neighbor, weight in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                depth[neighbor] = depth[node] + 1
                dist_from_root[neighbor] = dist_from_root[node] + weight
                queue.append(neighbor)
    
    def get_dist(u, v):
        # Find LCA and compute distance
        path_u = []
        path_v = []
        
        # Get ancestors of u
        curr = u
        while curr != -1:
            path_u.append(curr)
            curr = parent[curr]
        
        # Get ancestors of v
        curr = v
        while curr != -1:
            path_v.append(curr)
            curr = parent[curr]
        
        set_u = set(path_u)
        lca = -1
        for node in path_v:
            if node in set_u:
                lca = node
                break
        
        return dist_from_root[u] + dist_from_root[v] - 2 * dist_from_root[lca]
    
    results = []
    for i in range(N + 1, N + 1 + Q):
        u, v = map(int, lines[i].split())
        results.append(str(get_dist(u, v)))
    
    return '\n'.join(results)


def solve_tdp010(inp: str) -> str:
    """Count pairs at distance K avoiding color F"""
    lines = inp.strip().split('\n')
    parts = lines[0].split()
    N = int(parts[0])
    K = int(parts[1])
    F = int(parts[2])
    
    colors = [0] + list(map(int, lines[1].split()))
    
    adj = defaultdict(list)
    for i in range(2, N + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Count pairs (u, v) with distance exactly K, no node on path has color F
    count = 0
    
    def bfs_count(start):
        nonlocal count
        if colors[start] == F:
            return
        
        visited = {start: 0}
        queue = deque([(start, 0)])
        while queue:
            node, dist = queue.popleft()
            if dist == K:
                count += 1
                continue
            if dist > K:
                continue
            for neighbor in adj[node]:
                if neighbor not in visited and colors[neighbor] != F:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, dist + 1))
    
    for start in range(1, N + 1):
        bfs_count(start)
    
    # Each pair is counted twice (once from each end)
    return str(count // 2)


def solve_tdp011(inp: str) -> str:
    """Path Sum Queries - sum of values on path u to v"""
    lines = inp.strip().split('\n')
    N = int(lines[0])
    values = [0] + list(map(int, lines[1].split()))
    
    adj = defaultdict(list)
    for i in range(2, N + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    Q = int(lines[N + 1])
    
    # Build parent array
    parent = [-1] * (N + 1)
    depth = [0] * (N + 1)
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
        # Collect path nodes
        path = set()
        
        # Bring to same depth
        while depth[u] > depth[v]:
            path.add(u)
            u = parent[u]
        while depth[v] > depth[u]:
            path.add(v)
            v = parent[v]
        
        # Move both up until they meet
        while u != v:
            path.add(u)
            path.add(v)
            u = parent[u]
            v = parent[v]
        path.add(u)  # LCA
        
        return sum(values[node] for node in path)
    
    results = []
    for i in range(N + 2, N + 2 + Q):
        u, v = map(int, lines[i].split())
        results.append(str(path_sum(u, v)))
    
    return '\n'.join(results)


def solve_tdp012(inp: str) -> str:
    """K-th Ancestor with Color Filter"""
    lines = inp.strip().split('\n')
    N = int(lines[0])
    colors = [0] + list(map(int, lines[1].split()))
    
    adj = defaultdict(list)
    for i in range(2, N + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    Q = int(lines[N + 1])
    
    # Build parent array
    parent = [-1] * (N + 1)
    queue = deque([1])
    visited = {1}
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
    
    def kth_ancestor_with_color(v, c, k):
        count = 0
        curr = v
        while curr != -1:
            if colors[curr] == c:
                count += 1
                if count == k:
                    return curr
            curr = parent[curr]
        return -1
    
    results = []
    for i in range(N + 2, N + 2 + Q):
        parts = lines[i].split()
        v, c, k = int(parts[0]), int(parts[1]), int(parts[2])
        results.append(str(kth_ancestor_with_color(v, c, k)))
    
    return '\n'.join(results)


def solve_tdp013(inp: str) -> str:
    """Maximum Matching on Tree"""
    lines = inp.strip().split('\n')
    N = int(lines[0])
    
    if N == 1:
        return "0"
    
    adj = defaultdict(list)
    for i in range(1, N):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    # dp[node][0] = max matching in subtree, node not matched to parent
    # dp[node][1] = max matching in subtree, node matched to parent (edge to parent in matching)
    dp = [[0, 0] for _ in range(N + 1)]
    
    def dfs(node, parent):
        dp[node][0] = 0
        dp[node][1] = 0
        
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
                dp[node][0] += dp[child][0]
        
        # Option 1: node not matched to any child
        # We already have sum of dp[child][0]
        
        # Option 2: node matched to one of its children
        max_gain = 0
        for child in adj[node]:
            if child != parent:
                # If we match node with child
                gain = 1 + dp[child][1] - dp[child][0]
                max_gain = max(max_gain, gain)
        
        dp[node][0] += max_gain
        
        # dp[node][1] = if this node is matched to parent
        # Children can be matched among themselves
        dp[node][1] = sum(dp[child][0] for child in adj[node] if child != parent)
    
    dfs(1, -1)
    return str(dp[1][0])


def solve_tdp015(inp: str) -> str:
    """LIS length for each node's root-to-node path"""
    lines = inp.strip().split('\n')
    N = int(lines[0])
    values = [0] + list(map(int, lines[1].split()))
    
    adj = defaultdict(list)
    for i in range(2, N + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Result array
    lis = [0] * (N + 1)
    
    import bisect
    
    def dfs(node, parent, current_lis):
        # current_lis is the LIS ending values for the path from root to parent
        val = values[node]
        pos = bisect.bisect_left(current_lis, val)
        
        if pos == len(current_lis):
            new_lis = current_lis + [val]
        else:
            new_lis = current_lis[:pos] + [val] + current_lis[pos+1:]
        
        lis[node] = len(new_lis)
        
        for child in adj[node]:
            if child != parent:
                dfs(child, node, new_lis)
    
    dfs(1, -1, [])
    
    return ' '.join(str(lis[i]) for i in range(1, N + 1))


def solve_tdp016(inp: str) -> str:
    """Tree Flatten with Subtree Updates"""
    lines = inp.strip().split('\n')
    N = int(lines[0])
    values = [0] + list(map(int, lines[1].split()))
    
    adj = defaultdict(list)
    for i in range(2, N + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    Q = int(lines[N + 1])
    
    # Build subtree info via DFS
    subtree = [set() for _ in range(N + 1)]
    
    def build_subtree(node, parent):
        subtree[node].add(node)
        for child in adj[node]:
            if child != parent:
                build_subtree(child, node)
                subtree[node].update(subtree[child])
    
    build_subtree(1, -1)
    
    results = []
    for i in range(N + 2, N + 2 + Q):
        parts = lines[i].split()
        op_type = int(parts[0])
        
        if op_type == 1:
            u = int(parts[1])
            val = int(parts[2])
            for node in subtree[u]:
                values[node] += val
        else:
            u = int(parts[1])
            results.append(str(values[u]))
    
    return '\n'.join(results)


SOLVERS = {
    'TDP-004': solve_tdp004,
    'TDP-005': solve_tdp005,
    'TDP-006': solve_tdp006,
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
        data = yaml.safe_load(f)
    
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
                        exp_preview = expected[:60].replace('\n', '\\n')
                        act_preview = actual[:60].replace('\n', '\\n')
                        print(f"    Was: {exp_preview}...")
                        print(f"    Now: {act_preview}...")
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
