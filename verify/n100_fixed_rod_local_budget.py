"""Exact scalar budget for augmented-Lagrangian LOCAL exclusion on a fixed rod domain.
Uses the accepted SOSC replay as a dependency; does not replay its large matrix calculation.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1];rp=R/'runtime/external-disk100-strict-local-replay/replay_verification.json';sp=rp.parent/'source/polynomial_system.json';mp=sp.parent/'rational_midpoint.json';dp=R/'verify/out/n100-first-order-rod-dual.json'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=load(rp);s=load(sp);mid=load(mp);dual=load(dp);assert r['verified'] and dual['verified']
assert dual['source_sha256'][str(sp.relative_to(R)).replace('\\','/')]==sha(sp)
assert dual['source_sha256'][str(mp.relative_to(R)).replace('\\','/')]==sha(mp)
b=r['exact_bounds'];get=lambda k:F(*b[k]);D=int(mid['denominator']);x=[F(int(v),D) for v in mid['numerators']];rho=F(1,10**58)
H=F(1);Z=F(110);RR=F(500000);mu=F(1,10000)
assert get('hessian_midpoint_infinity_norm')+get('hessian_root_perturbation_infinity_bound')<=H
assert (get('null_basis_midpoint_infinity_norm')+get('null_basis_error_infinity_bound'))*(get('null_basis_midpoint_transpose_infinity_norm')+get('null_basis_error_transpose_infinity_bound'))<=Z**2
assert 439*get('pivot_inverse_infinity_bound')<=RR
assert (1-get('transformed_total_identity_residual'))/(get('cholesky_transform_infinity_norm')*get('cholesky_transform_transpose_infinity_norm'))>=mu
# Bound Jacobian spectral norm by Frobenius norm via row l1 bounds.
nc=439;nb=493;t=492;rowbounds=[]
for poly in s['polynomials'][:nc]:
 deriv=[F(0)]*nb
 for c,vs in poly:
  cf=abs(F(*c) if isinstance(c,list) else F(c))
  for i,k in enumerate(vs):
   prod=cf
   for j,v in enumerate(vs):
    if j!=i:prod*=abs(x[v])+rho
   deriv[k]+=prod
 rowbounds.append(sum(deriv))
J=F(1000);q=F(42)
assert sum(v*v for v in rowbounds)<=J*J
assert q*q>=4*nc
# mu/2*u² + e² lower bound for H+2k J^T J, h=Z*u+R*e.
kappa=F(10**21);m=F(1,10**12);radius=F(1,10**40)
K=2*H**2*Z**2*RR**2/mu+H*RR**2
assert 2*kappa-K>=1
assert m<=mu/(4*Z**2) and m<=1/(2*RR**2)
alpha=F(dual['minimum_alpha_lower_bound']);assert alpha>F(1,100000)
# Exact quadratic constraints: f(x*+h)=J*h+Q(h), ||Q||<=q||h||².
assert 2*kappa*J*q*radius<=m/4
assert kappa*(J*radius+2*radius**2)<=alpha
# Negative controls exercise actual radius-dependent requirements.
rejected=[]
for bad in [F(1,10**30),F(1,10**10)]:
 if not (2*kappa*J*q*bad<=m/4 and kappa*(J*bad+2*bad**2)<=alpha):rejected.append(str(bad))
assert len(rejected)==2
out={'schema':'n100-fixed-rod-local-budget/v1','verified_scalar_budget':True,'norm':'Euclidean norm of 493 base variables, including t; affine rotation gauge fixed','constants':{k:str(v) for k,v in dict(H=H,Z=Z,R_right_inverse=RR,reduced_mu=mu,J=J,Q=q,kappa=kappa,ambient_m=m,radius=radius,alpha_min=alpha,growth_coefficient=m/4).items()},'conclusion':'At the certified exact KKT root x*, for 0<||h||_2<=radius, all 406 fixed rod constraints f_j<=0, all 32 unit equalities and affine gauge equality imply t(x*+h)-t* >= (m/4)||h||_2^2 > 0.','dependency':'Accepted SOSC exact replay; scalar budget does not independently repeat its matrix verification. Analytic decomposition and augmented-Lagrangian argument require separately reviewed proof note.','full_covering_LOCAL_leaf':False,'other_contact_graphs_excluded':False,'global_optimality':False,'oversized_radii_rejected':rejected,'source_sha256':{str(p.relative_to(R)).replace('\\','/'):sha(p) for p in [rp,sp,mp,dp]},'checker_sha256':sha(Path(__file__))}
op=R/'verify/out/n100-fixed-rod-local-budget.json';assert not op.exists();op.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('PASS exact augmented local scalar budget: radius 1e-40, growth 1/(4e12); fixed rod domain only; two oversized radii rejected')
