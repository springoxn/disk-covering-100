#!/usr/bin/env python3
"""B32 .11322 low-M reduction to one unique deep-five case."""
from fractions import Fraction as F
from pathlib import Path
import itertools,json,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import verify_extension as g
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_quadratic_marked_conjugate import conjugate
from exact_range_one_face_support import face_bound,verify as verify_face_range
from verify_global_star_anchor_degree_window import verify as degree_window
from verify_one_positive_curvature_isoperimetry import verify as weighted_core
from verify_unmarked_low_degree_core_obstruction import verify as core_obstruction
from reduce_B32_flat_core_0p11318 import ROWS as BASE_ROWS
R=F(5661,50000);B=32;DEN=10**9;FAN=F(1,50)
LOW24={"a":378148580,"lb":129204403,"c":500000000,"charges":[26923601,3184540,25,50630840],"u0":5000,"beta":122737779,"eta":-167531040,"delta":0,"nus":[-878148580,-789985351,-739234261,-708042197,-661326345,-616933844,-629204403,-584823137,-541897848,-500000000,-309016994]}
LOW25={"a":317484650,"lb":169607035,"c":354526424,"charges":[19030233,5474061,25,24996919],"u0":5000,"beta":161865979,"eta":-168207709,"delta":22680644,"nus":[-766456175,-702903941,-543398994,-717378185,-656564456,-599259869,-459452309,-669607035,-610762938,-554551749,-500000000,-370674462]}
HIGH26={"a":332869157,"lb":220245172,"c":263677154,"charges":[21196929,9204008,25,30698216],"u0":5000,"beta":211413807,"eta":-176345201,"delta":0,"nus":[-832869157,-794338066,-712206445,-596899161,-756891212,-677411668,-567010275,-603776656,-502763470,-414101459,-720245172,-642835251,-536406666,-570135712,-471472805,-383240436,-500000000,-406247989,-319592656,-236322846]}


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    g.R=R;g.check_kappa();g.check_concavity_factorization()
    n99=g.exclude_all(99,R)
    survivors=[b for b in range(3,100) if g.classify(100,b,R)['status']=='not excluded']
    assert survivors==list(range(31,40))
    geometry={'no_all_boundary_q0_q1':g.cluster_exclusion(B,4,F(457,1000),2,F(1,1000)),
              'q_at_most_three':g.cluster_exclusion(B,5,F(1733,2500),3,F(1,1000))}
    window=degree_window()
    old=((198-B)*g.AH+B*g.KAPPA)*R*R+B*g.H_upper(R,2*g.PL/B,2*g.PH/B)
    old_budget=(old-g.PL)/(R*R)
    assert old_budget<F(window['degree4_loss_lower'])
    weighted=weighted_core();assert next(x for x in weighted['cases'] if x['B']==B)['M_upper']==23
    topology=core_obstruction();range_check=verify_face_range()
    rr=q(R);A=3*q(3).sqrt()/4;ANG=PI/3;mu=PI/B;s=sine(mu);cc=cosine(mu)
    h=(rr.sq()-s.sq()).sqrt();H=s*h+mu-s*cc
    derivative=cc*(rr.sq()-2*s.sq())/h+2*s.sq()
    tangent=(H-mu*derivative)/mu.sq()
    assert tangent.l>q(F(1,2)).u
    difference=4*mu-q(F(1733,5000))
    payment=q(F(1,2))*difference.sq()/(4*rr.sq())
    assert payment.l>q(FAN).u
    for k in range(1,11):assert F(k,1)/(6*k-2-F(k*k,2))>=F(1,4)
    C0=conjugate(F(0),F(0))
    baseline=((198-2*B)*A+B*C0)*rr.sq()+B*H
    ear_cap=F(413,200)
    assert (q(2)/(1+(1-2*rr).sqrt())+1).u<q(ear_cap).l
    all_faces=list(itertools.combinations_with_replacement(range(4),3))
    all_types={(p,d) for p in range(4) for d in range(5,9)}
    face_total=vertex_total=0
    def row_bounds(row,M,faces,types,pair_allowance=False):
        nonlocal face_total,vertex_total
        a,lb,positive=[F(row[x],DEN) for x in('a','lb','c')]
        labels=[-a,-lb,F(0),positive];charges=[F(x,DEN) for x in row['charges']]
        delta=F(row.get('delta',0),DEN);assert delta>=0
        assert len(faces)==len(row['nus'])
        face_min=None
        for ids,rawnu in zip(faces,row['nus']):
            ls=[labels[i] for i in ids]
            upper,acute,vertex=face_bound(ls,F(rawnu,DEN))
            pair_count=ids.count(0)*int(3 in ids) if pair_allowance else 0
            allowance=A+q(sum((charges[i] for i in ids),F(0))+delta*pair_count)
            gap=allowance.l-upper.u
            assert gap>0,('face',M,ids,F(gap,S))
            face_min=gap if face_min is None else min(face_min,gap);face_total+=1
        u0,beta,eta=[F(row[x],DEN) for x in('u0','beta','eta')]
        assert u0>=0
        gaps={}
        for p,d in sorted(types):
            index=0 if d>=7 else 3 if d==5 else 2;lv=labels[index]
            score=p*(conjugate(F(0),lv+lb)-C0)-q(lv)*(6-d+p)*ANG+q((d-p)*charges[index])
            dual=q(u0+p*beta+(d-6)*eta+(FAN if p==3 else 0))
            gap=dual.l-score.u
            assert gap>=0,('vertex',M,p,d,F(gap,S))
            gaps[p,d]=F(gap,S);vertex_total+=1
        slope=q(-eta+charges[1])-q(lb)*ANG
        shifted_ear=A-2*C0+q(ear_cap-2*beta+eta)+q(lb)*PI+2*slope
        assert shifted_ear.u<0
        gain=q(68*u0+B*beta+eta*(26-M)+M*charges[1])-q(lb)*(2*PI+M*ANG)
        margin=PI-(baseline+rr.sq()*gain)
        return {'M':M,'face_count':len(faces),'vertex_count':len(types),
                'minimum_face_slack':str(F(face_min,S)),'minimum_vertex_slack':str(min(gaps.values())),
                'M_slope':[str(F(slope.l,S)),str(F(slope.u,S))],
                'shifted_ear_coefficient_upper':str(F(shifted_ear.u,S))},margin,slope,gaps,delta
    # First establish a unique deep degree-five witness for M<=25.
    base=dict(BASE_ROWS[0]);base['delta']=0
    base_result,margin,slope,gaps,_=row_bounds(base,25,all_faces,all_types)
    assert slope.l>0
    two_low=margin+rr.sq()*q(gaps[0,5]+min(z for (p,d),z in gaps.items() if d==5))
    assert two_low.l>0
    base_result.update(two_low_degree_margin=str(F(two_low.l,S)),
                       ordinary_margin=str(F(margin.l,S)),
                       conclusion='M<=25 has exactly one degree5 vertex; it is the deep p0 core witness')
    # Weighted core curvature makes M<=23 impossible with only one degree5.
    assert 5*(134-23)>23**2
    # At M24 the one-curvature core is simple/chordless and the unique5
    # has only strict degree6 core neighbors.
    assert 5*112>20**2 and 5*110>22**2
    assert 5*110>3**2+21**2 and 5*110>3**2+23**2
    assert F(24+18)+F(18**2,5)<110
    assert F(24+19)+F(19**2,6)<110
    unique_types={(0,5)}|{(p,d) for p in range(4) for d in range(6,9)}
    faces24=list(itertools.combinations_with_replacement(range(3),3))+[(2,2,3)]
    low24,m24,_,g24,_=row_bounds(LOW24,24,faces24,unique_types)
    final24=m24+rr.sq()*q(g24[0,5]);assert final24.l>0
    low24.update(final_margin=str(F(final24.l,S)),positive_face_pattern='Only (ordinary0,ordinary0,positive)')
    # At M25, one negative degree unit and Euler force positive degree
    # excess=2-e; hence at most2 high vertices and at most4 high/positive
    # face-pair incidences. The positive witness has no BC neighbor.
    assert 26-25+1==2
    faces25=[ids for ids in all_faces if ids.count(3)<=1 and ids.count(0)<=2
             and not(1 in ids and 3 in ids)]
    low25,m25,_,g25,delta=row_bounds(LOW25,25,faces25,unique_types,True)
    final25=m25+rr.sq()*q(g25[0,5]-4*delta)
    low25.update(final_margin=str(F(final25.l,S)),pair_incidence_multiplier=str(delta),
                 pair_incidence_count_upper=4,maximum_high_degree_vertices=2)
    profiles=[(e,h7,h8) for e in range(3) for h7 in range(3) for h8 in range(2)
              if h7+2*h8==2-e]
    assert sorted(profiles)==[(0,0,1),(0,2,0),(1,1,0),(2,0,0)]
    needed=-final25/rr.sq()
    return {'status':'PASS','radius':str(R),'B':32,'m':100,'M_domain':'M<=25',
            'scope':'All M<=24 excluded; M25 reduced to a unique deep degree5 witness. Its final metric/local-star exclusion is separate.',
            'n99_exclusion':n99,'remaining_boundary_counts':survivors,'geometry':geometry,
            'degree_window':window,'B32_old_budget_upper':str(old_budget),
            'weighted_curvature_status':weighted['status'],'core_obstruction_status':topology['status'],
            'range_one_face_support_status':range_check['status'],
            'face_supports_checked':face_total,'vertex_supports_checked':vertex_total,
            'two_low_degree_margin':str(F(two_low.l,S)),
            'M24_margin':str(F(final24.l,S)),
            'remaining_case':{'M':25,'unique_low_degree':5,'low_marked_incidence':0,
                              'low_has_no_original_boundary_neighbor':True,
                              'other_degrees':[6,7,8],'maximum_high_degree_vertices':2,
                              'high_positive_face_pair_incidence_upper':4,
                              'degree_ear_profiles':[{'ears':e,'degree7':h7,'degree8':h8} for e,h7,h8 in profiles]},
            'reference_LOW25_angular_margin':str(F(final25.l,S)),
            'additional_normalized_face_gain_needed_upper':str(F(needed.u,S)),
            'reference_rows':[base_result,low24,low25]}
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
