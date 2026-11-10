#!/usr/bin/env python3
"""Exact all-degree5 contradiction row; no low-vertex location is assumed."""
from pathlib import Path
from fractions import Fraction as F
import sys,itertools,json,hashlib
ROOT=Path(__file__).resolve().parent
BASE=ROOT if (ROOT/'verify_star_lp_duals.py').exists() else ROOT.parent/'working'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/'lower_bounds_extension_20261004'))
import verify_extension as geometry
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_linear_halfside_marked_conjugate import conjugate
from exact_range_one_face_support import face_bound
from verify_jensen_slab_ear_support import cap as ear_cap
from verify_global_star_anchor_degree_window import verify as degree_check
import verify_exact_lens_boundary_0p11322 as whole
import verify_exact_lens_hinge_deficit as local
R=F(113231,1000000);K=F(11,25);T=F(23,250);C=F(3,100);SPAN=F(3467,5000)
A=3*q(3).sqrt()/4;ANG=PI/3
def charge(p):return C*max(F(0),(p+1)*T-SPAN/2)/(2*R*R)
def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    geometry.R=R;geometry.check_kappa();geometry.check_concavity_factorization();n99=geometry.exclude_all(99,R)
    old=((198-33)*geometry.AH+33*geometry.KAPPA)*R*R+33*geometry.H_upper(R,2*geometry.PL/33,2*geometry.PH/33)
    deficit=(old-geometry.PL)/(R*R);degree=degree_check()
    degree_margin=F(degree['degree4_loss_lower'])-deficit;assert degree_margin>0
    for v in(whole,local):v.R=R;v.B=33;v.K=K;v.CURVATURE=F(0)
    local.CUTOFF=T;local.SLOPE=C
    global_result=whole.verify();hinge=local.verify()
    footprint=sine(q(SPAN/2))-q(3*R);assert footprint.l>0
    data_path=ROOT/'B33_highM_any_five_0p11323_proposal.json';data=json.loads(data_path.read_text())
    assert data['radius']==str(R) and data['B']==33
    row=data['row'];D=row['denominator'];P=row['potential_denominator'];assert D==10**10 and P==10**8
    labels=[F(row['high_potential'],P),F(row['boundary_potential'],P),F(0),F(row['low_potential'],P)]
    charges=[F(row[k],D) for k in('charge_a','charge_b','charge_0','charge_low')]
    taus=[F(row[k],D) for k in('interface_a','interface_0','interface_low')]
    assert min(taus)>=0
    expected=list(itertools.combinations_with_replacement(range(4),3))
    assert [tuple(x['indices']) for x in row['faces']]==expected and len(expected)==20
    facegaps=[]
    for cell in row['faces']:
        ids=cell['indices'];cap,_,_=face_bound([labels[i] for i in ids],F(cell['nu'],D))
        credit=sum(tau*sum({ids[j],ids[(j+1)%3]}=={lab,1} for j in range(3)) for lab,tau in zip((0,2,3),taus))
        upper=A+q(sum((charges[i] for i in ids),F(0))-credit)
        gap=F(upper.l-cap.u,S);assert gap>0;facegaps.append(gap)
    u0,beta,eta,apex,flag=[q(F(row[k],D)) for k in('u0','beta','eta','apex','flag')]
    assert min(u0.l,apex.l,flag.l)>=0 and flag.l>0
    C0=conjugate(K,F(0));lb=-labels[1];vertexgaps=[]
    for d in range(5,9):
        for p in range(d):
            ix=3 if d==5 else 2 if d==6 else 0;lv=labels[ix]
            score=p*(conjugate(K,lv+lb)-C0)-q(lv)*(6-d+p)*ANG+(d-p)*q(charges[ix])-q(charge(p))
            if p:score-=q(2*taus[{0:0,2:1,3:2}[ix]])
            upper=u0+p*beta+(d-6)*eta+(apex if p else q(0))-(flag if d==5 else q(0))
            gap=F(upper.l-score.u,S);assert gap>0,('vertex',p,d,gap);vertexgaps.append(gap)
    slope=-eta+apex+q(charges[1])-q(lb)*ANG;assert slope.u<0
    shifted=A-2*C0+ear_cap(R,K)-2*beta+eta+q(lb)*PI+2*slope
    rr=q(R);w=q(2)/(1+(1-2*rr).sqrt());y=(q(K)+q(K*K+8).sqrt())/4
    bad=w+(1-y.sq()).sqrt()*(y-q(K))-C0-beta-eta
    assert shifted.u<0 and bad.u<0
    mu=PI/33;s=sine(mu);rho=cosine(mu)-(rr.sq()-s.sq()).sqrt()
    Q=33*(mu-s*rho+q(K)*rr*s*rho)
    center=132*A+33*C0+67*u0+33*beta+eta+26*apex-flag+26*q(charges[1])-q(lb)*(2*PI+26*ANG)
    margin=PI-(rr.sq()*center+Q);assert margin.l>0
    return dict(status='PASS',radius=str(R),B=33,m=100,M_domain='M>=26',
        scope='Every interior degree is at least six; ears and bad q1 are not yet excluded',
        required_center_norm_squared_upper=str(1-R*R),n99_exclusion=n99,
        initial_degree_window=[5,8],initial_degree_window_margin=str(degree_margin),
        assumed_contradiction='At least one original interior degree5; all degree5 vertices receive the positive label',
        low_vertex_boundary_adjacency_allowed=True,face_supports=20,vertex_supports=26,
        minimum_face_slack=str(min(facegaps)),minimum_vertex_slack=str(min(vertexgaps)),
        M_slope_upper=str(F(slope.u,S)),shifted_ear_upper=str(F(shifted.u,S)),bad_q1_upper=str(F(bad.u,S)),
        degree5_contradiction_margin=str(F(margin.l,S)),
        proposal_sha256=hashlib.sha256(data_path.read_bytes()).hexdigest(),
        hinge_slope=str(C),hinge_zero=str(T),hinge_scalar_margin=hinge['minimum_bad_arc_margin'],
        remaining_Euler_cases=[dict(M=26,ears=0,bad_q1=0,degree_excess=1),dict(M=26,ears=1,bad_q1=0,degree_excess=0),
            dict(M=26,ears=0,bad_q1=1,degree_excess=0),dict(M=27,ears=0,bad_q1=0,degree_excess=0)])
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
