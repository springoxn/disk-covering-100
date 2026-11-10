#!/usr/bin/env python3
"""Exact all-p boundary-endpoint charges from a scalar hinge deficit."""
from fractions import Fraction as F
import json
import verify_exact_lens_boundary_0p11322 as whole
import verify_exact_lens_hinge_deficit as local
from verify_star_lp_duals import q,S
from verify_potential_star_duals import sine
R=F(5661,50000);B=33;K=F(11,25);SLOPE=F(3,100);ZERO=F(23,250);SPAN=F(3467,5000)
def charge(p):
    assert type(p) is int and 0<=p<B
    return SLOPE*max(F(0),(p+1)*ZERO-SPAN/2)/(2*R*R)
def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    whole.R=R;whole.B=B;whole.K=K;whole.CURVATURE=F(0)
    global_bound=whole.verify()
    local.R=R;local.B=B;local.K=K;local.CURVATURE=F(0);local.CUTOFF=ZERO;local.SLOPE=SLOPE
    hinge=local.verify()
    assert global_bound['status']==hinge['status']=='PASS'
    assert hinge['affine_slope']==str(SLOPE) and hinge['hinge_zero']==str(ZERO)
    footprint=sine(q(SPAN/2))-q(3*R);assert footprint.l>0
    values=[str(charge(p)) for p in range(B)]
    assert all(charge(p)==0 for p in range(3)) and charge(3)>0
    return dict(status='PASS',radius=str(R),B=B,halfside_multiplier=str(K),
        scope='Conditional normalized boundary allocation only; no covering-radius exclusion',
        required_center_norm_squared_upper=str(1-R*R),required_interior_vertex_count_minimum=2,
        hinge_slope=str(SLOPE),hinge_zero=str(ZERO),footprint_span_upper=str(SPAN),
        footprint_sine_margin=str(F(footprint.l,S)),endpoint_owner_multiplicity_upper=2,
        marked_incidence_domain=[0,B-1],normalized_area_charges=values,
        charge_convention='Total area loss is at least R^2 times the sum of the charge indexed by each ordinary marked apex count',
        simultaneous_variance_spending='None; the hinge consumes the stated scalar deficit',
        split_fans_allowed=True,ears_and_bad_marked_faces_allowed=True,
        global_nonnegative_deficit_status=global_bound['status'],
        hinge_interval_boxes=hinge['bad_arc_boxes'],minimum_hinge_scalar_margin=hinge['minimum_bad_arc_margin'])
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
