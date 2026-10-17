"""Integer finite-grid covering controls at the actual candidate midpoint.
Only finite witness coverage is claimed, never continuous coverage.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1]
MP='runtime/external-disk100-strict-local-replay/source/rational_midpoint.json'
def points(N):
    for i in range(-N,N+1):
        for j in range(-N,N+1):
            if i*i+j*j<=N*N:yield ('grid',i,j),(i,j,N)
    # Rational unit-circle points in all quadrants, including axes.
    for turn in range(4):
        for k in range(N):
            a,b,d=N*N-k*k,2*N*k,N*N+k*k
            for _ in range(turn):a,b=-b,a
            yield ('circle',turn,k),(a,b,d)
def main():
    m=json.loads((R/MP).read_text(encoding='utf-8'));D=int(m['denominator']);X=list(map(int,m['numerators']));C=list(zip(X[:200:2],X[1:200:2]))
    b=json.loads((R/'verify/out/n100-local-widened-budget.json').read_text(encoding='utf-8'))
    if hashlib.sha256((R/MP).read_bytes()).hexdigest()!=b['dependencies_sha256'][MP]:raise ValueError('root binding')
    # Krawczyk coordinate rho=1e-58 equals100/D for this midpoint.
    if D!=10**60:raise ValueError('denominator')
    lower=F(X[492]-100,D)
    results=[]
    for N in (16,32,64,128):
        assignments=[];maximum=F(0);worst=None
        for label,(a,c,d) in points(N):
            distances=[(a*D-d*u)**2+(c*D-d*v)**2 for u,v in C]
            j=min(range(100),key=distances.__getitem__);val=F(distances[j],D*D*d*d)
            if val>maximum:maximum=val;worst=list(label)
            assignments.append(j)
        if not maximum<lower:raise ValueError('finite set not strictly below root')
        results.append({'N':N,'witness_count':len(assignments),'assigned_centers':assignments,
            'maximum_squared_distance':str(maximum),'worst_point_label':worst,
            'strict_gap_below_candidate_squared_lower':str(lower-maximum)})
        print('PASS N=',N,'points=',len(assignments),'finite radius squared strictly below candidate root')
    op=R/'verify/out/n100-finite-grid-candidate-controls.json'
    if op.exists():raise FileExistsError(op)
    op.write_text(json.dumps({'verified':True,'results':results,'squared_candidate_lower':str(lower),
        'midpoint_path':MP,'midpoint_sha256':hashlib.sha256((R/MP).read_bytes()).hexdigest(),
        'budget_sha256':hashlib.sha256((R/'verify/out/n100-local-widened-budget.json').read_bytes()).hexdigest(),
        'arithmetic':'integers and Fraction only','scope':'these four explicit finite witness sets admit100-disk covers strictly below the candidate radius; no continuous coverage or global lower bound',
        'global_optimality':False,'minimal_polynomial_obtained':False,
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
