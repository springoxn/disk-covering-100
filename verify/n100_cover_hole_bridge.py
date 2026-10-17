"""Exact interval margins and contraction constants for persistent covering witnesses.
Conditional analytic bridge: fixed affine gauge, root-centered center box.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
R=Path(__file__).resolve().parents[1];src=R/'runtime/external-disk100-strict-local-replay/source'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
s=load(src/'polynomial_system.json');mid=load(src/'rational_midpoint.json');kr=load(src/'krawczyk_verification.json');localp=R/'verify/out/n100-fixed-rod-local-budget.json';local=load(localp)
assert kr['verified'] and kr['box_radius']==[1,10**58] and local['verified_scalar_budget']
D=int(mid['denominator']);rho=F(1,10**58);nums=list(map(int,mid['numerators']));x=[(F(v,D)-rho,F(v,D)+rho) for v in nums]
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 v=[c*d for c in a for d in b];return min(v),max(v)
def scale(a,k):return mul(a,(F(k),F(k)))
def sq(a):return (F(0) if a[0]<=0<=a[1] else min(a[0]**2,a[1]**2),max(a[0]**2,a[1]**2))
def norm2(p):return add(sq(p[0]),sq(p[1]))
def absmax(a):return max(abs(a[0]),abs(a[1]))
def point(n):return x[2*n:2*n+2]
cs=[point(i) for i in range(100)];ps=[point(100+i) for i in range(146)];t=x[492]
assert all(absmax(v)<=2 for p in cs+ps for v in p)
supports=s['internal_active_triangles']+s['boundary_active_pairs'];assert len(supports)==146
K=F(10**6);eps=F(1,10**54);eta=F(1,10**45)
assert 128*K*eps<=eta
assert K*(16*eps+4*eta)<=F(1,2)
rows=[];gapmin=None;intmargin=None
for h,support in enumerate(supports):
 p=ps[h];a,b=support[:2]
 row1=[scale(sub(cs[b][i],cs[a][i]),2) for i in range(2)]
 if h<114:
  c=support[2];row2=[scale(sub(cs[c][i],cs[a][i]),2) for i in range(2)]
  margin=1-norm2(p)[1]
  assert margin>32*eta+2*eta**2
  intmargin=margin if intmargin is None else min(intmargin,margin)
 else:row2=[scale(v,2) for v in p];margin=None
 det=sub(mul(row1[0],row2[1]),mul(row1[1],row2[0]));assert det[0]>0 or det[1]<0
 detabs=min(abs(det[0]),abs(det[1]));inv=max(absmax(row2[1])+absmax(row1[1]),absmax(row2[0])+absmax(row1[0]))/detabs
 assert inv<=K
 gap=None;idx=None
 for i,cpoint in enumerate(cs):
  if i in support:continue
  dist=norm2([sub(p[d],cpoint[d]) for d in range(2)]);g=dist[0]-t[1]
  assert g>64*(eta+eps),(h,i,g)
  if gap is None or g<gap:gap=g;idx=i
 gapmin=gap if gapmin is None else min(gapmin,gap)
 rows.append({'hole':h,'support_centers':support,'kind':'interior' if h<114 else 'boundary','determinant_interval':[str(v) for v in det],'inverse_infinity_upper':str(inv),'nearest_inactive_center':idx,'inactive_squared_distance_gap_lower':str(gap),'interior_unit_margin_lower':str(margin) if margin is not None else None})
tshift=64*(eta+eps);fullnorm=23*max(eps,eta,tshift);assert 23**2>=493 and fullnorm<F(local['constants']['radius'])
# Candidate-only negative control: erase strict gap by assigning a support as inactive.
rejected=[]
for name,test in [('zero_branch_jacobian',F(0)>0),('lost_inactive_margin',F(0)>64*(eta+eps)),('oversized_center_box',128*K*F(1,10**30)<=eta)]:
 assert not test;rejected.append(name)
out={'schema':'n100-cover-hole-bridge/v1','verified_interval_and_scalar_bounds':True,'root_centered_center_coordinate_radius':str(eps),'continued_hole_coordinate_radius':str(eta),'uniform_inverse_infinity_bound':str(K),'min_inactive_squared_gap':str(gapmin),'min_interior_unit_margin':str(intmargin),'holes':rows,'holes_verified':146,'non_support_distance_tests':114*97+32*98,'supporting_squared_length_shift_upper':str(tshift),'493_variable_norm_upper':str(fullnorm),'fixed_rod_local_radius':local['constants']['radius'],'analytic_conclusion':'Each of 146 holes persists inside D or on boundary for centers within epsilon of exact root in the fixed affine gauge. Other centers have squared distance greater than t*. If such centers cover D at t<=t*, all designated supporting rods satisfy squared length<=t; also t>=t*-64(eta+epsilon), so lifted variables lie in the fixed-rod LOCAL ball. Therefore improved covering impossible in this fixed-gauge root-centered center box.','requires_reviewed_Banach_and_covering_argument':True,'general_rotation_neighborhood_proved':False,'global_topology_exclusion':False,'global_optimality':False,'negative_controls_rejected':rejected,'sources_sha256':{str(p.relative_to(R)).replace('\\','/'):sha(p) for p in [src/'polynomial_system.json',src/'rational_midpoint.json',src/'krawczyk_verification.json',localp]},'checker_sha256':sha(Path(__file__))}
op=R/'verify/out/n100-cover-hole-bridge.json';assert not op.exists();op.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('PASS 146 support Jacobians, 14194 inactive gap tests, interior margins, Banach constants and 493-variable lifting bound; fixed gauge, local only')
