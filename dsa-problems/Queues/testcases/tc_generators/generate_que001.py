import random
import yaml

def solve(commands):
    queue = []
    front_idx = 0
    results = []
    for cmd in commands:
        if cmd[0] == "ENQUEUE":
            queue.append(cmd[1])
        elif cmd[0] == "DEQUEUE":
            if front_idx < len(queue):
                results.append(str(queue[front_idx]))
                front_idx += 1
            else:
                results.append("EMPTY")
        elif cmd[0] == "FRONT":
            if front_idx < len(queue):
                results.append(str(queue[front_idx]))
            else:
                results.append("EMPTY")
    return results

def make_test_case(commands):
    results = solve(commands)
    input_str = f"{len(commands)}\n" + "\n".join(" ".join(map(str, cmd)) for cmd in commands)
    output_str = "\n".join(results)
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case([
                ["ENQUEUE", 12],
                ["ENQUEUE", -5],
                ["FRONT"],
                ["DEQUEUE"],
                ["FRONT"],
                ["DEQUEUE"]
            ]),
            make_test_case([["ENQUEUE", 100], ["DEQUEUE"], ["FRONT"]]),
            make_test_case([["ENQUEUE", i] for i in [5, 10, 15]] + [["DEQUEUE"]] * 3)
        ],
        "public": [
            make_test_case([["DEQUEUE"], ["FRONT"]]),
            make_test_case([["ENQUEUE", 100], ["DEQUEUE"], ["DEQUEUE"]]),
            make_test_case([["ENQUEUE", i] for i in range(5)] + [["FRONT"], ["DEQUEUE"]] * 5),
            make_test_case([["ENQUEUE", -1], ["ENQUEUE", 0], ["ENQUEUE", 1], ["FRONT"], ["DEQUEUE"]]),
            make_test_case([["ENQUEUE", 999], ["FRONT"], ["FRONT"], ["DEQUEUE"], ["FRONT"]])
        ],
        "hidden": []
    }

    # Edge: Empty operations
    tc["hidden"].append(make_test_case([["DEQUEUE"]] * 5))
    tc["hidden"].append(make_test_case([["FRONT"]] * 3))
    tc["hidden"].append(make_test_case([["DEQUEUE"], ["FRONT"], ["DEQUEUE"]]))
    
    # Edge: Single element
    tc["hidden"].append(make_test_case([["ENQUEUE", 42], ["FRONT"], ["DEQUEUE"], ["FRONT"]]))
    tc["hidden"].append(make_test_case([["ENQUEUE", -999], ["DEQUEUE"], ["ENQUEUE", 888], ["FRONT"]]))
    
    # Corner: Alternating operations
    ops1 = []
    for i in range(10):
        ops1.append(["ENQUEUE", i])
        ops1.append(["DEQUEUE"])
    tc["hidden"].append(make_test_case(ops1))
    
    ops2 = []
    for i in range(8):
        ops2.append(["ENQUEUE", i])
        ops2.append(["FRONT"])
    tc["hidden"].append(make_test_case(ops2))
    
    # Normal: Small sequences
    tc["hidden"].append(make_test_case([["ENQUEUE", i] for i in [1, 2, 3, 4]] + [["DEQUEUE"]] * 2 + [["FRONT"]]))
    tc["hidden"].append(make_test_case([["ENQUEUE", i*10] for i in range(6)] + [["FRONT"]] + [["DEQUEUE"]] * 6))
    tc["hidden"].append(make_test_case([["ENQUEUE", 100], ["ENQUEUE", 200], ["DEQUEUE"], ["ENQUEUE", 300], ["FRONT"]]))
    
    # Normal: Negative numbers
    tc["hidden"].append(make_test_case([["ENQUEUE", -i] for i in [10, 20, 30]] + [["DEQUEUE"]] * 3))
    tc["hidden"].append(make_test_case([["ENQUEUE", -50], ["FRONT"], ["ENQUEUE", -100], ["DEQUEUE"], ["FRONT"]]))
    
    # Normal: Mixed operations
    tc["hidden"].append(make_test_case([["ENQUEUE", 1], ["FRONT"], ["ENQUEUE", 2], ["DEQUEUE"], ["DEQUEUE"]]))
    tc["hidden"].append(make_test_case([["ENQUEUE", i] for i in [7, 8, 9]] + [["FRONT"], ["DEQUEUE"], ["FRONT"]]))
    tc["hidden"].append(make_test_case([["ENQUEUE", 50], ["DEQUEUE"], ["ENQUEUE", 60], ["ENQUEUE", 70], ["FRONT"]]))
    
    # Edge: Multiple FRONT without DEQUEUE
    tc["hidden"].append(make_test_case([["ENQUEUE", 111], ["FRONT"], ["FRONT"], ["FRONT"]]))
    tc["hidden"].append(make_test_case([["ENQUEUE", i] for i in [5, 6]] + [["FRONT"]] * 4 + [["DEQUEUE"]]))
    
    # Normal: Build and drain
    tc["hidden"].append(make_test_case([["ENQUEUE", i] for i in range(10, 20)] + [["DEQUEUE"]] * 10))
    tc["hidden"].append(make_test_case([["ENQUEUE", i*5] for i in range(8)] + [["DEQUEUE"]] * 4 + [["FRONT"]]))
    
    # Corner: Extreme values
    tc["hidden"].append(make_test_case([["ENQUEUE", 10**9], ["ENQUEUE", -10**9], ["DEQUEUE"], ["FRONT"]]))
    tc["hidden"].append(make_test_case([["ENQUEUE", 0], ["ENQUEUE", 0], ["FRONT"], ["DEQUEUE"], ["DEQUEUE"]]))
    
    # Normal: Random-like patterns
    tc["hidden"].append(make_test_case([["ENQUEUE", v] for v in [45, 12, 89, 3, 67]] + [["DEQUEUE"]] * 3 + [["FRONT"]]))
    tc["hidden"].append(make_test_case([["ENQUEUE", v] for v in [100, 50, 75, 25]] + [["FRONT"], ["DEQUEUE"]] * 2))
    tc["hidden"].append(make_test_case([["ENQUEUE", 1], ["DEQUEUE"], ["ENQUEUE", 2], ["DEQUEUE"], ["ENQUEUE", 3]]))
    
    # Edge: Empty after operations
    tc["hidden"].append(make_test_case([["ENQUEUE", 10], ["ENQUEUE", 20], ["DEQUEUE"], ["DEQUEUE"], ["FRONT"]]))
    tc["hidden"].append(make_test_case([["ENQUEUE", i] for i in [1, 2, 3]] + [["DEQUEUE"]] * 4))
    
    # Normal: Medium sequences
    tc["hidden"].append(make_test_case([["ENQUEUE", i] for i in range(15)] + [["FRONT"]] + [["DEQUEUE"]] * 10))
    tc["hidden"].append(make_test_case([["ENQUEUE", i*2] for i in range(12)] + [["DEQUEUE"]] * 6 + [["FRONT"]]))
    tc["hidden"].append(make_test_case([["ENQUEUE", v] for v in [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]] + [["DEQUEUE"]] * 5 + [["FRONT"]]))

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
