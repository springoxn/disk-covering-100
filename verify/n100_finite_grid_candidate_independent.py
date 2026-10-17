"""Independent coverage-only replay: reconstruct rational points and verify assignments.
Does not recompute nearest centers or import the generator.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json
R=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def replay():
    p=R/'verify/out/n100-finite-grid-candidate-controls.json';z=json.loads(p.read_text(encoding='utf-8'))
    mpath=R/z['midpoint_path'];need(hashlib.sha256(mpath.read_bytes()).hexdigest()==z['midpoint_sha256'],'midpoint')
    m=json.loads(mpath.read_text(encoding='utf-8'));D=int(m['denominator']);v=list(map(int,m['numerators']))
    C=[(Q(v[2*j],D),Q(v[2*j+1],D)) for j in range(100)]
    lo=Q(v[492],D)-Q(1,10**58);need(lo==Q(z['squared_candidate_lower']),'root lower')
    rows=[]
    for row in z['results']:
        N=row['N'];P=[]
        for a in range(-N,N+1):
            for b in range(-N,N+1):
                if a*a+b*b<=N*N:P.append((Q(a,N),Q(b,N)))
        for turn in range(4):
            for k in range(N):
                t=Q(k,N);x=(1-t*t)/(1+t*t);y=2*t/(1+t*t)
                if turn==0:q=(x,y)
                elif turn==1:q=(-y,x)
                elif turn==2:q=(-x,-y)
                else:q=(y,-x)
                P.append(q)
        ids=row['assigned_centers'];need(len(P)==len(ids)==row['witness_count'],'count')
        T=Q(row['maximum_squared_distance']);need(0<=T<lo,'strict endpoint')
        actual=Q(0)
        for point,j in zip(P,ids):
            need(type(j) is int and 0<=j<100,'label');need(sum(x*x for x in point)<=1,'point in D')
            d=sum((x-y)**2 for x,y in zip(point,C[j]));need(d<=T,'assigned coverage');actual=max(actual,d)
        need(actual==T,'maximum attained');need(lo-T==Q(row['strict_gap_below_candidate_squared_lower']),'gap')
        rows.append({'N':N,'assignments_checked':len(P),'strict_squared_gap':str(lo-T)})
    need(hashlib.sha256((R/'verify/n100_finite_grid_candidate_controls.py').read_bytes()).hexdigest()==z['checker_sha256'],'generator')
    op=R/'verify/out/n100-finite-grid-candidate-independent.json';need(not op.exists(),'overwrite')
    op.write_text(json.dumps({'verified':True,'rows':rows,'scope':'independent assigned finite-point coverage; no nearest-center optimality or continuous coverage claim',
        'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS independent rational reconstruction, all four assigned covers strictly below candidate')
if __name__=='__main__':replay()
