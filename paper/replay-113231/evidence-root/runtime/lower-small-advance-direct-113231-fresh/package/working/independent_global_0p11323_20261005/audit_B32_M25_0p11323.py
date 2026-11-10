#!/usr/bin/env python3
"""Independent B32 M25 receipt; high-M and other B remain separate."""
from pathlib import Path
from fractions import Fraction as F
import itertools,json,subprocess,sys,os,hashlib
ROOT=Path(__file__).resolve().parents[1]
STAGING=ROOT.parent/'lower_staging';R=F(113231,1000000)
def verify():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 data=json.loads((STAGING/'B32_M25_direct_interface_0p11323_proposal.json').read_text())
 cycles=set()
 for bits in itertools.product((0,1),repeat=5):
  if sum(bits)<=2:
   cycles.add((sum(bits),tuple(sum(bits[i]+bits[(i+1)%5]==h for i in range(5)) for h in range(3))))
 assert {(s['high_neighbors'],tuple(s['counts'])) for s in data['stars']}==cycles and len(cycles)==4
 assert data['epsilon']==[1,2] and data['perimeter_penalty']==[13,10]
 D=[F(d,data['denominator']) for d in data['outside_allowances']]
 J=max((5-2*j)*D[0]+j*D[1] for j in range(3))
 charge=F(119,2000)*(4*F(187,2000)-F(3467,10000))/(2*R*R)
 expected=[]
 for e,h7,h8 in [(0,2,0),(0,0,1),(1,1,0),(2,0,0)]:
  degrees=[7]*h7+[8]*h8
  for ps in itertools.product(range(4),repeat=len(degrees)):
   for i,k in enumerate((0,1,2,2)):
    if k<=len(degrees):expected.append((e,tuple(degrees),ps,i))
 assert len(expected)==len(set(expected))==81
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
 raw=subprocess.check_output([sys.executable,'-B','-S',str(STAGING/'verify_B32_M25_direct_interface_0p11323.py')],cwd=ROOT,env=env,text=True)
 z=json.loads(raw)
 assert z['status']=='PASS' and z['radius']==str(R) and (z['B'],z['m'],z['M'])==(32,100,25)
 assert F(z['required_center_norm_squared_upper'])==1-R*R
 assert z['integer_profile_cases']==81
 assert (z['ordinary_face_supports'],z['outside_face_supports'],z['central_face_supports'])==(9,18,8)
 received=[(v['ears'],tuple(v['high_degrees']),tuple(v['high_marked']),v['star_pattern']) for v in z['rows']]
 assert set(received)==set(expected) and len(received)==len(set(received))==81
 assert F(z['minimum_area_margin'])==min(F(v['area_margin_lower']) for v in z['rows'])>F(4384,10**7)
 assert F(z['q3_hinge_charge'])==charge and F(z['outside_total_allowance'])==J
 assert z['same_radius_boundary_scalar']['global_nonnegative_deficit']['variance_coefficient']=='0'
 assert z['same_radius_boundary_scalar']['local_positive_hinge']['variance_coefficient']=='0'
 assert z==json.loads((STAGING/'B32_M25_direct_interface_0p11323_result.json').read_text())
 paths=[STAGING/p for p in ['verify_B32_M25_direct_interface_0p11323.py','B32_M25_direct_interface_0p11323_proposal.json','refresh_B32_low_core_0p11323.py','B32_M25_DIRECT_INTERFACE_0p11323_PROOF.md']]
 paths += [ROOT/p for p in ['polygon_star_perimeter_support.py','POLYGON_STAR_AREA_PERIMETER.md','exact_signed_sine_full_face_support.py','exact_range_one_face_support.py','verify_tight_hinges_B32_0p11323.py','MARKED_APEX_HINGE_CHARGE.md','FACE_LABEL_INTERFACE_CHARGES.md','EXACT_NORMALIZED_LENS_PENALTY.md','verify_exact_lens_boundary_0p11322.py','verify_exact_lens_hinge_deficit_tight.py']]
 return dict(status='PASS',radius=str(R),scope='Independent B32 M<=25/M25 audit only',minimum_area_margin=z['minimum_area_margin'],fresh_output_equal_to_author_result=True,independently_rebuilt_integer_cases=81,source_sha256={str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},full_branch_result=z)
if __name__=='__main__':print(json.dumps(verify(),indent=2))
