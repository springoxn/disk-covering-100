"""Executable positive/negative checks for n100 proof interface contracts."""
from pathlib import Path
from fractions import Fraction as F
import copy,json,hashlib
import n100_proof_interfaces as I
R=Path(__file__).resolve().parents[1]
def main():
 h=json.loads((R/'verify/out/n100-separated-witness-hall.json').read_text(encoding='utf-8'));c=json.loads((R/'verify/out/n100-nonseparated-capacity-cut.json').read_text(encoding='utf-8'))
 hp={'target':'closed_unit_disk','radius_units':'squared','box':h['example_box'],'points':h['example_points']};cp={'target':'closed_unit_disk','radius_units':'squared','box':c['root_box'],'points':c['points']}
 hr=I.run_leaf('separated_hall',hp);cr=I.run_leaf('small_pool_capacity',cp);assert hr['status']==cr['status']=='EXCLUDED';joint=I.intersect_leaf_results([hr,cr]);assert joint['status']=='EXCLUDED' and not joint['global_optimality']
 full=copy.deepcopy(cp);full['box']=[['-1','1'] for _ in range(200)]+[cp['box'][-1]];assert I.run_leaf('small_pool_capacity',full)['status']=='NOT_EXCLUDED'
 closed={'target':'closed_unit_disk','radius_units':'squared','box':[['-1','1'],['-1','1'],['0','1']],'points':[['-1','0'],['1','0']]};assert I.run_leaf('small_pool_capacity',closed)['status']=='NOT_EXCLUDED';assert I.run_leaf('separated_hall',closed)['status']=='PRECONDITION_MISSING'
 controls=[]
 for label,mutate in [('radius_instead_of_squared',lambda p:p.update(radius_units='radius')),('float_proof_data',lambda p:p['box'][0].__setitem__(0,-0.5)),('wrong_target',lambda p:p.update(target='open_unit_disk'))]:
  bad=copy.deepcopy(cp);mutate(bad);assert I.run_leaf('small_pool_capacity',bad)['status']=='PRECONDITION_MISSING';controls.append(label)
 assert I.run_leaf('unreviewed_method',cp)['status']=='PRECONDITION_MISSING';controls.append('unreviewed_callable')
 ctx={'domain_type':'count_domain','radius_units':'radius','instance_id':'domain-U','representation_id':'normalized_B_cells','normalization_id':'same_radius_common_diagram','radius_domain_id':'r<=U'}
 nodes=[{'id':'inner','method':'recursive_count','context':copy.deepcopy(ctx),'premises_satisfied':True},{'id':'outer','method':'radius_local_joint','context':copy.deepcopy(ctx),'depends_on':['inner'],'premises_satisfied':True}];plan=I.validate_plan(nodes);assert plan['structurally_valid'] and plan['mathematical_verdict'] is None
 cases=[]
 def case(label,mutation,mode='INTERSECT'):
  bad=copy.deepcopy(nodes);mutation(bad)
  try:I.validate_plan(bad,mode)
  except ValueError:cases.append(label)
  else:raise AssertionError(label)
 case('unreviewed_method',lambda q:q[1].update(method='withdrawn_cut'))
 case('cycle_or_forward_dependency',lambda q:q[0].update(depends_on=['outer']))
 case('implicit_radius_conversion',lambda q:q[1]['context'].update(radius_units='squared'))
 case('different_configuration',lambda q:q[1]['context'].update(instance_id='different-domain'))
 case('different_normalization',lambda q:q[1]['context'].update(normalization_id='inner-rescaled'))
 case('different_radius_domain',lambda q:q[1]['context'].update(radius_domain_id='r<=newU'))
 case('missing_analytic_premise',lambda q:q[1].update(premises_satisfied=False))
 case('implicit_count_to_word_adapter',lambda q:q[1].update(method='ear_representative'))
 case('unlicensed_additive_area',lambda q:None,'ADD_BOUNDS')
 try:I.intersect_leaf_results([hr,I.run_leaf('small_pool_capacity',full)])
 except ValueError:cases.append('different_boxes_cannot_intersect_as_same_domain')
 else:raise AssertionError('different box accepted')
 for label,mutation in [('forged_exclusion_label',lambda q:q.update(status='NOT_EXCLUDED')),('tampered_capacity_certificate',lambda q:q['certificate'].update(capacity_sum=-1)),('global_scope_upgrade',lambda q:q.update(scope='global',global_optimality=True))]:
  bad=copy.deepcopy(cr);mutation(bad)
  try:I.intersect_leaf_results([bad])
  except ValueError:cases.append(label)
  else:raise AssertionError(label)
 out=R/'verify/out/n100-proof-interface-contracts-v2.json';assert not out.exists();source=R/'verify/n100_proof_interfaces.py';out.write_text(json.dumps({'schema':'n100-proof-interface-contracts/v1','verified_callable_leaf_examples':{'hall':hr,'capacity':cr,'intersection':joint},'closed_radius_equality_retained':True,'full_box_not_excluded':True,'leaf_negative_controls':controls,'plan_negative_controls':cases,'valid_plan':plan,'registered_contracts':I.METHODS,'scope':'first reviewed contract batch and two real leaf adapters; validates wiring and exact leaf examples, not all252scripts or analytic premises; plan validation alone carries no proof verdict','global_optimality':False,'bindings':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,R/'verify/out/n100-separated-witness-hall.json',R/'verify/out/n100-nonseparated-capacity-cut.json']},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS proof interfaces;2 real leaf exclusions;full/closed controls;negative controls',len(controls)+len(cases))
if __name__=='__main__':main()
