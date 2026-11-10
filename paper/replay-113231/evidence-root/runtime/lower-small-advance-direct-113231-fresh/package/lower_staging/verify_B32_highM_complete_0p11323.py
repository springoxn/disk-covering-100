#!/usr/bin/env python3
"""Exact catalog-free normalized B32 high-M exclusion at R=113231/1000000.

Standard-library acceptance only. Historical files are immutable support
inputs, not historical-radius acceptance results. Every radius-dependent
comparison is recomputed here. Generic diagram/area foundations are stated
in the accompanying proof; this entry does not exclude another B branch.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,itertools,hashlib,subprocess
HERE=Path(__file__).resolve().parent
BASE=HERE if (HERE/'verify_star_lp_duals.py').exists() else HERE.parent/'working'
sys.path[:0]=[str(BASE),str(BASE/'lower_bounds_extension_20261004')]
import verify_extension as geometry
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_linear_halfside_marked_conjugate import conjugate
from exact_range_one_face_support import face_bound as plain_face,verify as range_check
from exact_signed_sine_full_face_support import face_bound as signed_face
from verify_jensen_slab_ear_support import cap as ear_cap
from polygon_star_perimeter_support import support as polygon_support
import verify_normalized_boundary_B32_0p11322 as small_boundary
import verify_exact_lens_boundary_0p11322 as lens_boundary
from reduce_B32_high_core_0p11322 import ROW
R=F(113231,1000000);B=32;I=68;D=10**9
A=3*q(3).sqrt()/4;ANG=PI/3
HIGH_SOURCE_SHA='4f3fafad244c9c69db3ee62980dd9fd7002fcab90d7662692b0c5abf5b28126c'
DIRECT_PROPOSAL_SHA='628f9c5db6ee9e73880f6dc27b32544034aad659d9448d4688a490b81ca9e011'

def lower(z):return F(z.l,S)
def upper(z):return F(z.u,S)

def reduce_profiles():
    K=F(3,10)
    source=BASE/'lower_bounds_extension_20261004/reduce_B32_high_core_0p11322.py'
    assert hashlib.sha256(source.read_bytes()).hexdigest()==HIGH_SOURCE_SHA
    for name,value in [('R',R),('B',B),('K',K),('CURVATURE',F(0))]:setattr(small_boundary,name,value)
    envelope=small_boundary.verify()
    assert envelope['radius']==str(R) and envelope['B']==B
    assert F(envelope['required_center_norm_squared_upper'])==1-R*R
    geometry.R=R;geometry.check_kappa();geometry.check_concavity_factorization()
    n99=geometry.exclude_all(99,R)
    survivors=[b for b in range(3,100) if geometry.classify(100,b,R)['status']=='not excluded']
    assert survivors==list(range(31,40))
    clusters={
        'no_all_boundary_q0_q1':geometry.cluster_exclusion(B,4,F(457,1000),2,F(1,1000)),
        'ordinary_marked_incidence_at_most_three':geometry.cluster_exclusion(B,5,F(1733,2500),3,F(1,1000))}
    local_range=range_check()
    labels=[-F(ROW['a'],D),-F(ROW['lb'],D),F(0),F(ROW['c'],D)]
    charges=[F(x,D) for x in ROW['charges']]
    assert max(labels)-min(labels)<1
    facegaps=[]
    faces=list(itertools.combinations_with_replacement(range(4),3))
    assert len(faces)==len(ROW['nus'])==20
    for ids,nu in zip(faces,ROW['nus']):
        cap,_,_=plain_face([labels[i] for i in ids],F(nu,D))
        gap=lower(A+q(sum((charges[i] for i in ids),F(0))))-upper(cap)
        assert gap>0,('face',ids,gap);facegaps.append(gap)
    u0,beta,eta=[F(ROW[k],D) for k in ('u0','beta','eta')]
    assert u0>=0
    C0=conjugate(K,F(0));gaps={}
    types=[(p,d) for p in range(4) for d in range(max(3,p+1),100)]
    for p,d in types:
        ix=0 if d>=7 else 3 if d<=5 else 2;lv=labels[ix]
        score=p*(conjugate(K,lv-labels[1])-C0)-q(lv)*(6-d+p)*ANG+q((d-p)*charges[ix])
        gap=lower(q(u0+p*beta+(d-6)*eta))-upper(score)
        assert gap>=0,('vertex',p,d,gap);gaps[p,d]=gap
    assert len(types)==387
    lb=-labels[1];slope=q(-eta+charges[1])-q(lb)*ANG
    shifted_ear=A-2*C0+ear_cap(R,K)+q(-2*beta+eta)+q(lb)*PI+2*slope
    rr=q(R);w=q(2)/(1+(1-2*rr).sqrt());y=(q(K)+q(K*K+8).sqrt())/4
    bad=w+(1-y.sq()).sqrt()*(y-q(K))-C0-q(beta+eta)
    assert max(slope.u,shifted_ear.u,bad.u)<0
    mu=PI/B;s=sine(mu);c=cosine(mu);h=(rr.sq()-s.sq()).sqrt()
    boundary=B*(s*h+mu-s*c+q(K)*rr*s*(c-h))
    center=134*A+B*C0+q(I*u0+B*beta+26*charges[1])-q(lb)*(2*PI+26*ANG)
    raw=PI-(rr.sq()*center+boundary)
    # Weighted positive curvature, rather than a count assuming degree5.
    flag=min(z/F(6-d) for (p,d),z in gaps.items() if d<=5)
    assert flag>0
    assert all(z>=flag*(6-d) for (p,d),z in gaps.items() if d<=5)
    one=raw+rr.sq()*q(flag)
    two=raw+rr.sq()*q(2*flag);assert two.l>0
    marked=min(z for (p,d),z in gaps.items() if p>0 and d<=5)
    marked_margin=raw+rr.sq()*q(marked);assert marked_margin.l>0
    shifted={
        'M_at_least_27':one-rr.sq()*slope,
        'at_least_one_ear':one-rr.sq()*shifted_ear,
        'at_least_one_bad_q1':one-rr.sq()*bad}
    assert all(z.l>0 for z in shifted.values())
    # With no low vertex Euler has nonnegative left side. With precisely
    # one degree5 and no other low vertex, the high-degree excess is one.
    assert [(M,e,b) for M in range(26,100) for e in range(17) for b in range(33)
            if 26-M-e-b>=0]==[(26,0,0)]
    assert 26-26-0-0+1==1
    return dict(status='PASS',radius=str(R),B=B,m=100,M_domain='M>=26',
        required_center_norm_squared_upper=str(1-R*R),
        n99_exclusion=n99,remaining_boundary_counts=survivors,geometry=clusters,
        normalized_boundary_envelope=envelope,range_one_face_status=local_range['status'],
        face_supports=20,vertex_supports=len(types),
        minimum_face_slack=str(min(facegaps)),minimum_vertex_slack=str(min(gaps.values())),
        weighted_low_curvature_cost=str(flag),raw_M26_margin=str(lower(raw)),
        one_low_diagnostic_margin=str(lower(one)),two_curvature_margin=str(lower(two)),
        marked_low_margin=str(lower(marked_margin)),
        M_slope_upper=str(upper(slope)),shifted_ear_upper=str(upper(shifted_ear)),bad_q1_upper=str(upper(bad)),
        low_case_shift_margins={k:str(lower(v)) for k,v in shifted.items()},
        remaining_profiles=[dict(M=26,ears=0,bad_q1=0,all_interior_degrees=6),
            dict(M=26,ears=0,bad_q1=0,unique_degree5_marked_incidence=0,
                 degree7_vertices=1,other_interior_degrees=6)],
        source_sha256=HIGH_SOURCE_SHA)

def topology_checks():
    # /6 applies if no low vertex exists, or if the unique low vertex has
    # an original boundary neighbor: strict block interiors cannot do so.
    for components in range(2,8):
        frontier=26-4*(components-1);faces=108+2*(components-1)
        assert frontier>=0 and 6*faces>frontier*frontier
    assert 6*108>24**2                       # no bridge
    assert 6*108>3**2+23**2                  # one face-bearing block
    assert 6*108>3**2+25**2                  # chordless core boundary
    assert 108==2*68-26-2 and 68-26==42
    return dict(status='PASS',core_vertices=68,core_boundary=26,core_faces=108,
        deep_vertices=42,scope='General induced-core Euler identities and /6 block disk isoperimetry; no flat development or graph catalog')

def direct_deep_five():
    """Conditional local closure when the unique5 has no original B neighbor."""
    path=BASE/'direct_M25_metric_20261004/exact_proposals.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==DIRECT_PROPOSAL_SHA
    data=json.loads(path.read_text());den=data['denominator'];assert den==10**12
    def rational(z):assert type(z) is int;return F(z,den)
    labels=list(map(rational,data['labels']));charges=list(map(rational,data['charges']))
    allowances=list(map(rational,data['outside_allowances']))
    assert len(labels)==len(charges)==3 and labels[2]==0 and len(allowances)==2
    assert min(charges)>=0 and min(allowances)>=0
    a,b=-labels[0],-labels[1];assert a>0 and b>=0
    assert data['epsilon']==[3,5] and data['perimeter_penalty']==[13,10]
    eps=F(3,5);weight=1-eps;tau=F(13,10);edge=eps*tau
    expected=[list(ids) for ids in itertools.combinations_with_replacement(range(3),3) if ids!=(0,0,0)]
    assert [row['ids'] for row in data['face_rows']]==expected
    ordinary_slacks=[]
    for row in data['face_rows']:
        ids=row['ids'];cap,_,_=signed_face([labels[i] for i in ids],[0,0,0],rational(row['nu']))
        slack=lower(A+q(sum((charges[i] for i in ids),F(0))))-upper(cap)
        assert slack>0;ordinary_slacks.append(slack)
    expected=[(1,[x,y,z]) for x,y,z in itertools.product([0,2],[0,2],[0,1,2]) if [x,y,z].count(0)<=2]
    expected +=[(2,list(ids)) for ids in itertools.product([0,2],repeat=3) if ids.count(0)<=2]
    assert [(row['selected_edges'],row['ids']) for row in data['outside_rows']]==expected
    outside_slacks=[]
    for row in data['outside_rows']:
        count=row['selected_edges'];ids=row['ids'];edges=[0,0,edge] if count==1 else [edge,0,edge]
        cap,_,_=signed_face([labels[i] for i in ids],edges,rational(row['nu']))
        slack=lower(A+q(sum((charges[i] for i in ids),F(0))+allowances[count-1]))-upper(cap)
        assert slack>0;outside_slacks.append(slack)
    J=max((5-2*j)*allowances[0]+j*allowances[1] for j in range(3))
    patterns=[(0,[5,0,0]),(1,[3,2,0]),(2,[2,2,1]),(2,[1,4,0])]
    assert [(star['high_neighbors'],star['counts']) for star in data['stars']]==patterns
    polygon=polygon_support(5,1,-tau);caps=[];central_supports=0
    for star in data['stars']:
        k=star['high_neighbors'];counts=star['counts'];v=rational(star['center_potential'])
        assert sum(counts)==5 and counts[1]+2*counts[2]==2*k
        assert [row['high_base_vertices'] for row in star['faces']]==[h for h in range(3) if counts[h]]
        cap=q(eps)*polygon-q(v)*ANG
        for row in star['faces']:
            h=row['high_base_vertices'];ls=[v]+[-a]*h+[F(0)]*(2-h)
            normalized=[z/weight for z in ls];assert max(normalized)-min(normalized)<1
            bound,_,_=plain_face(normalized,rational(row['nu']))
            cap+=counts[h]*q(weight)*bound;central_supports+=1
        caps.append(cap)
    assert central_supports==8
    # One unique degree5, one degree7, 66 other degree6 sites, U=26.
    # The historical 1/50 fan charge is deliberately discarded.
    K=F(0);C0=conjugate(K,F(0));mu=PI/B;rr=q(R)
    s=sine(mu);c=cosine(mu);H=s*(rr.sq()-s.sq()).sqrt()+mu-s*c
    rows=[]
    for p in range(4):
        ordinary=66;po=B-p
        baseline=134*A+B*C0+po*(conjugate(K,b)-C0)-q(b)*(2*PI+26*ANG)
        baseline+=p*(conjugate(K,b-a)-C0)+q(a*(p-1))*ANG
        for index,(k,counts) in enumerate(patterns[:2]):
            center=baseline-5*A+caps[index]+q(J)
            center+=q((7-p-2*k)*charges[0]+26*charges[1]+(6*ordinary-po+5-(15-2*k))*charges[2])
            margin=PI-rr.sq()*center-B*H;assert margin.l>0,('deep5',p,k,lower(margin))
            rows.append(dict(high_marked_incidence=p,high_neighbors=k,area_margin=str(lower(margin))))
    assert len(rows)==8
    return dict(status='PASS',radius=str(R),B=B,m=100,M=26,
        required_center_norm_squared_upper=str(1-R*R),
        scope='Conditional unique-degree5/no-original-boundary-neighbor local closure, one degree7 and other degrees6',
        proposal_sha256=DIRECT_PROPOSAL_SHA,ordinary_face_supports=9,outside_face_supports=18,
        central_face_supports=central_supports,integer_profile_cases=8,
        minimum_ordinary_slack=str(min(ordinary_slacks)),minimum_outside_slack=str(min(outside_slacks)),
        fan_charge='0',variance_charge='0',halfside_multiplier='0',
        minimum_area_margin=str(min(F(row['area_margin']) for row in rows)),rows=rows)

def four_face_metric():
    """Simple chordless P26/F108 core with deep degree excess h=0 or1."""
    K=F(11,25);LR=F(-20663069056,10**11);LB=F(-72993038978,10**11);TAU=F(6623191134,10**10)
    for name,value in [('R',R),('B',B),('K',K),('CURVATURE',F(0))]:setattr(lens_boundary,name,value)
    envelope=lens_boundary.verify()
    assert envelope['radius']==str(R) and envelope['B']==B
    assert F(envelope['halfside_multiplier'])==K
    assert F(envelope['required_center_norm_squared_upper'])==1-R*R
    patterns=[('DDD',[F(0)]*3,[F(0)]*3,F(-1,2)),
        ('DDR',[F(0),F(0),LR],[F(0)]*3,F(-56597508864,10**11)),
        ('DRR',[F(0),LR,LR],[-TAU,F(0),F(0)],F(-75767205590,10**11)),
        ('BRR',[LR,LR,LB],[F(0),F(0),TAU],F(-75767203850,10**11))]
    caps=[];supports=[]
    for name,labels,edges,nu in patterns:
        guard=1-(max(labels)-min(labels)+sum((max(-z,F(0)) for z in edges),F(0))/2)
        assert guard>0
        cap,acute,boundaries=signed_face(labels,edges,nu)
        assert len(boundaries)==3 and all(cap.u>=z.u for z in [acute]+boundaries)
        caps.append(cap);supports.append(dict(pattern=name,guard=str(guard),support_upper=str(upper(cap))))
    rr=q(R);mu=PI/B;s=sine(mu);rho=cosine(mu)-(rr.sq()-s.sq()).sqrt()
    outer=B*(mu-s*rho+q(K)*rr*s*rho);rows=[]
    for h in (0,1):
        counts=[62+h,20-h,26,26]
        assert sum(counts[:3])==108 and 3*counts[0]+2*counts[1]+26==42*6+h
        assert counts[1]+2*26==3*108-(42*6+h)==72-h
        center=sum((count*cap for count,cap in zip(counts,caps)),q(0))
        center+=B*conjugate(K,LR-LB)-q((B+h)*LR)*ANG+q(LB)*(2*PI+26*ANG)
        margin=PI-rr.sq()*center-outer;assert margin.l>0,('four-face',h,lower(margin))
        rows.append(dict(deep_degree_excess=h,multiplicities=dict(zip(('DDD','DDR','DRR','BRR'),counts)),
            normalized_center_upper=str(upper(center)),area_margin=str(lower(margin))))
    return dict(status='PASS',radius=str(R),B=B,scope='Conditional simple chordless P26/F108 core; all42 deep degrees at least6 with total excess0 or1; ring degrees unrestricted',
        required_center_norm_squared_upper=str(1-R*R),halfside_multiplier=str(K),
        shared_edge_pairs=26,shared_edge_multiplier=str(TAU),face_supports=4,face_support_rows=supports,
        normalized_boundary_envelope=envelope,outer_boundary_upper=str(upper(outer)),
        graph_catalog_used=False,boundary_turn_window_used=False,
        minimum_area_margin=str(min(F(row['area_margin']) for row in rows)),rows=rows)

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    # Component globals and caches cannot leak between specializations.
    def fresh(name):
        raw=subprocess.check_output([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--component',name],cwd=BASE,text=True)
        return json.loads(raw)
    reduction=fresh('profiles');topology=fresh('topology')
    deep=fresh('deep_five');metric=fresh('four_face')
    assert all(row['status']=='PASS' for row in (reduction,topology,deep,metric))
    for row in (reduction,deep,metric):
        assert row['radius']==str(R) and row['B']==B
        assert F(row['required_center_norm_squared_upper'])==1-R*R
    assert reduction['M_domain']=='M>=26' and deep['M']==26
    minimum=min(F(deep['minimum_area_margin']),F(metric['minimum_area_margin']))
    assert minimum>0
    # Without a low vertex, Euler gives the all-six topology and h=0.
    # With the unique5, split on whether it has an original B neighbor.
    # No B neighbor uses the direct star. A B neighbor prevents it from
    # being strict block-interior, so /6 topology and h in {0,1} apply.
    return dict(status='PASS',radius=str(R),B=B,m=100,M_domain='M>=26',
        scope='Complete normalized-diagram B32 high-M branch only; low-M, other B branches, universal radius and exact optimality are separate',
        required_center_norm_squared_upper=str(1-R*R),graph_catalog_used=False,
        profile_reduction=reduction,core_topology=topology,
        deep_five_local_closure=deep,four_face_metric=metric,
        minimum_area_margin=str(minimum),fresh_process_components=True)

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    if len(sys.argv)==3 and sys.argv[1]=='--component':
        result={'profiles':reduce_profiles,'topology':topology_checks,
                'deep_five':direct_deep_five,'four_face':four_face_metric}[sys.argv[2]]()
    else:
        assert len(sys.argv)==1,'Unsupported command-line arguments'
        result=verify()
    print(json.dumps(result,indent=2),flush=True)
