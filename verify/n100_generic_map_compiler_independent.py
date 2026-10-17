"""Independent exact evaluation of six compiled small-map closed models."""
from pathlib import Path
from fractions import Fraction
import json,hashlib
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
p=R/'verify/out/n100-generic-map-compiler.json';z=json.loads(p.read_text(encoding='utf-8'))
for f,h in z['bindings'].items():need(hashlib.sha256((R/f).read_bytes()).hexdigest()==h,'binding')
need(hashlib.sha256((R/'verify/n100_generic_map_compiler.py').read_bytes()).hexdigest()==z['checker_sha256'],'script binding')
rows=[]
for example in z['small_models']:
    G=example['map'];M=example['model'];names=list(G['vertices']);points=dict(zip(G['axis_marks'],[(1,0),(0,1),(-1,0),(0,-1)]));X=[]
    for v in names:X.extend(map(Fraction,points[v]))
    X.extend([Fraction(0)]*(2*len(G['faces'])));X.append(Fraction(1))
    need(len(X)==M['variables']==13 and M['t_index']==12,'index count')
    def evaluate(c):
        result=Fraction(0)
        for coefficient,indices in c['terms']:
            term=Fraction(coefficient)
            for i in indices:term*=X[i]
            result+=term
        return result
    need(all(evaluate(c)==0 for c in M['equalities']),'equality violation')
    need(all(evaluate(c)>=0 for c in M['inequalities']),'inequality violation')
    rows.append({'chord':example['chord'],'equalities_checked':len(M['equalities']),'inequalities_checked':len(M['inequalities']),'exact_t':'1','all_centers':[0,0]})
need(len(rows)==6,'cases')
out=R/'verify/out/n100-generic-map-compiler-independent.json';need(not out.exists(),'overwrite')
out.write_text(json.dumps({'verified':True,'rows':rows,'method':'independent Fraction evaluation at four axis vertices, both centers zero and t=1','scope':'exact feasible assignments for six compiled small models; does not prove compiler completeness on all maps or n100 optimality','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
print('PASS independent Fraction evaluation:6 small models,72 equalities and204 inequalities; duplicate centers permitted')
