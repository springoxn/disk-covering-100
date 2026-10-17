"""Independent exact boundary audit using midpoint-radius error bounds.
Analytic trigonometric linear maximum lemma remains a reviewed dependency.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parents[1];S='runtime/external-disk100-strict-local-replay/source/'
def need(x,m):
    if not x:raise ValueError(m)
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def product_error(a,ea,b,eb):return abs(a)*eb+abs(b)*ea+ea*eb

def verify_order(order,P):
    need(sorted(order)==list(range(32)),'order permutation')
    for a,b in zip(order,order[1:]+order[:1]):need(cross(P[a],P[b])>0 and dot(P[a],P[b])>0,'order reversal')

if __name__=='__main__':
    p=R/'verify/out/n100-boundary-pair-intersections.json';z=json.loads(p.read_text(encoding='utf-8'))
    for path,h in z['bindings'].items():need(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'source binding')
    need(hashlib.sha256((R/'verify/n100_boundary_pair_intersections.py').read_bytes()).hexdigest()==z['checker_sha256'],'primary script')
    m=json.loads((R/(S+'rational_midpoint.json')).read_text(encoding='utf-8'));s=json.loads((R/(S+'polynomial_system.json')).read_text(encoding='utf-8'));D=int(m['denominator']);v=[F(int(n),D) for n in m['numerators']];r=F(1,10**58);C=[v[2*j:2*j+2] for j in range(100)];P=[v[428+2*j:430+2*j] for j in range(32)];pairs=s['boundary_active_pairs'];order=z['cycle_order'];verify_order(order,P)
    def cross_bound(A,ea,B,eb):
        e=product_error(A[0],ea,B[1],eb)+product_error(A[1],ea,B[0],eb)
        return cross(A,B)-e,cross(A,B)+e
    tested=0;slacks=[]
    for a,b in zip(order,order[1:]+order[:1]):
        need(cross_bound(P[a],r,P[b],r)[0]>0,'interval arc order')
        doterr=sum(product_error(P[a][k],r,P[b][k],r) for k in (0,1));need(dot(P[a],P[b])-doterr>0,'interval short arc')
        owner=set(pairs[a])&set(pairs[b]);need(len(owner)==1,'owner');owner=next(iter(owner))
        for j in range(100):
            if j==owner:continue
            d=[C[j][k]-C[owner][k] for k in (0,1)]
            K=(dot(C[j],C[j])-dot(C[owner],C[owner]))/2
            errK=sum(2*abs(C[l][k])*r+r*r for l in (j,owner) for k in (0,1))/2
            for h in (a,b):
                if j in pairs[h]:continue
                e=errK+sum(product_error(d[k],2*r,P[h][k],r) for k in (0,1))
                margin=K-dot(d,P[h])-e;need(margin>0,'endpoint competitor');slacks.append(margin)
            if cross_bound(P[a],r,d,2*r)[1]<0 or cross_bound(d,2*r,P[b],r)[1]<0:pass
            else:
                normupper=sum((abs(x)+2*r)**2 for x in d)
                need(K-errK>0 and (K-errK)**2>normupper,'whole arc support bound')
            tested+=1
    rejected=[]
    for name,o in [('reversed_cycle',list(reversed(order))),('repeated_hole',[order[0]]+order[:-1])]:
        try:verify_order(o,P)
        except ValueError:rejected.append(name)
        else:raise RuntimeError('negative order accepted')
    need(tested==3168,'competitor count')
    out=R/'verify/out/n100-boundary-owner-independent.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'verified':True,'whole_arc_checks':tested,'minimum_endpoint_margin':str(min(slacks)),
        'method':'midpoint plus explicit coordinate error, independent of primary interval arithmetic',
        'rejected_controls':rejected,'analytic_dependency':'short unit arc positive linear support maximum; exact active endpoint equalities from accepted KKT root',
        'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS independent root-box ownership error bounds,3168 comparisons,two malformed cycles rejected')
