"""Independent rational arithmetic replay of optimized cap thresholds."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def atan(q,n):
 total=F(0);power=F(1,q);x2=F(1,q*q)
 for j in range(n):total+=((-1)**j)*power/(2*j+1);power*=x2
 return total
def sqrt_up(x):
 S=10**20;target=x.numerator*S*S;den=x.denominator;lo=0;hi=S
 while hi*hi*den<=target:hi*=2
 while hi-lo>1:
  m=(lo+hi)//2
  if m*m*den<=target:lo=m
  else:hi=m
 u=F(lo+1,S);need((u-F(1,S))**2<=x<u*u,'strict square enclosure');return u

def main():
 source=ROOT/'verify/out/n100-cap-area-thresholds.json';z=json.loads(source.read_text(encoding='utf-8'));pi=(16*atan(5,8)-4*atan(239,7),16*atan(5,7)-4*atan(239,8));need(list(map(str,pi))==z['pi_interval'],'independent pi bracket');L,U=map(F,z['radius_interval']);deltas=[F(j,10000) for j in range(1,201)];checked=0;searches=0
 def margin(r,k,d):return pi[0]*(1-2*r+d)**2-(100-k)*pi[1]*r*r-k*F(4,3)*sqrt_up(2*r*d**3)
 def check(C):
  nonlocal checked
  r=F(C['radius_cut']);k=C['circle_serving_disks'];d=F(C['delta']);cap=F(4,3)*sqrt_up(2*r*d**3);m=margin(r,k,d);need(str(cap)==C['one_boundary_disk_cap_area_upper'] and str(m)==C['area_deficit_lower'] and (m>0)==C['excluded'],'independent full certificate arithmetic');checked+=1
 for row in z['rows']:
  if row['status']=='conditional_threshold':
   C=row['certificate'];N=row['next_radius_grid_no_exclusion'];check(C);check(N);r=F(C['radius_cut']);s=F(N['radius_cut']);need(s-r==F(1,10**8) and C['excluded'] and not N['excluded'],'adjacent cut grid and strict deficit');vals=[margin(s,row['k'],d) for d in deltas];need(max(vals)==F(N['area_deficit_lower'])<=0,'all next-radius grid deltas replay');searches+=len(vals)
  elif row['status']=='excluded_at_U':check(row['certificate']);need(F(row['certificate']['radius_cut'])==U and row['certificate']['excluded'],'upper endpoint exclusion')
  else:raise ValueError('unexpected untested status')
 need(F(next(row for row in z['rows'] if row['k']==55)['certificate']['radius_cut'])>F(23,200),'k55 improvement');need(all(0<d<2*L and 0<1-2*U+d<=1 for d in deltas),'uniform monotonicity parameter domain')
 # Deficit increases in k when full disk area bound exceeds cap bound.
 need(all(pi[1]*L*L>F(4,3)*sqrt_up(2*U*d**3) for d in deltas),'uniform full-disk area greater than cap on interval')
 out=ROOT/'verify/out/n100-cap-area-thresholds-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-cap-area-thresholds-independent/v1','verified_independent_rational_replay':True,'checked_saved_certificates':checked,'independent_next_grid_parameter_checks':searches,'pi_recurrence_agrees':True,'sqrt_method':'integer binary search with squared rational enclosure, no imported producer arithmetic','k55_strictly_improved':True,'fixed_delta_radius_monotonicity_domain_checked':True,'uniform_deficit_monotone_in_serving_count':True,'scope':'conditional area-cap counts only; analytic cap inequality inherited, no global radius lower bound improvement','global_optimality':False,'minimal_polynomial_obtained':False,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent thresholds',checked,'certificates',searches,'parameter checks')
if __name__=='__main__':main()
