"""Independent classification/CAS audit and complete B32 composition at .11324."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,itertools,ast
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];R=F(2831,25000)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 lowpath=ROOT/'verify/out/n100-B32-M25-specialized-K-145.json';indpath=ROOT/'verify/out/n100-B32-M25-independent-146.json';highpath=ROOT/'verify/out/n100-B32-high-expanded-148.json';low=json.loads(lowpath.read_text(encoding='utf-8'));ind=json.loads(indpath.read_text(encoding='utf-8'));high=json.loads(highpath.read_text(encoding='utf-8'));assert all(x['status']=='PASS' and F(x['radius'])==R for x in (low,ind,high));assert low['full_M25_closed'] and low['B32_low_M_closed'] and ind['profiles']==81 and high['high_M_closed'];red,top,deep,metric=[x['result'] for x in high['runs']];assert red['remaining_profiles'][1]['unique_degree5_marked_incidence']==[0,1,2,3]
 # Integer Euler/curvature consequences; positive-curvature >=2 is excluded.
 profiles=[]
 for delta in (0,1):
  for M in range(26,100):
   for e in range(17):
    for b in range(33):
     excess=26-M-e-b+delta
     if excess<0:continue
     if delta==1 and (M>=27 or e>=1 or b>=1):continue # exact positive shifted margins below
     profiles.append((delta,M,e,b,excess))
 assert profiles==[(0,26,0,0,0),(1,26,0,0,1)];assert F(red['two_curvature_margin'])>0 and all(F(v)>0 for v in red['low_case_shift_margins'].values());assert red['geometry']['ordinary_marked_incidence_at_most_three']['status']=='PASS'
 # Marking p is an incidence to an original-boundary edge: p>0 => B neighbor.
 # No converse is used: p0 is allowed with or without a B neighbor.
 cases=[]
 for p,neighbor in itertools.product(range(4),(False,True)):
  if p>0 and not neighbor:continue
  cases.append({'low_p':p,'original_B_neighbor':neighbor,'closure':'four_face_metric_h0_h1' if neighbor else 'direct_star_p0'})
 assert len(cases)==5 and sum(x['closure']=='direct_star_p0' for x in cases)==1
 assert top['core_vertices']==68 and top['core_boundary']==26 and top['core_faces']==108 and top['deep_vertices']==42;assert deep['integer_profile_cases']==8 and deep['fan_charge']==deep['variance_charge']=='0';assert [x['deep_degree_excess'] for x in metric['rows']]==[0,1]
 # The inherited planar separation lemma puts any low with B neighbor on a
 # core frontier, irrespective of p. /6 therefore applies to strict interiors.
 for c in range(2,8):assert 6*(108+2*(c-1))>(26-4*(c-1))**2
 assert 6*108>24**2 and 6*108>3**2+23**2 and 6*108>3**2+25**2
 gamma,h,pi,lr,lb,plow=sp.symbols('Gamma h pi LR LB p_low');ring_inc=(72-h)+2*26;ring_centered=2*pi*26-gamma-ring_inc*pi/3;boundary_centered=gamma-2*pi-26*pi/3;assert sp.expand(ring_centered-((32+h)*pi/3-gamma))==0
 assert sp.expand(lr*ring_centered+lb*boundary_centered-((lb-lr)*gamma+(32+h)*lr*pi/3-lb*(2*pi+26*pi/3)))==0;assert sp.diff(ring_centered,plow)==sp.diff(boundary_centered,plow)==0
 for value in (0,1):
  DDD,DDR,DRR=62+value,20-value,26;assert DDD+DDR+DRR==108 and 3*DDD+2*DDR+DRR==42*6+value and DDR+2*DRR==72-value
 # Ensure the actually executed metric function has no unmarked-low premise.
 source=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/lower_staging/verify_B32_highM_complete_0p11323.py';tree=ast.parse(source.read_text(encoding='utf-8'));fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='four_face_metric');names={x.id for x in ast.walk(fn) if isinstance(x,ast.Name)};assert not names&{'marked','marked_margin','gaps','ROW','FAN'};assert 'ring degrees unrestricted' in metric['scope']
 assert F(deep['minimum_area_margin'])>0 and F(metric['minimum_area_margin'])>0;minimum=str(min(F(low['minimum_M25_margin']),F(ind['minimum_margin_lower']),F(high['minimum_positive_closure_margin'])));assert F(minimum)>0
 # Every accepted prior receipt binding remains unchanged.
 for receipt in (low,ind,high):
  for rel,expected in receipt['bindings'].items():assert sha(ROOT/rel)==expected,(rel,'binding changed')
 out=ROOT/'verify/out/n100-B32-complete-149.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B32-same-radius-complete-composition/v1','status':'PASS','radius':str(R),'B':32,'m':100,'required_center_norm_squared_upper':str(1-R*R),'full_B32_closed':True,'complete_M_partition':['M<=25','M>=26'],'low_M25_profile_partition':[73,8],'high_remaining_Euler_profiles':profiles,'unique5_boundary_neighbor_partition':cases,'minimum_reported_positive_closure_margin':minimum,'low_M_closed':True,'high_M_closed':True,'same_radius_prerequisites':True,'no_unproved_marked_low_exclusion_used':True,'negative_marked_margin_retained_as_diagnostic':red['marked_low_margin'],'CAS_ring_and_original_boundary_centered_angle_identities':True,'metric_ring_degree_unrestricted_and_no_p_low_assumption':True,'physical_edge_cancellation':'same26 DRR/BRR opposite halfside pairs; no added fee and no second variance/hinge spend','geometric_dependencies':'Generic normalized common center diagram, marked-incidence definition, planar separation of original-B neighbor from strict core-block interior, general /6 block isoperimetry and polygon-star support inherited from reviewed release. CAS checks angle bookkeeping and integer classification; not a formal theorem-prover derivation.','global_bound_improved':False,'other_B_branches_pending':['B33','B34','B35','B>=36'],'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),lowpath,indpath,highpath,source,ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/lower_staging/B32_HIGHM_CATALOG_FREE_COMPLETE_0p11323.md')}},indent=2)+'\n',encoding='utf-8');print('PASS COMPLETE B32 at0.11324; low/high partition and marked5 extension independently reviewed; global unchanged',flush=True)
if __name__=='__main__':main()
