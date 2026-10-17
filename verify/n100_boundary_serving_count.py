"""Universal boundary-serving disk count via rational arc-capacity bounds."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parents[1]
def need(v,m):
    if not v:raise ValueError(m)
if __name__=='__main__':
    U=F(1154469548855829,10**16);P=F(157,50)
    # Machin pi=16 atan(1/5)-4 atan(1/239), alternating bounds.
    machin_lower=16*(F(1,5)-F(1,3*5**3))-F(4,239)
    need(machin_lower>P,'pi lower')
    margin=P*P*(1-U*U)-27**2*U*U;need(margin>0,'27 disks not excluded')
    need(P*P*(1-U*U)-28**2*U*U<0,'28 control')
    map_path=R/'verify/out/n100-candidate-clipped-map.json';G=json.loads(map_path.read_text(encoding='utf-8'))
    serving=sorted({f for e in G['edges'] if len(e['faces'])==1 for f in e['faces']});need(len(serving)==32,'candidate boundary faces')
    models_path=R/'verify/out/n100-generic-map-compiler.json';models=json.loads(models_path.read_text(encoding='utf-8'));small=[]
    for example in models['small_models']:
        g=example['map'];k=len({f for e in g['edges'] if len(e['faces'])==1 for f in e['faces']});need(k<28,'small maps')
        small.append({'chord':example['chord'],'distinct_boundary_faces':k,'excluded_at_U':True})
    op=R/'verify/out/n100-boundary-serving-count.json';need(not op.exists(),'overwrite')
    op.write_text(json.dumps({'verified_rational_inequalities':True,'radius_upper':str(U),'pi_strict_lower':str(P),'machin_strict_lower':str(machin_lower),'27_disk_squared_margin':str(margin),'minimum_boundary_serving_disks':28,'candidate_boundary_faces':serving,'candidate_boundary_face_count':len(serving),'candidate_boundary_arc_count':G['boundary_edges'],'small_map_exclusions':small,'28_disk_not_excluded_by_this_bound':True,'analytic_dependencies':['Machin identity with real branch and alternating atan series','circle intersection arc length at most 2 asin(r) via AM-GM','asin(r)<=r/sqrt(1-r^2) via monotone integrand','circle arc-length finite subadditivity','model boundary edges are served by their incident face via same-quadrant arc lemma'],'scope':'universal necessary count of distinct boundary-serving disks or boundary-incident model faces at r<=U; not number of boundary vertices; no radius-bound improvement or complete map enumeration','bindings':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (map_path,models_path)},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'formal_kernel_verified':False,'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS strict rational27-arc exclusion;at least28 distinct boundary-serving disks;candidate32 distinct faces/36 arcs;28 control not excluded')
