#!/usr/bin/env python3
"""Exact finite verification of a covering of the CLOSED UNIT DISK.

Usage: python verify_cover.py centers.csv 0.11573102001
Input coordinates and radius are exact finite-decimal rationals.
This proves a configuration-specific upper bound, never global optimality.
"""
import argparse, hashlib, itertools, json, math, sys, time
from decimal import Decimal
from pathlib import Path

def surd_le_zero(a,b,q):
    """Exact a+b*sqrt(q)<=0, integer q>=0."""
    assert q>=0
    if b==0 or q==0: return a<=0
    if b>0: return a<=0 and b*b*q<=a*a
    return a<=0 or a*a<=b*b*q

def read_centers(path):
    raw=Path(path).read_text()
    if Path(path).suffix.lower()=='.json':
        rows=json.loads(raw,parse_float=str)
        if isinstance(rows,dict): rows=rows['centers']
        rows=[[str(v) for v in p] for p in rows]
    else:
        rows=[]
        for line in raw.splitlines():
            line=line.strip()
            if not line or line.startswith('#'): continue
            p=line.replace(',',' ').split()
            if len(p)==3: p=p[1:]
            if len(p)!=2: raise ValueError('Expected two coordinate columns')
            try: [Decimal(v) for v in p]
            except Exception:
                if not rows: continue
                raise
            rows.append(p)
    if not rows: raise ValueError('No centers')
    return rows,hashlib.sha256(raw.encode()).hexdigest()

def verify(rows,radius):
    start=time.monotonic()
    vals=[Decimal(str(v)) for p in rows for v in p]+[Decimal(str(radius))]
    if not all(v.is_finite() for v in vals): raise ValueError('Nonfinite input')
    if vals[-1]<0: raise ValueError('Negative radius')
    places=max(0,*[-v.as_tuple().exponent for v in vals])
    S=10**places
    def as_int(d):
        sign,digits,exp=d.as_tuple()
        v=int(''.join(map(str,digits))) if digits else 0
        return (-v if sign else v)*10**(exp+places)
    ints=[as_int(d) for d in vals]
    R=ints[-1]; R2=R*R; S2=S*S
    pts=list(dict.fromkeys(zip(ints[:-1:2],ints[1:-1:2])))
    n=len(pts); norms=[x*x+y*y for x,y in pts]
    floats=[(x/S,y/S) for x,y in pts]
    try:
        from scipy.spatial import cKDTree
        tree=cKDTree(floats)
        def guess(x,y): return int(tree.query([x/S,y/S])[1])
    except ImportError:
        def guess(x,y):
            return min(range(n),key=lambda k:(x/S-floats[k][0])**2+(y/S-floats[k][1])**2)
    counts=dict(triples=0,degenerate_triples=0,outside_triples=0,
                interior_candidates=0,boundary_pairs=0,disjoint_bisectors=0,
                boundary_candidates=0,antipodes=0,cardinal=0,exact_fallbacks=0)
    used=set(); maximum=0.; worst=None
    def accept(pred,x,y,data):
        nonlocal maximum,worst
        k=guess(x,y)
        distance=math.hypot(x/S-floats[k][0],y/S-floats[k][1])
        if distance>maximum: maximum,worst=distance,data
        if pred(k): used.add(k); return
        counts['exact_fallbacks']+=1
        for j in range(n):
            if j!=k and pred(j): used.add(j); return
        raise ValueError(json.dumps(dict(status='FAIL',uncovered_candidate=data,
                                        distance_approx=distance,counts=counts)))
    for x,y in [(S,0),(-S,0),(0,S),(0,-S)]:
        counts['cardinal']+=1
        accept(lambda k:(x-pts[k][0])**2+(y-pts[k][1])**2<=R2,
               x,y,dict(kind='cardinal',scaled_xy=[x,y]))
    for i,j,k in itertools.combinations(range(n),3):
        counts['triples']+=1
        xi,yi=pts[i]
        a,b=2*(pts[j][0]-xi),2*(pts[j][1]-yi); c=norms[j]-norms[i]
        d,e=2*(pts[k][0]-xi),2*(pts[k][1]-yi); f=norms[k]-norms[i]
        det=a*e-b*d
        if det==0: counts['degenerate_triples']+=1; continue
        xx,yy=c*e-b*f,a*f-c*d
        if det<0: det,xx,yy=-det,-xx,-yy
        if xx*xx+yy*yy>S2*det*det: counts['outside_triples']+=1; continue
        counts['interior_candidates']+=1; rhs=R2*det*det
        accept(lambda t:(xx-pts[t][0]*det)**2+(yy-pts[t][1]*det)**2<=rhs,
               xx/det,yy/det,dict(kind='circumcenter',indices=[i,j,k],
                                 scaled_numerators=[xx,yy],denominator=det))
    for i,j in itertools.combinations(range(n),2):
        counts['boundary_pairs']+=1
        a,b=2*(pts[j][0]-pts[i][0]),2*(pts[j][1]-pts[i][1])
        d=norms[j]-norms[i]; L=a*a+b*b
        assert L>0
        q=S2*L-d*d
        if q<0: counts['disjoint_bisectors']+=1; continue
        sq=math.sqrt(q)
        for sign in ([1] if q==0 else [-1,1]):
            counts['boundary_candidates']+=1
            xx,yy=(a*d-sign*b*sq)/L,(b*d+sign*a*sq)/L
            def pred(k):
                xk,yk=pts[k]
                aa=(S2+norms[k]-R2)*L-2*d*(a*xk+b*yk)
                bb=sign*(2*b*xk-2*a*yk)
                return surd_le_zero(aa,bb,q)
            accept(pred,xx,yy,dict(kind='bisector_boundary',indices=[i,j],
                                  a=a,b=b,d=d,surd_radicand=q,sign=sign))
    for i,(xi,yi) in enumerate(pts):
        qi=norms[i]
        if qi==0: continue
        counts['antipodes']+=1; sq=math.sqrt(qi)
        def pred(k):
            aa=(S2+norms[k]-R2)*qi
            bb=2*S*(xi*pts[k][0]+yi*pts[k][1])
            return surd_le_zero(aa,bb,qi)
        accept(pred,-S*xi/sq,-S*yi/sq,dict(kind='antipode',index=i))
    return dict(status='PASS',claim='The listed closed disks cover the closed unit disk.',
                radius=str(radius),input_centers=len(rows),distinct_centers=n,scale=S,
                counts=counts,witness_disks_used=len(used),
                maximum_candidate_distance_approx=maximum,worst_candidate_approx=worst,
                seconds=time.monotonic()-start,
                arithmetic='All acceptance and candidate inclusion tests use exact integers. Floats only choose witnesses and report approximations.',
                scope='Configuration-specific upper bound only; no assertion of local or global optimality.')

