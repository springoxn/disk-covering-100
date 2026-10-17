"""Conservative weighted capacity leaf. Pair/triple tests are necessary only.
No Helly sufficiency is required for soundness: allowed patterns are an overapproximation.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
import json,hashlib,copy
from n100_global_witness_tree import interval,dist1,require
R=Path(__file__).resolve().parents[1]
def d2(a,b):return sum((x-y)**2 for x,y in zip(a,b))
def triple_radius2(a,b,c):
    u,v,w=sorted((d2(a,b),d2(a,c),d2(b,c)))
    if w>=u+v:return w/4
    cross=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    require(cross!=0,'acute nonzero determinant')
    return u*v*w/(4*cross*cross)

def capacity(box,points,weights):
    B=[interval(z) for z in box];require(len(B)>=3 and len(B)%2==1 and B[-1][0]>=0,'dimension')
    n=(len(B)-1)//2;T=B[-1][1];P=[tuple(map(F,p)) for p in points];W=list(map(F,weights));k=len(P)
    require(0<k<=16 and len(W)==k and all(w>=0 for w in W),'bounded positive weights')
    require(all(len(p)==2 and sum(x*x for x in p)<=1 for p in P),'target points')
    badpairs={s for s in combinations(range(k),2) if d2(P[s[0]],P[s[1]])>4*T}
    badtriples={s for s in combinations(range(k),3) if triple_radius2(*(P[v] for v in s))>T}
    neighborhoods=[];bounds=[];counts=[]
    for j in range(n):
        allowed=[v for v,p in enumerate(P) if dist1(p[0],B[2*j])+dist1(p[1],B[2*j+1])<=T]
        best=F(0);count=0
        for mask in range(1<<len(allowed)):
            S={allowed[v] for v in range(len(allowed)) if mask>>v&1}
            if any(set(p)<=S for p in badpairs) or any(set(p)<=S for p in badtriples):continue
            count+=1;best=max(best,sum((W[v] for v in S),F(0)))
        neighborhoods.append(allowed);bounds.append(best);counts.append(count)
    total=sum(W,F(0));upper=sum(bounds,F(0))
    return {'excluded':upper<total,'total_weight':str(total),'sum_capacity_upper':str(upper),
            'strict_deficit':str(total-upper),'per_center_capacity_upper':[str(v) for v in bounds],
            'per_center_admitted_patterns':counts,'neighborhoods':neighborhoods,
            'forbidden_pairs':[list(s) for s in sorted(badpairs)],'forbidden_triples':[list(s) for s in sorted(badtriples)]}

def verify(box,points,weights):
    result=capacity(box,points,weights);require(result['excluded'],'capacity deficit absent');return result

if __name__=='__main__':
    U=F(1154469548855829,10**16);T=U*U
    box=[['-1/2','1/2'] for _ in range(198)]+[['-1','1'],['-1','1'],['0',str(T)]]
    P=[['4/5','0'],['1','0'],['9/10','9/50']];W=['1','2','3']
    result=verify(box,P,W)
    require(result['forbidden_pairs']==[] and result['forbidden_triples']==[[0,1,2]],'genuine triple obstruction')
    require(result['sum_capacity_upper']=='5' and result['total_weight']=='6','weights')
    q=[tuple(map(F,p)) for p in P];radius=triple_radius2(*q)
    require(radius==F(2809,202500) and radius>T,'exact radius')
    rejected=[]
    tests=[('extra_available_center',lambda b,p,w:b.__setitem__(196,['-1','1'])),
           ('closed_circumradius_endpoint',lambda b,p,w:b.__setitem__(-1,['0',str(radius)])),
           ('negative_weight',lambda b,p,w:w.__setitem__(0,'-1')),
           ('outside_target',lambda b,p,w:p.__setitem__(0,['2','0'])),
           ('zero_weight_no_deficit',lambda b,p,w:w.__setitem__(0,'0'))]
    for name,mutate in tests:
        b=copy.deepcopy(box);p=copy.deepcopy(P);w=copy.deepcopy(W);mutate(b,p,w)
        try:verify(b,p,w)
        except ValueError:rejected.append(name)
        else:raise RuntimeError('negative control accepted '+name)
    full=[['-1','1'] for _ in range(200)]+[['0',str(T)]]
    full_result=capacity(full,P,W);require(not full_result['excluded'] and full_result['sum_capacity_upper']=='500','full domain remains open')
    op=R/'verify/out/n100-weighted-witness-capacity.json';require(not op.exists(),'refuse overwrite')
    op.write_text(json.dumps({'schema':'n100-weighted-witness-capacity/v1','verified':True,
        'example_box':box,'points':P,'weights':W,'result':result,'circumradius_squared':str(radius),
        'full_domain_control':full_result,'rejected_controls':rejected,'arithmetic':'Fraction only',
        'scope':'restricted center box; necessary pair/triple pattern relaxation, not exact constrained MEC',
        'global_optimality':False,'minimal_polynomial_obtained':False,
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print('PASS capacity 5 < weight6, all pairs feasible, triple impossible; five controls rejected; full domain not excluded')
