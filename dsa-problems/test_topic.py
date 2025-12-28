import subprocess
import sys
import yaml
import re
from pathlib import Path

TIMEOUT = 10

def extract_code(path):
    content = open(path, encoding='utf-8').read()
    for m in re.findall(r'```python\s*(.*?)```', content, re.DOTALL):
        if 'def main' in m or '__name__' in m:
            return m
    return None

def run(code, inp):
    try:
        r = subprocess.run([sys.executable, '-c', code], input=inp, capture_output=True, text=True, timeout=TIMEOUT)
        return r.stdout.strip(), None
    except subprocess.TimeoutExpired:
        return None, 'TIMEOUT'
    except Exception as e:
        return None, str(e)

def test_problem(ed_path, tc_path):
    code = extract_code(ed_path)
    if not code:
        return 0, 0, 'NO_CODE'
    tests = yaml.safe_load(open(tc_path))
    total = passed = 0
    for section in ['samples', 'public', 'hidden']:
        for tc in tests.get(section, []):
            total += 1
            inp = tc['input'].strip()
            exp = str(tc['output']).strip()
            actual, err = run(code, inp)
            if not err and actual == exp:
                passed += 1
    return passed, total, None

topic = sys.argv[1] if len(sys.argv) > 1 else 'TreesDP'
tc_dir = Path(topic) / 'testcases'
ed_dir = Path(topic) / 'editorials'

if not tc_dir.exists():
    print(f'Directory {tc_dir} does not exist')
else:
    results = []
    for tc_file in sorted(tc_dir.glob('*.yaml')):
        prob_id = tc_file.stem
        ed_file = ed_dir / f'{prob_id}.md'
        if not ed_file.exists():
            results.append((prob_id, 0, 0, 'NO_EDITORIAL'))
        else:
            passed, total, err = test_problem(ed_file, tc_file)
            results.append((prob_id, passed, total, err))

    print(f'{topic} Test Results:')
    print('=' * 60)
    total_passed = total_tests = 0
    for prob_id, passed, total, err in results:
        total_passed += passed
        total_tests += total
        status = f'{passed}/{total}' if not err else err
        pct = f'{100*passed/total:.0f}%' if total > 0 else 'N/A'
        marker = '' if passed == total and not err else ' <-- FAILING'
        print(f'  {prob_id}: {status} ({pct}){marker}')
    print('=' * 60)
    pct = 100*total_passed/total_tests if total_tests > 0 else 0
    print(f'Total: {total_passed}/{total_tests} ({pct:.1f}%)')
