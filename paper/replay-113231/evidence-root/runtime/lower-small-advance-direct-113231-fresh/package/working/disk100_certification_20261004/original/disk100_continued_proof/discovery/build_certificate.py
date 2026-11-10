#!/usr/bin/env python3
"""Certificate discovery; all proposed witnesses are separately checked exactly.
NumPy/SciPy are used only to propose nearest centers, not to accept coverage.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,math,time
import numpy as np
from scipy.spatial import cKDTree
HERE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(HERE))
from verify_critical import candidates,squared_comparison,verify
Q=10**14
U=F(11563027143,10**11)
source=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'discovery'/'basin_best_0.npy'
raw=np.load(source)
C=[[int(round(float(x)*Q)),int(round(float(y)*Q))] for x,y in raw]
cfg={'coordinate_denominator':Q,'centers_numerators':C,
     'radius_bound':[U.numerator,U.denominator],
     'scope':'Specific rational configuration; no claim of global optimality.'}
(HERE/'configuration.json').write_text(json.dumps(cfg,indent=2)+'\n')
cf=np.array(C,dtype=float)/Q;tree=cKDTree(cf)
def approximate(P):
    if P[0]=='R':return P[1]/P[3],P[2]/P[3]
    if P[0]=='B':
        _,u,v,h,s,d,sig=P;rt=math.sqrt(d)
        return (h*u-sig*v*rt)/s,(h*v+sig*u*rt)/s
    if P[0]=='A':
        _,ax,ay,s=P;rt=math.sqrt(s)
        return -ax/rt,-ay/rt
    raise ValueError('Unknown candidate kind')
rows=list(candidates(C,Q));coords=np.array([approximate(P) for k,P in rows])
_,proposals=tree.query(coords,k=1)
witnesses=[];fallbacks=0
for (key,P),guess in zip(rows,proposals):
    w=int(guess)
    if squared_comparison(P,C[w],Q,U*U)>0:
        fallbacks+=1
        valid=[i for i,c in enumerate(C) if squared_comparison(P,c,Q,U*U)<=0]
        if not valid:raise ValueError(f'Uncovered candidate {key}')
        w=valid[0]
    witnesses.append(w)
cert={'bound_squared':[(U*U).numerator,(U*U).denominator],
      'covering_indices':witnesses}
(HERE/'upper_certificate.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
report=verify(HERE/'configuration.json',HERE/'upper_certificate.json')
report.update({'fallback_count':fallbacks,'radius_bound':[U.numerator,U.denominator]})
(HERE/'upper_verification_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
print('PASS: independent exact checker accepted all candidates; entire disk coverage follows from the critical-point theorem.')
