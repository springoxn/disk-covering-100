#!/usr/bin/env python3
"""Three exact B32 scalar hinges at R=.11323; no radius exclusion."""
from fractions import Fraction as F
import json
import verify_exact_lens_boundary_0p11322 as whole
import verify_exact_lens_hinge_deficit_tight as local
R=F(113231,1000000);B=32
SETTINGS=((F(11,25),F(187,2000),F(119,2000)),
          (F(11,25),F(47,500),F(111,2000)),
          (F(11,25),F(19,200),F(11,250)))

def verify_case(index):
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    assert type(index) is int and 0<=index<len(SETTINGS)
    k,cutoff,slope=SETTINGS[index]
    for source in (whole,local):
        source.R=R;source.B=B;source.K=k;source.CURVATURE=F(0)
    local.CUTOFF=cutoff;local.SLOPE=slope
    global_bound=whole.verify();hinge=local.verify()
    assert global_bound['status']==hinge['status']=='PASS'
    assert global_bound['radius']==hinge['radius']==str(R)
    assert global_bound['B']==hinge['B']==B
    assert global_bound['halfside_multiplier']==hinge['halfside_multiplier']==str(k)
    assert hinge['affine_slope']==str(slope) and hinge['hinge_zero']==str(cutoff)
    assert global_bound['variance_coefficient']==hinge['variance_coefficient']=='0'
    return dict(status='PASS',case=index,radius=str(R),B=B,
      halfside_multiplier=str(k),hinge_slope=str(slope),hinge_zero=str(cutoff),
      required_center_norm_squared_upper=str(1-R*R),
      global_nonnegative_deficit=global_bound,local_positive_hinge=hinge,
      scope='Conditional normalized scalar deficit >= c*(T-t)_+ only. No center-face, owner-allocation or universal radius exclusion is asserted; no variance is spent.')

def verify():
    rows=[verify_case(index) for index in range(len(SETTINGS))]
    assert len(rows)==3 and all(z['status']=='PASS' for z in rows)
    return dict(status='PASS',radius=str(R),B=B,settings_count=3,
      scope='Three exact same-radius boundary-envelope/hinge tradeoffs only',cases=rows)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
