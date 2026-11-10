#!/usr/bin/env python3
"""Complete B31 exclusion through .11322 by a degree-six curvature test."""
from fractions import Fraction as F
import json
import verify_extension as v
import check_global_apex_minimum_degree as tangents

R=F(5661,50000);B=31


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    v.R=R;v.check_kappa();v.check_concavity_factorization()
    n99=v.exclude_all(99,R)
    center=((198-B)*v.AH+B*v.KAPPA)*R*R
    surplus=center+B*v.H_upper(R,2*v.PL/B,2*v.PH/B)-v.PL
    d=surplus/(R*R)
    v.need(d<F(27,100),'old normalized loss budget below .27')
    source=tangents.verify()
    r5l,r5h=v.sqrt_bounds(F(5));cl,ch=(r5l-1)/4,(r5h-1)/4
    sl=v.sqrt_bounds(1-ch*ch)[0];sh=v.sqrt_bounds(1-cl*cl)[1]
    kl=sl*(1+cl)+v.PL/5;kh=sh*(1+ch)+v.PH/5
    Lh=v.sqrt_bounds(F(3))[1]+v.PH/6
    v.need(v.AH-kl<0,'degree coefficient negative')
    v.need(v.KAPPA+kl-Lh>0,'marked-incidence coefficient positive')
    low_degree_loss=v.PL+5*(v.AL-kh)
    v.need(low_degree_loss>F(27,100),'every degree at most five costs more than .27')
    m=100;faces=2*m-B-2
    v.need(6*faces>B*B,'degree-six disk isoperimetric contradiction')
    dlo,dhi=v.outward(d,d,25)
    llo,lhi=v.outward(low_degree_loss,low_degree_loss,25)
    return {'status':'PASS','radius_upper':str(R),'B':B,'m':m,
            'scope':'Complete B31 branch exclusion only; other boundary counts and exact optimality remain separate',
            'exclusion_of_99':n99,'global_tangent_lemma_status':source['status'],
            'normalized_old_loss_budget_interval':[str(dlo),str(dhi)],
            'degree_at_most_five_loss_lower_interval':[str(llo),str(lhi)],
            'forced_minimum_interior_degree':6,'center_faces':faces,
            'disk_isoperimetric_integer_gap':6*faces-B*B,
            'additional_arc_or_fan_hypotheses':False,
            'ears_and_all_boundary_faces_allowed':True}


if __name__=='__main__':print(json.dumps(verify(),indent=2))
