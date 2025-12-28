"""
Comprehensive Queue Test Case Regeneration Script
Fixes all generators and regenerates test cases
"""
import os
import sys
import subprocess

# List of all Queue problems
QUEUE_PROBLEMS = [
    "QUE-001-campus-service-line",
    "QUE-002-circular-shuttle-buffer-overwrite",
    "QUE-003-cafeteria-queue-rotation",
    "QUE-004-hallway-interleave",
    "QUE-005-lab-printer-reversal",
    "QUE-006-ticket-window-distinct-prefix",
    "QUE-007-lab-window-instability",
    "QUE-008-corridor-window-second-minimum",
    "QUE-009-battery-lab-first-negative",
    "QUE-010-shuttle-seat-assignment",
    "QUE-011-event-registration-merge",
    "QUE-012-bus-loop-one-skip",
    "QUE-013-task-stream-rate-limit",
    "QUE-014-deque-balance-rearrange",
    "QUE-015-festival-lantern-spread",
    "QUE-016-assembly-line-buffer-swap",
]

def regenerate_all():
    """Regenerate all Queue test cases"""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    base_path = "dsa-problems/Queues/testcases"
    gen_path = os.path.join(base_path, "tc_generators")
    
    print("=" * 80)
    print("QUEUE TEST CASE REGENERATION")
    print("=" * 80)
    
    for i, problem in enumerate(QUEUE_PROBLEMS, 1):
        # problem is like "QUE-001-campus-service-line"
        parts = problem.split("-")
        num_only = parts[1]  # "001"
        gen_file = f"generate_que{num_only}.py"
        gen_path_full = os.path.join(gen_path, gen_file)
        
        print(f"\n[{i}/16] {problem}")
        
        if not os.path.exists(gen_path_full):
            print(f"  ⚠️  Generator not found: {gen_file}")
            continue
        
        # Run generator
        try:
            result = subprocess.run(
                [sys.executable, gen_path_full],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Save YAML
                yaml_file = os.path.join(base_path, f"{problem}.yaml")
                with open(yaml_file, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                print(f"  ✅ Generated test cases")
            else:
                print(f"  ❌ Generator failed:")
                print(f"     {result.stderr[:200]}")
        except subprocess.TimeoutExpired:
            print(f"  ❌ Timeout after 30s")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("Regeneration complete!")
    print("=" * 80)

if __name__ == "__main__":
    regenerate_all()
