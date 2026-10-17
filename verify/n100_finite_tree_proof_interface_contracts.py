"""Finite-cycle, parent-specific nogood and closed-real-tree contracts."""
from pathlib import Path
from itertools import product
import json,copy,hashlib
import n100_finite_proof_interfaces as F
import n100_split_tree_proof_interfaces as T
R=Path(__file__).resolve().parents[1]
def finite(n=3,inequality=False):
 return {'context':{'semantics_id':'finite-ordered-arc-relaxation/v1','map_id':'test-declared-system','frame_id':'fixed-test-frame','parent_box_id':'test-parent','radius_domain_id':'declared-squared-bounds'},'variables':list(range(n)),'domains':[3]*n,'tables':[{'0':2,'1':1} if inequality else {'0':3,'1':3} for _ in range(n)],'same_quadrant':[False]*n,'nogoods':[]}
def continuous():
 q=2**20;ctx={'semantics_id':'scaled-real-map-boxes/v1','scale':q,'map_id':'test-declared-system','frame_id':'fixed-test-frame','parent_box_id':'test-parent','radius_domain_id':'declared-squared-bounds'}
 return {'context':ctx,'boxes':[[-3*q,3*q,0,0]]*3,'constraints':[{'op':'norm_range','v':0,'lower2':str(q*q),'upper2':str(4*q*q),'map_id':ctx['map_id']}],'sweep_limit':1}
def main():
 controls=[];assert F.run(finite(3,True))['status']=='EXCLUDED';assert F.run(finite(4,True))['supported_domains']==[3]*4
 p=finite();p['domains']=[7]*3;p['tables']=[{'0':7,'1':7,'2':7} for _ in range(3)];p['same_quadrant']=[True,True,False];r=F.run(p);assignments=[]
 for x in product((0,1,2),repeat=3):
  if all(max(x[:i+1])<=x[i]+1 for i in (1,2)):assignments.append(x)
 expected=[sum(1<<j for j in {x[i] for x in assignments}) for i in range(3)];assert r['supported_domains']==expected
 for x in product((0,1,2),repeat=3):
  fixed=copy.deepcopy(p);fixed['domains']=[1<<j for j in x];assert (F.run(fixed)['status']!='EXCLUDED')==(x in assignments)
 for key in (0.5,'00'):
  bad=finite();bad['tables'][0]={key:3,'1':3};assert F.run(bad)['status']=='PRECONDITION_MISSING';controls.append('invalid_relation_key_'+str(key))
 parent=continuous();q=2**20;tiles={str(v):{'0':[0,0,0,0],'1':[-3*q,3*q,0,0]} for v in range(3)};record=F.learn_nogood(parent,tiles,[[0,0]]);p=finite();p.update(continuous_parent=parent,tiles=tiles,nogoods=[record]);assert F.run(p)['supported_domains']==[2,3,3]
 bad=copy.deepcopy(p);bad['nogoods'][0]['proof']['status']='NOT_EXCLUDED';assert F.run(bad)['status']=='PRECONDITION_MISSING';controls.append('tampered_nogood_proof');bad=copy.deepcopy(p);bad['continuous_parent']['context']['parent_box_id']='different-parent';assert F.run(bad)['status']=='PRECONDITION_MISSING';controls.append('cross_parent_nogood');bad=copy.deepcopy(p);bad['tiles']['0']['0']=[q,q,0,0];assert F.run(bad)['status']=='PRECONDITION_MISSING';controls.append('changed_tile_realization')
 try:F.learn_nogood(parent,tiles,[[0,1]])
 except ValueError:controls.append('feasible_subbox_cannot_be_learned')
 else:raise AssertionError('false nogood')
 bad=finite();bad['same_quadrant'][-1]=True;assert F.run(bad)['status']=='PRECONDITION_MISSING';controls.append('closing_prefix_not_reset')
 # Actual saved pairwise finite models: exact support, no continuous-cover claim.
 source=R/'verify/out/n100-arc-ordered-cycle.json';saved=json.loads(source.read_text(encoding='utf-8'));actual=[]
 for case in saved['cases']:
  order=case['cycle_order'];lookup={frozenset((r['v'],r['w'])):r for r in case['relations']};tables=[]
  for i,v in enumerate(order):
   w=order[(i+1)%len(order)];rel=lookup[frozenset((v,w))];tables.append(rel['forward'] if rel['v']==v else rel['reverse'])
  model=finite(len(order));model.update(variables=order,domains=[case['domains_after_arc_consistency'][str(v)] for v in order],tables=tables);res=F.run(model);assert res['supported_domains']==[case['globally_supported_domains'][str(v)] for v in order];actual.append({'placement':case['placement'],'source_node':case['source_node'],'supported_label_count':sum(b.bit_count() for b in res['supported_domains']),'statistics':res['statistics'],'status':res['status']})
 root=continuous();root['boxes']=root['boxes'][:1];root['constraints'][0]['upper2']=str(q*q);root['constraints'].append({'op':'norm_range','v':0,'lower2':str(4*q*q),'upper2':str(4*q*q),'map_id':root['context']['map_id']});shallow=T.generate(root,0);assert T.verify(shallow)['status']=='UNDECIDED';tree=T.generate(root,3);result=T.verify(tree);assert result['status']=='EXCLUDED'
 for label,change in [('missing_child',lambda z:z['nodes'][0]['children'].pop()),('reused_child',lambda z:z['nodes'][0]['children'].__setitem__(1,z['nodes'][0]['children'][0])),('false_excluded_root',lambda z:z['nodes'][0].update(kind='excluded')),('unreachable_extra_node',lambda z:z['nodes'].append(copy.deepcopy(z['nodes'][-1]))),('integer_lattice_gap',lambda z:z['nodes'][z['nodes'][0]['children'][1]]['replay']['boxes'][0].__setitem__(0,z['nodes'][0]['cut']+1))]:
  bad=copy.deepcopy(tree);change(bad)
  try:T.verify(bad)
  except ValueError:controls.append(label)
  else:raise AssertionError(label)
 out=R/'verify/out/n100-finite-tree-proof-interface-contracts-v2.json';assert not out.exists();paths=[R/'verify/n100_finite_proof_interfaces.py',R/'verify/n100_split_tree_proof_interfaces.py',R/'verify/n100_continuous_proof_interfaces.py',R/'verify/n100_arc_nogood_state_dp.py',R/'verify/n100_arc_cycle_support.py',source];out.write_text(json.dumps({'schema':'n100-finite-tree-proof-interface-contracts/v2','odd_cycle_excluded_even_cycle_retained':True,'ordered_small_model_bruteforce_support_match':True,'parent_specific_nogood':record,'unproved_nogood_rejected':True,'actual_two_saved_cycle_models':actual,'depth0_unresolved':T.verify(shallow),'closed_real_tree_full_replay':result,'complete_tree_certificate':tree,'negative_controls':controls,'scope':'finite necessary models and complete declared real-root tree; geometric bridges inherited; no full map/global cover claim','global_optimality':False,'bindings':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS finite/tree interfaces;2 actual cycles;parent-bound nogood;closed tree nodes',result['nodes_replayed'],'controls',len(controls))
if __name__=='__main__':main()
