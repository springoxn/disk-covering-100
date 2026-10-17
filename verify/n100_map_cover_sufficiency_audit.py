"""Arithmetic/combinatorial audit for coverage sufficiency of closed disk-map models.
Winding-number theorem is an explicit analytic dependency, not machine formalized.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib,argparse
import sympy as S
from n100_dart_map_canonicalization import permutations
from n100_generic_map_compiler import compile_model
from n100_small_map_enumeration_calibration import cycles
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def audit(g):
    need(1<=len(g['faces'])<=100,'n100 face count')
    model=compile_model(g)
    phi,tags=permutations(g);n=len(phi)
    outer_darts=[d for d in range(n) if tags[d][0]=='outer']
    face_cycles=cycles([phi[d] for d in range(n)])
    outer_cycles=[row for row in face_cycles if row[0] in outer_darts]
    need(len(outer_cycles)==1 and set(outer_cycles[0])==set(outer_darts),'single outer cycle')
    origins=[g['edges'][d//2]['ends'][d%2] for d in outer_cycles[0]]
    claimed=list(reversed(g['boundary_cycle']))
    need(len(origins)==len(claimed) and any(origins==claimed[k:]+claimed[:k] for k in range(len(claimed))),'oriented outer boundary match')
    inner=[d for d in range(n) if tags[d][0]=='inner'];outer=[d for d in range(n) if tags[d][0]=='outer']
    signed=Counter()
    for d in inner:signed[d//2]+=1 if d%2==0 else -1
    boundary=Counter()
    for d in outer:boundary[d//2]+=-(1 if d%2==0 else -1)
    need({e:c for e,c in signed.items() if c}=={e:c for e,c in boundary.items() if c},'oriented edge cancellation')
    need(len(outer)==len(g['boundary_cycle']),'outer size')
    ids={e for e in boundary};need(all(sum(d//2==e for d in inner)==1 for e in ids),'boundary owner')
    need(all(sum(d//2==e for d in inner)==2 for e in range(n//2) if e not in ids),'internal two sides')
    cycle=g['boundary_cycle'];marks=g['axis_marks'];root=cycle.index(marks[0]);rot=cycle[root:]+cycle[:root];indices=[rot.index(v) for v in marks]
    need(indices==sorted(indices) and len(set(marks))==4,'axis cyclic order')
    return {'vertices':len(g['vertices']),'faces':len(g['faces']),'edges':n//2,'outer_arcs':len(outer),'internal_oriented_pairs_cancel':n//2-len(outer),'one_owner_per_boundary_arc':True,'compiler_reaccepted':True,'compiled_variables':model['variables'],'oriented_outer_cycle_matches':True,'axis_order_preserved':True}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-map-cover-sufficiency-audit.json');args=ap.parse_args()
    lam,dot,A,e1,e2,s=S.symbols('lambda dot A e1 e2 s',real=True)
    checks={}
    # p,q unit and dot=p.q, v=(1-lambda)p+lambda*q; s=|v|.
    checks['convex_chord_norm']=S.expand((1-lam)**2+lam**2+2*lam*(1-lam)*dot-(1-2*lam*(1-lam)*(1-dot)))==0
    # 2c.p=A+e1 and 2c.q=A+e2; normalize v to short-arc point x.
    checks['normalized_arc_slack']=S.simplify(((1-lam)*(A+e1)+lam*(A+e2))/s-A-((1-lam)*e1+lam*e2+A*(1-s))/s)==0
    need(all(checks.values()),'symbolic identities')
    # Explicit rational negative control for omitting t<=1.
    p=(F(3,5),F(4,5));q=(F(-3,5),F(4,5));c=(F(0),F(-1,10));x=(F(0),F(1));t=F(117,100)
    def distance(u,v):return sum((a-b)**2 for a,b in zip(u,v))
    need(distance(p,c)==t and distance(q,c)==t and distance(x,c)>t,'t>1 counterexample')
    paths=[ROOT/'verify/out/n100-candidate-clipped-map.json',ROOT/'verify/out/n100-expanded-map-models.json',ROOT/'verify/out/n100-one-interior-map-enumeration.json']
    maps=[('candidate100',json.loads(paths[0].read_text(encoding='utf-8')))]
    expanded=json.loads(paths[1].read_text(encoding='utf-8'))
    for f in expanded['families']:
        for j,item in enumerate(f['models']):maps.append((str(f['boundary_vertices'])+'-'+str(f['inner_faces'])+'-'+str(j),item['map']))
    interior=json.loads(paths[2].read_text(encoding='utf-8'))
    maps.extend(('interior-'+str(j),item['map']) for j,item in enumerate(interior['models']))
    rows=[{'label':label,'audit':audit(g)} for label,g in maps];need(len(rows)==62,'map total')
    # Reversing a single face would defeat orientation; shared adapter reorients valid inputs.
    # No arbitrary embedding or noncrossing assumption is used by winding cancellation.
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    output={'schema':'n100-map-cover-sufficiency-audit/v1','verified_symbolic_and_combinatorial':True,'symbolic_identities':checks,'sympy_version':S.__version__,'maps_audited':len(rows),'rows':rows,
        't_le_1_necessary_for_arc_lemma_control':{'p':list(map(str,p)),'q':list(map(str,q)),'center':list(map(str,c)),'t':str(t),'uncovered_arc_midpoint':list(map(str,x)),'midpoint_distance_squared':str(distance(x,c))},
        'conditional_sufficiency_claim':'Any exact feasible assignment of a valid connected oriented disk map accepted by the compiler covers the closed unit disk, under the listed analytic winding/arc lemmas. Coordinate edges need not embed without crossings.',
        'analytic_dependencies':['ordered unit-circle quadrant chains yield short arcs covering the circle once, allowing collapsed vertices','normalization of positive convex combinations of nonantipodal endpoints parameterizes their short arc','convex disks contain segments between face vertices; t<=1 endpoint constraints imply boundary arc containment','winding number is additive under concatenation and sums of oriented chains','a loop wholly in a convex disk has winding zero about any point outside that disk','positively oriented unit circle has winding one about every point in its interior','covering all interior points by a finite closed union covers its closure'],
        'machine_verified_geometry':False,'global_optimality':False,'n100_all_map_completeness_proven':False,
        'scope':'sufficiency interface audit, not feasibility solving or completeness of global map enumeration',
        'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+[ROOT/'verify/n100_generic_map_compiler.py',ROOT/'verify/n100_dart_map_canonicalization.py']},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8');print('PASS short-arc slack identities;62 map oriented boundary cancellations; t>1 negative control; winding geometry explicitly nonformal')
if __name__=='__main__':main()
