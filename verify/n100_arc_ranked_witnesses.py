"""Exact assignment-rank witnesses, geometric checks, and median conflict learning."""
from pathlib import Path
from itertools import product
from fractions import Fraction
import json,hashlib
from n100_arc_nogood_state_dp import ROOT,load,need,labels,make_marks,state_dp
from n100_arc_learning_counts import count_dp
from n100_arc_range_nogood import range_marks
from n100_arc_nogood_reinjection import setup,build,intersect,independent_tile,coupled,independent

def unrank(domains,tables,same,marks,k,anchor_counts,rank):
 original=rank;offset=0;anchor=None
 for a,n in anchor_counts:
  if rank<n:anchor=a;break
  rank-=n;offset+=n
 need(anchor is not None,'rank in range');moves=[]
 for i in range(len(domains)-1):
  moves.append({(j,M):[(z,max(M,z) if same[i] else z) for z in labels(tables[i][j]&domains[i+1]) if not same[i] or M<=z+1] for j in labels(domains[i]) for M in (j,j+1)})
 first=(anchor,anchor,marks[0][anchor]);forward=[{first}]
 for i,row in enumerate(moves):forward.append({(z,N,s|marks[i+1][z]) for j,M,s in forward[-1] for z,N in row[j,M]})
 suffix=[{} for _ in domains];suffix[-1]={s:1 for s in forward[-1] if s[2]==(1<<k)-1 and tables[-1][s[0]]&(1<<anchor)}
 for i in range(len(domains)-2,-1,-1):
  for j,M,s in forward[i]:suffix[i][j,M,s]=sum(suffix[i+1].get((z,N,s|marks[i+1][z]),0) for z,N in moves[i][j,M])
 need(suffix[0].get(first,0)==dict(anchor_counts)[anchor],'suffix count versus source anchor oracle');w=[first]
 for i,row in enumerate(moves):
  j,M,s=w[-1];chosen=None
  for z,N in row[j,M]:
   target=(z,N,s|marks[i+1][z]);ways=suffix[i+1].get(target,0)
   if rank>=ways:rank-=ways
   else:chosen=target;break
  need(chosen is not None,'choose counted child');w.append(chosen)
 need(rank==0,'leaf rank');inverse=offset
 for i,row in enumerate(moves):
  j,M,s=w[i]
  for z,N in row[j,M]:
   target=(z,N,s|marks[i+1][z])
   if target==w[i+1]:break
   inverse+=suffix[i+1].get(target,0)
 need(inverse==original,'inverse rank replay');return w

