#!/usr/bin/env python3
"""Unpenalized B31 exclusion after unit-disk projection, with global degree-five flags."""
from pathlib import Path
from fractions import Fraction as F
import itertools,json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'lower_bounds_extension_20261004'))
import verify_extension as geometry
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_range_one_face_support import face_bound
from exact_quadratic_marked_conjugate import conjugate
from verify_jensen_slab_ear_support import quadratic_cap
from verify_global_star_anchor_degree_window import verify as check_window
from verify_one_positive_curvature_isoperimetry import verify as check_weighted
R=F(113231,1000000);B=31;I=69;A=3*q(3).sqrt()/4;ANG=PI/3

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    geometry.R=R;geometry.check_kappa();geometry.check_concavity_factorization()
    n99=geometry.exclude_all(99,R)
    footprint=geometry.cluster_exclusion(B,5,F(6933,10000),3,F(1,1000))
    old=((198-B)*geometry.AH+B*geometry.KAPPA)*R*R+B*geometry.H_upper(R,2*geometry.PL/B,2*geometry.PH/B)
    budget=(old-geometry.PL)/(R*R)
    window=check_window();assert window['status']=='PASS'
    assert I>1 and budget<F(window['degree4_loss_lower'])
    assert window['minimum_interior_degree']==5 and window['maximum_interior_degree']==8
    # /6 on the entire disk forces at least one degree-five interior site.
    assert 6*(198-B)>B*B
    # If there were at most one degree-five site, /5 applies blockwise
    # to the induced core. For M<=23 it contradicts Fcore>=136-M.
    assert check_weighted()['status']=='PASS' and 5*(2*I-2-23)>23*23
    rows=json.loads((ROOT/'B31_global_low_degree_0p11323_proposals.json').read_text())
    assert rows['radius']==str(R) and rows['B']==B
    assert [(z['M'],z['required_degree_five_count']) for z in rows['rows']]==[(23,2),(24,1)]
    triples=list(itertools.combinations_with_replacement(range(4),3));assert len(triples)==20
    mu=PI/B;s=sine(mu);Q=B*(mu-s*(cosine(mu)-(q(R).sq()-s.sq()).sqrt()))
    C0=conjugate(F(0),F(0));reports=[];minimum=None;face_count=vertex_count=0
    for row in rows['rows']:
        M=row['M'];required=row['required_degree_five_count'];D=row['denominator'];P=row['potential_denominator']
        labels=[F(row['high_potential'],P),F(row['boundary_potential'],P),F(0),F(row['low_potential'],P)]
        charges=[F(row[k],D) for k in ('charge_a','charge_b','charge_0','charge_low')]
        tau={0:F(row['interface_a'],D),2:F(row['interface_0'],D),3:F(row['interface_low'],D)}
        assert max(labels)-min(labels)<1 and min(tau.values())>=0
        assert [tuple(z['indices']) for z in row['faces']]==triples
        fmin=None
        for cell in row['faces']:
            ids=cell['indices'];val,_,_=face_bound([labels[i] for i in ids],F(cell['nu'],D))
            credit=sum(t*sum({ids[j],ids[(j+1)%3]}=={ix,1} for j in range(3)) for ix,t in tau.items())
            gap=(A+q(sum((charges[i] for i in ids),F(0))-credit)).l-val.u
            assert gap>0,('face',M,ids,F(gap,S));fmin=gap if fmin is None else min(fmin,gap);face_count+=1
        u0,beta,eta,apex,flag=[q(F(row[k],D)) for k in ('u0','beta','eta','apex','flag')]
        assert min(apex.l,flag.l)>=0;lb=-labels[1];vmin=None
        for p in range(4):
            for d in range(5,9):
                ix=3 if d==5 else 2 if d==6 else 0;lv=labels[ix]
                val=p*(conjugate(F(0),lv+lb)-C0)-q(lv)*(6-d+p)*ANG+(d-p)*q(charges[ix])
                if p:val-=2*q(tau[ix])
                upper=u0+p*beta+(d-6)*eta+(apex if p else q(0))-(flag if d==5 else q(0))
                gap=upper.l-val.u;assert gap>0,('vertex',M,p,d,F(gap,S))
                vmin=gap if vmin is None else min(vmin,gap);vertex_count+=1
        slope=-eta+apex+q(charges[1])-q(lb)*ANG
        assert slope.l>0 if M==23 else slope.u<0
        ear=A-2*C0+quadratic_cap(R,F(0))-2*beta+eta+q(lb)*PI+2*slope
        width=q(2)/(q(1)+(q(1)-2*q(R)).sqrt())
        bad=width+q(F(1,2))-C0-beta-eta
        assert ear.u<0 and bad.u<0
        center=(198-2*B)*A+B*C0+I*u0+B*beta+(B-6-M)*eta+M*apex+M*q(charges[1])-required*flag-q(lb)*(2*PI+M*ANG)
        margin=PI-q(R).sq()*center-Q;assert margin.l>0
        minimum=margin.l if minimum is None else min(minimum,margin.l)
        reports.append(dict(M_endpoint=M,required_degree_five_count=required,
            M_slope_lower=str(F(slope.l,S)),M_slope_upper=str(F(slope.u,S)),
            shifted_ear_upper=str(F(ear.u,S)),bad_q1_upper=str(F(bad.u,S)),
            minimum_face_slack=str(F(fmin,S)),minimum_vertex_slack=str(F(vmin,S)),
            area_margin=str(F(margin.l,S))))
    assert (face_count,vertex_count)==(40,32)
    return dict(status='PASS',radius=str(R),B=B,m=100,
        scope='Complete B31 branch after unit-disk projection before classification; other counts and exact optimality remain separate',
        required_center_norm_squared_upper='1',center_projection_precedes_classification=True,
        n99_exclusion=n99,ordinary_marked_incidence_upper=3,footprint=footprint,
        degree_window=[5,8],old_normalized_loss_upper=str(budget),
        global_degree_five_requirement=1,degree_five_requirement_for_M_le23=2,
        all_twenty_face_label_multisets_allowed=True,deep_label_assumption=False,
        reflected_center_hypothesis=False,squared_edge_penalty='0',halfside_multiplier='0',
        arbitrary_ears_and_bad_faces_allowed=True,face_supports=face_count,vertex_supports=vertex_count,
        minimum_area_margin=str(F(minimum,S)),branches=reports)

if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
