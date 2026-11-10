#!/usr/bin/env python3
"""Recompute all claimed certificates. No numerical optimizer is used."""
from pathlib import Path
from fractions import Fraction as F
import json
from verify_critical import verify as critical_verify
from verify_quadtree import verify as rectangle_verify
from verify_reduction import verify as reduction_verify,U,require
HERE=Path(__file__).resolve().parent

def verify():
    cfg=json.loads((HERE/'configuration.json').read_text())
    cert=json.loads((HERE/'upper_certificate.json').read_text())
    require(F(*cfg['radius_bound'])==U,'configuration radius does not match claimed upper bound')
    require(F(*cert['bound_squared'])==U*U,'critical certificate radius mismatch')
    upper=critical_verify(HERE/'configuration.json',HERE/'upper_certificate.json')
    rectangle=rectangle_verify(HERE/'configuration.json',HERE/'quadtree_certificate.json')
    reduction=reduction_verify()
    lo=F(*reduction['relaxation_pass_at_0_113']['expression_interval'][0])
    require(lo>F(4,100000),'stated positive relaxation margin failed')
    (HERE/'upper_verification_result.json').write_text(json.dumps(upper,indent=2)+'\n')
    (HERE/'quadtree_verification_result.json').write_text(json.dumps(rectangle,indent=2)+'\n')
    (HERE/'reduction_verification_result.json').write_text(json.dumps(reduction,indent=2)+'\n')
    report={'status':'PASS','lower':[11297473,100000000],
            'upper':[U.numerator,U.denominator],
            'critical_candidates':upper['candidate_counts'],
            'quadtree':rectangle,
            'necessary_count_pairs':reduction['count_families_not_excluded'],
            'exact_optimum_proved':False,
            'scope':'A rigorous interval and necessary count restrictions, not the exact optimal value.'}
    (HERE/'verification_result.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    a=verify()
    print('PASS: independent exact critical-point checker:',a['critical_candidates'])
    print('PASS: independent exact whole-rectangle checker:',a['quadtree'])
    print('PASS: inherited global lower bound and new count restrictions.')
    print('Necessary count pairs not excluded:',a['necessary_count_pairs'])
    print('CERTIFIED: 11297473/100000000 < r_D(100) <= 11563027143/100000000000')
    print('NOT CERTIFIED: exact optimum, exact optimal centers, or global optimality of this configuration.')
