"""Complete circumcenter inventory over the accepted exact KKT root box."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1];S='runtime/external-disk100-strict-local-replay/source/'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    z=[x*y for x in a for y in b];return min(z),max(z)
def div(a,b):
    need(b[0]>0 or b[1]<0,'zero denominator');return mul(a,tuple(sorted((1/b[0],1/b[1]))))
def sq(a):return (F(0) if a[0]<=0<=a[1] else min(x*x for x in a),max(x*x for x in a))
def norm(p):return add(sq(p[0]),sq(p[1]))
def scale(a,k):return mul(a,(F(k),F(k)))
def circum(A,B,C):
    u=[sub(B[d],A[d]) for d in range(2)];v=[sub(C[d],A[d]) for d in range(2)]
    det=scale(sub(mul(u[0],v[1]),mul(u[1],v[0])),2)
    U,V=norm(u),norm(v)
    q=[add(A[0],div(sub(mul(U,v[1]),mul(V,u[1])),det)),
       add(A[1],div(sub(mul(u[0],V),mul(v[0],U)),det))]
    return q,det

def main():
    load=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
    m=load(S+'rational_midpoint.json');k=load(S+'krawczyk_verification.json');t=load(S+'algebraic_cover_topology.json');s=load(S+'polynomial_system.json');b=load('verify/out/n100-local-widened-budget.json')
    need(k['verified'] and k['box_radius']==[1,10**58],'root receipt')
    for p in (S+'rational_midpoint.json',S+'polynomial_system.json'):need(hashlib.sha256((R/p).read_bytes()).hexdigest()==b['dependencies_sha256'][p],'budget binding')
    D=int(m['denominator']);rho=F(*k['box_radius']);x=[(F(int(v),D)-rho,F(int(v),D)+rho) for v in m['numerators']]
    C=[x[2*j:2*j+2] for j in range(100)];T=x[492];active={tuple(sorted(z)) for z in s['internal_active_triangles']}
    rows=[];inside=outside=inactive=0;empty_min=None;slack_min=None
    for index,tri in enumerate(t['triangles']):
        a,c,d=tri;q,det=circum(C[a],C[c],C[d]);N=norm(q);rad=norm([sub(q[z],C[a][z]) for z in range(2)])
        if N[1]<1:kind='inside';inside+=1
        elif N[0]>1:kind='outside';outside+=1
        else:raise ValueError('undecided disk classification')
        isactive=tuple(sorted(tri)) in active;slack=None
        if kind=='inside' and not isactive:
            slack=T[0]-rad[1];need(slack>0,'inactive radius slack');inactive+=1;slack_min=slack if slack_min is None else min(slack_min,slack)
        if isactive:need(kind=='inside' and rad[0]<=T[1] and rad[1]>=T[0],'active radius consistency')
        gap=None
        for j in range(100):
            if j in tri:continue
            G=norm([sub(q[z],C[j][z]) for z in range(2)])[0]-rad[1]
            need(G>0,'empty circle gap');gap=G if gap is None else min(gap,G)
        empty_min=gap if empty_min is None else min(empty_min,gap)
        rows.append({'triangle_index':index,'support':tri,'kind':kind,'active':isactive,
                     'circumcenter_box':[[str(v) for v in I] for I in q],
                     'determinant_interval':[str(v) for v in det],'norm_squared_interval':[str(v) for v in N],
                     'radius_squared_interval':[str(v) for v in rad],'empty_circle_gap_lower':str(gap),
                     'inactive_radius_slack_lower':str(slack) if slack is not None else None})
    need((inside,outside,inactive)==(166,12,52),'counts')
    rejected=[]
    try:div((F(1),F(1)),(F(-1),F(1)))
    except ValueError:rejected.append('denominator_crosses_zero')
    need(len(rejected)==1,'control')
    op=R/'verify/out/n100-full-circumcenter-root-box.json';need(not op.exists(),'overwrite')
    paths=[S+'rational_midpoint.json',S+'krawczyk_verification.json',S+'algebraic_cover_topology.json',S+'polynomial_system.json','verify/out/n100-local-widened-budget.json']
    op.write_text(json.dumps({'verified':True,'root_box_radius':str(rho),'inside_count':inside,'outside_count':outside,
        'inactive_inside_count':inactive,'active_inside_count':114,'other_center_tests':178*97,
        'minimum_empty_circle_gap_lower':str(empty_min),'minimum_inactive_squared_radius_slack':str(slack_min),
        'rows':rows,'rejected_controls':rejected,'scope':'all178 circumcenters over the accepted root box; does not build clipped map or exclude other configurations',
        'bindings':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in paths},
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS full root box:166 inside,12 outside,52 inactive slack positive,17266 strict empty-circle tests')
if __name__=='__main__':main()
