"""Second interface batch: incomparability, clutter/weights and closed controls."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
import n100_proof_interfaces_v2 as I
R=Path(__file__).resolve().parents[1]
def payload(box,points,weights=None):
 p={'target':'closed_unit_disk','radius_units':'squared','box':box,'points':points}
 if weights is not None:p['weights']=weights
 return p
def main():
 aware=json.loads((R/'verify/out/n100-box-aware-capacity.json').read_text(encoding='utf-8'));cap=json.loads((R/'verify/out/n100-nonseparated-capacity-cut.json').read_text(encoding='utf-8'));u=F(cap['radius_upper']);box=cap['root_box'];controls=[];examples=[]
 # Box-aware geometry can reject a pair despite its unconstrained MEC fitting.
 p=payload(aware['box'],aware['pool']);old=I.run_leaf('small_pool_capacity',p);new=I.run_leaf('box_aware_patterns',p);assert old['status']=='NOT_EXCLUDED' and new['status']=='EXCLUDED';I.intersect_leaf_results([old,new]);examples.append({'name':'box_constraint_beats_global_MEC','small_pool':old,'box_aware':new})
 # Conversely, average energy is not an exact MEC test for an acute triple.
 triple=[['159/250','0'],['108/125','0'],['3/4','67/500']];p=payload(box,triple);mec=I.run_leaf('small_pool_capacity',p);energy=I.run_leaf('box_aware_patterns',p);assert mec['status']=='EXCLUDED' and energy['status']=='NOT_EXCLUDED';examples.append({'name':'global_MEC_beats_mean_energy','small_pool':mec,'box_aware':energy})
 # An irrelevant reachable witness inflates sum of unweighted whole-pool capacities.
 clutter=triple+[['0','0']];p=payload(box,clutter,['1','1','1','0']);plain=I.run_leaf('small_pool_capacity',p);weighted=I.run_leaf('weighted_capacity',p);assert plain['status']=='NOT_EXCLUDED' and weighted['status']=='EXCLUDED';examples.append({'name':'zero_weight_removes_clutter','unweighted':plain,'weighted':weighted});assert I.intersect_leaf_results([plain,weighted])['status']=='EXCLUDED'
 equal=I.run_leaf('weighted_capacity',payload(box,triple,['1','1','1']));assert equal['status']=='EXCLUDED';assert equal['certificate']['sum_capacity_upper']==str(mec['certificate']['capacity_sum'])
 # Closed endpoints and arbitrary nonnegative weights remain admissible.
 closed=payload([['-1','1'],['-1','1'],['0','1']],[['-1','0'],['1','0']],['2','3']);assert I.run_leaf('weighted_capacity',closed)['status']=='NOT_EXCLUDED';assert I.run_leaf('box_aware_patterns',closed)['status']=='NOT_EXCLUDED'
 for label,change in [('negative_weight',lambda q:q['weights'].__setitem__(0,'-1')),('weight_length',lambda q:q.update(weights=['1'])),('float_weight',lambda q:q['weights'].__setitem__(0,1.0))]:
  bad=copy.deepcopy(closed);change(bad);assert I.run_leaf('weighted_capacity',bad)['status']=='PRECONDITION_MISSING';controls.append(label)
 zero=copy.deepcopy(closed);zero['weights']=['0','0'];assert I.run_leaf('weighted_capacity',zero)['status']=='NOT_EXCLUDED'
 tampered=copy.deepcopy(weighted);tampered['certificate']['per_center_capacity_upper'][-1]='0'
 try:I.intersect_leaf_results([tampered])
 except ValueError:controls.append('weighted_certificate_tamper')
 else:raise AssertionError('tampered weighted result')
 # Independent nonacute/collinear and duplicate small-circle controls.
 assert I.explicit_mec([(F(0),F(0)),(F(0),F(0)),(F(1),F(0))])==F(1,4)
 assert I.explicit_mec([(F(0),F(0)),(F(2),F(0)),(F(1),F(1,2))])==1
 ctx={'domain_type':'center_box','radius_units':'squared','instance_id':'box1','representation_id':'xy_then_squared_radius','normalization_id':'none','radius_domain_id':'T<=U2'};nodes=[{'id':m,'method':m,'context':ctx,'premises_satisfied':True} for m in ('small_pool_capacity','box_aware_patterns','weighted_capacity')];plan=I.validate_plan(nodes);assert plan['mathematical_verdict'] is None
 try:I.validate_plan(nodes,'ADD_BOUNDS')
 except ValueError:controls.append('shared_witness_budget_addition')
 else:raise AssertionError('additive witnesses accepted')
 out=R/'verify/out/n100-proof-interface-batch2.json';assert not out.exists();paths=[R/'verify/n100_proof_interfaces_v2.py',R/'verify/n100_proof_interfaces.py',R/'verify/n100_box_aware_capacity.py',R/'verify/n100_weighted_witness_capacity.py'];out.write_text(json.dumps({'schema':'n100-proof-interface-batch2/v1','verified_new_callable_methods':['box_aware_patterns','weighted_capacity'],'all_new_method_decisions_independently_replayed':True,'incomparability_and_clutter_examples':examples,'equal_weight_capacity_matches_unweighted_example':True,'closed_equality_and_zero_weights_not_excluded':True,'rejected_controls':controls,'valid_nonadditive_plan':plan,'registered_contracts':I.METHODS,'scope':'second reviewed batch; incomparability shown by explicit inputs, not universal timing or performance claims; other methods still under review','global_optimality':False,'bindings':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS batch2;box/MEC incomparable;weighted clutter;all new decisions independently replayed;controls',len(controls))
if __name__=='__main__':main()
