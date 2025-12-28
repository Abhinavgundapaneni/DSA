s = "programming"
# p r o g r a m m i n g
# 0 1 2 3 4 5 6 7 8 9 10

print("Let's check all substrings of length 5:")
for i in range(len(s) - 4):
    substr = s[i:i+5]
    print(f"{i}-{i+4}: '{substr}'")
    
print("\nNow let's look at index 2-6:")
print(f"s[2:7] = '{s[2:7]}'")

print("\nExpected output claims 'ograr' - where is this?")
print(f"Is 'ograr' in s? {s.find('ograr')}")

# Wait, maybe the test case expects something else
# Let me check the positions more carefully
print("\nMaybe it's extracted differently:")
positions = [2, 3, 4, 5, 6]
chars = [s[i] for i in positions]
print(f"Positions {positions}: {''.join(chars)}")
