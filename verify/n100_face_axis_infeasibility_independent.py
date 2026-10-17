"""Independent exact interpolation proof of six negative-one infeasibility identities.
No import of the primary SOS polynomial implementation.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import json,hashlib,copy
R=Path(__file__).resolve().parents[1]
def need(x,msg):
    if not x:raise ValueError(msg)
def evaluate(terms,values):
    total=Q(0)
    for coef,indices in terms:
        term=Q(coef)
        for i in indices:term*=values[i]
        total+=term
    return total

def verify(entry,example,T):
    G,M=example['map'],example['model'];C=entry['certificate'];names=list(G['vertices']);marks=G['axis_marks'];axis=[(1,0),(0,1),(-1,0),(0,-1)];j=C['center'];face=next(f for f in G['faces'] if f['center']==j);A,B=C['axes']
    need(A!=B and A in marks and B in marks and A in face['vertices'] and B in face['vertices'],'axis incidence')
    values={2*names.index(v)+d:Q(value) for v,coord in zip(marks,axis) for d,value in enumerate(coord)}
    need(C['fixed_axis_substitution']=={str(i):str(v) for i,v in values.items()},'substitution')
    # Verify substituted coordinates against actual model equality polynomials.
    axis_eq=[e for e in M['equalities'] if e['kind']=='axis_coordinate'];need(len(axis_eq)==8,'axis eq count')
    need(all(evaluate(e['terms'],values)==0 for e in axis_eq),'axis equations')
    base=2*len(names);center=[base+2*j,base+2*j+1];ti=M['t_index'];free=set(center+[ti]);constraints=[]
    need(len(C['distance_constraint_indices'])==2 and len(set(C['distance_constraint_indices']))==2,'distance IDs')
    for idx,v in zip(C['distance_constraint_indices'],(A,B)):
        need(0<=idx<len(M['inequalities']),'constraint index');g=M['inequalities'][idx];need(g['kind']=='face_vertex_distance','distance kind')
        support={i for coef,ids in g['terms'] if coef for i in ids};expected=set(center+[ti]+[2*names.index(v),2*names.index(v)+1]);need(support==expected,'distance variable support');constraints.append(g)
    P,S=axis[marks.index(A)],axis[marks.index(B)];L=sum(Q(p-s)**2 for p,s in zip(P,S))/4;gap=L-T
    need(gap>0 and Q(C['t_lower_bound'])==L and Q(entry['excluded_entire_closed_domain_at_t_upper'])==T,'positive exclusion gap')
    multipliers=list(map(Q,C['nonnegative_multipliers']));need(len(multipliers)==2 and all(v>=0 for v in multipliers),'positive multipliers')
    need(len(C['square_terms'])==2 and {s['center_coordinate_index'] for s in C['square_terms']}==set(center),'square index')
    # Each term has individual degree <=2 in the three free variables. Evaluating
    # on {-1,0,1}^3 proves the polynomial identity by successive univariate interpolation.
    for g in constraints:
        need(all(len(ids)<=2 and set(ids)<=free|set(values) for coef,ids in g['terms']),'degree/support bound')
    for x,y,t in product((-1,0,1),repeat=3):
        assigned=dict(values);assigned.update(zip(center+[ti],map(Q,(x,y,t))))
        total=sum(mult*evaluate(g['terms'],assigned) for mult,g in zip(multipliers,constraints))
        total+=sum((assigned[s['center_coordinate_index']]-Q(s['offset']))**2 for s in C['square_terms'])
        total+=T-assigned[ti]
        need(total/gap==-1,'negative-one identity')
    return {'distance_multipliers':[str(v/gap) for v in multipliers],'square_multipliers':[str(1/gap)]*2,'upper_bound_multiplier':str(1/gap),'upper_bound_terms':[[str(T),[]],['-1',[ti]]],'exact_negative_one_identity_verified':True,'tensor_interpolation_nodes':27,'gap':str(gap)}

if __name__=='__main__':
    certpath=R/'verify/out/n100-face-axis-global-exclusion.json';modelpath=R/'verify/out/n100-generic-map-compiler.json';z=json.loads(certpath.read_text(encoding='utf-8'));models=json.loads(modelpath.read_text(encoding='utf-8'))
    need(hashlib.sha256(modelpath.read_bytes()).hexdigest()==z['input_sha256'],'model binding')
    for path,h in models['bindings'].items():need(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'dependency binding')
    need(hashlib.sha256((R/'verify/n100_face_axis_global_exclusion.py').read_bytes()).hexdigest()==z['checker_sha256'],'primary binding')
    T=Q(1154469548855829,10**16)**2;need(Q(z['t_upper'])==T,'upper endpoint')
    examples={tuple(e['chord']):e for e in models['small_models']};results=[]
    for e in z['small_map_exclusions']:results.append({'chord':e['chord'],'certificate':verify(e,examples[tuple(e['chord'])],T)})
    need(len(results)==6,'six maps')
    rejected=[];first=z['small_map_exclusions'][0];model=examples[tuple(first['chord'])]
    for name,mut in [('negative_multiplier',lambda e:e['certificate']['nonnegative_multipliers'].__setitem__(0,'-1/2')),('wrong_square_offset',lambda e:e['certificate']['square_terms'][0].__setitem__('offset','1/3')),('wrong_constraint_reference',lambda e:e['certificate']['distance_constraint_indices'].__setitem__(0,0)),('wrong_lower_bound',lambda e:e['certificate'].__setitem__('t_lower_bound','2'))]:
        bad=copy.deepcopy(first);mut(bad)
        try:verify(bad,model,T)
        except (ValueError,KeyError):rejected.append(name)
        else:raise RuntimeError('corruption accepted')
    out=R/'verify/out/n100-face-axis-infeasibility-independent.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'verified':True,'certificates':results,'exact_interpolation_nodes_total':162,'rejected_controls':rejected,'method':'independent rational evaluation with proved individual degree bound and full tensor interpolation; not random testing','scope':'six model domains at explicit T; general two-axis face identity, no remaining n100 domains excluded','bindings':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (certpath,modelpath)},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'formal_kernel_verified':False,'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS independent6 negative-one certificates,162 exact interpolation nodes,actual model references;4 corruptions rejected')
