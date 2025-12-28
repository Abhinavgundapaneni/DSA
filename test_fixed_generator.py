import sys
sys.path.insert(0, r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA')

import importlib
if 'regenerate_greedy_correct' in sys.modules:
    del sys.modules['regenerate_greedy_correct']

from regenerate_greedy_correct import solve_grd012

result = solve_grd012([('A', 13, 2), ('B', 11, 2), ('C', 18, 1)], 8)
print(f"Fixed generator: {result}")
print(f"Expected: 254 (to match editorial)")
