"""Exact single-chord B34 supports and full integer model replay."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import ast,sys,json,itertools,hashlib
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'lower_bounds_extension_20261004')]
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_signed_sine_full_face_support import face_bound
from exact_linear_halfside_marked_conjugate import conjugate
import verify_exact_lens_boundary_0p11322 as boundary
R=F(2831,25000);PAIRS=[(0,0),(0,1),(1,1)]
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 pp=ROOT/'runtime/B34-onechord-labelled-discovery-178/proposal.json';tp=ROOT/'verify/out/n100-B34-high-topology-174.json';source=ROOT/'tools/n100_B34_onechord_labelled_discover.py';proposal=json.loads(pp.read_text(encoding='utf-8'));assert proposal['radius']==str(R);assert json.loads(tp.read_text(encoding='utf-8'))['status']=='PASS_REDUCTION'
 # Extract only integer model generator; no scipy/numeric discovery executed.
 tree=ast.parse(source.read_text(encoding='utf-8'));node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='models');env={'itertools':itertools,'Counter':Counter,'PAIRS':PAIRS};exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),env);models=env['models']();assert models==proposal['models'];labels=list(map(F,proposal['labels']));LB=F(proposal['LB']);tau=F(proposal['tau']);K=F(proposal['K']);den=proposal['denominator'];triples=sorted({tuple(m['RRR']) for m in models});patterns=[('DDD',[0,0,0],[0,0,0])]+[(f'DDR{i}',[0,0,labels[i]],[0,0,0]) for i in range(2)]
 for i,j in PAIRS:patterns.extend([(f'DRR{i}{j}',[0,labels[i],labels[j]],[-tau,0,0]),(f'BRR{i}{j}',[labels[i],labels[j],LB],[0,0,tau]),(f'BRR0{i}{j}',[labels[i],labels[j],LB],[0,0,0])])
 for ids in triples:patterns.append(('RRR'+''.join(map(str,ids)),[labels[i] for i in ids],[tau,0,0]))
 assert [x['pattern'] for x in proposal['face_rows']]==[x[0] for x in patterns];caps={};supports=[]
 for (name,ls,ts),row in zip(patterns,proposal['face_rows']):
  guard=1-(max(ls)-min(ls)+sum((max(-t,F(0)) for t in ts),F(0))/2);assert guard>0;cap,acute,edges=face_bound(ls,ts,F(row['nu'],den));assert all(cap.u>=x.u for x in (acute,*edges));caps[name]=cap;supports.append({'pattern':name,'guard':str(guard),'upper':str(F(cap.u,S))})
 bs=Path(boundary.__file__).read_text(encoding='utf-8');assert bs.count('count=1000;')==1;exec(compile(bs.replace('count=1000;','count=10000;'),str(boundary.__file__),'exec'),boundary.__dict__);boundary.R=R;boundary.B=34;boundary.K=K;boundary.CURVATURE=F(0);envelope=boundary.verify();assert envelope['status']=='PASS' and F(envelope['required_center_norm_squared_upper'])==1-R*R
 mu=PI/34;s=sine(mu);rho=cosine(mu)-(q(R).sq()-s.sq()).sqrt();outer=34*(mu-s*rho+q(K)*q(R)*s*rho);conjs=[conjugate(K,v-LB) for v in labels];rows=[]
 for m in models:
  assert sum(m['DDR'])==19 and min(m['DDR'])>=0;assert sum(m['DRR'])==25 and sum(m['BRR'])==24 and sum(m['BRR0'])==2;assert m['pR']+m['pH']==34 and sum(d-6 for d in m['high_ring_degrees'])==2
  assert 59+19+25+1==104 and 3*59+2*19+25==240;assert 19+2*25+3==124
  # Edge incidence identities ensure one chord edge against theRRR face,
  # and24 original ring edges between DRR and BRR, not26 paired outer edges.
  rr=m['RRR'];chord=tuple(sorted(rr[1:]));assert all(m['DRR'][i]-m['BRR'][i]==int(pair==chord) for i,pair in enumerate(PAIRS));assert m['ear_high']==rr[0]
  center=59*caps['DDD']+sum((n*caps[f'DDR{i}'] for i,n in enumerate(m['DDR'])),q(0))
  for region in ('DRR','BRR','BRR0'):center+=sum((n*caps[f'{region}{i}{j}'] for (i,j),n in zip(PAIRS,m[region])),q(0))
  center+=caps['RRR'+''.join(map(str,rr))];center+=m['pR']*conjs[0]+m['pH']*conjs[1];center-=q(m['pR']*labels[0]+(m['pH']-2)*labels[1])*PI/3;center+=q(LB)*(2*PI+26*PI/3);margin=PI-q(R).sq()*center-outer;assert margin.l>0;rows.append({'model':m,'area_margin':str(F(margin.l,S))})
 out=ROOT/'verify/out/n100-B34-onechord-complete-179.json';assert not out.exists();minimum=min(F(x['area_margin']) for x in rows);out.write_text(json.dumps({'schema':'B34-onechord-exact/v1','status':'PASS','radius':str(R),'B':34,'chords':1,'core_faces':104,'core_boundary':26,'deep_excess':0,'models':len(models),'face_supports':len(caps),'supports':supports,'labels':list(map(str,labels)),'LB':str(LB),'tau':str(tau),'K':str(K),'boundary_envelope':envelope,'minimum_area_margin':str(minimum),'rows':rows,'shared_edge_pairs':{'DRR_BRR':24,'DRR_RRR_chord':1},'unpaired_BRR':2,'hinge_payment':0,'variance_payment':0,'geometry_review_pending':True,'full_B34_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),pp,tp,source)}},indent=2)+'\n',encoding='utf-8');print('B34 ONECHORD EXACT PASS',len(models),'margin',minimum,flush=True)
if __name__=='__main__':main()
