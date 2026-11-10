#!/usr/bin/env python3
"""Propose an exact rectangle certificate; floats select search order only."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,time
import numpy as np
from scipy.spatial import cKDTree
HERE=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(HERE))
from verify_quadtree import covered,outside,verify
cfg=json.loads((HERE/'configuration.json').read_text());Q=cfg['coordinate_denominator'];C=cfg['centers_numerators']
U=F(*cfg['radius_bound']);tree=cKDTree(np.array(C,dtype=float)/Q)
stack=[(0,0,0)];codes=[];t=time.time()
while stack:
    d,i,j=stack.pop()
    if outside(d,i,j):codes.append(-1);continue
    s=1<<d;mid=((2*i-s+1)/s,(2*j-s+1)/s)
    _,ww=tree.query(mid,k=8)
    found=None
    for w in ww:
        w=int(w)
        if covered(d,i,j,C[w],Q,U):found=w;break
    if found is not None:codes.append(found);continue
    if d>=50:raise ValueError('Depth limit reached; this is not an accepted certificate')
    codes.append(-2)
    stack.extend([(d+1,2*i+1,2*j+1),(d+1,2*i,2*j+1),
                  (d+1,2*i+1,2*j),(d+1,2*i,2*j)])
cert={'radius_bound':cfg['radius_bound'],'preorder_nodes':codes}
(HERE/'quadtree_certificate.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
a=verify(HERE/'configuration.json',HERE/'quadtree_certificate.json')
(HERE/'quadtree_verification_result.json').write_text(json.dumps(a,indent=2)+'\n')
print(json.dumps(a,indent=2));print('seconds',time.time()-t)
