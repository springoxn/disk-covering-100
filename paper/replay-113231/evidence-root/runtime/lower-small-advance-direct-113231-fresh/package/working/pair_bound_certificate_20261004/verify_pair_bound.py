"""Exploratory exact fixed-point enclosure for the boundary-pair relaxation.

Own implementation. A successful exhaustive run is a scalar-inequality
certificate only; the accompanying geometry must also be audited.
"""
from fractions import Fraction as Q
from math import isqrt, comb
from functools import lru_cache
import time, heapq, json

D=10**15
A_UP=Q(129903810568,10**11)
KAPPA=Q(17999,50000)  # 0.35998
def ci(q):
    q=Q(q); return (q.numerator*D//q.denominator, -((-q.numerator*D)//q.denominator))
ZERO=(0,0); ONE=(D,D); R=ci(Q(113,1000)); R2=ci(Q(12769,10**6)); LAM=ci(Q(1,25))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[1],-a[0])
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    z=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]);return (min(z)//D,-((-max(z))//D))
def scal(a,n):return (a[0]*n,a[1]*n) if n>=0 else (a[1]*n,a[0]*n)
def half(a):return (a[0]//2,-((-a[1])//2))
def sq(a):
    lo=0 if a[0]<=0<=a[1] else min(a[0]**2,a[1]**2)
    hi=max(a[0]**2,a[1]**2)
    return (lo//D,-((-hi)//D))
def ab(a):return (0 if a[0]<=0<=a[1] else min(abs(a[0]),abs(a[1])), max(abs(a[0]),abs(a[1])))
def sqrt(a):
    assert a[1]>=0
    lo=isqrt(max(0,a[0])*D); n=a[1]*D;hi=isqrt(n)
    if hi*hi<n:hi+=1
    return lo,hi
def dot(a,b):return add(mul(a[0],b[0]),mul(a[1],b[1]))
def vs(a,b):return sub(a[0],b[0]),sub(a[1],b[1])
def vm(a,s):return mul(a[0],s),mul(a[1],s)
def va(a,b):return add(a[0],b[0]),add(a[1],b[1])
@lru_cache(None)
def asin_at(t):
    z=Q(t,D); val=sum((Q(comb(2*k,k),4**k*(2*k+1))*z**(2*k+1) for k in range(10)),Q(0))
    tail=z**21/(1-z*z)
    return ci(val)[0],ci(val+tail)[1]
def asin(a):return asin_at(a[0])[0],asin_at(a[1])[1]
def state(x,sign):
    s=mul(R,x);c=sqrt(sub(ONE,sq(s)));h=mul(R,sqrt(sub(ONE,sq(x))));rho=sub(c,h)
    u=(c,scal(s,sign));v=(scal(s,-sign),c)
    center=vm(u,rho);H=sub(asin(s),mul(s,rho))
    return s,h,u,v,center,H
def support(w,s,h,u,v):
    wr=dot(w,u);wt=ab(dot(w,v))
    # The inward corner is the exact maximizer in this normal cone.
    if wr[1]<=0 and mul(wt,h)[1] <= mul(neg(wr),s)[0]:return ZERO
    norm=sqrt(add(sq(w[0]),sq(w[1])))
    # Unconstrained circular support is an upper bound for either arc branch.
    val=add(sub(mul(wr,h),mul(wt,s)),mul(R,norm))
    return (0,max(0,val[1]))
def bound(box,mu):
    x=(box[0],box[1]);y=(box[2],box[3])
    s,h,u,v,c,H=state(x,-1);S,j,U,V,C,J=state(y,1);d=vs(c,C)
    w=va(vm(d,scal(LAM,2)),vm(u,sub(mul(scal(LAM,4),h),half(s))))
    W=va(vm(d,scal(LAM,-2)),vm(U,sub(mul(scal(LAM,4),j),half(S))))
    val=add(mul(LAM,add(sq(d[0]),sq(d[1]))),half(add(H,J)))
    val=add(val,add(support(w,s,h,u,v),support(W,S,j,U,V)))
    return sub(val,mul(mu,half(add(asin(s),asin(S)))))[1]
def run(B,limit_seconds=3600):
    pars={33:(Q(-37951627,10**9),Q(11270,10**6)),34:(Q(-19173670,10**9),Q(9530,10**6)),35:(Q(-4281108,10**9),Q(8200,10**6))}
    mu,target=pars[B];M=ci(mu);T=ci(target)[0]
    # Symmetry allows x <= y; straddling diagonal boxes are kept whole.
    todo=[(0,D,0,D)];visited=accepted=0;max_depth=0;start=time.time();last=start
    while todo:
        box=todo.pop();visited+=1
        if box[0]>box[3]:continue
        hi=bound(box,M)
        if hi<=T:accepted+=1;continue
        widths=(box[1]-box[0],box[3]-box[2]);axis=0 if widths[0]>=widths[1] else 2
        mid=(box[axis]+box[axis+1])//2
        if mid in (box[axis],box[axis+1]):raise RuntimeError('Unresolved fixed-point box')
        left=list(box);right=list(box);left[axis+1]=mid;right[axis]=mid
        todo.extend((tuple(left),tuple(right)))
        now=time.time()
        if now-last>10:
            print(json.dumps(dict(B=B,visited=visited,accepted=accepted,pending=len(todo),seconds=now-start,cache=asin_at.cache_info().currsize)),flush=True);last=now
        if now-start>limit_seconds:
            return dict(B=B,status='PENDING',visited=visited,accepted=accepted,pending=len(todo),seconds=now-start)
    return dict(B=B,status='PASS',mu=str(mu),target=str(target),visited=visited,accepted=accepted,seconds=time.time()-start)
def triangle_checks():
    assert A_UP*A_UP>Q(27,16)
    def val(q,x):
        if q==1:
            return sub(mul(x,add(ONE,scal(sqrt(sub(ONE,sq(x))),2))),mul(ci(Q(4,25)),sq(x)))
        if q==2:
            root=sqrt(sub(scal(x,2),sq(x)))
            if x[1]<=D:return sub(add(x,root),mul(ci(Q(4,25)),x))
            assert x[0]>=D
            return sub(mul(add(x,ONE),root),mul(ci(Q(4,25)),x))
        return add(mul(ci(4*A_UP/9-Q(4,25)),x),sqrt(sub(scal(x,3),sq(x))))
    out=[]
    for q,initial in [(1,[(0,D)]),(2,[(0,D),(D,2*D)]),(3,[(0,3*D)])]:
        todo=initial[:];count=0;target=ci(A_UP+q*KAPPA)[0]
        while todo:
            x=todo.pop();count+=1
            if val(q,x)[1]<=target:continue
            mid=sum(x)//2
            assert x[0]<mid<x[1]
            todo.extend([(x[0],mid),(mid,x[1])])
        out.append(dict(marked_sides=q,status='PASS',boxes=count))
    return out
def global_margins():
    def atan_bounds(q,N):
        x=Q(1,q);v=sum(((-1)**k*x**(2*k+1)/Q(2*k+1) for k in range(N)),Q(0));e=(-1)**N*x**(2*N+1)/Q(2*N+1)
        return min(v,v+e),max(v,v+e)
    a,b=atan_bounds(5,40);c,d=atan_bounds(239,12);pi_lo=16*a-4*d
    pars={33:(Q(-37951627,10**9),Q(11270,10**6)),34:(Q(-19173670,10**9),Q(9530,10**6)),35:(Q(-4281108,10**9),Q(8200,10**6))}
    out=[]
    for B,(mu,L) in pars.items():
        margin=(1-mu)*pi_lo-((198-B)*A_UP+B*KAPPA)*Q(12769,10**6)-B*L
        assert margin>0
        out.append(dict(B=B,status='PASS',exact_margin_lower=str(margin),margin_decimal=float(margin)))
    return out
def remaining_counts():
    from math import factorial
    def atan_bounds(q,N):
        x=Q(1,q);v=sum(((-1)**k*x**(2*k+1)/Q(2*k+1) for k in range(N)),Q(0));e=(-1)**N*x**(2*N+1)/Q(2*N+1)
        return min(v,v+e),max(v,v+e)
    a,b=atan_bounds(5,40);c,d=atan_bounds(239,12);pl,ph=16*a-4*d,16*b-4*c
    def trig_at(x,is_cos):
        powers=(2*k if is_cos else 2*k+1 for k in range(16))
        val=sum(((-1)**k*x**p/Q(factorial(p)) for k,p in enumerate(powers)),Q(0))
        p=32 if is_cos else 33;err=x**p/Q(factorial(p))
        return val-err,val+err
    oldA=sqrt(ci(Q(27,16)));oldK=ci(Q(461134488,10**9));radius=Q(113,1000)
    root3=sqrt(ci(3));root33=sqrt(ci(33))
    G1=sqrt(mul(add(ci(207),scal(root33,33)),ci(Q(1,128))))
    G2=half(sqrt(add(ci(9),scal(root3,6))))
    old_margins=[sub(add(oldA,oldK),G1)[0],
                 sub(add(oldA,scal(oldK,2)),G2)[0],
                 sub(scal(oldK,3),oldA)[0]]
    assert all(z>0 for z in old_margins)
    survivors=[];rows=[]
    for B in range(3,100):
        sl=trig_at(pl/B,False)[0];sh=trig_at(ph/B,False)[1]
        cl=trig_at(ph/B,True)[0];ch=trig_at(pl/B,True)[1]
        si=(ci(sl)[0],ci(sh)[1]);co=(ci(cl)[0],ci(ch)[1])
        if si[0]>R[1]:rows.append((B,'arc'));continue
        assert si[1]<R[0]
        coeff=add(mul(ci(Q(198,B)-1),oldA),oldK)
        value=sub(add(mul(coeff,R2),mul(si,sqrt(sub(R2,sq(si))))),mul(si,co))
        if value[1]<0:rows.append((B,'area'))
        else:
            assert value[0]>0
            survivors.append(B);rows.append((B,'pair bound required'))
    assert survivors==[33,34,35]
    return dict(status='PASS',counts_checked=len(rows),survivors=survivors,rows=rows,
                old_kappa_margin_numerators=old_margins,margin_denominator=D)
if __name__=='__main__':
    import sys
    if not __debug__:
        raise RuntimeError('Run with assertions enabled; optimized Python is not accepted')
    if sys.argv[1]=='final':
        print(json.dumps(dict(triangle_checks=triangle_checks(),global_margins=global_margins())),flush=True)
    elif sys.argv[1]=='all':
        result=dict(scope='Universal lower bound r_D(100)>113/1000; not exact optimality',remaining_counts=remaining_counts(),triangle_checks=triangle_checks())
        result['pair_bounds']=[run(B) for B in [33,34,35]]
        if not all(x['status']=='PASS' for x in result['pair_bounds']):
            raise RuntimeError('Pair proof remains incomplete')
        result['global_margins']=global_margins()
        result['status']='PASS'
        print(json.dumps(result),flush=True)
    elif sys.argv[1]=='remaining':
        print(json.dumps(remaining_counts()),flush=True)
    else:
        print(json.dumps(run(int(sys.argv[1]),float(sys.argv[2]) if len(sys.argv)>2 else 3600)),flush=True)
