"""Independent geometric strip and multi-radius verdict audit."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def main():
 path=ROOT/'verify/out/n100-multiradius-capacity.json';z=json.loads(path.read_text(encoding='utf-8'));r=F(z['radius']);pl,ph=map(F,z['pi_interval']);types={t['kind']:t for t in z['types']};checked=0;counts={'excluded':0,'capacity_satisfied':0,'undecided':0}
 def atan(q,n):return sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(n)),F(0))
 need(pl<16*atan(5,10)-4*atan(239,9) and ph>16*atan(5,9)-4*atan(239,10),'pi independently bounded');need([F(p['target_radius']) for p in z['profiles']]==[F(i,100) for i in range(1,101)],'all 100 targets')
 for profile in z['profiles']:
  t=F(profile['target_radius']);L=46*pl*min(t,r)**2;U=46*ph*min(t,r)**2
  for part in profile['parts']:
   ty=types[part['type']];d=F(ty['distance']);xmin=max(-t,d-r);xmax=min(t,d+r);rows=part['slabs'];lower=upper=F(0)
   if xmin>=xmax:need(not rows,'empty lens')
   else:
    need(len(rows)==512,'complete slab count')
    for j,row in enumerate(rows):
     a,b,l,u=map(F,row);need(a==xmin+(xmax-xmin)*j/512 and b==xmin+(xmax-xmin)*(j+1)/512,'exact partition');v0=[t*t-a*a,t*t-b*b];v1=[r*r-(a-d)**2,r*r-(b-d)**2];low=max(F(0),min(v0+v1));max0=t*t if a<=0<=b else max(v0);max1=r*r if a<=d<=b else max(v1);high=max(F(0),min(max0,max1));need(0<=l<=u and (l/2)**2<=low and (u/2)**2>=high,'independent height enclosure');lower+=(b-a)*l;upper+=(b-a)*u;checked+=1
   need(lower==F(part['lower']) and upper==F(part['upper']),'saved type integrals');L+=ty['count']*lower;U+=ty['count']*upper
  need(L==F(profile['total_capacity_lower']) and U==F(profile['total_capacity_upper']),'profile sums');verdict='excluded' if U<pl*t*t else ('capacity_satisfied' if L>=ph*t*t else 'undecided');need(verdict==profile['verdict'],'strict capacity verdict');counts[verdict]+=1
 need(counts==z['counts'],'summary counts');out=ROOT/'verify/out/n100-multiradius-capacity-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-multiradius-capacity-independent/v1','verified_independent_strip_profiles':True,'profiles':100,'slabs_checked':checked,'counts':counts,'scope':'checks geometry strips, area sums and verdicts for saved radial multiset; arc series lower bound analytic and not independently rederived here; no actual covering or all-k54 exclusion','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent profiles',counts,'slabs',checked)
if __name__=='__main__':main()
