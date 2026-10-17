"""Independent MEC by explicit singleton/diameter/circumcenter candidate circles."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
p=R/'verify/out/n100-weighted-witness-capacity.json';data=json.loads(p.read_text(encoding='utf-8'))
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sq(a,b):return (a[0]-b[0])**2+(a[1]-b[1])**2
def mec(S):
    if not S:return Q(0)
    candidates=[(a,Q(0)) for a in S]
    for a,b in combinations(S,2):
        c=((a[0]+b[0])/2,(a[1]+b[1])/2);candidates.append((c,sq(c,a)))
    for a,b,c in combinations(S,3):
        ux,uy=b[0]-a[0],b[1]-a[1];vx,vy=c[0]-a[0],c[1]-a[1]
        D=2*(ux*vy-uy*vx)
        if D==0:continue
        L=ux*ux+uy*uy;M=vx*vx+vy*vy
        center=(a[0]+(L*vy-M*uy)/D,a[1]+(ux*M-vx*L)/D)
        candidates.append((center,sq(center,a)))
    feasible=[r for c,r in candidates if all(sq(c,a)<=r for a in S)]
    need(bool(feasible),'circle candidates');return min(feasible)
P=[tuple(map(Q,z)) for z in data['points']];W=list(map(Q,data['weights']))
T=Q(data['example_box'][-1][1]);radii=[];capacity=Q(0)
for mask in range(1<<len(P)):
    ids=[j for j in range(len(P)) if mask>>j&1];r=mec([P[j] for j in ids])
    radii.append({'subset':ids,'minimum_radius_squared':str(r),'fits':r<=T})
    if r<=T:capacity=max(capacity,sum((W[j] for j in ids),Q(0)))
need(capacity==5 and sum(W)==6,'capacity')
need(mec(P)==Q(2809,202500)>T,'triple radius')
need(all(mec(list(S))<=T for S in combinations(P,2)),'pairs all fit')
# First99 boxes cannot reach any of the witnesses using a separate x-only bound.
need(all((a-Q(1,2))**2>T for a,b in P),'first99 service exclusion')
need(mec([(Q(0),Q(0)),(Q(0),Q(0)),(Q(1),Q(0))])==Q(1,4),'repeated collinear')
need(mec([(Q(0),Q(0)),(Q(2),Q(0)),(Q(1),Q(1,2))])==1,'obtuse diameter')
need(hashlib.sha256((R/'verify/n100_weighted_witness_capacity.py').read_bytes()).hexdigest()==data['checker_sha256'],'primary binding')
out=R/'verify/out/n100-weighted-witness-capacity-independent.json';need(not out.exists(),'overwrite')
out.write_text(json.dumps({'verified':True,'method':'explicit candidate circle centers, not side-product inequality',
    'subsets_checked':radii,'maximum_weight_of_feasible_subset':'5','total_weight':'6',
    'first99_boxes_excluded_by_x_only':True,'degenerate_controls_passed':True,
    'scope':'independent verification of saved three-point example; no universal constrained-capacity implementation audit',
    'global_optimality':False,'minimal_polynomial_obtained':False,
    'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
    'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
print('PASS independent explicit MEC construction, eight subsets, capacity5, total6, repeated/obtuse controls')
