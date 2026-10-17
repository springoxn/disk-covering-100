"""Independent integer-distance verification of ownership counterexample."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
p=R/'verify/out/n100-disconnected-boundary-owner-counterexample.json';z=json.loads(p.read_text(encoding='utf-8'));D=1300
A=(1287,0);B=(1300,0);points=[(1292,-144),(1300,0),(1292,144)]
def n2(P):return P[0]*P[0]+P[1]*P[1]
def d2(P,C):return (P[0]-C[0])**2+(P[1]-C[1])**2
a,b=1154469548855829,10**16
for i,P in enumerate(points):
    need(n2(P)==D*D,'circle')
    need((d2(P,A)<d2(P,B)) if i!=1 else (d2(P,B)<d2(P,A)),'owner')
    need(d2(P,A)*b*b<a*a*D*D,'A covers including middle')
need(2*1292<199*D//100,'cut')
need(z['nearest_owner_sequence_on_three_points']==['A','B','A'],'claimed owners')
# A squared distance along the short arc is D²+|A|²-2 Ax X,
# hence largest at smallest X=1292. Circle short arc has X>=1292.
need(D*D+n2(A)-2*A[0]*1292==d2(points[0],A),'arc maximum')
for path,h in z['bindings'].items():need(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'binding')
op=R/'verify/out/n100-disconnected-boundary-owner-independent.json';need(not op.exists(),'overwrite')
op.write_text(json.dumps({'verified':True,'coordinate_denominator':D,'integer_points':points,'A_endpoint_distance_numerator':d2(points[0],A),'distance_denominator_squared':D*D,'ownership':['A','B','A'],'method':'independent integer denominator clearing, exact endpoint maximum formula','scope':'counterexample only; two disks do not cover the full unit disk at U','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8');print('PASS independent integer geometry:unit points,strict A-B-A owners,entire short arc covered by A')
