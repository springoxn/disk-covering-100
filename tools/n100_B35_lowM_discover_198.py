"""Discovery-only B35 lowM replacement search around flagged row."""
from pathlib import Path
import sys,math,json,itertools,hashlib
from fractions import Fraction as F
from scipy.optimize import differential_evolution,minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'));import n100_B32_M25_coherent_discover as kernel
R=.11324;DEN=10**12;ANG=math.pi/3
def evalp(p,full=False):
 a,b,c,tau,K=map(float,p);labels=[-a,-b,c];LB=-0.55
 if not (.05<a<.5 and .05<b<.9 and -.1<c<.3 and .1<tau<1.3 and .2<K<.55 and max(labels+[0])-min(labels+[0])+tau/2<.99):return 1e9
 pats=[('DDD',[0,0,0],[0,0,0])]+[(f'DDR{i}',[0,0,labels[i]],[0,0,0]) for i in range(3)]
 for i,j in ((0,0),(0,1),(1,1)):pats.extend([(f'DRR{i}{j}',[0,labels[i],labels[j]],[-tau,0,0]),(f'BRR{i}{j}',[labels[i],labels[j],LB],[0,0,tau])])
 caps={};rows=[]
 for n,l,e in pats:v,nu=kernel.face(l,e);caps[n]=v;rows.append({'pattern':n,'nu':round(nu*DEN)})
 kernel.K=K;mu=math.pi/35;s=math.sin(mu);rho=math.cos(mu)-math.sqrt(R*R-s*s);outer=35*(mu-s*rho+K*R*s*rho);conj=[kernel.conjugate(v-LB) for v in labels];tot=[]
 for ph in (11,12):
  center=59*caps['DDD']+sum(n*caps[f'DDR{i}'] for i,n in enumerate([7+ph,12-ph]));center+=sum(n*(caps[f'DRR{i}{j}']+caps[f'BRR{i}{j}']) for (i,j),n in zip(((0,0),(0,1),(1,1)),(13,6,6)));center+=34*conj[0]+ph*conj[1];center-=(34*labels[0]+(ph-4)*labels[1])*ANG;center+=LB*(2*math.pi+25*ANG);tot.append(center+outer/(R*R))
 gap=math.pi-R*R*max(tot)
 if full:return {'parameters':list(map(float,p)),'margin':gap,'rows':rows}
 return -gap

def main():
 opt=differential_evolution(evalp,[(.05,.3),(.2,.8),(.0,.25),(.2,.9),(.25,.53)],seed=198,popsize=6,maxiter=35,tol=1e-9,polish=False);loc=minimize(evalp,opt.x,method='Nelder-Mead',options={'maxiter':500});ps=[F(float(x)).limit_denominator(10**8) for x in loc.x];best=evalp(list(map(float,ps)),True);folder=ROOT/'runtime/B35-lowM-discovery-198';assert not folder.exists();folder.mkdir(parents=True);(folder/'proposal.json').write_text(json.dumps({'schema':'B35-lowM-discovery/v1','radius':'2831/25000','parameters':[str(x) for x in ps],'candidate':best},indent=2)+'\n');print('B35 LOW DISCOVERY',best['margin'],flush=True)
if __name__=='__main__':main()
