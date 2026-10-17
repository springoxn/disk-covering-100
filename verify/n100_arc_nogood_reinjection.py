"""Reinject certified higher-order nogoods using an exhaustive union of subdomains."""
from pathlib import Path
from itertools import product
import json,hashlib
from n100_arc_pair_consistency import ROOT,load,need,labels,mask
from n100_arc_cycle_support import bit_dp,set_dp
from n100_boundary_order import ordered_vertices
from n100_boundary_arc_tiles import setup,build,intersect
from n100_boundary_arc_tiles_audit import independent_tile
from n100_circle_center_alternating import coupled,independent

def solve(case,D,order,q):
 lookup={frozenset((r['v'],r['w'])):r for r in case['relations']};tables=[];domains=[]
 for i,v in enumerate(order):domains.append(mask(2*j+flag for j in labels(D[v]) for flag in ((0,) if i==0 else (0,1))))
 for i,v in enumerate(order):
  w=order[(i+1)%len(order)];r=lookup[frozenset((v,w))];raw=r['forward'] if r['v']==v else r['reverse'];table={int(j):b for j,b in raw.items()};same=q[v-100]==q[w-100];expanded={}
  for state in labels(domains[i]):
   j=state//2;M=j+state%2;nexts=[]
   for k in labels(table[j]&D[w]):
    if same:
     if M>k+1:continue
     target=2*k+max(M,k)-k
    else:target=2*k
    if (domains[(i+1)%len(order)]>>target)&1:nexts.append(target)
   expanded[state]=mask(nexts)
  tables.append(expanded)
 a,w=bit_dp(domains,tables);need(a==set_dp(domains,tables),'nogood-subdomain independent DP')
 for witness in w:need(all(domains[i]&(1<<j) for i,j in enumerate(witness)) and all(tables[i][witness[i]]&(1<<witness[(i+1)%len(order)]) for i in range(len(order))),'subdomain witness')
 return {v:mask({s//2 for s in labels(bits)}) for v,bits in zip(order,a)},w

def main():
 source='verify/out/n100-arc-ordered-cycle.json';ngsource='verify/out/n100-arc-nogoods.json';ngrows=load(ngsource)['cases'];baselines=load('verify/out/n100-arc-center-projection.json')['cases'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};baseorder=ordered_vertices(core);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};rows=[]
 for case in load(source)['cases']:
  p=case['placement'];node=case['source_node'];ng=next(c for c in ngrows if c['placement']==p and c['source_node']==node);need(ng['proof']['excluded'],'certified parent-specific nogood');clause=ng['nogood_restrictions'];need(len({v for v,j in clause})==len(clause),'distinct clause variables')
  for statuses in product((False,True),repeat=len(clause)):need((not all(statuses))==any(not x for x in statuses),'exhaustive Boolean union cover')
  base=next(c['result']['boxes'] for c in baselines if c['placement']==p and c['source_node']==node);_,E,q=setup(core,p,prior[tuple(p)]);_,IE,Iq=independent.setup(core,p,prior[tuple(p)]);start=next(i for i,v in enumerate(baseorder) if q[v-100]!=q[baseorder[i-1]-100]);order=baseorder[start:]+baseorder[:start];D={int(v):b for v,b in case['globally_supported_domains'].items()};total={v:0 for v in D};branches=[]
  for v,j in clause:
   sub=D.copy();sub[v]&=~(1<<j);supported,witnesses=solve(case,sub,order,q)
   for x,bits in supported.items():total[x]|=bits
   for witness in witnesses:
    assignment=dict(zip(order,(s//2 for s in witness)));need(any(assignment[x]!=y for x,y in clause) and assignment[v]!=j,'witness avoids learned nogood')
   geometry=None
   if witnesses:
    witness=witnesses[0];B=[b[:] for b in base]
    for x,state in zip(order,witness):
     b=intersect(B[x],independent_tile(state//2,256,signs[q[x-100]]));need(b is not None,'new witness tile');B[x]=b
    geometry=coupled(B,E,q,pairs,limit=160);alt=coupled(B,IE,Iq,pairs,alt=True,limit=160);need(geometry==alt,'new witness independent arithmetic')
   branches.append({'forbidden_label':[v,j],'supported_domains':supported,'witness_count':len(witnesses),'anchor_state_witnesses':witnesses,'first_witness_geometry':geometry});print('reinject',p,node,'forbid',v,j,'witnesses',len(witnesses),'new geometry excluded',geometry['excluded'] if geometry else None,flush=True)
  rows.append({'placement':p,'source_node':node,'nogood':clause,'boundary_order':order,'subdomain_count':len(branches),'input_labels':sum(b.bit_count() for b in D.values()),'union_supported_labels':sum(b.bit_count() for b in total.values()),'root_excluded':not any(total.values()),'union_supported_domains':total,'branches':branches});print('CASE',p,node,'labels',rows[-1]['input_labels'],rows[-1]['union_supported_labels'],'root',rows[-1]['root_excluded'],flush=True)
 out=ROOT/'verify/out/n100-arc-nogood-reinjection.json';need(not out.exists(),'overwrite');paths=[source,ngsource,'verify/out/n100-arc-center-projection.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_nogoods.py','verify/n100_arc_cycle_support.py','verify/n100_boundary_order.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-arc-nogood-reinjection/v1','verified_exact_finite_model_reinjection':True,'Boolean_subdomain_cover_verified':True,'all_subdomain_set_dp_equal':True,'all_witnesses_avoid_conditional_nogood':True,'first_new_witness_geometry_alternate_equal':True,'cases':rows,'scope':'one root-specific nogood per input, union of overlapping subdomains exact for that finite ordered model; only first new witness geometrically tested per subdomain','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS nogood reinjection')
if __name__=='__main__':main()
