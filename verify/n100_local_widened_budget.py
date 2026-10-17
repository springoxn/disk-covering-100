from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rp=R/'runtime/external-disk100-strict-local-replay/replay_verification.json';hp=R/'verify/out/n100-cover-hole-bridge.json';ap=R/'verify/out/n100-local-augmented-audit.json';bp=R/'verify/out/n100-cover-bridge-review.json';sp=rp.parent/'source/polynomial_system.json';mp=sp.parent/'rational_midpoint.json'
r=load(rp);h=load(hp);a=load(ap);br=load(bp);s=load(sp);mid=load(mp)
assert r['verified'] and a['audit_verified'] and br['verdict']=='PASS_WITHIN_DECLARED_SCOPE'
b=r['exact_bounds'];qv=lambda k:F(*b[k]);H=F(2,25);Z=F(44);RR=F(22000);mu=F(1,10000);J=F(165);q=F(42);k=F(10**14);m=F(1,10**9);radius=F(1,10**29)
assert qv('hessian_midpoint_infinity_norm')+qv('hessian_root_perturbation_infinity_bound')<=H
assert (qv('null_basis_midpoint_infinity_norm')+qv('null_basis_error_infinity_bound'))*(qv('null_basis_midpoint_transpose_infinity_norm')+qv('null_basis_error_transpose_infinity_bound'))<=Z**2
assert 439*qv('pivot_inverse_infinity_bound')**2<=RR**2
assert (1-qv('transformed_total_identity_residual'))/(qv('cholesky_transform_infinity_norm')*qv('cholesky_transform_transpose_infinity_norm'))>=mu
D=int(mid['denominator']);nums=[F(int(v),D) for v in mid['numerators']];rho=F(1,10**58);rows=[]
for poly in s['polynomials'][:439]:
 row=[F(0)]*493
 for c,vs in poly:
  coeff=abs(F(*c) if isinstance(c,list) else F(c))
  for i,j in enumerate(vs):
   val=coeff
   for ii,v in enumerate(vs):
    if ii!=i:val*=abs(nums[v])+rho
   row[j]+=val
 rows.append(sum(row))
assert sum(v*v for v in rows)<=J*J
Kyoung=2*H*H*Z*Z*RR*RR/mu+H*RR*RR
assert 2*k-Kyoung>=1
assert m<=mu/(4*Z*Z) and m<=1/(2*RR*RR)
alpha=F(a['constants']['alpha_min'])
assert 2*k*J*q*radius<=m/4
assert k*(J*radius+2*radius**2)<=alpha
K=F(7);eps=F(1,10**36);eta=F(1,10**33);ungauged=F(1,10**37)
assert max(F(v['inverse_infinity_upper']) for v in h['holes'])<=K
assert 128*K*eps<=eta and K*(16*eps+4*eta)<=F(1,2)
delta=64*(eta+eps);assert F(h['min_inactive_squared_gap'])>delta
assert F(h['min_interior_unit_margin'])>32*eta+2*eta**2
lift=23*max(eps,eta,delta);assert lift<radius
assert all(abs(v)+rho+ungauged<2 for v in nums[:200])
assert nums[148]+rho+ungauged<-F(9,10)
angle=2*ungauged;assert F(9,10)*(1-angle**2/2)-2*angle>F(1,2)
normalized=ungauged+2*angle+angle**2;assert normalized<eps
badlocal=F(1,10**20);assert 2*k*J*q*badlocal>m/4
badcenters=F(1,10**30);assert 128*K*badcenters>eta
out={'schema':'n100-local-widened-budget/v1','verified':True,'constants':{key:str(v) for key,v in dict(H=H,Z=Z,R=RR,mu=mu,J=J,Q=q,kappa=k,ambient_m=m,fixed_rod_radius=radius,branch_inverse=K,fixed_gauge_center_radius=eps,hole_radius=eta,ungauged_center_radius=ungauged,growth_coefficient=m/4).items()},'493_lift_norm_bound':str(lift),'rotation_normalized_coordinate_error_bound':str(normalized),'young_negative_normal_term':str(Kyoung),'fixed_rod_radius_improvement_factor':str(radius/F(1,10**40)),'ungauged_center_radius_improvement_factor':str(ungauged/F(1,10**55)),'negative_controls':['oversized_fixed_rod_radius_1e-20','oversized_center_radius_1e-30'],'local_covering_conclusion':'For labeled centers coordinatewise within 1e-37 of exact root, no t<t* covering of D exists. Small rotation reaches the 1e-36 fixed gauge box, continued 146 holes force 406 inequalities and lift into radius1e-29 fixed-rod domain.','global_optimality':False,'all_topology_domains_excluded':False,'minimal_polynomial_obtained':False,'dependencies_sha256':{str(p.relative_to(R)).replace('\\','/'):sha(p) for p in [rp,hp,ap,bp,sp,mp]},'checker_sha256':sha(Path(__file__))}
p=R/'verify/out/n100-local-widened-budget.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('PASS widened exact constants: fixed-rod radius1e-29, ungauged center radius1e-37, 18 orders larger center neighborhood, local only')
