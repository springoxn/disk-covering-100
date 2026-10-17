"""Filter shared-center tile relations by necessary closed-arc CCW order."""
from pathlib import Path
from fractions import Fraction
import json,hashlib
from n100_arc_pair_consistency import ROOT,load,need,labels,mask,propagate,replay_removals
from n100_arc_cycle_support import cycle,bit_dp,set_dp
from n100_boundary_order import ordered_vertices
from n100_boundary_circle_propagation import setup

def allowed(j,k):return j<=k+1

def main():
 controls=0
 for j in range(256):
  for k in range(256):
   need(allowed(j,k)==(Fraction(j,256)<=Fraction(k+1,256)),'independent closed interval order');controls+=1
 need(allowed(17,16) and not allowed(18,16),'closed shared endpoint control')
 source='verify/out/n100-arc-pair-consistency.json';core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];boundary=ordered_vertices(core);need(boundary==ordered_vertices(core,True),'independent boundary traversal');ccw=set(zip(boundary,boundary[1:]+boundary[:1]));prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};rows=[]
 for old in load(source)['cases']:
  p=old['placement'];_,E,q=setup(core,p,prior[tuple(p)]);D={int(v):b for v,b in old['final_domains'].items()};relations=[];before=after=ordered_edges=0
  for r in old['relations']:
   v,w=r['v'],r['w'];need((v,w) in ccw or (w,v) in ccw,'relation is boundary neighbor');same=q[v-100]==q[w-100];ordered_edges+=same;forward={int(j):0 for j in r['forward']};reverse={int(k):0 for k in r['reverse']}
   for rawj,bits in r['forward'].items():
    j=int(rawj)
    for k in labels(bits):
     before+=1;ok=not same or (allowed(j,k) if (v,w) in ccw else allowed(k,j))
     if ok:forward[j]|=1<<k;reverse[k]|=1<<j;after+=1
   relations.append({'face':r['face'],'v':v,'w':w,'forward':forward,'reverse':reverse})
  need(ordered_edges==28,'28 same-quadrant edges');final,log,empty=propagate(D,relations);replay_removals(D,relations,log,final)
  model={'relations':relations,'final_domains':final};order,domains,tables=cycle(model);support,witnesses=bit_dp(domains,tables);need(support==set_dp(domains,tables),'independent global support')
  need(not empty or not any(support),'arc-empty then cycle-empty')
  for witness in witnesses:need(all(domains[i]&(1<<j) for i,j in enumerate(witness)) and all(tables[i][witness[i]]&(1<<witness[(i+1)%len(order)]) for i in range(len(order))),'witness')
  if old['source_node'] is None:need(any(support),'candidate rejected: investigate')
  rows.append({'placement':p,'source_node':old['source_node'],'pairs_before':before,'pairs_after':after,'pair_order_rejections':before-after,'initial_labels':sum(b.bit_count() for b in D.values()),'labels_after_arc_consistency':sum(b.bit_count() for b in final.values()),'labels_after_exact_cycle':sum(b.bit_count() for b in support),'excluded':not any(support),'removals':log,'domains_after_arc_consistency':final,'cycle_order':order,'globally_supported_domains':dict(zip(order,support)),'anchor_witnesses':witnesses,'relations':relations});print('ordered cycle',p,'node',old['source_node'],'pair removals',before-after,'labels',rows[-1]['initial_labels'],rows[-1]['labels_after_arc_consistency'],rows[-1]['labels_after_exact_cycle'],'excluded',rows[-1]['excluded'],flush=True)
 out=ROOT/'verify/out/n100-arc-ordered-cycle.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_boundary_order.py','verify/n100_arc_pair_consistency.py','verify/n100_arc_cycle_support.py'];out.write_text(json.dumps({'schema':'n100-arc-ordered-cycle/v1','verified_integer_rational_tests':True,'rational_interval_order_controls':controls,'shared_endpoint_retained':True,'independent_boundary_traversal_equal':True,'all_removal_replays_passed':True,'independent_set_dp_all_equal':True,'candidate_retained':True,'cases':rows,'scope':'closed same-quadrant CCW necessary order on two inherited pair models; finite support not continuous feasibility; no nonadjacent order constraints','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS ordered cycle')
if __name__=='__main__':main()
