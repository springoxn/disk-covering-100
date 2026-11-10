#!/usr/bin/env python3
"""Reject invalid parameters and altered upper certificates.
These are implementation tests, not substitutes for the geometric proof.
"""
from fractions import Fraction as F
from pathlib import Path
import tempfile,json
from verify_global_lower import verify as lower, R0, KAPPA, sqrt_bounds
from verify_critical import verify as upper
HERE=Path(__file__).resolve().parent

def rejects(label,fn):
    try: fn()
    except (ValueError,KeyError,TypeError):
        print('PASS: rejected',label);return
    raise AssertionError('not rejected: '+label)

def main():
    rejects('radius above the certified exclusion threshold',lambda:lower(F(113,1000)))
    rejects('radius increased by 10^-8',lambda:lower(R0+F(1,10**8)))
    rejects('invalid concavity range',lambda:lower(F(1,3)))
    rejects('zero radius',lambda:lower(F(0)))
    rejects('negative kappa',lambda:lower(R0,F(-1)))
    rejects('insufficient q=1 joint-triangle constant',lambda:lower(R0,F(46,100)))
    rejects('negative radicand',lambda:sqrt_bounds(F(-1)))
    original=json.loads((HERE/'upper_certificate.json').read_text())
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'cert.json'
        for name,mutate in [
            ('missing candidate',lambda x:x['covering_indices'].pop()),
            ('extra candidate',lambda x:x['covering_indices'].append(0)),
            ('invalid covering-center index',lambda x:x['covering_indices'].__setitem__(0,100)),
            ('radius too small',lambda x:x.__setitem__('bound_squared',[1,10**6]))]:
            data=json.loads(json.dumps(original));mutate(data);p.write_text(json.dumps(data))
            rejects(name,lambda:upper(HERE/'configuration.json',p))
    print('PASS: all 11 rejection tests.')

if __name__=='__main__':main()
