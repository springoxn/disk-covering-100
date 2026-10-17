"""Independent denominator-cleared boundary count and midpoint-free face counting."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def boundary_faces(g):
    uses={i:[] for i in range(len(g['edges']))}
    for face in g['faces']:
        for edge in face['edges']:uses[edge].append(face['center'])
    for i,u in uses.items():need(sorted(u)==sorted(g['edges'][i]['faces']),'owner incidence')
    return sorted({u[0] for u in uses.values() if len(u)==1})
if __name__=='__main__':
    p=R/'verify/out/n100-boundary-serving-count.json';z=json.loads(p.read_text(encoding='utf-8'))
    for f,h in z['bindings'].items():need(hashlib.sha256((R/f).read_bytes()).hexdigest()==h,'binding')
    need(hashlib.sha256((R/'verify/n100_boundary_serving_count.py').read_bytes()).hexdigest()==z['checker_sha256'],'script')
    a,b=1154469548855829,10**16
    # 157^2(b^2-a^2) - 50^2 k^2 a^2 clears all square roots and rational denominators.
    margin=lambda k:157**2*(b*b-a*a)-50**2*k*k*a*a
    need(margin(27)>0 and margin(28)<0,'integer margins')
    # 16(74/375)-4/239-157/50>0 after clearing denominator375*239*50.
    pi_margin=16*74*239*50-4*375*50-157*375*239
    need(pi_margin>0,'Machin comparison')
    need(z['minimum_boundary_serving_disks']==28 and z['radius_upper']=='1154469548855829/10000000000000000','claim endpoint')
    g=json.loads((R/'verify/out/n100-candidate-clipped-map.json').read_text(encoding='utf-8'));actual=boundary_faces(g)
    need(actual==z['candidate_boundary_faces'] and len(actual)==32,'boundary ownership count')
    models=json.loads((R/'verify/out/n100-generic-map-compiler.json').read_text(encoding='utf-8'))
    for e in models['small_models']:need(len(boundary_faces(e['map']))==2,'small count')
    rejected=[]
    for name,k in [('unsupported_29_minimum',28),('unsupported_30_minimum',29)]:
        need(margin(k)<=0,'bad boundary count accepted');rejected.append(name)
    op=R/'verify/out/n100-boundary-serving-count-independent.json';need(not op.exists(),'overwrite')
    op.write_text(json.dumps({'verified':True,'integer_margin_27':str(margin(27)),'integer_margin_28':str(margin(28)),'integer_machin_margin':str(pi_margin),'candidate_boundary_face_count':32,'small_model_boundary_face_count':2,'rejected_overclaims':rejected,'method':'integer denominator clearing and face-cycle incidence counting; does not formalize analytic arc or Machin lemmas','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS independent integer arc bound and face-cycle count;minimum28,candidate32;29/30 overclaims rejected')
