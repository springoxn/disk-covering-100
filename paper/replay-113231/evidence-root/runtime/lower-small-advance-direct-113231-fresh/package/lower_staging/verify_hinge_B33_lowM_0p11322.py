#!/usr/bin/env python3
"""Exact normalized B33 exclusion for M<=25 using hinge charges."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,itertools,hashlib
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'lower_bounds_extension_20261004'))
import verify_extension as geometry
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_linear_halfside_marked_conjugate import conjugate,verify as check_marked
from exact_range_one_face_support import face_bound,verify as check_faces
from verify_jensen_slab_ear_support import cap as ear_cap
from verify_global_star_anchor_degree_window import verify as check_degrees
from verify_unmarked_low_degree_core_obstruction import verify as check_core
from verify_one_positive_curvature_isoperimetry import verify as check_weighted
import verify_B33_marked_hinge_charges_0p11322 as hinge
R=F(5661,50000);B=33;K=F(11,25);A=3*q(3).sqrt()/4;ANG=PI/3

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    geometry.R=R;geometry.check_kappa();geometry.check_concavity_factorization()
    n99=geometry.exclude_all(99,R)
    old=((198-B)*geometry.AH+B*geometry.KAPPA)*R*R+B*geometry.H_upper(R,2*geometry.PL/B,2*geometry.PH/B)
    deficit=(old-geometry.PL)/(R*R)
    degree=check_degrees();degree_margin=F(degree['degree4_loss_lower'])-deficit
    assert degree_margin>0 and 100-B>1
    coregap=geometry.PL*(111*geometry.AL-deficit)-441;assert coregap>0
    assert next(z for z in check_core()['cases'] if z['B']==B)['U_upper']==25
    assert next(z for z in check_weighted()['cases'] if z['B']==B)['M_upper']==23
    assert check_marked()['status']==check_faces()['status']=='PASS'
    support=hinge.verify()
    assert support['status']=='PASS' and support['radius']==str(R) and support['B']==B
    assert F(support['halfside_multiplier'])==K
    assert F(support['required_center_norm_squared_upper'])==1-R*R
    rr=q(R);mu=PI/B;s=sine(mu);rho=cosine(mu)-(rr.sq()-s.sq()).sqrt()
    Q=B*(mu-s*rho+q(K)*rr*s*rho)
    C0=conjugate(K,F(0));data_path=ROOT/'hinge_B33_lowM_0p11322_proposals.json'
    data=json.loads(data_path.read_text())
    assert data['radius']==str(R) and data['B']==B
    assert [z['branch'] for z in data['rows']]==['M22_23','M24_profile','M24_isolated','M25']
    general=[t for t in itertools.combinations_with_replacement(range(4),3) if not(1 in t and 3 in t)]
    isolated=[t for t in general if 3 not in t or t==(2,2,3)]
    assert len(general)==16 and len(isolated)==11
    totals=[0,0];results=[];accepted=[]
    def row_bounds(row):
        M=row['M'];need=row['deep_witnesses'];special=row['branch']=='M24_isolated'
        den=row['denominator'];pd=row['potential_denominator']
        assert den==10**10 and pd==10**8
        labels=[F(row['high_potential'],pd),F(row['boundary_potential'],pd),F(0),F(row['deep_potential'],pd)]
        charges=[F(row[k],den) for k in('charge_a','charge_b','charge_0','charge_deep')]
        ta=F(row['interface_a'],den);tz=F(row['interface_0'],den)
        assert min(ta,tz)>=0 and row['interface_deep']==0
        expected=isolated if special else general
        assert [tuple(c['indices']) for c in row['faces']]==expected
        face_min=None
        for cell in row['faces']:
            ids=cell['indices'];ls=[labels[i] for i in ids];assert max(ls)-min(ls)<1
            cap,acute,vertex=face_bound(ls,F(cell['nu'],den))
            credit=sum(tau*sum({ids[j],ids[(j+1)%3]}=={lab,1} for j in range(3))
                       for lab,tau in((0,ta),(2,tz)))
            upper=A+q(sum((charges[i] for i in ids),F(0))-credit)
            gap=upper.l-cap.u;assert gap>0,('face',row['branch'],ids,F(gap,S))
            face_min=gap if face_min is None else min(face_min,gap);totals[0]+=1
        u0,beta,eta,apex,flag=[q(F(row[k],den)) for k in('u0','beta','eta','apex','flag')]
        assert min(u0.l,apex.l,flag.l)>=0
        types=[]
        for d in range(5,9):
            for p in range(d):
                if d==5:
                    if p==0:types.append((p,d,3))
                    if not special:types.append((p,d,2))
                else:types.append((p,d,0 if d>=7 else 2))
        assert len(types)==(22 if special else 27)
        gaps={};lb=-labels[1]
        for p,d,ix in types:
            lv=labels[ix]
            score=p*(conjugate(K,lv+lb)-C0)-q(lv)*(6-d+p)*ANG+(d-p)*q(charges[ix])-q(hinge.charge(p))
            if p:score-=q(2*(ta if ix==0 else tz))
            upper=u0+p*beta+(d-6)*eta+(apex if p else q(0))
            if ix==3:upper-=flag
            gap=upper.l-score.u;assert gap>0,('vertex',row['branch'],p,d,ix,F(gap,S))
            gaps[p,d,ix]=F(gap,S);totals[1]+=1
        slope=-eta+apex+q(charges[1])-q(lb)*ANG;assert slope.u<0
        shifted=A-2*C0+ear_cap(R,K)-2*beta+eta+q(lb)*PI+2*slope
        width=q(2)/(1+(1-2*rr).sqrt());y=(q(K)+q(K*K+8).sqrt())/4
        bad=width+(1-y.sq()).sqrt()*(y-q(K))-C0-beta-eta
        assert shifted.u<0 and bad.u<0
        center=132*A+B*C0+67*u0+B*beta+(27-M)*eta+M*apex-need*flag+M*q(charges[1])-q(lb)*(2*PI+M*ANG)
        margin=PI-(rr.sq()*center+Q)
        report=dict(branch=row['branch'],M=M,deep_witnesses=need,faces=len(expected),vertices=len(types),
            minimum_face_slack=str(F(face_min,S)),minimum_vertex_slack=str(min(gaps.values())),
            M_slope_upper=str(F(slope.u,S)),shifted_ear_upper=str(F(shifted.u,S)),
            bad_q1_upper=str(F(bad.u,S)),ordinary_area_margin=str(F(margin.l,S)))
        return report,margin,gaps
    row,margin,gaps=row_bounds(data['rows'][0]);assert (row['M'],row['deep_witnesses'])==(22,2) and margin.l>0
    row['covered_M']=[22,23];results.append(row);accepted.append(margin.l)
    row,margin,gaps=row_bounds(data['rows'][1]);assert (row['M'],row['deep_witnesses'])==(24,1)
    # Choose exactly one guaranteed deep5 for the positive label. Every
    # additional degree5 is neutral, including additional deep ones.
    extra=min(v for(p,d,ix),v in gaps.items() if d==5 and ix==2)
    unique_margin=margin+rr.sq()*q(extra);assert unique_margin.l>0
    row['extra_degree5_slack']=str(extra);row['unique_global_five_margin']=str(F(unique_margin.l,S))
    results.append(row);accepted.append(unique_margin.l)
    # The audited isolated-five M24 topology, with I67, is exact and
    # allows ears and bad faces through the shifted-core identities.
    assert 5*110>20**2 and 5*109>23**2
    assert 5*108>22**2 and 5*108>3**2+21**2 and 5*108>3**2+23**2
    assert F(24+18)+F(18**2,5)<108
    assert F(24+19)+F(19**2,6)<108
    row,margin,gaps=row_bounds(data['rows'][2]);assert margin.l>0
    row['premise']='Exactly one global degree5; isolated-five core forces all five positive faces to(P,0,0)'
    results.append(row);accepted.append(margin.l)
    row,margin,gaps=row_bounds(data['rows'][3]);assert (row['M'],row['deep_witnesses'])==(25,1) and margin.l>0
    results.append(row);accepted.append(margin.l)
    assert totals==[59,103]
    return dict(status='PASS',radius=str(R),B=B,m=100,M_domain='M<=25',
        scope='Complete low-M B33 branch only after whole-cover normalization; M>=26 and other B are separate',
        required_center_norm_squared_upper=str(1-R*R),proposal_sha256=hashlib.sha256(data_path.read_bytes()).hexdigest(),
        n99_exclusion=n99,minimum_M=22,core_cut_margin=str(coregap),
        global_degree_window=[5,8],global_degree_window_margin=str(degree_margin),
        hinge_allocation=support,qmax_footprint_premise=False,
        face_supports=totals[0],vertex_supports=totals[1],arbitrary_ears=True,arbitrary_bad_q1=True,
        minimum_area_margin=str(F(min(accepted),S)),branches=results)
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
