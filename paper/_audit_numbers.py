import hashlib, json, pathlib
R = pathlib.Path(r'E:\study\ADB\n100-public')
def L(rel):
    return json.loads((R / rel).read_text(encoding='utf-8'))
def sha(p):
    p = pathlib.Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'MISSING'

print('== independent lattice script sha (current) ==')
print(sha(R / 'verify/independent_lattice97_upperbound_n100.py'))

print()
print('== tail candidate 224 ==')
t = L('verify/out/n100-tail-candidate-224.json')
for k, v in t.items():
    if k in ('rows', 'boxes', 'traces'):
        print(f'  {k}: <omitted len={len(v) if hasattr(v, "__len__") else "?"}>')
    else:
        print(f'  {k}: {v}')

print()
print('== external bounds: lower/upper shape ==')
b = L('verify/out/external-disk100-bounds-67ebf1c.json')
def walk(d, prefix=''):
    if isinstance(d, dict):
        for k, v in d.items():
            if k in ('rows', 'boxes'):
                print(f'{prefix}{k}: <omitted>')
            elif isinstance(v, (dict, list)):
                if isinstance(v, list):
                    print(f'{prefix}{k}: list[{len(v)}]')
                else:
                    walk(v, prefix + k + '.')
            else:
                s = str(v)
                print(f'{prefix}{k}: {s[:160]}')
    else:
        print(f'{prefix}: {str(d)[:160]}')
walk(b.get('result', {}), 'result.')
print('top keys:', list(b.keys()))

print()
print('== margin cert ==')
m = L('verify/out/external-disk100-margin-67ebf1c.json')
walk(m.get('result', {}), 'result.')

print()
print('== quadtree replay ==')
q = L('verify/out/external-disk100-local-quadtree/replay.json')
walk(q, '')

print()
print('== denominator digit counts ==')
def digits(s):
    if '/' in s:
        n, d = s.split('/')
        return len(n), len(d), d.count('0') == len(d) - 1
    return len(s), None, None
for name, rel, key in [
    ('cand225 B36 margin', 'verify/out/n100-candidate-complete-225.json', None),
    ('budget222 B36 margin', 'verify/out/n100-candidate-budget-222.json', None),
]:
    z = L(rel)
    if 'B36plus_certificate' in z:
        s = z['B36plus_certificate']['B36_margin']
    else:
        s = z['B36_margin']
    print(name, '->', digits(s), s[:20], '...')

o = L('verify/out/n100-tail-support-obstruction-206.json')
for k in ('point_relaxation_interval', 'point_lower_excess_over_old_intercept',
          'max_intercept_allowed_by_B36_area', 'point_lower_excess_over_area_budget',
          'old_intercept', 'slope', 'penalty', 'x', 'y', 'status'):
    print('obstruction', k, '=', o[k], digits(o[k]) if isinstance(o[k], str) and '/' in o[k] else '')

print()
print('== B37plus cert keys ==')
z = L('verify/out/n100-tail-B37plus-210-a.json')
walk(z, '')
