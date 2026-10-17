"""Independent gap-composition representative enumeration and direct subset packing."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache
import json,hashlib
from n100_recursive_joint_area_independent import rnd,atan,series,sqrtiv,need
R=Path(__file__).resolve().parents[1]
def comps(total,k):
 if k==1:
  if total>=2:yield (total,)
 else:
  for d in range(2,total-2*(k-1)+1):
   for tail in comps(total-d,k-1):yield (d,)+tail
def canonical(mask,B):
 bits=[(mask>>i)&1 for i in range(B)];return min(sum(bits[(j+s)%B]<<j for j in range(B)) for s in range(B))
def gapreps(B,allowed):
 reps=set()
 for e in allowed:
  if e==0:reps.add(0);continue
  for ds in comps(B,e):
   pos=0;mask=1
   for d in ds[:-1]:pos+=d;mask|=1<<pos
   reps.add(canonical(mask,B))
 return reps
def pack(mask,B):
 tips=[i for i in range(B) if mask>>i&1];groups=[{(i-1)%B,i,(i+1)%B} for i in tips]
 for n in range(len(groups),-1,-1):
  for subset in combinations(groups,n):
   if len(set().union(*subset))==3*n:return n
 raise AssertionError('packing')
def main():
 p=R/'verify/out/n100-m99-boundary-representatives.json';z=json.loads(p.read_text(encoding='utf-8'));srcp=R/'verify/out/n100-boundary-ear-pattern-domain.json';src=json.loads(srcp.read_text(encoding='utf-8'));need(z['input_sha256']==hashlib.sha256(srcp.read_bytes()).hexdigest(),'source binding');angles=json.loads((R/'verify/out/n100-disjoint-ear-group-cuts.json').read_text(encoding='utf-8'));rho=F(z['radius_upper_inclusive']);g=F(angles['three_arc_sum_upper']);arc=F(angles['individual_arc_upper']);pl,ph=rnd(16*atan(F(1,5),40)-4*atan(F(1,239),41),16*atan(F(1,5),41)-4*atan(F(1,239),40));A=F(3,4)*sqrtiv(F(3))[1];G1=sqrtiv((207+33*sqrtiv(F(33))[1])/128)[1];G2=sqrtiv(9+6*sqrtiv(F(3))[1])[1]/2
 for x,upper in [(rho,arc),(2*rho,g)]:need(2*atan(x/sqrtiv(1-x*x)[0],31)<=upper,'angle enclosure')
 def H(a,b):
  sl=series(a/2)[0];sh=series(b/2)[1];need(0<sl<=sh<rho,'radicand');return sh*sqrtiv(rho*rho-sl*sl)[1]+(b-series(a)[0])/2
 statuses=[]
 for proof in z['joint_area_proofs']:
  B,e,q=proof['B'],proof['ears'],proof['disjoint_groups'];need(g*B<6*pl,'group mean ordering');k=B-3*q;cap=2*pl-q*g-k*arc
  if cap>0:status='excluded by capacity'
  else:
   need(k>0,'remainder');lo=(2*pl-q*g)/k;hi=(2*ph-q*g)/k
   if series(hi/2)[1]>=rho:status='undecided'
   else:
    base=((196-2*B+e)*A+(B-2*e)*G1+e*G2)*rho*rho;boundary=(3*q*H(g/3,g/3) if q else 0)+k*H(lo,hi);gap=pl-base-boundary;status='excluded by area' if gap>0 else 'not excluded'
  need(status==proof['status'],'independent numeric classification');statuses.append(status)
 reports=[];checked=0
 for row in z['families']:
  B=row['B'];s=next(f for f in src['families'] if f['m']==99 and f['B']==B);reps=gapreps(B,s['allowed_ear_counts']);need(sorted(reps)==[c['mask'] for c in row['all_records']],'complete independent gap reps');kept=[]
  for record in row['all_records']:
   mask=record['mask'];q=pack(mask,B);e=mask.bit_count();need((e,q)==(record['ears'],record['maximum_disjoint_groups']),'exact set packing');proof=z['joint_area_proofs'][record['proof_index']];need((B,e,q)==(proof['B'],proof['ears'],proof['disjoint_groups']),'proof association');bad=statuses[record['proof_index']].startswith('excluded');need(bad==record['excluded'],'decision');checked+=1
   if not bad:kept.append(mask)
  need(kept==row['remaining_masks'] and len(reps)==row['prior_representative_count'] and len(kept)==row['remaining_representative_count'],'all result counts');reports.append({'B':B,'prior':len(reps),'remaining':len(kept),'excluded':len(reps)-len(kept)})
 out=R/'verify/out/n100-m99-boundary-representatives-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-m99-boundary-representatives-independent/v1','verified_complete_gap_composition_representatives':True,'verified_every_representative_exact_packing_and_decision':True,'numeric_proof_cases':len(statuses),'representatives_checked':checked,'families':reports,'scope':'independent complete boundary-word relaxation and scalar proofs only; internal triangulation and full coverage not enumerated, no full m99 family exclusion','global_optimality':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent m99 complete reps',checked,'proofs',len(statuses),'families',reports)
if __name__=='__main__':main()
