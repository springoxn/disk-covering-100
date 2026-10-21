import json, pathlib
R = pathlib.Path(r'E:\study\ADB\n100-public')
b = json.loads((R / 'verify/out/external-disk100-bounds-67ebf1c.json').read_text(encoding='utf-8'))
res = b['result']
lo = res['lower']['result']
print('complete_surviving_boundary_counts:', lo.get('complete_surviving_boundary_counts'))
print('common_count_bridge:', json.dumps(lo.get('common_count_bridge'))[:900])
print('required_center_norm_squared_upper:', lo.get('required_center_norm_squared_upper'))
print('B33 keys:', list(lo['B33'].keys()))
print('B33 result keys:', list(lo['B33'].get('result', {}).keys()))
print('B33 margin:', lo['B33'].get('result', {}).get('minimum_area_margin') or lo['B33'].get('result', {}).get('minimum_reported_positive_margin'))
print('B36plus keys:', list(lo['B36plus'].keys()))
print('B36plus result keys:', list(lo['B36plus'].get('result', {}).keys()))
m = json.loads((R / 'verify/out/external-disk100-margin-67ebf1c.json').read_text(encoding='utf-8'))['result']
s = m['actual_covering_squared_bound']
n, d = s.split('/')
print('covering_squared_bound num_digits', len(n), 'den_digits', len(d), 'den_is_10pow', set(d) == {'1', '0'})
from fractions import Fraction as F
print('covering_squared_bound float:', float(F(int(n), int(d))))
print('U^2 =', float(F(1154469548855829, 10**16)**2))
print('V^2 =', float(F(115446954885583, 10**15)**2))
print('strict_radius_margin:', m['strict_radius_margin'], 'local', m['local_cover_radius_bound'], 'ref', m['reference_radius_bound'])
print('local float:', float(F(1154469548855829, 10**16)), 'ref float:', float(F(115446954885583, 10**15)))
print('ref - local =', F(115446954885583, 10**15) - F(1154469548855829, 10**16))
