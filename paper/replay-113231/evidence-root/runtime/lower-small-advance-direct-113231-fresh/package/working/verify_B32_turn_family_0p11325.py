#!/usr/bin/env python3
"""Exactly replay all16 supplied B32 all-six graph certificates at .11325."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import verify_turn_B32_graph_0p11325 as one
ROOT=Path(__file__).resolve().parent
def verify():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 folder=ROOT/'B32_turn_family_0p11325_20261005'
 catalog=list(one.iter_graphs());assert len(catalog)==16
 results=[];bindings=[]
 for generated in catalog:
  fid=generated['family_id']
  gp=ROOT/'signed_edge_metric_B32_20261004/graphs'/(fid+'.json')
  cp=folder/(fid+'.certificate.json')
  raw=gp.read_bytes();craw=cp.read_bytes()
  assert json.loads(raw)==json.loads(json.dumps(generated))
  cert=json.loads(craw);r=one.verify(gp,cert);assert r['status']=='PASS'
  results.append(r)
  bindings.append({'family':fid,'graph_sha256':hashlib.sha256(raw).hexdigest(),'certificate_sha256':hashlib.sha256(craw).hexdigest()})
 assert len({x['family'] for x in bindings})==16
 worst=min(results,key=lambda x:F(x['area_margin']))
 return dict(status='PASS',radius='453/4000',graph_count=16,
  scope='All16 regenerated B32 P26/F108 all-six catalog families are excluded. A complete reduction of arbitrary covers at .11325 to this catalog remains separate.',
  minimum_area_margin=worst['area_margin'],worst_family=worst['family_id'],
  bindings_sha256=hashlib.sha256(json.dumps(bindings,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
  bindings=bindings,results=results)
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

