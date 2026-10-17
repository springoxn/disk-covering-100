"""Arc budget adapters: fixed-radius guard, support tampering and relaxation survival."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
import n100_arc_budget_interfaces as I
R=Path(__file__).resolve().parents[1]
def base():return {'configuration_id':'declared-normalized-cover-at-U','semantics_id':I.SEM,'radius_units':'radius','radius':str(I.U)}
def main():
 requests=[]
 for method,m,k in [('arc_cap',100,55),('arc_cap',100,54),('arc_lens',100,54)]:
  p=base();p.update(m=m,k=k);requests.append((method,p))
 for counts in ({'near':34,'tail':20,'central':46},{'near':33,'tail':21,'central':46},{'near':0,'tail':0,'central':100}):
  p=base();p['counts']=counts;requests.append(('radial_profiles',p))
 controls=[]
 for label,change in [('implicit_transfer_below_U',lambda p:p.update(radius=str(I.U-F(1,10**12)))),('squared_radius',lambda p:p.update(radius_units='squared')),('wrong_count_semantics',lambda p:p.update(semantics_id='B-is-number-of-arcs')),('k_exceeds_m',lambda p:p.update(k=101)),('float_radius',lambda p:p.update(radius=0.115)),('missing_configuration',lambda p:p.pop('configuration_id'))]:
  p=base();p.update(m=100,k=55);change(p);requests.append(('arc_cap',p));controls.append(label)
 p=base();p['counts']={'near':33,'tail':21,'central':-1};requests.append(('radial_profiles',p));controls.append('invalid_multiplicities')
 results,receipt=I.run_batch(requests);assert results[0]['status']=='EXCLUDED' and results[1]['status']=='NOT_EXCLUDED' and results[2]['status']=='NOT_EXCLUDED';assert results[4]['status']=='NOT_EXCLUDED' and results[4]['detail']['capacity_satisfied_is_cover'] is False;assert all(row['verdict']=='NOT_EXCLUDED' for row in results[4]['detail']['target_rows']);assert results[5]['status']=='EXCLUDED';assert all(r['status']=='PRECONDITION_MISSING' for r in results[6:]);assert receipt['replay_counts']=={'cap_segments':2000,'lens_slabs':65536,'profile_slabs':18432,'target_radii':100}
 original=json.loads((R/'verify/out/n100-multiradius-capacity.json').read_text(encoding='utf-8'));mapping={'excluded':'EXCLUDED','capacity_satisfied':'NOT_EXCLUDED','undecided':'UNDECIDED'};assert [r['verdict'] for r in results[3]['detail']['target_rows']]==[mapping[p['verdict']] for p in original['profiles']]
 cap=json.loads((R/'verify/out/n100-arc-cap-rational-support.json').read_text(encoding='utf-8'));bad=copy.deepcopy(cap);bad['steps'][0]['cap_upper']='0'
 try:I.cap_audit(bad)
 except ValueError:controls.append('understated_cap_support')
 else:raise AssertionError('invalid cap accepted')
 lens=json.loads((R/'verify/out/n100-arc-lens-support.json').read_text(encoding='utf-8'));bad=copy.deepcopy(lens);bad['steps'][0]['slab_heights_upper'][0]='0'
 try:I.audit_lens(bad)
 except ValueError:controls.append('understated_lens_height')
 else:raise AssertionError('invalid lens accepted')
 bad=copy.deepcopy(original);bad['profiles'][-1]['parts'][0]['lower']='999'
 try:I.audit_profiles(bad,F(lens['maximum_half_arc_upper']))
 except ValueError:controls.append('false_profile_lower_integral')
 else:raise AssertionError('invalid profile accepted')
 paths=[R/'verify/n100_arc_budget_interfaces.py',R/'verify/n100_arc_cap_independent.py'];out=R/'verify/out/n100-arc-budget-interface-contracts.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-arc-budget-interface-contracts/v1','replay':receipt,'arc_cap_k55_excluded':results[0],'arc_cap_k54_retained':results[1],'arc_lens_k54_retained':results[2],'original_profiles_match_saved_verdicts':True,'reweighted_profile_relaxation_survives':results[4],'all_central_radial_type_excluded_by_arcs':results[5],'negative_controls':controls,'scope':'three fixed-U necessary budget adapters; independent squared support/strip replay and noncover relaxation semantics; no uniform radius transfer or angular coverage','global_optimality':False,'bindings':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS arc budgets;2000 cap segments;65536 lens +18432 profile slabs;100 targets;controls',len(controls))
if __name__=='__main__':main()
