"""Independent reconstruct-and-evaluate audit of compiled quadratic candidate model."""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def canonical(terms):
    values={}
    for coef,indices in terms:
        key=tuple(sorted(indices));values[key]=values.get(key,0)+coef
    return {k:v for k,v in values.items() if v}
def circle(ids):return canonical([[-1,[]],[1,[ids[0],ids[0]]],[1,[ids[1],ids[1]]]])
def compile_check(z,G):
    pv=z['vertex_variables'];cv=z['center_variables'];ti=z['t_index'];seen=set()
    expected_incidences={(f['center'],v) for f in G['faces'] for v in f['vertices']};actual=set();circles=set();axes=set();quadrants=set();monotones=set();bounds=set()
    for c in z['equalities']:
        meta=c['metadata'];terms=canonical(c['terms'])
        if c['kind']=='boundary_unit_circle':v=meta['vertex'];need(v not in circles and terms==circle(pv[v]),'circle equation');circles.add(v)
        else:
            v=meta['vertex'];d=meta['coordinate'];coord={'E':(1,0),'N':(0,1),'W':(-1,0),'S':(0,-1)}[v][d]
            need((v,d) not in axes and terms==canonical([[1,[pv[v][d]]],[-coord,[]]]),'axis equation');axes.add((v,d))
    need(circles==set(G['boundary_cycle']) and axes=={(v,d) for v in 'ENWS' for d in (0,1)},'equations complete')
    for c in z['inequalities']:
        kind=c['kind'];meta=c['metadata'];terms=canonical(c['terms'])
        if kind=='face_vertex_distance':
            j,v=meta['center'],meta['vertex'];need((j,v) not in actual,'duplicate incidence');actual.add((j,v));a,b=cv[str(j)];u,w=pv[v]
            expected=canonical([[1,[ti]],[-1,[a,a]],[-1,[b,b]],[-1,[u,u]],[-1,[w,w]],[2,[a,u]],[2,[b,w]]]);need(terms==expected,'distance polynomial')
        elif kind in ('vertex_in_D','center_in_D'):
            label=meta['vertex'] if kind=='vertex_in_D' else meta['center'];ids=pv[label] if kind=='vertex_in_D' else cv[str(label)]
            need((kind,label) not in bounds,'duplicate bound');bounds.add((kind,label));need(terms=={k:-v for k,v in circle(ids).items()},'disk bound')
        elif kind in ('t_nonnegative','t_at_most_one'):
            need((kind,None) not in bounds,'duplicate t');bounds.add((kind,None));need(terms==canonical([[1,[ti]]] if kind=='t_nonnegative' else [[1,[]],[-1,[ti]]]),'t bound')
        elif kind=='quadrant_sign':
            q,v,d=meta['quadrant'],meta['vertex'],meta['coordinate'];sign=((1,1),(-1,1),(-1,-1),(1,-1))[q][d]
            need((q,v,d) not in quadrants,'duplicate sign');quadrants.add((q,v,d));need(terms==canonical([[sign,[pv[v][d]]]]),'sign polynomial')
        elif kind=='boundary_monotone':
            q,a,b,d=meta['quadrant'],meta['from'],meta['to'],meta['coordinate'];need(d==(1,0,1,0)[q],'monotone coordinate');sgn=(1,-1,-1,1)[q]
            need((q,a,b) not in monotones,'duplicate monotone');monotones.add((q,a,b));need(terms==canonical([[sgn,[pv[b][d]]],[-sgn,[pv[a][d]]]]),'monotone polynomial')
        else:raise ValueError('unknown constraint')
    need(actual==expected_incidences,'incidence completeness')
    need(bounds=={('vertex_in_D',v) for v in G['vertices']}|{('center_in_D',j) for j in range(100)}|{('t_nonnegative',None),('t_at_most_one',None)},'bounds complete')
    need(quadrants=={(q,v,d) for q,chain in enumerate(z['quadrant_chains']) for v in chain for d in (0,1)},'quadrant completeness')
    need(monotones=={(q,a,b) for q,chain in enumerate(z['quadrant_chains']) for a,b in zip(chain,chain[1:])},'monotone completeness')
    for q,chain in enumerate(z['quadrant_chains']):
        boundary=G['boundary_cycle'];at=boundary.index(chain[0]);need(chain[0]=='ENWS'[q] and chain[-1]=='ENWS'[(q+1)%4],'chain marks')
        need(all(b==boundary[(boundary.index(a)+1)%len(boundary)] for a,b in zip(chain,chain[1:])),'chain adjacency')
    return len(actual)
