"""Boundary root-hole cycle and whole-arc nearest-owner audit.
Exact equalities at active endpoints rely on the accepted KKT equations.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1];S='runtime/external-disk100-strict-local-replay/source/'
def need(x,m):
    if not x:raise ValueError(m)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[1],a[1]-b[0]
def mul(a,b):
    z=[x*y for x in a for y in b];return min(z),max(z)
def sq(a):return (F(0) if a[0]<=0<=a[1] else min(a[0]**2,a[1]**2),max(a[0]**2,a[1]**2))
def norm(p):return add(sq(p[0]),sq(p[1]))
def cross(a,b):return sub(mul(a[0],b[1]),mul(a[1],b[0]))
def dot(a,b):return add(mul(a[0],b[0]),mul(a[1],b[1]))
def scale(a,v):return mul(a,(F(v),F(v)))
def main():
    load=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
    m=load(S+'rational_midpoint.json');k=load(S+'krawczyk_verification.json');s=load(S+'polynomial_system.json');t=load(S+'algebraic_cover_topology.json');inv=load('verify/out/n100-full-circumcenter-root-box.json')
    for p,h in inv['bindings'].items():need(hashlib.sha256((R/p).read_bytes()).hexdigest()==h,'inventory binding')
    need(k['verified'] and k['box_radius']==[1,10**58],'root');D=int(m['denominator']);rho=F(*k['box_radius']);x=[(F(int(v),D)-rho,F(int(v),D)+rho) for v in m['numerators']];C=[x[2*j:2*j+2] for j in range(100)];Q=[x[428+2*h:430+2*h] for h in range(32)]
    pairs=s['boundary_active_pairs'];order=t['boundary_order'];need(sorted(order)==list(range(32)),'boundary order')
    rows=[];checks=0;line_margins=[];endpoint_gaps=[]
    for h,pair in enumerate(pairs):
        a,b=pair;d=[sub(C[b][v],C[a][v]) for v in (0,1)];D2=norm(d);rhs=scale(sub(norm(C[b]),norm(C[a])),F(1,2))
        # Bisector d.q=rhs crosses the unit circle twice iff |d|²>rhs².
        gap=D2[0]-sq(rhs)[1];need(gap>0,'bisector tangent/empty');line_margins.append(gap)
    for h,j in zip(order,order[1:]+order[:1]):
        A,B=Q[h],Q[j];need(cross(A,B)[0]>0,'CCW short arc')
        # Positive dot implies angle below pi/2; starting point has opposite terminal half-plane.
        need(dot(A,B)[0]>0,'short arc angle')
        owner=set(pairs[h])&set(pairs[j]);need(len(owner)==1,'shared owner');owner=next(iter(owner))
        branches={'endpoint_max':0,'global_support_bound':0}
        for other in range(100):
            if other==owner:continue
            d=[sub(C[other][v],C[owner][v]) for v in (0,1)]
            rhs=scale(sub(norm(C[other]),norm(C[owner])),F(1,2))
            for hole,P in ((h,A),(j,B)):
                if other in pairs[hole]:continue # exact equality from accepted active equations
                gap=sub(rhs,dot(d,P))[0];need(gap>0,'endpoint nearest');endpoint_gaps.append(gap)
            # Positive linear functional max on a short unit arc is at an endpoint unless its
            # positive direction d lies inside the wedge. Certify exclusion by one strict cross.
            if cross(A,d)[1]<0 or cross(d,B)[1]<0:
                branches['endpoint_max']+=1
            else:
                need(rhs[0]>0 and sq(rhs)[0]>norm(d)[1],'interior support bound')
                branches['global_support_bound']+=1
            checks+=1
        rows.append({'from_hole':h,'to_hole':j,'owner_center':owner,'cross_lower':str(cross(A,B)[0]),'dot_lower':str(dot(A,B)[0]),'competitor_branches':branches})
    # Winding exactly1 certified by quadrants, ordered after first-quadrant starting point.
    def quadrant(P):
        a,b=P
        if a[0]>0 and b[0]>0:return 0
        if a[1]<0 and b[0]>0:return 1
        if a[1]<0 and b[1]<0:return 2
        if a[0]>0 and b[1]<0:return 3
        raise ValueError('axis straddling')
    quadrants=[quadrant(Q[h]) for h in order];need(quadrants==sorted(quadrants) and set(quadrants)=={0,1,2,3},'single winding')
    op=R/'verify/out/n100-boundary-pair-intersections.json';need(not op.exists(),'overwrite')
    paths=[S+'rational_midpoint.json',S+'krawczyk_verification.json',S+'polynomial_system.json',S+'algebraic_cover_topology.json','verify/out/n100-full-circumcenter-root-box.json']
    op.write_text(json.dumps({'verified':True,'cycle_order':order,'quadrants':quadrants,'rows':rows,'whole_arc_competitor_checks':checks,
        'minimum_bisector_circle_discriminant_margin':str(min(line_margins)),'minimum_non_support_endpoint_gap':str(min(endpoint_gaps)),
        'analytic_dependency':'active KKT root equations give exact circle and equal-distance endpoints; short-arc linear maximum lemma gives whole-arc Voronoi ownership',
        'scope':'full candidate root-box boundary ownership cycle; no enumeration of other configurations',
        'bindings':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in paths},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS 32 bisectors meet circle twice;32 CCW arcs,3168 whole-arc nearest-owner comparisons;winding1')
if __name__=='__main__':main()
