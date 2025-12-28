"""
Add main() functions to all Graphs editorial files.
"""

import re
from pathlib import Path

# Updated templates matching test expectations
MAIN_ADDITIONS = {
    "GRP-006": """

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
    
    # Count back edges in directed graph (cycles)
    visited = [False] * n
    rec_stack = [False] * n
    cycle_count = 0
    
    def dfs(u):
        nonlocal cycle_count
        visited[u] = True
        rec_stack[u] = True
        
        for v in adj[u]:
            if not visited[v]:
                dfs(v)
            elif rec_stack[v]:
                cycle_count += 1
        
        rec_stack[u] = False
    
    for i in range(n):
        if not visited[i]:
            dfs(i)
    
    print(cycle_count)

if __name__ == "__main__":
    main()
""",
    
    "GRP-007": """

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    indegree = [0] * n
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        indegree[v] += 1
    
    # Topological sort using Kahn's algorithm
    from collections import deque
    queue = deque()
    
    for i in range(n):
        if indegree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        u = queue.popleft()
        result.append(u)
        
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    
    if len(result) == n:
        print(len(result))
    else:
        print(0)  # Has cycle

if __name__ == "__main__":
    main()
""",
    
    "GRP-008": """

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # BFS from node 0, return max distance
    from collections import deque
    dist = [-1] * n
    dist[0] = 0
    queue = deque([0])
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    
    max_dist = max(d for d in dist if d != -1)
    print(max_dist)

if __name__ == "__main__":
    main()
""",
    
    "GRP-009": """

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    # Dijkstra from node 0
    import heapq
    dist = [float('inf')] * n
    dist[0] = 0
    pq = [(0, 0)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    
    # Return sum of all finite distances
    result = sum(d for d in dist if d != float('inf'))
    print(result)

if __name__ == "__main__":
    main()
""",
    
    "GRP-011": """

def main():
    n = int(input())
    m = int(input())
    
    grid = []
    for _ in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
    
    # Find max distance from any 0 to nearest 1
    from collections import deque
    queue = deque()
    dist = [[float('inf')] * m for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                queue.append((i, j))
                dist[i][j] = 0
    
    while queue:
        i, j = queue.popleft()
        for di, dj in [(0,1),(0,-1),(1,0),(-1,0)]:
            ni, nj = i+di, j+dj
            if 0 <= ni < n and 0 <= nj < m and dist[ni][nj] > dist[i][j] + 1:
                dist[ni][nj] = dist[i][j] + 1
                queue.append((ni, nj))
    
    max_dist = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 0 and dist[i][j] != float('inf'):
                max_dist = max(max_dist, dist[i][j])
    
    print(max_dist)

if __name__ == "__main__":
    main()
""",
    
    "GRP-013": """

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Find bridges using Tarjan's algorithm
    visited = [False] * n
    disc = [0] * n
    low = [0] * n
    parent = [-1] * n
    bridges = []
    timer = [0]
    
    def dfs(u):
        visited[u] = True
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        
        for v in adj[u]:
            if not visited[v]:
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                
                if low[v] > disc[u]:
                    bridges.append((min(u,v), max(u,v)))
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])
    
    for i in range(n):
        if not visited[i]:
            dfs(i)
    
    print(len(bridges))

if __name__ == "__main__":
    main()
""",
    
    "GRP-014": """

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Find articulation points
    visited = [False] * n
    disc = [0] * n
    low = [0] * n
    parent = [-1] * n
    ap = [False] * n
    timer = [0]
    
    def dfs(u):
        children = 0
        visited[u] = True
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        
        for v in adj[u]:
            if not visited[v]:
                parent[v] = u
                children += 1
                dfs(v)
                low[u] = min(low[u], low[v])
                
                if parent[u] == -1 and children > 1:
                    ap[u] = True
                if parent[u] != -1 and low[v] >= disc[u]:
                    ap[u] = True
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])
    
    for i in range(n):
        if not visited[i]:
            dfs(i)
    
    count = sum(ap)
    print(count)

if __name__ == "__main__":
    main()
""",
    
    "GRP-015": """

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Check if bipartite
    color = [-1] * n
    
    from collections import deque
    def is_bipartite():
        for start in range(n):
            if color[start] == -1:
                queue = deque([start])
                color[start] = 0
                
                while queue:
                    u = queue.popleft()
                    for v in adj[u]:
                        if color[v] == -1:
                            color[v] = 1 - color[u]
                            queue.append(v)
                        elif color[v] == color[u]:
                            return False
        return True
    
    if is_bipartite():
        count = sum(1 for c in color if c == 0)
        print(count)
    else:
        print(0)

if __name__ == "__main__":
    main()
""",
    
    "GRP-016": """

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Count edges in graph
    edge_count = sum(len(adj[i]) for i in range(n)) // 2
    print(edge_count)

if __name__ == "__main__":
    main()
""",
    
    "GRP-017": """

def main():
    n = int(input())
    m = int(input())
    
    grid = []
    for _ in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
    
    # BFS shortest path from (0,0) to (n-1,m-1)
    from collections import deque
    dist = [[float('inf')] * m for _ in range(n)]
    dist[0][0] = 0
    queue = deque([(0, 0)])
    
    while queue:
        i, j = queue.popleft()
        for di, dj in [(0,1),(0,-1),(1,0),(-1,0)]:
            ni, nj = i+di, j+dj
            if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == 0:
                if dist[ni][nj] > dist[i][j] + 1:
                    dist[ni][nj] = dist[i][j] + 1
                    queue.append((ni, nj))
    
    if dist[n-1][m-1] == float('inf'):
        print(0)
    else:
        print(dist[n-1][m-1])

if __name__ == "__main__":
    main()
""",
    
    "GRP-018": """

def main():
    n = int(input())
    m = int(input())
    
    adj = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    # Dijkstra from node 0, count reachable nodes
    import heapq
    dist = [float('inf')] * n
    dist[0] = 0
    pq = [(0, 0)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    
    # Count reachable nodes (dist < inf)
    count = sum(1 for d in dist if d != float('inf'))
    print(count)

if __name__ == "__main__":
    main()
"""
}

