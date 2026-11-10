#!/usr/bin/env python3
"""Exact B33 .1132 face rows with deep curvature witnesses.

Requires the separately proved normalized-cover geometry, both independent
arc bootstraps, and the two same-radius radial supports.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,itertools
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'lower_bounds_extension_20261004'))
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine
from exact_quadratic_marked_conjugate import conjugate,verify as verify_conjugate
from exact_range_one_face_support import face_bound,verify as verify_range_one
from verify_reflected_radial_B33_lowM_0p1132 import SUPPORT as LOW
from verify_reflected_radial_B33_highM_0p1132 import SUPPORT as HIGH
from verify_jensen_slab_ear_support import quadratic_cap
from verify_multiple_p3_footprint_variance import verify as verify_fan
from verify_unmarked_low_degree_core_obstruction import verify as verify_core
from verify_one_positive_curvature_isoperimetry import verify as verify_weighted
from check_core_cut_isoperimetry import verify as verify_cut
import verify_extension as geometry
R=F(283,2500);B=33;A=3*q(3).sqrt()/4;ANG=PI/3


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    assert LOW.radius==HIGH.radius==R and LOW.B==HIGH.B==B
    assert (LOW.penalty,LOW.stability)==(F(7,125),F(3,2))
    assert (HIGH.penalty,HIGH.stability)==(F(11,100),F(0))
    assert verify_conjugate()['status']=='PASS'
    range_check=verify_range_one();assert range_check['status']=='PASS'
    core=verify_core();weighted=verify_weighted();cut=verify_cut();fan=verify_fan()
    assert next(z for z in core['cases'] if z['B']==B)['U_upper']==25
    assert next(z for z in weighted['cases'] if z['B']==B)['M_upper']==23
    assert cut['minimum_M']==22
    upper=((198-B)*geometry.AH+B*geometry.KAPPA)*R*R
    upper+=B*geometry.H_upper(R,2*geometry.PL/B,2*geometry.PH/B)
    old_deficit=(upper-geometry.PL)/(R*R);assert old_deficit<1
    radius=q(R);span3=q(F(571,1250));span4=q(F(6931,10000))
    assert sine(span3/2).l>(2*radius).u and sine(span4/2).l>(3*radius).u
    delta3=3*PI/B-span3/2;delta4=4*PI/B-span4/2
    assert min(delta3.l,delta4.l)>0
    data=json.loads((ROOT/'deep_face_B33_0p1132_proposals.json').read_text())
    assert data['radius']==str(R) and data['B']==B
    assert [(z['ears'],z['U'],z['support']) for z in data['rows']]==[
        (0,22,'low'),(0,24,'low'),(1,24,'low'),(0,26,'high')]
    branches=[('e0,M22..23',23,2,1),('e0,M24..25',24,1,-1),
              ('e>=1,M22..25',24,1,-1),('all_e,M>=26',26,0,-1)]
    expected=[t for t in itertools.combinations_with_replacement(range(4),3)
              if not(1 in t and 3 in t)]
    assert len(expected)==16
    face_count=vertex_count=0;minimum=None;results=[]
    for row,(branch,endpoint,flag_requirement,sign) in zip(data['rows'],branches):
        instance=LOW if row['support']=='low' else HIGH;e=row['ears']
        assert row['curvature_flag']==(2 if flag_requirement==2 else 0)
        den=row['denominator'];pd=row['potential_denominator']
        labels=[F(row['high_potential'],pd),F(row['boundary_potential'],pd),F(0),F(row['deep_potential'],pd)]
        assert max(labels)-min(labels)<1
        charges=[F(row[k],den) for k in('charge_a','charge_b','charge_0','charge_deep')]
        tau_a=F(row['interface_a'],den);tau_0=F(row['interface_0'],den)
        assert min(tau_a,tau_0)>=0 and row['interface_deep']==0
        assert [tuple(z['indices']) for z in row['faces']]==expected
        min_face=None
        for cell in row['faces']:
            ids=cell['indices'];ls=[labels[i] for i in ids]
            value,acute,vertex=face_bound(ls,F(cell['nu'],den))
            credit=F(0)
            for label,tau in((0,tau_a),(2,tau_0)):
                credit+=tau*sum({ids[i],ids[(i+1)%3]}=={label,1} for i in range(3))
            allowance=A+q(sum((charges[i] for i in ids),F(0))-credit)
            gap=allowance.l-value.u
            assert gap>0,('face',branch,ids,F(gap,S))
            min_face=gap if min_face is None else min(min_face,gap);face_count+=1
        u0,beta,eta,apex,flag=[q(F(row[k],den)) for k in('u0','beta','eta','apex','flag')]
        assert min(apex.l,flag.l)>=0
        if not flag_requirement:assert flag.l==flag.u==0
        C0=conjugate(instance.penalty,F(0));lb=-labels[1]
        per_fan=instance.GAMMA*q(F(33,133))*delta4.sq()/radius.sq()
        minimum_vertex=None
        types=[]
        for p in range(4):
            for d in range(max(3,p+1),100):
                if p==0 and d<=5:types.extend([(p,d,3),(p,d,2)])
                else:types.append((p,d,0 if d>=7 else 2))
        assert len(types)==390
        for p,d,ix in types:
            lv=labels[ix]
            score=p*(conjugate(instance.penalty,lv+lb)-C0)-q(lv)*(6-d+p)*ANG+(d-p)*q(charges[ix])
            if p>0:score-=q(2*(tau_a if ix==0 else tau_0))
            if p==3 and e==0:score-=per_fan
            dual=u0+p*beta+(d-6)*eta+(apex if p else q(0))
            if ix==3:
                assert p==0 and d<=5
                dual-=(6-d if flag_requirement==2 else 1)*flag
            gap=dual.l-score.u
            assert gap>0,('vertex',branch,p,d,ix,F(gap,S))
            minimum_vertex=gap if minimum_vertex is None else min(minimum_vertex,gap);vertex_count+=1
        slope=-eta+apex+q(charges[1])-q(lb)*ANG
        assert (slope.l>0 if sign>0 else slope.u<0)
        ear=quadratic_cap(R,instance.penalty)
        shifted=A-2*C0+ear-2*beta+eta+q(lb)*PI+2*slope
        if e or row['support']=='high':assert shifted.u<0
        U=endpoint
        total=(132+e)*A+(B-2*e)*C0+e*ear
        total+=67*u0+(B-2*e)*beta+(27+e-U)*eta+U*apex-flag_requirement*flag+U*q(charges[1])
        total-=q(lb)*((2-e)*PI+U*ANG)
        Q=B*instance.TARGET+2*PI*instance.MU
        variance=q(0) if not e else q(F(11,30))*delta3.sq()
        bound=radius.sq()*total+Q-instance.GAMMA*variance
        gap=PI.l-bound.u
        assert gap>0,('area',branch,F(gap,S))
        minimum=gap if minimum is None else min(minimum,gap)
        results.append({'branch':branch,'U_endpoint':U,'support':row['support'],
             'required_deep_curvature_flag':flag_requirement,'penalty':str(instance.penalty),
             'potential_range':str(max(labels)-min(labels)),
             'minimum_face_slack':str(F(min_face,S)),'minimum_vertex_slack':str(F(minimum_vertex,S)),
             'shifted_ear_upper':str(F(shifted.u,S)),'area_margin':str(F(gap,S))})
    assert (face_count,vertex_count)==(64,1560)
    return {'status':'PASS','radius':str(R),'B':B,'m':100,
            'scope':'B33 after whole-cover normalization only; requires both unpenalized domains, the new high-M variance bootstrap, and final low/high radial pairs',
            'new_face_theorem':range_check['status'],'deep_witness_lemma':'DEEP_CORE_CURVATURE_WITNESSES.md',
            'face_supports':face_count,'vertex_supports':vertex_count,'integer_ranges':4,
            'old_normalized_loss_upper':str(old_deficit),'footprint_spans':['571/1250','6931/10000'],
            'minimum_area_margin':str(F(minimum,S)),'branches':results}


if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
