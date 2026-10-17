"""Exact ordered cycle DP with accumulated nogood-satisfaction state."""
from pathlib import Path
import json,hashlib
from n100_arc_pair_consistency import ROOT,load,need,labels,mask
from n100_boundary_arc_tiles import setup

def state_dp(domains,tables,same,marks,clause_count):
 n=len(domains);allbits=(1<<clause_count)-1;total=[0]*n;witnesses=[];peak=0;visited=0
 need(not same[-1],'anchor must start after quadrant switch')
 moves=[]
 for i in range(n-1):
  row={}
  for j in labels(domains[i]):
   for M in (j,j+1):
    opts=[]
    for k in labels(tables[i][j]&domains[i+1]):
     if same[i] and M>k+1:continue
     opts.append((k,max(M,k) if same[i] else k))
    row[(j,M)]=opts
  moves.append(row)
 for anchor in labels(domains[0]):
  first=(anchor,anchor,marks[0][anchor]);forward=[{first}]
  for i in range(n-1):
   nxt=set()
   for j,M,sat in forward[-1]:
    for k,N in moves[i][(j,M)]:nxt.add((k,N,sat|marks[i+1][k]))
   forward.append(nxt)
  peak=max(peak,max(map(len,forward)));visited+=sum(map(len,forward));good=[set() for _ in domains];good[-1]={s for s in forward[-1] if s[2]==allbits and tables[-1][s[0]]&(1<<anchor)}
  for i in range(n-2,-1,-1):
   for s in forward[i]:
    j,M,sat=s
    if any((k,N,sat|marks[i+1][k]) in good[i+1] for k,N in moves[i][(j,M)]):good[i].add(s)
  if first not in good[0]:continue
  w=[first]
  for i in range(n-1):
   j,M,sat=w[-1];w.append(min((k,N,sat|marks[i+1][k]) for k,N in moves[i][(j,M)] if (k,N,sat|marks[i+1][k]) in good[i+1]))
  need(w[-1][2]==allbits and tables[-1][w[-1][0]]&(1<<anchor),'satisfied closing witness');witnesses.append(w)
  for i,S in enumerate(good):total[i]|=mask({s[0] for s in S})
 return total,witnesses,{'maximum_states_in_one_layer':peak,'total_reachable_states_across_anchors_layers':visited,'anchor_count':domains[0].bit_count()}

def make_marks(order,D,clauses):
 out=[]
 for v in order:
  row={}
  for j in labels(D[v]):
   sat=0
   for i,c in enumerate(clauses):
    if any(v==w and j!=k for w,k in c):sat|=1<<i
   row[j]=sat
  out.append(row)
 return out

def main():
 # Unary clauses on one vertex: one feasible restriction, then a contradictory pair.
 order=[0,1,2];D={v:3 for v in order};tables=[{0:3,1:3} for _ in order]
 for clauses,expected in (([[[0,0]]],[2,3,3]),([[[0,0]],[[0,1]]],[0,0,0])):
  support,w,stats=state_dp([3,3,3],tables,[False]*3,make_marks(order,D,clauses),len(clauses));need(support==expected,'satisfaction state controls')
 modelsource='verify/out/n100-arc-ordered-cycle.json';oracle='verify/out/n100-arc-two-nogoods.json';models=load(modelsource)['cases'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};rows=[]
 for case in load(oracle)['cases']:
  p=case['placement'];node=case['source_node'];model=next(c for c in models if c['placement']==p and c['source_node']==node);D={int(v):b for v,b in model['globally_supported_domains'].items()};inherited=next(c for c in load('verify/out/n100-arc-nogood-reinjection.json')['cases'] if c['placement']==p and c['source_node']==node);order=inherited['boundary_order'];_,E,q=setup(core,p,prior[tuple(p)]);lookup={frozenset((r['v'],r['w'])):r for r in model['relations']};tables=[];same=[]
  for i,v in enumerate(order):
   w=order[(i+1)%len(order)];r=lookup[frozenset((v,w))];tables.append({int(j):b for j,b in (r['forward'] if r['v']==v else r['reverse']).items()});same.append(q[v-100]==q[w-100])
  clauses=case['clauses'];support,witnesses,stats=state_dp([D[v] for v in order],tables,same,make_marks(order,D,clauses),len(clauses));actual=dict(zip(order,support));expected={int(v):b for v,b in case['two_clause_supported_domains'].items()};need(actual==expected,'exact equality with exhaustive subdomain oracle')
  for witness in witnesses:
   values=dict(zip(order,(s[0] for s in witness)));need(all(any(values[v]!=j for v,j in c) for c in clauses),'all clauses satisfied')
   need(all(D[v]&(1<<s[0]) for v,s in zip(order,witness)),'witness labels')
   for i,s in enumerate(witness):
    j,M,sat=s;need(j<=M<=j+1 and tables[i][j]&(1<<witness[(i+1)%len(order)][0]),'witness interval and edge')
    if i:need(M==(max(witness[i-1][1],j) if same[i-1] else j),'witness monotone prefix')
  rows.append({'placement':p,'source_node':node,'clause_count':len(clauses),'supported_label_count':sum(b.bit_count() for b in support),'supported_domains':actual,'boundary_order':order,'state_statistics':stats,'anchor_witnesses':witnesses,'exact_oracle_match':True,'root_excluded':not any(support)});print('state DP',p,node,'support',rows[-1]['supported_label_count'],'states',stats,'oracle equal',True,flush=True)
 out=ROOT/'verify/out/n100-arc-nogood-state-dp.json';need(not out.exists(),'overwrite');paths=[modelsource,oracle,'verify/out/n100-arc-nogood-reinjection.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_two_nogoods.py','verify/n100_arc_nogood_reinjection.py','verify/n100_arc_cycle_support.py'];out.write_text(json.dumps({'schema':'n100-arc-nogood-state-dp/v1','verified_integer_state_dp':True,'feasible_unary_and_contradictory_clause_controls':True,'all_exact_supports_equal_exhaustive_subdomain_oracle':True,'all_witnesses_checked':True,'cases':rows,'scope':'new accumulated clause-state solver checked against saved exact union-of-subdomains outputs; source oracle previously double-DP verified, no new continuous elimination','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS nogood satisfaction-state DP')
if __name__=='__main__':main()
