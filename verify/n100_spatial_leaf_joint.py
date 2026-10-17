"""Apply inherited finite Voronoi relations and twelve nogoods to all spatial leaves."""
from pathlib import Path
import json,hashlib
from n100_arc_nogood_state_dp import ROOT,load,need,state_dp,labels
from n100_arc_range_nogood import range_marks
from n100_arc_center_projection import run,build,setup
from n100_boundary_arc_class32 import audit_terminal
from n100_arc_ranked_projection import width

def mask(items):return sum(1<<j for j in items)
def main():
 source='verify/out/n100-center-spatial-tree.json';tree=load(source);parentfile='verify/out/n100-arc-conflict-branch.json';parent=load(parentfile);branch=next(c for c in parent['children'] if c['child']==1);need(not branch['excluded'],'unresolved parent');model=load('verify/out/n100-arc-geometry-feedback.json');median=load('verify/out/n100-arc-median-learning.json');p=tree['placement'];need(p==parent['placement']==model['placement']==median['placement'] and all(z['source_node']==27 for z in (tree,parent,model,median)),'parent placement bindings');D={int(v):b for v,b in branch['final_supported_domains'].items()};order=median['boundary_order'];clauses=median['clauses'];need(len(clauses)==12,'twelve inherited clauses');core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});lookup={frozenset((r['v'],r['w'])):r for r in model['final_relations']};T=[];same=[]
 for i,v in enumerate(order):
  w=order[(i+1)%len(order)];r=lookup[frozenset((v,w))];T.append({int(j):b for j,b in (r['forward'] if r['v']==v else r['reverse']).items()});same.append(q[v-100]==q[w-100])
 leaves=[n for n in tree['nodes'] if n['kind']=='unresolved'];need(len(leaves)==32,'complete tree leaf count');rows=[]
 for index,node in enumerate(leaves,1):
  B=node['result']['boxes'];a=run(B,E,q,pairs,limit=80);row={'tree_node':node['id'],'arc_result':a,'width_before':width(B)}
  if a['excluded']:row.update({'excluded':True,'phase':'arc_projection'});rows.append(row);print('JOINT',index,'node',node['id'],'arc excluded',flush=True);continue
  # Only use masks recomputed at a verified fixed point. Capped boxes remain unresolved.
  if not a['fixed']:row.update({'excluded':False,'phase':'arc_capped'});rows.append(row);print('JOINT',index,'node',node['id'],'arc capped',flush=True);continue
  audit_terminal(a['boxes'],E,q,a['masks'],256);F={v:bits&mask(a['masks'][str(v-100)]) for v,bits in D.items()};m=range_marks(order,F,clauses);support,witnesses,stats=state_dp([F[v] for v in order],T,same,m,len(clauses))
  for witness in witnesses:
   vals=dict(zip(order,(s[0] for s in witness)));need(all(any(not lo<=vals[v]<=hi for v,lo,hi in c) for c in clauses),'leaf witness satisfies twelve clauses');need(all(F[v]&(1<<vals[v]) for v in order),'leaf mask membership');need(all(T[i][vals[v]]&(1<<vals[order[(i+1)%len(order)]]) for i,v in enumerate(order)),'leaf inherited pair relations')
  row.update({'excluded':not any(support),'phase':'finite_support','labels_before':sum(b.bit_count() for b in D.values()),'labels_after_arc_masks':sum(b.bit_count() for b in F.values()),'labels_after_twelve_clauses':sum(b.bit_count() for b in support),'supported_domains':dict(zip(order,support)),'anchor_witnesses':witnesses,'state_statistics':stats,'width_after':width(a['boxes'])});rows.append(row);print('JOINT',index,'node',node['id'],'labels',row['labels_after_twelve_clauses'],'excluded',row['excluded'],flush=True)
 need({r['tree_node'] for r in rows}=={n['id'] for n in leaves},'every spatial leaf processed exactly once');byid={r['tree_node']:r for r in rows}
 def closed(i):
  n=tree['nodes'][i]
  if n['kind']=='excluded':return True
  if n['kind']=='unresolved':return byid[i]['excluded']
  return all(closed(j) for j in n['children'])
 summary={'leaf_count':len(rows),'strictly_excluded_leaves':sum(r['excluded'] for r in rows),'unresolved_leaves':sum(not r['excluded'] for r in rows),'source_child_excluded':closed(0),'sum_leaf_width_reductions':sum(r['width_before']-r['width_after'] for r in rows if 'width_after' in r),'leaf_label_min':min((r['labels_after_twelve_clauses'] for r in rows if 'labels_after_twelve_clauses' in r),default=None),'leaf_label_max':max((r['labels_after_twelve_clauses'] for r in rows if 'labels_after_twelve_clauses' in r),default=None)};out=ROOT/'verify/out/n100-spatial-leaf-joint.json';need(not out.exists(),'overwrite');paths=[source,parentfile,'verify/out/n100-arc-geometry-feedback.json','verify/out/n100-arc-median-learning.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_center_projection.py','verify/n100_boundary_arc_class32.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_arc_nogood_state_dp.py','verify/n100_arc_range_nogood.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_circle_center_alternating.py'];out.write_text(json.dumps({'schema':'n100-spatial-leaf-joint/v1','verified_integer_joint_leaf_tests':True,'all_terminal_masks_audited':True,'every_spatial_leaf_processed':True,'placement':p,'source_node':27,'source_child':1,'summary':summary,'boundary_order':order,'clauses':clauses,'leaves':rows,'scope':'32 spatial boxes of one conditional child, inherited pair relations and twelve nogoods; finite support machinery shared; no exact covering feasibility or full geometric replay independence','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS joint spatial leaves',summary)
if __name__=='__main__':main()