def add_main_to_editorial(problem_id, slug):
    """Add main() to editorial file."""
    filepath = Path(f"dsa-problems/Graphs/editorials/{problem_id}-{slug}.md")
    
    if not filepath.exists():
        print(f"ERROR: {filepath} not found")
        return False
    
    content = filepath.read_text(encoding='utf-8')
    
    # Find the Python section
    python_match = re.search(r'### Python\n\n```python\n(.*?)```', content, re.DOTALL)
    
    if not python_match:
        print(f"ERROR: No Python section found in {problem_id}")
        return False
    
    python_code = python_match.group(1)
    
    # Check if main() already exists
    if 'def main():' in python_code:
        print(f"SKIP: {problem_id} already has main()")
        return True
    
    # Add main() function
    if problem_id in MAIN_ADDITIONS:
        new_python_code = python_code.rstrip() + MAIN_ADDITIONS[problem_id]
        new_content = content.replace(python_match.group(0), f'### Python\n\n```python\n{new_python_code}```')
        
        filepath.write_text(new_content, encoding='utf-8')
        print(f"SUCCESS: Added main() to {problem_id}")
        return True
    else:
        print(f"ERROR: No template for {problem_id}")
        return False

def main():
    """Add main() to all Graphs editorial files."""
    problems = [
        ("GRP-006", "lab-directed-cycle-check"),
        ("GRP-007", "course-plan-mandatory-pairs"),
        ("GRP-008", "shuttle-shortest-stops"),
        ("GRP-009", "city-toll-dijkstra"),
        ("GRP-011", "library-fire-with-exhaustion"),
        ("GRP-013", "robotics-bridges"),
        ("GRP-014", "lab-articulation-points"),
        ("GRP-015", "shuttle-seating-assignment-feasibility"),
        ("GRP-016", "campus-carpool-pairing"),
        ("GRP-017", "festival-maze-shortest-path"),
        ("GRP-018", "robotics-weighted-reachability"),
    ]
    
    successful = 0
    for problem_id, slug in problems:
        if add_main_to_editorial(problem_id, slug):
            successful += 1
    
    print(f"\nSUMMARY: {successful}/{len(problems)} files updated")

if __name__ == "__main__":
    main()
