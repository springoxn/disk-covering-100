#!/usr/bin/env python3
"""Sanity tests for rejection paths; not a replacement for the mathematical proof."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
from tempfile import TemporaryDirectory
import json
from verify_critical import verify as cv
from verify_quadtree import verify as qv
from verify_reduction import exclude_all,classify,U
HERE=Path(__file__).resolve().parent

def rejected(name,fn):
    try:fn()
    except (ValueError,TypeError,IndexError,KeyError,ZeroDivisionError):
        print('PASS: rejected',name);return
    raise RuntimeError('Invalid input was accepted: '+name)

def main():
    cfg=json.loads((HERE/'configuration.json').read_text())
    cert=json.loads((HERE/'upper_certificate.json').read_text())
    qc=json.loads((HERE/'quadtree_certificate.json').read_text())
    with TemporaryDirectory() as d:
        d=Path(d);cp=d/'c.json';tp=d/'t.json'
        def call(c,t,fn):
            cp.write_text(json.dumps(c));tp.write_text(json.dumps(t));return fn(cp,tp)
        t=deepcopy(cert);t['covering_indices']=t['covering_indices'][:-1]
        rejected('truncated critical certificate',lambda:call(cfg,t,cv))
        t=deepcopy(cert);t['covering_indices'].append(0)
        rejected('extra critical certificate entry',lambda:call(cfg,t,cv))
        t=deepcopy(cert);t['bound_squared']=[1,100]
        rejected('false smaller critical radius',lambda:call(cfg,t,cv))
        c=deepcopy(cfg);c['centers_numerators'][1]=c['centers_numerators'][0]
        rejected('duplicate centers',lambda:call(c,cert,cv))
        t=deepcopy(qc);t['preorder_nodes']=[-1]
        rejected('claim that the root rectangle is outside D',lambda:call(cfg,t,qv))
        t=deepcopy(qc);t['preorder_nodes']=[0]
        rejected('claim that one small disk covers the root rectangle',lambda:call(cfg,t,qv))
        t=deepcopy(qc);t['preorder_nodes']=t['preorder_nodes'][:-1]
        rejected('truncated rectangle tree',lambda:call(cfg,t,qv))
        t=deepcopy(qc);t['preorder_nodes'].append(0)
        rejected('extra rectangle tree node',lambda:call(cfg,t,qv))
        t=deepcopy(qc);t['radius_bound']=[1,10]
        rejected('rectangle radius not bound to the configuration',lambda:call(cfg,t,qv))
    rejected('false exclusion of n=100 at radius .113',lambda:exclude_all(100,F(113,1000)))
    rejected('false exclusion of n=57 at radius .16',lambda:exclude_all(57,F(4,25)))
    rejected('radius outside the established concavity range',lambda:classify(100,34,F(1,4)))
    rejected('boundary count outside the proven range',lambda:classify(100,100,U))
    print('PASS: all 13 rejection tests.')

if __name__=='__main__':main()
