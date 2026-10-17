"""Radius-conditional recursive count frontier via existing exact joint-area test."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working/lower_bounds_extension_20261004/verify_extension.py';sys.path.insert(0,str(P.parent))
import verify_extension as E
E.trig=lru_cache(None)(E.trig)
def main():
 L=F(11323,100000);U=F(1154469548855829,10**16);scale=10**8;priorpath=ROOT/'verify/out/n100-recursive-joint-area.json';prior=json.loads(priorpath.read_text(encoding='utf-8'));old=set(map(tuple,prior['remaining_triples']));results=[]
 def check(n,r):
  t=r/(1-2*r);rows=[E.classify(n,B,t) for B in range(3,n)];return all(c['status']!='not excluded' for c in rows),rows
 for n in range(58,62):
  yes,rows=check(n,L)
  if not yes:
   results.append({'excluded_inner_count':n,'excluded_at_current_lower':False});continue
  lo=int(L*scale);hi=U.numerator*scale//U.denominator+1;trace=[]
  while hi-lo>1:
   mid=(lo+hi)//2;valid,_=check(n,F(mid,scale));trace.append([mid,valid])
   if valid:lo=mid
   else:hi=mid
  r=F(lo,scale);valid,rows=check(n,r);E.need(valid,'saved cut exclusion');next_valid,next_rows=check(n,F(hi,scale));E.need(not next_valid,'next-grid upper search result');kept=sorted(T for T in old if T[0]-T[2]>=n+1);results.append({'excluded_inner_count':n,'excluded_at_current_lower':True,'radius_cut':str(r),'normalized_radius':str(r/(1-2*r)),'cases':rows,'next_grid_radius':str(F(hi,scale)),'next_grid_not_excluded_B':[c['B'] for c in next_rows if c['status']=='not excluded'],'trace':trace,'minimum_nonserving_count':n+1,'remaining_triples':kept,'remaining_triple_count':len(kept),'remaining_family_count':len({(m,B) for m,B,k in kept})});print('FRONTIER inner',n,'cut',r,'triples',len(kept),flush=True)
 out=ROOT/'verify/out/n100-recursive-radius-frontier.json';E.need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-recursive-radius-frontier/v1','radius_lower_reference':str(L),'radius_upper_reference':str(U),'baseline_minimum_nonserving':58,'baseline_triple_count':len(old),'cuts':results,'all_float_free':True,'analytic_dependencies':['same recursive inner-disk and joint-area/normalization hypotheses as stage105','for fixed inner boundary b, joint necessary residual increases with center count n, hence excluding all b at n also excludes smaller effective counts','enlarging outer disks to saved radius preserves coverage and does not decrease circle-serving count; nonserving upper count cannot increase'],'scope':'certified conditional cuts on finite radius grid; binary search not a continuous-optimality proof; no new unconditional pruning at U or global radius bound','global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P,priorpath]},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS recursive radius frontier')
if __name__=='__main__':main()