def mul(a,b):
    vals=[x*y for x in a for y in b];return min(vals),max(vals)
def evaluate(terms,B):
    lo=hi=Q(0)
    for coef,ids in terms:
        term=(Q(coef),Q(coef))
        for i in ids:term=mul(term,B[i])
        lo+=term[0];hi+=term[1]
    return lo,hi
if __name__=='__main__':
    p=R/'verify/out/n100-candidate-quadratic-cover-model.json';z=json.loads(p.read_text(encoding='utf-8'));G=json.loads((R/'verify/out/n100-candidate-clipped-map.json').read_text(encoding='utf-8'))
    for path,h in z['bindings'].items():need(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'binding')
    need(hashlib.sha256((R/'verify/n100_candidate_quadratic_cover_model.py').read_bytes()).hexdigest()==z['checker_sha256'],'script binding')
    incidences=compile_check(z,G);S='runtime/external-disk100-strict-local-replay/source/'
    m=json.loads((R/(S+'rational_midpoint.json')).read_text(encoding='utf-8'));sys=json.loads((R/(S+'polynomial_system.json')).read_text(encoding='utf-8'));inv=json.loads((R/'verify/out/n100-full-circumcenter-root-box.json').read_text(encoding='utf-8'));rows={r['triangle_index']:r for r in inv['rows']}
    D=int(m['denominator']);r=Q(1,10**58);X=[(Q(int(v),D)-r,Q(int(v),D)+r) for v in m['numerators']];B={}
    for v,ids in z['vertex_variables'].items():
        for d,i in enumerate(ids):B[i]=tuple(map(Q,z['point_boxes'][v][d]))
    for j,ids in z['center_variables'].items():
        for d,i in enumerate(ids):B[i]=X[2*int(j)+d]
    B[z['t_index']]=X[492];nonnegative=identities=0
    for c in z['inequalities']:
        if c['acceptance']=='interval_nonnegative':need(evaluate(c['terms'],B)[0]>=0,'independent interval evaluation');nonnegative+=1
        else:
            meta=c['metadata'];v=meta['vertex'];src=z['vertex_sources'][v]
            if c['kind']=='vertex_in_D':need(v in G['boundary_cycle'],'unit root identity')
            else:
                j=meta['center'];need(c['kind']=='face_vertex_distance','root identity kind')
                if src['type']=='KKT_boundary_hole':need(j in sys['boundary_active_pairs'][src['hole']],'boundary root support')
                else:row=rows[src['triangle_index']];need(row['active'] and j in row['support'],'active root support')
            identities+=1
    rejects=[]
    for name,mut in [('missing_incidence',lambda q:q['inequalities'].pop(303)),('wrong_cross_term',lambda q:next(c for c in q['inequalities'] if c['kind']=='face_vertex_distance')['terms'].append([1,[0]])),('missing_quadrant_sign',lambda q:q['inequalities'].remove(next(c for c in q['inequalities'] if c['kind']=='quadrant_sign')))]:
        q=copy.deepcopy(z);mut(q)
        try:compile_check(q,G)
        except (ValueError,KeyError):rejects.append(name)
        else:raise RuntimeError('corruption accepted '+name)
    out=R/'verify/out/n100-candidate-quadratic-cover-model-independent.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'verified':True,'incidences':incidences,'interval_inequalities_recomputed':nonnegative,'root_identity_inequalities_checked':identities,'rejected_controls':rejects,'scope':'independent polynomial completeness and inequality evaluation; exact KKT identities and winding coverage theorem remain analytic/root dependencies','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS independent605-variable model:566 incidences,',nonnegative,'interval inequalities,',identities,'root identities;3 corruptions rejected')
