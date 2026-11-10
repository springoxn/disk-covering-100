#!/usr/bin/env python3
"""Exact B=34,35,36 exclusions at radius 2261/20000.

The separate star certificate handles B=33. This file does not prove exact
optimality. All decisions use integers or fractions; floats only show timings.
"""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util
import json
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj
b = load('pair_base_11305', ROOT/'pair_bound_certificate_20261004'/'verify_pair_bound.py')
v = load('fraction_base_11305', ROOT/'lower_bounds_extension_20261004'/'verify_extension.py')
R = Q(2261, 20000)
LAMBDA34 = Q(3, 50)
K34 = Q(3892, 12500)
MU34 = Q(-4534107, 10**9)
L34 = Q(7, 800)
MU35 = Q(-4281108, 10**9)
L35 = Q(41, 5000)

def bridge_and_minimum_arc():
    v.check_concavity_factorization()
    v.check_kappa()
    ex99 = v.exclude_all(99, R)
    survivors = [B for B in range(3,100)
                 if v.classify(100,B,R)['status'] == 'not excluded']
    assert survivors == [33,34,35,36]
    B, theta = 34, Q(9,100)
    assert theta < 2*v.PL/B
    upper = (((198-B)*v.AH+B*v.KAPPA)*R**2
             +v.H_upper(R,theta,theta)
             +(B-1)*v.H_upper(R,(2*v.PL-theta)/(B-1),(2*v.PH-theta)/(B-1)))
    margin = v.PL-upper
    assert margin > Q(1,100000)
    assert v.sin_at(theta/2)[0] > R*Q(397,1000)
    return dict(status='PASS', exclusion_of_99=ex99, survivors=survivors,
                minimum_B34_full_arc=str(theta), normalized_sine_lower='397/1000',
                exact_constrained_Jensen_margin=str(margin))

def triangle_checks_34():
    D, ONE = b.D, b.ONE
    assert b.A_UP*b.A_UP > Q(27,16)
    def val(q,x):
        if q == 1:
            return b.sub(b.mul(x,b.add(ONE,b.scal(b.sqrt(b.sub(ONE,b.sq(x))),2))),
                         b.mul(b.ci(4*LAMBDA34),b.sq(x)))
        if q == 2:
            root = b.sqrt(b.sub(b.scal(x,2),b.sq(x)))
            if x[1] <= D:
                return b.sub(b.add(x,root),b.mul(b.ci(4*LAMBDA34),x))
            assert x[0] >= D
            return b.sub(b.mul(b.add(x,ONE),root),b.mul(b.ci(4*LAMBDA34),x))
        return b.add(b.mul(b.ci(4*b.A_UP/9-4*LAMBDA34),x),
                     b.sqrt(b.sub(b.scal(x,3),b.sq(x))))
    rows=[]
    for q, initial in [(1,[(0,D)]),(2,[(0,D),(D,2*D)]),(3,[(0,3*D)])]:
        todo=initial[:]; count=0; target=b.ci(b.A_UP+q*K34)[0]
        while todo:
            x=todo.pop(); count+=1
            if val(q,x)[1] <= target:
                continue
            mid=sum(x)//2
            assert x[0] < mid < x[1], 'Unresolved triangle interval'
            todo.extend([(x[0],mid),(mid,x[1])])
        rows.append(dict(marked_sides=q,status='PASS',boxes=count))
    return rows

def pair_replay(B, lam, mu, target, xmin):
    b.R, b.R2, b.LAM = b.ci(R), b.ci(R*R), b.ci(lam)
    lo = b.ci(xmin)[0]
    assert Q(lo,b.D) == xmin
    todo=[(lo,b.D,lo,b.D)]; visited=accepted=0
    M,T=b.ci(mu),b.ci(target)[0]
    start=time.monotonic()
    while todo:
        box=todo.pop(); visited+=1
        if box[0] > box[3]:
            continue
        if b.bound(box,M) <= T:
            accepted+=1
            continue
        widths=(box[1]-box[0],box[3]-box[2])
        axis=0 if widths[0]>=widths[1] else 2
        mid=(box[axis]+box[axis+1])//2
        assert box[axis]<mid<box[axis+1], 'Unresolved pair interval'
        left=list(box); right=list(box)
        left[axis+1]=mid; right[axis]=mid
        todo.extend((tuple(left),tuple(right)))
    return dict(B=B,status='PASS',lambda_value=str(lam),mu=str(mu),target=str(target),
                normalized_sine_minimum=str(xmin),visited=visited,accepted=accepted,
                seconds=time.monotonic()-start)

def final_margins():
    rows=[]
    for B,K,mu,L in [(34,K34,MU34,L34),(35,b.KAPPA,MU35,L35),(36,b.KAPPA,MU35,L35)]:
        margin=(1-mu)*v.PL-((198-B)*b.A_UP+B*K)*R**2-B*L
        assert margin > 0
        rows.append(dict(B=B,status='PASS',exact_margin_lower=str(margin)))
    return rows

def verify():
    result=dict(scope='Exact exclusions of B34, B35, B36 at r=.11305; B33 is separate',
                bridge=bridge_and_minimum_arc(),
                baseline_triangles=b.triangle_checks(),
                retuned_triangles=triangle_checks_34())
    result['pair_bounds']=[pair_replay(34,LAMBDA34,MU34,L34,Q(397,1000)),
                           pair_replay(35,Q(1,25),MU35,L35,Q(0))]
    result['final_margins']=final_margins()
    result['status']='PASS'
    return result

if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run Python with assertions enabled')
    print(json.dumps(verify(),indent=2),flush=True)
