#!/usr/bin/env python3
"""Re-run both independent exact verifiers. Standard library only."""
from pathlib import Path
from fractions import Fraction as F
import json
from verify_global_lower import verify as verify_lower, R0
from verify_critical import verify as verify_upper

HERE=Path(__file__).resolve().parent
U=F(11573102001,10**11)

def main():
    lower=verify_lower()
    upper=verify_upper(HERE/'configuration.json',
                       HERE/'upper_certificate.json')
    if F(upper['upper_squared']) != U*U:
        raise ValueError('upper certificate does not use the claimed radius')
    if upper['exact_radius_squared'] is not None:
        raise ValueError('unexpected exact-radius exception in upper certificate')
    if not R0<U:
        raise ValueError('invalid resulting interval')
    (HERE/'lower_verification_result.json').write_text(json.dumps(lower,indent=2)+'\n')
    result={'lower_bound':str(R0),'upper_bound':str(U),'lower_strict':True,'upper_inclusive':True,
            'lower_counts':lower['counts'],'tightest_lower_case':lower['tightest_area_case']['B'],
            'upper_verification':upper,'exact_optimum_proved':False}
    (HERE/'verification_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: joint triangle lemma for q=0,1,2,3.')
    print('PASS: all B=3,...,99; 25 arc exclusions, 72 area exclusions.')
    print('PASS: fixed-center entire closed disk coverage:',upper['candidate_counts'])
    print('CERTIFIED:',R0,'< r_D(100) <=',U)
    print('NOT PROVED: an exact optimum, a matching lower bound, or globally optimal centers.')

if __name__=='__main__':main()
