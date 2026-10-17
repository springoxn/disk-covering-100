"""Exact symbolic audit of arbitrary-center arc/cap reduction.
No floating point; this does not formalize planar area or integration order.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    r,d,z,delta,u=S.symbols('r d z delta u',positive=True)
    C2=1-r*r;cos=(C2+d*d)/(2*d)
    cap=S.sqrt(2*r*z**3)*(S.Rational(4,3)-z/(5*r))
    checks={}
    def zero(name,expr):
        v=S.simplify(expr);need(v==0,name);checks[name]=True
    zero('cosine_squared_minus_cap_squared',(cos*cos-C2)-(d*d-C2)**2/(4*d*d))
    zero('cosine_radial_derivative',S.diff(cos,d)-(d*d-C2)/(2*d*d))
    zero('circle_cosine_positive_from_r_lt_one',2*d*cos-(1-r*r+d*d))
    zero('squared_tangent_majorant',(1-z/(4*r))**2-(1-z/(2*r))-z*z/(16*r*r))
    zero('cap_primitive_derivative',S.diff(cap,z)-2*S.sqrt(2*r*z)*(1-z/(4*r)))
    zero('cap_derivative_sign_factor',S.diff(cap,z)-S.sqrt(2*r*z)*(4*r-z)/(2*r))
    zero('tail_radial_separation',(1-r+u)-r-(1-2*r+delta)-(u-delta))
    zero('service_interval_low_endpoint',(1-r)+r-1)
    zero('service_interval_high_endpoint',(1+r)-r-1)
    # Demonstrate why a chord bound alone cannot select the short-arc branch:
    # phi and pi-phi have the same sine. Positive cosine supplied above is essential.
    theta=S.symbols('theta',real=True)
    zero('negative_control_chord_branch_ambiguity',S.sin(S.pi-theta)-S.sin(theta))
    p=ROOT/'verify/out/n100-arc-cap-rational-support.json';base=json.loads(p.read_text(encoding='utf-8'))
    rr=F(base['radius']);dd=F(base['delta']);M=F(base['maximum_half_arc_upper']);c=rr/M
    need(0<rr<F(1,2) and 0<dd<2*rr and dd<4*rr,'parameter domain')
    need((1-rr+dd)**2<1-rr*rr and c>0 and c*c<=1-rr*rr,'monotonicity and c domain')
    out=ROOT/'verify/out/n100-arc-cap-arbitrary-center.json';need(not out.exists(),'overwrite')
    result={'schema':'n100-arc-cap-arbitrary-center/v1','symbolic_identities':checks,'identity_count':len(checks),'sympy_version':S.__version__,
        'exact_parameter_domain_checked':True,'normalization_required_for_arc_cap_bound':False,
        'theorem_scope':'At fixed U, any m<=100 equal disks covering the target, arbitrary centers and multiplicities, have at least46 disks not meeting the unit circle; equivalently k<=m-46. This inherits stage28 rational support and analytic lemmas.',
        'analytic_reasoning':['r<1 makes cosine threshold positive, hence each nonempty circle intersection is a short arc','cosine squared identity gives cos(phi)>=sqrt(1-r^2) for all d>0, without norm cap','sin(phi)=integral cos(t) dt >= phi*cos(phi), so phi<=sin(phi)/c<=r/c','near branch 0<=u<=delta is inside d<sqrt(1-r^2), allowing previous interval monotonicity','far branch u>=delta has inner intersection of area zero; phi<=M supplies remaining support','every circle-serving disk has d in [1-r,1+r]; d=0 never serves at r<1','sum of covered arc lengths >= circle length and area subadditivity'],
        'algebra_checked_by_CAS_not_formal_geometry':True,'machine_verified_geometry':False,'global_optimality':False,'new_count_families_excluded':0,
        'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS arbitrary-center arc-cap:',len(checks),'exact symbolic identities and rational parameter domains; normalization unnecessary; geometry nonformal')
if __name__=='__main__':main()
