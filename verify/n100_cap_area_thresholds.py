"""Rational-grid optimization of conditional boundary-cap area exclusions."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_boundary_cap_area_branch import R,need,atan_bracket,certificate

def main():
 a,b=atan_bracket(5),atan_bracket(239);pi=(16*a[0]-4*b[1],16*a[1]-4*b[0]);L=F(11323,100000);U=F(1154469548855829,10**16);scale=10**8;rows=[];deltas=[F(j,10000) for j in range(1,201)]
 def best(r,k):
  values=[certificate(r,100,k,d,pi) for d in deltas];return max(values,key=lambda c:F(c['area_deficit_lower']))
 for k in range(53,59):
  atL=best(L,k);atU=best(U,k)
  if not atL['excluded']:rows.append({'k':k,'status':'no_grid_exclusion_at_L','at_lower':atL,'at_upper':atU});print('CAP GRID',k,'no exclusion at lower',flush=True);continue
  if atU['excluded']:rows.append({'k':k,'status':'excluded_at_U','certificate':atU});print('CAP GRID',k,'excluded at U',flush=True);continue
  lo=int(L*scale);hi=U.numerator*scale//U.denominator+1
  while hi-lo>1:
   mid=(lo+hi)//2;C=best(F(mid,scale),k)
   if C['excluded']:lo=mid
   else:hi=mid
  C=best(F(lo,scale),k);upper=best(F(hi,scale),k);need(C['excluded'] and not upper['excluded'],'adjacent rational grid search endpoint');rows.append({'k':k,'status':'conditional_threshold','certificate':C,'next_radius_grid_no_exclusion':upper,'threshold_bracket':[str(F(lo,scale)),str(F(hi,scale))]});print('CAP GRID',k,'cut',F(lo,scale),'delta',C['delta'],flush=True)
 # All fixed delta deficits decrease with r on [L,U]: s=1-2r+d>0,
 # inner area falls, nonserving disk area and cap sqrt term rise.
 need(all(0<d<2*L and 0<1-2*U+d<=1 for d in deltas),'uniform parameter and monotonicity domain')
 k55=next(r for r in rows if r['k']==55);need(k55['status']=='conditional_threshold' and F(k55['certificate']['radius_cut'])>F(23,200),'strict improvement over previous k55 cut')
 out=R/'verify/out/n100-cap-area-thresholds.json';need(not out.exists(),'overwrite');paths=['verify/n100_boundary_cap_area_branch.py','verify/out/n100-boundary-cap-area-branch.json'];out.write_text(json.dumps({'schema':'n100-cap-area-thresholds/v1','verified_rational_parameter_search':True,'n':100,'radius_interval':[str(L),str(U)],'pi_interval':list(map(str,pi)),'delta_grid':{'denominator':10000,'first_numerator':1,'last_numerator':200},'radius_grid_denominator':scale,'rows':rows,'analytic_dependencies':['boundary-serving centers have norm >=1-r','area in inner radius s<=1-2r+delta bounded by (4/3)sqrt(2r delta^3)','area subadditivity and Machin alternating pi brackets','for each fixed delta on [L,U], positive inner radius decreases while disk and cap area bounds increase, hence deficit decreases'],'scope':'conditional exclusion by serving count k, grid-optimal only, no exclusion of smaller-k branches; nonpositive certified deficit is failure of this test, not feasible covering','global_optimality':False,'minimal_polynomial_obtained':False,'bindings':{s:hashlib.sha256((R/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS rational conditional cap thresholds')
if __name__=='__main__':main()
