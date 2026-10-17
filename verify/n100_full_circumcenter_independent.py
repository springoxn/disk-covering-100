"""Independent absolute-coordinate interval solve of all circumcenters.
No import of the relative-coordinate primary implementation.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
R=Path(__file__).resolve().parents[1];S='runtime/external-disk100-strict-local-replay/source/'
def need(x,m):
    if not x:raise ValueError(m)
def plus(a,b):return a[0]+b[0],a[1]+b[1]
def minus(a,b):return a[0]-b[1],a[1]-b[0]
def product(a,b):
    return min(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]),max(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
def square(a):return (0 if a[0]<=0<=a[1] else min(a[0]**2,a[1]**2),max(a[0]**2,a[1]**2))
def divide(a,b):
    need(not b[0]<=0<=b[1],'singular');return product(a,(1/b[1],1/b[0]))
def norm(a):return plus(square(a[0]),square(a[1]))
def main():
    p=R/'verify/out/n100-full-circumcenter-root-box.json';z=json.loads(p.read_text(encoding='utf-8'))
    for path,h in z['bindings'].items():need(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,path)
    need(hashlib.sha256((R/'verify/n100_full_circumcenter_root_box.py').read_bytes()).hexdigest()==z['checker_sha256'],'primary script')
    m=json.loads((R/(S+'rational_midpoint.json')).read_text(encoding='utf-8'));D=int(m['denominator']);rho=Q(z['root_box_radius']);x=[(Q(int(v),D)-rho,Q(int(v),D)+rho) for v in m['numerators']];C=[x[2*j:2*j+2] for j in range(100)];T=x[492]
    counts={'inside':0,'outside':0,'inactive':0};gaps=[];slacks=[];inverse=[]
    for row in z['rows']:
        a,b,c=row['support'];A,B,V=C[a],C[b],C[c]
        # Equidistance: 2(B-A).q=|B|²-|A|²; 2(V-A).q=|V|²-|A|².
        u=[product((Q(2),Q(2)),minus(B[d],A[d])) for d in (0,1)]
        v=[product((Q(2),Q(2)),minus(V[d],A[d])) for d in (0,1)]
        rhs1=minus(norm(B),norm(A));rhs2=minus(norm(V),norm(A))
        det=minus(product(u[0],v[1]),product(u[1],v[0]))
        q=[divide(minus(product(rhs1,v[1]),product(rhs2,u[1])),det),
           divide(minus(product(u[0],rhs2),product(v[0],rhs1)),det)]
        N=norm(q);rad=norm([minus(q[d],A[d]) for d in (0,1)])
        if N[1]<1:kind='inside'
        elif N[0]>1:kind='outside'
        else:raise ValueError('classification uncertain')
        need(kind==row['kind'],'classification agreement');counts[kind]+=1
        if kind=='inside' and not row['active']:
            slack=T[0]-rad[1];need(slack>0,'inactive slack');slacks.append(slack);counts['inactive']+=1
        for j in range(100):
            if j in row['support']:continue
            gap=norm([minus(q[d],C[j][d]) for d in (0,1)])[0]-rad[1];need(gap>0,'empty circle');gaps.append(gap)
    need(counts=={'inside':166,'outside':12,'inactive':52} and len(gaps)==17266,'counts')
    out=R/'verify/out/n100-full-circumcenter-independent.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'verified':True,'counts':counts,'other_center_tests':len(gaps),
      'independent_min_empty_gap':str(min(gaps)),'independent_min_inactive_slack':str(min(slacks)),
      'method':'independently implemented absolute-coordinate interval linear solve, rather than primary relative-coordinate formula',
      'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'scope':'complete candidate circumcenter root-box inventory; no clipped-map/global enumeration',
      'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS independent absolute-coordinate solve:166 inside,12 outside,52 inactive positive;17266 empty-circle inequalities')
if __name__=='__main__':main()
