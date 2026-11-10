#!/usr/bin/env python3
"""Exact integer consequences of the induced-core block isoperimetry."""
import json


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    rows=[]
    for B in range(32,39):
        m=100;limit=25 if B<=34 else 24
        base=2*m-2*B-2
        margins=[6*(base-U)-U*U for U in range(limit+1)]
        assert min(margins)>0
        rows.append({'m':m,'B':B,'U_upper':limit,
                     'minimum_integer_contradiction_margin':min(margins),
                     'necessary_low_star_types':[[0,3],[0,4],[0,5]],
                     'shifted_U_upper_including_bad_q0_q1':str(limit)+'+2e'})
    return {'status':'PASS','cases':rows,
            'required_combinatorial_theorem':'Face-bearing induced-core blocks with interior degrees at least 6 have F<=b^2/6',
            'general_shift_identity':'n2+n3=e+2(c-1), where c>=1 counts induced-interior components',
            'general_frontier_bound':'b=U-2e-4(c-1)-n3<=U-2e',
            'scope':'Necessary occurrence of a low-degree unmarked interior star; no radius exclusion'}


if __name__=='__main__':print(json.dumps(verify(),indent=2))
