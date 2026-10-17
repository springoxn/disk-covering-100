"""Enumerate and screen all m99 relaxed boundary-ear rotation representatives."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache
import json,hashlib
from n100_recursive_ear_obstruction import E,H_upper,ROOT

def canon(mask,B):
 full=(1<<B)-1;return min(((mask<<s)&full)|(mask>>(B-s)) for s in range(B))
def packing(mask,B):
 tips=[i for i in range(B) if mask>>i&1];sets=[sum(1<<j for j in [(i-1)%B,i,(i+1)%B]) for i in tips]
 def search(i,used):
  if i==len(sets):return 0
  return max(search(i+1,used),1+search(i+1,used|sets[i]) if not used&sets[i] else 0)
 return search(0,0)
def main():
 srcp=ROOT/'verify/out/n100-boundary-ear-pattern-domain.json';src=json.loads(srcp.read_text(encoding='utf-8'));aa=json.loads((ROOT/'verify/out/n100-disjoint-ear-group-cuts.json').read_text(encoding='utf-8'));r=F(src['radius_upper_inclusive']);g=F(aa['three_arc_sum_upper']);arc=F(aa['individual_arc_upper']);A=E.AH;G1=E.sqrt_bounds((207+33*E.sqrt_bounds(F(33))[1])/128)[1];G2=E.sqrt_bounds(9+6*E.sqrt_bounds(F(3))[1])[1]/2;proofs=[]
 @lru_cache(None)
 def test(B,e,q):
  k=B-3*q;cap=2*E.PL-q*g-k*arc
  if cap>0:status='excluded by capacity';gap=cap
  else:
   E.need(k>0,'remainder');lo=(2*E.PL-q*g)/k;hi=(2*E.PH-q*g)/k
   if E.sin_at(hi/2)[1]>=r:status='undecided';gap=F(0)
   else:
    base=((198-2*B-2+e)*A+(B-2*e)*G1+e*G2)*r*r;boundary=(3*q*H_upper(r,g/3,g/3) if q else 0)+k*H_upper(r,lo,hi);gap=E.PL-base-boundary;status='excluded by area' if gap>0 else 'not excluded'
  index=len(proofs);proofs.append({'B':B,'ears':e,'disjoint_groups':q,'status':status,'gap':str(gap)});return index
 rows=[]
 for family in src['families']:
  if family['m']!=99:continue
  B=family['B'];full=(1<<B)-1;reps=set()
  for e in family['allowed_ear_counts']:
   for tips in combinations(range(B),e):
    mask=sum(1<<i for i in tips)
    if mask&(((mask<<1)&full)|(mask>>(B-1))):continue
    reps.add(canon(mask,B))
  E.need(len(reps)==family['rotation_orbits'],'complete representatives match counts');records=[]
  for mask in sorted(reps):
   e=mask.bit_count();q=packing(mask,B);pi=test(B,e,q);records.append({'mask':mask,'ears':e,'maximum_disjoint_groups':q,'proof_index':pi,'excluded':proofs[pi]['status'].startswith('excluded')})
  kept=[c['mask'] for c in records if not c['excluded']];rows.append({'m':99,'B':B,'prior_representative_count':len(reps),'remaining_representative_count':len(kept),'remaining_masks':kept,'all_records':records});print('BOUNDARY99',B,len(reps),'->',len(kept),flush=True)
 out=ROOT/'verify/out/n100-m99-boundary-representatives.json';E.need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-m99-boundary-representatives/v1','radius_upper_inclusive':str(r),'families':rows,'joint_area_proofs':proofs,'scope':'complete rotation representatives of m99 relaxed nonadjacent ear-tip words with stage114 allowed ears, then exact triple packing and joint marked-area/Jensen cuts; no internal triangulation or continuous geometry feasibility enumeration','global_optimality':False,'input_sha256':hashlib.sha256(srcp.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS complete m99 boundary representatives')
if __name__=='__main__':main()
