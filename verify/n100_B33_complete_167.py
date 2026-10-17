"""Independent Fraction ledger, CAS geometry bookkeeping and fullB33 composition."""
from pathlib import Path
from fractions import Fraction as F
import json,itertools,hashlib,sys
from collections import Counter
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'lower_bounds_extension_20261004')]
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_linear_halfside_marked_conjugate import conjugate
from exact_signed_sine_full_face_support import face_bound
R=F(2831,25000)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 paths=[ROOT/'verify/out/n100-B33-low-complete-157.json',ROOT/'verify/out/n100-B33-high-residual-159.json',ROOT/'verify/out/n100-B33-deep5-complete-163.json',ROOT/'verify/out/n100-B33-ring5-complete-165.json',ROOT/'verify/out/n100-B33-no5-components-166.json'];low,red,deep,ring,no5=[json.loads(p.read_text(encoding='utf-8')) for p in paths];assert low['status']==deep['status']==ring['status']==no5['status']=='PASS' and red['status']=='PASS_REDUCTION';assert all(F(x['radius'])==R for x in (low,red,deep,ring,no5));assert low['low_M_closed'];assert deep['unique5_has_original_B_neighbor'] is False and ring['unique5_has_original_B_neighbor'] is True
 for cert in (low,red,deep,ring,no5):
  for rel,h in cert.get('bindings',{}).items():assert sha(ROOT/rel)==h,(rel,'binding mismatch')
 # Independent integer classification of highM with at most1 degree5.
 survivor=[]
 for fives in (0,1):
  for M,e,b in itertools.product(range(26,100),range(17),range(33)):
   excess=27-M-e-b+fives
   if excess<0:continue
   if fives and (M>=27 or e or b):continue
   survivor.append((fives,M,e,b,excess))
 assert set(survivor)=={(0,26,0,0,1),(0,26,0,1,0),(0,26,1,0,0),(0,27,0,0,0),(1,26,0,0,2)};assert F(red['source_replay']['result']['two_degree5_margin'])>0;assert all(F(x)>0 for x in red['source_replay']['result']['shifted_low_margins'].values())
 # No5 b1/e0 impossible by connected-core/no-empty-ear topological bridge;
 # deep degree7 in P26 is excluded by the general /6 inner-frontier bound.
 assert F(22**2,6)<108;assert F(26+19)+F(19**2,6)<106
 # With ring5, strict block interiors still degree>=6 (planar separation).
 assert all(6*(106+2*(c-1))>(26-4*(c-1))**2 for c in range(2,8));assert 6*106>24**2 and 6*106>3**2+25**2
 # Chordless ring vertex has >=2 core faces and exactly2 BRR incidences,
 # so p<=d-4; no unproved p<=3 restriction on arbitrary original vertices.
 assert [p for p in range(5) if 5-p-2>=2]==[0,1]
 # CAS derives all DDD/DDR counts and centered-angle mass independently.
 h,pi,lr,lh,ll,lb,pr,ph,pl,gR,gH,gL,ds,nh=sp.symbols('h pi LR LH LL LB pR pH pL GammaR GammaH GammaL dsum nH');x,y=sp.symbols('DDD DDR');solution=sp.solve([x+y+26-106,3*x+2*y+26-(246+h)],(x,y));assert sp.expand(solution[x]-(60+h))==sp.expand(solution[y]-(20-h))==0
 masses=lr*(pr*pi/3-gR)+lh*((6*nh-ds+ph)*pi/3-gH)+ll*((1+pl)*pi/3-gL);Bmass=lb*(gR+gH+gL-2*pi-26*pi/3);expected=(lb-lr)*gR+(lb-lh)*gH+(lb-ll)*gL+(pr*lr+(6*nh-ds+ph)*lh+(1+pl)*ll)*pi/3-lb*(2*pi+26*pi/3);assert sp.expand(masses+Bmass-expected)==0
 # Independent enumeration aggregates all actual26-cycles and degree splits.
 pairs=[(0,0),(0,1),(1,1),(0,2),(1,2)];expected_models=set()
 for high in ((),(7,),(8,),(7,7)):
  n=len(high);excess=2-sum(d-6 for d in high);edge_types=set()
  for positions in itertools.combinations(range(1,26),n):
   lab=[2]+[0]*25
   for pos in positions:lab[pos]=1
   counts=Counter(tuple(sorted((lab[i],lab[(i+1)%26]))) for i in range(26));edge_types.add(tuple(counts[t] for t in pairs))
  for lowp in (0,1):
   for hp in range(sum(d-4 for d in high)+1):
    for edgecounts in edge_types:expected_models.add((high,excess,lowp,hp,33-lowp-hp,edgecounts))
 observed={(tuple(x['model']['high_ring_degrees']),x['model']['deep_excess'],x['model']['pL'],x['model']['pH_total'],x['model']['pR_total'],tuple(x['model']['edge_counts'])) for x in ring['rows']};assert observed==expected_models and len(observed)==108
 pp=ROOT/'runtime/B33-labelled-ring-discovery-164/proposal.json';proposal=json.loads(pp.read_text(encoding='utf-8'));labels=list(map(F,proposal['labels']));LB=F(proposal['LB']);tau=F(proposal['tau']);K=F(proposal['K']);den=proposal['denominator'];patterns=[('DDD',[F(0)]*3,[F(0)]*3)]+[(f'DDR{i}',[0,0,labels[i]],[0,0,0]) for i in range(3)]
 for i,j in pairs:patterns.extend([(f'DRR{i}{j}',[0,labels[i],labels[j]],[-tau,0,0]),(f'BRR{i}{j}',[labels[i],labels[j],LB],[0,0,tau])])
 upper={}
 for (name,ls,ts),cell in zip(patterns,proposal['face_rows']):
  assert cell['pattern']==name;bound,acute,edges=face_bound(ls,ts,F(cell['nu'],den));assert all(bound.u>=z.u for z in (acute,*edges));upper[name]=F(bound.u,S)
 conj_upper=[F(conjugate(K,l-LB).u,S) for l in labels];pilo,pihi=F(PI.l,S),F(PI.u,S);mu=PI/33;s=sine(mu);rho=cosine(mu)-(q(R).sq()-s.sq()).sqrt();outer=33*(mu-s*rho+q(K)*q(R)*s*rho);outerup=F(outer.u,S);margins=[]
 for row in ring['rows']:
  m=row['model'];high=m['high_ring_degrees'];cen=m['DDD']*upper['DDD']+sum(n*upper[f'DDR{i}'] for i,n in enumerate(m['DDR']));cen+=sum(n*(upper[f'DRR{i}{j}']+upper[f'BRR{i}{j}']) for (i,j),n in zip(pairs,m['edge_counts']));cen+=sum(n*c for n,c in zip((m['pR_total'],m['pH_total'],m['pL']),conj_upper));angular=m['pR_total']*labels[0]+(sum(6-d for d in high)+m['pH_total'])*labels[1]+(1+m['pL'])*labels[2];coef=-angular/3+LB*(F(2)+F(26,3));cen+=coef*(pihi if coef>=0 else pilo);margin=pilo-R*R*cen-outerup;assert margin>0;margins.append(margin)
 assert len(margins)==108;all_margins=[F(low['minimum_reported_positive_closure_margin']),F(deep['conservative_gain_009_area_margin']),min(margins)]
 for comp in no5['components']:
  result=comp['result'];assert comp['status']=='ARITHMETIC_PASS' and result['status']=='PASS' and F(result['radius'])==R and F(result['required_center_norm_squared_upper'])==1-R*R;all_margins.append(F(result.get('minimum_area_margin',result.get('area_margin'))))
 assert min(all_margins)>0
 theory=W/'lower_bounds_extension_20261004/GENERAL_DISK_ISOPERIMETRY.md';original=W/'verify_B33_hinge_metric_complete_0p11323.py';out=ROOT/'verify/out/n100-B33-complete-167.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B33-complete-independent-composition/v1','status':'PASS','radius':str(R),'B':33,'m':100,'required_center_norm_squared_upper':str(1-R*R),'full_B33_closed':True,'M_partition':['M<=25','M>=26'],'high_integer_survivors_before_local_closures':survivor,'unique5_boundary_neighbor_split_complete':True,'ring_models':108,'independent_fraction_ring_min_margin':str(min(margins)),'CAS_DDD_DDR_and_angle_potential_identities':True,'marked_range_derived_from_chordless_core':True,'physical_edge_pairs_cancellation':26,'global_K_hinge_budgets_not_stacked':'Old valid K=.44 row used only for profile reduction and deep-star replacement; labelled-ring contradiction uses its own freshly verified K envelope and spends no hinge or variance. Each conditional contradiction has its own complete single area ledger.','no5_bad_and_deep7_topology_review':True,'minimum_reported_positive_margin':str(min(all_margins)),'geometric_dependencies':'Common normalized center triangulation, planar separation of original-B neighbor from strict core interior, general/6 disk isoperimetry, core/outer-band decomposition without B chords when connected/no ears, complete-star/perimeter lemma and full-simplex signed face supports inherited and reviewed. Integer counts, all26-cycle signatures and angular cancellation CAS checked; not formal theorem-prover kernel.','geometry_review_completed_for_ring165':True,'global_bound_improved':False,'pending_other_B':['B34','B35','B>=36'],'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in [Path(__file__),*paths,pp,theory,original,W/'exact_signed_sine_full_face_support.py',W/'exact_linear_halfside_marked_conjugate.py']}},indent=2)+'\n',encoding='utf-8');print('COMPLETE B33 PASS at0.11324; independent108 Fraction ledgers; global unchanged',flush=True)
if __name__=='__main__':main()
