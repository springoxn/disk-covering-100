"""Independent audit of one-interior-vertex orbit models and a two-point radius lemma.
Reconstructs every compiled polynomial and tests exact rational boundary assignments.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib,copy,argparse
from n100_expanded_map_models import expected,signature
from n100_raw_dart_model_adapter import decode
from n100_generic_map_compiler import compile_model
from n100_dart_independent_canonicalization import need
ROOT=Path(__file__).resolve().parents[1]
def val(poly,X):
    z=F(0)
    for a,ix in poly['terms']:
        q=F(a)
        for i in ix:q*=X[i]
        z+=q
    return z
def assignment(g):
    # Axis vertices are fixed; every other boundary vertex is a rational point on the proper quarter arc.
    pts=dict(zip(g['axis_marks'],[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]));B=g['boundary_cycle'];A=g['axis_marks']
    for q,a in enumerate(A):
        i=B.index(a);chain=[]
        while True:
            i=(i+1)%len(B);v=B[i]
            if v==A[(q+1)%4]:break
            chain.append(v)
        for j,v in enumerate(chain):
            t=F(j+1,len(chain)+1);x=(1-t*t)/(1+t*t);y=2*t/(1+t*t);pts[v]=[(x,y),(-y,x),(-x,-y),(y,-x)][q]
    for v in g['vertices']:pts.setdefault(v,(F(0),F(0)))
    return [x for v in g['vertices'] for x in pts[v]]+[F(0)]*(2*len(g['faces']))+[F(1)]
def audit(g,m):
    e,i=expected(g);need(Counter(signature(p['kind'],p['terms']) for p in m['equalities'])==e,'eq reconstruction');need(Counter(signature(p['kind'],p['terms']) for p in m['inequalities'])==i,'ineq reconstruction')
    X=assignment(g);need(all(val(p,X)==0 for p in m['equalities']),'eq assignment');need(all(val(p,X)>=0 for p in m['inequalities']),'ineq assignment')
    return {'variables':m['variables'],'equalities':len(m['equalities']),'inequalities':len(m['inequalities']),'exact_assignment':True}
def two_point_bound(g,m):
    points=dict(zip(g['axis_marks'],[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]));bounds=[]
    # At fixed axis points, verify the polynomial identity in symbolic center coordinates:
    # 2*(t-|c-p|^2)+2*(t-|c-q|^2)+4*|c-(p+q)/2|^2=4*t-|p-q|^2.
    identities=0
    for face in g['faces']:
        vs=[v for v in face['vertices'] if v in points];mx=F(0);pair=None
        for ia,a in enumerate(vs):
            for b in vs[ia+1:]:
                p,q=points[a],points[b];distance=sum((x-y)**2 for x,y in zip(p,q));lower=distance/4
                # Independent coefficient accumulation in basis (1,cx,cy,cx^2,cy^2,t).
                coef=[F(0)]*6
                for point in (p,q):
                    coef[0]-=2*sum(v*v for v in point);coef[1]+=4*point[0];coef[2]+=4*point[1];coef[3]-=2;coef[4]-=2;coef[5]+=2
                mean=tuple((x+y)/2 for x,y in zip(p,q));coef[0]+=4*sum(v*v for v in mean);coef[1]-=8*mean[0];coef[2]-=8*mean[1];coef[3]+=4;coef[4]+=4
                need(coef==[-distance,F(0),F(0),F(0),F(0),F(4)],'pair SOS identity');identities+=1
                if lower>mx:mx,pair=lower,[a,b]
        bounds.append({'face':face['center'],'fixed_axis_pair':pair,'radius_squared_lower':str(mx)})
    return {'face_bounds':bounds,'sos_identities_verified':identities,'maximum_lower':str(max((F(row['radius_squared_lower']) for row in bounds),default=F(0)))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-one-interior-models-independent.json');args=ap.parse_args()
    src=ROOT/'verify/out/n100-one-interior-map-enumeration.json';z=json.loads(src.read_text(encoding='utf-8'));rows=[];total=0
    for item in sum((family['models'] for family in [{'models':z['models']}]),[]):
        g=item['map'];m=item['model'];rows.append({'audit':audit(g,m),'two_point_bounds':two_point_bound(g,m)});total+=1
    need(total==16,'model count');bad=copy.deepcopy(z['models'][0]['model']);bad['equalities'][0]['terms'][0][0]=F(bad['equalities'][0]['terms'][0][0])+1
    try:audit(z['models'][0]['map'],bad)
    except ValueError:pass
    else:raise ValueError('corruption accepted')
    U=F(1154469548855829,10**16);cut=U*U
    histogram=Counter(r['two_point_bounds']['maximum_lower'] for r in rows)
    need(all(F(r['two_point_bounds']['maximum_lower'])>cut for r in rows),'all small domains excluded')
    candidate_path=ROOT/'verify/out/n100-candidate-clipped-map.json';candidate=json.loads(candidate_path.read_text(encoding='utf-8'));candidate_model=compile_model(candidate)
    eq,iq=expected(candidate)
    need(eq==Counter(signature(p['kind'],p['terms']) for p in candidate_model['equalities']) and iq==Counter(signature(p['kind'],p['terms']) for p in candidate_model['inequalities']),'candidate coefficients')
    candidate_pairs=two_point_bound(candidate,candidate_model);need(F(candidate_pairs['maximum_lower'])==0,'candidate negative control')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    output={'schema':'n100-one-interior-models-independent/v2','verified':True,'models':total,'audits':rows,'polynomials_reconstructed':sum(r['audit']['equalities']+r['audit']['inequalities'] for r in rows),'two_point_radius_bounds_exact':True,'coefficient_corruption_rejected':True,'fixed_axis_lower_histogram':dict(histogram),'squared_radius_cut':str(cut),'small_orbit_domains_excluded_at_U':16,'candidate_fixed_axis_pair_control':candidate_pairs,'candidate_excluded':False,'new_n100_count_families_excluded':0,'scope':'16 small map continuous domains excluded by fixed-axis pair SOS; real n100 candidate has no such pair; no n100 global exclusion','global_optimality':False,'minimal_polynomial_obtained':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (src,candidate_path,ROOT/'verify/n100_expanded_map_models.py',ROOT/'verify/n100_generic_map_compiler.py')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('PASS16 internal models; exact pair SOS bounds',dict(histogram),';16 small continuous domains excluded at U; real n100 candidate no pair, preserved')
if __name__=='__main__':main()
