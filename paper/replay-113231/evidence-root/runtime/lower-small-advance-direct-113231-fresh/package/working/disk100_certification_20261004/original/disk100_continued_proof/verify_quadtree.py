#!/usr/bin/env python3
"""Independent integer-only whole-disk coverage check by a complete quadtree."""
from pathlib import Path
from fractions import Fraction as F
import json,sys

def require(p,s):
    if not p: raise ValueError(s)

def outside(d,i,j):
    s=1<<d;ax=2*i-s;ay=2*j-s
    mx=0 if ax<=0<=ax+2 else min(abs(ax),abs(ax+2))
    my=0 if ay<=0<=ay+2 else min(abs(ay),abs(ay+2))
    return mx*mx+my*my>s*s

def covered(d,i,j,center,Q,U):
    s=1<<d;ax=2*i-s;ay=2*j-s;X,Y=center
    dx=max(abs(ax*Q-X*s),abs((ax+2)*Q-X*s))
    dy=max(abs(ay*Q-Y*s),abs((ay+2)*Q-Y*s))
    return (dx*dx+dy*dy)*U.denominator**2 <= (U.numerator*Q*s)**2

def verify(config_path,certificate_path):
    cfg=json.loads(Path(config_path).read_text())
    cert=json.loads(Path(certificate_path).read_text())
    Q=cfg['coordinate_denominator'];C=cfg['centers_numerators']
    require(type(Q) is int and Q>0,'bad coordinate denominator')
    require(len(C)==100,'expected exactly 100 centers')
    require(all(len(c)==2 and all(type(x) is int for x in c) for c in C),'bad centers')
    U=F(*cert['radius_bound'])
    require(U==F(*cfg['radius_bound']) and U>0,'wrong radius')
    codes=cert['preorder_nodes'];stack=[(0,0,0)];k=0
    counts={'split':0,'outside':0,'covered':0};depth=0
    while stack:
        d,i,j=stack.pop();depth=max(depth,d)
        require(k<len(codes),'missing nodes')
        w=codes[k];k+=1;require(type(w) is int,'noninteger node')
        if w==-2:
            counts['split']+=1
            stack.extend([(d+1,2*i+1,2*j+1),(d+1,2*i,2*j+1),
                          (d+1,2*i+1,2*j),(d+1,2*i,2*j)])
        elif w==-1:
            require(outside(d,i,j),'invalid outside leaf');counts['outside']+=1
        else:
            require(0<=w<100,'invalid center index')
            require(covered(d,i,j,C[w],Q,U),'uncovered rectangle');counts['covered']+=1
    require(k==len(codes),'extra nodes')
    require(k==4*counts['split']+1,'incomplete full quadtree')
    return {'status':'PASS','node_counts':counts,'total_nodes':k,'max_depth':depth,
            'scope':'Every point of the entire closed unit disk is covered.'}

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: verify_quadtree.py CONFIG CERTIFICATE')
    print(json.dumps(verify(sys.argv[1],sys.argv[2]),indent=2))
