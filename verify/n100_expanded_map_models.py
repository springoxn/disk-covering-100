"""Compile all expanded bounded map orbits and audit every polynomial independently."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib,argparse,copy
from n100_raw_dart_model_adapter import decode
from n100_generic_map_compiler import compile_model
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def terms(items):
    vals={}
    for coefficient,indices in items:
        key=tuple(sorted(indices));vals[key]=vals.get(key,F(0))+F(coefficient)
    return tuple(sorted((key,str(v)) for key,v in vals.items() if v))
def signature(kind,items):return kind,terms(items)
def expected(g):
    names=list(g['vertices']);m=len(g['faces']);V=len(names);T=2*(V+m)
    pv={v:(2*i,2*i+1) for i,v in enumerate(names)};cv={j:(2*V+2*j,2*V+2*j+1) for j in range(m)}
    eq=[];iq=[]
    def put(target,kind,parts):target.append(signature(kind,parts))
    put(iq,'t_nonnegative',[(1,[T])]);put(iq,'t_at_most_one',[(1,[]),(-1,[T])])
    for v in names:put(iq,'vertex_in_D',[(1,[]),(-1,[pv[v][0]]*2),(-1,[pv[v][1]]*2)])
    for j in range(m):put(iq,'center_in_D',[(1,[]),(-1,[cv[j][0]]*2),(-1,[cv[j][1]]*2)])
    for face in g['faces']:
        for v in face['vertices']:
            parts=[(1,[T])]
            for p,c in zip(pv[v],cv[face['center']]):parts.extend([(-1,[p,p]),(2,[p,c]),(-1,[c,c])])
            put(iq,'face_vertex_distance',parts)
    for v in g['boundary_cycle']:put(eq,'boundary_unit_circle',[(-1,[]),(1,[pv[v][0]]*2),(1,[pv[v][1]]*2)])
    coords=[(1,0),(0,1),(-1,0),(0,-1)]
    for v,xy in zip(g['axis_marks'],coords):
        for d,value in enumerate(xy):put(eq,'axis_coordinate',[(-value,[]),(1,[pv[v][d]])])
    boundary=g['boundary_cycle'];signs=[(1,1),(-1,1),(-1,-1),(1,-1)]
    for quadrant,a in enumerate(g['axis_marks']):
        b=g['axis_marks'][(quadrant+1)%4];at=boundary.index(a);chain=[a]
        while chain[-1]!=b:at=(at+1)%len(boundary);chain.append(boundary[at])
        for v in chain:
            for d in (0,1):put(iq,'quadrant_sign',[(signs[quadrant][d],[pv[v][d]])])
        dimension=(1,0,1,0)[quadrant];sgn=(1,-1,-1,1)[quadrant]
        for left,right in zip(chain,chain[1:]):put(iq,'boundary_monotone',[(sgn,[pv[right][dimension]]),(-sgn,[pv[left][dimension]])])
    return Counter(eq),Counter(iq)
def audit(g,model):
    e,i=expected(g)
    need(Counter(signature(p['kind'],p['terms']) for p in model['equalities'])==e,'equality coefficients')
    need(Counter(signature(p['kind'],p['terms']) for p in model['inequalities'])==i,'inequality coefficients')
    need(model['variables']==2*(len(g['vertices'])+len(g['faces']))+1,'variables')
    # Rational boundary placement, permitting coincident centers as the closed model does.
    points=dict(zip(g['axis_marks'],[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]))
    boundary=g['boundary_cycle'];axis=g['axis_marks']
    for q,start in enumerate(axis):
        chain=[];idx=boundary.index(start)
        while True:
            idx=(idx+1)%len(boundary);v=boundary[idx]
            if v==axis[(q+1)%4]:break
            chain.append(v)
        for j,v in enumerate(chain):
            t=F(j+1,len(chain)+1);x=(1-t*t)/(1+t*t);y=2*t/(1+t*t)
            points[v]=[(x,y),(-y,x),(-x,-y),(y,-x)][q]
    X=[coord for v in g['vertices'] for coord in points[v]]+[F(0)]*(2*len(g['faces']))+[F(1)]
    def value(p):
        total=F(0)
        for coefficient,indices in p['terms']:
            v=F(coefficient)
            for j in indices:v*=X[j]
            total+=v
        return total
    need(all(value(p)==0 for p in model['equalities']),'assignment equations')
    need(all(value(p)>=0 for p in model['inequalities']),'assignment inequalities')
    return {'all_coefficients_reconstructed':True,'exact_feasible_assignment':[str(x) for x in X]}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-expanded-map-models.json');args=ap.parse_args()
    source=ROOT/'verify/out/n100-expanded-map-enumeration.json';z=json.loads(source.read_text(encoding='utf-8'));rows=[];total=0;polys=0
    for family in z['families']:
        models=[]
        for raw in family['orbit_representatives']:
            need(raw['alpha']==[d^1 for d in range(len(raw['phi']))],'paired-dart adapter convention')
            g=decode(raw['phi'],1,[0,2,4,6]);m=compile_model(g);result=audit(g,m)
            need(len(g['vertices'])==family['boundary_vertices'] and len(g['edges'])==family['edges'] and len(g['faces'])==family['inner_faces'],'family counts')
            models.append({'map':g,'model':m,'independent_audit':result});total+=1;polys+=len(m['equalities'])+len(m['inequalities'])
        rows.append({'boundary_vertices':family['boundary_vertices'],'edges':family['edges'],'inner_faces':family['inner_faces'],'models':models})
    need(total==45,'orbit total');bad=copy.deepcopy(rows[0]['models'][0]);bad['model']['inequalities'][0]['terms'][0][0]=2
    try:audit(bad['map'],bad['model'])
    except ValueError:pass
    else:raise ValueError('corrupted polynomial accepted')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-expanded-map-models/v1','verified':True,'orbit_models':total,'polynomials_checked':polys,'families':rows,'coefficient_corruption_rejected':True,'independent_expected_polynomial_construction':True,'all_exact_feasible_assignments_at_t1':True,'continuous_domains_excluded':0,'n100_complete_enumeration':False,'global_optimality':False,'scope':'45 enumerated small-map orbit models; shared raw-dart decoder but independently reconstructed every polynomial; no radius improvement',
        'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (source,ROOT/'verify/n100_raw_dart_model_adapter.py',ROOT/'verify/n100_generic_map_compiler.py')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS45 orbit models;',polys,'independently reconstructed polynomials;exact rational t=1 assignments;coefficient corruption rejected')
if __name__=='__main__':main()
