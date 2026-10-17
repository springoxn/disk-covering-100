"""Floating discovery of retuned B32 M25 coherent proposal. No acceptance."""
from pathlib import Path
from fractions import Fraction as F
import math,json,itertools,copy,hashlib
import numpy as np
from scipy.optimize import brentq,minimize_scalar,linprog,differential_evolution
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/lower_staging/B32_M25_direct_interface_0p11323_proposal.json';DATA=json.loads(P.read_text(encoding='utf-8'));DEN=10**12;labels=[x/DEN for x in DATA['labels']];a,b=-labels[0],-labels[1];A=3*math.sqrt(3)/4;ANG=math.pi/3;RAD=.11324;K=.44;SLOPE=.05945;FAN=SLOPE*(4*.0935-.3467)/(2*RAD**2);SAFETY=2e-7

def conjugate(t):
 c=max(0.,min(1.,(-(1-K)+math.sqrt(max(0.,(1-K)**2+16*(2-t))))/8));x=math.acos(c);values=[0.,(1-K)+t*math.pi/2,t*math.pi,(1-K)*math.sin(x)+math.sin(2*x)+t*x]
 if 0<t<1-K:x=math.acos(t/(1-K));values.append((1-K)*math.sin(x)+t*(math.pi-x))
 return max(values)
C0=conjugate(0.)

def signed(t,z):
 if z>=1+t:return 0.,0.
 if z<=-1:return t-z*math.pi/2,math.pi/2
 c=max(0.,min(1.,(-t+math.sqrt(max(0.,t*t+8*(1+z))))/4));ang=math.acos(c);return .5*math.sin(2*ang)+t*math.sin(ang)-z*ang,ang

def face(ls,ts=(0.,0.,0.)):
 def derivative(nu):return math.pi-sum(signed(t,nu-l)[1] for l,t in zip(ls,ts))
 nu=brentq(derivative,min(ls)-2.,max(ls)+max(ts)+2.,xtol=1e-12);mean=sum(ls)/3;acute=math.pi*(nu-mean)+sum(signed(t,nu-l)[0] for l,t in zip(ls,ts));bounds=[]
 for k in range(3):
  i,j=[z for z in range(3) if z!=k];T=ts[i]+ts[j];d=ls[i]-ls[j];v=max(math.pi*(ls[i]-mean),math.pi*(ls[j]-mean))
  if T>0 and abs(d)<T:v=max(v,math.sqrt(T*T-d*d)+d*math.acos(-d/T)+math.pi*(ls[j]-mean))
  bounds.append(v)
 return max(acute,*bounds),nu

def credit(ids):return sum({ids[j],ids[(j+1)%3]}=={0,1} for j in range(3))

