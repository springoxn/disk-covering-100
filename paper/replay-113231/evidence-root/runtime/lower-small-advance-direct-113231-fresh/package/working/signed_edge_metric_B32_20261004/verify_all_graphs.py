#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib,time
ROOT=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(ROOT/'lower_bounds_extension_20261004')]
from export_B32_P26_F108_families import iter_graphs,CATALOG
from verify_pure_metric import verify as verify_graph
M=Path(__file__).resolve().parent

def verify():
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    start=time.monotonic();rows=[]
    assert hashlib.sha256(CATALOG.read_bytes()).hexdigest()=='6bc2f1e934d36d6ee35a2aeb6ee7ee68f2eac8d3faa473975fceb2447ebb5742'
    for graph in iter_graphs():
        cert=json.loads((M/'certificates'/(graph['family_id']+'.json')).read_text());rows.append(verify_graph(graph,cert))
    assert len(rows)==16 and len({x['family_id'] for x in rows})==16
    from fractions import Fraction
    worst=min(rows,key=lambda x:Fraction(x['area_margin']))
    return dict(status='PASS',scope='All16 generated B32 graph families are excluded at .11316; the separate reduction and catalog-completeness proof are required for the complete B32 branch',radius='2829/25000',graph_count=16,catalog_sha256=hashlib.sha256(CATALOG.read_bytes()).hexdigest(),minimum_area_margin=worst['area_margin'],minimum_margin_family=worst['family_id'],rows=rows,seconds_reporting_only=time.monotonic()-start)
if __name__=='__main__':print(json.dumps(verify(),indent=2))
