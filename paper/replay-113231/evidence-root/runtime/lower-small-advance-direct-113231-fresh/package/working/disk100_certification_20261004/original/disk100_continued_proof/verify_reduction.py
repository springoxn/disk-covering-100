#!/usr/bin/env python3
"""Exact finite checks for necessary count constraints, NOT an optimality proof.

All numerical acceptance uses Python integers/Fraction and rigorously bounded
trigonometric functions and square roots. The continuous geometry is proved
in PROOF.md and previous/GLOBAL_LOWER_PROOF.md.
"""
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import json
from verify_global_lower import (require,pi_bounds,sqrt_bounds,sin_at,cos_at,
                                 outward,encode,KAPPA,verify as verify_old_lower)
HERE=Path(__file__).resolve().parent
U=F(11563027143,10**11)
PI_LO,PI_HI=pi_bounds()
_s3lo,_s3hi=sqrt_bounds(F(3))
A_LO,A_HI=3*_s3lo/4,3*_s3hi/4

@lru_cache(None)
def trig(B):
    require(type(B) is int and B>=3,'B must be an integer at least three')
    sl,sh=outward(sin_at(PI_LO/B)[0],sin_at(PI_HI/B)[1])
    cl,ch=outward(cos_at(PI_HI/B)[0],cos_at(PI_LO/B)[1])
    require(0<sl<=sh<1 and 0<cl<=ch<1,'bad trigonometric interval')
    return sl,sh,cl,ch

def classify(n,B,r):
    """Return rigorous interval for the necessary expression, or arc exclusion."""
    require(type(n) is int and 3<=B<=n-1,'outside proven count range')
    require(type(r) is F and 0<r<F(1,5),'outside concavity range')
    sl,sh,cl,ch=trig(B)
    if sl>r:
        return {'n':n,'B':B,'status':'excluded by arc length','margin':encode(sl-r)}
    require(sh<r,'unresolved square root domain')
    coef=F(2*n-2,B)-1
    require(coef>0,'unexpected coefficient sign')
    lamlo,lamhi=coef*A_LO+KAPPA,coef*A_HI+KAPPA
    rl=sqrt_bounds(r*r-sh*sh)[0]
    rh=sqrt_bounds(r*r-sl*sl)[1]
    lo=lamlo*r*r+sl*rl-sh*ch
    hi=lamhi*r*r+sh*rh-sl*cl
    require(lo<=hi,'bad interval propagation')
    if hi<0:status='excluded by joint area'
    elif lo>0:status='not excluded by these necessary conditions'
    else:raise ValueError('insufficient arithmetic precision to classify')
    return {'n':n,'B':B,'status':status,'expression_interval':[encode(lo),encode(hi)]}

def exclude_all(n,r):
    rows=[classify(n,B,r) for B in range(3,n)]
    require(all(row['status'].startswith('excluded') for row in rows),
            f'Covering with {n} disks was NOT excluded')
    require(len(rows)==n-3,'missing count')
    return {'n':n,'radius':encode(r),'all_B_count':len(rows),'cases':rows}

def verify():
    # Also checks all four cases of the joint triangle lemma, rather than
    # treating numerical constants as unverified assumptions.
    old=verify_old_lower()
    require(old['status']=='PASS','inherited lower verification failed')
    exclude_95=exclude_all(95,U)
    inner=U/(1-2*U)
    require(0<inner<F(1,5),'inner disk exceeds the proved range')
    exclude_57=exclude_all(57,inner)
    families={};all_rows=[]
    for m in range(96,101):
        accepted=[]
        for B in range(3,m):
            if B>m-58:
                all_rows.append({'n':m,'B':B,'status':'excluded by inner disk count'})
            else:
                row=classify(m,B,U);all_rows.append(row)
                if row['status']=='not excluded by these necessary conditions':
                    accepted.append(B)
        families[str(m)]=accepted
    expected={"96":list(range(30,39)),"97":list(range(29,40)),
              "98":list(range(28,41)),"99":list(range(28,42)),
              "100":list(range(28,43))}
    require(families==expected,'the stated count families do not match recomputation')
    # A necessary-condition pass at .113 demonstrates the limitation of this
    # relaxation, not the existence of an actual .113 covering.
    obstruction=classify(100,34,F(113,1000))
    require(obstruction['status']=='not excluded by these necessary conditions',
            'claimed relaxation obstruction failed')
    return {'status':'PASS','upper_radius':encode(U),
            'inherited_lower_radius':old['radius'],
            'exclusion_of_95_disks':exclude_95,
            'inner_radius':encode(inner),'exclusion_of_57_inner_disks':exclude_57,
            'count_families_not_excluded':families,
            'total_count_pairs_not_excluded':sum(map(len,families.values())),
            'all_count_tests':all_rows,
            'relaxation_pass_at_0_113':obstruction,
            'scope':'Necessary count restrictions only. No enumeration of planar maps; no proof of exact global optimality.'}

if __name__=='__main__':
    result=verify()
    (HERE/'reduction_verification_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: inherited universal lower bound and joint triangle lemma.')
    print('PASS: all 92 boundary counts for n=95 excluded at U.')
    print('PASS: all 54 boundary counts for n=57 excluded at U/(1-2U).')
    print('Count pairs not excluded:',result['count_families_not_excluded'])
    print('Total:',result['total_count_pairs_not_excluded'])
    print('PASS: (n,B,r)=(100,34,113/1000) passes the area relaxation strictly.')
    print('NOT PROVED: actual feasibility of any surviving count pair; exact optimum.')
