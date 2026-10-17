"""Discover coherent5 replacement for B33 residual unique deep5, high curvature2.
Frozen highM row; only local support eps/tau/free-center optimized.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,math,json,itertools,hashlib
from scipy.optimize import differential_evolution,minimize_scalar,minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'));import n100_B32_M25_coherent_discover as kernel
P=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working/B33_highM_any_five_0p11323_proposal.json';ROW=json.loads(P.read_text(encoding='utf-8'))['row'];D=ROW['denominator'];PD=ROW['potential_denominator'];ls=[ROW['high_potential']/PD,ROW['boundary_potential']/PD,0.,ROW['low_potential']/PD];g=[ROW[k]/D for k in ('charge_a','charge_b','charge_0','charge_low')];interface=[ROW[k]/D for k in ('interface_a','interface_0','interface_low')];A=3*math.sqrt(3)/4;ANG=math.pi/3;PATTERNS=[(0,[5,0,0]),(1,[3,2,0]),(2,[2,2,1]),(2,[1,4,0])];DEN=10**12

def evaluate(params,full=False):
 eps,tau=map(float,params);w=1-eps;a=-ls[0]
 if not .05<eps<.66 or not 1.1<tau<1.32 or w<a+.005:return None if full else 1e9
 outside=[];extras={1:[],2:[]};poly=eps*max(0.,5*math.sin(2*math.pi/5)*(1+math.cos(2*math.pi/5))-tau*5*math.sin(2*math.pi/5))
 for n in (1,2):
  idslist=itertools.product([0,2],[0,2],[0,1,2]) if n==1 else itertools.product([0,2],repeat=3)
  for ids in idslist:
   if ids.count(0)>2:continue
   edges=[0.,0.,eps*tau] if n==1 else [eps*tau,0.,eps*tau];val,nu=kernel.face([ls[i] for i in ids],edges);credit=sum(interface[ix]*sum({ids[j],ids[(j+1)%3]}=={typ,1} for j in range(3)) for ix,typ in enumerate((0,2,3)));old=A+sum(g[i] for i in ids)-credit;extras[n].append(val-old);outside.append({'selected_edges':n,'ids':list(ids),'nu':round(nu*DEN)})
 D1,D2=max(extras[1]),max(extras[2]);J=max((5-2*j)*D1+j*D2 for j in range(3));stars=[];gains=[]
 for k,counts in PATTERNS:
  def central(y,save=False):
   result=poly-(y-ls[3])*ANG;cells=[]
   for h,count in enumerate(counts):
    if not count:continue
    vals=[y/w]+[ls[0]/w]*h+[0.]*(2-h);cap,nu=kernel.face(vals);result+=count*w*cap;cells.append({'high_base_vertices':h,'nu':round(nu*DEN)})
   return (result,cells) if save else result
  opt=minimize_scalar(central,bounds=(.00001,w-a-.00001),method='bounded',options={'xatol':1e-11});y=round(opt.x*DEN)/DEN;cap,cells=central(y,True);old=5*A+5*g[3]+2*k*g[0]+(10-2*k)*g[2];gain=old-cap-J;gains.append(gain);stars.append({'high_neighbors':k,'counts':counts,'center_potential':round(y*DEN),'faces':cells})
 if full:return {'parameters':[eps,tau],'outside_rows':outside,'stars':stars,'gains':gains,'D1':D1,'D2':D2,'J':J}
 return -min(gains)
def main():
 baseline=evaluate([.3,1.3],True);opt=differential_evolution(evaluate,[(.12,.6),(1.2,1.30901699)],seed=162,popsize=6,maxiter=25,tol=1e-9,polish=False);local=minimize(evaluate,opt.x,method='Nelder-Mead',options={'maxiter':350,'xatol':1e-10,'fatol':1e-10});xs=min(([.3,1.3],opt.x,local.x),key=evaluate);ps=[F(float(x)).limit_denominator(10**8) for x in xs];best=evaluate(list(map(float,ps)),True);assert best;folder=ROOT/'runtime/B33-deep5-coherent-discovery-162';assert not folder.exists();folder.mkdir(parents=True);candidate={'schema':'B33-highM-deep5-coherent/v1','radius':'2831/25000','B':33,'M':26,'denominator':DEN,'epsilon':str(ps[0]),'tau':str(ps[1]),'outside_rows':best['outside_rows'],'stars':best['stars'],'reference_sha256':hashlib.sha256(P.read_bytes()).hexdigest()};(folder/'proposal.json').write_text(json.dumps(candidate,indent=2)+'\n',encoding='utf-8');(folder/'receipt.json').write_text(json.dumps({'discovery_only':True,'exact_acceptance':False,'baseline':baseline,'candidate':best,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('B33 DEEP5 DISCOVERY gains',best['gains'],'eps/tau',[str(x) for x in ps],flush=True)
if __name__=='__main__':main()
