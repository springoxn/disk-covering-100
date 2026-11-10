#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path[:0]=[str(HERE),str(ROOT/'lower_bounds_extension_20261004')]
from verify_same_radius_0p11322 import verify as verify_graph
from export_B32_P26_F108_families import iter_graphs,CATALOG

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    assert hashlib.sha256(CATALOG.read_bytes()).hexdigest()=='6bc2f1e934d36d6ee35a2aeb6ee7ee68f2eac8d3faa473975fceb2447ebb5742'
    rows=[]
    for graph in iter_graphs():
        name=graph['family_id']+'.json'
        path=ROOT/'signed_edge_metric_B32_20261004'/'graphs'/name
        assert json.loads(path.read_text())==json.loads(json.dumps(graph))
        certificate=json.loads((HERE/'certificates_0p1132'/name).read_text())
        assert certificate['radius']==[283,2500]
        certificate=dict(certificate,radius=[5661,50000])
        rows.append(verify_graph(path,certificate))
    assert len(rows)==len({r['family_id'] for r in rows})==16
    worst=min(rows,key=lambda r:F(r['area_margin']))
    return dict(status='PASS',scope='All sixteen catalog graphs only; same-radius global topology reduction remains a separate premise',
                radius='5661/50000',graph_count=16,catalog_sha256=hashlib.sha256(CATALOG.read_bytes()).hexdigest(),
                minimum_area_margin=worst['area_margin'],minimum_margin_family=worst['family_id'],rows=rows)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
