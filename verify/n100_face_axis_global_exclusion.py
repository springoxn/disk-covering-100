"""Exact whole-domain face-axis SOS lower bound after fixed-axis substitution."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json,hashlib
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def clean(p):return {k:v for k,v in p.items() if v}
def add(*ps):
    out={}
    for p in ps:
        for k,v in p.items():out[k]=out.get(k,F(0))+v
    return clean(out)
def scale(p,v):return clean({k:x*v for k,x in p.items()})
def square(p):
    out={}
    for a,x in p.items():
        for b,y in p.items():k=tuple(sorted(a+b));out[k]=out.get(k,F(0))+x*y
    return clean(out)
def dist_constraint(c,P,t):
    return add({(t,):F(1)},scale(square({(c[0],):F(1),():-F(P[0])}),-1),scale(square({(c[1],):F(1),():-F(P[1])}),-1))
def substitute(terms,values):
    out={}
    for coef,indices in terms:
        coef=F(coef);mon=[]
        for i in indices:
            if i in values:coef*=values[i]
            else:mon.append(i)
        key=tuple(sorted(mon));out[key]=out.get(key,F(0))+coef
    return clean(out)
def certificate(G,M,face,A,B):
    names=list(G['vertices']);marks=G['axis_marks'];coords=[(1,0),(0,1),(-1,0),(0,-1)];P=coords[marks.index(A)];Q=coords[marks.index(B)];j=face['center'];base=2*len(names);c=[base+2*j,base+2*j+1];t=M['t_index']
    need(A!=B and A in face['vertices'] and B in face['vertices'],'support incidence')
    fixed={2*names.index(v)+d:F(value) for v,point in zip(marks,coords) for d,value in enumerate(point)}
    # Locate constraints by exact face traversal, not by assuming fixed offsets.
    distances=[(f['center'],v) for f in G['faces'] for v in f['vertices']];offset=2+len(names)+len(G['faces']);ids=[offset+distances.index((j,v)) for v in (A,B)]
    gs=[]
    for index,point in zip(ids,(P,Q)):
        constraint=M['inequalities'][index];need(constraint['kind']=='face_vertex_distance','constraint type');g=substitute(constraint['terms'],fixed);need(g==dist_constraint(c,point,t),'compiled distance mismatch');gs.append(g)
    midpoint=[F(P[d]+Q[d],2) for d in (0,1)];L=sum(F(P[d]-Q[d])**2 for d in (0,1))/4
    sos=[square({(c[d],):F(1),():-midpoint[d]}) for d in (0,1)]
    lhs={(t,):F(1),():-L};rhs=add(scale(gs[0],F(1,2)),scale(gs[1],F(1,2)),*sos);need(clean(lhs)==rhs,'SOS identity')
    return {'center':j,'axes':[A,B],'distance_constraint_indices':ids,'nonnegative_multipliers':['1/2','1/2'],'square_terms':[{'center_coordinate_index':c[d],'offset':str(midpoint[d])} for d in (0,1)],'t_lower_bound':str(L),'identity':'t-L=(gA+gB)/2+|c-(A+B)/2|^2','fixed_axis_substitution':{str(i):str(v) for i,v in fixed.items()}}
def strongest(G,M):
    allc=[]
    for face in G['faces']:
        for A,B in combinations([v for v in face['vertices'] if v in G['axis_marks']],2):allc.append(certificate(G,M,face,A,B))
    return max(allc,key=lambda c:F(c['t_lower_bound'])) if allc else None
if __name__=='__main__':
    p=R/'verify/out/n100-generic-map-compiler.json';z=json.loads(p.read_text(encoding='utf-8'))
    for path,h in z['bindings'].items():need(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'binding')
    U=F(1154469548855829,10**16);T=U*U;rows=[]
    for e in z['small_models']:
        C=strongest(e['map'],e['model']);need(C is not None and F(C['t_lower_bound'])==1 and T<1,'small exclusion');rows.append({'chord':e['chord'],'certificate':C,'excluded_entire_closed_domain_at_t_upper':str(T)})
    G=json.loads((R/'verify/out/n100-candidate-clipped-map.json').read_text(encoding='utf-8'));candidate=strongest(G,z['candidate_model']);need(candidate is None,'candidate unexpectedly excluded')
    need(T<F(1,2),'universal adjacent axis exclusion')
    # Coefficient identity controls.
    g=dist_constraint([0,1],(1,0),2);h=dist_constraint([0,1],(0,1),2);rhs=add(scale(g,F(1,2)),scale(h,F(1,2)),square({(0,):F(1),():F(-1,2)}),square({(1,):F(1),():F(-1,2)}));need(rhs!={(2,):F(1),():F(-1,4)},'false lower bound control')
    out=R/'verify/out/n100-face-axis-global-exclusion.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'verified':True,'t_upper':str(T),'universally_excluded_pattern':'any inner face contains two distinct fixed axis marks','adjacent_axis_t_lower':'1/2','opposite_axis_t_lower':'1','small_map_exclusions':rows,'candidate_triggered':False,'negative_control_wrong_constant_rejected':True,'scope':'whole-domain exclusion for a structural subfamily, including all six calibrated small maps; remaining n100 maps not enumerated or excluded','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS exact SOS identities;all6 small map domains excluded at upper bound;any face with2 axes impossible;candidate unaffected')
