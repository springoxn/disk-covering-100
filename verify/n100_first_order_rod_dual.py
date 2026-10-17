"""Sparse exact polynomial verification of the root's first-order rod dual certificate.
Not a global lower bound and not quantitative nonlinear isolation.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,hashlib,copy
R=Path(__file__).resolve().parents[1];SROOT=R/'runtime/external-disk100-strict-local-replay/source'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sys=load(SROOT/'polynomial_system.json');mid=load(SROOT/'rational_midpoint.json');kr=load(SROOT/'krawczyk_verification.json');bind=load(SROOT.parent/'SOURCE_BINDING.json')
for f,h in bind['files'].items():assert sha(SROOT/f)==h
assert kr['verified'] and kr['box_radius']==[1,10**58]
b=int(sys['n_base']);nc=int(sys['n_constraints']);t=int(sys['t_index']);nvar=len(sys['polynomials']);D=int(mid['denominator']);nums=list(map(int,mid['numerators']));cm=sys['constraint_metadata']
assert b==493 and nc==439 and nvar==932 and t==492
kind=[x['kind'] for x in cm];rods=[j for j in range(nc) if kind[j]=='distance'];units=[j for j in range(nc) if kind[j]=='unit'];gauges=[j for j in range(nc) if kind[j]=='gauge'];assert len(rods)==406 and len(units)==32 and len(gauges)==1
constraints=sys['polynomials'][:nc]
def norm(poly):
 d=defaultdict(F)
 for c,vs in poly:
  a=F(*c) if isinstance(c,list) else F(c);d[tuple(sorted(vs))]+=a
 return {k:v for k,v in d.items() if v}
def verify(polys):
 # Coefficients of arbitrary formal velocities in dL: exact derivative of all f_j.
 for coordinate in range(b):
  terms=[]
  if coordinate==t:terms.append([1,[]])
  for j,poly in enumerate(constraints):
   for c,vs in poly:
    for i,k in enumerate(vs):
     if k==coordinate:terms.append([c,[b+j]+vs[:i]+vs[i+1:]])
  assert norm(terms)==norm(polys[nc+coordinate]),('stationarity identity',coordinate)
 # ∂L/∂t = 1-sum distance alpha; establish normalization independently.
 target=[[1,[]]]+[[-1,[b+j]] for j in rods]
 assert norm(polys[nc+t])==norm(target)
verify(sys['polynomials'])
alpha_intervals=[(F(nums[b+j]-100,D),F(nums[b+j]+100,D)) for j in rods]
assert min(a for a,z in alpha_intervals)>0
# Gauge fixing is harmless for first-order rods: subtract an infinitesimal rotation.
gauge=cm[gauges[0]];gc=int(gauge['center']);assert gauge['coordinate']=='y'
cx=(F(nums[2*gc]-100,D),F(nums[2*gc]+100,D));assert cx[0]>0 or cx[1]<0
# Rotation derivative of each distance and each unit polynomial vanishes identically.
rotation=[[] for _ in range(b)]
for node in range(246):rotation[2*node]=[[-1,[2*node+1]]];rotation[2*node+1]=[[1,[2*node]]]
for j in rods+units:
 terms=[]
 for c,vs in constraints[j]:
  coeff=F(*c) if isinstance(c,list) else F(c)
  for i,k in enumerate(vs):
   for rc,rv in rotation[k]:terms.append([coeff*rc,vs[:i]+vs[i+1:]+rv])
 assert not norm(terms)
rejected=[]
for name,index,term in [('missing_normalization',nc+t,[1,[]]),('corrupted_force_coefficient',nc,sys['polynomials'][nc][0])]:
 bad=copy.deepcopy(sys['polynomials']);bad[index].remove(term)
 try:verify(bad)
 except AssertionError:rejected.append(name)
assert len(rejected)==2
out={'schema':'n100-first-order-rod-dual/v1','verified':True,'arithmetic':'integer/Fraction sparse polynomial identities','stationarity_coefficients_checked':493,'distance_rows':406,'unit_rows':32,'alpha_all_strictly_positive_on_root_box':True,'minimum_alpha_lower_bound':str(min(a for a,z in alpha_intervals)),'normalization_at_exact_root':'sum distance alpha = 1','identity':'sum alpha_j * rod_length_derivative_j + sum nu_k * unit_derivative_k + gamma * gauge_derivative = 0 at exact KKT root','cone_certificate':'for unit-tangent and gauge-fixed velocities, sum alpha_j * rod_length_derivative_j = 0; all rod derivatives <= dt<0 would imply 0 <= dt<0, contradiction','gauge_center':gc,'gauge_center_x_nonzero_interval':[str(x) for x in cx],'rotation_invariance_identity_rows_checked':438,'gauge_removal':'subtract rotation omega=velocity_y(gauge_center)/center_x(gauge_center); leaves rod derivatives and unit tangency unchanged','covers_all_velocities_at_this_root':True,'finite_step_or_other_root_exclusion':False,'quantitative_LOCAL_leaf_proved':False,'global_optimality_proved':False,'negative_controls_rejected':rejected,'source_sha256':{str(p.relative_to(R)).replace('\\','/'):sha(p) for p in [SROOT/'polynomial_system.json',SROOT/'rational_midpoint.json',SROOT/'krawczyk_verification.json',SROOT.parent/'SOURCE_BINDING.json']},'checker_sha256':sha(Path(__file__))}
p=R/'verify/out/n100-first-order-rod-dual.json'
assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('PASS 493 dual coefficient identities, positive 406 weights, exact normalization, 438 rotation identities, two corruptions rejected; first-order root only')
