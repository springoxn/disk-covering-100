"""B34 chordless core labelled R/H metric discovery only."""
from pathlib import Path
from fractions import Fraction as F
import sys,math,json,itertools,hashlib
from collections import Counter
from scipy.optimize import differential_evolution,minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'));import n100_B32_M25_coherent_discover as kernel
R=.11324;DEN=10**12;PAIRS=[(0,0),(0,1),(1,1)]
def models():
 out=[]
 for high in ((7,),(8,),(7,7)):
  n=len(high);h=2-sum(d-6 for d in high);cycles=set()
  for pos in itertools.combinations(range(26),n):
   lab=[int(i in pos) for i in range(26)];ct=Counter(tuple(sorted((lab[i],lab[(i+1)%26]))) for i in range(26));cycles.add(tuple(ct[p] for p in PAIRS))
  for ph in range(sum(d-4 for d in high)+1):
   pr=34-ph;ddr=[2*(26-n)-pr,sum(d-4 for d in high)-ph];assert sum(ddr)==20-h and min(ddr)>=0
   for edges in sorted(cycles):out.append({'high_ring_degrees':list(high),'deep_excess':h,'pH':ph,'pR':pr,'DDD':58+h,'DDR':ddr,'edges':list(edges)})
 return out
MODELS=models()
def evaluate(p,full=False):
 ar,ah,b,tau,K=map(float,p);ls=[-ar,-ah];LB=-b
 if not (.00001<ar<.5 and .05<ah<.8 and .25<b<.97 and .05<tau<1.4 and .2<K<.56 and max(ls+[0])-min(ls+[0])+tau/2<.99 and max(ls+[LB])-min(ls+[LB])<.99):return None if full else 1e9
 mu=math.pi/34;s=math.sin(mu);co=math.cos(mu);hm=math.sqrt(R*R-s*s);bt=R*K*(hm*co+s*s);fm=s*hm+mu-s*co+bt*(math.asin(s/R)-mu);dm=co*(R*R-2*s*s)/hm+2*s*s+bt*(co/hm-1);zero=fm-dm*mu-K*R*R*math.sqrt(2*(1-R))
 if zero<2e-6:return None if full else 1e9
 patterns=[('DDD',[0]*3,[0]*3)]+[(f'DDR{i}',[0,0,ls[i]],[0]*3) for i in range(2)]
 for i,j in PAIRS:patterns.extend([(f'DRR{i}{j}',[0,ls[i],ls[j]],[-tau,0,0]),(f'BRR{i}{j}',[ls[i],ls[j],LB],[0,0,tau])])
 caps={};rows=[]
 for name,labels,edges in patterns:
  val,nu=kernel.face(labels,edges);caps[name]=val;rows.append({'pattern':name,'nu':round(nu*DEN)})
 kernel.K=K;conj=[kernel.conjugate(v-LB) for v in ls];rho=co-hm;outer=34*(mu-s*rho+K*R*s*rho);totals=[]
 for m in MODELS:
  center=m['DDD']*caps['DDD']+sum(n*caps[f'DDR{i}'] for i,n in enumerate(m['DDR']));center+=sum(n*(caps[f'DRR{i}{j}']+caps[f'BRR{i}{j}']) for (i,j),n in zip(PAIRS,m['edges']));center+=m['pR']*conj[0]+m['pH']*conj[1];center-=(m['pR']*ls[0]+(m['pH']-sum(d-6 for d in m['high_ring_degrees']))*ls[1])*math.pi/3;center+=LB*(2*math.pi+26*math.pi/3);totals.append(center+outer/(R*R))
 if full:return {'parameters':list(map(float,p)),'face_rows':rows,'numeric_min_margin':math.pi-R*R*max(totals),'worst_model':MODELS[totals.index(max(totals))],'model_count':len(MODELS),'zero_gap':zero}
 return max(totals)
def main():
 initial=[.10,.48,.56,.49,.44];opt=differential_evolution(evaluate,[(.015,.3),(.15,.65),(.35,.9),(.2,.9),(.28,.53)],seed=176,popsize=7,maxiter=45,tol=1e-9,polish=False);local=minimize(evaluate,opt.x,method='Nelder-Mead',options={'maxiter':700,'xatol':1e-9,'fatol':1e-10});options=[]
 for xs in (initial,opt.x,local.x):
  ps=[F(float(x)).limit_denominator(10**8) for x in xs];best=evaluate(list(map(float,ps)),True)
  if best:options.append((best['numeric_min_margin'],ps,best))
 assert options;_,ps,best=max(options,key=lambda x:x[0]);folder=ROOT/'runtime/B34-chordless-labelled-discovery-176';assert not folder.exists();folder.mkdir(parents=True);proposal={'schema':'B34-chordless-labelled/v1','radius':'2831/25000','B':34,'denominator':DEN,'labels':[str(-ps[0]),str(-ps[1])],'LB':str(-ps[2]),'tau':str(ps[3]),'K':str(ps[4]),'face_rows':best['face_rows'],'models':MODELS};(folder/'proposal.json').write_text(json.dumps(proposal,indent=2)+'\n',encoding='utf-8');(folder/'receipt.json').write_text(json.dumps({'discovery_only':True,'exact_acceptance':False,'candidate':best,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('B34 CHORDLESS DISCOVERY',best['numeric_min_margin'],'models',len(MODELS),'params',[str(x) for x in ps],flush=True)
if __name__=='__main__':main()
