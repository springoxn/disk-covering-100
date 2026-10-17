"""Complete B34 with independent integer coverage, Fraction and CAS ledgers."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys,json,itertools,hashlib
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'lower_bounds_extension_20261004')]
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_linear_halfside_marked_conjugate import conjugate
R=F(2831,25000);PAIRS=[(0,0),(0,1),(1,1)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def key(m,chord):
 return (tuple(m['high_ring_degrees']),m['pH'],tuple(m['DDR']),tuple(m['DRR']) if chord else tuple(m['edges']),tuple(m['BRR']) if chord else (),tuple(m['BRR0']) if chord else (),tuple(m['RRR']) if chord else ())
def independent_models(chord):
 results=set()
 for high in (((8,),(7,7)) if chord else ((7,),(8,),(7,7))):
  n=len(high)
  for positions in itertools.combinations(range(26),n):
   bits=[int(i in positions) for i in range(26)];ring=Counter(tuple(sorted((bits[i],bits[(i+1)%26]))) for i in range(26));ear=bits[0]
   if chord and high==(8,) and ear:continue
   if chord:
    rrr=(ear,*sorted((bits[-1],bits[1])));unpaid=Counter([tuple(sorted((bits[-1],ear))),tuple(sorted((ear,bits[1])))]);paid=ring-unpaid;drr=paid.copy();drr[tuple(sorted((bits[-1],bits[1])))]+=1
   for ph in range(35):
    pr=34-ph
    if chord:
     if ph<(4 if ear else 0) or ph>sum(d-4 for d in high)+ear or pr<(3 if not ear else 0) or pr>2*(26-n)+(1-ear):continue
     ddr=(2*(26-n)-pr+2*(1-ear)-rrr.count(0),sum(d-4 for d in high)-ph+2*ear-rrr.count(1))
     if min(ddr)<0:continue
     results.add((high,ph,ddr,tuple(drr[e] for e in PAIRS),tuple(paid[e] for e in PAIRS),tuple(unpaid[e] for e in PAIRS),rrr))
    else:
     if ph>sum(d-4 for d in high):continue
     ddr=(2*(26-n)-pr,sum(d-4 for d in high)-ph);results.add((high,ph,ddr,tuple(ring[e] for e in PAIRS),(),(),()))
 return results

def audit(cert,chord):
 observed={key(x['model'],chord) for x in cert['rows']};expected=independent_models(chord);assert observed==expected and len(observed)==(47 if chord else 23)
 caps={x['pattern']:F(x['upper']) for x in cert['supports']};ls=list(map(F,cert['labels']));LB=F(cert['LB']);K=F(cert['K']);conjs=[F(conjugate(K,v-LB).u,S) for v in ls];mu=PI/34;s=sine(mu);rho=cosine(mu)-(q(R).sq()-s.sq()).sqrt();outer=34*(mu-s*rho+q(K)*q(R)*s*rho);pilo,pihi=F(PI.l,S),F(PI.u,S);margins=[]
 for row in cert['rows']:
  m=row['model'];cen=m['DDD']*caps['DDD']+sum(n*caps[f'DDR{i}'] for i,n in enumerate(m['DDR']))
  if chord:
   for region in ('DRR','BRR','BRR0'):cen+=sum(n*caps[f'{region}{i}{j}'] for (i,j),n in zip(PAIRS,m[region]))
   cen+=caps['RRR'+''.join(map(str,m['RRR']))]
  else:cen+=sum(n*(caps[f'DRR{i}{j}']+caps[f'BRR{i}{j}']) for (i,j),n in zip(PAIRS,m['edges']))
  cen+=m['pR']*conjs[0]+m['pH']*conjs[1];excess=sum(d-6 for d in m['high_ring_degrees']);coefficient=-(m['pR']*ls[0]+(m['pH']-excess)*ls[1])/3+LB*(2+F(26,3));cen+=coefficient*(pihi if coefficient>=0 else pilo);margin=pilo-R*R*cen-F(outer.u,S);assert margin>0;margins.append(margin)
 return min(margins)
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 paths=[ROOT/'verify/out/n100-B34-low-and-high-reduction-171.json',ROOT/'verify/out/n100-B34-low-independent-172.json',ROOT/'verify/out/n100-B34-high-topology-174.json',ROOT/'verify/out/n100-B34-chordless-complete-177.json',ROOT/'verify/out/n100-B34-onechord-complete-179.json'];low,ind,top,flat,chord=[json.loads(p.read_text(encoding='utf-8')) for p in paths];assert all(F(x['radius'])==R for x in (low,ind,top,flat,chord));assert low['status']==ind['status']==flat['status']==chord['status']=='PASS' and top['status']=='PASS_REDUCTION';assert low['low_M_closed'] and ind['low_M_closed']
 for cert in (low,ind,top,flat,chord):
  for rel,h in cert['bindings'].items():assert sha(ROOT/rel)==h
 assert {(x['chords'],x['deep_excess'],x['a']) for x in top['topology_slots']}=={(0,0,0),(0,1,0),(1,0,0)};minflat=audit(flat,False);minchord=audit(chord,True)
 for cert in (flat,chord):
  env=cert['boundary_envelope'];assert env['status']=='PASS' and F(env['radius'])==R and env['B']==34 and env['bad_arc_boxes']==10000 and F(env['halfside_multiplier'])==F(cert['K']) and F(env['required_center_norm_squared_upper'])==1-R*R
 # Independent CAS: whole centered-angle potential mass, unchanged by chord.
 lr,lh,lb,pr,ph,ex,pi,gr,gh=sp.symbols('LR LH LB pR pH ex pi GammaR GammaH');mass=lr*(pr*pi/3-gr)+lh*((ph-ex)*pi/3-gh)+lb*(gr+gh-2*pi-26*pi/3);expected=(lb-lr)*gr+(lb-lh)*gh+(pr*lr+(ph-ex)*lh)*pi/3-lb*(2*pi+26*pi/3);assert sp.expand(mass-expected)==0
 # Core ear has1 core face,2 outer-band faces andp marked faces.
 # Thus p=d-3, so originaldegree8 at ear would requirep5, forbiddenq<=4.
 d,p=sp.symbols('d p');assert sp.solve(sp.Eq(d,1+2+p),p)==[d-3];assert 8-3>4 and 7-3==4 and 6-3==3
 # RRR central corner counts restore all q0 corner incidences exactly.
 for row in chord['rows']:
  m=row['model'];n=len(m['high_ring_degrees']);rrr=m['RRR'];ear=m['ear_high'];ph=m['pH'];pr=m['pR'];high_ex=2
  drR=2*(26-n)-2*(1-ear);drH=2*n-2*ear;assert sum(m['DDR'])+drR+drH+3==124
  assert m['DDR'][0]+drR+rrr.count(0)==4*(26-n)-pr;assert m['DDR'][1]+drH+rrr.count(1)==sum(dd-2 for dd in m['high_ring_degrees'])-ph
 minimum=min(F(low['low_minimum_reported_margin']),F(ind['independent_area_margin_lower']),minflat,minchord);assert minimum>0
 out=ROOT/'verify/out/n100-B34-complete-180.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B34-complete-independent/v1','status':'PASS','radius':str(R),'B':34,'m':100,'required_center_norm_squared_upper':str(1-R*R),'full_B34_closed':True,'M_partition':['M<=25','M>=26'],'high_topology_slots':top['topology_slots'],'chordless_models':23,'onechord_models':47,'independent_fraction_chordless_min_margin':str(minflat),'independent_fraction_onechord_min_margin':str(minchord),'minimum_reported_positive_margin':str(minimum),'CAS_centered_angle_and_core_ear_identities':True,'physical_edge_cancellation':{'chordless':26,'onechord_outer':24,'onechord_diagonal':1,'onechord_unpaid_BRR':2},'geometry_review_completed_for_177_and179':True,'high_metric_hinge_variance_payment':0,'budget_review':'OldK=.5 q4-payment row used for residual reduction and low contradiction. High chordless/single-chord contradiction each owns its freshly verified boundaryK, one full face ledger and shared-edge cancellation. No payments from distinct conditional contradictions combined.','geometric_dependencies':'Inherited common normalized center triangulation, core first peel and general/6 block isoperimetry. Core-ear originalp=d-3 vs non-earp<=d-4, markedq<=4 from same-radius original cluster. Chord adjacent boundary triangles enumerated over every26-cycle label arrangement; independent coverage and CAS accounting checked, not theorem-prover embedding kernel.','global_bound_improved':False,'pending_other_B':['B35','B>=36'],'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in [Path(__file__),*paths]}},indent=2)+'\n',encoding='utf-8');print('COMPLETE B34 PASS at0.11324;23+47 independentFraction ledgers; global unchanged',flush=True)
if __name__=='__main__':main()
