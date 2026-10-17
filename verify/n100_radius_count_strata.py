"""Compile radius-stratified necessary (m,B,k) domains from certified cuts."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def main():
 U=F(1154469548855829,10**16);L=F(11323,100000);f=json.loads((ROOT/'verify/out/n100-recursive-radius-frontier.json').read_text(encoding='utf-8'));base=json.loads((ROOT/'verify/out/n100-recursive-joint-area.json').read_text(encoding='utf-8'));old={(m,b,k) for m,b,k in base['remaining_triples']};cuts=[(L,F('0.11367968'),61,'cut61'),(F('0.11367968'),F('0.11444972'),60,'cut60'),(F('0.11444972'),F('0.11523976'),59,'cut59'),(F('0.11523976'),U,58,'U')];layers=[]
 for i,(lo,hi,ns,tag) in enumerate(cuts):
  if tag!='U':
   source=next(c for c in f['cuts'] if c.get('minimum_nonserving_count')==ns);need(F(source['radius_cut'])==hi,'cut radius/count binding')
  else:need(ns==base['minimum_non_circle_serving_disks'],'baseline count binding')
  if i:need(lo==cuts[i-1][1],'gap-free strata')
  T=sorted(t for t in old if t[0]-t[2]>=ns);need(lo<=hi,'layer ordering');layers.append({'label':tag,'radius_lower':str(lo),'radius_upper':str(hi),'minimum_nonserving':ns,'maximum_serving_for_m100':100-ns,'triples':T,'triple_count':len(T),'families':sorted({(m,b) for m,b,k in T}),'family_count':len({(m,b) for m,b,k in T})})
 # Correct open/closed interpretation: cuts certify r<=cut. The lower-bound layer is [L,cut61] and stronger domains apply at upper endpoint; store nested certs rather than claim partition.
 need(len(layers)==4 and [x['triple_count'] for x in layers]==[245,294,347,404],'expected strata');cand=(100,32,32);need(all(cand in layer['triples'] for layer in layers),'candidate all strata');out=ROOT/'verify/out/n100-radius-count-strata.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-radius-count-strata/v1','radius_lower_global':str(L),'radius_upper_global':str(U),'layers':layers,'candidate_tuple':list(cand),'candidate_retained_all_layers':True,'interpretation':'nested certified domains: for any r<=layer radius_upper, use that layer minimum count; lower reference is reporting anchor, not a proof of r lying in a disjoint interval','monotone_inclusion_checked':all(set(layers[i]['triples']).issubset(set(layers[i+1]['triples'])) for i in range(3)),'analytic_dependencies':['radius-frontier cuts certified in stage106','m-k nonserving count bridge inherited from recursive inner reduction and boundary-serving semantics','no claim that surviving triples are feasible'],'scope':'finite radius-stratified necessary-domain interface for later branch search; no new geometric exclusion','global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'verify/out/n100-recursive-radius-frontier.json',ROOT/'verify/out/n100-recursive-joint-area.json']},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS strata',[(x['label'],x['triple_count'],x['family_count']) for x in layers])
if __name__=='__main__':main()
