"""Real-box retention and declared-map contractor composition checks."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
import n100_continuous_proof_interfaces as I
R=Path(__file__).resolve().parents[1]
def make(boxes,constraints,limit=3):
 ctx={'semantics_id':'scaled-real-map-boxes/v1','scale':I.Q,'map_id':'test-declared-system','frame_id':'fixed-test-frame','parent_box_id':'test-parent','radius_domain_id':'declared-squared-bounds'}
 for c in constraints:c['map_id']=ctx['map_id']
 return {'context':ctx,'boxes':boxes,'constraints':constraints,'sweep_limit':limit}
def bound(x):return [x.numerator//x.denominator,-((-x.numerator)//x.denominator)]
def main():
 examples=[];controls=[];retained=0
 for r2,expected in [(25,'NOT_EXCLUDED'),(24,'EXCLUDED')]:
  p=make([[0,0,0,0],[3,3,4,4]],[{'op':'distance_le','v':0,'b':1,'radius2':r2}]);r=I.run(p);assert r['status']==expected;examples.append(r)
 for j in range(1,7):
  t=F(j,7);x=I.Q*(1-t*t)/(1+t*t);y=I.Q*2*t/(1+t*t);p=make([bound(x)+bound(y)],[{'op':'circle_eq','v':0,'signs':[1,1]}]);r=I.run(p);assert r['status']=='NOT_EXCLUDED';b=r['boxes'][0];assert b[0]<=x<=b[1] and b[2]<=y<=b[3];retained+=1
 for j in range(-12,13):
  y=F(j,7);p=make([[-3,4]+bound(y),[-2,-2,0,0],[2,2,0,0]],[{'op':'bisector_eq','v':0,'a':1,'b':2}]);r=I.run(p);assert r['status']=='NOT_EXCLUDED';b=r['boxes'][0];assert b[0]<=0<=b[1] and b[2]<=y<=b[3];retained+=1
 p=make([[1,2,0,0],[-2,-2,0,0],[2,2,0,0]],[{'op':'nearest_le','v':0,'a':1,'b':2}]);assert I.run(p)['status']=='EXCLUDED';p=make([[0,0,0,0]],[{'op':'norm_range','v':0,'lower2':'1','upper2':'2'}]);assert I.run(p)['status']=='EXCLUDED'
 # A one-sweep contraction is unresolved, even though its box is nonempty.
 parent=[[-3,4,-2,5],[-2,-2,0,0],[2,2,0,0]];eq=make(copy.deepcopy(parent),[{'op':'bisector_eq','v':0,'a':1,'b':2}],1);near=make(copy.deepcopy(parent),[{'op':'nearest_le','v':0,'a':1,'b':2}],1);a,b=I.run(eq),I.run(near);assert a['status']=='UNDECIDED';joint=I.intersect_results([a,b]);assert joint['status']=='NOT_EXCLUDED' and joint['boxes'][0][:2]==[0,0]
 for label,change in [('wrong_map',lambda p:p['constraints'][0].update(map_id='other-map')),('wrong_scale',lambda p:p['context'].update(scale=1)),('missing_radius_domain',lambda p:p['context'].pop('radius_domain_id')),('float_coordinate',lambda p:p['boxes'][0].__setitem__(0,-3.0)),('invalid_variable',lambda p:p['constraints'][0].update(v=999)),('zero_budget',lambda p:p.update(sweep_limit=0))]:
  bad=copy.deepcopy(eq);change(bad);assert I.run(bad)['status']=='PRECONDITION_MISSING';controls.append(label)
 other=copy.deepcopy(near);other['context']['frame_id']='different-frame';different=I.run(other)
 try:I.intersect_results([a,different])
 except ValueError:controls.append('cross_frame_composition')
 else:raise AssertionError('cross frame')
 bad=copy.deepcopy(a);bad['status']='EXCLUDED'
 try:I.intersect_results([bad])
 except ValueError:controls.append('forged_contractor_exclusion')
 else:raise AssertionError('forged output')
 # Actual fixed-core compilation, including all nearest-owner relations.
 payload,bridge=I.compile_fixed_core([30,6,14,22],nearest_all=True,sweep_limit=1);actual=I.run(payload);assert actual['status'] in ('NOT_EXCLUDED','UNDECIDED');assert not actual['covering_exclusion_authorized_without_bridge'];summary={k:v for k,v in actual.items() if k not in ('proof_input','boxes')};summary['initial_box_count']=len(payload['boxes']);summary['constraint_count']=len(payload['constraints']);summary['input_sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
 out=R/'verify/out/n100-continuous-proof-interface-contracts.json';assert not out.exists();paths=[R/'verify/n100_continuous_proof_interfaces.py',R/'verify/n100_axis_coupled_boxes.py',R/'verify/n100_axis_coupled_boxes_independent.py',R/'verify/n100_boundary_circle_propagation.py',R/'verify/n100_voronoi_bisector_vertex.py',R/'verify/n100_voronoi_nearest_sites.py'];out.write_text(json.dumps({'schema':'n100-continuous-proof-interface-contracts/v1','primitive_methods':['distance_le','circle_eq','bisector_eq','nearest_le','norm_range'],'real_rational_solution_retention_cases':retained,'closed_tangent_and_strict_distance_examples':examples,'same_parent_contraction_intersection':joint,'fixed_core_actual_case':summary,'fixed_core_bridge':bridge,'negative_controls':controls,'scope':'declared necessary constraint systems; one actual fixed-core candidate compiled and retained; primitive soundness controls, not full4200 replay or independently proved geometry bridge','global_optimality':False,'bindings':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS continuous interfaces;5 primitives;',retained,'rational real solutions;',len(payload['constraints']),'actual map constraints;controls',len(controls))
if __name__=='__main__':main()
