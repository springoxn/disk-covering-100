"""Exact separated-witness Hall leaf: no symmetry or contact graph assumption."""
from fractions import Fraction as F
from pathlib import Path
import json,copy,hashlib
from n100_global_witness_tree import interval,dist1,require
R=Path(__file__).resolve().parents[1]
def verify(box,points):
    B=[interval(v) for v in box];require(len(B)%2==1 and B[-1][0]>=0,'dimension/radius')
    n=(len(B)-1)//2;T=B[-1][1];P=[tuple(map(F,p)) for p in points]
    require(len(P)>0 and all(len(p)==2 and sum(v*v for v in p)<=1 for p in P),'points in D')
    for i,p in enumerate(P):
        for q in P[:i]:require(sum((a-b)**2 for a,b in zip(p,q))>4*T,'pair not strictly separated')
    neighborhoods=[]
    for p in P:
        neighborhoods.append([j for j in range(n) if dist1(p[0],B[2*j])+dist1(p[1],B[2*j+1])<=T])
    union=sorted(set(j for row in neighborhoods for j in row))
    require(len(union)<len(P),'Hall deficiency absent')
    return {'verified':True,'points':len(P),'possible_centers':union,'neighborhoods':neighborhoods,
            'deficiency':len(P)-len(union),'squared_radius_upper':str(T)}
if __name__=='__main__':
    U=F(1154469548855829,10**16);T=U*U
    # Each witness has a possible serving center, yet one disk cannot serve both.
    box=[['-1/2','1/2'] for _ in range(198)]+[['-1','1'],['-1','1'],['0',str(T)]]
    points=[['-1','0'],['1','0']];result=verify(box,points)
    require(result['neighborhoods']==[[99],[99]],'expected broad-box Hall case')
    rejected=[]
    cases=[('two_available_centers',lambda b,p:b.__setitem__(196,['-1','1'])),
           ('pair_can_share_at_closed_endpoint',lambda b,p:b.__setitem__(-1,['0','1'])),
           ('outside_target',lambda b,p:p.__setitem__(0,['-2','0'])),
           ('duplicate_point',lambda b,p:p.__setitem__(1,['-1','0'])),
           ('radius_too_large_for_clustering',lambda b,p:b.__setitem__(-1,['0','1/4']))]
    for name,change in cases:
        b=copy.deepcopy(box);p=copy.deepcopy(points);change(b,p)
        try:verify(b,p)
        except ValueError:rejected.append(name)
        else:raise RuntimeError('accepted corruption '+name)
    # Independent sufficient bound: 99 centers have |x|<=1/2, distance to both endpoints >=1/2.
    require(T<F(1,4) and 4>4*T,'independent geometric margins')
    op=R/'verify/out/n100-separated-witness-hall.json';require(not op.exists(),'refuse overwrite')
    op.write_text(json.dumps({'schema':'n100-separated-witness-hall/v1','verified':True,
        'example_box':box,'example_points':points,'result':result,'rejected_controls':rejected,
        'independent_example_bounds':{'first_99_distance_squared_lower':'1/4','witness_pair_distance_squared':'4'},
        'arithmetic':'Fraction only','scope':'specified broad 100-center box; no complete global tree',
        'global_optimality':False,'minimal_polynomial_obtained':False,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print('PASS Hall leaf: two witnesses each reachable, one possible center, deficiency1; five corruptions rejected')