def evaluate(params,full=False):
 eps,tau=map(float,params);w=1-eps;kappa=eps*tau
 if w<=a+.005:return None if full else 100.
 starcaps=[];stars=[];sd=5*math.sin(2*math.pi/5)*(1+math.cos(2*math.pi/5));td=5*math.sin(2*math.pi/5);poly=max(0.,sd-tau*td)*eps
 for st in DATA['stars']:
  counts=st['counts']
  def central(y,save=False):
   v=poly-y*ANG;cells=[]
   for h,count in enumerate(counts):
    if not count:continue
    ls=[y/w]+[-a/w]*h+[0.]*(2-h);val,nu=face(ls);v+=count*w*val;cells.append({'high_base_vertices':h,'nu':round(nu*DEN)})
   return (v,cells) if save else v
  opt=minimize_scalar(central,bounds=(.00001,w-a-.00001),method='bounded',options={'xatol':1e-10});cap,cells=central(opt.x,True);starcaps.append(cap);stars.append({'high_neighbors':st['high_neighbors'],'counts':counts,'center_potential':round(opt.x*DEN),'faces':cells})
 constraints=[];rhs=[];face_rows=[];outside_rows=[]
 for st in DATA['face_rows']:
  ids=st['ids'];val,nu=face([labels[i] for i in ids]);v=np.zeros(8)
  for i in ids:v[i]-=1
  v[5]=credit(ids);constraints.append(v);rhs.append(A-val-SAFETY);face_rows.append({'ids':ids,'nu':round(nu*DEN)})
 for st in DATA['outside_rows']:
  n=st['selected_edges'];ids=st['ids'];edges=[0.,0.,kappa] if n==1 else [kappa,0.,kappa];val,nu=face([labels[i] for i in ids],edges);v=np.zeros(8)
  for i in ids:v[i]-=1
  v[5]=credit(ids);v[2+n]=-1;constraints.append(v);rhs.append(A-val-SAFETY);outside_rows.append({'selected_edges':n,'ids':ids,'nu':round(nu*DEN)})
 for j in range(3):
  v=np.zeros(8);v[3]=5-2*j;v[4]=j;v[6]=-1;constraints.append(v);rhs.append(-SAFETY)
 for e,degrees in [(0,[7,7]),(0,[8]),(1,[7]),(2,[])]:
  high=len(degrees);ordinary=67-high;U=25+2*e
  for ps in itertools.product(range(4),repeat=high):
   po=32-2*e-sum(ps);constant=(134+e)*A+(32-2*e)*C0+e*1.332634+po*(conjugate(b)-C0)-b*((2-e)*math.pi+U*ANG)
   for d,p in zip(degrees,ps):constant+=p*(conjugate(b-a)-C0)+a*(6-d+p)*ANG-FAN*int(p==3)
   for si,st in enumerate(DATA['stars']):
    k=st['high_neighbors']
    if k>high:continue
    v=np.zeros(8);v[0]=sum(d-p for d,p in zip(degrees,ps))-2*k;v[1]=U;v[2]=6*ordinary-po+5-(15-2*k);v[5]=-2*sum(p>0 for p in ps);v[6]=1;v[7]=-1;constraints.append(v);rhs.append(-(constant-5*A+starcaps[si])-SAFETY)
 obj=np.zeros(8);obj[7]=1;res=linprog(obj,A_ub=np.array(constraints),b_ub=np.array(rhs),bounds=[(1e-7,None)]*6+[(0,None),(None,None)],method='highs')
 if not res.success:return None if full else 100.
 if full:return {'variables':res.x.tolist(),'normalized_worst_center':res.x[7],'stars':stars,'face_rows':face_rows,'outside_rows':outside_rows,'parameters':[eps,tau]}
 return res.x[7]

def main():
 opt=differential_evolution(evaluate,[(.42,.62),(1.25,1.309)],seed=142,popsize=6,maxiter=24,tol=1e-8,polish=False,workers=1);eps=F(float(opt.x[0])).limit_denominator(10000);tau=F(float(opt.x[1])).limit_denominator(10000);best=evaluate([float(eps),float(tau)],True);assert best;v=best['variables'];candidate=copy.deepcopy(DATA);candidate.update(radius='2831/25000',epsilon=[eps.numerator,eps.denominator],perimeter_penalty=[tau.numerator,tau.denominator],charges=[round(x*DEN) for x in v[:3]],outside_allowances=[round(x*DEN) for x in v[3:5]],interface_H=round(v[5]*DEN),face_rows=best['face_rows'],outside_rows=best['outside_rows'],stars=best['stars']);mu=math.pi/32;s=math.sin(mu);h=math.sqrt(RAD**2-s*s);outer=32*(s*h+mu-s*math.cos(mu)+K*RAD*s*(math.cos(mu)-h));margin=math.pi-RAD**2*best['normalized_worst_center']-outer
 folder=ROOT/'runtime/B32-M25-coherent-discovery-142';assert not folder.exists();folder.mkdir(parents=True);(folder/'proposal.json').write_text(json.dumps(candidate,indent=2)+'\n',encoding='utf-8');(folder/'receipt.json').write_text(json.dumps({'discovery_only':True,'exact_acceptance':False,'epsilon':str(eps),'tau':str(tau),'numeric_area_margin':margin,'ear_used_for_discovery':1.332634,'best':best,'optimizer_success':bool(opt.success),'function_evaluations':int(opt.nfev),'FAN_slope':str(F('0.05945')),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('DISCOVERY eps',eps,'tau',tau,'numeric minimum margin',margin,flush=True)
if __name__=='__main__':main()
