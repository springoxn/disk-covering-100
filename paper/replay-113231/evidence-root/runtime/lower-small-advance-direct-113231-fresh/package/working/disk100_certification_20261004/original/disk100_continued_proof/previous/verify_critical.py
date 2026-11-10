#!/usr/bin/env python3
"""Exhaustive exact critical-point coverage checker. Python standard library only.

No floats are used in this module. All possible non-collinear triple
circumcenters, all pair-bisector/unit-circle intersections, and all antipodes
are enumerated. A certificate supplies one covering-center index for each.
The accompanying proof explains why this covers the whole closed disk.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json,sys

def require(ok,msg):
    if not ok: raise ValueError(msg)

def sign_surd(a,b,d):
    """Exact sign of a+b*sqrt(d), for integers a,b and d>=0."""
    require(d>=0,'negative radicand')
    if b==0 or d==0:return (a>0)-(a<0)
    if a==0:return (b>0)-(b<0)
    if a>0 and b>0:return 1
    if a<0 and b<0:return -1
    diff=a*a-b*b*d
    if a>0:return (diff>0)-(diff<0)
    return (diff<0)-(diff>0)

def candidates(C,Q):
    # Types R: rational point (nx/den,ny/den);
    # B: intersection u*x+v*y=h with x^2+y^2=1;
    # A: antipode -C_i/||C_i||.
    for i,j,k in combinations(range(len(C)),3):
        ax,ay=C[i];ux,uy=C[j][0]-ax,C[j][1]-ay
        vx,vy=C[k][0]-ax,C[k][1]-ay
        det=ux*vy-uy*vx
        if det==0:continue
        u2=ux*ux+uy*uy;v2=vx*vx+vy*vy
        nx=2*det*ax+u2*vy-v2*uy
        ny=2*det*ay+ux*v2-vx*u2
        den=2*det*Q
        if den<0:nx,ny,den=-nx,-ny,-den
        if nx*nx+ny*ny<=den*den:
            yield ('T',i,j,k),('R',nx,ny,den)
    for i,j in combinations(range(len(C)),2):
        ax,ay=C[i];bx,by=C[j]
        u=2*Q*(ax-bx);v=2*Q*(ay-by)
        s=u*u+v*v;h=ax*ax+ay*ay-bx*bx-by*by
        require(s>0,'duplicate centers')
        d=s-h*h
        if d<0:continue
        for sig in (-1,1):
            yield ('B',i,j,sig),('B',u,v,h,s,d,sig)
    for i,(ax,ay) in enumerate(C):
        s=ax*ax+ay*ay
        if s>0:yield ('A',i),('A',ax,ay,s)
    yield ('E',),('R',1,0,1)

def squared_comparison(P,center,Q,bound):
    """Sign of (distance squared - rational bound)."""
    X,Y=center; N,D=bound.numerator,bound.denominator
    if P[0]=='R':
        _,nx,ny,den=P
        z=D*((Q*nx-X*den)**2+(Q*ny-Y*den)**2)-N*Q*Q*den*den
        return (z>0)-(z<0)
    if P[0]=='B':
        _,u,v,h,s,d,sig=P
        a=s*(Q*Q+X*X+Y*Y)-2*Q*h*(X*u+Y*v)
        b=2*Q*sig*(X*v-Y*u)
        den=s*Q*Q
    elif P[0]=='A':
        _,ax,ay,s=P
        a=s*(Q*Q+X*X+Y*Y)
        b=2*Q*(ax*X+ay*Y)
        d=s;den=s*Q*Q
    else:raise ValueError('unknown candidate type')
    return sign_surd(D*a-N*den,D*b,d)

def rational_dist2(P,center,Q):
    require(P[0]=='R','not a rational point')
    _,nx,ny,den=P;X,Y=center
    return F((Q*nx-X*den)**2+(Q*ny-Y*den)**2,Q*Q*den*den)

def verify(config_path,cert_path):
    cfg=json.loads(Path(config_path).read_text())
    cert=json.loads(Path(cert_path).read_text())
    Q=cfg['coordinate_denominator'];C=cfg['centers_numerators']
    require(type(Q) is int and Q>0,'bad coordinate denominator')
    require(len(C)==100,'expected 100 centers')
    require(all(len(c)==2 and all(type(z) is int for z in c) for c in C),'bad centers')
    require(len({tuple(c) for c in C})==100,'duplicate centers')
    bound=F(*cert['bound_squared'])
    require(bound>0,'nonpositive bound')
    witnesses=cert['covering_indices']
    exc=tuple(cert.get('exception',[]))
    rad2=F(*cert['exact_radius_squared']) if exc else None
    if exc:
        require(bound<rad2,'strict comparison threshold is not below exact radius')
        lo=F(*cert['root_interval'][0]);hi=F(*cert['root_interval'][1])
        require(0<lo<hi and lo*lo<rad2<hi*hi,'invalid positive root isolation')
    counts={'T':0,'B':0,'A':0,'E':0};seen=0;exception_seen=0
    for key,P in candidates(C,Q):
        require(seen<len(witnesses),'truncated certificate')
        w=witnesses[seen];seen+=1;counts[key[0]]+=1
        require(type(w) is int,'noninteger covering index')
        if w==-1:
            require(exc and key==exc,'unexpected exception')
            exception_seen+=1
            require(rational_dist2(P,C[key[1]],Q)==rad2,'wrong exact radius')
            signs=[squared_comparison(P,c,Q,rad2) for c in C]
            require(all(s>=0 for s in signs),'exception not a hole of claimed radius')
            require([i for i,s in enumerate(signs) if s==0]==list(key[1:]),'unexpected tied center at the maximum')
            require(rad2<1,'uniqueness proof requires radius below 1')
        else:
            require(0<=w<100,'covering index out of range')
            require(squared_comparison(P,C[w],Q,bound)<=0,f'uncovered candidate {key}')
    require(seen==len(witnesses),'extra certificate entries')
    require(exception_seen==(1 if exc else 0),'missing/duplicate exception')
    return {'candidate_counts':counts,'total':seen,'exact_radius_squared':str(rad2) if exc else None,
            'upper_squared':str(bound),'unique_worst_candidate':list(exc) if exc else None}

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: python verify_critical.py CONFIG CERTIFICATE')
    print(json.dumps(verify(sys.argv[1],sys.argv[2]),indent=2))
    print('PASS: exhaustive exact arithmetic checks completed.')
