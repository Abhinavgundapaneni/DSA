---
title: Circuit Postfix Evaluator with Variables
slug: circuit-postfix-variables
difficulty: Medium
difficulty_score: 55
tags:
- Stack
- Postfix Evaluation
- Parsing
problem_id: STK_CIRCUIT_POSTFIX_VARIABLES__7493
display_id: STK-011
topics:
- Stack
- Expression Evaluation
- Parsing
---
# Circuit Postfix Evaluator with Variables - Editorial

## Problem Summary

Evaluate a postfix expression (Reverse Polish Notation) containing:
-   Integers and Variables (single letters).
-   Operators: `+`, `-`, `*`, `/`, `%`.
-   Stack Operations: `DUP` (duplicate top), `SWAP` (swap top two).
-   All calculations are modulo `10^9 + 7`.
-   Division uses "integer division after modulo normalization".
-   If `a` and `b` are normalized to `[0, MOD-1]`, then `a/b` is just `floor(a/b)`.


## Constraints

- `1 <= t <= 10000`
- `0 <= m <= 26`
- Variable values fit in 64-bit signed integer
## Real-World Scenario

Imagine you are designing a **Programmable Circuit Controller**.
-   The controller receives instructions in a compact "stack-based" bytecode (like Java Bytecode or PostScript).
-   Variables represent sensor inputs (e.g., `t` for temperature, `p` for pressure).
-   The instructions tell the controller how to combine these inputs to calculate a control signal.
-   `DUP` and `SWAP` allow efficient data manipulation without re-reading sensors.

## Problem Exploration

### 1. Postfix Evaluation
-   Standard algorithm: Iterate through tokens.
-   If operand (number/variable): Push to stack.
-   If operator: Pop required operands, compute, push result.
-   This works perfectly for `+ - * / %`.

### 2. Variables
-   We are given a map of variable values.
-   When we encounter a variable token (e.g., "x"), we look up its value and push that.

### 3. Stack Operations
-   `DUP`: Pop `x`, push `x`, push `x`. (Or just `peek` and push).
-   `SWAP`: Pop `a`, pop `b`, push `a`, push `b`.

### 4. Modulo Arithmetic
-   `MOD = 1000000007`.
-   Addition: `(a + b) % MOD`.
-   Subtraction: `(a - b + MOD) % MOD`. (Crucial to handle negative results).
-   Multiplication: `(a * b) % MOD`.
-   Modulo: `a % b`. (Since inputs are normalized, this is just `a % b`. But `b` could be 0? Problem assumes valid expression).
-   Division: "integer division after modulo normalization".
    -   This likely means: `val1 = stack.pop()`, `val2 = stack.pop()`.
    -   `res = (val2 % MOD) / (val1 % MOD)`.
    -   Since we store values already modulo'd, it's just `val2 / val1`.
    -   Note: In standard modular arithmetic fields, division is `val2 * modInverse(val1)`. But the problem explicitly says "integer division". This is a specific rule for this problem.

## Approaches

### Approach 1: Stack Simulation
-   Use a stack of `long` (64-bit integers) to prevent overflow before modulo.
-   Iterate tokens.
-   Handle each type.
-   Complexity: `O(T)` time, `O(T)` space.

## Implementations

### Java

```java
import java.util.*;

class Solution {
    long MOD = 1000000007L;

    public long eval(List<String> tokens, Map<String, Long> vars) {
        Stack<Long> stack = new Stack<>();
        
        for (String token : tokens) {
            if (vars.containsKey(token)) {
                stack.push(vars.get(token) % MOD);
            } else if (isNumber(token)) {
                stack.push(Long.parseLong(token) % MOD);
            } else if (token.equals("DUP")) {
                stack.push(stack.peek());
            } else if (token.equals("SWAP")) {
                long a = stack.pop();
                long b = stack.pop();
                stack.push(a);
                stack.push(b);
            } else {
                long b = stack.pop();
                long a = stack.pop();
                long res = 0;
                
                switch (token) {
                    case "+": res = (a + b) % MOD; break;
                    case "-": res = (a - b + MOD) % MOD; break;
                    case "*": res = (a * b) % MOD; break;
                    case "/": res = a / b; break; // Integer division as per problem
                    case "%": res = a % b; break;
                }
                stack.push(res);
            }
        }
        return stack.pop();
    }
    
    private boolean isNumber(String s) {
        try {
            Long.parseLong(s);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }
}
```

### Python

```python
def eval_postfix(tokens: list[str], vars: dict[str, int]) -> int:
    stack = []
    MOD = 1000000007
    
    for token in tokens:
        if token in vars:
            stack.append(vars[token] % MOD)
        elif token.lstrip("-").isdigit(): # Handle negative numbers
            stack.append(int(token) % MOD)
        elif token == "DUP":
            stack.append(stack[-1])
        elif token == "SWAP":
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)
        else:
            b = stack.pop()
            a = stack.pop()
            res = 0
            
            if token == "+":
                res = (a + b) % MOD
            elif token == "-":
                res = (a - b + MOD) % MOD
            elif token == "*":
                res = (a * b) % MOD
            elif token == "/":
                res = a // b # Integer division
            elif token == "%":
                res = a % b
            
            stack.append(res)
            
    return stack[-1]

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    tokens = lines[1].split()
    k = int(lines[2])
    variables = {}
    for i in range(3, 3 + k):
        var, val = lines[i].split()
        variables[var] = int(val)
    
    print(eval_postfix(tokens, variables))

if __name__ == "__main__":
    main()

```

