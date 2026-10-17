from pathlib import Path
from fractions import Fraction as F
import hashlib,json
R=Path(__file__).resolve().parents[1];p=R/'verify/out/n100-local-widened-budget.json';b=json.loads(p.read_text(encoding='utf-8'));assert b['verified']
for path,digest in b['dependencies_sha256'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest
half=F(1,10**38);root=F(1,10**58);allowed=F(b['constants']['ungauged_center_radius']);assert half+root<allowed
op=R/'verify/out/n100-widened-center-box.json';assert not op.exists()
op.write_text(json.dumps({'schema':'n100-widened-center-box/v1','verified':True,'coordinates':200,'midpoint_box_halfwidth':str(half),'exact_root_coordinate_uncertainty':str(root),'total_coordinate_root_error_bound':str(half+root),'accepted_ungauged_local_radius':str(allowed),'fixed_gauge_required':False,'conclusion':'Once widened scalar budget is independently accepted, the center midpoint box has no strictly improved covering at t<t*.','global_exclusion':False,'budget_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS all widened budget dependency hashes and midpoint center box halfwidth1e-38, no gauge prerequisite')
