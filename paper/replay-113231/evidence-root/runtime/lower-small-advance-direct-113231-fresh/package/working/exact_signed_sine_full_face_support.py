"""Exact signed-sine complete-simplex dual supports, including boundary edges.

The interval encloses the chosen support expression. Its upper bounds the
true constrained face maximum; for arbitrary nu its lower need not bound
that true constrained maximum from below.
"""
from fractions import Fraction as F
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'signed_edge_metric_20261004'))
from verify_star_lp_duals import I,q,S,PI
from exact_signed_conjugates import signed_conjugate,acos_unit

def face_bound(labels,edges,nu,area_coefficient=F(1)):
    labels=tuple(F(x) for x in labels);edges=tuple(F(x) for x in edges)
    nu=F(nu);area=F(area_coefficient)
    assert len(labels)==len(edges)==3 and area>0
    guard=area-(max(labels)-min(labels)+sum((max(-t,F(0)) for t in edges),F(0))/2)
    assert guard>0,'The full-simplex localization hypothesis failed'
    ls=tuple(x/area for x in labels);ts=tuple(x/area for x in edges);eta=nu/area
    mean=sum(ls,F(0))/3
    acute=PI*q(eta-mean)+sum((signed_conjugate(q(t),q(eta-l),True) for l,t in zip(ls,ts)),q(0))
    candidates=[acute];boundary=[]
    for k in range(3):
        i,j=[v for v in range(3) if v!=k]
        T=ts[i]+ts[j];d=ls[i]-ls[j]
        values=[PI*q(ls[j]-mean),PI*q(ls[i]-mean)]
        if T>0 and abs(d)<T:
            x=q(-d/T);assert -S<=x.l<=x.u<=S
            values.append(q(T*T-d*d).sqrt()+q(d)*acos_unit(x)+PI*q(ls[j]-mean))
        cap=I(max(v.l for v in values),max(v.u for v in values))
        boundary.append(cap);candidates.append(cap)
    total=I(max(v.l for v in candidates),max(v.u for v in candidates))
    return q(area)*total,q(area)*acute,[q(area)*z for z in boundary]

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    from verify_potential_star_duals import sine,cosine
    cases=[
      ([0,0,0],[0,0,0],F(-1,2),1),
      ([0,F(1,2),0],[0,0,F(51,100)],0,1),
      ([F(-1,3),0,F(-1,5)],[-F(1,4),F(1,4),0],F(-1,2),1),
      ([F(1,4),0,F(-1,4)],[-F(1,4),-F(1,4),F(1,4)],F(-1,2),1),
      ([F(-3,5),0,F(-1,5)],[-F(1,4)]*3,F(-1,2),1),
      ([F(3,10),0,F(-1,5)],[F(12),-F(1,4),0],0,1),
      ([F(1,4),0,F(-1,4)],[F(13),F(17),F(11)],0,1),
      ([F(-1,5),0,0],[-F(1,8),F(1,4),0],F(-1,4),F(1,2))]
    # Critical ratios may round to closed acos endpoints at this scale.
    tiny=F(1,10**80)
    for sign in (-1,1):
        face_bound([sign*F(1,2),0,0],[F(1,2)+tiny,0,0],0)
    comparisons=0
    for labels,edges,nu,area in cases:
        bound,acute,boundaries=face_bound(labels,edges,nu,area)
        assert all(bound.u>=x.u for x in [acute]+boundaries)
        for i in range(17):
            for j in range(17-i):
                angles=[PI*i/16,PI*j/16,PI*(16-i-j)/16]
                score=sum((q(area)*sine(a)*cosine(a)+q(t)*sine(a)+q(l)*(a-PI/3) for l,t,a in zip(labels,edges,angles)),q(0))
                assert score.l<=bound.u
                comparisons+=1
    rejected=0
    for args in [([0,0],[0,0,0],0,1),([0,0,0],[0,0],0,1),([0,0,0],[0,0,0],0,0),([0,1,0],[0,0,0],0,1),([0,0,0],[-2,0,0],0,1)]:
        try:face_bound(*args)
        except AssertionError:rejected+=1
        else:raise AssertionError('Invalid domain was accepted')
    return dict(status='PASS',scope='Local full-simplex support implementation only; no graph or radius exclusion',
      exact_grid_diagnostics=comparisons,negative_cases=rejected,support_cases=len(cases),
      theorem='range(labels)+sum(max(-edge,0))/2<positive area coefficient; all three edge caps included')

if __name__=='__main__':
    import json
    print(json.dumps(verify(),indent=2))
