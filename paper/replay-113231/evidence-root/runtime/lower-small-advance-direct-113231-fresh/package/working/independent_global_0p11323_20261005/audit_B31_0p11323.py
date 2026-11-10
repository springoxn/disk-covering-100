#!/usr/bin/env python3
"""Independent same-radius audit of the B31 two-row branch, not universal optimality."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,itertools,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
R=F(113231,1000000)
def verify():
    if not __debug__: raise RuntimeError('Assertions must remain enabled')
    # Independent arithmetic for the two combinatorial curvature contradictions.
    assert 6*167-31*31==41
    for M in range(24): assert 5*(136-M)-M*M>0
    assert 5*(136-23)-23*23==36
    for b in (3,4): assert b-2<=F(b*b,5)
    for b in range(5,201):
        for b1 in range(3,b):
            b2=b+2-b1
            assert b2>=3 and b1*b1+b2*b2<=b*b
        assert b+(b-5)+F((b-5)**2,5)==F(b*b,5)
    data=json.loads((ROOT/'B31_global_low_degree_0p11323_proposals.json').read_text())
    assert data['radius']==str(R) and data['B']==31
    multisets=list(itertools.combinations_with_replacement(range(4),3))
    assert len(multisets)==20
    assert [(z['M'],z['required_degree_five_count']) for z in data['rows']]==[(23,2),(24,1)]
    for z in data['rows']:
        assert [tuple(f['indices']) for f in z['faces']]==multisets
        potentials=[F(z[k],z['potential_denominator']) for k in ('high_potential','boundary_potential')]+[F(0),F(z['low_potential'],z['potential_denominator'])]
        assert max(potentials)-min(potentials)<1
        assert z['flag']>=0 and z['apex']==0
        assert all(z[k]>=0 for k in ('interface_a','interface_0','interface_low'))
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    done=subprocess.run([sys.executable,'-B','-S',str(ROOT/'verify_B31_global_low_degree_0p11323.py')],cwd=ROOT,env=env,text=True,capture_output=True,check=True)
    result=json.loads(done.stdout)
    assert result['status']=='PASS' and result['radius']==str(R) and (result['m'],result['B'])==(100,31)
    assert result['required_center_norm_squared_upper']=='1'
    assert result['center_projection_precedes_classification'] is True
    assert result['all_twenty_face_label_multisets_allowed'] is True and result['deep_label_assumption'] is False
    assert result['reflected_center_hypothesis'] is False
    assert result['halfside_multiplier']==result['squared_edge_penalty']=='0'
    assert result['degree_window']==[5,8] and result['ordinary_marked_incidence_upper']==3
    assert result['face_supports']==40 and result['vertex_supports']==32
    assert result['arbitrary_ears_and_bad_faces_allowed'] is True
    assert result['global_degree_five_requirement']==1 and result['degree_five_requirement_for_M_le23']==2
    assert F(result['minimum_area_margin'])>F(3797,10**6)
    assert [z['M_endpoint'] for z in result['branches']]==[23,24]
    assert F(result['branches'][0]['M_slope_lower'])>0 and F(result['branches'][1]['M_slope_upper'])<0
    for z in result['branches']:
        assert F(z['shifted_ear_upper'])<0 and F(z['bad_q1_upper'])<0
        assert F(z['minimum_face_slack'])>0 and F(z['minimum_vertex_slack'])>0 and F(z['area_margin'])>0
    prior=json.loads((ROOT/'B31_global_low_degree_0p11323_result.json').read_text())
    assert result==prior
    paths=['B31_GLOBAL_LOW_DEGREE_0p11323.md','verify_B31_global_low_degree_0p11323.py','B31_global_low_degree_0p11323_proposals.json','ONE_POSITIVE_CURVATURE_ISOPERIMETRY.md','verify_one_positive_curvature_isoperimetry.py','UNMARKED_LOW_DEGREE_CORE_OBSTRUCTION.md','lower_bounds_extension_20261004/GENERAL_DISK_ISOPERIMETRY.md','FULL_FACE_RANGE_ONE_SUPPORT.md','exact_range_one_face_support.py','QUADRATIC_MARKED_CONJUGATE.md','exact_quadratic_marked_conjugate.py','verify_global_star_anchor_degree_window.py','GLOBAL_STAR_ANCHOR_DEGREE_WINDOW.md','FACE_LABEL_INTERFACE_CHARGES.md','JENSEN_SLAB_EAR_SUPPORT.md','verify_jensen_slab_ear_support.py','lower_bounds_extension_20261004/verify_extension.py']
    return dict(status='PASS',radius=str(R),scope='Independent B31 branch audit only; no universal radius or exact-optimum claim',minimum_area_margin=result['minimum_area_margin'],fresh_output_equal_to_saved_result=True,full_branch_result=result,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})
if __name__=='__main__': print(json.dumps(verify(),indent=2))
