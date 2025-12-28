import sys
sys.path.insert(0, '.')
from tree_generator_utils import generate_connected_binary_tree, count_leaves, format_tree_input

# Generate same tree as public[1]
tree = generate_connected_binary_tree(20, seed=210)
print("Input:")
print(format_tree_input(tree))
print("\nMy count:", count_leaves(tree))

# Manually count using editorial logic
count = 0
for val, left, right in tree:
    if left == -1 and right == -1:
        count += 1
print("Editorial count:", count)
