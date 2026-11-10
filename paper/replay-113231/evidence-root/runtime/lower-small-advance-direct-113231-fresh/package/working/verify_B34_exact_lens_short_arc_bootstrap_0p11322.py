#!/usr/bin/env python3
"""Conditional B34 raw-deficit bootstrap; the caller supplies its center row."""
from fractions import Fraction as F
import json
import verify_exact_lens_boundary_0p11322 as global_support
import verify_short_arc_exact_lens_loss as short_support
from verify_star_lp_duals import q,S
from verify_potential_star_duals import sine
R=F(5661,50000);B=34;K=F(1,2);HALF=F(39,500);BUDGET=F(1,2500)
def verify():
    global_support.R=R;global_support.B=B;global_support.K=K;global_support.CURVATURE=F(3,100)
    whole=global_support.verify()
    short_support.R=R;short_support.B=B;short_support.K=K
    short_support.CURVATURE=F(0);short_support.CUTOFF=HALF
    short=short_support.verify()
    assert whole['status']==short['status']=='PASS'
    loss=F(short['minimum_bad_arc_margin']);assert loss>BUDGET
    two=sine(q(3*HALF))-q(2*R)
    three=sine(q(5*HALF))-q(3*R)
    assert two.l>0 and three.l>0
    return dict(status='PASS',radius=str(R),B=B,initial_halfside_multiplier=str(K),
        scope='Conditional bootstrap: requires an independent initial row with raw total surplus<=the reported budget and no boundary-deficit spending',
        required_raw_surplus_upper=str(BUDGET),short_arc_loss_lower=str(loss),
        half_arc_lower=str(HALF),full_arc_lower=str(2*HALF),
        all_boundary_center_faces_excluded=True,ears_excluded=True,
        maximum_consecutive_boundary_neighbor_cells=4,ordinary_marked_incidence_upper=3,
        radius2_footprint_sine_margin=str(F(two.l,S)),radius3_footprint_sine_margin=str(F(three.l,S)),
        global_scalar_status=whole['status'],short_interval_boxes=short['bad_arc_boxes'])
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
