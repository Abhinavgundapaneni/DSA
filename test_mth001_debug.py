import sys
from io import StringIO
import cmath

# Extract and test MTH-001 editorial code
test_input = """2 2
1 2
3 4"""

class Solution:
    def multiply_polynomials(self, A: list[int], B: list[int]) -> list[int]:
        MOD = 1000000007
        S = 1 << 15  # Split size
        
        def fft(a, invert):
            n = len(a)
            if n == 1: return
            
            a0 = [a[i] for i in range(0, n, 2)]
            a1 = [a[i] for i in range(1, n, 2)]
            
            fft(a0, invert)
            fft(a1, invert)
            
            ang = 2 * cmath.pi / n * (-1 if invert else 1)
            w = 1
            wn = cmath.exp(1j * ang)
            
            for i in range(n // 2):
                t = w * a1[i]
                a[i] = a0[i] + t
                a[i + n // 2] = a0[i] - t
                w *= wn
                
            if invert:
                for i in range(n):
                    a[i] /= 2
        
        def multiply_mod(A, B, mod):
            n = 1
            while n < len(A) + len(B):
                n <<= 1
                
            fa = [complex(x) for x in A] + [complex(0)] * (n - len(A))
            fb = [complex(x) for x in B] + [complex(0)] * (n - len(B))
            
            fft(fa, False)
            fft(fb, False)
            
            for i in range(n):
                fa[i] *= fb[i]
                
            fft(fa, True)
            
            res = []
            for i in range(len(A) + len(B) - 1):
                val = int(fa[i].real + 0.5) % mod
                res.append(val)
            return res
        
        # Split each coefficient into parts
        A0 = [x % S for x in A]
        A1 = [x // S for x in A]
        B0 = [x % S for x in B]
        B1 = [x // S for x in B]
        
        c0 = multiply_mod(A0, B0, MOD)
        c1_temp1 = multiply_mod(A0, B1, MOD)
        c1_temp2 = multiply_mod(A1, B0, MOD)
        c2 = multiply_mod(A1, B1, MOD)
        
        res = []
        for i in range(len(c0)):
            v0 = c0[i]
            v1 = (c1_temp1[i] + c1_temp2[i]) % MOD
            v2 = c2[i] if i < len(c2) else 0
            val = (v2 * S * S + v1 * S + v0) % MOD
            res.append(val)
            
        return res

old_stdin = sys.stdin
try:
    sys.stdin = StringIO(test_input)
    data = sys.stdin.read().split()
    
    iterator = iter(data)
    n = int(next(iterator))
    m = int(next(iterator))
    A = [int(next(iterator)) for _ in range(n)]
    B = [int(next(iterator)) for _ in range(m)]
    
    print(f"n={n}, m={m}")
    print(f"A={A}")
    print(f"B={B}")
    
    sol = Solution()
    res = sol.multiply_polynomials(A, B)
    print(f"Result: {res}")
    print(f"Output: {' '.join(map(str, res))}")
    
finally:
    sys.stdin = old_stdin
