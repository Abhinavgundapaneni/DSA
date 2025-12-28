from collections import deque
import random
import yaml

def solve(s):
    counts = {}
    queue = deque()
    results = []
    
    for char in s:
        counts[char] = counts.get(char, 0) + 1
        queue.append(char)
        
        while queue and counts[queue[0]] > 1:
            queue.popleft()
            
        if queue:
            results.append(queue[0])
        else:
            results.append("#")
    return results

def make_test_case(s):
    res = solve(s)
    input_str = f"{s}"
    output_str = " ".join(res)
    return {"input": input_str, "output": output_str}

def generate_yaml():
    tc = {
        "samples": [
            make_test_case("abacb"),
            make_test_case("a"),
            make_test_case("aaaaa")
        ],
        "public": [
            make_test_case("abcdef"),  # All different
            make_test_case("aabbcc"),  # Pairs
            make_test_case("abc"),  # Short unique
            make_test_case("abba"),  # Palindrome
            make_test_case("z" * 10)  # Repeated char
        ],
        "hidden": []
    }

    # Edge cases (8-10)
    tc["hidden"].append(make_test_case("a"))  # Single char
    tc["hidden"].append(make_test_case("aa"))  # Two same
    tc["hidden"].append(make_test_case("ab"))  # Two different
    tc["hidden"].append(make_test_case("aaa"))  # Three same
    tc["hidden"].append(make_test_case("abc"))  # Three different
    tc["hidden"].append(make_test_case("z" * 50))  # All same medium
    tc["hidden"].append(make_test_case("abcdefghij"))  # Ten unique
    tc["hidden"].append(make_test_case("aabbccddee"))  # Pairs medium

    # Corner cases (8-10)
    tc["hidden"].append(make_test_case("qwertyuiopasdfghjklzxcvbnm"))  # All 26 letters
    tc["hidden"].append(make_test_case("zzzzz"))  # Five same
    tc["hidden"].append(make_test_case("abcabcabc"))  # Repeating pattern
    tc["hidden"].append(make_test_case("a" * 20 + "b"))  # Many same then different
    tc["hidden"].append(make_test_case("abcdefghijklmnop"))  # Long unique
    tc["hidden"].append(make_test_case("aabbccddee" * 5))  # Pattern repeat
    tc["hidden"].append(make_test_case("x" * 30))  # Thirty same
    tc["hidden"].append(make_test_case("abcdefghijklmnopqrstuvwxyz"))  # Full alphabet

    # Normal cases (10-14)
    tc["hidden"].append(make_test_case("abcabc"))  # Small pattern
    tc["hidden"].append(make_test_case("aabbccddeeff"))  # Medium pairs
    letters = "abcdefghijklmnopqrstuvwxyz"
    tc["hidden"].append(make_test_case("".join(random.choice(letters[:5]) for _ in range(20))))  # Random small set
    tc["hidden"].append(make_test_case("abcdefgh" * 3))  # Medium repeat
    tc["hidden"].append(make_test_case("".join(random.choice(letters[:10]) for _ in range(30))))  # Random medium
    tc["hidden"].append(make_test_case("aabbccddee" * 8))  # Longer pattern
    tc["hidden"].append(make_test_case("".join(random.choice(letters) for _ in range(50))))  # Random all letters
    tc["hidden"].append(make_test_case("abcdefghijklm" * 4))  # Large repeat
    tc["hidden"].append(make_test_case("".join(random.choice(letters[:15]) for _ in range(40))))  # Random mid-range
    tc["hidden"].append(make_test_case("abc" * 20))  # Repeating triplet
    tc["hidden"].append(make_test_case("".join(random.choice(letters[:8]) for _ in range(60))))  # Random longer
    tc["hidden"].append(make_test_case("abcdefghijklmnopqrstuvwxyz" * 3))  # Alphabet triple
    tc["hidden"].append(make_test_case("".join(random.choice(letters) for _ in range(80))))  # Random large
    tc["hidden"].append(make_test_case("abcd" * 15))  # Quad pattern

    print(yaml.dump(tc, sort_keys=False, default_flow_style=False))

if __name__ == "__main__":
    generate_yaml()
