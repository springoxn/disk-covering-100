#!/usr/bin/env python3
"""Fresh exact radius-only extension of the unchanged sixteen metric rows."""
from fractions import Fraction as F
from pathlib import Path
import sys,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path[:0]=[str(HERE),str(ROOT/'signed_edge_metric_20261004'),str(ROOT)]
from verify_all_graphs import verify as verify_source
from exact_signed_conjugates import q,S,PI
from verify_potential_star_duals import sine
TARGET=F(11317,100000)

def verify():
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    source=verify_source()
    assert source['status']=='PASS' and source['radius']=='2829/25000'
    assert source['graph_count']==16
    theta=2*PI/32
    r=q(TARGET);s=sine(theta/2)
    H=s*(r.sq()-s.sq()).sqrt()+(theta-sine(theta))/2
    rows=[]
    for old in source['rows']:
        assert old['status']=='PASS' and old['radius']=='2829/25000'
        assert old['q0_supports']==134 and old['q1_supports']==32
        C=F(old['normalized_center_upper'])
        assert C>0
        margin=F((PI-(r.sq()*q(C)+32*H)).l,S)
        assert margin>0,old['family_id']
        row=dict(old,radius=str(TARGET),area_margin=str(margin))
        rows.append(row)
    worst=min(rows,key=lambda x:F(x['area_margin']))
    return dict(status='PASS',scope='All sixteen supplied B32 graph families are excluded at .11317; the complete same-radius reduction and catalog theorem remain separate premises',
                radius=str(TARGET),source_radius=source['radius'],graph_count=16,
                catalog_sha256=source['catalog_sha256'],
                minimum_area_margin=worst['area_margin'],
                minimum_margin_family=worst['family_id'],rows=rows)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
