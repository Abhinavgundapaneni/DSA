import random
import yaml

def solve(k, operations):
    buffer = [0] * k
    head = 0
    tail = 0
    size = 0
    results = []
    
    for op_row in operations:
        op = op_row[0]
        if op == "ENQ":
            x = op_row[1]
            if size < k:
                buffer[tail] = x
                tail = (tail + 1) % k
                size += 1
                results.append("true")
            else:
                results.append("false")
        elif op == "ENQ_OVR":
            x = op_row[1]
            if size < k:
                buffer[tail] = x
                tail = (tail + 1) % k
                size += 1
                results.append("NONE")
            else:
                # Save the value that will be overwritten
                overwritten_val = buffer[head]
                buffer[tail] = x
                tail = (tail + 1) % k
                head = (head + 1) % k
                results.append(str(overwritten_val))
        elif op == "DEQ":
            if size > 0:
                val = buffer[head]
                head = (head + 1) % k
                size -= 1
                results.append(str(val))
            else:
                results.append("EMPTY")
        elif op == "FRONT":
            if size > 0:
                results.append(str(buffer[head]))
            else:
                results.append("EMPTY")
        elif op == "REAR":
            if size > 0:
                results.append(str(buffer[(tail - 1 + k) % k]))
            else:
                results.append("EMPTY")
        elif op == "ISEMPTY":
            results.append("true" if size == 0 else "false")
        elif op == "ISFULL":
            results.append("true" if size == k else "false")
    return results

