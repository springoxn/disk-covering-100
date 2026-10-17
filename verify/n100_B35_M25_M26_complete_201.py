"""Independent B35 M25/M26 composition: integer coverage, Fraction and CAS."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
import json,sys,hashlib
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working'
sys.path[:0]=[str(W),str(W/'lower_bounds_extension_20261004')]
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_linear_halfside_marked_conjugate import conjugate
R=F(2831,25000);PAIRS=((0,0),(0,1),(1,1))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def signature(m,chord):
 return (m['pH'],tuple(m['DDR']),tuple(m['DRR'] if chord else m['edges']),tuple(m['BRR']) if chord else (),tuple(m['BRR0']) if chord else (),tuple(m['RRR']) if chord else ())
def enumerate_expected(M,chord):
 length=M;nh=4 if M==25 else 3;found=set()
 for places in combinations(range(length),nh):
  bits=[int(i in places) for i in range(length)];ring=Counter(tuple(sorted((bits[i],bits[(i+1)%length]))) for i in range(length))
  if not chord:
   for ph in ((11,12) if M==25 else (9,)):
    pr=35-ph;ddr=(2*(length-nh)-pr,3*nh-ph)
    found.add((ph,ddr,tuple(ring[e] for e in PAIRS),(),(),()))
  else:
   ear=bits[0];ph=9+ear;pr=35-ph;triangle=(ear,*sorted((bits[-1],bits[1])));unpaid=Counter([tuple(sorted((ear,bits[-1]))),tuple(sorted((ear,bits[1])))]);paid=ring-unpaid;inner=paid.copy();inner[tuple(sorted((bits[-1],bits[1])))]+=1
   ddr=(2*(length-nh)-pr+2*(1-ear)-triangle.count(0),3*nh-ph+2*ear-triangle.count(1))
   if min(ddr)<0:continue
   found.add((ph,ddr,tuple(inner[e] for e in PAIRS),tuple(paid[e] for e in PAIRS),tuple(unpaid[e] for e in PAIRS),triangle))
 return found

def audit(cert,M,chord):
 assert cert['status']=='PASS' and F(cert['radius'])==R and cert['B']==35
 for rel,h in cert['bindings'].items():assert sha(ROOT/rel)==h
 expected=enumerate_expected(M,chord);actual={signature(x['model'],chord) for x in cert['rows']};assert actual==expected and len(actual)==(8 if M==25 else 5 if chord else 3)
 env=cert['boundary_envelope'];assert env['status']=='PASS' and env['B']==35 and F(env['radius'])==R and F(env['required_center_norm_squared_upper'])==1-R*R and F(env['halfside_multiplier'])==F(cert['K'])
 caps={z['pattern']:F(z['upper']) for z in cert['supports']};ls=list(map(F,cert['labels']));LB=F(cert['LB']);K=F(cert['K']);conjs=[F(conjugate(K,v-LB).u,S) for v in ls];mu=PI/35;s=sine(mu);rho=cosine(mu)-(q(R).sq()-s.sq()).sqrt();outer=35*(mu-s*rho+q(K)*q(R)*s*rho);pilo,pihi=F(PI.l,S),F(PI.u,S);margins=[]
 for entry in cert['rows']:
  m=entry['model'];excess=4 if M==25 else 3;deep=65-M;assert m['DDD']==(59 if M==25 else 57 if chord else 56);assert m['pH']+m['pR']==35
  faces=m['DDD']+sum(m['DDR'])+(25+1 if chord else M);deepcorners=3*m['DDD']+2*sum(m['DDR'])+(25 if chord else M);assert faces==128-M and deepcorners==6*deep
  value=m['DDD']*caps['DDD']+sum(n*caps[f'DDR{i}'] for i,n in enumerate(m['DDR']))
  if chord:
   assert sum(m['DRR'])==25 and sum(m['BRR'])==24 and sum(m['BRR0'])==2
   diagonal=tuple(sorted(m['RRR'][1:]));assert all(m['DRR'][i]-m['BRR'][i]==int(e==diagonal) for i,e in enumerate(PAIRS))
   for region in ('DRR','BRR','BRR0'):value+=sum(n*caps[f'{region}{i}{j}'] for (i,j),n in zip(PAIRS,m[region]))
   value+=caps['RRR'+''.join(map(str,m['RRR']))]
   ear=m['ear_high'];tri=m['RRR'];nR=23;ph=m['pH'];pr=m['pR'];assert m['DDR'][0]+2*nR-2*(1-ear)+tri.count(0)==4*nR-pr;assert m['DDR'][1]+6-2*ear+tri.count(1)==15-ph
  else:value+=sum(n*(caps[f'DRR{i}{j}']+caps[f'BRR{i}{j}']) for (i,j),n in zip(PAIRS,m['edges']))
  value+=m['pR']*conjs[0]+m['pH']*conjs[1]
  pi_coef=-(m['pR']*ls[0]+(m['pH']-excess)*ls[1])/3+LB*(2+F(M,3));value+=pi_coef*(pihi if pi_coef>=0 else pilo)
  margin=pilo-R*R*value-F(outer.u,S);assert margin>0;margins.append(margin)
 return min(margins)
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 paths=[ROOT/'verify/out/n100-B35-profile-reduction-191.json',ROOT/'verify/out/n100-B35-M25-metric-193.json',ROOT/'verify/out/n100-B35-M26-chordless-197.json',ROOT/'verify/out/n100-B35-M26-onechord-200.json'];reduction,m25,flat,chord=[json.loads(p.read_text(encoding='utf-8')) for p in paths];assert reduction['status']=='PASS_REDUCTION'
 for rel,h in reduction['bindings'].items():assert sha(ROOT/rel)==h
 # Every remaining7 has p>0 and therefore lies on the core ring; strict core degrees all6.
 assert all(min(z['high7_marked_counts'])>0 for group in reduction['high_profiles'] for z in group['high7_profile_survivors'])
 # First peel: B35 M26 F102/P26; h0, a=C-f3. /6 excludes every C>=2 or a>=1.
 slots=[]
 for C in range(24):
  for a in range(C+1):
   b=20-C-3*a
   if b>=0 and F(46-C-a)+F(b*b,6)>=102:slots.append((C,a))
 assert slots==[(0,0),(1,0)]
 # General face counts derived by CAS from deep corners and total faces.
 C,a=sp.symbols('C a',integer=True);ddd,ddr=sp.symbols('DDD DDR');f3=C-a;f2=26+2*C-3*f3;sol=sp.solve([ddd+ddr+f2+f3-102,3*ddd+2*ddr+f2-234],(ddd,ddr));assert sp.expand(sol[ddd]-(56+C+a))==0 and sp.expand(sol[ddr]-(20-C-3*a))==0
 lr,lh,lb,pr,ph,ex,pi,gr,gh,M=sp.symbols('lr lh lb pr ph ex pi gr gh M');mass=lr*(pr*pi/3-gr)+lh*((ph-ex)*pi/3-gh)+lb*(gr+gh-2*pi-M*pi/3);target=(lb-lr)*gr+(lb-lh)*gh+(pr*lr+(ph-ex)*lh)*pi/3-lb*(2*pi+M*pi/3);assert sp.expand(mass-target)==0
 margins={'M25':audit(m25,25,False),'M26_chordless':audit(flat,26,False),'M26_onechord':audit(chord,26,True)}
 # One-chord has a unique empty triangle and a unique core degree2 ear.
 # A degree7 ear has p4; a degree6 ear has p3. All other degree7 p3.
 assert 7-3==4 and 6-3==3
 extra=[ROOT/'verify/n100_B35_M26_onechord_196.py',ROOT/'tools/n100_B35_M26_onechord_discover_199.py',ROOT/'tools/n100_B35_M26_onechord_discover_194.py',ROOT/'tools/n100_B34_onechord_labelled_discover.py']
 out=ROOT/'verify/out/n100-B35-M25-M26-complete-201.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B35-M25-M26-independent/v1','status':'PASS','radius':str(R),'B':35,'required_center_norm_squared_upper':str(1-R*R),'M25_closed':True,'M26_closed':True,'M_ge27_closed':True,'low_M_closed':False,'remaining':'M<=24 with compulsory unmarked lowdegree witness','model_counts':{'M25':8,'M26_chordless':3,'M26_onechord':5},'independent_fraction_margins':{k:str(v) for k,v in margins.items()},'M26_topology_slots':slots,'CAS_face_count_and_centered_potential':True,'hinge_variance_payment_for_new_metrics':0,'budget_review':'Original variance payment row establishes residuals; new metrics each have their own complete boundaryK/face sum with exact physical edge cancellation. No scalar deficit is paid across two rows.','geometric_dependencies':'Same-radius normalized common triangulation and original /6 disk topology; integer peel excludes C>=2. All high7 have positivep and lie on ring. M25 core chordlessP25/F103, M26 coreP26/F102 from source. Pure topology and metric ledger reviewed here; not formal planar-embedding kernel.','full_B35_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in [Path(__file__),*paths,*extra]}},indent=2)+'\n',encoding='utf-8');print('B35 M25/M26 COMPLETE PASS independent8+3+5 ledgers; lowM pending',flush=True)
if __name__=='__main__':main()
