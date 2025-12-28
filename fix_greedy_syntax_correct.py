#!/usr/bin/env python3
"""
CORRECT VERSION: Fix the greedy editorial files.
The issue is that the previous fix used semicolons incorrectly in Python.
Python doesn't use semicolons to separate statements in the same way as C/Java.

The pattern:
    variable.append(int(data[idx]); idx += 1)
    
Should be:
    variable.append(int(data[idx]))
    idx += 1
"""

import os
import re

# Base path
base = r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Greedy\editorials"

# List of all problematic files
problems = {
    "GRD-003": "GRD-003-festival-stall-placement.md",
    "GRD-005": "GRD-005-shuttle-overtime-minimizer.md",
    "GRD-006": "GRD-006-robotics-component-bundling-loss-quality.md",
    "GRD-007": "GRD-007-campus-wifi-expansion.md",
    "GRD-008": "GRD-008-exam-proctor-allocation.md",
    "GRD-010": "GRD-010-library-merge-queues.md",
    "GRD-011": "GRD-011-campus-event-ticket-caps.md",
    "GRD-012": "GRD-012-workshop-task-cooldown-priority.md",
    "GRD-013": "GRD-013-auditorium-seat-refunds.md",
    "GRD-014": "GRD-014-festival-bandwidth-split.md",
    "GRD-015": "GRD-015-robotics-median-after-batches-stale.md",
}

print("=" * 60)
print("FIXING GREEDY EDITORIAL PYTHON SYNTAX")
print("=" * 60)

for prob_id, filename in problems.items():
    path = os.path.join(base, filename)
    
    if not os.path.exists(path):
        print(f"⚠️  {prob_id}: File not found")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    modified = False
    
    for i, line in enumerate(lines):
        # Check for the problematic pattern: something); idx += 1) or similar
        # Pattern 1: .append(int(data[idx]); idx += 1)
        if re.search(r'\(data\[idx\]\); idx \+= 1\)', line):
            # Split into two lines
            indent = len(line) - len(line.lstrip())
            spaces = ' ' * indent
            
            # Extract the statement before the semicolon
            match = re.search(r'(.+)\(data\[idx\]\); idx \+= 1\)', line)
            if match:
                first_part = match.group(1) + '(data[idx]))\n'
                second_part = spaces + 'idx += 1\n'
                fixed_lines.append(first_part)
                fixed_lines.append(second_part)
                modified = True
                continue
        
        # Pattern 2: variable = int(data[idx]); idx += 1
        if re.search(r'= int\(data\[idx\]\); idx \+= 1', line):
            indent = len(line) - len(line.lstrip())
            spaces = ' ' * indent
            
            match = re.search(r'(.+ = int\(data\[idx\]\));', line)
            if match:
                first_part = match.group(1) + '\n'
                second_part = spaces + 'idx += 1\n'
                fixed_lines.append(first_part)
                fixed_lines.append(second_part)
                modified = True
                continue
        
        # Pattern 3: .append(int(data[i; i += 1) - wrong pattern from before
        if re.search(r'\(data\[i; i \+= 1\)', line):
            indent = len(line) - len(line.lstrip())
            spaces = ' ' * indent
            
            match = re.search(r'(.+)\(data\[i; i \+= 1\)', line)
            if match:
                first_part = match.group(1) + '(data[i]))\n'
                second_part = spaces + 'i += 1\n'
                fixed_lines.append(first_part)
                fixed_lines.append(second_part)
                modified = True
                continue
        
        # Pattern 4: variable = int(data[i); i += 1
        if re.search(r'= int\(data\[i\); i \+= 1', line):
            indent = len(line) - len(line.lstrip())
            spaces = ' ' * indent
            
            match = re.search(r'(.+ = int\(data\[i\));', line)
            if match:
                first_part = match.group(1) + '\n'
                second_part = spaces + 'i += 1\n'
                fixed_lines.append(first_part)
                fixed_lines.append(second_part)
                modified = True
                continue
        
        # No match, keep the line as-is
        fixed_lines.append(line)
    
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        print(f"✅ Fixed {prob_id}")
    else:
        print(f"⚠️  {prob_id}: No changes needed")

print("=" * 60)
print("DONE")
print("=" * 60)
