"""Fix all MathAdvanced main() functions to use hardcoded MOD instead of reading from input."""

import re
from pathlib import Path

# Map of problem_id to MOD value (998244353 for NTT problems, 1000000007 for others)
PROBLEM_MODS = {
    "MTH-001": 1000000007,  # Polynomial multiplication with 10^9+7
    "MTH-002": 998244353,   # NTT
    "MTH-003": 998244353,   # Polynomial inverse (NTT)
    "MTH-004": 1000000007,  # Multipoint evaluation
    "MTH-005": 1000000007,  # Lagrange interpolation
    "MTH-006": 1000000007,  # Determinant
    "MTH-007": 1000000007,  # Matrix exponentiation
    "MTH-008": 1000000007,  # FWHT
    "MTH-009": 1000000007,  # Subset convolution (already works)
    "MTH-010": 1000000007,  # Berlekamp-Massey
    "MTH-011": 1000000007,  # Minimal polynomial
    "MTH-012": 1000000007,  # Multi-mod CRT
    "MTH-013": 1000000007,  # Invert Vandermonde
    "MTH-014": None,        # Eigenvalue (doesn't use MOD)
}

# Problems that need main() fixes
PROBLEMS_TO_FIX = [
    ("MTH-001", "polynomial-multiplication-fft"),
    ("MTH-002", "convolution-ntt"),
    ("MTH-003", "inverse-polynomial"),
    ("MTH-004", "multipoint-evaluation"),
    ("MTH-005", "lagrange-interpolation-mod"),
    ("MTH-006", "determinant-gaussian"),
    ("MTH-007", "matrix-exp-linear-recurrence"),
    ("MTH-008", "fwht-xor-convolution"),
    # MTH-009 already works
    ("MTH-010", "berlekamp-massey"),
    ("MTH-011", "minimal-polynomial-matrix"),
    ("MTH-012", "convolution-multi-mod-crt"),
    ("MTH-013", "invert-vandermonde"),
    ("MTH-014", "largest-eigenvalue-power"),
]

def fix_problem(problem_id, slug):
    """Fix main() function for a problem."""
    filepath = Path(f"dsa-problems/MathAdvanced/editorials/{problem_id}-{slug}.md")
    
    if not filepath.exists():
        print(f"SKIP: {filepath} not found")
        return False
    
    content = filepath.read_text(encoding='utf-8')
    
    # Find the Python main() function
    pattern = r'(### Python\s+```python\s+import sys.*?def main\(\):.*?```)'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"ERROR: No Python main() found in {problem_id}")
        return False
    
    python_section = match.group(1)
    
    mod_value = PROBLEM_MODS.get(problem_id)
    
    # Check what needs to be fixed based on problem
    if problem_id == "MTH-001":
        # Remove MOD = int(next(iterator)) line, add MOD = 1000000007
        if "MOD = int(next(iterator))" in python_section or "MOD = int(data[" in python_section:
            new_section = python_section.replace(
                "MOD = int(next(iterator))",
                "MOD = 1000000007  # Fixed modulo"
            ).replace(
                "MOD = int(data[",
                "# MOD = int(data["
            )
            content = content.replace(python_section, new_section)
            filepath.write_text(content, encoding='utf-8')
            print(f"FIXED: {problem_id} (removed MOD from input)")
            return True
    
    elif problem_id == "MTH-003":
        # Remove MOD input reading
        if "MOD = int(next(iterator))" in python_section:
            new_section = re.sub(
                r'P = \[int\(next\(iterator\)\) for _ in range\(k\)\]\s+MOD = int\(next\(iterator\)\)',
                'P = [int(next(iterator)) for _ in range(k)]\n        MOD = 998244353  # NTT modulo',
                python_section
            )
            content = content.replace(python_section, new_section)
            filepath.write_text(content, encoding='utf-8')
            print(f"FIXED: {problem_id}")
            return True
    
    elif problem_id == "MTH-004":
        # No MOD in MTH-004 - it doesn't use modulo
        # Actually checking the editorial...
        print(f"CHECK: {problem_id} - need to verify if it uses MOD")
        return False
    
    elif problem_id == "MTH-005":
        # Remove MOD from input: k X MOD points -> k X points
        if "MOD = int(next(iterator))" in python_section:
            new_section = re.sub(
                r'X = int\(next\(iterator\)\)\s+MOD = int\(next\(iterator\)\)',
                'X = int(next(iterator))\n        MOD = 1000000007  # Fixed modulo',
                python_section
            )
            content = content.replace(python_section, new_section)
            filepath.write_text(content, encoding='utf-8')
            print(f"FIXED: {problem_id}")
            return True
    
    elif problem_id in ["MTH-007", "MTH-010"]:
        # These read: m n S[0..m-1] MOD - remove MOD
        if "MOD = int(next(iterator))" in python_section:
            new_section = re.sub(
                r'S = \[int\(next\(iterator\)\) for _ in range\(m\)\]\s+MOD = int\(next\(iterator\)\)',
                f'S = [int(next(iterator)) for _ in range(m)]\n        MOD = {mod_value}  # Fixed modulo',
                python_section
            )
            content = content.replace(python_section, new_section)
            filepath.write_text(content, encoding='utf-8')
            print(f"FIXED: {problem_id}")
            return True
    
    elif problem_id == "MTH-012":
        # Reads: n m A[0..n-1] B[0..m-1] MOD
        if "MOD = int(next(iterator))" in python_section:
            new_section = re.sub(
                r'B = \[int\(next\(iterator\)\) for _ in range\(m\)\]\s+MOD = int\(next\(iterator\)\)',
                f'B = [int(next(iterator)) for _ in range(m)]\n        MOD = {mod_value}  # Fixed modulo',
                python_section
            )
            content = content.replace(python_section, new_section)
            filepath.write_text(content, encoding='utf-8')
            print(f"FIXED: {problem_id}")
            return True
    
    print(f"TODO: {problem_id} - manual fix needed")
    return False

def main():
    """Fix all problems."""
    for problem_id, slug in PROBLEMS_TO_FIX:
        fix_problem(problem_id, slug)

if __name__ == "__main__":
    main()
