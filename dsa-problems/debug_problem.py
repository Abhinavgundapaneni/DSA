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
        return r.stdout.strip(), r.stderr.strip() if r.returncode != 0 else None
    except subprocess.TimeoutExpired:
        return None, 'TIMEOUT'
    except Exception as e:
        return None, str(e)

prob_id = sys.argv[1] if len(sys.argv) > 1 else 'TDP-001-lca-binary-lifting'
topic = sys.argv[2] if len(sys.argv) > 2 else 'TreesDP'

ed_path = Path(topic) / 'editorials' / f'{prob_id}.md'
tc_path = Path(topic) / 'testcases' / f'{prob_id}.yaml'

code = extract_code(ed_path)
if not code:
    print('NO_CODE')
    sys.exit(1)

tests = yaml.safe_load(open(tc_path))

i = 0
for section in ['samples', 'public', 'hidden']:
    for tc in tests.get(section, []):
        i += 1
        inp = tc['input'].strip()
        exp = str(tc['output']).strip()
        actual, err = run(code, inp)
        if err:
            print(f'{i}: {err}')
            if 'Traceback' in str(err) or len(str(err)) > 50:
                print(f'    Input: {inp[:100]}...')
        elif actual != exp:
            print(f'{i}: WRONG got="{actual}" exp="{exp}"')
