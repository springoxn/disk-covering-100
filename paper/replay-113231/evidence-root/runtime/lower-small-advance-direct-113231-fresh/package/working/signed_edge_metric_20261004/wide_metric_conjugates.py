"""A separately verified wider full-simplex localization domain."""
from fractions import Fraction as F
from functools import lru_cache
import time
from exact_signed_conjugates import I,q,S,PI,imax,signed_conjugate
from verify_potential_star_duals import sine

def absolute(z):
 return I(0 if z.l<=0<=z.u else min(abs(z.l),abs(z.u)),max(abs(z.l),abs(z.u)))

TABLE=[(F(3,10),F(1,5),F(63,50)),(F(3,10),F(1,4),F(129,100)),(F(2,5),F(3,20),F(129,100)),(F(1,2),F(1,20),F(259,200))]

def nonacute_upper(box,L,epsilon):
 x,y=I(box[0],box[1]),I(box[2],box[3]);theta=PI*(1+x)/2;remaining=PI*(1-x)/2
 beta=remaining*y/2;gamma=remaining*(1-y/2)
 st,sb,sg=sine(theta),sine(beta),sine(gamma);s0=q(3).sqrt()/2
 d=imax(theta-PI/3,PI/3-beta)
 return 2*st*sb*sg+q(L)*d+q(epsilon)*(absolute(st-s0)+absolute(sb-s0)+absolute(sg-s0))

@lru_cache(maxsize=4)
def verify_wide_localization(mode=0):
 if not __debug__:raise RuntimeError('Assertions must be enabled')
 assert isinstance(mode,int) and 0<=mode<len(TABLE),'Unrecognized localization mode'
 L,epsilon,cap=TABLE[mode]
 stack=[(0,S,0,S)];visited=leaves=0;worst=0;target=q(cap).l;start=time.monotonic()
 while stack:
  box=stack.pop();v=nonacute_upper(box,L,epsilon);visited+=1
  if v.u<=target:leaves+=1;worst=max(worst,v.u);continue
  assert visited<2000000,'Wide localization did not close within the explicit resource cap'
  a,b,c,d=box
  if b-a>=d-c:
   m=(a+b)//2;assert a<m<b;stack.extend([(a,m,c,d),(m,b,c,d)])
  else:
   m=(c+d)//2;assert c<m<d;stack.extend([(a,b,c,m),(a,b,m,d)])
 A=3*q(3).sqrt()/4;gap=A-q(cap);assert gap.l>0
 return dict(status='PASS',mode=mode,potential_range=str(L),absolute_edge_potential=str(epsilon),nonacute_bound=str(cap),visited_boxes=visited,accepted_leaves=leaves,minimum_localization_gap=str(F(gap.l,S)),worst_accepted_upper=str(F(worst,S)),seconds_reporting_only=time.monotonic()-start)

def localization_guards(corners,edges):
 assert len(corners)==len(edges)==3
 cs=[F(x) for x in corners];ts=[F(x) for x in edges]
 for mode,(L,epsilon,cap) in enumerate(TABLE):
  if max(cs)-min(cs)<=L and max(abs(t) for t in ts)<=epsilon:
   verify_wide_localization(mode);return [3*q(3).sqrt()/4-q(cap)]
 from exact_signed_conjugates import localization_guards as narrow
 return narrow(cs,ts)

def triangle_support(corners,edges,face_multiplier,localize=True):
 assert len(corners)==len(edges)==3
 assert localize
 cs=[F(x) for x in corners];ts=[F(x) for x in edges];localization_guards(cs,ts);eta=q(face_multiplier)
 one=PI*eta
 for u,t in zip(cs,ts):one+=signed_conjugate(q(t),q(u)+eta,True)
 return imax(one,-PI*q(min(cs)))

if __name__=='__main__':
 import json
 print(json.dumps([verify_wide_localization(i) for i in range(len(TABLE))],indent=2))
