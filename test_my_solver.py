import sys
sys.path.insert(0, r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA')
from regenerate_greedy_correct import solve_grd012

# Sample 1: A:4, k=1
result = solve_grd012([('A', 4, 2)], 1)
print(f"Sample 1 result: {result}, expected: 7")

# Public 1: A:13/B:11/C:18, k=8
result2 = solve_grd012([('A', 13, 2), ('B', 11, 2), ('C', 18, 1)], 8)
print(f"Public 1 result: {result2}, expected: 245")
