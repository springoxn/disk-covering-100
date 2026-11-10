#!/usr/bin/env python3
"""Fresh-process universal exact .11323 lower-bound replay. No exact optimum claim."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parent;STAGING=ROOT.parent/'lower_staging'
R=F(113231,1000000);NORM=1-R*R
def run(label,path,checks):
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=os.pathsep.join(map(str,[ROOT,ROOT/'lower_bounds_extension_20261004',STAGING,path.parent])))
 prelude="from fractions import Fraction as F\nimport importlib.util,json\nassert __debug__\n"
 code="spec=importlib.util.spec_from_file_location('component',%r)\nc=importlib.util.module_from_spec(spec)\nspec.loader.exec_module(c)\nresult=c.verify()\n"%str(path)
 start=time.monotonic()
 done=subprocess.run([sys.executable,'-B','-S','-c',prelude+code+checks+"\nassert result['status']=='PASS'\nprint(json.dumps(result),flush=True)\n"],cwd=ROOT,env=env,text=True,capture_output=True,check=True)
 return dict(label=label,source=str(path.relative_to(ROOT.parent)),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),seconds=time.monotonic()-start,result=json.loads(done.stdout))
def verify():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 out=dict(theorem='r_D(100)>113231/1000000',scope='Universal lower bound for100 congruent closed disks and arbitrary centers; exact optimality unresolved',normalization='Normalize ALL centers at this radius before common diagram and m/B classification',required_center_norm_squared_upper=str(NORM))
 out['B31']=run('B31 global full-face curvature',ROOT/'verify_B31_global_low_degree_0p11323.py',"""
assert result['radius']=='113231/1000000' and (result['B'],result['m'])==(31,100)
assert result['required_center_norm_squared_upper']=='1'
assert result['degree_window']==[5,8] and result['all_twenty_face_label_multisets_allowed'] is True
assert (result['face_supports'],result['vertex_supports'])==(40,32)
assert result['global_degree_five_requirement']==1 and result['degree_five_requirement_for_M_le23']==2
assert F(result['minimum_area_margin'])>0
""")
 out['B32']=run('B32 complete low/high-M catalog-free chain',STAGING/'verify_B32_complete_0p11323_v2.py',"""
assert result['radius']=='113231/1000000' and (result['B'],result['m'])==(32,100)
assert F(result['required_center_norm_squared_upper'])==1-F(113231,1000000)**2
assert result['same_radius_components'] is True and result['fresh_process_components']==2
assert result['low_M_domain']=='M<=25' and result['high_M_domain']=='M>=26'
assert result['direct_M25_cases']==81 and result['graph_catalog_used'] is False
assert result['remaining_boundary_counts']==list(range(31,40))
assert F(result['minimum_area_margin'])>0
""")
 out['B33']=run('B33 coherent five-star and compact metric chain',ROOT/'verify_B33_hinge_metric_complete_0p11323.py',"""
assert result['radius']=='113231/1000000' and result['B']==33 and result['m_maximum']==100
assert F(result['required_center_norm_squared_upper'])==1-F(113231,1000000)**2
assert result['graph_catalog_dependency'] is result['quadratic_radial_bootstrap_dependency'] is False
assert len(result['components'])==6
assert F(result['M25_coherent_area_margin'])>0 and F(result['minimum_reported_area_margin'])>0
""")
 out['B34']=run('B34 complete one-bank q4 hinge rows',STAGING/'B34_0p11323/verify_hinge_B34_complete_0p11323.py',"""
assert result['radius']=='113231/1000000' and (result['B'],result['m'])==(34,100)
assert (result['face_supports'],result['vertex_supports'],result['integer_ranges'])==(48,1455,3)
assert result['arbitrary_ears'] is result['arbitrary_bad_q1'] is result['arbitrary_all_boundary_q0'] is True
assert result['geometry']['minimum_M']==22 and result['geometry']['remaining_boundary_counts']==list(range(31,40))
assert F(result['halfside_multiplier'])==F(1,2)
assert F(result['normalized_boundary_envelope']['required_center_norm_squared_upper'])==1-F(113231,1000000)**2
assert result['normalized_boundary_envelope']['variance_coefficient']=='0'
assert F(result['q4_hinge_allocation']['paid_q4_charge'])==F(1,50)
assert result['no_second_deficit_spend'] is True and F(result['minimum_area_margin'])>0
""")
 out['B35']=run('B35 normalized rows and one-core-ear exception',ROOT/'lower_staging/B35_0p11323/check_B35_complete_0p11323_v2.py',"""
assert result['radius']=='113231/1000000' and (result['B'],result['m'])==(35,100)
assert F(result['required_center_norm_squared_upper'])==1-F(113231,1000000)**2
assert result['remaining_boundary_counts']==list(range(31,40))
assert (result['total_face_supports'],result['total_vertex_supports'])==(80,2382)
assert result['range_one_face_support_status']==result['global_marked_status']==result['ear_support_status']==result['core_obstruction_status']=='PASS'
assert F(result['halfside_multiplier'])==F(33,100) and F(result['paid_q4_charge'])==F(1,500)
assert result['M26_core_topology']['core_faces']==102 and result['M26_core_topology']['degree_two_core_vertices_upper']==1
assert F(result['minimum_area_margin'])>0
""")
 out['B36plus']=run('All B36 through99 unrestricted capped-pair tail',ROOT/'verify_capped_pair_B36plus_0p11323.py',"""
assert result['radius']=='113231/1000000' and result['m_at_most']==100 and result['boundary_counts']=='36 through 99'
assert result['complete_capped_pair']['status']=='PASS'
assert F(result['minimum_area_margin_at_B36'])>0 and F(result['additional_margin_per_boundary_cell'])>0
""")
 out['common_count_bridge']=out['B32']['result']['low_M']['premises']['n99_exclusion']
 assert out['common_count_bridge']['radius']==str(R) and out['common_count_bridge']['n']==99
 assert F(out['common_count_bridge']['minimum_area_margin'])>0
 out['complete_surviving_boundary_counts']=list(range(31,40))
 out['status']='PASS';return out
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
