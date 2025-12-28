import sys
from pathlib import Path
sys.path.insert(0, '.')
from test_topic_editorials import test_problem

result = test_problem('STK-007', Path('./dsa-problems/Stacks'))
print(f"STK-007: {result['passed']}/{result['total']} tests passing")
if result['passed'] < result['total']:
    print(f"\nFailed: {result['failed']}")
    if result['errors']:
        print("\nFirst 3 errors:")
        for err in result['errors'][:3]:
            print(f"  {err}")
