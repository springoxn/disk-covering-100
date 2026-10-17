"""Exact joint arc/lens support on radial center intervals."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
from n100_arc_cap_rational_support import ROOT,need,sqrt_bounds

def lens(r,delta,u,n=128,save=False):
 depth=delta-u;s=1-2*r+delta;left=1-2*r+u;need(0<depth<r and left>0,'lens regime');total=F(0);slabs=[]
 for i in range(n):
  a=depth*i/n;b=depth*(i+1)/n;rad=min(2*r*b-b*b,s*s-(left+a)**2);need(rad>=0,'nonnegative slab');h=2*sqrt_bounds(rad)[1];total+=(b-a)*h
  if save:slabs.append(str(h))
 return total,slabs

def main():
 source=ROOT/'verify/out/n100-arc-cap-rational-support.json';z=json.loads(source.read_text(encoding='utf-8'));r=F(z['radius']);c=sqrt_bounds(1-r*r)[0];M=r/c;pl,ph=F(314159,100000),F(314160,100000);N=512;n=128;params=[];best=None
 for delta in (F(20,1000),F(28,1000),F(36,1000),F(44,1000)):
  slope=F(0)
  for j in range(N):
   lo=delta*j/N;hi=delta*(j+1)/N;d=1-r+hi;cos=(1-r*r+d*d)/(2*d);need(d*d<1-r*r and 0<cos<=1,'arc branch');p=sqrt_bounds(1-cos*cos)[1]/c;cap,_=lens(r,delta,lo,n);need(M>p,'arc slack');slope=max(slope,cap/(M-p))
  den=10**12;slope=F(-((-slope.numerator*den)//slope.denominator),den);margin=pl*(1-2*r+delta)**2-46*ph*r*r-slope*(54*M-pl);row={'delta':str(delta),'slope':str(slope),'k54_margin':str(margin)};params.append(row);print('ARC LENS',delta,'k54 excluded',margin>0,flush=True)
  if best is None or margin>best[0]:best=(margin,delta,slope)
 margin,delta,slope=best;steps=[]
 for j in range(N):
  lo=delta*j/N;hi=delta*(j+1)/N;d=1-r+hi;cos=(1-r*r+d*d)/(2*d);p=sqrt_bounds(1-cos*cos)[1]/c;cap,heights=lens(r,delta,lo,n,True);need(slope*(M-p)>=cap,'saved joint support');steps.append({'u_lower':str(lo),'u_upper':str(hi),'arc_half_upper':str(p),'lens_area_upper':str(cap),'slab_heights_upper':heights})
 families=json.loads((ROOT/'verify/out/n100-vonequinox-count-domain-bound.json').read_text(encoding='utf-8'))['surviving_m_B_families'];triples=[]
 for m,b in families:
  for k in range(b,m+1):
   if pl*(1-2*r+delta)**2-(m-k)*ph*r*r-slope*(k*M-pl)<=0:triples.append([m,b,k])
 old=json.loads((ROOT/'verify/out/n100-arc-cap-optimized.json').read_text(encoding='utf-8'))['compatible_triples'];removed=sorted(set(map(tuple,old))-set(map(tuple,triples)));out=ROOT/'verify/out/n100-arc-lens-support.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-arc-lens-support/v1','radius':str(r),'delta':str(delta),'slope':str(slope),'maximum_half_arc_upper':str(M),'pi_interval':[str(pl),str(ph)],'radial_interval_count':N,'slabs_per_lens':n,'parameters_tested':params,'k54_margin':str(margin),'k54_excluded':margin>0,'steps':steps,'compatible_triples':triples,'old_count_domain_intersection':sorted(set(map(tuple,old))&set(map(tuple,triples))),'additional_triples_removed':removed,'analytic_dependencies':['short-arc radial monotonicity below sqrt(1-r^2)','at u_lower lens area bounds every center distance in the radial interval because overlap decreases with separation','upper Darboux sum using both circle heights','far centers u>=delta have zero inner area and phi<=M','arc length sum>=pi and area subadditivity'],'scope':'four selected deltas, not continuous optimization; analytic geometry inherited, no full global cover or map enumeration','global_optimality':False,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS arc lens support','delta',delta,'k54',margin>0,'removed',len(removed))
if __name__=='__main__':main()
