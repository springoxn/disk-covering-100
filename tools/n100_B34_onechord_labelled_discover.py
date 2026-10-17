"""B34 single-chord core labelled metric; the chord pairs DRR with RRR."""
from pathlib import Path
from fractions import Fraction as F
import sys,math,json,itertools,hashlib
from collections import Counter
from scipy.optimize import differential_evolution,minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'));import n100_B34_chordless_labelled_discover as base
kernel=base.kernel;R=.11324;DEN=10**12;PAIRS=base.PAIRS
def models():
 out=[]
 for high in ((8,),(7,7)):
  n=len(high);types=set()
  for pos in itertools.combinations(range(26),n):
   labels=[int(i in pos) for i in range(26)];ear=labels[0]
   if ear and high==(8,):continue # p5 violates independently verifiedq<=4
   paid=Counter(tuple(sorted((labels[i],labels[(i+1)%26]))) for i in range(1,25));unpaid=Counter(tuple(sorted((labels[25],labels[0]))) for _ in range(1));unpaid[tuple(sorted((labels[0],labels[1])))]+=1;chord=tuple(sorted((labels[25],labels[1])));drr=paid.copy();drr[chord]+=1;rrr=(ear,*sorted((labels[25],labels[1])));types.add((ear,tuple(drr[p] for p in PAIRS),tuple(paid[p] for p in PAIRS),tuple(unpaid[p] for p in PAIRS),rrr))
  for ear,drr,paid,unpaid,rrr in sorted(types):
   minimum=4 if ear else 0;maximum=sum(d-4 for d in high)+ear
   for ph in range(minimum,maximum+1):
    pr=34-ph;nR=26-n
    if pr<(3 if not ear else 0) or pr>2*nR+(1-ear):continue
    counts=[2*nR-pr+2*(1-ear)-rrr.count(0),sum(d-4 for d in high)-ph+2*ear-rrr.count(1)]
    if min(counts)<0:continue
    assert sum(counts)==19;out.append({'high_ring_degrees':list(high),'ear_high':ear,'pH':ph,'pR':pr,'DDD':59,'DDR':counts,'DRR':list(drr),'BRR':list(paid),'BRR0':list(unpaid),'RRR':list(rrr)})
 return out
MODELS=models();TRIPLES=sorted({tuple(m['RRR']) for m in MODELS})
def evaluate(p,full=False):
 ar,ah,b,tau,K=map(float,p);ls=[-ar,-ah];LB=-b
 if base.evaluate(p,True) is None:return None if full else 1e9
 patterns=[('DDD',[0]*3,[0]*3)]+[(f'DDR{i}',[0,0,ls[i]],[0]*3) for i in range(2)]
 for i,j in PAIRS:patterns.extend([(f'DRR{i}{j}',[0,ls[i],ls[j]],[-tau,0,0]),(f'BRR{i}{j}',[ls[i],ls[j],LB],[0,0,tau]),(f'BRR0{i}{j}',[ls[i],ls[j],LB],[0,0,0])])
 for ids in TRIPLES:patterns.append(('RRR'+''.join(map(str,ids)),[ls[i] for i in ids],[tau,0,0]))
 caps={};rows=[]
 for name,labels,edges in patterns:
  value,nu=kernel.face(labels,edges);caps[name]=value;rows.append({'pattern':name,'nu':round(nu*DEN)})
 kernel.K=K;conj=[kernel.conjugate(v-LB) for v in ls];mu=math.pi/34;s=math.sin(mu);rho=math.cos(mu)-math.sqrt(R*R-s*s);outer=34*(mu-s*rho+K*R*s*rho);totals=[]
 for m in MODELS:
  center=59*caps['DDD']+sum(n*caps[f'DDR{i}'] for i,n in enumerate(m['DDR']))
  for region in ('DRR','BRR','BRR0'):center+=sum(n*caps[f'{region}{i}{j}'] for (i,j),n in zip(PAIRS,m[region]))
  center+=caps['RRR'+''.join(map(str,m['RRR']))];center+=m['pR']*conj[0]+m['pH']*conj[1];center-=(m['pR']*ls[0]+(m['pH']-2)*ls[1])*math.pi/3;center+=LB*(2*math.pi+26*math.pi/3);totals.append(center+outer/(R*R))
 if full:return {'parameters':list(map(float,p)),'face_rows':rows,'numeric_min_margin':math.pi-R*R*max(totals),'worst_model':MODELS[totals.index(max(totals))],'model_count':len(MODELS)}
 return max(totals)
def main():
 prior=json.loads((ROOT/'runtime/B34-chordless-labelled-discovery-176/proposal.json').read_text(encoding='utf-8'));initial=[-float(F(x)) for x in prior['labels']]+[-float(F(prior['LB'])),float(F(prior['tau'])),float(F(prior['K']))];opt=differential_evolution(evaluate,[(.015,.3),(.15,.65),(.35,.9),(.2,.9),(.28,.53)],seed=178,popsize=6,maxiter=35,tol=1e-9,polish=False);local=minimize(evaluate,opt.x,method='Nelder-Mead',options={'maxiter':600,'xatol':1e-9,'fatol':1e-10});options=[]
 for xs in (initial,opt.x,local.x):
  ps=[F(float(x)).limit_denominator(10**8) for x in xs];best=evaluate(list(map(float,ps)),True)
  if best:options.append((best['numeric_min_margin'],ps,best))
 assert options;_,ps,best=max(options,key=lambda x:x[0]);folder=ROOT/'runtime/B34-onechord-labelled-discovery-178';assert not folder.exists();folder.mkdir(parents=True);proposal={'schema':'B34-onechord-labelled/v1','radius':'2831/25000','B':34,'denominator':DEN,'labels':[str(-ps[0]),str(-ps[1])],'LB':str(-ps[2]),'tau':str(ps[3]),'K':str(ps[4]),'face_rows':best['face_rows'],'models':MODELS};(folder/'proposal.json').write_text(json.dumps(proposal,indent=2)+'\n',encoding='utf-8');(folder/'receipt.json').write_text(json.dumps({'discovery_only':True,'exact_acceptance':False,'candidate':best,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('B34 ONECHORD DISCOVERY',best['numeric_min_margin'],'models',len(MODELS),flush=True)
if __name__=='__main__':main()
