import io, json, pathlib, re
ADB = pathlib.Path(r'E:\study\ADB')
NP = ADB / 'n100-public'


def load(rel, root=ADB):
    p = root / rel
    return json.loads(p.read_text(encoding='utf-8')) if p.is_file() else None


print('== 1. lambda ceiling values ==')
doc = (NP / 'docs/notes-lowerbound-n100.md')
if doc.is_file():
    t = doc.read_text(encoding='utf-8')
    for m in re.finditer(r'(n\s*=\s*\d+)[^\n]{0,60}?(0\.\d{3,4})', t):
        print('   ', m.group(0).strip()[:90])
    i = t.find('lambda')
    print('   context:', t[max(0, i - 200):i + 400].replace('\n', ' ')[:600] if i > 0 else 'not found')

print()
print('== 2. long-chord bundle ==')
b = load('verify/out/n100-longchord-bundle-frozen.json')
if b:
    def walk(d, pre=''):
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, (dict, list)):
                    if isinstance(v, list):
                        print(f'   {pre}{k}: list[{len(v)}]')
                    else:
                        walk(v, pre + k + '.')
                else:
                    s = str(v)
                    if any(x in k.lower() for x in ('status', 'accepted', 'all_passed', 'worst', 'count',
                                                    'margin', 'radius', 'universal', 'exit', 'rows',
                                                    'machine', 'premise', 'gap')):
                        print(f'   {pre}{k}: {s[:120]}')
    walk(b)
else:
    print('   not found')

print()
print('== 3. strengthened lower bound ==')
s = load('verify/out/strengthened_lowerbound_n100.json')
if s:
    def walk(d, pre=''):
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, (dict, list)):
                    if isinstance(v, list):
                        print(f'   {pre}{k}: list[{len(v)}]')
                    else:
                        walk(v, pre + k + '.')
                else:
                    if any(x in k.lower() for x in ('status', 'accepted', 'passed', 'margin',
                                                    'bound', 'interval', 'machine', 'certified')):
                        print(f'   {pre}{k}: {str(v)[:130]}')
    walk(s)
else:
    print('   not found')

print()
print('== 4. sharp envelope ==')
a = load('verify/out/n100-algebraic-bounds-bundle.json')
if a:
    print('   keys:', list(a.keys())[:25])
    print('   all_passed:', a.get('all_passed'), 'exit codes:', a.get('actual_exit_codes'))
    print('   global_optimality_proved:', a.get('global_optimality_proved'),
          'minpoly_obtained:', a.get('optimal_radius_minpoly_obtained'))
for rel in ('verify/out/sharp_envelope_arithmetic_n100.json',
            'verify/out/independent_sharp_envelope_n100.json'):
    z = load(rel)
    print('   ', rel, '->', 'found' if z else 'MISSING')
    if z:
        for k, v in z.items():
            if isinstance(v, dict) and 'arithmetic' in k:
                for kk, vv in v.items():
                    if 'margin' in kk.lower() or 'bound' in kk.lower() or 'T' == kk:
                        print('       ', kk, '=', str(vv)[:130])

print()
print('== 5. branch certificates: exact margins ==')
for rel in ('verify/out/n100-B32-complete-149.json', 'verify/out/n100-B33-complete-167-v2.json',
            'verify/out/n100-B34-complete-180.json', 'verify/out/n100-B35-complete-203.json',
            'verify/out/n100-B31-at-11324.json'):
    z = load(rel)
    if not z:
        print('   ', rel, 'MISSING')
        continue
    keys = [k for k in z.keys() if 'margin' in k.lower()]
    print('   ', rel.split('/')[-1], 'radius=', z.get('radius'), 'status=', z.get('status'),
          {k: str(z[k])[:60] for k in keys[:4]})
