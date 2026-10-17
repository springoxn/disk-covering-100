"""Independent replay by recursive inherited rectangles; no import of primary verifier."""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
src=R/'verify/out/n100-global-witness-tree-interface.json'
data=json.loads(src.read_text(encoding='utf-8'))
script=R/'verify/n100_global_witness_tree.py'
if hashlib.sha256(script.read_bytes()).hexdigest()!=data['script_sha256']:raise ValueError('script binding')

def check(z,global_required):
    n=z['n']; b=[tuple(map(Q,p)) for p in z['root_box']]
    if len(b)!=2*n+1 or any(a>v for a,v in b) or b[-1][0]<0:raise ValueError('root')
    full=b==[(Q(-1),Q(1))]*(2*n)+[(Q(0),b[-1][1])]
    if global_required and not full:raise ValueError('restricted')
    visited=set();leaves=[]
    def walk(key,box):
        if key in visited:raise ValueError('reuse')
        visited.add(key); node=z['nodes'][key]
        if node['type']=='SPLIT':
            d=node['coordinate'];p=Q(node['cut']);a,v=box[d]
            if not a<p<v:raise ValueError('cut')
            walk(node['left'],box[:d]+[(a,p)]+box[d+1:])
            walk(node['right'],box[:d]+[(p,v)]+box[d+1:])
        elif node['type']=='WITNESS':
            px,py=map(Q,node['point'])
            if px*px+py*py>1:raise ValueError('point')
            gaps=[]
            for j in range(n):
                # Coordinate projection formula differs from primary's case split.
                xlo,xhi=box[2*j];ylo,yhi=box[2*j+1]
                cx=min(xhi,max(xlo,px));cy=min(yhi,max(ylo,py))
                gap=(px-cx)**2+(py-cy)**2-box[-1][1]
                if gap<=0:raise ValueError('gap')
                gaps.append(gap)
            leaves.append(str(min(gaps)))
        else:raise ValueError('unsupported example leaf')
    walk(z['root'],b)
    if visited!=set(z['nodes']):raise ValueError('unused')
    return {'full_domain':full,'nodes':len(visited),'strict_leaf_margins':leaves}
results=[check(data['examples'][0],True),check(data['examples'][1],False)]
if results[0]['strict_leaf_margins']!=['1/100','1/100']:raise ValueError('single disk margin')
if results[1]['strict_leaf_margins']!=['1/20']:raise ValueError('100 center margin')
try:check(data['examples'][1],True)
except ValueError:upgrade_rejected=True
else:raise ValueError('global upgrade accepted')
out=R/'verify/out/n100-global-witness-tree-independent.json'
if out.exists():raise ValueError('refuse overwrite')
out.write_text(json.dumps({'verified':True,'arithmetic':'Fraction only','results':results,
    'restricted_upgrade_rejected':upgrade_rejected,'n100_global_optimality':False,
    'scope':'Independent replay of the two saved witness-tree examples; not an exhaustive audit of all verifier inputs or a formal compactness proof.',
    'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
    'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
print('PASS independent recursive replay; margins 1/100, 1/100, 1/20; restricted upgrade rejected')
