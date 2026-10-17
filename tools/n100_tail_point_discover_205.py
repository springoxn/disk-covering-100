"""Floating discovery only: locate worst capped-pair relaxation at targetR."""
from pathlib import Path
import sys,math,json,hashlib
from scipy.optimize import differential_evolution,minimize
ROOT=Path(__file__).resolve().parents[1];R=.11324;LAM=.06;MU=.0092531
def state(x,sign):
 s=R*x;c=math.sqrt(max(0,1-s*s));h=R*math.sqrt(max(0,1-x*x));rho=c-h;u=(c,sign*s);v=(-sign*s,c);return s,h,u,v,(rho*u[0],rho*u[1]),math.asin(s)-s*rho
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def support(w,s,h,u,v):
 wr=dot(w,u);wt=abs(dot(w,v))
 if wr<=0 and wt*h<=-wr*s:return 0.
 return max(0.,wr*h-wt*s+R*math.hypot(*w))
def objective(xy):
 x,y=xy;s,h,u,v,c,H=state(x,-1);t,j,U,V,C,J=state(y,1);d=tuple(a-b for a,b in zip(c,C));w=tuple(2*LAM*di+(4*LAM*h-s/2)*ui for di,ui in zip(d,u));W=tuple(-2*LAM*di+(4*LAM*j-t/2)*ui for di,ui in zip(d,U));base=(H+J)/2-MU*(math.asin(s)+math.asin(t))/2;orig=LAM*dot(d,d)+support(w,s,h,u,v)+support(W,t,j,U,V);direct=4*LAM*R*R;return base+min(orig,direct)
def main():
 opt=differential_evolution(lambda xy:-objective(xy),[(0,1),(0,1)],seed=205,popsize=15,maxiter=120,tol=1e-12,polish=True);loc=minimize(lambda xy:-objective(xy),opt.x,method='Nelder-Mead',bounds=[(0,1),(0,1)],options={'maxiter':1000,'xatol':1e-13,'fatol':1e-15});rows=[{'xy':list(map(float,x)),'value':objective(x)} for x in (opt.x,loc.x,[0,0],[1,1],[0,1])];out=ROOT/'runtime/n100-tail-point-discovery-205.json';assert not out.exists();out.write_text(json.dumps({'discovery_only':True,'radius':'2831/25000','points':rows,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print(json.dumps(rows),flush=True)
if __name__=='__main__':main()