def main():
 controls=0
 for clauses in ([],[[[1,0]]]):
  D={i:3 for i in range(3)};T=[{0:3,1:3} for _ in D];marks=make_marks(list(D),D,clauses);expected=[v for v in product((0,1),repeat=3) if all(any(v[x]!=j for x,j in c) for c in clauses)];n,counts=count_dp([3]*3,T,[False]*3,marks,len(clauses));need(n==len(expected),'toy counts')
  for r,v in enumerate(expected):need(tuple(s[0] for s in unrank([3]*3,T,[False]*3,marks,len(clauses),counts,r))==v,'toy exhaustive unrank');controls+=1
 source='verify/out/n100-arc-bounded-learning.json';z=load(source);p=z['placement'];node=z['source_node'];order=z['boundary_order'];clauses=[[[v,j,j] for v,j in c] for c in z['clauses']];model=next(c for c in load('verify/out/n100-arc-ordered-cycle.json')['cases'] if c['placement']==p and c['source_node']==node);D={int(v):b for v,b in model['globally_supported_domains'].items()};base=next(c['result']['boxes'] for c in load('verify/out/n100-arc-center-projection.json')['cases'] if c['placement']==p and c['source_node']==node);core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);_,IE,Iq=independent.setup(core,p,prior);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});lookup={frozenset((r['v'],r['w'])):r for r in model['relations']};T=[];same=[]
 for i,v in enumerate(order):
  w=order[(i+1)%len(order)];r=lookup[frozenset((v,w))];T.append({int(j):b for j,b in (r['forward'] if r['v']==v else r['reverse']).items()});same.append(q[v-100]==q[w-100])
 signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};log=[]
 def test(restrictions):
  B=[b[:] for b in base]
  for v,lo,hi in restrictions:
   a=independent_tile(lo,256,signs[q[v-100]]);b=independent_tile(hi,256,signs[q[v-100]]);c=intersect(B[v],[min(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),max(a[3],b[3])]);need(c is not None,'rank tile restriction');B[v]=c
  a=coupled(B,E,q,pairs,limit=160);b=coupled(B,IE,Iq,pairs,alt=True,limit=160);need(a==b,'rank geometry alternate');return a
 oracle=load('verify/out/n100-arc-learning-counts.json')['rows'][-1];total=oracle['assignment_count'];counts=oracle['anchor_counts'];marks=range_marks(order,D,clauses);ranked=[]
 for numerator in (1,2,3):
  rank=total*numerator//4;w=unrank([D[v] for v in order],T,same,marks,len(clauses),counts,rank);restrictions=[[v,s[0],s[0]] for v,s in zip(order,w)];values={v:j for v,j,h in restrictions};need(all(any(not lo<=values[v]<=hi for v,lo,hi in c) for c in clauses),'rank witness avoids all prior conflicts');g=test(restrictions);ranked.append({'rank':rank,'quartile_numerator':numerator,'restrictions':restrictions,'geometry':g});print('RANK',numerator,'excluded',g['excluded'],'fixed',g.get('fixed'),'sweeps',g.get('sweep',g.get('sweeps')),flush=True)
 learned=None;median=ranked[1]
 if median['geometry']['excluded']:
  active=[r[:] for r in median['restrictions']]
  for r in median['restrictions']:
   trial=[a for a in active if a!=r];g=test(trial);log.append({'kind':'remove','restriction':r,'excluded':g['excluded']})
   if g['excluded']:active=trial
  for i in range(len(active)):
   for side,target in ((1,0),(2,255)):
    accepted=active[i][side]
    if accepted==target:continue
    trial=[r[:] for r in active];trial[i][side]=target;g=test(trial);log.append({'kind':'expand','i':i,'side':side,'value':target,'excluded':g['excluded']})
    if g['excluded']:active[i][side]=target;continue
    rejected=target
    while abs(rejected-accepted)>1:
     middle=(rejected+accepted)//2;trial=[r[:] for r in active];trial[i][side]=middle;g=test(trial);log.append({'kind':'expand','i':i,'side':side,'value':middle,'excluded':g['excluded']})
     if g['excluded']:accepted=middle;active[i][side]=middle
     else:rejected=middle
  proof=test(active);need(active and proof['excluded'],'rank conflict range proof');newclauses=clauses+[active];m=range_marks(order,D,newclauses);support,w,stats=state_dp([D[v] for v in order],T,same,m,len(newclauses));after,acounts=count_dp([D[v] for v in order],T,same,m,len(newclauses));need(after<=total and all(b&~int(z['final_supported_domains'][str(v)])==0 for v,b in zip(order,support)),'rank learning monotonicity');ratio=Fraction(after,total);learned={'range_clause':active,'proof':proof,'clauses':newclauses,'support_after':sum(b.bit_count() for b in support),'supported_domains':dict(zip(order,support)),'anchor_witnesses':w,'assignment_count_after':after,'retained_fraction':[ratio.numerator,ratio.denominator],'state_statistics':stats,'root_excluded':not any(support)};print('MEDIAN LEARN sizes',len(active),'labels',learned['support_after'],'counts',total,after,'ratio',ratio,flush=True)
 out=ROOT/'verify/out/n100-arc-ranked-witnesses.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-learning-counts.json','verify/out/n100-arc-ordered-cycle.json','verify/out/n100-arc-center-projection.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_nogood_state_dp.py','verify/n100_arc_learning_counts.py','verify/n100_arc_range_nogood.py','verify/n100_arc_nogood_reinjection.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-arc-ranked-witnesses/v1','verified_integer_rank_selection':True,'exhaustive_unrank_controls':controls,'all_suffix_counts_match_anchor_oracle':True,'all_inverse_ranks_equal_targets':True,'all_geometry_alternate_equal':True,'placement':p,'source_node':node,'assignment_count_before':total,'boundary_order':order,'ranked_witnesses':ranked,'learning_trials':log,'learned':learned,'scope':'quartiles in finite assignment lexicographic rank, not continuous volume or geometry; no root exclusion from selected witnesses alone','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS ranked witnesses')
if __name__=='__main__':main()
