#!/usr/bin/env python3
"""Complete normalized-diagram B32 branch at the exact radius .11322."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
R=F(5661,50000)

def run(path):
    result=subprocess.run([sys.executable,'-B','-S',str(path)],cwd=ROOT,
                          capture_output=True,text=True,check=True)
    data=json.loads(result.stdout);assert data['status']=='PASS';return data

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    high_path=HERE/'reduce_B32_high_core_0p11322.py'
    low_path=ROOT/'direct_M25_metric_20261004'/'verify.py'
    metric_path=ROOT/'metric_boundary_unrestricted_20261004'/'verify_family_0p11322.py'
    high=run(high_path)
    assert F(high['radius'])==R and high['B']==32 and high['M_domain']=='M>=26'
    assert F(high['required_center_norm_squared_upper'])==1-R*R
    expected={'M':26,'ears':0,'bad_q1':0,'all_interior_degrees':6,
              'core_vertices':68,'core_boundary':26,'core_faces':108,'canonical_full_graphs':16}
    assert high['remaining_case']==expected and F(high['flagged_margin'])>0
    low=run(low_path)
    assert F(low['radius'])==R and (low['B'],low['m'],low['M'])==(32,100,25)
    assert low['integer_profile_cases']==81 and F(low['minimum_area_margin'])>0
    premises=low['premises']
    assert F(premises['radius'])==R and premises['B']==32 and premises['m']==100
    assert premises['remaining_case']['M']==25
    # This is a complete M<=25 reduction, freshly replayed by the metric
    # star checker, not merely a free-standing assertion of its premises.
    assert premises['M_domain']=='M<=25' and premises['status']=='PASS'
    assert F(premises['two_low_degree_margin'])>0 and F(premises['M24_margin'])>0
    assert premises['weighted_curvature_status']=='PASS'
    catalog=run(HERE/'enumerate_B32_P26_F108_cores.py')
    catalog_path=HERE/'B32_P26_F108_core_catalog.json'
    assert catalog==json.loads(catalog_path.read_text())
    assert catalog['raw_perimeter_candidates']==41 and catalog['core_count']==16
    index=run(HERE/'export_B32_P26_F108_families.py')
    assert index==json.loads((HERE/'B32_P26_F108_graph_index.json').read_text())
    from export_B32_P26_F108_families import iter_graphs
    graph_hashes={}
    for graph in iter_graphs():
        path=ROOT/'signed_edge_metric_B32_20261004'/'graphs'/(graph['family_id']+'.json')
        raw=path.read_bytes()
        assert json.loads(raw)==json.loads(json.dumps(graph))
        graph_hashes[graph['family_id']]=hashlib.sha256(raw).hexdigest()
    assert len(graph_hashes)==16
    metric=run(metric_path)
    assert F(metric['radius'])==R and metric['graph_count']==16
    assert {x['family_id'] for x in metric['rows']}==set(graph_hashes)
    for row in metric['rows']:
        assert row['graph_sha256']==graph_hashes[row['family_id']]
        assert F(row['radius'])==R and F(row['area_margin'])>0
    assert F(metric['minimum_area_margin'])>0
    digest=hashlib.sha256(catalog_path.read_bytes()).hexdigest()
    assert index['core_catalog_sha256']==digest
    sources=[high_path,low_path,metric_path,HERE/'reduce_B32_low_core_0p11322.py']
    return dict(status='PASS',radius=str(R),B=32,m=100,
        scope='Complete B32 branch for whole-cover normalized diagrams; other B and the exact optimum remain separate',
        normalization='All centers have norm squared at most 1-R^2 before this diagram is classified',
        required_center_norm_squared_upper=str(1-R*R),
        same_radius_components=True,fresh_process_components=5,
        low_M_reduction_status=premises['status'],low_M_remaining_case=25,
        direct_M25_cases=81,direct_M25_minimum_margin=low['minimum_area_margin'],
        high_M_flagged_margin=high['flagged_margin'],high_M_remaining_case=expected,
        exhaustive_deletion_masks=41,canonical_cores=16,validated_full_graphs=16,
        exact_generated_graph_equality_checks=16,core_catalog_sha256=digest,
        minimum_metric_area_margin=metric['minimum_area_margin'],
        minimum_metric_margin_family=metric['minimum_margin_family'],
        remaining_boundary_counts=high['remaining_boundary_counts'],
        component_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})

if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
