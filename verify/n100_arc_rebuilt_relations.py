"""Rebuild finite pair support using learned, propagated continuous parent boxes."""
from pathlib import Path
import json,hashlib
from n100_arc_nogood_state_dp import ROOT,load,need,labels,state_dp
from n100_arc_range_nogood import range_marks
from n100_arc_learning_counts import count_dp
from n100_arc_center_projection import run,checked_contract,build,radiussquared
from n100_boundary_arc_class32 import audit_terminal
from n100_arc_pair_consistency import mask,propagate,replay_removals,setup,intersect,support,independent_tile

def main():
 source='verify/out/n100-arc-ranked-projection.json';rankedsource='verify/out/n100-arc-ranked-witnesses.json';src=load(source);z=load(rankedsource);p=z['placement'];node=z['source_node'];learned=z['learned'];oldD={int(v):b for v,b in learned['supported_domains'].items()};order=z['boundary_order'];clauses=learned['clauses'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});initialB=src['result']['boxes'];r=run(initialB,E,q,pairs,limit=80);need(not r['excluded'] and r['fixed'],'projection empty or capped: inspect before continuation');B=r['boxes'];need(all(a[2*k]<=b[2*k]<=b[2*k+1]<=a[2*k+1] for a,b in zip(initialB,B) for k in (0,1)),'narrowed parent nesting');audit_terminal(B,E,q,r['masks'],256);D={v:oldD[v]&mask(r['masks'][str(v-100)]) for v in oldD};need(all(D.values()),'domain empty after verified masks: inspect');signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};pieces={}
 for v,bits in D.items():
  for j in labels(bits):
   b=intersect(B[v],independent_tile(j,256,signs[q[v-100]]));need(b is not None,'retained piece');pieces[v,j]=b
 oldmodel=next(c for c in load('verify/out/n100-arc-ordered-cycle.json')['cases'] if c['placement']==p and c['source_node']==node);relations=[];tested=accepted=0
 for old in oldmodel['relations']:
  f,v,w=old['face'],old['v'],old['w'];P={j:checked_contract(B[f],pieces[v,j],radiussquared(1)) for j in labels(D[v])};Q={j:checked_contract(B[f],pieces[w,j],radiussquared(1)) for j in labels(D[w])};need(all(b is not None for b in list(P.values())+list(Q.values())),'terminal center projections');forward={j:0 for j in P};reverse={k:0 for k in Q}
  for j in P:
   for k in labels(int(old['forward'][str(j)])&D[w]):
    tested+=1;overlap=intersect(P[j],Q[k]) is not None;alt=all(max(P[j][2*t],Q[k][2*t])<=min(P[j][2*t+1],Q[k][2*t+1]) for t in (0,1));need(overlap==alt,'new center overlap audit');good=overlap and support(pieces[v,j],pieces[w,k],radiussquared(2))
    if good:forward[j]|=1<<k;reverse[k]|=1<<j;accepted+=1
  relations.append({'face':f,'v':v,'w':w,'forward':forward,'reverse':reverse})
 final,log,empty=propagate(D,relations);replay_removals(D,relations,log,final);lookup={frozenset((r['v'],r['w'])):r for r in relations};tables=[];same=[]
 for i,v in enumerate(order):
  w=order[(i+1)%len(order)];row=lookup[frozenset((v,w))];tables.append(row['forward'] if row['v']==v else row['reverse']);same.append(q[v-100]==q[w-100])
 m=range_marks(order,final,clauses);a,witnesses,stats=state_dp([final[v] for v in order],tables,same,m,len(clauses));n,acounts=count_dp([final[v] for v in order],tables,same,m,len(clauses));need(n<=learned['assignment_count_after'] and all(b&~oldD[v]==0 for v,b in zip(order,a)),'new model strengthens inherited support')
 for w in witnesses:
  values=dict(zip(order,(s[0] for s in w)));need(all(any(not lo<=values[v]<=hi for v,lo,hi in c) for c in clauses),'new model respects all nine clauses')
 summary={'old_supported_labels':sum(b.bit_count() for b in oldD.values()),'after_geometry_masks':sum(b.bit_count() for b in D.values()),'after_arc_consistency':sum(b.bit_count() for b in final.values()),'after_nine_clause_support':sum(b.bit_count() for b in a),'old_accepted_pairs_tested':tested,'new_pairs_accepted':accepted,'new_pair_rejections':tested-accepted,'assignments_before':learned['assignment_count_after'],'assignments_after':n,'root_excluded':not any(a),'projection_sweeps':r['sweeps']};out=ROOT/'verify/out/n100-arc-rebuilt-relations.json';need(not out.exists(),'overwrite');paths=[source,rankedsource,'verify/out/n100-arc-ordered-cycle.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_nogood_state_dp.py','verify/n100_arc_learning_counts.py','verify/n100_arc_range_nogood.py','verify/n100_arc_center_projection.py','verify/n100_boundary_arc_class32.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_arc_pair_consistency.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py'];out.write_text(json.dumps({'schema':'n100-arc-rebuilt-relations/v1','verified_integer_rebuild':True,'terminal_masks_independently_audited':True,'all_projection_contractors_equal':True,'all_removals_replayed_with_sets':True,'placement':p,'source_node':node,'summary':summary,'geometry_result':r,'initial_domains':D,'domains_after_arc_consistency':final,'removals':log,'relations':relations,'boundary_order':order,'clauses':clauses,'supported_domains':dict(zip(order,a)),'anchor_witnesses':witnesses,'state_statistics':stats,'anchor_assignment_counts':acounts,'scope':'one inherited parent, necessary finite model rebuilt from smaller boxes; shared DP/count machinery, not independent end-to-end proof','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS rebuilt relations',summary)
if __name__=='__main__':main()
