"""Independent replay of saved radius cuts, not the binary-search discovery."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib
from n100_recursive_joint_area_independent import atan,rnd,sqrtiv,series,need,ROOT

def main():
 path=ROOT/'verify/out/n100-recursive-radius-frontier.json';z=json.loads(path.read_text(encoding='utf-8'));pl,ph=rnd(16*atan(F(1,5),40)-4*atan(F(1,239),41),16*atan(F(1,5),41)-4*atan(F(1,239),40));Alo,Ahi=[3*v/4 for v in sqrtiv(F(3))];kap=F(461134488,10**9)
 @lru_cache(None)
 def trig(B):return (*rnd(series(pl/B)[0],series(ph/B)[1]),*rnd(series(ph/B,True)[0],series(pl/B,True)[1]))
 def check(n,r):
  t=r/(1-2*r);need(0<t<F(1,5),'analytic radius range');rows=[]
  for B in range(3,n):
   sl,sh,cl,ch=trig(B)
   if sl>t:status='arc exclusion'
   else:
    need(sh<t,'undecided arc');coef=F(2*n-2,B)-1;lo=(coef*Alo+kap)*t*t+sl*sqrtiv(t*t-sh*sh)[0]-sh*ch;hi=(coef*Ahi+kap)*t*t+sh*sqrtiv(t*t-sl*sl)[1]-sl*cl
    if hi<0:status='area exclusion'
    else:need(lo>0,'undecided area');status='not excluded'
   rows.append((B,status))
  return rows
 prior=json.loads((ROOT/'verify/out/n100-recursive-joint-area.json').read_text(encoding='utf-8'));old=set(map(tuple,prior['remaining_triples']));reports=[];checked=0
 for c in z['cuts']:
  n=c['excluded_inner_count']
  if not c['excluded_at_current_lower']:
   rows=check(n,F(z['radius_lower_reference']));need(any(status=='not excluded' for B,status in rows),'lower-point failure classification');checked+=len(rows);reports.append({'excluded_inner_count':n,'cut_available':False});continue
  r=F(c['radius_cut']);rows=check(n,r);checked+=len(rows);need(rows==[(v['B'],v['status']) for v in c['cases']] and all(status!='not excluded' for B,status in rows),'all cut branches excluded');need(F(z['radius_lower_reference'])<=r<=F(z['radius_upper_reference']) and c['minimum_nonserving_count']==n+1,'cut interval and count');T=sorted(t for t in old if t[0]-t[2]>=n+1);need(T==list(map(tuple,c['remaining_triples'])) and len(T)==c['remaining_triple_count'] and len({(m,B) for m,B,k in T})==c['remaining_family_count'],'conditional count domain');reports.append({'excluded_inner_count':n,'cut_available':True,'radius_cut':str(r),'minimum_nonserving_count':n+1,'remaining_triples':len(T),'remaining_families':len({(m,B) for m,B,k in T})})
 out=ROOT/'verify/out/n100-recursive-radius-frontier-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-recursive-radius-frontier-independent/v1','verified_independent_saved_cut_arithmetic':True,'inner_boundary_cases_checked':checked,'results':reports,'scope':'independent all saved-cut B statuses and domains; does not independently replay discovery search or next-grid nonexclusion, no continuous optimality; geometry same dependencies as stage105','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent radius frontier','inner cases',checked,'certified cuts',sum(r['cut_available'] for r in reports))
if __name__=='__main__':main()
