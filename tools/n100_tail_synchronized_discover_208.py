"""Tail synchronized discovery only: lambda, mu, K and intercept."""
from pathlib import Path
from fractions import Fraction as F
import math,json,hashlib
import numpy as np
from scipy.optimize import minimize_scalar,minimize,differential_evolution
ROOT=Path(__file__).resolve().parents[1];R=.11324;A=3*math.sqrt(3)/4

def triangleK(lam):
 def f(q,x):
  if q==1:return x*(1+2*math.sqrt(max(0,1-x*x)))-4*lam*x*x
  root=math.sqrt(max(0,(2 if q==2 else 3)*x-x*x))
  if q==2:return ((x+root) if x<=1 else (x+1)*root)-4*lam*x
  return (4*A/9-4*lam)*x+root
 vals=[]
 for q,lo,hi in ((1,0,1),(2,0,1),(2,1,2),(3,0,3)):
  z=minimize_scalar(lambda x:-f(q,x),bounds=(lo,hi),method='bounded',options={'xatol':1e-13});vals.append((f(q,z.x)-A)/q)
 return max(vals)
def states(x,sign):
 s=R*x;c=np.sqrt(1-s*s);h=R*np.sqrt(np.maximum(0,1-x*x));rho=c-h
 return s,h,c,sign*s,-sign*s,c,rho*c,rho*sign*s,np.arcsin(s)-s*rho
xs=np.linspace(0,1,181);xx,yy=np.meshgrid(xs,xs);S1=states(xx,-1);S2=states(yy,1)
def pair(x,y,lam,mu):
 sa,ha,ux,uy,vx,vy,px,py,Ha=states(x,-1);sb,hb,Ux,Uy,Vx,Vy,Px,Py,Hb=states(y,1);dx=px-Px;dy=py-Py
 wx=2*lam*dx+(4*lam*ha-sa/2)*ux;wy=2*lam*dy+(4*lam*ha-sa/2)*uy;Wx=-2*lam*dx+(4*lam*hb-sb/2)*Ux;Wy=-2*lam*dy+(4*lam*hb-sb/2)*Uy
 def sup(wx,wy,h,s,ux,uy,vx,vy):
  wr=wx*ux+wy*uy;wt=np.abs(wx*vx+wy*vy);raw=np.maximum(0,wr*h-wt*s+R*np.hypot(wx,wy));return np.where((wr<=0)&(wt*h<=-wr*s),0,raw)
 raw=lam*(dx*dx+dy*dy)+sup(wx,wy,ha,sa,ux,uy,vx,vy)+sup(Wx,Wy,hb,sb,Ux,Uy,Vx,Vy)
 return np.minimum(raw,4*lam*R*R)+(Ha+Hb)/2-mu*(np.arcsin(sa)+np.arcsin(sb))/2

def evaluate(par,full=False):
 lam,mu=par;K=triangleK(lam);vals=pair(xx,yy,lam,mu);idx=np.unravel_index(np.argmax(vals),vals.shape);peak=float(vals[idx]);xy=[float(xx[idx]),float(yy[idx])]
 opt=minimize(lambda p:-float(pair(p[0],p[1],lam,mu)),xy,bounds=[(0,1),(0,1)],method='Nelder-Mead',options={'maxiter':130,'xatol':1e-9,'fatol':1e-13})
 if -opt.fun>peak:peak=-float(opt.fun);xy=list(map(float,opt.x))
 allowed=((1-mu)*math.pi-((198-36)*A+36*K)*R*R)/36
 gap=allowed-peak
 if full:return {'lambda':lam,'mu':mu,'K_numeric':K,'peak':peak,'peak_xy':xy,'area_allowed_L':allowed,'per_cell_margin':gap,'B36_margin':36*gap}
 return -gap

def main():
 opt=differential_evolution(evaluate,[(.025,.11),(-.03,.04)],seed=208,popsize=6,maxiter=22,tol=1e-8,polish=False);loc=minimize(evaluate,opt.x,method='Nelder-Mead',options={'maxiter':200,'xatol':1e-9,'fatol':1e-13});best=evaluate(loc.x,True);folder=ROOT/'runtime/n100-tail-synchronized-discovery-208';assert not folder.exists();folder.mkdir(parents=True);ps=[F(float(v)).limit_denominator(10**8) for v in loc.x];best=evaluate(list(map(float,ps)),True);(folder/'proposal.json').write_text(json.dumps({'discovery_only':True,'radius':'2831/25000','lambda':str(ps[0]),'mu':str(ps[1]),'candidate':best,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print(json.dumps(best),flush=True)
if __name__=='__main__':main()
