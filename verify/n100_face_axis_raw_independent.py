"""Independent raw certificate identity verification by sparse rational accumulation."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def check(row,T,example):
    G,M=example['map'],example['model'];names=list(G['vertices']);axis=dict(zip(G['axis_marks'],[(1,0),(0,1),(-1,0),(0,-1)]));f=next(f for f in G['faces'] if f['center']==row['face']);A,B=row['axes'];need(A!=B and A in f['vertices'] and B in f['vertices'],'incidence');coords=[axis[A],axis[B]];L=sum(F(a-b)**2 for a,b in zip(*coords))/4;delta=L-T;need(delta>0 and F(row['delta'])==delta,'gap')
    acc={}
    def insert(c,ids):
        key=tuple(sorted(ids));acc[key]=acc.get(key,F(0))+F(c)
    refs=[(face['center'],v) for face in G['faces'] for v in face['vertices']];start=2+len(names)+len(G['faces']);need(row['distance_indices']==[start+refs.index((row['face'],v)) for v in (A,B)],'references')
    for i in row['distance_indices']:
        for c,ids in M['inequalities'][i]['terms']:insert(F(c)/2,ids)
    base=2*len(names)+2*row['face']
    for d in (0,1):
        mid=F(coords[0][d]+coords[1][d],2);insert(1,[base+d,base+d]);insert(-2*mid,[base+d]);insert(mid*mid,[])
    insert(T,[]);insert(-1,[M['t_index']]);insert(delta,[])
    fixed={2*names.index(v)+d:F(value) for v,p in axis.items() for d,value in enumerate(p)};need(len(row['axis_quotients'])==8,'quotient count');seen=set()
    for item in row['axis_quotients']:
        i=item['variable'];a=F(item['constant']);need(i not in seen and i in fixed and a==fixed[i],'axis constant');seen.add(i)
        # Check that x_i-a is an actual equality, not only a coordinate label.
        eq={tuple(ids):F(c) for c,ids in next(e for e in M['equalities'] if e['kind']=='axis_coordinate' and any(ids==[i] for c,ids in e['terms']))['terms']}
        need(eq==({(i,):F(1),():-a} if a else {(i,):F(1)}),'axis equation')
        for c,ids in item['quotient']:insert(-F(c),ids+[i]);insert(F(c)*a,ids)
    need(all(v==0 for v in acc.values()),'raw identity failed')
    return str(1/delta)
if __name__=='__main__':
    p=R/'verify/out/n100-face-axis-raw-variable-certificates-v2.json';z=json.loads(p.read_text(encoding='utf-8'));models=json.loads((R/'verify/out/n100-generic-map-compiler.json').read_text(encoding='utf-8'));T=F(1154469548855829,10**16)**2;need(F(z['T'])==T,'endpoint')
    for path,h in z['bindings'].items():need(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'binding')
    lookup={tuple(e['chord']):e for e in models['small_models']};results=[]
    from itertools import combinations
    for pair,row in zip(combinations(range(4),2),z['certificates']):results.append({'chord':pair,'positive_scale':check(row,T,lookup[pair])})
    need(len(results)==6,'count');first=z['certificates'][0];e=lookup[(0,1)];reject=[]
    for name,mut in [('wrong_axis',lambda r:r['axis_quotients'][0].__setitem__('constant','2')),('wrong_quotient',lambda r:r['axis_quotients'][0].__setitem__('quotient',[['1',[]]])),('missing_quotient',lambda r:r['axis_quotients'].pop()),('wrong_distance',lambda r:r['distance_indices'].__setitem__(0,0))]:
        bad=copy.deepcopy(first);mut(bad)
        try:check(bad,T,e)
        except ValueError:reject.append(name)
        else:raise RuntimeError('corruption accepted')
    op=R/'verify/out/n100-face-axis-raw-independent.json';need(not op.exists(),'overwrite');op.write_text(json.dumps({'verified':True,'results':results,'rejected_controls':reject,'method':'direct full-variable coefficient accumulation, no quotient generator import','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8');print('PASS independent6 full-variable identities and4 corruption rejections')
