"""Discovery for B34 no-low M26 core, zero/one chord, deep excess0/1/2.
Six face supports, paired physical edge multipliers; no hinge payment.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,math,json,hashlib
from scipy.optimize import differential_evolution,minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'));import n100_B32_M25_coherent_discover as kernel
R=.11324;ANG=math.pi/3;DEN=10**12

def evaluate(p,full=False):
 a,b,tau,K=map(float,p);LR=-a;LB=-b
 if not (.000001<a<b<.98 and .000001<tau<1.8 and .15<K<.56 and a+tau/2<.99):return None if full else 1e9
 mu=math.pi/34;rr=R*R;sm=math.sin(mu);cm=math.cos(mu);hm=math.sqrt(rr-sm*sm);bt=rr*K*(hm*cm+sm*sm)/R;fm=sm*hm+mu-sm*cm+bt*(math.asin(sm/R)-mu);dm=cm*(rr-2*sm*sm)/hm+2*sm*sm+bt*(cm/hm-1);gap0=fm-dm*mu-K*rr*math.sqrt(2*(1-R))
 if gap0<2e-6:return None if full else 1e9
 patterns=[('DDD',[0.,0.,0.],[0.,0.,0.]),('DDR',[0.,0.,LR],[0.,0.,0.]),('DRR',[0.,LR,LR],[-tau,0.,0.]),('BRR',[LR,LR,LB],[0.,0.,tau]),('BRR0',[LR,LR,LB],[0.,0.,0.]),('RRR',[LR,LR,LR],[0.,0.,tau])];caps={};rows=[]
 for name,ls,edges in patterns:
  val,nu=kernel.face(ls,edges);caps[name]=val;rows.append({'pattern':name,'nu':round(nu*DEN)})
 kernel.K=K;rho=cm-hm;outer=34*(mu-sm*rho+K*R*sm*rho);totals=[];cases=[]
 for chord in (0,1):
  for h in range(3):
   counts=[58+chord+h,20-chord-h,26-chord,26-2*chord,2*chord,chord];center=sum(n*caps[name] for n,(name,_,_) in zip(counts,patterns));center+=34*kernel.conjugate(LR-LB)-(32+h)*LR*ANG+LB*(2*math.pi+26*ANG);total=center+outer/rr;totals.append(total);cases.append({'chords':chord,'deep_excess':h,'counts':counts,'numeric_margin':math.pi-rr*total})
 if full:return {'parameters':[a,b,tau,K],'face_rows':rows,'cases':cases,'numeric_min_margin':math.pi-rr*max(totals),'numeric_global_zero_deficit':gap0}
 return max(totals)
def main():
 initial=[.20663069056,.72993038978,.6623191134,.44];base=evaluate(initial,True);opt=differential_evolution(evaluate,[(.03,.35),(.4,.94),(.25,.95),(.25,.54)],seed=173,popsize=6,maxiter=35,tol=1e-9,polish=False);local=minimize(evaluate,opt.x,method='Nelder-Mead',options={'maxiter':450,'xatol':1e-9,'fatol':1e-10});options=[]
 for xs in (initial,opt.x,local.x):
  ps=[F(float(x)).limit_denominator(10**8) for x in xs];best=evaluate(list(map(float,ps)),True)
  if best:options.append((best['numeric_min_margin'],ps,best))
 assert options;_,ps,best=max(options,key=lambda x:x[0]);folder=ROOT/'runtime/B34-uniform-core-discovery-173';assert not folder.exists();folder.mkdir(parents=True);proposal={'schema':'B34-M26-core-zero-one-chord/v1','radius':'2831/25000','B':34,'core_vertices':66,'core_boundary':26,'core_faces':104,'deep_vertices':40,'LR':str(-ps[0]),'LB':str(-ps[1]),'tau':str(ps[2]),'K':str(ps[3]),'denominator':DEN,'face_rows':best['face_rows']};(folder/'proposal.json').write_text(json.dumps(proposal,indent=2)+'\n',encoding='utf-8');(folder/'receipt.json').write_text(json.dumps({'discovery_only':True,'exact_acceptance':False,'baseline':base,'candidate':best,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('B34 UNIFORM CORE DISCOVERY',best['numeric_min_margin'],'params',[str(x) for x in ps],flush=True)
if __name__=='__main__':main()
