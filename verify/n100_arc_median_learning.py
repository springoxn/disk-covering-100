"""Bounded median-rank learning on the stage82 fixed parent."""
from pathlib import Path
from fractions import Fraction
import json,hashlib
from n100_arc_ranked_witnesses import ROOT,load,need,unrank,range_marks,state_dp,count_dp,setup,build,intersect,independent_tile,coupled,independent
from n100_arc_ranked_projection import width

def main():
 source='verify/out/n100-arc-geometry-feedback.json';z=load(source);need(z['stop']=='fixed' and not z['root_excluded'],'fixed starting parent');p=z['placement'];node=z['source_node'];order=z['boundary_order'];clauses=z['clauses'];base=z['final_boxes'];D={int(v):b for v,b in z['final_supported_domains'].items()};core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);_,IE,Iq=independent.setup(core,p,prior);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});lookup={frozenset((r['v'],r['w'])):r for r in z['final_relations']};T=[];same=[]
 for i,v in enumerate(order):
  w=order[(i+1)%len(order)];r=lookup[frozenset((v,w))];T.append({int(j):b for j,b in (r['forward'] if r['v']==v else r['reverse']).items()});same.append(q[v-100]==q[w-100])
 signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3}
 def test(restrictions):
  B=[b[:] for b in base]
  for v,lo,hi in restrictions:
   a=independent_tile(lo,256,signs[q[v-100]]);b=independent_tile(hi,256,signs[q[v-100]]);box=intersect(B[v],[min(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),max(a[3],b[3])]);need(box is not None,'median restriction nonempty');B[v]=box
  a=coupled(B,E,q,pairs,limit=160);b=coupled(B,IE,Iq,pairs,alt=True,limit=160);need(a==b,'median learning geometry alternate');return a
 history=[];last=z['final_assignment_count'];start_count=last;stop='iteration_limit';witnesses=[]
 for iteration in range(1,4):
  marks=range_marks(order,D,clauses);before,counts=count_dp([D[v] for v in order],T,same,marks,len(clauses));need(before==last,'exact count before next median')
  if not before:stop='finite_empty';break
  rank=before//2;w=unrank([D[v] for v in order],T,same,marks,len(clauses),counts,rank);assignment=[[v,s[0],s[0]] for v,s in zip(order,w)];vals={v:j for v,j,h in assignment};need(all(any(not lo<=vals[v]<=hi for v,lo,hi in c) for c in clauses),'median satisfies all inherited clauses');g=test(assignment)
  if not g['excluded']:history.append({'iteration':iteration,'learned':False,'rank':rank,'assignment':assignment,'geometry':g});stop='median_not_excluded';break
  active=[r[:] for r in assignment];trials=[]
  for r in assignment:
   trial=[a for a in active if a!=r];g=test(trial);trials.append({'kind':'remove','restriction':r,'excluded':g['excluded']})
   if g['excluded']:active=trial
  for i in range(len(active)):
   for side,target in ((1,0),(2,255)):
    accepted=active[i][side]
    if accepted==target:continue
    trial=[r[:] for r in active];trial[i][side]=target;g=test(trial);trials.append({'kind':'expand','i':i,'side':side,'value':target,'excluded':g['excluded']})
    if g['excluded']:active[i][side]=target;continue
    rejected=target
    while abs(rejected-accepted)>1:
     middle=(rejected+accepted)//2;trial=[r[:] for r in active];trial[i][side]=middle;g=test(trial);trials.append({'kind':'expand','i':i,'side':side,'value':middle,'excluded':g['excluded']})
     if g['excluded']:accepted=middle;active[i][side]=middle
     else:rejected=middle
  proof=test(active);need(active and proof['excluded'],'expanded median conflict proof');oldD=D.copy();clauses=clauses+[active];marks=range_marks(order,D,clauses);support,witnesses,stats=state_dp([D[v] for v in order],T,same,marks,len(clauses));after,counts=count_dp([D[v] for v in order],T,same,marks,len(clauses));D=dict(zip(order,support));need(after<=before and all(b&~oldD[v]==0 for v,b in D.items()),'learning nesting');ratio=Fraction(after,before);history.append({'iteration':iteration,'learned':True,'rank':rank,'median_assignment':assignment,'range_clause':active,'proof':proof,'trials':trials,'clauses_after':len(clauses),'labels_before':sum(b.bit_count() for b in oldD.values()),'labels_after':sum(b.bit_count() for b in D.values()),'assignments_before':before,'assignments_after':after,'retained_fraction':[ratio.numerator,ratio.denominator],'supported_domains':D,'state_statistics':stats});last=after;print('MEDIAN ROUND',iteration,'range',active,'labels',history[-1]['labels_before'],history[-1]['labels_after'],'assignments',before,after,flush=True)
  if not after:stop='finite_empty';break
 leaf_excluded=not last;P=[b[:] for b in base];continuous=None
 if not leaf_excluded:
  for v,bits in D.items():
   parts=[]
   for j in range(bits.bit_length()):
    if (bits>>j)&1:
     b=intersect(base[v],independent_tile(j,256,signs[q[v-100]]))
     if b is not None:parts.append(b)
   need(parts,'final median support hull');P[v]=[min(b[0] for b in parts),max(b[1] for b in parts),min(b[2] for b in parts),max(b[3] for b in parts)]
  continuous=coupled(P,E,q,pairs,limit=160);alt=coupled(P,IE,Iq,pairs,alt=True,limit=160);need(continuous==alt,'median final projection replay');leaf_excluded=continuous['excluded']
 summary={'starting_labels':sum(b.bit_count() for b in z['final_supported_domains'].values()),'final_labels':sum(b.bit_count() for b in D.values()),'assignments_before':start_count,'assignments_after':last,'leaf_excluded':leaf_excluded,'parent_width':width(base),'projected_width':width(P)}
 if continuous and not continuous['excluded']:summary.update({'final_width':width(continuous['boxes']),'continuous_fixed':continuous['fixed'],'continuous_sweeps':continuous['sweeps']})
 out=ROOT/'verify/out/n100-arc-median-learning.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_ranked_witnesses.py','verify/n100_arc_range_nogood.py','verify/n100_arc_nogood_state_dp.py','verify/n100_arc_learning_counts.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-arc-median-learning/v1','verified_integer_bounded_median_learning':True,'all_ranks_replayed_by_unrank':True,'all_geometry_alternate_equal':True,'placement':p,'source_node':node,'iteration_limit':3,'stop':stop,'summary':summary,'history':history,'clauses':clauses,'boundary_order':order,'final_supported_domains':D,'final_anchor_witnesses':witnesses,'continuous_result':continuous,'scope':'new conflicts valid only within stage82 fixed parent; three rank-median trials max, not full continuous enumeration','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS bounded median learning',stop,summary)
if __name__=='__main__':main()
