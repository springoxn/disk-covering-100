"""Exact B35 M25 residual metric: all25-cycle signatures,9 face supports."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys,json,itertools,hashlib
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'lower_bounds_extension_20261004')]
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_signed_sine_full_face_support import face_bound
from exact_linear_halfside_marked_conjugate import conjugate
import verify_exact_lens_boundary_0p11322 as boundary
R=F(2831,25000);PAIRS=[(0,0),(0,1),(1,1)]
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 pp=ROOT/'runtime/B35-M25-labelled-discovery-192/proposal.json';tp=ROOT/'verify/out/n100-B35-profile-reduction-191.json';proposal=json.loads(pp.read_text(encoding='utf-8'));top=json.loads(tp.read_text(encoding='utf-8'));assert top['status']=='PASS_REDUCTION' and proposal['radius']==str(R);signatures=set();models=[]
 for positions in itertools.combinations(range(25),4):
  lab=[int(i in positions) for i in range(25)];counts=Counter(tuple(sorted((lab[i],lab[(i+1)%25]))) for i in range(25));signatures.add(tuple(counts[p] for p in PAIRS))
 for ph in (11,12):
  for edges in sorted(signatures):models.append({'high_ring_degrees':[7]*4,'deep_excess':0,'pH':ph,'pR':35-ph,'DDD':59,'DDR':[7+ph,12-ph],'edges':list(edges)})
 assert models==proposal['models'] and len(models)==8;labels=list(map(F,proposal['labels']));LB=F(proposal['LB']);tau=F(proposal['tau']);K=F(proposal['K']);den=proposal['denominator'];patterns=[('DDD',[0,0,0],[0,0,0])]+[(f'DDR{i}',[0,0,labels[i]],[0,0,0]) for i in range(2)]
 for i,j in PAIRS:patterns.extend([(f'DRR{i}{j}',[0,labels[i],labels[j]],[-tau,0,0]),(f'BRR{i}{j}',[labels[i],labels[j],LB],[0,0,tau])])
 assert [x['pattern'] for x in proposal['face_rows']]==[x[0] for x in patterns];caps={};supports=[]
 for (name,ls,ts),cell in zip(patterns,proposal['face_rows']):
  guard=1-(max(ls)-min(ls)+sum((max(-t,F(0)) for t in ts),F(0))/2);assert guard>0;bound,acute,edges=face_bound(ls,ts,F(cell['nu'],den));assert all(bound.u>=x.u for x in (acute,*edges));caps[name]=bound;supports.append({'pattern':name,'guard':str(guard),'upper':str(F(bound.u,S))})
 boundary.R=R;boundary.B=35;boundary.K=K;boundary.CURVATURE=F(0);env=boundary.verify();assert env['status']=='PASS' and F(env['required_center_norm_squared_upper'])==1-R*R
 mu=PI/35;s=sine(mu);rho=cosine(mu)-(q(R).sq()-s.sq()).sqrt();outer=35*(mu-s*rho+q(K)*q(R)*s*rho);conjs=[conjugate(K,v-LB) for v in labels];rows=[]
 for m in models:
  assert m['pH']+m['pR']==35 and sum(m['DDR'])==19;assert 59+19+25==103 and 3*59+2*19+25==240;assert sum(m['edges'])==25 and m['edges'][1]+2*m['edges'][2]==8
  center=59*caps['DDD']+sum((n*caps[f'DDR{i}'] for i,n in enumerate(m['DDR'])),q(0));center+=sum((n*(caps[f'DRR{i}{j}']+caps[f'BRR{i}{j}']) for (i,j),n in zip(PAIRS,m['edges'])),q(0));center+=m['pR']*conjs[0]+m['pH']*conjs[1];center-=q(m['pR']*labels[0]+(m['pH']-4)*labels[1])*PI/3;center+=q(LB)*(2*PI+25*PI/3);margin=PI-q(R).sq()*center-outer;assert margin.l>0;rows.append({'model':m,'area_margin':str(F(margin.l,S))})
 out=ROOT/'verify/out/n100-B35-M25-metric-193.json';assert not out.exists();minimum=min(F(x['area_margin']) for x in rows);out.write_text(json.dumps({'schema':'B35-M25-labelled-exact/v1','status':'PASS','radius':str(R),'B':35,'M':25,'core_faces':103,'core_boundary':25,'deep_vertices':40,'models':8,'face_supports':9,'supports':supports,'K':str(K),'labels':list(map(str,labels)),'LB':str(LB),'tau':str(tau),'boundary_envelope':env,'minimum_area_margin':str(minimum),'rows':rows,'physical_edge_pairs':25,'hinge_payment':0,'variance_payment':0,'M25_residual_closed':True,'full_B35_closed':False,'global_bound_improved':False,'scope':'Conditional metric for the two residual profiles in reduction191: four ring7 with pH11 or12, simple chordlessP25/F103 and40 strictdegree6. Does not exclude lowM orM26.','bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),pp,tp,ROOT/'tools/n100_B35_M25_labelled_discover_192.py',ROOT/'tools/n100_B34_chordless_labelled_discover.py')}},indent=2)+'\n',encoding='utf-8');print('B35 M25 METRIC PASS8 margin',minimum,flush=True)
if __name__=='__main__':main()
