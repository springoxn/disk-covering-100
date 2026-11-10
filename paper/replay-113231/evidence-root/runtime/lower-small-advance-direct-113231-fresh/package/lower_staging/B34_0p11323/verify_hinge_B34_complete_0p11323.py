#!/usr/bin/env python3
"""Complete normalized B34 .11323 branch using a single exact-lens q4 hinge allocation."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,itertools
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]/"working"
sys.path.insert(0,str(ROOT))
from verify_star_lp_duals import q,S,PI
from exact_linear_halfside_marked_conjugate import conjugate,verify as check_conjugate
from exact_range_one_face_support import face_bound,verify as check_faces
from verify_jensen_slab_ear_support import cap as ear_cap
from verify_potential_star_duals import sine,cosine
from verify_unmarked_low_degree_core_obstruction import verify as check_core
from verify_one_positive_curvature_isoperimetry import verify as check_weighted
sys.path.insert(0,str(ROOT/'lower_bounds_extension_20261004'))
import verify_extension as geometry
import verify_exact_lens_boundary_0p11322 as boundary
import verify_B34_q4_hinge_charge_0p11323 as hinge
R=F(113231,1000000);B=34;K=F(1,2);PAID=F(1,50);A=3*q(3).sqrt()/4;ANG=PI/3


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    geometry.R=R;geometry.check_kappa();geometry.check_concavity_factorization()
    n99=geometry.exclude_all(99,R)
    survivors=[b for b in range(3,100) if geometry.classify(100,b,R)['status']=='not excluded']
    assert survivors==list(range(31,40))
    fan=geometry.cluster_exclusion(B,6,F(1733,2500),3,F(1,1000))
    old=((198-B)*geometry.AH+B*geometry.KAPPA)*R*R+B*geometry.H_upper(R,2*geometry.PL/B,2*geometry.PH/B)
    deficit=(old-geometry.PL)/(R*R)
    coregap=geometry.PL*(109*geometry.AL-deficit)-441;assert coregap>0
    domain={'status':'PASS','radius':str(R),'m':100,'B':B,'remaining_boundary_counts':survivors,
            'n99_exclusion':n99,'q_at_most_four':fan,'minimum_M':22,
            'old_normalized_loss_upper':str(deficit),'core_cut_gap':str(coregap)}
    boundary.R=R;boundary.B=B;boundary.K=K;boundary.CURVATURE=F(0)
    env=boundary.verify()
    assert env['status']=='PASS' and env['radius']==str(R) and env['B']==B
    assert F(env['halfside_multiplier'])==K and env['required_center_norm_squared_upper']==str(1-R*R)
    radius=q(R);mu=PI/B;sm=sine(mu);rho=cosine(mu)-(radius.sq()-sm.sq()).sqrt()
    Q=B*(mu-sm*rho+q(K)*radius*sm*rho)
    assert check_conjugate()['status']==check_faces()['status']=='PASS'
    assert next(z for z in check_core()['cases'] if z['B']==B)['U_upper']==25
    assert next(z for z in check_weighted()['cases'] if z['B']==B)['M_upper']==23
    support=hinge.verify()
    assert support['status']=='PASS' and support['radius']==str(R) and support['B']==B
    assert F(support['paid_q4_charge'])==PAID and F(support['paid_q4_charge_margin'])>0
    assert support['required_center_norm_squared_upper']==str(1-R*R)
    data=json.loads((HERE/'hinge_B34_0p11323_proposals.json').read_text())
    assert data['radius']==str(R) and data['B']==B
    assert [(z['U'],z['support']) for z in data['rows']]==[(22,'linear_q4_hinge'),(24,'linear_q4_hinge'),(26,'linear_q4_hinge')]
    assert data['paid_q4_charge']==str(PAID)
    branches=[('M22..23',22,2,4),('M24..25',24,1,4),('M>=26',26,0,4)]
    expected=[t for t in itertools.combinations_with_replacement(range(4),3) if not(1 in t and 3 in t)]
    assert len(expected)==16
    face_count=vertex_count=0;minimum=None;results=[];raw_budgets={};boot=None
    for idx,(row,(branch,M,required,qmax)) in enumerate(zip(data['rows'],branches)):
        assert row['curvature_flag']==(2 if required==2 else 0)
        den=row['denominator'];pd=row['potential_denominator']
        labels=[F(row['high_potential'],pd),F(row['boundary_potential'],pd),F(0),F(row['deep_potential'],pd)]
        assert max(labels)-min(labels)<1
        charges=[F(row[k],den) for k in('charge_a','charge_b','charge_0','charge_deep')]
        ta=F(row['interface_a'],den);tz=F(row['interface_0'],den)
        assert min(ta,tz)>=0 and row['interface_deep']==0
        assert [tuple(z['indices']) for z in row['faces']]==expected
        face_min=None
        for cell in row['faces']:
            ids=cell['indices'];ls=[labels[i] for i in ids]
            value,acute,vertex=face_bound(ls,F(cell['nu'],den))
            credit=sum(tau*sum({ids[i],ids[(i+1)%3]}=={lab,1} for i in range(3))
                       for lab,tau in((0,ta),(2,tz)))
            upper=A+q(sum((charges[i] for i in ids),F(0))-credit)
            gap=upper.l-value.u
            assert gap>0,('face',branch,ids,F(gap,S))
            face_min=gap if face_min is None else min(face_min,gap);face_count+=1
        u0,beta,eta,apex,flag=[q(F(row[k],den)) for k in('u0','beta','eta','apex','flag')]
        assert min(apex.l,flag.l)>=0
        if not required:assert flag.l==flag.u==0
        C0=conjugate(K,F(0));lb=-labels[1];types=[]
        for p in range(qmax+1):
            for d in range(max(3,p+1),100):
                if p==0 and d<=5:types.extend([(p,d,3),(p,d,2)])
                else:types.append((p,d,0 if d>=7 else 2))
        assert len(types)==(485 if qmax==4 else 390);vertex_min=None
        for p,d,ix in types:
            lv=labels[ix]
            score=p*(conjugate(K,lv+lb)-C0)-q(lv)*(6-d+p)*ANG+(d-p)*q(charges[ix])-q(PAID if p==4 else 0)
            if p>0:score-=q(2*(ta if ix==0 else tz))
            upper=u0+p*beta+(d-6)*eta+(apex if p else q(0))
            if ix==3:upper-=(6-d if required==2 else 1)*flag
            gap=upper.l-score.u
            assert gap>0,('vertex',branch,p,d,ix,F(gap,S))
            vertex_min=gap if vertex_min is None else min(vertex_min,gap);vertex_count+=1
        slope=-eta+apex+q(charges[1])-q(lb)*ANG
        if idx<3:assert slope.u<0
        ear=ear_cap(R,K)
        shifted=A-2*C0+ear-2*beta+eta+q(lb)*PI+2*slope
        if idx<3:assert shifted.u<0
        width=q(2)/(q(1)+(q(1)-2*q(R)).sqrt())
        y=(q(K)+(q(K*K+8)).sqrt())/4
        badcap=width+(1-y.sq()).sqrt()*(y-q(K))
        bad=badcap-C0-beta-eta
        if idx<3:assert bad.u<0
        center=130*A+B*C0+66*u0+B*beta+(28-M)*eta+M*apex-required*flag+M*q(charges[1])-q(lb)*(2*PI+M*ANG)
        total=q(R).sq()*center+Q
        gap=PI.l-total.u
        assert gap>0,('area',branch,F(gap,S))
        minimum=gap if minimum is None else min(minimum,gap)
        results.append({'branch':branch,'M_endpoint':M,'support':row['support'],
             'deep_flag_requirement':required,'q_max':qmax,
             'directly_excluded_M':M,'potential_range':str(max(labels)-min(labels)),
             'minimum_face_slack':str(F(face_min,S)),'minimum_vertex_slack':str(F(vertex_min,S)),
             'shifted_ear_upper':str(F(shifted.u,S)),
             'bad_q1_coefficient_upper':str(F(bad.u,S)),'area_margin':str(F(gap,S))})
    assert (face_count,vertex_count)==(48,1455)
    return {'status':'PASS','radius':str(R),'B':B,'m':100,
            'scope':'Complete B34 branch after whole-cover norm normalization; no all-count radius theorem',
            'geometry':domain,'normalized_boundary_envelope':env,'halfside_multiplier':str(K),'arbitrary_ears':True,'arbitrary_bad_q1':True,'arbitrary_all_boundary_q0':True,
            'face_supports':face_count,'vertex_supports':vertex_count,'integer_ranges':3,'q4_hinge_allocation':support,
            'no_second_deficit_spend':True,
            'minimum_area_margin':str(F(minimum,S)),'branches':results}


if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
