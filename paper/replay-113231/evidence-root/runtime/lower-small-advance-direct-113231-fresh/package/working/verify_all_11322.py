#!/usr/bin/env python3
"""Fresh-process exact replay of the complete .11322 lower-bound chain."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
def run_component(label,code):
 prelude="from fractions import Fraction as F\nimport json,sys\nassert __debug__\n"
 suffix="\nassert result['status']=='PASS'\nprint(json.dumps(result),flush=True)\n"
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',
  PYTHONPATH=os.pathsep.join([str(ROOT),str(ROOT/'lower_bounds_extension_20261004')]))
 start=time.monotonic()
 done=subprocess.run([sys.executable,'-B','-S','-c',prelude+code+suffix],cwd=ROOT,env=env,text=True,capture_output=True,check=True)
 return dict(label=label,seconds=time.monotonic()-start,result=json.loads(done.stdout))
def verify():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 out=dict(theorem='r_D(100)>5661/50000',scope='Universal lower bound; exact optimality remains unresolved',
  logical_normalization='Enlarge and normalize ALL centers at this same radius before generic reduction and common m/B classification')
 out['B31']=run_component('B31 unrestricted curvature at .11322',"""
import check_B31_curvature_0p11322 as c
result=c.verify()
assert result['radius_upper']=='5661/50000' and result['B']==31 and result['m']==100
assert result['forced_minimum_interior_degree']==6 and result['disk_isoperimetric_integer_gap']==41
""")
 out['B32']=run_component('B32 complete same-radius low/high-M and16-family chain',"""
import verify_B32_complete_0p11322 as c
result=c.verify()
assert result['radius']=='5661/50000' and result['B']==32 and result['m']==100
assert result['required_center_norm_squared_upper']==str(1-F(5661,50000)**2)
assert result['same_radius_components'] is True and result['fresh_process_components']==5
assert result['low_M_reduction_status']=='PASS' and result['low_M_remaining_case']==25
assert result['direct_M25_cases']==81 and F(result['direct_M25_minimum_margin'])>0
assert result['validated_full_graphs']==result['exact_generated_graph_equality_checks']==16
assert result['exhaustive_deletion_masks']==41 and result['canonical_cores']==16
assert result['remaining_boundary_counts']==list(range(31,40))
assert F(result['high_M_flagged_margin'])>0 and F(result['minimum_metric_area_margin'])>0
""")
 out['B33']=run_component('B33 complete same-radius hinge and compact shared-edge metric chain',"""
import verify_B33_hinge_metric_complete_0p11322 as c
result=c.verify()
assert result['radius']=='5661/50000' and result['B']==33 and result['m_maximum']==100
assert result['required_center_norm_squared_upper']==str(1-F(5661,50000)**2)
assert result['graph_catalog_dependency'] is False and result['quadratic_radial_bootstrap_dependency'] is False
assert F(result['minimum_reported_area_margin'])>0
parts=result['components'];assert len(parts)==4
assert [p['source'] for p in parts]==['verify_hinge_B33_lowM_0p11322.py','verify_B33_highM_no_ears_0p11322.py','verify_N26_seven_face_metric_0p11322.py','verify_N27_metric_chord_cases_0p11322.py']
for part in parts:
 assert part['result']['status']=='PASS' and part['result']['radius']=='5661/50000'
assert parts[0]['result']['M_domain']=='M<=25'
assert parts[1]['result']['M_domain']=='M>=26'
assert parts[1]['result']['remaining_Euler_cases']==[dict(M=26,ears=0,bad_q1=0,degree_excess=1),dict(M=27,ears=0,bad_q1=0,degree_excess=0)]
assert parts[2]['result']['face_supports']==parts[3]['result']['face_supports']==7
assert parts[2]['result']['hinge_charge_spent'] is parts[3]['result']['hinge_charge_spent'] is False
""")
 out['B34']=run_component('B34 complete same-radius exact-lens bootstrap and face chain',"""
import verify_linear_bootstrap_B34_0p11322 as c
result=c.verify()
assert result['radius']=='5661/50000' and result['B']==34 and result['m']==100
assert (result['face_supports'],result['vertex_supports'],result['integer_ranges'])==(80,2235,5)
assert result['arbitrary_ears'] is result['arbitrary_bad_q1'] is result['arbitrary_all_boundary_q0'] is True
assert result['geometry']['status']=='PASS' and result['geometry']['remaining_boundary_counts']==list(range(31,40))
assert F(result['halfside_multiplier'])==F(1,2)
env=result['normalized_boundary_envelope']
assert env['status']=='PASS' and env['radius']=='5661/50000' and env['B']==34
assert env['required_center_norm_squared_upper']==str(1-F(5661,50000)**2)
assert result['no_second_deficit_spend'] is True
assert F(result['minimum_area_margin'])>0
""")
 out['B35']=run_component('B35 complete same-radius normalized penalty and core-profile chain',"""
import check_B35_normalized_penalty_0p11322 as c
result=c.verify()
assert result['radius']=='5661/50000' and result['B']==35 and result['m']==100
assert result['required_center_norm_squared_upper']==str(1-F(5661,50000)**2)
assert result['remaining_boundary_counts']==list(range(31,40))
assert result['range_one_face_support_status']==result['global_marked_status']==result['ear_support_status']==result['core_obstruction_status']=='PASS'
assert F(result['halfside_multiplier'])==F(33,100) and F(result['paid_q4_charge'])==F(1,500)
assert (result['total_face_supports'],result['total_vertex_supports'])==(70,1913)
assert result['normalized_boundary_envelope']['status']=='PASS'
assert F(result['minimum_area_margin'])>0
""")
 out['B36plus']=run_component('All B>=36 at the stronger unrestricted radius .11323',"""
import verify_capped_pair_B36plus_0p11323 as c
result=c.verify()
assert result['radius']=='113231/1000000' and result['m_at_most']==100 and result['boundary_counts']=='36 through 99'
assert result['complete_capped_pair']['status']=='PASS'
assert F(result['minimum_area_margin_at_B36'])>0 and F(result['additional_margin_per_boundary_cell'])>0
""")
 out['status']='PASS';return out
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

