from collections import deque
import random
import yaml

def solve(r, c, grid):
    queue = deque()
    unlit = 0
    for i in range(r):
        for j in range(c):
            if grid[i][j] == 1:
                queue.append((i, j, 0))
            else:
                unlit += 1
                
    if unlit == 0:
        return 0
    if not queue:
        return -1
        
    max_dist = 0
    visited = [[False]*c for _ in range(r)]
    for i, j, d in queue:
        visited[i][j] = True
        
    while queue:
        curr_r, curr_c, d = queue.popleft()
        max_dist = max(max_dist, d)
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc
            if 0 <= nr < r and 0 <= nc < c and not visited[nr][nc] and grid[nr][nc] == 0:
                visited[nr][nc] = True
                unlit -= 1
                queue.append((nr, nc, d + 1))
                
    return max_dist if unlit == 0 else -1

def make_test_case(grid):
    r = len(grid)
    c = len(grid[0])
    res = solve(r, c, grid)
    input_str = f"{r} {c}\n" + "\n".join(" ".join(map(str, row)) for row in grid)
    output_str = str(res)
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]]),
            make_test_case([[1, 1], [1, 1]]),
            make_test_case([[0, 0], [0, 0]])
        ],
        "public": [
            make_test_case([[1, 0], [0, 0]]),  # Single source
            make_test_case([[1, 0, 0], [0, 0, 0], [0, 0, 1]]),  # Two sources
            make_test_case([[1]*3 for _ in range(3)]),  # All lit
            make_test_case([[0]*3 for _ in range(3)]),  # None lit
            make_test_case([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # Diagonal
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case([[1]]))  # 1x1 lit
    tc["hidden"].append(make_test_case([[0]]))  # 1x1 unlit
    tc["hidden"].append(make_test_case([[1, 0]]))  # 1x2
    tc["hidden"].append(make_test_case([[1], [0]]))  # 2x1
    tc["hidden"].append(make_test_case([[1, 1], [1, 1]]))  # 2x2 all lit
    tc["hidden"].append(make_test_case([[0, 0], [0, 0]]))  # 2x2 none
    tc["hidden"].append(make_test_case([[1, 0], [0, 1]]))  # 2x2 diagonal
    tc["hidden"].append(make_test_case([[1, 0, 0], [0, 0, 0], [0, 0, 0]]))  # Corner only

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case([[1] + [0]*9]))  # 1x10 one source
    tc["hidden"].append(make_test_case([[1 if i == j else 0 for j in range(5)] for i in range(5)]))  # 5x5 diagonal
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(6)] for _ in range(6)]))  # 6x6 random
    tc["hidden"].append(make_test_case([[1]*8 for _ in range(8)]))  # 8x8 all lit
    tc["hidden"].append(make_test_case([[0]*8 for _ in range(8)]))  # 8x8 none
    tc["hidden"].append(make_test_case([[1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
                                       [0, 0, 0, 0, 0], [0, 0, 0, 0, 1]]))  # 5x5 corners
    tc["hidden"].append(make_test_case([[1 if (i+j) % 2 == 0 else 0 for j in range(7)] for i in range(7)]))  # Checkerboard
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(10)] for _ in range(10)]))  # 10x10 random

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case([[1, 0, 0], [0, 0, 0], [0, 0, 0]]))  # 3x3 one corner
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(4)] for _ in range(4)]))  # 4x4 random
    tc["hidden"].append(make_test_case([[1 if i == 0 else 0 for _ in range(5)] for i in range(5)]))  # 5x5 first row
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(5)] for _ in range(5)]))  # 5x5 random
    tc["hidden"].append(make_test_case([[1 if j == 0 else 0 for j in range(6)] for _ in range(6)]))  # 6x6 first col
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(7)] for _ in range(7)]))  # 7x7 random
    tc["hidden"].append(make_test_case([[1 if (i == 0 or j == 0) else 0 for j in range(8)] for i in range(8)]))  # 8x8 edges
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(8)] for _ in range(8)]))  # 8x8 random
    tc["hidden"].append(make_test_case([[1 if i < 3 else 0 for _ in range(9)] for i in range(9)]))  # 9x9 top rows
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(10)] for _ in range(10)]))  # 10x10 random
    tc["hidden"].append(make_test_case([[1 if (i+j) < 6 else 0 for j in range(12)] for i in range(12)]))  # 12x12 diagonal
    tc["hidden"].append(make_test_case([[random.randint(0, 1) for _ in range(12)] for _ in range(12)]))  # 12x12 random

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
