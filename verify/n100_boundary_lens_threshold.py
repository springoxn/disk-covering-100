"""Rational upper Darboux sums for a boundary disk/inner disk lens."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,hashlib
from n100_boundary_cap_area_branch import R,need,atan_bracket

def root_up(x):
 need(x>=0,'nonnegative radicand');S=10**20;n=isqrt(x.numerator*S*S//x.denominator);u=F(n+1,S);need(u*u>x,'strict root enclosure');return u

def lens(r,delta,n=256,save=False):
 # Closest serving-center distance d=1-r, target inner radius s=d-r+delta.
 s=1-2*r+delta;left=1-2*r;need(0<delta<r and left>0 and s<=1,'lens regime');step=delta/n;total=F(0);rows=[]
 for i in range(n):
  a=i*step;b=(i+1)*step;small=2*r*b-b*b;target=s*s-(left+a)**2;rad=min(small,target);need(rad>=0,'lens slab radicand');height=2*root_up(rad);area=step*height;total+=area
  if save:rows.append({'a':str(a),'b':str(b),'small_disk_square_upper':str(small),'target_disk_square_upper':str(target),'chosen_square_upper':str(rad),'height_upper':str(height)})
 return total,rows

def main():
 a,b=atan_bracket(5),atan_bracket(239);pi=(16*a[0]-4*b[1],16*a[1]-4*b[0]);L=F(11323,100000);U=F(1154469548855829,10**16);old=F(11516023,10**8);grid=[F(j,10000) for j in range(60,111)];k=55;n=256
 def best(r):
  vals=[]
  for d in grid:
   cap,_=lens(r,d,n);margin=pi[0]*(1-2*r+d)**2-45*pi[1]*r*r-k*cap;vals.append((margin,d,cap))
  return max(vals)
 oldtest=best(old);endtest=best(U);need(oldtest[0]>0,'new lens must exclude old threshold');scale=10**8;lo=int(old*scale);hi=U.numerator*scale//U.denominator+1;iterations=[]
 while hi-lo>1:
  m=(lo+hi)//2;score,d,cap=best(F(m,scale));iterations.append({'radius':str(F(m,scale)),'margin':str(score),'delta':str(d)});print('LENS SEARCH',F(m,scale),'excluded',score>0,flush=True)
  if score>0:lo=m
  else:hi=m
 r=F(lo,scale);margin,d,cap=best(r);need(margin>0 and r>old,'strict threshold improvement');full,slabs=lens(r,d,n,True);need(full==cap,'saved slab sum');next_margin,next_delta,next_cap=best(F(hi,scale));need(next_margin<=0,'next grid test inconclusive');baseline=F(4,3)*root_up(2*r*d**3);need(cap<baseline and pi[1]*r*r>cap,'lens tighter and deficit increases in serving count');out=R/'verify/out/n100-boundary-lens-threshold.json';need(not out.exists(),'overwrite');paths=['verify/out/n100-cap-area-thresholds.json','verify/n100_boundary_cap_area_branch.py'];out.write_text(json.dumps({'schema':'n100-boundary-lens-threshold/v1','verified_integer_rational_lens_upper_sum':True,'total_disks':100,'serving_disks':55,'radius_cut':str(r),'delta':str(d),'inner_radius':str(1-2*r+d),'pi_interval':list(map(str,pi)),'subinterval_count':n,'lens_area_upper':str(cap),'old_tangent_cap_upper_same_parameters':str(baseline),'area_deficit_lower':str(margin),'old_threshold':str(old),'old_threshold_new_margin':str(oldtest[0]),'candidate_endpoint_best_margin':str(endtest[0]),'candidate_endpoint_best_delta':str(endtest[1]),'delta_grid':{'denominator':10000,'first_numerator':60,'last_numerator':110},'next_radius_grid':{'radius':str(F(hi,scale)),'margin':str(next_margin),'delta':str(next_delta)},'iterations':iterations,'slabs':slabs,'analytic_dependencies':['intersection area of two disks of fixed radii decreases with nonnegative center distance: integrate overlap lengths of symmetric horizontal intervals','serving centers have norm>=1-r; maximum overlap attained at closest allowed distance 1-r','on each slab z in [a,b], small-disk half-height square <=2rb-b² since b<r, inner-disk half-height square <=s²-(1-2r+a)² since positive radial coordinate','upper area sum = sum 2(b-a)sqrt(min(small_upper,target_upper))','at saved radius full disk area upper exceeds lens cap upper, so deficit increases with serving count; enlarging every disk preserves coverage and cannot decrease number intersecting unit circle'],'scope':'strict exclusion at the saved radius and by disk-enlargement argument all smaller radii; no continuous delta optimality, no full global lower bound; next grid nonexclusion is inconclusive','global_optimality':False,'minimal_polynomial_obtained':False,'bindings':{s:hashlib.sha256((R/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS lens threshold',r,'delta',d,'candidate excluded',endtest[0]>0)
if __name__=='__main__':main()
