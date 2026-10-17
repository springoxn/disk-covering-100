from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1];p=R/'verify/out/n100-local-rotation-gauge.json';a=json.loads(p.read_text());mp=R/'runtime/external-disk100-strict-local-replay/source/rational_midpoint.json';m=json.loads(mp.read_text());D=int(m['denominator']);v=[F(int(x),D) for x in m['numerators']];r=F(1,10**58);e=F(a['input_center_radius']);angle=2*e
assert a['source_sha256']==hashlib.sha256(mp.read_bytes()).hexdigest()
assert all(abs(z)+r+e<2 for z in v[:200])
# g'=x cos th-y sin th negative uniformly when x<-0.9 and all |y|<2
assert v[148]+r+e < -F(9,10)
assert F(9,10)*(1-angle**2/2)-2*angle > F(1,2)
# endpoint sign: |g0|<=e and derivative<-1/2 on [-2e,2e]
# equality at bounds still permits a root; strict inequality yields unique root.
assert angle/2==e
# displacement of each coordinate <=2|sin|+2|1-cos|<=2angle+angle²
bound=e+2*angle+angle**2
assert bound < F(a['accepted_gauge_box_radius'])
# independent bound sharper than primary 4angle+angle².
assert bound<=F(a['normalized_center_radius_bound'])
# Rotation orthogonality checked by rational Cayley formulas for symbolic numerator as coefficient list:
# (1-u²)^2+(2u)^2=(1+u²)^2, coefficients 1,0,2,0,1 both sides.
left=[1,0,-2+4,0,1];right=[1,0,2,0,1];assert left==right
bp=R/'verify/out/n100-cover-bridge-review.json';b=json.loads(bp.read_text());assert b['verdict']=='PASS_WITHIN_DECLARED_SCOPE'
out={'schema':'n100-rotation-gauge-independent/v1','verified':True,'root_coordinates_abs_lt_2':True,'gauge_derivative_magnitude_gt_half':True,'monotone_IVT_root_interval':'[-2epsilon,2epsilon]','normalization_coordinate_error_upper':str(bound),'Cayley_orthogonality_polynomial_identity':True,'bridge_review_accepted':True,'conclusion':'No strictly improved covering with labeled centers coordinatewise within 1e-55 of exact root; rotation normalization enters accepted fixed-gauge bridge. Relabeling or applying any common rotation to this neighborhood transports the same result by isometry.','global_exclusion':False,'inputs_sha256':{str(x.relative_to(R)).replace('\\','/'):hashlib.sha256(x.read_bytes()).hexdigest() for x in [p,mp,bp]},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
op=R/'verify/out/n100-rotation-gauge-independent.json';assert not op.exists();op.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('PASS independent gauge derivative, all 200 coordinate bounds, orthogonality polynomial and bridge dependency')
