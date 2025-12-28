import sys
from pathlib import Path
sys.path.insert(0, '.')
from test_topic_editorials import test_problem

for prob_id in ['STK-008', 'STK-009', 'STK-010', 'STK-011']:
    result = test_problem(prob_id, Path('./dsa-problems/Stacks'))
    print(f"{prob_id}: {result['passed']}/{result['total']}")
    if result['passed'] < result['total'] and result['errors']:
        print(f"  First error: {result['errors'][0]}")
        print()
