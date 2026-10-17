"""Exact global support for finite-domain boundary compatibility cycles."""
from pathlib import Path
import json,hashlib
from n100_arc_pair_consistency import ROOT,load,need,labels,mask

def cycle(case):
 D={int(v):b for v,b in case['final_domains'].items()};relations=case['relations'];adj={v:[] for v in D}
 for i,r in enumerate(relations):
  v,w=r['v'],r['w'];adj[v].append((w,i));adj[w].append((v,i))
 need(len(relations)==len(D) and all(len(a)==2 for a in adj.values()),'simple cycle degrees');start=min(D,key=lambda v:(D[v].bit_count(),v));order=[start];edgeids=[];previous=None;v=start
 while True:
  candidates=sorted((w,i) for w,i in adj[v] if w!=previous);need(candidates,'next cycle edge');w,i=candidates[0];edgeids.append(i)
  if w==start:break
  need(w not in order,'early subcycle');order.append(w);previous,v=v,w
 need(len(order)==len(D),'one connected cycle');tables=[]
 for i,edge in enumerate(edgeids):
  r=relations[edge];v=order[i];raw=r['forward'] if r['v']==v else r['reverse'];tables.append({int(j):b for j,b in raw.items()})
 return order,[D[v] for v in order],tables

def bit_dp(domains,tables):
 n=len(domains);total=[0]*n;witnesses=[]
 for anchor in labels(domains[0]):
  forward=[1<<anchor]
  for i in range(n-1):
   nxt=0
   for j in labels(forward[-1]):nxt|=tables[i][j]
   forward.append(nxt&domains[i+1])
  good=[0]*n;good[-1]=mask(j for j in labels(forward[-1]) if tables[-1][j]&(1<<anchor))
  for i in range(n-2,-1,-1):good[i]=mask(j for j in labels(forward[i]) if tables[i][j]&good[i+1])
  if not good[0]:continue
  need(good[0]==1<<anchor,'anchor retained');w=[anchor]
  for i in range(n-1):w.append(min(labels(tables[i][w[-1]]&good[i+1])))
  need(tables[-1][w[-1]]&(1<<anchor),'witness closes');witnesses.append(w)
  total=[a|b for a,b in zip(total,good)]
 return total,witnesses

def set_dp(domains,tables):
 # Independent set forward/backward recurrence using explicit relational edges.
 domains=[set(labels(d)) for d in domains];relations=[{(a,b) for a,bits in t.items() for b in labels(bits)} for t in tables];allgood=[set() for _ in domains]
 for first in sorted(domains[0]):
  reachable=[{first}]
  for i in range(len(domains)-1):reachable.append({b for a,b in relations[i] if a in reachable[-1] and b in domains[i+1]})
  suffix={a for a,b in relations[-1] if b==first and a in reachable[-1]};good=[set() for _ in domains];good[-1]=suffix
  for i in reversed(range(len(domains)-1)):good[i]={a for a,b in relations[i] if a in reachable[i] and b in good[i+1]}
  if first in good[0]:
   for i,s in enumerate(good):allgood[i]|=s
 return [mask(s) for s in allgood]

def main():
 inequality={0:2,1:1}
 for n in (3,4):
  d=[3]*n;t=[inequality.copy() for _ in range(n)];a,w=bit_dp(d,t);need(a==set_dp(d,t),'toy independent DP');need(a==([0]*n if n==3 else [3]*n),'odd/even inequality cycle')
 source='verify/out/n100-arc-pair-consistency.json';rows=[]
 for c in load(source)['cases']:
  order,D,T=cycle(c);a,w=bit_dp(D,T);b=set_dp(D,T);need(a==b,'independent exact cycle DP')
  for witness in w:
   need(all(D[i]&(1<<j) for i,j in enumerate(witness)) and all(T[i][witness[i]]&(1<<witness[(i+1)%len(order)]) for i in range(len(order))),'whole cycle witness')
  rows.append({'placement':c['placement'],'source_node':c['source_node'],'order':order,'initial_labels':sum(x.bit_count() for x in D),'globally_supported_labels':sum(x.bit_count() for x in a),'additional_labels_removed':sum(x.bit_count() for x in D)-sum(x.bit_count() for x in a),'excluded':not any(a),'supported_domains':dict(zip(order,a)),'anchor_witnesses':w});print('cycle',c['placement'],'node',c['source_node'],'labels',rows[-1]['initial_labels'],'supported',rows[-1]['globally_supported_labels'],'witnesses',len(w),'excluded',rows[-1]['excluded'],flush=True)
 need(not rows[-1]['excluded'],'candidate lost: investigate');out=ROOT/'verify/out/n100-arc-cycle-support.json';need(not out.exists(),'overwrite');paths=[source,'verify/n100_arc_pair_consistency.py'];out.write_text(json.dumps({'schema':'n100-arc-cycle-support/v1','verified_exact_finite_cycle_dp':True,'independent_set_dp_all_results_equal':True,'odd_cycle_rejection_control':True,'even_cycle_retention_control':True,'all_witnesses_checked':True,'cases':rows,'candidate_retained':True,'scope':'exact support of inherited finite pairwise relation model, not exact continuous geometric feasibility','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS exact cycle support')
if __name__=='__main__':main()
