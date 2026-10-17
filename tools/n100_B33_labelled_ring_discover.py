"""Discover labelled-ring metric for B33 unique ring5 plus high curvature2.
Single physical multiplier on every DRR/BRR edge pair; no hinge/variance spend.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,math,json,itertools,hashlib
from collections import Counter
from scipy.optimize import differential_evolution,minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'));import n100_B32_M25_coherent_discover as kernel
R=.11324;ANG=math.pi/3;DEN=10**12;PAIRS=[(0,0),(0,1),(1,1),(0,2),(1,2)] # ordinaryR, highH, lowL

def models():
 result=[]
 for high in ((),(7,),(8,),(7,7)):
  n=len(high);excess=sum(d-6 for d in high);h=2-excess;signatures=set()
  for positions in itertools.combinations(range(1,26),n):
   labels=[0]*26;labels[0]=2
   for pos in positions:labels[pos]=1
   edges=Counter(tuple(sorted((labels[i],labels[(i+1)%26]))) for i in range(26));signatures.add(tuple(edges[p] for p in PAIRS))
  for pL in (0,1):
   for pH in range(sum(d-4 for d in high)+1):
    pR=33-pL-pH;nR=25-n;ddr=[2*nR-pR,sum(d-4 for d in high)-pH,1-pL];assert min(ddr)>=0 and sum(ddr)==20-h
    for edges in sorted(signatures):
     assert sum(edges)==26 and edges[3]+edges[4]==2 and edges[1]+2*edges[2]+edges[4]==2*n
     result.append({'high_ring_degrees':list(high),'deep_excess':h,'pL':pL,'pH_total':pH,'pR_total':pR,'DDD':60+h,'DDR':ddr,'edge_counts':list(edges)})
 return result
MODELS=models()
def evaluate(p,full=False):
 ar,ah,c,b,tau,K=map(float,p);labels=[-ar,-ah,c];LB=-b
 if not (.02<=ar<=.4 and .12<=ah<=.7 and -.25<=c<=.4 and .3<=b<=.95 and .15<=tau<=1.1 and .2<=K<=.55 and c>-ar and max(labels+[0.])-min(labels+[0.])+tau/2<.99 and max(labels+[LB])-min(labels+[LB])<.99):return None if full else 1e9
 patterns=[('DDD',[0.,0.,0.],[0.,0.,0.])]+[(f'DDR{i}',[0.,0.,labels[i]],[0.,0.,0.]) for i in range(3)]
 for i,j in PAIRS:patterns.extend([(f'DRR{i}{j}',[0.,labels[i],labels[j]],[-tau,0.,0.]),(f'BRR{i}{j}',[labels[i],labels[j],LB],[0.,0.,tau])])
 caps={};rows=[]
 for name,ls,edges in patterns:
  val,nu=kernel.face(ls,edges);caps[name]=val;rows.append({'pattern':name,'nu':round(nu*DEN)})
 kernel.K=K;conjs=[kernel.conjugate(v-LB) for v in labels];mu=math.pi/33;s=math.sin(mu);rho=math.cos(mu)-math.sqrt(R*R-s*s);outer=33*(mu-s*rho+K*R*s*rho);totals=[]
 for m in MODELS:
  center=m['DDD']*caps['DDD']+sum(n*caps[f'DDR{i}'] for i,n in enumerate(m['DDR']))
  center+=sum(n*(caps[f'DRR{i}{j}']+caps[f'BRR{i}{j}']) for (i,j),n in zip(PAIRS,m['edge_counts']))
  center+=m['pR_total']*conjs[0]+m['pH_total']*conjs[1]+m['pL']*conjs[2]
  centered=m['pR_total']*labels[0]+(sum(6-d for d in m['high_ring_degrees'])+m['pH_total'])*labels[1]+(1+m['pL'])*labels[2];center-=centered*ANG;center+=LB*(2*math.pi+26*ANG);totals.append(center+outer/(R*R))
 if full:return {'parameters':list(map(float,p)),'face_rows':rows,'numeric_min_margin':math.pi-R*R*max(totals),'worst_model':MODELS[totals.index(max(totals))],'model_count':len(MODELS),'totals':totals}
 return max(totals)
def main():
 initial=[.13,.48,.15,.56,.49,.44];base=evaluate(initial,True);opt=differential_evolution(evaluate,[(.05,.28),(.2,.6),(.02,.28),(.45,.85),(.3,.8),(.25,.53)],seed=164,popsize=6,maxiter=40,tol=1e-9,polish=False);ref=minimize(evaluate,opt.x,method='Nelder-Mead',options={'maxiter':650,'xatol':1e-9,'fatol':1e-10});options=[]
 for xs in (initial,opt.x,ref.x):
  ps=[F(float(x)).limit_denominator(10**8) for x in xs];best=evaluate(list(map(float,ps)),True)
  if best:options.append((best['numeric_min_margin'],ps,best))
 assert options;_,ps,best=max(options,key=lambda x:x[0]);folder=ROOT/'runtime/B33-labelled-ring-discovery-164';assert not folder.exists();folder.mkdir(parents=True);candidate={'schema':'B33-unique-ring5-labelled-metric/v1','radius':'2831/25000','B':33,'denominator':DEN,'labels':[str(-ps[0]),str(-ps[1]),str(ps[2])],'LB':str(-ps[3]),'tau':str(ps[4]),'K':str(ps[5]),'face_rows':best['face_rows'],'models':MODELS};(folder/'proposal.json').write_text(json.dumps(candidate,indent=2)+'\n',encoding='utf-8');(folder/'receipt.json').write_text(json.dumps({'discovery_only':True,'exact_acceptance':False,'baseline':base,'candidate':best,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('LABELLED RING DISCOVERY',best['numeric_min_margin'],'models',len(MODELS),'params',[str(x) for x in ps],flush=True)
if __name__=='__main__':main()