def self_test():
    for a,b,q,want in [(-2,1,4,True),(-2,1,5,False),(2,-1,4,True),
                       (3,-1,4,False),(-3,-1,4,True),(3,1,4,False)]:
        assert surd_le_zero(a,b,q)==want
    cases=[([['0','0']],'1',True),([['0','0']],'.999',False),
           ([['.5','0'],['-.5','0']],'1.12',True),
           ([['.5','0'],['-.5','0']],'1.11',False),
           ([['0','0'],['0','0']],'1',True),
           ([['0','0'],['0','.5'],['0','-.5']],'1',True),
           ([['.5','.5'],['-.5','.5'],['.5','-.5'],['-.5','-.5']],'.708',True),
           ([['.5','.5'],['-.5','.5'],['.5','-.5'],['-.5','-.5']],'.707',False)]
    for rows,r,want in cases:
        try: verify(rows,r); got=True
        except ValueError: got=False
        assert got==want,(rows,r,want,got)
    print(json.dumps(dict(self_test='PASS',cases=len(cases),surd_tests=6)))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('coordinates',nargs='?'); p.add_argument('radius',nargs='?')
    p.add_argument('--self-test',action='store_true'); args=p.parse_args()
    if args.self_test: self_test()
    else:
        if not args.coordinates or not args.radius: p.error('coordinates and radius required')
        rows,sha=read_centers(args.coordinates)
        try: result=verify(rows,args.radius)
        except ValueError as e: print(str(e)); sys.exit(1)
        result['input_sha256']=sha
        result['verifier_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        print(json.dumps(result,indent=2))
