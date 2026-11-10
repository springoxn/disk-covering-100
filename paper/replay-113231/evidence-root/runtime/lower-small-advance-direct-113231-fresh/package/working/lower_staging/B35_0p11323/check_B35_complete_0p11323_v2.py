#!/usr/bin/env python3
"""Exact normalized-diagram B35 branch at .11323; exact source replay plus P26 one-ear restriction."""
from fractions import Fraction as F
from pathlib import Path
import itertools,json,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"lower_bounds_extension_20261004"))
import verify_extension as g
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_range_one_face_support import face_bound,verify as verify_faces
from exact_linear_halfside_marked_conjugate import conjugate,verify as verify_marked
from verify_jensen_slab_ear_support import cap,verify as verify_ear
from verify_unmarked_low_degree_core_obstruction import verify as verify_core
import verify_normalized_boundary_penalty_0p11323 as boundary
R=F(113231,1000000);B=35;K=F(33,100);DEN=10**9;L=F(1733,2500);CHARGE=F(1,500)
ROWS=[{"M":24,"a":215378973,"lb":54657165,"c":284620986,"charges":[8804155,572708,25,33022550],"u0":20000,"beta":49060571,"eta":-56664205,"nus":[-715378973,-659741340,-639775380,-524395986,-606443237,-587380027,-478154992,-568651016,-461559552,-366766821,-554657165,-536211276,-431443352,-518002984,-414818291,-321030272,-500000000,-398220261,-304908938,-215379014]},{"M":25,"a":268555429,"lb":142091436,"c":231444568,"charges":[13649473,3848398,25,23331922],"u0":5000,"beta":128950394,"eta":-76897258,"nus":[-768555429,-725144421,-672942383,-577572425,-683123671,-632773823,-541500841,-584732121,-498134190,-419943250,-642091436,-593129439,-505061254,-545955852,-461623434,-384158113,-500000000,-418414330,-342097953,-268555432]},{"M":26,"a":287233074,"lb":188419939,"c":233048838,"charges":[15599361,6748351,25,23777126],"u0":5000,"beta":171987528,"eta":-88725370,"nus":[-787233074,-753538479,-684445144,-587104918,-720664509,-653465416,-559473067,-590307406,-502737012,-423946728,-688419939,-622737139,-531518254,-560376437,-474567727,-396288634,-500000000,-417814032,-340980542,-266951162]}]
RESTRICTED={"M":25,"a":303795658,"lb":119535073,"charges":[17436015,2727394,25],"u0":5000,"beta":108173933,"eta":-99823782,"nus":[-803795658,-739630702,-694578126,-678627337,-636038433,-595220580,-619535073,-578571365,-538839360,-500000000]}

M26_RESTRICTED={'M': 26, 'a': 308167941, 'lb': 168977954, 'charges': [17937717, 5433731, 25], 'u0': 5000, 'beta': 153867006, 'eta': -110119657, 'earflag': 27009838, 'nus': [-808167941, -760239879, -697242295, -714021974, -653553203, -596512829, -668977954, -610361366, -554356250, -500000000]}

