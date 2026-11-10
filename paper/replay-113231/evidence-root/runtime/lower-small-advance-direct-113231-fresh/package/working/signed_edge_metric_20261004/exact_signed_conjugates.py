"""Exact signed-edge triangle supports on the complete angle simplex.

Numerical coefficients are proposals only. Acceptance uses the audited
integer interval kernel and an exhaustive list of scalar critical points.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt
import sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from verify_star_lp_duals import I,q,S,PI

def imax(*xs):return I(max(x.l for x in xs),max(x.u for x in xs))
def atan_small(x):
 assert 0<=x.l<=x.u<=S//2
 term=x;xx=x.sq();value=q(0)
 for j in range(40):
  value+=term/(2*j+1) if j%2==0 else -term/(2*j+1)
  term*=xx
 return value+I(0,(term/81).u)

@lru_cache(maxsize=100000)
def acos_point(raw):
 assert isinstance(raw,int) and -S<=raw<=S
 if raw<0:return PI-acos_point(-raw)
 if raw==S:return q(0)
 if raw==0:return PI/2
 x=I(raw);z=((1-x)/(1+x)).sqrt()
 # acos(x)=2atan(z)=4atan(z/(1+sqrt(1+z²))).
 h=z/(1+(1+z.sq()).sqrt())
 assert h.u<=S//2
 return 4*atan_small(h)

def acos_unit(x):
 assert -S<=x.l<=x.u<=S
 return I(acos_point(x.u).l,acos_point(x.l).u)

@lru_cache(maxsize=100000)
def conjugate_point(tau_raw,w_raw,acute=True):
 assert isinstance(tau_raw,int) and isinstance(w_raw,int)
 tau,w=I(tau_raw),I(w_raw)
 # sin is nonnegative on both domains; endpoint scores are exact enclosures.
 endpoint=tau-w*PI/2 if acute else -w*PI
 lower=max(0,endpoint.l);upper=max(0,endpoint.u)
 discriminant=tau_raw*tau_raw+8*S*(S+w_raw)
 if discriminant>=0:
  a=isqrt(discriminant);root=I(a,a+(a*a<discriminant));xmin=0 if acute else -S
  for sign in (-1,1):
   x=(-tau+sign*root)/4
   if x.u<xmin or x.l>S:continue
   fully_inside=x.l>=xmin and x.u<=S
   clipped=I(max(xmin,x.l),min(S,x.u))
   value=(clipped+tau)*(1-clipped.sq()).sqrt()-w*acos_unit(clipped)
   upper=max(upper,value.u)
   if fully_inside:lower=max(lower,value.l)
 return I(lower,upper)

def signed_conjugate(tau,w,acute=True):
 tau=tau if isinstance(tau,I) else q(tau);w=w if isinstance(w,I) else q(w)
 # Supremum is increasing in tau and decreasing in w.
 lower=conjugate_point(tau.l,w.u,acute)
 upper=conjugate_point(tau.u,w.l,acute)
 return I(lower.l,upper.u)

def localization_guards(corners,edges):
 assert len(corners)==len(edges)==3
 corners=[F(x) for x in corners];edges=[F(x) for x in edges]
 span=max(corners)-min(corners);assert 0<=span<=F(1,2)
 root3=q(3).sqrt();A=3*root3/4;loss=root3*q(sum(abs(x) for x in edges))/2;L=q(span)
 caps=[1+L*PI/6,2*L*PI/3,root3/2+(1+L)*PI/12]
 gaps=[A-v-loss for v in caps]
 assert all(g.l>0 for g in gaps),'Signed-edge full-simplex localization failed'
 return gaps

def triangle_support(corners,edges,face_multiplier,localize=True):
 corners=[F(x) for x in corners];edges=[F(x) for x in edges]
 if localize:localization_guards(corners,edges)
 eta=q(face_multiplier);one=PI*eta
 for u,tau in zip(corners,edges):one+=signed_conjugate(q(tau),q(u)+eta,localize)
 zero=-PI*q(min(corners))
 return imax(one,zero)
