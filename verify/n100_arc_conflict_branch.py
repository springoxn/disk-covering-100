"""Branch on a certified two-vertex range conflict with exact finite coverage."""
from pathlib import Path
import json,hashlib
from n100_arc_ranked_witnesses import ROOT,load,need,labels,range_marks,state_dp,count_dp,setup,build,intersect,independent_tile,coupled,independent
from n100_arc_center_projection import run
from n100_boundary_arc_class32 import audit_terminal
from n100_arc_ranked_projection import width

def bitmask(items):return sum(1<<j for j in items)
def main():
 source='verify/out/n100-arc-median-learning.json';z=load(source);geomsource='verify/out/n100-arc-geometry-feedback.json';g=load(geomsource);p=z['placement'];node=z['source_node'];base=g['final_boxes'];D={int(v):b for v,b in z['final_supported_domains'].items()};clauses=z['clauses'];order=z['boundary_order'];clause=z['history'][0]['range_clause'];need(len(clause)==2,'binary learned clause');(v,lo,hi),(w,low,high)=clause
 for A in (False,True):
  for B in (False,True):need((not (A and B))==((not A) or (A and not B)) and not ((not A) and (A and not B)),'disjoint Boolean cover')
 core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);_,IE,Iq=independent.setup(core,p,prior);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});lookup={frozenset((r['v'],r['w'])):r for r in g['final_relations']};T=[];same=[]
 for i,x in enumerate(order):
  y=order[(i+1)%len(order)];r=lookup[frozenset((x,y))];T.append({int(j):b for j,b in (r['forward'] if r['v']==x else r['reverse']).items()});same.append(q[x-100]==q[y-100])
 marks=range_marks(order,D,clauses);parent_count,acounts=count_dp([D[x] for x in order],T,same,marks,len(clauses));need(parent_count==z['summary']['assignments_after'],'parent count');signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};branch_domains=[];a=D.copy();a[v]&=bitmask(j for j in range(256) if not lo<=j<=hi);branch_domains.append(a);b=D.copy();b[v]&=bitmask(j for j in range(256) if lo<=j<=hi);b[w]&=bitmask(j for j in range(256) if not low<=j<=high);branch_domains.append(b);rows=[];sum_initial=0
 for child,domains in enumerate(branch_domains):
  m=range_marks(order,domains,clauses);support,witnesses,stats=state_dp([domains[x] for x in order],T,same,m,len(clauses));initial_count,ac=count_dp([domains[x] for x in order],T,same,m,len(clauses));sum_initial+=initial_count;S=dict(zip(order,support));row={'child':child,'branch_domains':domains,'initial_supported_domains':S,'initial_count':initial_count,'state_statistics':stats}
  for witness in witnesses:
   values=dict(zip(order,(s[0] for s in witness)));A=lo<=values[v]<=hi;B=low<=values[w]<=high;need((not A) if child==0 else (A and not B),'witness branch membership')
  if not initial_count:row.update({'excluded':True,'phase':'finite_initial','final_count':0});rows.append(row);print('BRANCH',child,'finite empty',flush=True);continue
  P=[box[:] for box in base]
  for x,bits in S.items():
   parts=[intersect(base[x],independent_tile(j,256,signs[q[x-100]])) for j in labels(bits)];parts=[part for part in parts if part is not None];need(parts,'child support hull');P[x]=[min(part[0] for part in parts),max(part[1] for part in parts),min(part[2] for part in parts),max(part[3] for part in parts)]
  result=coupled(P,E,q,pairs,limit=160);alt=coupled(P,IE,Iq,pairs,alt=True,limit=160);need(result==alt,'child continuous alternate');row['continuous_result']=result
  if result['excluded']:row.update({'excluded':True,'phase':'continuous','final_count':0});rows.append(row);print('BRANCH',child,'continuous excluded',flush=True);continue
  arc=run(result['boxes'],E,q,pairs,limit=80);row['arc_result']=arc
  if arc['excluded']:row.update({'excluded':True,'phase':'arc','final_count':0});rows.append(row);print('BRANCH',child,'arc excluded',flush=True);continue
  if arc['fixed']:audit_terminal(arc['boxes'],E,q,arc['masks'],256)
  # Terminal masks are safe to use only after fixed; otherwise retain previous finite support.
  F={x:S[x]&bitmask(arc['masks'][str(x-100)]) for x in S} if arc['fixed'] else S;fm=range_marks(order,F,clauses);fs,fw,st=state_dp([F[x] for x in order],T,same,fm,len(clauses));final_count,fac=count_dp([F[x] for x in order],T,same,fm,len(clauses));need(final_count<=initial_count,'child narrowing');row.update({'excluded':not final_count,'phase':'finite_after_geometry','final_count':final_count,'final_supported_domains':dict(zip(order,fs)),'final_anchor_witnesses':fw,'final_state_statistics':st,'final_width':width(arc['boxes']),'arc_fixed':arc['fixed']});rows.append(row);print('BRANCH',child,'initial',initial_count,'final',final_count,'labels',sum(bits.bit_count() for bits in fs),'excluded',not final_count,flush=True)
 need(sum_initial==parent_count,'exact disjoint parent count identity');summary={'parent_count':parent_count,'sum_initial_child_counts':sum_initial,'sum_final_unresolved_counts':sum(r['final_count'] for r in rows),'excluded_children':sum(r['excluded'] for r in rows),'unresolved_children':sum(not r['excluded'] for r in rows),'parent_leaf_excluded':all(r['excluded'] for r in rows)};out=ROOT/'verify/out/n100-arc-conflict-branch.json';need(not out.exists(),'overwrite');paths=[source,geomsource,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_ranked_witnesses.py','verify/n100_arc_nogood_state_dp.py','verify/n100_arc_learning_counts.py','verify/n100_arc_range_nogood.py','verify/n100_arc_center_projection.py','verify/n100_boundary_arc_class32.py','verify/n100_circle_center_alternating.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py','verify/n100_boundary_arc_tiles_audit.py'];out.write_text(json.dumps({'schema':'n100-arc-conflict-branch/v1','verified_integer_disjoint_branch':True,'Boolean_coverage_checked':True,'exact_parent_child_count_identity':True,'all_continuous_alternate_equal':True,'all_fixed_arc_masks_audited':True,'placement':p,'source_node':node,'splitting_clause':clause,'clauses':clauses,'boundary_order':order,'summary':summary,'children':rows,'scope':'two finite-label-disjoint children cover the inherited parent necessary domain; geometric closed endpoints can overlap harmlessly; nonempty children do not prove coverage','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS conflict branch',summary)
if __name__=='__main__':main()
