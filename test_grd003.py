import sys

def max_stalls(stalls: list, d: int) -> int:
    # Sort by end time (second element)
    stalls.sort(key=lambda x: x[1])
    
    count = 0
    last_end = -float('inf')
    
    for start, end in stalls:
        if start - last_end >= d:
            count += 1
            last_end = end
            
    return count

def main():
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
    print(result)

if __name__ == "__main__":
    main()
