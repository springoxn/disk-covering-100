"""Exact closure of B33 M26 unique5 without an original-B neighbor."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,itertools
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'lower_bounds_extension_20261004')]
from verify_star_lp_duals import q,S,PI
from exact_signed_sine_full_face_support import face_bound
from exact_range_one_face_support import face_bound as ordinary
from polygon_star_perimeter_support import support
R=F(2831,25000)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 pp=ROOT/'runtime/B33-deep5-coherent-discovery-162/proposal.json';cp=ROOT/'verify/out/n100-B33-high-residual-159.json';ref=W/'B33_highM_any_five_0p11323_proposal.json';proposal=json.loads(pp.read_text(encoding='utf-8'));reduction=json.loads(cp.read_text(encoding='utf-8'));assert proposal['reference_sha256']==sha(ref) and proposal['radius']==str(R) and reduction['status']=='PASS_REDUCTION';row=json.loads(ref.read_text(encoding='utf-8'))['row'];D=row['denominator'];PD=row['potential_denominator'];den=proposal['denominator'];rat=lambda x:F(x,den);labels=[F(row['high_potential'],PD),F(row['boundary_potential'],PD),F(0),F(row['low_potential'],PD)];charges=[F(row[k],D) for k in ('charge_a','charge_b','charge_0','charge_low')];interfaces=[F(row[k],D) for k in ('interface_a','interface_0','interface_low')];A=3*q(3).sqrt()/4;ANG=PI/3;eps=F(proposal['epsilon']);tau=F(proposal['tau']);weight=1-eps;assert 0<eps<1 and tau>0
 def credit(ids):return sum((t*sum({ids[j],ids[(j+1)%3]}=={typ,1} for j in range(3)) for typ,t in zip((0,2,3),interfaces)),F(0))
 def old(ids):return A+q(sum((charges[i] for i in ids),F(0))-credit(ids))
 faces=[]
 for cell in row['faces']:
  ids=cell['indices'];bound,_,_=ordinary([labels[i] for i in ids],F(cell['nu'],D));slack=old(ids).l-bound.u;assert slack>0;faces.append(F(slack,S))
 assert len(faces)==20;outside={1:[],2:[]};expected=[]
 for n in (1,2):
  values=itertools.product([0,2],[0,2],[0,1,2]) if n==1 else itertools.product([0,2],repeat=3)
  expected.extend((n,list(ids)) for ids in values if ids.count(0)<=2)
 assert [(x['selected_edges'],x['ids']) for x in proposal['outside_rows']]==expected
 for cell in proposal['outside_rows']:
  n=cell['selected_edges'];ids=cell['ids'];edges=[0,0,eps*tau] if n==1 else [eps*tau,0,eps*tau];bound,acute,caps=face_bound([labels[i] for i in ids],edges,rat(cell['nu']));assert len(caps)==3 and all(bound.u>=x.u for x in (acute,*caps));outside[n].append(F(bound.u-old(ids).l,S))
 D1,D2=max(outside[1]),max(outside[2]);J=max((5-2*j)*D1+j*D2 for j in range(3));patterns=[(0,[5,0,0]),(1,[3,2,0]),(2,[2,2,1]),(2,[1,4,0])];assert [(x['high_neighbors'],x['counts']) for x in proposal['stars']]==patterns
 # Enumerate all binary5 neighbour cycles with at most2 high vertices.
 signatures={(sum(bits),tuple(sum(bits[i]+bits[(i+1)%5]==h for i in range(5)) for h in range(3))) for bits in itertools.product((0,1),repeat=5) if sum(bits)<=2};assert signatures=={(k,tuple(c)) for k,c in patterns};poly=support(5,eps,-eps*tau);gains=[];cases=[];checks=0
 for st in proposal['stars']:
  k=st['high_neighbors'];counts=st['counts'];y=rat(st['center_potential']);cap=poly-q(y-labels[3])*ANG;assert [x['high_base_vertices'] for x in st['faces']]==[h for h in range(3) if counts[h]]
  for cell in st['faces']:
   h=cell['high_base_vertices'];ls=[y]+[labels[0]]*h+[F(0)]*(2-h);assert max(ls)-min(ls)<weight;bound,_,_=ordinary([x/weight for x in ls],rat(cell['nu']));cap+=counts[h]*q(weight)*bound;checks+=1
  previous=5*A+q(5*charges[3]+2*k*charges[0]+(10-2*k)*charges[2]);gain=F((previous-cap-q(J)).l,S);assert gain>F(9,100);gains.append(gain);cases.append({'high_neighbors':k,'counts':counts,'gain_lower':str(gain)})
 assert checks==8;baseline=F(reduction['source_replay']['result']['degree5_contradiction_margin']);gain=min(gains);final=baseline+R*R*gain;conservative=baseline+R*R*F(9,100);assert baseline<0 and min(final,conservative)>0
 out=ROOT/'verify/out/n100-B33-deep5-complete-163.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B33-deep5-residual-closure/v1','status':'PASS','radius':str(R),'B':33,'M':26,'unique5_has_original_B_neighbor':False,'high_degree_profiles':[[7,7],[8]],'all_high_marked_counts_inherited_from_original_vertex_bounds':True,'frozen_high_row_faces':20,'outside_supports':len(expected),'neighbor_cycle_types':4,'central_supports':checks,'epsilon':str(eps),'tau':str(tau),'outside_D1':str(D1),'outside_D2':str(D2),'outside_total_allowance':str(J),'minimum_gain_lower':str(gain),'baseline_margin':str(baseline),'final_area_margin_lower':str(final),'conservative_gain_009_area_margin':str(conservative),'minimum_face_slack':str(min(faces)),'cases':cases,'scope':'Unique deep5, no other positive-labelled site, at most2 high vertices; replace original5 central faces once, physical shared halfedge cancellation with outside faces; old global K=.44 and hinge=.03 untouched, all original interface charges retained','full_B33_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),pp,cp,ref)}},indent=2)+'\n',encoding='utf-8');print('B33 DEEP5 EXACT PASS gain>',F(9,100),'conservative final',conservative,flush=True)
if __name__=='__main__':main()
