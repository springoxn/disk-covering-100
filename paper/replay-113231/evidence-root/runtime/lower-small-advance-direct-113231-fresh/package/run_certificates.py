#!/usr/bin/env python3
"""Fresh replay of universal lower and configuration-specific upper certificates."""
from pathlib import Path
from fractions import Fraction
import json,os,subprocess,sys,time
from verify_package import verify as verify_integrity
ROOT=Path(__file__).resolve().parent
LOW=Fraction(11323,100000)
HIGH=Fraction(1154469548855829,10**16)

def run(args):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    start=time.monotonic()
    result=subprocess.run([sys.executable,'-B','-S',*map(str,args)],cwd=ROOT,
                          env=env,capture_output=True,text=True,check=True)
    data=json.loads(result.stdout)
    assert data['status']=='PASS'
    return {'seconds_reporting_only':time.monotonic()-start,'result':data}

def verify():
    if not __debug__:
        raise RuntimeError('Assertions must remain enabled')
    integrity=verify_integrity()
    lower=run([ROOT/'working/verify_all_11323.py'])
    assert lower['result']['theorem']=='r_D(100)>113231/1000000'
    assert lower['result']['complete_surviving_boundary_counts']==list(range(31,40))
    for name in ['B31','B32','B33','B34','B35','B36plus']:
        assert lower['result'][name]['result']['status']=='PASS'
    upper=run([ROOT/'working/upper_configuration/verify_cover.py',
               ROOT/'working/upper_configuration/centers.csv','0.1154469548855829'])
    z=upper['result']
    assert Fraction(z['radius'])==HIGH
    assert z['input_centers']==z['distinct_centers']==100
    assert z['counts']['triples']==161700 and z['counts']['boundary_pairs']==4950
    assert z['counts']['boundary_candidates']==9900
    assert z['counts']['antipodes']==100 and z['counts']['cardinal']==4
    assert HIGH-LOW==Fraction(22169548855829,10**16)
    return {'status':'PASS','claim':'113231/1000000 < r_D(100) <= 1154469548855829/10^16',
            'lower_endpoint_strict':True,'upper_endpoint_inclusive':True,
            'unresolved_gap_exact':str(HIGH-LOW),'exact_optimum_claimed':False,
            'saved_PASS_reports_used_for_acceptance':False,
            'integrity':integrity,'lower':lower,'upper':upper}

if __name__=='__main__':
    print(json.dumps(verify(),indent=2),flush=True)
