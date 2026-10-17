"""Exact small-pool capacity cuts, using pair/triple minimal enclosing circles.
Closed-radius equality is retained as feasible. The geometry uses planar Helly.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def distance(p,q):return sum((a-b)**2 for a,b in zip(p,q))
def fits(points,t):
    for p,q in combinations(points,2):
        if distance(p,q)>4*t:return False
    for a,b,c in combinations(points,3):
        sides=sorted([distance(a,b),distance(a,c),distance(b,c)])
        x,y,z=sides
        if z>=x+y:continue # obtuse, right or collinear: diameter disk suffices
        cross=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        need(cross!=0,'acute collinear')
        if x*y*z>4*cross*cross*t:return False
    return True

def cut(box,raw):
    B=[tuple(map(F,z)) for z in box];P=[tuple(map(F,p)) for p in raw]
    need(len(B)%2==1 and all(len(z)==2 and z[0]<=z[1] for z in B) and B[-1][0]>=0,'box')
    need(0<len(P)<=12 and len(set(P))==len(P) and all(len(p)==2 and sum(x*x for x in p)<=1 for p in P),'pool')
    t=B[-1][1];n=(len(B)-1)//2
    masks=[s for s in range(1<<len(P)) if fits([P[i] for i in range(len(P)) if s>>i&1],t)]
    capacities=[];possible=[]
    for j in range(n):
        reach=0
        for i,p in enumerate(P):
            d=sum((lo-x)**2 if x<lo else ((x-hi)**2 if x>hi else F(0)) for x,(lo,hi) in zip(p,B[2*j:2*j+2]))
            if d<=t:reach|=1<<i
        possible.append(reach)
        capacities.append(max(s.bit_count() for s in masks if s&reach==s))
    return {'excluded':sum(capacities)<len(P),'pool_size':len(P),'capacity_sum':sum(capacities),'capacity_per_center':capacities,'reachable_masks':possible,'geometrically_feasible_masks':masks,'deficiency':len(P)-sum(capacities)}

def independent_capacity(box,raw,result):
    # Recompute using determinant/Gram form and exhaustive mask rejection.
    P=[tuple(map(F,p)) for p in raw];t=F(box[-1][1]);valid=[]
    for mask in range(1<<len(P)):
        indices=[i for i in range(len(P)) if mask>>i&1];ok=True
        ds={}
        for i,j in combinations(indices,2):
            ds[i,j]=(P[i][0]-P[j][0])**2+(P[i][1]-P[j][1])**2
            if ds[i,j]>4*t:ok=False
        for i,j,k in combinations(indices,3):
            a,b,c=ds[i,j],ds[i,k],ds[j,k]
            if 2*max(a,b,c)>=a+b+c:continue
            # Gram determinant equals squared parallelogram area.
            gram=a*b-((a+b-c)/2)**2
            if gram<=0 or a*b*c>4*t*gram:ok=False
        if ok:valid.append(mask)
    need(valid==result['geometrically_feasible_masks'],'mask mismatch')
    caps=[]
    for j in range((len(box)-1)//2):
        reach=0
        for i,p in enumerate(P):
            q=[min(max(p[d],F(box[2*j+d][0])),F(box[2*j+d][1])) for d in (0,1)]
            if sum((p[d]-q[d])**2 for d in (0,1))<=t:reach|=1<<i
        caps.append(max(sum((s>>i)&1 for i in range(len(P))) for s in valid if s&reach==s))
    need(caps==result['capacity_per_center'] and sum(caps)<len(P),'capacity mismatch or no cut')
    return {'verified':True,'independent_capacity_sum':sum(caps),'method':'Gram determinant, exhaustive masks, clamped box distance'}

def main():
    u=F(1154469548855829,10**16);t=u*u
    pool=[['13/20','0'],['17/20','0'],['3/4','19/100']]
    box=[['-1/2','1/2'] for _ in range(198)]+[['-1','1'],['-1','1'],['0',str(t)]]
    z=cut(box,pool);need(z['excluded'] and z['capacity_sum']==2 and z['deficiency']==1,'triple cut')
    points=[tuple(map(F,p)) for p in pool]
    need(all(distance(p,q)<4*t for p,q in combinations(points,2)),'pair separation control')
    independent=independent_capacity(box,pool,z)
    two=box.copy();two[196:198]=[['-1','1'],['-1','1']]
    c=cut(two,pool);need(not c['excluded'],'two-center control')
    full=[['-1','1'] for _ in range(200)]+[['0',str(t)]]
    need(not cut(full,pool)['excluded'],'full domain control')
    # Exactly on the closed radius, antipodal pair is feasible.
    need(fits([(F(-1),F(0)),(F(1),F(0))],F(1)),'closed endpoint')
    rejected=[]
    for label,mutate in [('false_triple_feasibility',lambda q:q['geometrically_feasible_masks'].append(7)),('understated_capacity',lambda q:q['capacity_per_center'].__setitem__(99,1))]:
        q=json.loads(json.dumps(z));mutate(q)
        try:independent_capacity(box,pool,q)
        except ValueError:rejected.append(label)
    need(len(rejected)==2,'negative controls')
    result={'schema':'n100-nonseparated-capacity-cut/v1','verified':True,'radius_upper':str(u),'points':pool,'root_box':box,'result':z,'independent':independent,
        'all_pairs_can_fit_in_one_disk':True,'triple_cannot_fit_in_one_disk':True,
        'two_available_centers_not_excluded':True,'full_center_domain_not_excluded':True,'closed_radius_pair_retained':True,'negative_controls_rejected':rejected,
        'arithmetic':'integer/Fraction only','analytic_dependencies':['planar Helly for intersections of congruent center disks','minimal enclosing disk of three points: diameter if nonacute, otherwise circumcircle','finite capacity subadditivity'],
        'scope':'restricted 100-center box; arbitrary small nonseparated pool capacity implementation; no surviving count family excluded',
        'machine_verified_geometry':False,'global_optimality':False,'minimal_polynomial_obtained':False,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=ROOT/'verify/out/n100-nonseparated-capacity-cut.json';need(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('PASS nonseparated 3-point capacity cut: all pairs feasible, triple infeasible; independent Gram replay; two-center/full-domain/closed-endpoint controls; 2 corruptions rejected')
if __name__=='__main__':main()
