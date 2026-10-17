"""Third batch tests: supplied-pool Hall completeness and scoped LOCAL reuse."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
import n100_proof_interfaces_v3 as I
R=Path(__file__).resolve().parents[1]
def main():
 saved=json.loads((R/'verify/out/n100-hall-automatic-search.json').read_text(encoding='utf-8'));hall_cases=[];controls=[]
 for case in saved['results']:
  payload={'target':'closed_unit_disk','radius_units':'squared','box':case['root_box'],'points':saved['pool']};r=I.run_leaf('automatic_hall',payload);assert r['status']==('EXCLUDED' if case['available_outer_centers']<8 else 'NOT_EXCLUDED');hall_cases.append({'available':case['available_outer_centers'],'result':r})
 full=copy.deepcopy(payload);full['box']=[['-1','1'] for _ in range(200)]+[payload['box'][-1]];assert I.run_leaf('automatic_hall',full)['status']=='NOT_EXCLUDED'
 for label,change in [('duplicate_witness',lambda p:p['points'].append(p['points'][0])),('outside_witness',lambda p:p['points'].append(['2','0'])),('empty_pool',lambda p:p.update(points=[]))]:
  p=copy.deepcopy(full);change(p);assert I.run_leaf('automatic_hall',p)['status']=='PRECONDITION_MISSING';controls.append(label)
 nohall=hall_cases[-1]['result'];bad=copy.deepcopy(nohall);bad['certificate']['matching'][1][1]=bad['certificate']['matching'][0][1]
 try:I.matching_replay(bad['proof_input']['box'],bad['proof_input']['points'],bad['certificate'])
 except ValueError:controls.append('noninjective_matching')
 else:raise AssertionError('bad matching')
 local_saved=json.loads((R/'verify/out/n100-hybrid-local-tree-interface.json').read_text(encoding='utf-8'));local_cases=[]
 for tree in local_saved['examples']:
  p={'target':'closed_unit_disk','radius_units':'squared','box':tree['root_box'],'local_node':tree['nodes'][tree['root']]};r=I.run_leaf('local_root_box',p);assert r['status']=='EXCLUDED';assert r['independent_replay']['corner_checks']==400;local_cases.append(r)
 local_payload=local_cases[0]['proof_input']
 for label,change in [('wrong_rotation',lambda p:p['local_node'].update(rotation=['1','1'])),('duplicate_label',lambda p:p['local_node']['permutation'].__setitem__(0,1)),('oversized_local_box',lambda p:p['box'].__setitem__(0,['-1','1'])),('strict_endpoint_lost',lambda p:p['box'].__setitem__(-1,['0','1'])),('missing_local_theorem_binding',lambda p:p['local_node'].update(binding={})),('kkt_root_only_is_not_LOCAL_leaf',lambda p:p.update(local_node={'kkt_root_exists':True}))]:
  bad=copy.deepcopy(local_payload);change(bad);assert I.run_leaf('local_root_box',bad)['status']=='PRECONDITION_MISSING';controls.append(label)
 # A LOCAL result can intersect other necessary constraints on its exact same box.
 cp={'target':'closed_unit_disk','radius_units':'squared','box':local_payload['box'],'points':[['-1','0'],['1','0']]};capacity=I.run_leaf('small_pool_capacity',cp);assert capacity['status']=='NOT_EXCLUDED';joined=I.intersect_leaf_results([local_cases[0],capacity]);assert joined['status']=='EXCLUDED' and joined['scope']=='specified_box_only'
 for label,change in [('forged_local_global_scope',lambda p:p.update(scope='global',global_optimality=True)),('altered_local_binding',lambda p:p['certificate']['local_binding'].update(fake='0'*64))]:
  bad=copy.deepcopy(local_cases[0]);change(bad)
  try:I.intersect_leaf_results([bad])
  except ValueError:controls.append(label)
  else:raise AssertionError(label)
 paths=[R/'verify/n100_proof_interfaces_v3.py',R/'verify/n100_proof_interfaces_v2.py',R/'verify/n100_hall_automatic_search.py',R/'verify/n100_hybrid_local_tree.py',R/'verify/out/n100-hybrid-local-tree-interface.json'];out=R/'verify/out/n100-proof-interface-batch3.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-proof-interface-batch3/v1','hall_supplied_pool_cases':hall_cases,'full_box_hall_not_excluded':True,'local_identity_and_rotation_relabel_cases':local_cases,'same_box_LOCAL_capacity_intersection':joined,'negative_controls':controls,'registered_contracts':I.METHODS,'scope':'six callable methods, including discovery vs verification separation and LOCAL hash-chain/corner inclusion; supplied-pool Hall completeness only; no global tree or independent reproof of local theorem','global_optimality':False,'bindings':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS batch3;Hall available1/3/7/8;LOCAL identity+rotation;LOCAL+capacity;controls',len(controls))
if __name__=='__main__':main()
