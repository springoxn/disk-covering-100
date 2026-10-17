"""Exact labelled-ring closure for B33 unique5 with original-B neighbor.
Original ring degrees5/6/7/8 distinguished; core deep excess0/1/2.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import itertools,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'lower_bounds_extension_20261004')]
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_signed_sine_full_face_support import face_bound
from exact_linear_halfside_marked_conjugate import conjugate
import verify_exact_lens_boundary_0p11322 as boundary
R=F(2831,25000);PAIRS=[(0,0),(0,1),(1,1),(0,2),(1,2)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def models():
 rows=[]
 for high in ((),(7,),(8,),(7,7)):
  n=len(high);h=2-sum(d-6 for d in high);cycles=set()
  for positions in itertools.combinations(range(1,26),n):
   lab=[0]*26;lab[0]=2
   for j in positions:lab[j]=1
   edges=Counter(tuple(sorted((lab[j],lab[(j+1)%26]))) for j in range(26));cycles.add(tuple(edges[x] for x in PAIRS))
  for pl in (0,1):
   for ph in range(sum(d-4 for d in high)+1):
    pr=33-pl-ph;ddr=[2*(25-n)-pr,sum(d-4 for d in high)-ph,1-pl]
    for edges in sorted(cycles):rows.append({'high_ring_degrees':list(high),'deep_excess':h,'pL':pl,'pH_total':ph,'pR_total':pr,'DDD':60+h,'DDR':ddr,'edge_counts':list(edges)})
 return rows
def main():
 pp=ROOT/'runtime/B33-labelled-ring-discovery-164/proposal.json';cp=ROOT/'verify/out/n100-B33-high-residual-159.json';proposal=json.loads(pp.read_text(encoding='utf-8'));reduction=json.loads(cp.read_text(encoding='utf-8'));assert proposal['radius']==str(R) and reduction['status']=='PASS_REDUCTION';expected=models();assert proposal['models']==expected and len(expected)==108;labels=list(map(F,proposal['labels']));LB=F(proposal['LB']);tau=F(proposal['tau']);K=F(proposal['K']);den=proposal['denominator'];assert 0<K<1 and tau>0 and len(labels)==3
 boundary.R=R;boundary.B=33;boundary.K=K;boundary.CURVATURE=F(0);envelope=boundary.verify();assert envelope['status']=='PASS' and F(envelope['radius'])==R and F(envelope['halfside_multiplier'])==K and F(envelope['required_center_norm_squared_upper'])==1-R*R
 # Core: unique5 cannot be strict-interior because it has an original-B edge.
 # Every remaining strict-interior vertex degree>=6. /6 rules out components,
 # bridges and chords with positive integer margins, including chord gap2.
 assert all(6*(106+2*(c-1))>(26-4*(c-1))**2 for c in range(2,8));assert 6*106>24**2 and 6*106>3**2+23**2 and 6*106>3**2+25**2
 patterns=[('DDD',[F(0)]*3,[F(0)]*3)]+[(f'DDR{i}',[F(0),F(0),labels[i]],[F(0)]*3) for i in range(3)]
 for i,j in PAIRS:patterns.extend([(f'DRR{i}{j}',[F(0),labels[i],labels[j]],[-tau,0,0]),(f'BRR{i}{j}',[labels[i],labels[j],LB],[0,0,tau])])
 assert [r['pattern'] for r in proposal['face_rows']]==[r[0] for r in patterns];caps={};supports=[]
 for (name,ls,edges),row in zip(patterns,proposal['face_rows']):
  guard=1-(max(ls)-min(ls)+sum((max(-x,F(0)) for x in edges),F(0))/2);assert guard>0;cap,acute,boundaries=face_bound(ls,edges,F(row['nu'],den));assert len(boundaries)==3 and all(cap.u>=z.u for z in (acute,*boundaries));caps[name]=cap;supports.append({'pattern':name,'guard':str(guard),'upper':str(F(cap.u,S))})
 assert len(caps)==14;mu=PI/33;s=sine(mu);rho=cosine(mu)-(q(R).sq()-s.sq()).sqrt();outer=33*(mu-s*rho+q(K)*q(R)*s*rho);conjs=[conjugate(K,v-LB) for v in labels];rows=[]
 for m in expected:
  high=m['high_ring_degrees'];n=len(high);h=m['deep_excess'];pl,ph,pr=m['pL'],m['pH_total'],m['pR_total'];ddr=m['DDR'];edges=m['edge_counts'];assert min(ddr)>=0 and sum(ddr)==20-h and sum(edges)==26;assert pl+ph+pr==33 and pl<=5-4 and ph<=sum(d-4 for d in high) and 0<=pr<=2*(25-n);assert edges[3]+edges[4]==2 and edges[1]+2*edges[2]+edges[4]==2*n
  assert m['DDD']+sum(ddr)+26==106 and 3*m['DDD']+2*sum(ddr)+26==41*6+h
  # All q0 ring corner incidences, regrouped from individual original degrees.
  assert (25-n)*6+sum(high)+5-pr-ph-pl==sum(ddr)+104==124-h
  center=m['DDD']*caps['DDD']+sum((count*caps[f'DDR{i}'] for i,count in enumerate(ddr)),q(0));center+=sum((count*(caps[f'DRR{i}{j}']+caps[f'BRR{i}{j}']) for (i,j),count in zip(PAIRS,edges)),q(0));center+=pr*conjs[0]+ph*conjs[1]+pl*conjs[2]
  centered=pr*labels[0]+(sum(6-d for d in high)+ph)*labels[1]+(1+pl)*labels[2];center-=q(centered)*(PI/3);center+=q(LB)*(2*PI+26*PI/3);margin=PI-q(R).sq()*center-outer;assert margin.l>0,('ring',m,F(margin.l,S));rows.append({'model':m,'area_margin_lower':str(F(margin.l,S))})
 out=ROOT/'verify/out/n100-B33-ring5-complete-165.json';assert not out.exists();minimum=min(F(x['area_margin_lower']) for x in rows);out.write_text(json.dumps({'schema':'n100-B33-ring5-labelled-exact/v1','status':'PASS','radius':str(R),'B':33,'M':26,'unique5_has_original_B_neighbor':True,'core_vertices':67,'core_faces':106,'core_boundary':26,'deep_vertices':41,'deep_excess':[0,1,2],'ring_degree_unrestricted_except_original5_6_7_8':True,'low_marked_range':[0,1],'low_marked_range_reason':'Chordless core ring vertex has at least one deep neighbor and at least2 core faces. Original degree d has2 BRR faces and p marked faces, hence core faces=d-p-2>=2; p<=d-4. For d5 this is p<=1.','models':108,'face_supports':14,'face_support_rows':supports,'labels':list(map(str,labels)),'LB':str(LB),'tau':str(tau),'K':str(K),'boundary_envelope':envelope,'required_center_norm_squared_upper':str(1-R*R),'shared_physical_edge_pairs':26,'hinge_payment':0,'variance_payment':0,'minimum_area_margin':str(minimum),'rows':rows,'scope':'Unique original5 on simple chordless core ring, all other original interior degrees>=6, high curvature2 split between ring and deep; every actual26-cycle arrangement maps to an enumerated signature, all admissible marked totals covered. Opposite DRR/BRR terms cancel on each unchanged edge; no hinge/variance/old-face charge added.','geometry_review_pending':True,'full_B33_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),pp,cp)}},indent=2)+'\n',encoding='utf-8');print('B33 RING5 EXACT PASS108 margin',minimum,flush=True)
if __name__=='__main__':main()
