#!/usr/bin/env python3
"""
FIXED VERSION: Fix syntax errors in Greedy editorial files
that were introduced by the previous fix attempt.
"""

import os
import re

# Base path
base = r"c:\Users\agundapaneni\OneDrive - Microsoft\Desktop\Nikhil\DSA\dsa-problems\Greedy\editorials"

# List of all problematic files
problems = {
    # Files with wrong parenthesis/semicolon placement
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
print("FIXING GREEDY EDITORIAL SYNTAX ERRORS")
print("=" * 60)

for prob_id, filename in problems.items():
    path = os.path.join(base, filename)
    
    if not os.path.exists(path):
        print(f"⚠️  {prob_id}: File not found")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix 1: Incorrect parenthesis placement like: int(data[idx]; idx += 1)
    # Should be: int(data[idx])); idx += 1
    content = re.sub(r'\(data\[idx\]; idx \+= 1\)', r'(data[idx])); idx += 1', content)
    
    # Fix 2: Incorrect parenthesis like: int(data[i; i += 1)
    # Should be: int(data[i])); i += 1
    content = re.sub(r'\(data\[i; i \+= 1\)', r'(data[i])); i += 1', content)
    
    # Fix 3: Missing closing parenthesis after data[idx]
    # Pattern: .append(int(data[idx]) where it should be .append(int(data[idx]))
    content = re.sub(r'\.append\(int\(data\[idx\]\)\)', r'.append(int(data[idx]))', content)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed {prob_id}")
    else:
        print(f"⚠️  {prob_id}: No changes needed")

print("=" * 60)
print("DONE")
print("=" * 60)
