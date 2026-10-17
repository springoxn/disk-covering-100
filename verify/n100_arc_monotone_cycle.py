"""Exact ordered interval realization by prefix-lower-bound states on each quadrant."""
from pathlib import Path
import json,hashlib
from n100_arc_pair_consistency import ROOT,load,need,labels,mask
from n100_arc_cycle_support import bit_dp,set_dp
from n100_boundary_order import ordered_vertices
from n100_boundary_circle_propagation import setup

def main():
 # Three adjacent descending closed intervals pass local order, but not total order.
 sequence=[5,4,3];need(all(a<=b+1 for a,b in zip(sequence,sequence[1:])) and max(sequence[:2])>sequence[2]+1,'descending counterexample')
 source='verify/out/n100-arc-ordered-cycle.json';core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};base=ordered_vertices(core);rows=[]
 for case in load(source)['cases']:
  p=case['placement'];_,E,q=setup(core,p,prior[tuple(p)]);start=next(i for i,v in enumerate(base) if q[v-100]!=q[base[i-1]-100]);order=base[start:]+base[:start];need(q[order[0]-100]!=q[order[-1]-100],'quadrant reset at closure');D={int(v):b for v,b in case['globally_supported_domains'].items()};lookup={frozenset((r['v'],r['w'])):r for r in case['relations']};tables=[];domains=[]
  for i,v in enumerate(order):domains.append(mask(2*j+flag for j in labels(D[v]) for flag in ((0,) if i==0 else (0,1))))
  for i,v in enumerate(order):
   w=order[(i+1)%len(order)];r=lookup[frozenset((v,w))];table={int(j):b for j,b in (r['forward'] if r['v']==v else r['reverse']).items()};same=q[v-100]==q[w-100];expanded={}
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
  supported,witnesses=bit_dp(domains,tables);need(supported==set_dp(domains,tables),'independent expanded DP');projected={v:mask({s//2 for s in labels(bits)}) for v,bits in zip(order,supported)}
  for witness in witnesses:
   need(all(domains[i]&(1<<s) for i,s in enumerate(witness)) and all(tables[i][witness[i]]&(1<<witness[(i+1)%len(order)]) for i in range(len(order))),'expanded witness edges')
   for i,s in enumerate(witness):
    j=s//2;M=j+s%2;need(j<=M<=j+1,'closed parameter interval')
    if i and q[order[i]-100]==q[order[i-1]-100]:need(M==max(witness[i-1]//2+witness[i-1]%2,j),'prefix max')
    else:need(M==j,'reset prefix')
  if case['source_node'] is None:need(any(supported),'candidate rejected: investigate')
  rows.append({'placement':p,'source_node':case['source_node'],'boundary_order':order,'input_labels':sum(b.bit_count() for b in D.values()),'globally_monotone_supported_labels':sum(b.bit_count() for b in projected.values()),'excluded':not any(supported),'projected_supported_domains':projected,'anchor_state_witnesses':witnesses,'parameter_witness_rule':'state=2*j+flag; t=(j+flag)/256 in each quadrant; flags encode running maximum of lower labels'});print('global monotone',p,case['source_node'],'labels',rows[-1]['input_labels'],rows[-1]['globally_monotone_supported_labels'],'witnesses',len(witnesses),'excluded',rows[-1]['excluded'],flush=True)
 out=ROOT/'verify/out/n100-arc-monotone-cycle.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_boundary_order.py','verify/n100_arc_ordered_cycle.py','verify/n100_arc_cycle_support.py'];out.write_text(json.dumps({'schema':'n100-arc-monotone-cycle/v1','verified_exact_expanded_finite_model':True,'independent_set_dp_all_equal':True,'local_order_counterexample_control':True,'all_witness_parameters_checked':True,'cases':rows,'candidate_retained':True,'scope':'global interval-monotone label realizations with inherited pair relations, not continuous disk-distance realizations','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS globally monotone cycle')
if __name__=='__main__':main()
