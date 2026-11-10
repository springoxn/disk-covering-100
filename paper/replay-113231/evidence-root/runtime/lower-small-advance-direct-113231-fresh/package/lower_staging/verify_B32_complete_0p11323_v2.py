#!/usr/bin/env python3
"""Complete same-radius B32 branch, with catalog-free high-M metric closure."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
R=F(113231,1000000)

def run(path):
    proc=subprocess.run([sys.executable,'-B','-S',str(path)],cwd=HERE,
                        capture_output=True,text=True,check=True)
    data=json.loads(proc.stdout)
    assert data['status']=='PASS'
    assert F(data['radius'])==R and (data['B'],data['m'])==(32,100)
    assert F(data['required_center_norm_squared_upper'])==1-R*R
    assert F(data['minimum_area_margin'])>0
    return data

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    low_path=HERE/'verify_B32_M25_direct_interface_0p11323.py'
    high_path=HERE/'verify_B32_highM_complete_0p11323.py'
    low=run(low_path);high=run(high_path)
    assert low['M']==25 and low['integer_profile_cases']==81
    premises=low['premises']
    assert premises['status']=='PASS' and F(premises['radius'])==R
    assert (premises['B'],premises['m'])==(32,100)
    assert premises['M_domain']=='M<=25'
    assert F(premises['two_low_degree_margin'])>0
    assert F(premises['M24_margin'])>0
    assert premises['remaining_case']['M']==25
    assert high['M_domain']=='M>=26'
    low_margin=min(F(low['minimum_area_margin']),F(premises['two_low_degree_margin']),F(premises['M24_margin']))
    margin=min(low_margin,F(high['minimum_area_margin']))
    paths=[low_path,high_path,HERE/'refresh_B32_low_core_0p11323.py',
           HERE/'B32_M25_direct_interface_0p11323_proposal.json']
    return dict(status='PASS',radius=str(R),B=32,m=100,
        scope='Complete B32 branch only, after whole-cover same-radius normalization; other boundary counts and the exact optimum remain separate',
        normalization='Normalize ALL centers before classifying this diagram',
        required_center_norm_squared_upper=str(1-R*R),
        same_radius_components=True,fresh_process_components=2,
        low_M_domain='M<=25',high_M_domain='M>=26',
        direct_M25_cases=81,
        low_M_minimum_area_margin=str(low_margin),
        direct_M25_minimum_area_margin=low['minimum_area_margin'],
        high_M_minimum_area_margin=high['minimum_area_margin'],
        minimum_area_margin=str(margin),graph_catalog_used=False,
        remaining_boundary_counts=premises['remaining_boundary_counts'],
        source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        low_M=low,high_M=high)

if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
