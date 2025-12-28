import random

random.seed(412)

# Generate sample tests
print("=== SAMPLES ===")
for sample_idx in range(3):
    n = random.randint(1, 3)
    k = random.randint(0, 3)
    tasks = []
    for i in range(n):
        task = chr(65 + i)
        count = random.randint(1, 5)
        priority = random.randint(1, 3)
        tasks.append((task, count, priority))
    
    print(f"Sample {sample_idx}: n={n}, k={k}")
    for t, c, p in tasks:
        print(f"  {t}: count={c}, pri={p}")
    print()

print("=== PUBLIC (first 2) ===")
for idx in range(2):
    n = random.randint(1, 5)
    k = random.randint(0, 10)
    tasks = []
    for i in range(n):
        task = chr(65 + i)
        count = random.randint(1, 20)
        priority = random.randint(1, 3)
        tasks.append((task, count, priority))
    
    print(f"Public {idx}: n={n}, k={k}")
    for t, c, p in tasks:
        print(f"  {t}: count={c}, pri={p}")
    print()
