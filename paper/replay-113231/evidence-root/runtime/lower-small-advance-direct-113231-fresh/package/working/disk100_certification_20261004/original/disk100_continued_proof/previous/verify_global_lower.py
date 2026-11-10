#!/usr/bin/env python3
"""Exact acceptance of finite inequalities for a UNIVERSAL lower bound.

Standard library only. No floating point in the acceptance path.
The geometric reduction is given in GLOBAL_LOWER_PROOF.md.
This is not a certificate of the exact optimal radius.
"""
from fractions import Fraction as F
from math import factorial, isqrt
from pathlib import Path
import json,sys

R0=F(11297473,100000000)
KAPPA=F(461134488,1000000000)
HERE=Path(__file__).resolve().parent

def require(test,msg):
    if not test: raise ValueError(msg)

def atan_bounds(q,N=40):
    x=F(1,q)
    value=sum(((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(N)),F(0))
    next_term=(-1)**N*x**(2*N+1)/F(2*N+1)
    return min(value,value+next_term),max(value,value+next_term)

def outward(lo,hi,digits=50):
    scale=10**digits
    lower=F(lo.numerator*scale//lo.denominator,scale)
    upper=F(-((-hi.numerator*scale)//hi.denominator),scale)
    require(lower<=lo<=hi<=upper,'bad outward rational rounding')
    return lower,upper

def pi_bounds():
    al,ah=atan_bounds(5);bl,bh=atan_bounds(239)
    return outward(16*al-4*bh,16*ah-4*bl)

def sqrt_bounds(value,digits=50):
    require(value>=0,'negative square root')
    scale=10**digits
    k=isqrt(value.numerator*scale*scale//value.denominator)
    lo,hi=F(k,scale),F(k+1,scale)
    require(lo*lo<=value<hi*hi,'bad square root enclosure')
    return lo,hi

def sin_at(x):
    # Taylor through degree 50 (the coefficient of x^50 is zero).
    S=sum(((-1)**j*x**(2*j+1)/factorial(2*j+1) for j in range(25)),F(0))
    E=abs(x)**51/factorial(51)
    return S-E,S+E

def cos_at(x):
    # Taylor through degree 49 (the coefficient of x^49 is zero).
    S=sum(((-1)**j*x**(2*j)/factorial(2*j) for j in range(25)),F(0))
    E=abs(x)**50/factorial(50)
    return S-E,S+E

def encode(x):return [x.numerator,x.denominator]

def verify(r=R0,kappa=KAPPA):
    require(type(r) is F and type(kappa) is F,'use exact Fraction inputs')
    require(0<r<F(1,5),'concavity range failed')
    require(kappa>0,'nonpositive kappa')
    pi_lo,pi_hi=pi_bounds()
    require(F(3)<pi_lo<pi_hi<F(22,7),'pi bounds failed')
    s3_lo,s3_hi=sqrt_bounds(F(3));s33_lo,s33_hi=sqrt_bounds(F(33))
    A_lo,A_hi=3*s3_lo/4,3*s3_hi/4
    G1_hi=sqrt_bounds((207+33*s33_hi)/128)[1]
    G2_hi=sqrt_bounds(9+6*s3_hi)[1]/2
    # For q=0 the classical triangle area bound is used directly.
    margins={1:A_lo+kappa-G1_hi,2:A_lo+2*kappa-G2_hi,
             3:3*kappa-A_hi}
    for q,m in margins.items():
        require(m>0,f'joint triangle bound failed for q={q}')
    rows=[]
    for B in range(3,100):
        xl,xh=pi_lo/B,pi_hi/B
        # sin increasing, cos decreasing on [0,pi/3].
        sl,sh=outward(sin_at(xl)[0],sin_at(xh)[1])
        cl,ch=outward(cos_at(xh)[0],cos_at(xl)[1])
        require(0<sl<=sh<1 and 0<cl<=ch<1,'trigonometric enclosure failed')
        if sl>r:
            rows.append({'B':B,'reason':'arc-count exclusion','margin':encode(sl-r)})
            continue
        require(sh<r,'insufficient precision to classify arc feasibility')
        radical_hi=sqrt_bounds(r*r-sl*sl)[1]
        lam_hi=(F(198,B)-1)*A_hi+kappa
        # Necessary condition: lambda*r^2 + s*sqrt(r^2-s^2) - s*c >= 0.
        upper=lam_hi*r*r+sh*radical_hi-sl*cl
        require(upper<0,f'area exclusion FAILED for B={B}')
        rows.append({'B':B,'reason':'joint-area exclusion','margin':encode(-upper)})
    area_rows=[x for x in rows if x['reason']=='joint-area exclusion']
    minimum=min(area_rows,key=lambda x:F(*x['margin']))
    require(len(rows)==97 and [x['B'] for x in rows]==list(range(3,100)),
            'incomplete boundary-count enumeration')
    return {'status':'PASS','claim':'r_D(100) > radius',
            'radius':encode(r),'kappa':encode(kappa),
            'pi_enclosure':[encode(pi_lo),encode(pi_hi)],
            'joint_lemma_margins':{str(q):encode(v) for q,v in margins.items()},
            'counts':{'all_B':len(rows),'arc_excluded':len(rows)-len(area_rows),
                      'area_excluded':len(area_rows)},
            'tightest_area_case':minimum,'cases':rows,
            'scope':'All center configurations via the written geometric reduction; not an exact optimality proof.'}

def main():
    result=verify()
    path=HERE/'lower_verification_result.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: exact joint triangle-area inequalities for q=0,1,2,3.')
    print('PASS: all boundary counts B=3,...,99 exhausted.')
    print('PASS: B=1,2 excluded analytically by arc length (r<1).')
    print('Arc-count exclusions:',result['counts']['arc_excluded'])
    print('Joint-area exclusions:',result['counts']['area_excluded'])
    print('Tightest surviving boundary count:',result['tightest_area_case']['B'])
    print('Exact positive margin:',F(*result['tightest_area_case']['margin']))
    print('CERTIFIED UNIVERSAL LOWER BOUND:',R0,'< r_D(100)')
    print('NOT CERTIFIED: the exact optimal radius or a matching upper construction.')

if __name__=='__main__':main()
