import sys
from io import StringIO

# MTH-005 editorial code
class Solution:
    def lagrange_interpolation_mod(self, k: int, X: int, MOD: int, points: list) -> int:
        def power(base, exp):
            res = 1
            base %= MOD
            while exp > 0:
                if exp % 2 == 1: res = (res * base) % MOD
                base = (base * base) % MOD
                exp //= 2
            return res

        def modInverse(x):
            return power(x, MOD - 2)

        ans = 0
        for i in range(k):
            xi, yi = points[i]
            num = yi
            den = 1
            for j in range(k):
                if i == j: continue
                xj, _ = points[j]
                num = (num * (X - xj)) % MOD
                den = (den * (xi - xj)) % MOD
            
            term = (yi * num) % MOD
            term = (term * modInverse(den)) % MOD
            ans = (ans + term) % MOD
            
        return (ans + MOD) % MOD

# Test with first sample
test_input = """3 5 1000000007
0 1
1 3
2 7"""

old_stdin = sys.stdin
try:
    sys.stdin = StringIO(test_input)
    
    # Read using the main() format
    data = sys.stdin.read().split()
    print(f"Data: {data}")
    
    iterator = iter(data)
    k = int(next(iterator))
    X = int(next(iterator))
    MOD = int(next(iterator))
    
    points = []
    for _ in range(k):
        points.append([int(next(iterator)), int(next(iterator))])
    
    print(f"k={k}, X={X}, MOD={MOD}")
    print(f"points={points}")
    
    sol = Solution()
    result = sol.lagrange_interpolation_mod(k, X, MOD, points)
    print(f"Result: {result}")
    
finally:
    sys.stdin = old_stdin
