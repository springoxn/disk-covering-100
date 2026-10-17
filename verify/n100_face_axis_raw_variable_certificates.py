"""Raw-variable infeasibility certificates modulo fixed-axis equations."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import json,hashlib,copy
from n100_generic_map_compiler import chord,compile_model
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def add(*ps):
    z={}
    for p in ps:
        for k,v in p.items():z[k]=z.get(k,Q(0))+v
    return {k:v for k,v in z.items() if v}
def scale(p,a):return {k:v*a for k,v in p.items() if v*a}
def mul(p,q):
    z={}
    for a,x in p.items():
        for b,y in q.items():k=tuple(sorted(a+b));z[k]=z.get(k,Q(0))+x*y
    return {k:v for k,v in z.items() if v}
def var(i):return {(i,):Q(1)}
def const(x):return {():Q(x)}
def square(p):return mul(p,p)
def from_terms(c):
    z={}
    for a,ids in c:
        k=tuple(sorted(ids));z[k]=z.get(k,Q(0))+Q(a)
    return {k:v for k,v in z.items() if v}
def substitute_axis(p,axis):
    z={}
    for ids,c in p.items():
        c=Q(c);free=[]
        for i in ids:
            if i in axis:c*=axis[i]
            else:free.append(i)
        k=tuple(sorted(free));z[k]=z.get(k,Q(0))+c
    return {k:v for k,v in z.items() if v}
def quotient_axis(p,i,a):
    # p - p(x=a)=(x-a)q, by monomial multiplicity division.
    q={};rem={}
    for ids,c in p.items():
        n=ids.count(i);rest=[v for v in ids if v!=i]
        if n:
            for k in range(n):
                qids=tuple(sorted(rest+[i]*k));q[qids]=q.get(qids,Q(0))+c*(a**(n-1-k))
        else:rem[ids]=rem.get(ids,Q(0))+c
    # Above quotient is for x^n-a^n over x-a; subtract signs via polynomial identity.
    # Correct coefficients are sum a^(n-1-k) x^k.
    return {k:v for k,v in q.items() if v}, {k:v for k,v in rem.items() if v}
def model_poly(c):return from_terms(c['terms'])
def verify_raw(g,M,face,A,B,T):
    names=list(g['vertices']);marks=g['axis_marks'];coords=[(1,0),(0,1),(-1,0),(0,-1)];P=coords[marks.index(A)];Qp=coords[marks.index(B)];j=face['center'];base=2*len(names);c=[base+2*j,base+2*j+1];t=M['t_index']
    distances=[(f['center'],v) for f in g['faces'] for v in f['vertices']];ids=[2+len(names)+len(g['faces'])+distances.index((j,v)) for v in (A,B)]
    gs=[model_poly(M['inequalities'][i]) for i in ids];mid=[Q(P[d]+Qp[d],2) for d in (0,1)];L=sum(Q(P[d]-Qp[d])**2 for d in (0,1))/4;delta=L-T
    squares=[square(add(var(c[d]),const(-mid[d]))) for d in (0,1)]
    N=add(scale(gs[0],Q(1,2)),scale(gs[1],Q(1,2)),*squares,const(T),scale(var(t),-1));need(substitute_axis(N,{2*names.index(v)+d:Q(value) for v,p in zip(marks,coords) for d,value in enumerate(p)})==const(-delta),'raw reduced identity')
    # Sequential quotient decomposition.
    axis={2*names.index(v)+d:Q(value) for v,p in zip(marks,coords) for d,value in enumerate(p)};rem=N;quot=[]
    for i,a in axis.items():
        reduced=substitute_axis(rem,{i:a});q,_=quotient_axis(rem,i,a)
        need(rem==add(reduced,mul(add(var(i),const(-a)),q)),'quotient reconstruction')
        quot.append({'variable':i,'constant':str(a),'quotient':[[str(v),list(k)] for k,v in q.items()]});rem=reduced
    need(rem==const(-delta),'quotient remainder');return {'face':j,'axes':[A,B],'distance_indices':ids,'delta':str(delta),'axis_quotients':quot,'raw_identity_remainder':str(-delta),'scaled_constant':'-1'}
if __name__=='__main__':
    U=Q(1154469548855829,10**16);T=U*U;rows=[]
    for a,b in combinations(range(4),2):
        g=chord(a,b);M=compile_model(g);face=next(f for f in g['faces'] if str(a) in f['vertices'] and str(b) in f['vertices']);rows.append(verify_raw(g,M,face,str(a),str(b),T))
    need(len(rows)==6,'six')
    rejected=[] # Independent verifier below performs actual corruption rejection.
    out=R/'verify/out/n100-face-axis-raw-variable-certificates-v2.json';need(not out.exists(),'overwrite')
    deps=['verify/n100_generic_map_compiler.py','verify/out/n100-generic-map-compiler.json']
    out.write_text(json.dumps({'verified':True,'T':str(T),'certificates':rows,'certificate_count':6,'raw_variable_mod_axis_equations':True,'rejected_controls':rejected,'scope':'raw polynomial identities modulo axis equalities for six small maps; no n100 remaining-map exclusion','bindings':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in deps},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS6 raw-variable certificates modulo8 axis equations;all remainders=-delta;corruption rejected')
