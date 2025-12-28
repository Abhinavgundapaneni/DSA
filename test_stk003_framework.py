#!/usr/bin/env python3
import sys
import os

# Get to workspace root
os.chdir(r'c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA')
sys.path.insert(0, os.getcwd())

from test_topic_editorials import test_single_problem

print("Testing STK-003 with test framework...")
result = test_single_problem('STACKS', 'STK-003')
print(f"\nResult: {result['passed']}/{result['total']} tests passed")
if result['errors']:
    print(f"\nFirst error:")
    print(result['errors'][0])
