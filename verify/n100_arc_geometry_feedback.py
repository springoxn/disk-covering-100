"""Bounded feedback between finite label supports and inherited continuous boxes."""
from pathlib import Path
import json,hashlib
import n100_arc_rebuilt_relations as R
from n100_circle_center_alternating import coupled,independent
from n100_arc_ranked_projection import width
ROOT=R.ROOT

def main():
 source='verify/out/n100-arc-rebuilt-relations.json';src=R.load(source);p=src['placement'];node=src['source_node'];core=R.load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in R.load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=R.setup(core,p,prior);_,IE,Iq=independent.setup(core,p,prior);_,adj,_=R.build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};order=src['boundary_order'];clauses=src['clauses'];B=src['geometry_result']['boxes'];D={int(v):b for v,b in src['supported_domains'].items()};relations=[]
 for r in src['relations']:relations.append(dict(r,forward={int(j):b for j,b in r['forward'].items()},reverse={int(j):b for j,b in r['reverse'].items()}))
 history=[];lastcount=src['summary']['assignments_after'];stop='iteration_limit';root_excluded=False;witnesses=src['anchor_witnesses']
 for iteration in range(1,7):
  oldB=[b[:] for b in B];oldD=D.copy();oldrelations=relations;P=[b[:] for b in B]
  for v,bits in D.items():
   parts=[R.intersect(B[v],R.independent_tile(j,256,signs[q[v-100]])) for j in R.labels(bits)];parts=[b for b in parts if b is not None];R.need(parts,'feedback support pieces');P[v]=[min(b[0] for b in parts),max(b[1] for b in parts),min(b[2] for b in parts),max(b[3] for b in parts)]
  a=coupled(P,E,q,pairs,limit=160);b=coupled(P,IE,Iq,pairs,alt=True,limit=160);R.need(a==b,'feedback alternate geometry')
  if a['excluded']:
   history.append({'iteration':iteration,'phase':'continuous','proof':a});root_excluded=True;stop='continuous_empty';break
  R.need(a['fixed'],'continuous cap');r=R.run(a['boxes'],E,q,pairs,limit=80)
  if r['excluded']:
   history.append({'iteration':iteration,'phase':'arc_projection','proof':r});root_excluded=True;stop='arc_empty';break
  R.need(r['fixed'],'arc projection cap');B=r['boxes'];R.audit_terminal(B,E,q,r['masks'],256);R.need(all(x[2*k]<=y[2*k]<=y[2*k+1]<=x[2*k+1] for x,y in zip(oldB,B) for k in (0,1)),'feedback box nesting');initial={v:D[v]&R.mask(r['masks'][str(v-100)]) for v in D};pieces={(v,j):R.intersect(B[v],R.independent_tile(j,256,signs[q[v-100]])) for v,bits in initial.items() for j in R.labels(bits)};R.need(all(b is not None for b in pieces.values()),'feedback retained tiles');relations=[]
  for old in oldrelations:
   f,v,w=old['face'],old['v'],old['w'];F={j:R.checked_contract(B[f],pieces[v,j],R.radiussquared(1)) for j in R.labels(initial[v])};G={j:R.checked_contract(B[f],pieces[w,j],R.radiussquared(1)) for j in R.labels(initial[w])};R.need(all(b is not None for b in list(F.values())+list(G.values())),'feedback center support');forward={j:0 for j in F};reverse={j:0 for j in G}
   for j in F:
    for k in R.labels(old['forward'][j]&initial[w]):
     if R.intersect(F[j],G[k]) is not None and R.support(pieces[v,j],pieces[w,k],R.radiussquared(2)):forward[j]|=1<<k;reverse[k]|=1<<j
   relations.append({'face':f,'v':v,'w':w,'forward':forward,'reverse':reverse})
  final,log,empty=R.propagate(initial,relations);R.replay_removals(initial,relations,log,final);lookup={frozenset((r['v'],r['w'])):r for r in relations};tables=[];same=[]
  for i,v in enumerate(order):
   w=order[(i+1)%len(order)];rel=lookup[frozenset((v,w))];tables.append(rel['forward'] if rel['v']==v else rel['reverse']);same.append(q[v-100]==q[w-100])
  marks=R.range_marks(order,final,clauses);support,witnesses,stats=R.state_dp([final[v] for v in order],tables,same,marks,len(clauses));count,counts=R.count_dp([final[v] for v in order],tables,same,marks,len(clauses));D=dict(zip(order,support));R.need(count<=lastcount and all(bits&~oldD[v]==0 for v,bits in D.items()),'feedback finite nesting');history.append({'iteration':iteration,'phase':'finite','labels_before':sum(b.bit_count() for b in oldD.values()),'labels_after':sum(b.bit_count() for b in D.values()),'width_before':width(oldB),'width_after':width(B),'assignments_before':lastcount,'assignments_after':count,'geometry_result':r,'initial_domains':initial,'arc_domains':final,'removals':log,'supported_domains':D,'relations':relations,'state_statistics':stats});lastcount=count;print('FEEDBACK',iteration,'labels',history[-1]['labels_before'],history[-1]['labels_after'],'width',width(oldB),width(B),'count',count,flush=True)
  if not any(D.values()):root_excluded=True;stop='finite_empty';break
  if B==oldB and D==oldD and relations==oldrelations:stop='fixed';break
 out=ROOT/'verify/out/n100-arc-geometry-feedback.json';R.need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_rebuilt_relations.py','verify/n100_arc_nogood_state_dp.py','verify/n100_arc_learning_counts.py','verify/n100_arc_center_projection.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-arc-geometry-feedback/v1','verified_integer_bounded_feedback':True,'all_continuous_alternate_results_equal':True,'all_terminal_arc_masks_audited':True,'all_arc_removals_replayed':True,'placement':p,'source_node':node,'iteration_limit':6,'stop':stop,'root_excluded':root_excluded,'history':history,'clauses':clauses,'boundary_order':order,'final_boxes':B,'final_supported_domains':D,'final_relations':relations,'final_assignment_count':lastcount,'final_anchor_witnesses':witnesses,'scope':'bounded feedback for one inherited leaf, fixed is relaxation fixed point only; shared DP/count definitions, not an independent covering proof','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS geometry feedback',stop,'labels',sum(b.bit_count() for b in D.values()),'count',lastcount,'root',root_excluded)
if __name__=='__main__':main()
