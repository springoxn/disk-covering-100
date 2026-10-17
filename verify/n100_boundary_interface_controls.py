"""Exact controls for normalization collisions and nonowning boundary-service disks."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    r=F(1154469548855829,10**16);C2=1-r*r;d1=F(9,10);d2=F(99,100)
    need(1-r<d1<d2 and d2*d2<C2,'legal norm cap centers')
    threshold=(C2+d1*d1)/(2*d1);bisector=(d1+d2)/2
    need(threshold<1 and threshold>bisector,'nonempty covered arc dominated by outer site')
    # For any q on circle with q.x>=threshold:
    # |q-c1|²-|q-c2|² = 2(d2-d1)(q.x-bisector)>0.
    min_gap=2*(d2-d1)*(threshold-bisector);need(min_gap>0,'dominance')
    # Piecewise normalization is not globally injective across its two branches.
    outside=C2/d1
    need(outside*outside>C2 and outside!=d1 and d1*d1<C2,'collision parameters')
    need(C2/outside==d1,'normalization collision')
    output={'schema':'n100-boundary-interface-controls/v1','verified_rational_arithmetic':True,'radius':str(r),'norm_cap_squared':str(C2),'inner_center_norm':str(d1),'outer_center_norm':str(d2),
        'inner_service_arc_cosine_threshold':str(threshold),'bisector_coordinate':str(bisector),'minimum_squared_distance_advantage':str(min_gap),
        'norm_cap_does_not_imply_every_service_disk_owns_boundary':True,
        'normalization_collision':{'unmodified_center_norm':str(d1),'modified_center_original_norm':str(outside),'common_image_norm':str(d1)},
        'piecewise_normalization_global_injectivity':False,
        'B_le_k_requires_normalized_single_arc_and_full_cover':True,'k_equals_B_not_accepted':True,
        'psi_B_strictly_less_than_B_cannot_upper_bound_k_when_B_le_k':True,
        'scope':'exact two-site geometric countercontrols; not a complete 100-disk cover or global lower bound',
        'analytic_dependencies':['circle disk intersection cosine formula','distance difference along same radial direction','norm-cap normalization definition'],
        'global_optimality':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=ROOT/'verify/out/n100-boundary-interface-controls.json';need(not out.exists(),'refuse overwrite');out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('PASS exact dominated service arc and piecewise-normalization collision; reject k=B and injectivity assumptions')
if __name__=='__main__':main()
