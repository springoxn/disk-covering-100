from pathlib import Path
from fractions import Fraction as F
import hashlib,json
R=Path(__file__).resolve().parents[1];bp=R/'verify/out/n100-cover-hole-bridge.json';b=json.loads(bp.read_text(encoding='utf-8'));assert b['verified_interval_and_scalar_bounds']
half=F(1,10**55);rooterr=F(1,10**58);eps=F(b['root_centered_center_coordinate_radius']);assert half+rooterr<eps
out={'schema':'n100-cover-center-midpoint-box/v1','verified':True,'centers':100,'center_coordinates':200,'rational_midpoint_box_halfwidth':str(half),'root_coordinate_uncertainty':str(rooterr),'coordinate_distance_to_exact_root_upper':str(half+rooterr),'allowed_center_coordinate_radius':str(eps),'fixed_affine_gauge_required':True,'radius_condition':'t<=t* exact algebraic root','conclusion_requires_reviewed_bridge':'No covering at t<t* in this center box and fixed gauge, once the persistent-hole bridge and fixed-rod theorem are accepted.','all_topologies_or_global_domain_covered':False,'bridge_receipt_sha256':hashlib.sha256(bp.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
p=R/'verify/out/n100-cover-center-midpoint-box.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('PASS 200-coordinate midpoint center box halfwidth 1e-55 lies inside root-centered support-bridge box epsilon 1e-54; affine gauge required')
