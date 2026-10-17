"""Complete single-boundary-vertex arc lookahead on inherited child1."""
from pathlib import Path
import json,hashlib
from n100_arc_nogood_state_dp import ROOT,load,need,state_dp,labels
from n100_arc_range_nogood import range_marks
from n100_arc_center_projection import run,setup,build
from n100_boundary_arc_class32 import audit_terminal
from n100_arc_pair_consistency import intersect,independent_tile
from n100_circle_center_alternating import coupled,independent
from n100_arc_ranked_projection import width

def mask(items):return sum(1<<j for j in items)
def main():
 source='verify/out/n100-arc-conflict-branch.json';src=load(source);child=next(c for c in src['children'] if c['child']==1);need(not child['excluded'],'child unresolved');B=child['arc_result']['boxes'];D={int(v):b for v,b in child['final_supported_domains'].items()};vtest=169;trials=labels(D[vtest]);need(trials,'nonempty complete label trial set');model=load('verify/out/n100-arc-geometry-feedback.json');median=load('verify/out/n100-arc-median-learning.json');clauses=median['clauses'];order=median['boundary_order'];p=src['placement'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);_,IE,Iq=independent.setup(core,p,prior);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};lookup={frozenset((r['v'],r['w'])):r for r in model['final_relations']};tables=[];same=[]
 for i,v in enumerate(order):
  w=order[(i+1)%len(order)];r=lookup[frozenset((v,w))];tables.append({int(j):b for j,b in (r['forward'] if r['v']==v else r['reverse']).items()});same.append(q[v-100]==q[w-100])
 rows=[];union={v:0 for v in D};kept_boxes=[]
 for j in trials:
  P=[b[:] for b in B];box=intersect(B[vtest],independent_tile(j,256,signs[q[vtest-100]]));need(box is not None,'parent supported arc');P[vtest]=box;a=coupled(P,E,q,pairs,limit=160);b=coupled(P,IE,Iq,pairs,alt=True,limit=160);need(a==b,'lookahead alternate geometry');row={'label':j,'continuous_result':a}
  if a['excluded']:row.update({'excluded':True,'phase':'continuous'});rows.append(row);print('LOOK',j,'continuous empty',flush=True);continue
  arc=run(a['boxes'],E,q,pairs,limit=80);row['arc_result']=arc
  if arc['excluded']:row.update({'excluded':True,'phase':'arc'});rows.append(row);print('LOOK',j,'arc empty',flush=True);continue
  F={v:D[v]&mask(arc['masks'][str(v-100)]) for v in D} if arc['fixed'] else D.copy();F[vtest]&=1<<j
  if arc['fixed']:audit_terminal(arc['boxes'],E,q,arc['masks'],256)
  support,witnesses,stats=state_dp([F[v] for v in order],tables,same,range_marks(order,F,clauses),len(clauses));S=dict(zip(order,support));empty=not any(support)
  for w in witnesses:
   vals=dict(zip(order,(s[0] for s in w)));need(vals[vtest]==j and all(any(not lo<=vals[v]<=hi for v,lo,hi in c) for c in clauses),'lookahead witness label and clauses')
  row.update({'excluded':empty,'phase':'finite','supported_domains':S,'anchor_witnesses':witnesses,'state_statistics':stats});rows.append(row)
  if not empty:
   for v,bits in S.items():need(bits&~D[v]==0,'subset supports');union[v]|=bits
   kept_boxes.append(arc['boxes'])
  print('LOOK',j,'finite empty',empty,'labels',sum(bits.bit_count() for bits in support),flush=True)
 need([r['label'] for r in rows]==trials,'every parent label tested exactly once');hull=None
 if kept_boxes:
  hull=[[min(C[i][0] for C in kept_boxes),max(C[i][1] for C in kept_boxes),min(C[i][2] for C in kept_boxes),max(C[i][3] for C in kept_boxes)] for i in range(len(B))];need(all(a[2*k]<=b[2*k]<=b[2*k+1]<=a[2*k+1] for a,b in zip(B,hull) for k in (0,1)),'union hull nested in parent')
 summary={'tested_vertex':vtest,'tested_label_count':len(trials),'excluded_labels':[r['label'] for r in rows if r['excluded']],'retained_labels':[r['label'] for r in rows if not r['excluded']],'parent_supported_labels':sum(bits.bit_count() for bits in D.values()),'union_supported_labels':sum(bits.bit_count() for bits in union.values()),'whole_child_labels_removed':sum((D[v]&~union[v]).bit_count() for v in D),'parent_width':width(B),'union_hull_width':width(hull) if hull else None,'source_child_excluded':not kept_boxes};out=ROOT/'verify/out/n100-arc-singleton-lookahead.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-geometry-feedback.json','verify/out/n100-arc-median-learning.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_nogood_state_dp.py','verify/n100_arc_range_nogood.py','verify/n100_arc_center_projection.py','verify/n100_boundary_arc_class32.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_circle_center_alternating.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-arc-singleton-lookahead/v1','verified_integer_complete_single_vertex_lookahead':True,'all_initial_continuous_alternate_equal':True,'all_fixed_arc_masks_audited':True,'every_parent_label_tested':True,'placement':p,'source_node':27,'source_child':1,'summary':summary,'trials':rows,'union_supported_domains':union,'retained_box_hull':hull,'scope':'all supported labels of one vertex in one parent; closed tile endpoints may overlap; finite pair relations inherited, no independent full DP replay','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS singleton lookahead',summary)
if __name__=='__main__':main()
