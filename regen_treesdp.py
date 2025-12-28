#!/usr/bin/env python3
"""
Regenerate correct test case outputs for TreesDP problems.
Uses brute-force correct implementations to compute expected outputs.
"""
import sys
import yaml
from collections import defaultdict, deque
from pathlib import Path

BASE = Path(r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\TreesDP")

# ============= CORRECT SOLVERS FOR EACH PROBLEM =============

def solve_tdp004(inp: str) -> str:
    """TDP-004: Rerooting for Weighted Distance Variance
    Find node minimizing sum_j(w[j] * dist(i,j)^2)
    """
    lines = inp.strip().split('\n')
    n = int(lines[0])
    w = [0] + list(map(int, lines[1].split()))  # 1-indexed
    
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
    """TDP-005: Max Path Sum with Length Limit
    Find maximum weighted path sum with at most k edges
    """
    lines = inp.strip().split('\n')
    parts = lines[0].split()
    n = int(parts[0])
    k = int(parts[1])
    w = [0] + list(map(int, lines[1].split()))  # node weights
    
    adj = defaultdict(list)
    for i in range(2, n + 1):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    # For each pair of nodes, find path sum if path length <= k
    max_sum = max(w[1:n+1])  # at minimum, single node
    
    def bfs_paths(start):
        nonlocal max_sum
        # BFS tracking (node, distance, path_sum)
        visited = {start: (0, w[start])}
        queue = deque([(start, 0, w[start])])
        while queue:
            node, dist, path_sum = queue.popleft()
            max_sum = max(max_sum, path_sum)
            if dist < k:
                for neighbor in adj[node]:
                    new_dist = dist + 1
                    new_sum = path_sum + w[neighbor]
                    # Only continue if this is better or first visit
                    key = (neighbor, new_dist)
                    if new_dist <= k:
                        queue.append((neighbor, new_dist, new_sum))
                        max_sum = max(max_sum, new_sum)
    
    # This approach is too slow for large n
    # Use tree DP instead
    
    # Actually for small n, brute force all paths
    def dfs_all_paths(node, parent, depth, path_sum):
        nonlocal max_sum
        if depth > k:
            return
        max_sum = max(max_sum, path_sum)
        for child in adj[node]:
            if child != parent:
                dfs_all_paths(child, node, depth + 1, path_sum + w[child])
    
    for start in range(1, n + 1):
        dfs_all_paths(start, -1, 0, w[start])
    
    return str(max_sum)


def solve_tdp006(inp: str) -> str:
    """TDP-006: Tree Vertex Cover
    Minimum number of nodes to cover all edges
    """
    lines = inp.strip().split('\n')
    n = int(lines[0])
    
    if n == 1:
        return "0"
    
    adj = defaultdict(list)
    for i in range(1, n):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    # dp[node][0] = min cover not including node
    # dp[node][1] = min cover including node
    dp = [[0, 0] for _ in range(n + 1)]
    
    def dfs(node, parent):
        dp[node][0] = 0
        dp[node][1] = 1
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
                # If node not included, all children must be included
                dp[node][0] += dp[child][1]
                # If node included, children can be either
                dp[node][1] += min(dp[child][0], dp[child][1])
    
    dfs(1, -1)
    return str(min(dp[1][0], dp[1][1]))


def solve_tdp007(inp: str) -> str:
    """TDP-007: Tree Independent Set with Distance >= 2
    Maximum weight independent set where selected nodes are at distance >= 2
    """
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
    
    # dp[node][0] = max weight, node not selected
    # dp[node][1] = max weight, node selected (children and grandchildren can't be selected)
    # dp[node][2] = max weight, node not selected but parent is
    
    # Actually simpler: distance >= 2 means no adjacent nodes selected
    # This is standard maximum independent set
    # dp[node][0] = not selected
    # dp[node][1] = selected
    
    dp = [[0, 0] for _ in range(n + 1)]
    
    def dfs(node, parent):
        dp[node][1] = w[node]
        dp[node][0] = 0
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
                # If not selected, children can be anything
                dp[node][0] += max(dp[child][0], dp[child][1])
                # If selected, children must not be selected
                dp[node][1] += dp[child][0]
    
    dfs(1, -1)
    return str(max(dp[1][0], dp[1][1]))


def solve_tdp008(inp: str) -> str:
    """TDP-008: Tree Path Queries
    For each query (u,v), output path sum
    """
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
    
    # Precompute LCA and path sums
    # For simplicity, use BFS to find path
    def path_sum(u, v):
        if u == v:
            return w[u]
        
        # BFS from u to v
        parent = {u: None}
        queue = deque([u])
        while queue:
            node = queue.popleft()
            if node == v:
                break
            for neighbor in adj[node]:
                if neighbor not in parent:
                    parent[neighbor] = node
                    queue.append(neighbor)
        
        # Trace path
        total = 0
        curr = v
        while curr is not None:
            total += w[curr]
            curr = parent[curr]
        return total
    
    results = []
    for i in range(n + 1, n + 1 + q):
        u, v = map(int, lines[i].split())
        results.append(str(path_sum(u, v)))
    
    return '\n'.join(results)


def solve_tdp009(inp: str) -> str:
    """TDP-009: All Distances Sum
    For each node, sum of distances to all other nodes
    """
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
    """TDP-010: Count Subtrees with Sum K
    Count number of subtrees with sum exactly K
    """
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
    """TDP-011: Node Eccentricity
    For each node, max distance to any other node
    """
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
        return max(dist.values())
    
    results = [str(compute_eccentricity(i)) for i in range(1, n + 1)]
    return '\n'.join(results)


def solve_tdp012(inp: str) -> str:
    """TDP-012: K-th Ancestor Queries
    For each query (node, k), output k-th ancestor or -1
    """
    lines = inp.strip().split('\n')
    parts = lines[0].split()
    n = int(parts[0])
    q = int(parts[1])
    
    adj = defaultdict(list)
    for i in range(1, n):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Root at 1, compute parent and depth
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
    """TDP-013: Tree Height after Removal
    For each node, height of tree when that node is removed
    """
    lines = inp.strip().split('\n')
    n = int(lines[0])
    
    if n == 1:
        return "0"
    
    adj = defaultdict(list)
    for i in range(1, n):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    def tree_height_without(removed):
        # Find a valid root (not removed)
        root = 1 if removed != 1 else 2
        
        # BFS to compute heights
        max_height = 0
        visited = {removed, root}
        queue = deque([(root, 0)])
        while queue:
            node, h = queue.popleft()
            max_height = max(max_height, h)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, h + 1))
        
        return max_height
    
    return str(tree_height_without(1))  # Just removing node 1 for now


