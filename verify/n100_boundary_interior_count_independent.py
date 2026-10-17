"""Integer independent verification of coupled count and service classification."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
p=R/'verify/out/n100-boundary-interior-count.json';z=json.loads(p.read_text(encoding='utf-8'))
for path,h in z['bindings'].items():need(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'binding')
a,b=1154469548855829,10**16;A=(b-2*a)**2;need(44*a*a<A<45*a*a,'integer capacity')
S='runtime/external-disk100-strict-local-replay/source/';m=json.loads((R/(S+'rational_midpoint.json')).read_text(encoding='utf-8'));D=int(m['denominator']);v=list(map(int,m['numerators']));need(D==10**60,'denominator');e=100
serves=[];doesnot=[]
for j,row in enumerate(z['candidate_rows']):
    # Centers have intervals [(v-e)/D,(v+e)/D]. Integer squares bound norm numerator.
    def square_bounds(n):return (0 if n-e<=0<=n+e else min((n-e)**2,(n+e)**2),max((n-e)**2,(n+e)**2))
    x,y=square_bounds(v[2*j]),square_bounds(v[2*j+1]);lo=x[0]+y[0];hi=x[1]+y[1];tlo,thi=(v[492]-e)*D,(v[492]+e)*D
    blo,bhi=D*D+lo-thi,D*D+hi-tlo;need(blo>0,'positive branch')
    lower=4*lo*D*D-bhi*bhi;upper=4*hi*D*D-blo*blo
    kind='serves_circle' if lower>0 else 'does_not_serve_circle' if upper<0 else None
    need(kind==row['kind'] and kind is not None,'classification');(serves if lower>0 else doesnot).append(j)
need(len(serves)==32 and len(doesnot)==68 and z['minimum_non_boundary_serving_disks']==45,'counts')
op=R/'verify/out/n100-boundary-interior-count-independent.json';need(not op.exists(),'overwrite');op.write_text(json.dumps({'verified':True,'integer_area_numerator':str(A),'44_disk_capacity_numerator':str(44*a*a),'45_disk_capacity_numerator':str(45*a*a),'candidate_circle_serving_centers':serves,'candidate_non_circle_serving_centers':doesnot,'method':'integer-only capacity and interval discriminant recomputation','scope':'necessary count and root-box candidate classification, not n100 global exclusion','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8');print('PASS independent integer capacity45 and100 root-box classifications:32 serves/68 doesnot')
