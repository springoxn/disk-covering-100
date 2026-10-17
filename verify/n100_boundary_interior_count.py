"""Universal coupled boundary/interior count; root-box candidate classification."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];S='runtime/external-disk100-strict-local-replay/source/'
def need(ok,msg):
    if not ok:raise ValueError(msg)
if __name__=='__main__':
    U=F(1154469548855829,10**16);inner=1-2*U;ratio=inner**2/U**2
    need(inner>0 and F(44)<ratio<F(45),'interior count')
    boundary=json.loads((R/'verify/out/n100-boundary-serving-count.json').read_text(encoding='utf-8'));need(boundary['minimum_boundary_serving_disks']==28,'boundary count')
    m=json.loads((R/(S+'rational_midpoint.json')).read_text(encoding='utf-8'));k=json.loads((R/(S+'krawczyk_verification.json')).read_text(encoding='utf-8'));D=int(m['denominator']);rho=F(*k['box_radius']);need(k['verified'] and rho==F(1,10**58),'root')
    x=[(F(int(v),D)-rho,F(int(v),D)+rho) for v in m['numerators']];t=x[492]
    # Disk intersects circle iff (1+|c|²-t)² <=4|c|²; lhs base positive here.
    def sq(a):return (F(0) if a[0]<=0<=a[1] else min(a[0]**2,a[1]**2),max(a[0]**2,a[1]**2))
    rows=[];serving=[];non=[]
    for j in range(100):
        aa,bb=sq(x[2*j]),sq(x[2*j+1]);norm=(aa[0]+bb[0],aa[1]+bb[1]);base=(1+norm[0]-t[1],1+norm[1]-t[0]);need(base[0]>0,'positive branch');z=sq(base);disc=(4*norm[0]-z[1],4*norm[1]-z[0])
        if disc[0]>0:kind='serves_circle';serving.append(j)
        elif disc[1]<0:kind='does_not_serve_circle';non.append(j)
        else:raise ValueError('undecided circle service')
        rows.append({'center':j,'kind':kind,'discriminant_interval':list(map(str,disc))})
    need(serving==boundary['candidate_boundary_faces'],'geometric versus map boundary centers')
    need(len(non)>=45 and len(serving)<=55,'candidate counts')
    out=R/'verify/out/n100-boundary-interior-count.json';need(not out.exists(),'overwrite');paths=[S+'rational_midpoint.json',S+'krawczyk_verification.json','verify/out/n100-boundary-serving-count.json']
    out.write_text(json.dumps({'verified_rational_bounds':True,'radius_upper':str(U),'inner_disk_radius':str(inner),'inner_area_capacity_ratio':str(ratio),'minimum_non_boundary_serving_disks':45,'minimum_boundary_serving_disks':28,'maximum_boundary_serving_disks_for_n100':55,'total_disk_count_lower_from_this_argument':73,'candidate_boundary_serving_count':len(serving),'candidate_non_boundary_serving_count':len(non),'candidate_rows':rows,'analytic_dependencies':['triangle inequality: circle-intersecting disk cannot enter |p|<1-2r','area subadditivity on inner open disk','previous universal boundary28 count'],'scope':'necessary coupled count, no new accepted radius bound; boundary model faces are a subset of actual circle-serving disks','bindings':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in paths},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8');print('PASS at least45 non-circle-serving disks;actual boundary count28..55;candidate32 boundary/68 interior root-box classifications')
