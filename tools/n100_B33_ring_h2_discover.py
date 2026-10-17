"""Floating four-face discovery for B33 P26/F106 core, h=0/1/2.
Area bookkeeping uses32+h, independent of original B=33.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,math,json,hashlib
from scipy.optimize import differential_evolution,minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'));import n100_B32_M25_coherent_discover as kernel
R=.11324;A=3*math.sqrt(3)/4;ANG=math.pi/3

def evaluate(p,full=False):
 a,b,tau,K=map(float,p);LR=-a;LB=-b
 if not (0<a<b<.98 and 0<tau<1.8 and .15<K<.58 and a+tau/2<.99):return None if full else 1e9
 patterns=[('DDD',[0.,0.,0.],[0.,0.,0.]),('DDR',[0.,0.,LR],[0.,0.,0.]),('DRR',[0.,LR,LR],[-tau,0.,0.]),('BRR',[LR,LR,LB],[0.,0.,tau])];caps=[];rows=[]
 for name,ls,edges in patterns:
  val,nu=kernel.face(ls,edges);caps.append(val);rows.append({'pattern':name,'nu':round(nu*10**12)})
 kernel.K=K;mu=math.pi/33;s=math.sin(mu);rho=math.cos(mu)-math.sqrt(R*R-s*s);outer=33*(mu-s*rho+K*R*s*rho);totals=[]
 for h in range(3):
  center=sum(n*c for n,c in zip((60+h,20-h,26,26),caps))+33*kernel.conjugate(LR-LB)-(32+h)*LR*ANG+LB*(2*math.pi+26*ANG);totals.append(center+outer/(R*R))
 if full:return {'parameters':[a,b,tau,K],'face_rows':rows,'caps':caps,'totals':totals,'numeric_margins':[math.pi-R*R*x for x in totals]}
 return max(totals)
def main():
 initial=[.20663069056,.72993038978,.6623191134,.44];baseline=evaluate(initial,True);opt=differential_evolution(evaluate,[(.08,.4),(.5,.95),(.35,1.),(.2,.55)],seed=161,popsize=6,maxiter=35,tol=1e-9,polish=False);local=minimize(evaluate,opt.x,method='Nelder-Mead',options={'maxiter':500,'xatol':1e-10,'fatol':1e-10});xs=min((initial,opt.x,local.x),key=evaluate);ps=[F(float(x)).limit_denominator(10**8) for x in xs];best=evaluate(list(map(float,ps)),True);assert best;folder=ROOT/'runtime/B33-ring-h2-discovery-161';assert not folder.exists();folder.mkdir(parents=True);proposal={'schema':'B33-ring-h012-four-face/v1','radius':'2831/25000','B':33,'core_vertices':67,'core_faces':106,'core_boundary':26,'deep_vertices':41,'deep_excess':[0,1,2],'LR':str(-ps[0]),'LB':str(-ps[1]),'tau':str(ps[2]),'K':str(ps[3]),'denominator':10**12,'face_rows':best['face_rows']};(folder/'proposal.json').write_text(json.dumps(proposal,indent=2)+'\n',encoding='utf-8');(folder/'receipt.json').write_text(json.dumps({'discovery_only':True,'exact_acceptance':False,'baseline':baseline,'candidate':best,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('RING H012 DISCOVERY',best['numeric_margins'],'K',ps[3],flush=True)
if __name__=='__main__':main()
