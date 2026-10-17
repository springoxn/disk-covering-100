"""Exact scalar audit for removing the affine rotation gauge locally."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1];src=R/'runtime/external-disk100-strict-local-replay/source';mid=json.loads((src/'rational_midpoint.json').read_text());D=int(mid['denominator']);N=list(map(int,mid['numerators']));rho=F(1,10**58);rootx=F(N[148],D);rooty=F(N[149],D);eps=F(1,10**55);target=F(1,10**54);theta=F(1,10**54)
# root x nonzero and stays negative on the smaller center box
assert rootx+rho+eps < -F(9,10)
# g(theta)=x sin(theta)+y cos(theta)-y0, for |theta|<=theta0; derivative remains < -1/2
# use rational Taylor enclosures: |sin th|<=|th|, |1-cos th|<=th²/2.
assert (abs(rootx)+rho+eps)*F(1,1) > F(9,10)
assert (abs(rooty)+rho+eps)*theta + (abs(rootx)+rho+eps)*theta**2/2 < F(1,10**50)
assert F(9,10)*(1-theta**2/2)-(abs(rooty)+rho+eps)*theta > F(1,2)
# |g(0)|<=eps; interval derivative magnitude >=1/2; IVT root |theta*|<=2eps
rot_angle=2*eps
# coordinate change bound |Rtheta p-p| <= |theta|*(|x|+|y|) using |sin|<=theta and |cos-1|<=theta²/2
coord_abs=F(2);disp=rot_angle*(coord_abs+coord_abs)+rot_angle**2*coord_abs/2
final=eps+disp+rho
assert final<target
# exact distance preservation identities for rotation matrix symbols are recorded in receipt
rejected=[]
for e in (F(1,10**52),F(1,10**48)):
 if e+2*e*(coord_abs+coord_abs)+ (2*e)**2*coord_abs/2 < target: continue
 rejected.append(str(e))
assert len(rejected)==2
out={'schema':'n100-local-rotation-gauge/v1','verified':True,'gauge_center':74,'target_y_exact_root_midpoint_value':str(rooty),'root_x_interval_lower_abs':str(abs(rootx)-rho),'input_center_radius':str(eps),'root_uncertainty':str(rho),'derivative_lower_abs':'1/2 (conservative)','rotation_angle_abs_bound':'2*input_radius','coordinate_abs_bound':'2','rotation_displacement_bound':str(disp),'normalized_center_radius_bound':str(final),'accepted_gauge_box_radius':str(target),'rotation_preserves_all_distances_and_unit_circle':'exact orthogonal rotation identity; analytic fact, not float decision','covers_ungauged_local_centers_within_input_radius':True,'other_rotations_or_global_domain':False,'negative_controls_rejected':rejected,'source_sha256':hashlib.sha256((src/'rational_midpoint.json').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
p=R/'verify/out/n100-local-rotation-gauge.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('PASS local rotation gauge: centers radius 1e-55 normalize into gauge radius 1e-54; angle bound 2e-55; oversized controls rejected')
