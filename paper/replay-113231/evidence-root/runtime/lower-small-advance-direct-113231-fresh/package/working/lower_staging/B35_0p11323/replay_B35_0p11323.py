#!/usr/bin/env python3
"""Fresh-process standard-library replay and source preservation audit."""
from fractions import Fraction as F
from pathlib import Path
import ast,hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def assigned(path,name):
    tree=ast.parse(path.read_text())
    matches=[n.value for n in tree.body if isinstance(n,ast.Assign)
             and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
    assert len(matches)==1
    return ast.literal_eval(matches[0])
def run(path):
    p=subprocess.run([sys.executable,'-B',str(path)],cwd=str(ROOT),
                     capture_output=True,text=True,check=True)
    return json.loads(p.stdout)
def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    manifest=json.loads((HERE/'source_manifest.json').read_text())
    hashes=manifest['historical_source_hashes']
    for path,expected in hashes.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    old=ROOT/'lower_bounds_extension_20261004/check_B35_normalized_penalty_0p11322.py'
    entry=HERE/'check_B35_complete_0p11323_v2.py'
    for name in ('ROWS','RESTRICTED'):
        assert assigned(old,name)==assigned(entry,name),name
    proposal=json.loads((HERE/'M26_rational_support_0p11323.json').read_text())
    assert assigned(entry,'M26_RESTRICTED')==proposal['row']
    envelope=run(HERE/'verify_normalized_boundary_penalty_0p11323.py')
    result=run(entry)
    assert result['status']==envelope['status']=='PASS'
    assert result['normalized_boundary_envelope']==envelope
    assert result['radius']==envelope['radius']=='113231/1000000'
    assert result['B']==35 and result['m']==100
    assert result['required_center_norm_squared_upper']=='9871789671/10000000000'
    assert envelope['required_center_norm_squared_upper']==result['required_center_norm_squared_upper']
    assert result['remaining_boundary_counts']==list(range(31,40))
    assert result['total_face_supports']==80 and result['total_vertex_supports']==2382
    assert F(result['minimum_area_margin'])>F(8,100000)
    branches=result['branches'];assert len(branches)==5
    assert F(branches[0]['M_le24_flagged_margin'])>0
    assert F(branches[1]['any_low_degree_margin'])>0
    assert branches[2]['source_ordinary_M26_status'].startswith('FAIL')
    assert F(branches[2]['ordinary_margin'])<0
    for name in ('M_ge27_margin','M26_low_degree_margin',
                 'M26_one_original_ear_margin','M26_one_bad_q1_margin'):
        assert F(branches[2][name])>0
    assert F(branches[3]['ordinary_margin'])>0 and F(branches[4]['ordinary_margin'])>0
    assert result['M26_core_topology']['status']=='PASS'
    assert result['M26_core_topology']['degree_two_core_vertices_upper']==1
    assert result['M26_core_topology']['integer_contradiction_margins']=={
        'disconnected_components':140,'bridge':36,'multiple_face_blocks':74,
        'two_core_degree_two_vertices':24}
    for branch in branches:
        assert F(branch['minimum_face_slack'])>0
        assert F(branch['minimum_vertex_slack'])>=0
        assert F(branch['shifted_ear_upper'])<0 and F(branch['bad_q1_upper'])<0
    return {'status':'PASS','radius':result['radius'],'B':35,
            'historical_sources_unchanged':len(hashes),
            'historical_rational_row_equality':'PASS',
            'fresh_process_envelope_and_complete_branch':'PASS',
            'failed_source_direct_M26_margin_disclosed':'PASS',
            'complete_M_case_split':'PASS','minimum_area_margin':result['minimum_area_margin'],
            'entry_sha256':hashlib.sha256(entry.read_bytes()).hexdigest(),
            'proof_sha256':hashlib.sha256((HERE/'B35_COMPLETE_0p11323_PROOF.md').read_bytes()).hexdigest()}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
