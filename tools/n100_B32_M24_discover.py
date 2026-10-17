"""Floating discovery only: reoptimize B32 M24 fixed-pattern dual row.
All candidates require a separate exact checker before acceptance.
"""
from pathlib import Path
import math,json,itertools,hashlib
import numpy as np
from scipy.optimize import brentq,linprog,differential_evolution,minimize
R=Path(__file__).resolve().parents[1];A=3*math.sqrt(3)/4;ANG=math.pi/3;B=32;RAD=.11324;C0=3*math.sqrt(3)/2
FACES=list(itertools.combinations_with_replacement(range(3),3))+[(2,2,3)]
TYPES=[(0,5)]+[(p,d) for p in range(4) for d in range(6,9)]
EPS=2e-7

def sinecon(t):
 if t>=1:return 0.
 if t<=-1:return -t*math.pi/2
 return (math.sqrt(1-t*t)-t*math.acos(t))/2

def face(labels):
 def derivative(nu):return math.pi-sum(math.acos(max(-1.,min(1.,nu-x))) for x in labels)/2
 nu=brentq(derivative,min(labels)-1.1,max(labels)+1.1,xtol=1e-13);mean=sum(labels)/3
 return max(math.pi*nu+sum(sinecon(nu-x) for x in labels)-math.pi*mean,math.pi*(max(labels)-mean)),nu

def conj(t):
 c=max(0.,min(1.,(-1+math.sqrt(max(0.,33-16*t)))/8));a=math.acos(c);vals=[0.,1+t*math.pi/2,t*math.pi,math.sin(a)*(1+2*c)+t*a]
 if 0<t<1:
  x=math.acos(t);vals.append(math.sin(x)+t*(math.pi-x))
 return max(vals)

C0=conj(0.)

def lp(p,full=False):
 a,lb,c=map(float,p)
 if a+c>=.999 or min(a,lb,c)<=0:return (1e3 if not full else None)
 labels=[-a,-lb,0.,c];ubs=[];rhs=[];nus=[]
 for ids in FACES:
  val,nu=face([labels[i] for i in ids]);nus.append(nu);v=np.zeros(7)
  for i in ids:v[i]-=1
  ubs.append(v);rhs.append(A-val-EPS)
 for p0,d in TYPES:
  ix=3 if d==5 else 2 if d==6 else 0;lv=labels[ix];const=p0*(conj(lv+lb)-C0)-lv*(6-d+p0)*ANG;v=np.zeros(7);v[ix]=d-p0;v[4]=-1;v[5]=-p0;v[6]=-(d-6);ubs.append(v);rhs.append((.02 if p0==3 else 0)-const-EPS)
 # Same shifted-ear condition as source, with the source's conservative cap2.065.
 v=np.zeros(7);v[1]=2;v[5]=-2;v[6]=-1;ubs.append(v);rhs.append(-(A-2*C0+2.065+lb*ANG)-EPS)
 objective=np.array([0.,24.,0.,5.,67.,32.,3.]);result=linprog(objective,A_ub=np.array(ubs),b_ub=np.array(rhs),bounds=[(1e-9,None)]*5+[(None,None)]*2,method='highs')
 if not result.success:return (1e3 if not full else None)
 constant=134*A+32*C0-lb*(2*math.pi+24*ANG)-c*ANG;total=constant+result.fun
 if full:return {'labels':labels,'parameters':[a,lb,c],'linear_variables':result.x.tolist(),'nus':nus,'normalized_total':total,'minimum_numeric_constraint_slack':float(min(np.array(rhs)-np.array(ubs)@result.x))}
 return total

def main():
 initial=[.378148580,.129204403,.5];old=lp(initial,True);opt=differential_evolution(lp,[(.18,.6),(.03,.4),(.2,.7)],seed=141,popsize=8,maxiter=65,tol=1e-9,polish=False,workers=1);ref=minimize(lp,opt.x,method='Nelder-Mead',options={'maxiter':500,'xatol':1e-10,'fatol':1e-10});best=lp(ref.x,True);assert best is not None
 D=10**9;a,lb,c=best['parameters'];x=best['linear_variables'];row={'a':round(a*D),'lb':round(lb*D),'c':round(c*D),'charges':[round(v*D) for v in x[:4]],'u0':round(x[4]*D),'beta':round(x[5]*D),'eta':round(x[6]*D),'delta':0,'nus':[round(v*D) for v in best['nus']]};mu=math.pi/32;s=math.sin(mu);Q=32*(mu-s*(math.cos(mu)-math.sqrt(RAD*RAD-s*s)));margin=math.pi-RAD*RAD*best['normalized_total']-Q
 folder=R/'runtime/B32-M24-discovery-141';assert not folder.exists();folder.mkdir(parents=True);out=folder/'candidate.json';out.write_text(json.dumps({'schema':'n100-B32-M24-discovery/v1','discovery_only':True,'target_radius':'2831/25000','initial_fixed_potential_lp':old,'best':best,'row_DEN_1e9':row,'numeric_area_margin':margin,'optimizer_success':bool(opt.success),'optimizer_message':str(opt.message),'function_evaluations':int(opt.nfev)+int(ref.nfev),'geometric_scope':'same M24 face/vertex patterns as original; full B32 not claimed','exact_acceptance':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('DISCOVERY M24 numeric margin',margin,'candidate',out,flush=True)
if __name__=='__main__':main()
