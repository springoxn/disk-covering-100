#!/usr/bin/env python3
"""Normalized B32 high-M reduction at .11322; low-M cases are separate."""
from fractions import Fraction as F
from pathlib import Path
import itertools,json,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import verify_extension as g
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_range_one_face_support import face_bound,verify as verify_faces
from exact_linear_halfside_marked_conjugate import conjugate
from verify_jensen_slab_ear_support import cap
import verify_normalized_boundary_B32_0p11322 as boundary
R=F(5661,50000);B=32;K=F(3,10);D=10**9
ROW=dict(a=316853193,lb=296410489,c=251520713,
         charges=[19059352,16604579,25,28006333],
         u0=5000,beta=275436661,eta=-141245515,
         nus=[-816853193,-810007718,-702520876,-594407026,-803194046,
              -696292199,-588998886,-599073964,-503423733,-418635227,
              -796410489,-690067817,-583564470,-593033359,-497779385,
              -413064221,-500000000,-410862802,-328093870,-248479287])

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    assert boundary.R==R and boundary.B==B and boundary.K==K
    envelope=boundary.verify();g.R=R
    n99=g.exclude_all(99,R)
    survivors=[b for b in range(3,100) if g.classify(100,b,R)['status']=='not excluded']
    assert survivors==list(range(31,40))
    fan=g.cluster_exclusion(B,5,F(1733,2500),3,F(1,1000))
    face_lemma=verify_faces();rr=q(R);A=3*q(3).sqrt()/4;ANG=PI/3
    mu=PI/B;s=sine(mu);c=cosine(mu);h=(rr.sq()-s.sq()).sqrt()
    H=s*h+mu-s*c;sineta=s*(c-h)/rr
    C0=conjugate(K,F(0))
    baseline=((198-2*B)*A+B*(C0+q(K)*sineta))*rr.sq()+B*H
    a,lb,positive=[F(ROW[k],D) for k in('a','lb','c')]
    labels=[-a,-lb,F(0),positive];charges=[F(x,D) for x in ROW['charges']]
    assert max(labels)-min(labels)<1
    faces=list(itertools.combinations_with_replacement(range(4),3))
    fmin=None
    for ids,nu in zip(faces,ROW['nus']):
        upper,acute,vertex=face_bound([labels[i] for i in ids],F(nu,D))
        gap=(A+q(sum((charges[i] for i in ids),F(0)))).l-upper.u
        assert gap>0,('face',ids,F(gap,S))
        fmin=gap if fmin is None else min(fmin,gap)
    types={(p,d) for p in range(4) for d in range(max(3,p+1),100)}
    u0,beta,eta=[F(ROW[k],D) for k in('u0','beta','eta')]
    gaps={}
    for p,d in sorted(types):
        ix=0 if d>=7 else 3 if d<=5 else 2;lv=labels[ix]
        score=p*(conjugate(K,lv+lb)-C0)-q(lv)*(6-d+p)*ANG+q((d-p)*charges[ix])
        dual=q(u0+p*beta+(d-6)*eta)
        gap=dual.l-score.u
        assert gap>=0,('vertex',p,d,F(gap,S));gaps[p,d]=F(gap,S)
    slope=q(-eta+charges[1])-q(lb)*ANG;assert slope.u<0
    ear=A-2*C0+cap(R,K)+q(-2*beta+eta)+q(lb)*PI+2*slope
    width=q(2)/(1+(1-2*rr).sqrt());y=(q(K)+q(K*K+8).sqrt())/4
    bad=width+(1-y.sq()).sqrt()*(y-q(K))-C0-q(beta+eta)
    assert ear.u<0 and bad.u<0
    M=26
    gain=q(68*u0+B*beta+eta*(26-M)+M*charges[1])-q(lb)*(2*PI+M*ANG)
    margin=PI-(baseline+rr.sq()*gain)
    low_cost=min(v for(p,d),v in gaps.items() if d<=5)
    flagged=margin+rr.sq()*q(low_cost);assert flagged.l>0
    assert [(M,e,b) for M in range(26,100) for e in range(17) for b in range(33)
            if 26-M-e-b>=0]==[(26,0,0)]
    assert 6*110>22**2 and 6*108>24**2
    assert 6*108>3**2+23**2 and 6*108>3**2+25**2
    assert 6*108>25**2 and 108==2*68-26-2
    return {'status':'PASS','radius':str(R),'B':32,'M_domain':'M>=26',
            'scope':'Normalized-diagram high-M reduction to16 known flat-core graphs; low-M and metric closure are separate',
            'required_center_norm_squared_upper':str(1-R*R),
            'normalized_boundary_envelope':envelope,'n99_exclusion':n99,
            'remaining_boundary_counts':survivors,'q_at_most_three':fan,
            'range_one_face_status':face_lemma['status'],'face_supports':len(faces),
            'vertex_supports':len(types),'minimum_face_slack':str(F(fmin,S)),
            'minimum_vertex_slack':str(min(gaps.values())),
            'M_slope':[str(F(slope.l,S)),str(F(slope.u,S))],
            'shifted_ear_upper':str(F(ear.u,S)),'bad_q1_upper':str(F(bad.u,S)),
            'ordinary_margin':str(F(margin.l,S)),'low_degree_cost':str(low_cost),
            'flagged_margin':str(F(flagged.l,S)),
            'remaining_case':{'M':26,'ears':0,'bad_q1':0,'all_interior_degrees':6,
                              'core_vertices':68,'core_boundary':26,'core_faces':108,
                              'canonical_full_graphs':16}}
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
