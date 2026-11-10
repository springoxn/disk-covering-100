#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from verify_joint_metric_0p1132 import verify as verify_graph

def verify():
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    rows=[]
    for i in range(16):
        name='B32_P26_F108_'+str(i).zfill(3)+'.json'
        rows.append(verify_graph(HERE/'graphs'/name,json.loads((HERE/'joint_certificates_0p1132'/name).read_text())))
    assert len({r['family_id'] for r in rows})==16 and all(r['radius']=='283/2500' for r in rows)
    worst=min(rows,key=lambda r:F(r['area_margin']))
    return dict(status='PASS',radius='283/2500',scope='All sixteen specified B32 graph families only; a same-radius complete topology reduction is a separate obligation',graph_count=16,minimum_area_margin=worst['area_margin'],minimum_margin_family=worst['family_id'],maximum_pure_center_bound=str(max(F(r['pure_normalized_center_upper']) for r in rows)),rows=rows)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
