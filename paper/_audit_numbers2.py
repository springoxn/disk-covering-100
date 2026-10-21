import json, pathlib
from fractions import Fraction as F
R = pathlib.Path(r'E:\study\ADB\n100-public')
def L(rel):
    return json.loads((R / rel).read_text(encoding='utf-8'))

out = []
def p(*a):
    out.append(' '.join(str(x) for x in a))

b = L('verify/out/external-disk100-bounds-67ebf1c.json')
res = b['result']
p('--- external bounds upper block ---')
for k, v in res['upper'].items():
    if isinstance(v, dict):
        p(' upper.%s:' % k, json.dumps({kk: vv for kk, vv in v.items() if kk != 'counts'})[:600])
        if 'counts' in v:
            p('   counts:', json.dumps(v['counts']))
    else:
        p(' upper.%s:' % k, str(v)[:300])
p(' lower branch keys:', list(res['lower']['result'].keys()))
for k in ('B31', 'B32', 'B33', 'B34', 'B35', 'B36plus'):
    if k in res['lower']['result']:
        r = res['lower']['result'][k]
        p(' ', k, 'status=', r.get('result', {}).get('status'), 'radius=', r.get('result', {}).get('radius'),
          'margin=', str(r.get('result', {}).get('minimum_area_margin'))[:80])
p(' lower result other keys:', [k for k in res['lower']['result'].keys() if not k.startswith('B')])

p('')
p('--- margin cert ---')
m = L('verify/out/external-disk100-margin-67ebf1c.json')
p(' keys:', list(m.keys()))
p(' result:', json.dumps(m['result'])[:1500])

p('')
p('--- quadtree replay ---')
ADB = pathlib.Path(r'E:\study\ADB')
for cand in ('verify/out/external-disk100-local-quadtree/replay.json',):
    p(' path present under n100-public:', (R / cand).is_file(),
      '| under ADB root:', (ADB / cand).is_file())
    if (ADB / cand).is_file():
        q = json.loads((ADB / cand).read_text(encoding='utf-8'))
        p(' (ADB root copy) keys:', list(q.keys()))
        p(' radius:', q.get('radius'), 'all_passed:', q.get('all_passed'))
        for k in ('generator_result', 'independent', 'not_claimed', 'scope'):
            if k in q:
                p(' ', k, ':', json.dumps(q[k])[:700])

p('')
p('--- denominator digit counts ---')
def frac(s):
    n, d = s.split('/')
    return dict(num_digits=len(n), den_digits=len(d), den_is_10pow=set(d) == {'1', '0'} and d[0] == '1',
                den=('10^%d' % (len(d) - 1)) if set(d) == {'1', '0'} and d[0] == '1' else d[:24] + '...')
t = L('verify/out/n100-tail-candidate-224.json')
p(' 224 B36 margin:', frac(t['minimum_area_margin_at_B36']))
p(' 224 per-cell  :', frac(t['additional_margin_per_boundary_cell']))
c = L('verify/out/n100-candidate-complete-225.json')['B36plus_certificate']
p(' 225 B36 margin:', frac(c['B36_margin']), '| equals 224?', c['B36_margin'] == t['minimum_area_margin_at_B36'])
p(' 225 per-cell  :', frac(c['per_boundary_gain']))
z = L('verify/out/n100-candidate-budget-222.json')
p(' 222 B36 margin:', frac(z['B36_margin']))
p(' 222 per-cell  :', frac(z['per_boundary_gain']))

p('')
p('--- obstruction ---')
o = L('verify/out/n100-tail-support-obstruction-206.json')
for k in ('status', 'radius', 'x', 'y', 'slope', 'penalty', 'old_intercept', 'point_relaxation_interval',
          'point_lower_excess_over_old_intercept', 'max_intercept_allowed_by_B36_area',
          'point_lower_excess_over_area_budget', 'full_B36plus_closed', 'global_bound_improved'):
    v = o[k]
    extra = frac(v) if isinstance(v, str) and '/' in v else ''
    p(' ', k, '=', v, extra)

p('')
p('--- B37plus cert ---')
z = L('verify/out/n100-tail-B37plus-210-a.json')
p(' keys:', list(z.keys()))
for k, v in z.items():
    if k in ('rows', 'boxes', 'traces'):
        p('  %s: <omitted>' % k)
    elif isinstance(v, (dict, list)):
        p('  %s:' % k, json.dumps(v)[:400])
    else:
        p('  %s: %s' % (k, str(v)[:200]))

p('')
p('--- candidate budget formula re-evaluation ---')
PL = F(31415926535897932384626433832795028841971, 10 ** 40)   # pi lower, plenty
A = F(129903810568, 10 ** 11)
K = F(973, 3125)
for (Rn, Rd, Ln, Ld, label) in ((113237, 10 ** 6, 75097, 10 ** 7, 'stage221/222'),
                                (22647, 200000, 939, 125000, 'candidate224')):
    Rr = F(Rn, Rd); LL = F(Ln, Ld); mu = F(92531, 10 ** 7)
    margin = (1 - mu) * PL - ((198 - 36) * A + 36 * K) * Rr * Rr - 36 * LL
    gain = (A - K) * Rr * Rr - LL
    p(' ', label, 'margin~', float(margin), 'gain~', float(gain))
p(' certificate 222 margin float:', float(F(*map(int, L('verify/out/n100-candidate-budget-222.json')['B36_margin'].split('/')))))
p(' certificate 222 gain   float:', float(F(*map(int, L('verify/out/n100-candidate-budget-222.json')['per_boundary_gain'].split('/')))))

p('')
p('--- normalised centre norm squared bounds quoted by stage143 vs external ---')
p(' stage143 doc text value: 98717894445399/10^14 =', float(F(98717894445399, 10 ** 14)))
p(' external package value : 9871789671/10^10    =', float(F(9871789671, 10 ** 10)))
p(' stage149 doc text value: 616985439/625000000 =', float(F(616985439, 625000000)))
p(' 1 - (22647/200000)^2 =', float(1 - F(22647, 200000) ** 2))
p(' 1 - (2831/25000)^2   =', float(1 - F(2831, 25000) ** 2))

pathlib.Path('_audit_numbers_out.txt').write_text('\n'.join(out), encoding='utf-8')
print('\n'.join(out))
