"""Floating discovery for B33 highM any-five row; exact verifier required.
Optimize actual total area objective including the K-dependent boundary.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,math,json,copy,itertools,hashlib
import numpy as np
from scipy.optimize import linprog,differential_evolution,minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'));import n100_B32_M25_coherent_discover as support
P=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working/B33_highM_any_five_0p11323_proposal.json';DATA=json.loads(P.read_text(encoding='utf-8'));R=.11324;A=3*math.sqrt(3)/4;ANG=math.pi/3;SAFETY=2e-7;C=.03;T=.092;SPAN=.6934
# gH,gB,gO,gL,tH,tO,tL,u0,beta,eta,apex,flag
OBJ=np.array([0.,26.,0.,0.,0.,0.,0.,67.,33.,1.,26.,-1.]);BOUNDS=[(1e-9,None)]*4+[(0,None)]*3+[(1e-9,None),(None,None),(None,None),(0,None),(1e-7,None)]
def evaluate(params,full=False):
 a,b,c,K=map(float,params);labels=[-a,-b,0.,c]
 if not (.1<=a<=.6 and .1<=b<=.65 and .02<=c<=.4 and .2<=K<=.6) or max(labels)-min(labels)>=.98:return None if full else 1e9
 support.K=K;C0=support.conjugate(0.);rows=[];rhs=[];faces=[]
 for ids in itertools.combinations_with_replacement(range(4),3):
  cap,nu=support.face([labels[i] for i in ids]);v=np.zeros(12)
  for i in ids:v[i]-=1
  for ix,typ in enumerate((0,2,3)):v[4+ix]=sum({ids[j],ids[(j+1)%3]}=={typ,1} for j in range(3))
  rows.append(v);rhs.append(A-cap-SAFETY);faces.append({'indices':list(ids),'nu':round(nu*10**10)})
 for d in range(5,9):
  for p in range(d):
   ix=3 if d==5 else 2 if d==6 else 0;lv=labels[ix];pay=C*max(0.,(p+1)*T-SPAN/2)/(2*R*R);constant=p*(support.conjugate(lv+b)-C0)-lv*(6-d+p)*ANG-pay;v=np.zeros(12);v[ix]=d-p
   if p:v[4+{0:0,2:1,3:2}[ix]]=-2
   v[7]=-1;v[8]=-p;v[9]=-(d-6);v[10]=-int(p>0);v[11]=int(d==5);rows.append(v);rhs.append(-constant-SAFETY)
 v=np.zeros(12);v[9]=-1;v[10]=v[1]=1;rows.append(v);rhs.append(b*ANG-SAFETY)
 w=2/(1+math.sqrt(1-2*R));ear=w+math.sqrt(2*w-w*w)-K*math.sqrt(2*w);v=np.zeros(12);v[8]=-2;v[9]=-1;v[10]=v[1]=2;rows.append(v);rhs.append(-A+2*C0-ear-b*math.pi+2*b*ANG-SAFETY)
 y=(K+math.sqrt(K*K+8))/4;bad0=w+math.sqrt(1-y*y)*(y-K)-C0;v=np.zeros(12);v[8]=v[9]=-1;rows.append(v);rhs.append(-bad0-SAFETY)
 res=linprog(OBJ,A_ub=np.array(rows),b_ub=np.array(rhs),bounds=BOUNDS,method='highs')
 if not res.success:return None if full else 1e9
 mu=math.pi/33;s=math.sin(mu);rho=math.cos(mu)-math.sqrt(R*R-s*s);outer=33*(mu-s*rho+K*R*s*rho);center=132*A+33*C0-b*(2*math.pi+26*ANG)+res.fun;total=center+outer/(R*R)
 if full:return {'variables':res.x.tolist(),'faces':faces,'normalized_center':center,'outer_area':outer,'total_normalized_area':total,'numeric_area_margin':math.pi-R*R*total,'parameters':[a,b,c,K]}
 return total
def main():
 row=DATA['row'];PD=row['potential_denominator'];initial=[-row['high_potential']/PD,-row['boundary_potential']/PD,row['low_potential']/PD,.44];baseline=evaluate(initial,True);assert baseline;opt=differential_evolution(evaluate,[(.18,.45),(.18,.5),(.08,.35),(.2,.6)],seed=154,popsize=6,maxiter=32,tol=1e-8,polish=False);ref=minimize(evaluate,opt.x,method='Nelder-Mead',options={'maxiter':500,'xatol':1e-9,'fatol':1e-10});xs=min([initial,opt.x,ref.x],key=evaluate);params=[F(float(x)).limit_denominator(10**8) for x in xs];params[:3]=[F(round(float(x)*PD),PD) for x in params[:3]];best=evaluate(list(map(float,params)),True);assert best;candidate=copy.deepcopy(DATA);candidate['radius']='2831/25000';candidate['halfside_multiplier']=[params[3].numerator,params[3].denominator];row=candidate['row'];row.update(high_potential=-round(float(params[0])*PD),boundary_potential=-round(float(params[1])*PD),low_potential=round(float(params[2])*PD),faces=best['faces']);names=['charge_a','charge_b','charge_0','charge_low','interface_a','interface_0','interface_low','u0','beta','eta','apex','flag']
 for name,x in zip(names,best['variables']):row[name]=round(x*row['denominator'])
 folder=ROOT/'runtime/B33-high-row-discovery-154';assert not folder.exists();folder.mkdir(parents=True);(folder/'proposal.json').write_text(json.dumps(candidate,indent=2)+'\n',encoding='utf-8');(folder/'receipt.json').write_text(json.dumps({'discovery_only':True,'exact_acceptance':False,'hinge_slope':str(F(3,100)),'hinge_zero':str(F(23,250)),'halfside_multiplier':str(params[3]),'baseline_reoptimized_same_K':baseline,'candidate':best,'optimizer_success':bool(opt.success),'local_success':bool(ref.success),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('B33 HIGH DISCOVERY',best['numeric_area_margin'],'K',params[3],'baseline reoptimized',baseline['numeric_area_margin'],flush=True)
if __name__=='__main__':main()
