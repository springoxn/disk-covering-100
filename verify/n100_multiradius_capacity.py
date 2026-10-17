"""Actual radial-type arc bounds and multi-target lens capacity profiles."""
from fractions import Fraction as F
from math import isqrt,comb
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def roots(v):
 need(v>=0,'root domain');S=10**24;n=isqrt(v.numerator*S*S//v.denominator);return F(n,S),F(n+1,S)
def lens(r,t,d,n=512):
 lo=max(-t,d-r);hi=min(t,d+r)
 if lo>=hi:return F(0),F(0),[]
 lower=upper=F(0);rows=[]
 for j in range(n):
  a=lo+(hi-lo)*j/n;b=lo+(hi-lo)*(j+1)/n
  def squares(offset):
   x,y=a-offset,b-offset;return (F(0) if x<=0<=y else min(x*x,y*y),max(x*x,y*y))
  A=squares(F(0));B=squares(d);low=max(F(0),min(t*t-A[1],r*r-B[1]));high=max(F(0),min(t*t-A[0],r*r-B[0]));l=2*roots(low)[0];u=2*roots(high)[1];lower+=(b-a)*l;upper+=(b-a)*u;rows.append([str(a),str(b),str(l),str(u)])
 return lower,upper,rows

def main():
 path=ROOT/'verify/out/n100-arc-lens-support.json';z=json.loads(path.read_text(encoding='utf-8'));r=F(z['radius']);near=1-r+F(z['steps'][41]['u_upper']);tail=roots(1-r*r)[0];pl,ph=map(F,z['pi_interval']);types=[]
 for name,d,count in [('near',near,34),('tail',tail,20)]:
  cosine=(1-r*r+d*d)/(2*d);sinlo=roots(1-cosine*cosine)[0];c=roots(1-r*r)[0];phi_lo=sum((F(comb(2*j,j),4**j*(2*j+1))*sinlo**(2*j+1) for j in range(8)),F(0));phi_hi=roots(1-cosine*cosine)[1]/c;types.append({'kind':name,'distance':str(d),'count':count,'half_arc_lower':str(phi_lo),'half_arc_upper':str(phi_hi)})
 arcL=sum(t['count']*F(t['half_arc_lower']) for t in types);arcU=sum(t['count']*F(t['half_arc_upper']) for t in types);profiles=[]
 for j in range(1,101):
  t=F(j,100);L=46*pl*min(t,r)**2;U=46*ph*min(t,r)**2;parts=[]
  for ty in types:
   low,high,slabs=lens(r,t,F(ty['distance']));L+=ty['count']*low;U+=ty['count']*high;parts.append({'type':ty['kind'],'lower':str(low),'upper':str(high),'slabs':slabs})
  verdict='excluded' if U<pl*t*t else ('capacity_satisfied' if L>=ph*t*t else 'undecided');profiles.append({'target_radius':str(t),'total_capacity_lower':str(L),'total_capacity_upper':str(U),'target_area_lower':str(pl*t*t),'target_area_upper':str(ph*t*t),'verdict':verdict,'parts':parts})
 out=ROOT/'verify/out/n100-multiradius-capacity.json';need(not out.exists(),'overwrite');counts={v:sum(p['verdict']==v for p in profiles) for v in ('excluded','capacity_satisfied','undecided')};out.write_text(json.dumps({'schema':'n100-multiradius-capacity/v1','radius':str(r),'pi_interval':z['pi_interval'],'types':types,'central_nonserving_count':46,'arc_sum_lower':str(arcL),'arc_sum_upper':str(arcU),'arc_lower_covers_pi_upper':arcL>=ph,'arc_upper_below_pi_lower':arcU<pl,'profiles':profiles,'counts':counts,'analytic_dependencies':['arcsin positive power series partial sum is a lower bound on [0,1)','short-circle-arc cosine formula','circle intersection lower/upper Darboux sums','center-distance0 intersection area is pi*min(r,t)^2'],'scope':'specific radial multiset, not all configurations with k54; angles and overlap waste ignored; capacity satisfaction does not prove covering','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS radial capacity profiles','arc certified',arcL>=ph,'counts',counts)
if __name__=='__main__':main()
