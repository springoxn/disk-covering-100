from fractions import Fraction as F
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
p=R/'verify/out/n100-fixed-rod-local-budget.json';b=json.loads(p.read_text());assert b['verified_scalar_budget']
radius=F(b['constants']['radius']);rho=F(1,10**58);half=F(1,10**42);sqrt493_upper=F(23)
assert sqrt493_upper**2>=493
bound=sqrt493_upper*(half+rho)
assert bound<radius
out={'schema':'n100-local-midpoint-box-containment/v1','verified':True,'base_dimension':493,'midpoint_centered_box_half_width':str(half),'root_coordinate_error':str(rho),'Euclidean_distance_to_exact_root_upper':str(bound),'accepted_fixed_rod_radius':str(radius),'contained':True,'fixed_graph_feasibility_required':True,'automatically_maps_all_nearby_coverings':False,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
op=R/'verify/out/n100-local-midpoint-box-containment.json';assert not op.exists();op.write_text(json.dumps(out,indent=2)+'\n');print('PASS: 493-coordinate midpoint box halfwidth 1e-42 lies strictly inside fixed-rod root ball radius 1e-40')