def make_test_case(k, operations):
    results = solve(k, operations)
    input_str = f"{k}\n{len(operations)}\n" + "\n".join(" ".join(map(str, op)) for op in operations)
    output_str = "\n".join(results)
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case(2, [
                ["ENQ", 5],
                ["ENQ", 6],
                ["ENQ", 7],
                ["ENQ_OVR", 8],
                ["FRONT"],
                ["REAR"]
            ]),
            make_test_case(1, [["ENQ", 1], ["ENQ", 2], ["ENQ_OVR", 3], ["DEQ"]]),
            make_test_case(3, [["ISEMPTY"], ["ISFULL"], ["ENQ", 10], ["ISEMPTY"], ["ENQ", 20], ["ENQ", 30], ["ISFULL"]])
        ],
        "public": [
            make_test_case(1, [["ENQ_OVR", i] for i in range(5)] + [["FRONT"]]),  # Capacity 1 overwrite
            make_test_case(5, [["ENQ", i] for i in range(5)] + [["ISFULL"], ["ENQ_OVR", 100], ["FRONT"]]),  # Full buffer overwrite
            make_test_case(4, [["ENQ", 1], ["ENQ", 2], ["DEQ"], ["ENQ_OVR", 3], ["FRONT"], ["REAR"]]),  # Partial then overwrite
            make_test_case(2, [["ISEMPTY"], ["ENQ", 5], ["ISEMPTY"], ["ISFULL"]]),  # Empty/full checks
            make_test_case(3, [["ENQ", 10], ["ENQ", 20], ["ENQ", 30], ["DEQ"], ["FRONT"], ["REAR"]])  # Normal ops
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case(1, [["ENQ_OVR", 1], ["FRONT"], ["REAR"], ["ISEMPTY"], ["ISFULL"]]))  # Single capacity all ops
    tc["hidden"].append(make_test_case(5, [["ISEMPTY"], ["ISFULL"]]))  # Empty buffer checks
    tc["hidden"].append(make_test_case(1, [["ENQ_OVR", 1]]))  # Single overwrite
    tc["hidden"].append(make_test_case(2, [["ENQ", 1], ["ENQ", 2], ["ENQ_OVR", 3], ["ENQ_OVR", 4], ["FRONT"], ["REAR"]]))  # Multiple overwrites
    tc["hidden"].append(make_test_case(3, [["ENQ", 1], ["ENQ", 2], ["FRONT"], ["REAR"], ["ISEMPTY"], ["ISFULL"]]))  # Partial buffer
    tc["hidden"].append(make_test_case(4, [["ENQ", i] for i in range(4)] + [["DEQ"], ["ENQ_OVR", 100]]))  # Full then dequeue then overwrite
    tc["hidden"].append(make_test_case(5, [["ENQ_OVR", 1]]))  # Overwrite on empty
    tc["hidden"].append(make_test_case(3, [["ENQ", 1], ["ENQ", 2], ["ENQ", 3], ["FRONT"], ["REAR"]]))  # Exactly full
    
    # Corner cases (8-10)
    tc["hidden"].append(make_test_case(1, [["ENQ_OVR", 10**9], ["ENQ_OVR", -10**9], ["FRONT"]]))  # Extreme values capacity 1
    tc["hidden"].append(make_test_case(3, [["ENQ", -10**9], ["ENQ", 0], ["ENQ", 10**9], ["ENQ_OVR", 999], ["FRONT"], ["REAR"]]))  # Extremes
    tc["hidden"].append(make_test_case(2, [["ENQ", 0], ["ENQ", 0], ["ENQ_OVR", 0], ["FRONT"], ["REAR"]]))  # All zeros
    tc["hidden"].append(make_test_case(4, [["ENQ", 1], ["DEQ"], ["ENQ", 2], ["DEQ"], ["ENQ", 3], ["FRONT"]]))  # Alternating enq/deq
    tc["hidden"].append(make_test_case(5, [["ENQ", i] for i in range(5)] + [["ENQ_OVR", i] for i in range(5)] + [["FRONT"], ["REAR"]]))  # Fill then overwrite all
    tc["hidden"].append(make_test_case(2, [["ENQ", -1], ["ENQ", -2], ["ENQ_OVR", -3], ["DEQ"], ["FRONT"]]))  # Negative values
    tc["hidden"].append(make_test_case(3, [["ENQ", 1], ["ENQ", 2], ["ENQ", 3], ["DEQ"], ["DEQ"], ["ENQ_OVR", 4]]))  # Wrap around
    tc["hidden"].append(make_test_case(1, [["ENQ_OVR", i] for i in [1, 2, 3, 4, 5]] + [["FRONT"]]))  # Repeated overwrites capacity 1

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case(5, [["ENQ", i] for i in range(3)] + [["FRONT"], ["REAR"], ["ISEMPTY"]]))  # Small buffer
    tc["hidden"].append(make_test_case(8, [["ENQ", i] for i in range(5)] + [["DEQ"], ["DEQ"], ["ENQ_OVR", 100], ["FRONT"]]))  # Medium buffer
    tc["hidden"].append(make_test_case(10, [["ENQ", i] for i in range(10)] + [["ISFULL"], ["ENQ_OVR", 999], ["DEQ"], ["FRONT"]]))  # Fill medium
    tc["hidden"].append(make_test_case(6, [["ENQ", 10], ["ENQ", 20], ["ENQ", 30], ["DEQ"], ["ENQ", 40], ["FRONT"], ["REAR"]]))  # Mixed ops
    tc["hidden"].append(make_test_case(7, [["ENQ", i*10] for i in range(7)] + [["ISFULL"], ["FRONT"], ["REAR"]]))  # Fill exact
    tc["hidden"].append(make_test_case(4, [["ENQ", 5], ["ENQ", 10], ["DEQ"], ["ENQ", 15], ["ENQ", 20], ["FRONT"]]))  # Wrap pattern
    tc["hidden"].append(make_test_case(12, [["ENQ", i] for i in range(8)] + [["DEQ"]] * 3 + [["ENQ_OVR", 100], ["FRONT"]]))  # Larger buffer
    tc["hidden"].append(make_test_case(15, [["ENQ", i] for i in range(10)] + [["ISEMPTY"], ["ISFULL"], ["REAR"]]))  # Partial large
    tc["hidden"].append(make_test_case(5, [["ENQ", 1], ["ENQ", 2], ["ENQ", 3], ["ENQ", 4], ["ENQ", 5], ["ENQ_OVR", 6], ["DEQ"], ["FRONT"], ["REAR"]]))  # Full cycle
    tc["hidden"].append(make_test_case(8, [["ENQ", i*5] for i in range(6)] + [["DEQ"], ["DEQ"], ["ENQ_OVR", 999], ["ISEMPTY"], ["ISFULL"]]))  # Complex mix
    tc["hidden"].append(make_test_case(20, [["ENQ", i] for i in range(15)] + [["FRONT"], ["REAR"]]))  # Large partial
    tc["hidden"].append(make_test_case(10, [["ENQ", i] for i in range(10)] + [["DEQ"]] * 5 + [["ENQ_OVR", 100], ["FRONT"], ["REAR"]]))  # Half empty then overwrite

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
