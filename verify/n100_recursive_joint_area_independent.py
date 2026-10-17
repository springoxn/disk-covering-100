"""Independent joint-area arithmetic at the scaled inner radius."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt,factorial
from functools import lru_cache
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def rnd(a,b):
 S=10**40;return F(a.numerator*S//a.denominator,S),F(-((-b.numerator*S)//b.denominator),S)
def sqrtiv(x):
 S=10**40;n=isqrt(x.numerator*S*S//x.denominator);return F(n,S),F(n+1,S)
def atan(x,n):return sum((F((-1)**j,2*j+1)*x**(2*j+1) for j in range(n)),F(0))
def series(x,cos=False):
 total=sum((F((-1)**j,factorial(2*j+(0 if cos else 1)))*x**(2*j+(0 if cos else 1)) for j in range(26)),F(0));err=x**(52 if cos else 53)/factorial(52 if cos else 53);return total-err,total+err

def main():
 path=ROOT/'verify/out/n100-recursive-joint-area.json';z=json.loads(path.read_text(encoding='utf-8'));U=F(z['radius_upper']);s=F(z['inner_radius']);t=F(z['normalized_radius']);need(s==1-2*U and t==U/s and 0<t<F(1,5),'scale and analytic radius domain');pl,ph=rnd(16*atan(F(1,5),40)-4*atan(F(1,239),41),16*atan(F(1,5),41)-4*atan(F(1,239),40));root3=sqrtiv(F(3));Alo,Ahi=[3*v/4 for v in root3];kap=F(461134488,10**9);need(Alo+kap>sqrtiv((207+33*sqrtiv(F(33))[1])/128)[1] and Alo+2*kap>sqrtiv(9+6*root3[1])[1]/2 and 3*kap>Ahi,'independent joint constants')
 @lru_cache(None)
 def trig(B):return (*rnd(series(pl/B)[0],series(ph/B)[1]),*rnd(series(ph/B,True)[0],series(pl/B,True)[1]))
 first=None;checked=0;strict=[]
 q=1/(t*t);start=-((-q.numerator)//q.denominator);need(start==z['minimum_m_from_union_area'],'area count floor')
 for row in z['count_rows']:
  n=row['disk_count'];need(n==start+len(strict),'sequential count scan');alive=[];need([c['B'] for c in row['cases']]==list(range(3,n)),'all boundary counts')
  for c in row['cases']:
   B=c['B'];sl,sh,cl,ch=trig(B);need(0<sl<=sh<1 and 0<cl<=ch<1,'trig interval');checked+=1
   if sl>t:status='arc exclusion'
   else:
    need(sh<t,'undecided arc');coef=F(2*n-2,B)-1;lo=(coef*Alo+kap)*t*t+sl*sqrtiv(t*t-sh*sh)[0]-sh*ch;hi=(coef*Ahi+kap)*t*t+sh*sqrtiv(t*t-sl*sl)[1]-sl*cl
    need(lo<=hi,'area interval')
    if hi<0:status='area exclusion'
    else:need(lo>0,'undecided area');status='not excluded';alive.append(B)
   need(status==c['status'],'independent case status')
  need(alive==row['not_excluded_B'],'inner B survivors');strict.append(not alive)
  if alive:need(first is None,'scan past first survival');first=n
 need(first==z['minimum_non_circle_serving_disks'] and all(strict[:-1]) and not strict[-1],'necessary inner count threshold');prior=json.loads((ROOT/'verify/out/n100-recursive-inner-envelope.json').read_text(encoding='utf-8'));old=set(map(tuple,prior['remaining_triples']));new=sorted(T for T in old if T[0]-T[2]>=first);need(new==list(map(tuple,z['remaining_triples'])) and sorted(old-set(new))==list(map(tuple,z['removed_triples'])),'all triple pruning');families=sorted({(m,B) for m,B,k in new});need(families==list(map(tuple,z['remaining_families'])),'all family pruning');out=ROOT/'verify/out/n100-recursive-joint-area-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-recursive-joint-area-independent/v1','verified_independent_joint_area_arithmetic':True,'inner_count_B_cases_checked':checked,'minimum_non_circle_serving_disks':first,'prior_triples':len(old),'remaining_triples':len(new),'removed_triples':len(old-set(new)),'remaining_families':len(families),'scope':'independent all inner count/B and outer-domain arithmetic, analytic normalization/joint-area/concavity reduction inherited, not independently formalized here','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent recursive joint; nonserving',first,'inner cases',checked,'triples',len(old),'->',len(new),'families',len(families))
if __name__=='__main__':main()