### C++

```cpp
#include <vector>
#include <string>
#include <stack>
#include <unordered_map>

using namespace std;

class Solution {
    long long MOD = 1000000007;
    
    bool isNumber(const string& s) {
        if (s.empty()) return false;
        if (isdigit(s[0])) return true;
        if (s.size() > 1 && s[0] == '-' && isdigit(s[1])) return true;
        return false;
    }

public:
    long long eval(const vector<string>& tokens, const unordered_map<string, long long>& vars) {
        stack<long long> st;
        
        for (const string& token : tokens) {
            if (vars.count(token)) {
                st.push((vars.at(token) % MOD + MOD) % MOD); // Normalize input
            } else if (isNumber(token)) {
                st.push((stoll(token) % MOD + MOD) % MOD);
            } else if (token == "DUP") {
                st.push(st.top());
            } else if (token == "SWAP") {
                long long a = st.top(); st.pop();
                long long b = st.top(); st.pop();
                st.push(a);
                st.push(b);
            } else {
                long long b = st.top(); st.pop();
                long long a = st.top(); st.pop();
                long long res = 0;
                
                if (token == "+") res = (a + b) % MOD;
                else if (token == "-") res = (a - b + MOD) % MOD;
                else if (token == "*") res = (a * b) % MOD;
                else if (token == "/") res = a / b;
                else if (token == "%") res = a % b;
                
                st.push(res);
            }
        }
        return st.top();
    }
};
```

### JavaScript

```javascript
class Solution {
  eval(tokens, vars) {
    const stack = [];
    const MOD = 1000000007n;
    
    for (const token of tokens) {
      if (vars.has(token)) {
        let val = BigInt(vars.get(token)) % MOD;
        if (val < 0n) val += MOD;
        stack.push(val);
      } else if (!isNaN(token)) {
        let val = BigInt(token) % MOD;
        if (val < 0n) val += MOD;
        stack.push(val);
      } else if (token === "DUP") {
        stack.push(stack[stack.length - 1]);
      } else if (token === "SWAP") {
        const a = stack.pop();
        const b = stack.pop();
        stack.push(a);
        stack.push(b);
      } else {
        const b = stack.pop();
        const a = stack.pop();
        let res = 0n;
        
        if (token === "+") res = (a + b) % MOD;
        else if (token === "-") res = (a - b + MOD) % MOD;
        else if (token === "*") res = (a * b) % MOD;
        else if (token === "/") res = a / b;
        else if (token === "%") res = a % b;
        
        stack.push(res);
      }
    }
    return Number(stack[stack.length - 1]);
  }
}
```

### Python

```python

def evaluate_postfix(tokens, variables):
    stack = []
    MOD = 10**9 + 7
    
    for token in tokens:
        if token in ['+', '-', '*']:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append((a + b) % MOD)
            elif token == '-':
                stack.append((a - b) % MOD)
            elif token == '*':
                stack.append((a * b) % MOD)
        else:
            stack.append(variables[token])
    
    return stack[0]

def main():
    import sys
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    tokens = lines[1].split()
    k = int(lines[2])
    variables = {}
    for i in range(3, 3 + k):
        var, val = lines[i].split()
        variables[var] = int(val)
    
    print(evaluate_postfix(tokens, variables))

if __name__ == "__main__":
    main()

```

## 🧪 Test Case Walkthrough (Dry Run)
**Input:** `x 5 + y *`, `x=3, y=2`

1.  `x`: Push `3`. Stack `[3]`.
2.  `5`: Push `5`. Stack `[3, 5]`.
3.  `+`: Pop `5`, `3`. `3 + 5 = 8`. Push `8`. Stack `[8]`.
4.  `y`: Push `2`. Stack `[8, 2]`.
5.  `*`: Pop `2`, `8`. `8 * 2 = 16`. Push `16`. Stack `[16]`.

**Result:** `16`.

## Proof of Correctness

-   **Postfix Property**: Postfix expressions are unambiguously evaluated using a stack.
-   **Modulo Operations**: Applying modulo at each step (except division, as specified) keeps numbers within range and satisfies the problem constraints.
-   **Stack Ops**: `DUP` and `SWAP` are correctly implemented as stack manipulations.

## Interview Extensions

1.  **Infix to Postfix**: Convert `(x + 5) * y` to postfix first.
    -   *Hint*: Shunting Yard Algorithm.
2.  **Error Handling**: What if division by zero?
    -   *Hint*: Check `b == 0` before dividing.

### Common Mistakes

-   **Negative Modulo**: `(a - b) % MOD` can be negative in C++/Java. Use `(a - b + MOD) % MOD`.
-   **Division**: Using modular inverse when "integer division" is requested.
-   **Variable Lookup**: Forgetting to check the map for variables.
