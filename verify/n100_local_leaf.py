"""A scoped LOCAL leaf verifier, not a global search-tree completeness checker.
Accepts only boxes close to the labelled root and strictly below its squared radius.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
bp=R/'verify/out/n100-local-widened-budget.json';ip=R/'verify/out/n100-local-widened-independent.json';mp=R/'runtime/external-disk100-strict-local-replay/source/rational_midpoint.json'
b=load(bp);i=load(ip);mid=load(mp);assert b['verified'] and i['audit_verified']
for path,digest in b['dependencies_sha256'].items():assert sha(R/path)==digest
assert b['checker_sha256']==sha(R/'verify/n100_local_widened_budget.py')
D=int(mid['denominator']);x=[F(int(v),D) for v in mid['numerators']];rho=F(1,10**58);radius=F(b['constants']['ungauged_center_radius'])
binding={str(p.relative_to(R)).replace('\\','/'):sha(p) for p in [bp,ip,mp]}
def verify_leaf(leaf):
 assert leaf['type']=='LOCAL_ROOT_CENTER_BOX'
 assert leaf['binding']==binding
 coords=leaf['center_intervals'];assert len(coords)==200
 for j,raw in enumerate(coords):
  lo,hi=map(F,raw);assert lo<=hi
  assert max(abs(lo-x[j]),abs(hi-x[j]))+rho<=radius
 lo,hi=map(F,leaf['squared_radius_interval']);assert 0<=lo<=hi
 assert hi<x[492]-rho # sufficient strict root comparison, no floating algebraic approximation
 return True
half=F(1,10**38);leaf={'schema':'n100-local-root-center-box/v1','type':'LOCAL_ROOT_CENTER_BOX','binding':binding,'center_intervals':[[str(v-half),str(v+half)] for v in x[:200]],'squared_radius_interval':['0',str(x[492]-2*rho)]}
assert verify_leaf(leaf)
rejected=[]
for name,change in [('oversized_center_box',lambda z:z['center_intervals'].__setitem__(0,[str(x[0]-F(1,10**20)),str(x[0]+F(1,10**20))])),('radius_not_below_root',lambda z:z.__setitem__('squared_radius_interval',['0',str(x[492]+rho)])),('missing_coordinate',lambda z:z['center_intervals'].pop()),('altered_dependency_binding',lambda z:z['binding'].__setitem__(str(bp.relative_to(R)).replace('\\','/'),'0'*64))]:
 z=copy.deepcopy(leaf);change(z)
 try:verify_leaf(z)
 except AssertionError:rejected.append(name)
assert len(rejected)==4
lp=R/'verify/out/n100-local-leaf-example.json';op=R/'verify/out/n100-local-leaf-check.json';assert not lp.exists() and not op.exists()
lp.write_text(json.dumps(leaf,indent=2)+'\n',encoding='utf-8')
op.write_text(json.dumps({'schema':'n100-local-leaf-check/v1','verified':True,'leaf_sha256':sha(lp),'leaf_path':str(lp.relative_to(R)).replace('\\','/'),'center_coordinates_checked':200,'gauge_required':False,'rejected_controls':rejected,'scope':'This one LOCAL leaf excludes coverings in its labelled center box and squared-radius interval. No assertion that any larger domain is partitioned by these leaves.','global_partition_tree_supplied':False,'topology_enumeration_supplied':False,'global_optimality':False,'minimal_polynomial_obtained':False,'dependencies_sha256':binding,'checker_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8')
print('PASS concrete LOCAL leaf: 200 center intervals, strict root radius comparison and 4 corruptions rejected; global tree absent')