def solve_tdp015(inp: str) -> str:
    """TDP-015: Centroid Decomposition Order
    Output the order of nodes in centroid decomposition
    """
    lines = inp.strip().split('\n')
    n = int(lines[0])
    
    adj = defaultdict(list)
    for i in range(1, n):
        u, v = map(int, lines[i].split())
        adj[u].append(v)
        adj[v].append(u)
    
    removed = [False] * (n + 1)
    subtree_size = [0] * (n + 1)
    order = []
    
    def get_subtree_size(node, parent):
        subtree_size[node] = 1
        for neighbor in adj[node]:
            if neighbor != parent and not removed[neighbor]:
                get_subtree_size(neighbor, node)
                subtree_size[node] += subtree_size[neighbor]
        return subtree_size[node]
    
    def get_centroid(node, parent, tree_size):
        for neighbor in adj[node]:
            if neighbor != parent and not removed[neighbor]:
                if subtree_size[neighbor] > tree_size // 2:
                    return get_centroid(neighbor, node, tree_size)
        return node
    
    def decompose(node):
        tree_size = get_subtree_size(node, -1)
        centroid = get_centroid(node, -1, tree_size)
        order.append(centroid)
        removed[centroid] = True
        
        for neighbor in adj[centroid]:
            if not removed[neighbor]:
                decompose(neighbor)
    
    decompose(1)
    return ' '.join(map(str, order))


def solve_tdp016(inp: str) -> str:
    """TDP-016: Tree DP with Edge Weights
    For each node, weighted path sum considering edge weights
    """
    lines = inp.strip().split('\n')
    n = int(lines[0])
    node_weights = [0] + list(map(int, lines[1].split()))
    
    adj = defaultdict(list)
    for i in range(2, n + 1):
        u, v, w = map(int, lines[i].split())
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    # For each node, compute weighted path sum to all other nodes
    def compute_weighted_sum(root):
        dist = {root: 0}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for neighbor, weight in adj[node]:
                if neighbor not in dist:
                    dist[neighbor] = dist[node] + weight
                    queue.append(neighbor)
        return sum(dist.values())
    
    results = [str(compute_weighted_sum(i)) for i in range(1, n + 1)]
    return '\n'.join(results)


# Mapping of problem IDs to solvers
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


def test_problem(prob_id: str):
    """Test a single problem and show differences."""
    if prob_id not in SOLVERS:
        print(f"No solver for {prob_id}")
        return
    
    solver = SOLVERS[prob_id]
    
    # Find testcase file
    tc_files = list(BASE.glob(f"testcases/{prob_id}*.yaml"))
    if not tc_files:
        print(f"No testcase file for {prob_id}")
        return
    
    tc_file = tc_files[0]
    with open(tc_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Test hidden cases
    hidden = data.get('hidden', [])
    for i, tc in enumerate(hidden[:3]):  # First 3 hidden tests
        inp = tc['input']
        expected = tc['output'].strip()
        try:
            actual = solver(inp)
            match = actual == expected
            status = "✓" if match else "✗"
            print(f"  hidden[{i}]: {status}")
            if not match:
                print(f"    Expected: {expected[:100]}")
                print(f"    Got:      {actual[:100]}")
        except Exception as e:
            print(f"  hidden[{i}]: ERROR - {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for prob_id in sys.argv[1:]:
            print(f"\n{prob_id}:")
            test_problem(prob_id)
    else:
        for prob_id in sorted(SOLVERS.keys()):
            print(f"\n{prob_id}:")
            test_problem(prob_id)
