#!/usr/bin/env python3
"""Integer/rational checks for the developed-core isoperimetric reduction."""
from fractions import Fraction as F
import json


def verify():
    assert F(25*25,6)<106
    assert F(3*3+23*23,6)==F(269,3)<106
    assert F(3*3+24*24,6)==F(195,2)<105
    widths=[]
    regions=[]
    for x in range(1,27):
        for y in range(x,27):
            z=26-x-y
            if z<y:
                continue
            bound=F(26*26,6)-F((x-y)**2+(y-z)**2+(z-x)**2,3)
            if bound<106:
                continue
            widths.append((x,y,z))
            delta=x+y-z
            for L in range(max(0,max(x,y)-z),min(x,y,delta)+1):
                U=delta-L
                if L>U:
                    continue
                area=2*x*y-L*L-U*U
                if area>=106:
                    regions.append({'widths':[x,y,z],'lower_diagonal_offset':L,
                                    'upper_corner_cut':U,'triangle_count':area,
                                    'triangles_to_delete':area-106})
    assert widths==[(7,9,10),(8,8,10),(8,9,9)]
    assert len(regions)==6
    assert sorted(r['triangle_count'] for r in regions)==[106,108,108,110,110,112]
    return {'status':'PASS','N26_width_triples':[list(w) for w in widths],
            'N26_containing_regions':regions,
            'nonsimple_area_upper':{'P26':'269/3','P27':'195/2'},
            'scope':'Conditional injective-development and containing-region reduction, not a completed core or covering enumeration'}


if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
