from io import StringIO
import sys

# Test input: "abc\n\n"
test_input = "abc\n\n"
sys.stdin = StringIO(test_input)

a = input().strip()
b = input().strip()

print(f"a = '{a}'")
print(f"b = '{b}'")