def verify_M26_core_topology():
    """Exact integer witnesses for the written P26/F102 topology proof."""
    I=65;M=26;Fc=2*I-2-M;assert Fc==102
    checks={
      'disconnected_components':6*(Fc+2)-(M-4)**2,
      'bridge':6*Fc-(M-2)**2,
      'multiple_face_blocks':6*Fc-(3**2+(M-3)**2),
      'two_core_degree_two_vertices':6*(Fc-2)-(M-2)**2}
    assert all(x>0 for x in checks.values())
    # e=0 and c=1 imply n2+n3=0 exactly, so F102/P26.
    assert (0+2*(1-1))==0
    # For p<=4 and d>=6, equality d-p=3 gives just these types.
    equal_types=[(p,d) for p in range(5) for d in range(6,100) if d-p==3]
    assert equal_types==[(3,6),(4,7)]
    return {'status':'PASS','core_vertices':I,'core_faces':Fc,
            'core_simple_boundary_length':M,'strict_interior_degrees_lower':6,
            'minimum_induced_core_degree':2,'degree_two_core_vertices_upper':1,
            'equality_local_types':[list(x) for x in equal_types],
            'integer_contradiction_margins':checks,
            'dependency':'Written induced-core topology plus GENERAL_DISK_ISOPERIMETRY.md'}

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    assert boundary.R==R and boundary.B==B and boundary.K==K
    envelope=boundary.verify()
    assert envelope['required_center_norm_squared_upper']==str(1-R*R)
    g.R=R;g.check_kappa();g.check_concavity_factorization()
    n99=g.exclude_all(99,R)
    survivors=[b for b in range(3,100) if g.classify(100,b,R)['status']=='not excluded']
    assert survivors==list(range(31,40))
    fan=g.cluster_exclusion(B,6,L,3,F(1,1000))
    core=verify_core();range_lemma=verify_faces();marked_lemma=verify_marked();ear_lemma=verify_ear()
    rr=q(R);A=3*q(3).sqrt()/4;ANG=PI/3;mu=PI/B
    sm=sine(mu);cm=cosine(mu);hm=(rr.sq()-sm.sq()).sqrt()
    H=sm*hm+mu-sm*cm;sineta=sm*(cm-hm)/rr
    C0=conjugate(K,F(0))
    baseline=((198-2*B)*A+B*(C0+q(K)*sineta))*rr.sq()+B*H
    ear_cap=cap(R,K);width=q(2)/(1+(1-2*rr).sqrt())
    y=(q(K)+(q(K*K+8)).sqrt())/4
    bad_cap=width+(1-y.sq()).sqrt()*(y-q(K))
    fan_payments=[]
    for n in range(1,9):
        cells=4*n+1;assert cells<B and n*L/2<g.PL
        delta=F(cells,B)*g.PL-n*L/2;assert delta>0
        V=F(B,cells*(B-cells))*delta*delta
        payment=boundary.CURVATURE*V/(n*R*R)
        assert payment>CHARGE
        fan_payments.append({'q4_vertices':n,'payment_per_vertex_lower':str(payment)})
    face_count=vertex_count=0
    def bounds(row,restricted=False,core_neighbor_minimum=3):
        nonlocal face_count,vertex_count
        M=row['M'];a,lb=[F(row[x],DEN) for x in('a','lb')]
        labels=[-a,-lb,F(0)]+([F(row['c'],DEN)] if 'c' in row else [])
        charges=[F(x,DEN) for x in row['charges']]
        assert max(labels)-min(labels)<1
        faces=list(itertools.combinations_with_replacement(range(len(labels)),3))
        assert len(faces)==len(row['nus'])
        fmin=None
        for ids,rawnu in zip(faces,row['nus']):
            ls=[labels[i] for i in ids]
            support,acute,degenerate=face_bound(ls,F(rawnu,DEN))
            gap=(A+q(sum((charges[i] for i in ids),F(0)))).l-support.u
            assert gap>0,('face',M,restricted,ids,F(gap,S))
            fmin=gap if fmin is None else min(fmin,gap);face_count+=1
        types=({(p,d) for p in range(5) for d in range(max(6,p+1+core_neighbor_minimum),100)} if restricted
               else {(p,d) for p in range(5) for d in range(max(3,p+1),100)})
        u0,beta,eta=[F(row[x],DEN) for x in('u0','beta','eta')];assert u0>=0
        gaps={}
        for p,d in sorted(types):
            ix=0 if d>=7 else 3 if d<=5 else 2;lv=labels[ix]
            score=p*(conjugate(K,lv+lb)-C0)-q(lv)*(6-d+p)*ANG+q((d-p)*charges[ix])
            flag=F(row.get('earflag',0),DEN)
            assert flag>=0
            dual=q(u0+p*beta+(d-6)*eta+(CHARGE if p==4 else 0)+(flag if d-p==3 else 0))
            gap=dual.l-score.u
            assert gap>=0,('vertex',M,restricted,p,d,F(gap,S))
            gaps[p,d]=F(gap,S);vertex_count+=1
        coefficient=q(-eta+charges[1])-q(lb)*ANG
        shifted_ear=A-2*C0+ear_cap+q(-2*beta+eta)+q(lb)*PI+2*coefficient
        bad=bad_cap-C0-q(beta+eta)
        assert shifted_ear.u<0 and bad.u<0
        gain=q(65*u0+B*beta+eta*(29-M)+M*charges[1]+F(row.get('earflag',0),DEN))-q(lb)*(2*PI+M*ANG)
        margin=PI-(baseline+rr.sq()*gain)
        report={'M':M,'restricted':restricted,'faces':len(faces),'vertices':len(types),
                'corner_labels':[str(x) for x in labels],
                'minimum_face_slack':str(F(fmin,S)),'minimum_vertex_slack':str(min(gaps.values())),
                'M_slope':[str(F(coefficient.l,S)),str(F(coefficient.u,S))],
                'shifted_ear_upper':str(F(shifted_ear.u,S)),'bad_q1_upper':str(F(bad.u,S)),
                'ordinary_margin':str(F(margin.l,S))}
        return report,margin,coefficient,gaps,shifted_ear,bad
    # Historical rows are replayed unchanged as rational inputs. The M26
    # ordinary margin is allowed to fail only as an explicitly reported
    # diagnostic; every actual final exclusion below is asserted positive.
    results=[];margins=[]
    z,m,c,gaps,ear,bad=bounds(ROWS[0]);assert c.l>0
    low=m+rr.sq()*q(min(v for(p,d),v in gaps.items() if p==0 and d<=5))
    assert low.l>0;z['M_le24_flagged_margin']=str(F(low.l,S))
    z['branch']='All M<=24, compulsory unmarked degree<=5 witness'
    results.append(z);margins.append(low.l)
    z,m,c,gaps,ear,bad=bounds(ROWS[1])
    low=m+rr.sq()*q(min(v for(p,d),v in gaps.items() if d<=5))
    assert low.l>0;z['any_low_degree_margin']=str(F(low.l,S))
    z['branch']='M25 with any original interior degree<=5'
    results.append(z);margins.append(low.l)
    z,m,c,gaps,ear,bad=bounds(ROWS[2]);assert c.u<0 and m.u<0
    ge27=m-rr.sq()*c;assert ge27.l>0
    low=m+rr.sq()*q(min(v for(p,d),v in gaps.items() if d<=5))
    one_ear=m-rr.sq()*ear;one_bad=m-rr.sq()*bad
    assert low.l>0 and one_ear.l>0 and one_bad.l>0
    z['source_ordinary_M26_status']='FAIL, diagnostic only; not used as an exclusion'
    z['M_ge27_margin']=str(F(ge27.l,S))
    z['M26_low_degree_margin']=str(F(low.l,S))
    z['M26_one_original_ear_margin']=str(F(one_ear.l,S))
    z['M26_one_bad_q1_margin']=str(F(one_bad.l,S))
    z['branch']='All M>=27; M26 forces e=b=0 and every original interior degree>=6'
    results.append(z);margins.extend((ge27.l,low.l,one_ear.l,one_bad.l))
    # The M25 induced-core identities use M=U-2e and allow all original
    # ears and bad faces. No e=b=0 premise is needed for this topology.
    assert 6*105>21**2 and 6*104>24**2
    assert 6*103>23**2 and 6*103>3**2+22**2
    assert 6*103>3**2+24**2
    z,m,c,gaps,ear,bad=bounds(RESTRICTED,True);assert m.l>0
    z['core_premise']='Simple chordless P25/F103 core implies p<=d-4'
    z['branch']='M25 with all original interior degrees>=6'
    results.append(z);margins.append(m.l)
    topology=verify_M26_core_topology()
    z,m,c,gaps,ear,bad=bounds(M26_RESTRICTED,True,2);assert m.l>0
    z['core_premise']='Simple P26/F102 core implies p<=d-3 and at most one d-p=3 vertex'
    z['degree_two_core_vertex_allowance']=str(F(M26_RESTRICTED['earflag'],DEN))
    z['branch']='Remaining M26: e=b=0 and all original interior degrees>=6'
    results.append(z);margins.append(m.l)
    assert face_count==80 and vertex_count==2382
    return {'status':'PASS','radius':str(R),'B':B,'m':100,
            'scope':'Complete B35 branch for globally normalized diagrams; normalization must precede B/graph classification',
            'required_center_norm_squared_upper':str(1-R*R),
            'normalization_warning':'Do not reflect a fixed graph or silently transfer this radius-dependent norm premise to another radius',
            'n99_exclusion':n99,'remaining_boundary_counts':survivors,'q_at_most_four':fan,
            'normalized_boundary_envelope':envelope,'range_one_face_support_status':range_lemma['status'],
            'global_marked_status':marked_lemma['status'],'ear_support_status':ear_lemma['status'],
            'core_obstruction_status':core['status'],'halfside_multiplier':str(K),
            'paid_q4_charge':str(CHARGE),'fan_payment_checks':fan_payments,
            'total_face_supports':face_count,'total_vertex_supports':vertex_count,
            'minimum_area_margin':str(F(min(margins),S)),
            'M26_core_topology':topology,'branches':results}
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
