#!/usr/bin/env python3
"""Additive, source-bound independent B34 .11323 audit; standard library only."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys,json,hashlib,subprocess,itertools,datetime,platform
if not __debug__:raise RuntimeError('Assertions must remain enabled')
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];WORK=BASE/'working'
sys.path.insert(0,str(WORK))
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_linear_halfside_marked_conjugate import conjugate
from exact_range_one_face_support import face_bound
from verify_jensen_slab_ear_support import cap as ear_cap
R=F(113231,1000000);K=F(1,2);B=34;A=3*q(3).sqrt()/4;ANG=PI/3
ENTRY=HERE/'verify_hinge_B34_complete_0p11323.py';PROPOSAL=HERE/'hinge_B34_0p11323_proposals.json'
JO=HERE/'B34_HINGE_COMPLETE_INDEPENDENT_AUDIT_0p11323_20261005.json'
MO=HERE/'B34_HINGE_COMPLETE_INDEPENDENT_AUDIT_0p11323_20261005.md'
assert not JO.exists() and not MO.exists(),'Preserve existing audit artifacts'
code=['verify_star_lp_duals.py','verify_potential_star_duals.py','exact_angle_conjugates.py','exact_linear_halfside_marked_conjugate.py','exact_quadratic_marked_conjugate.py','exact_range_one_face_support.py','verify_exact_lens_boundary_0p11322.py','verify_exact_lens_hinge_deficit.py','verify_jensen_slab_ear_support.py','verify_one_positive_curvature_isoperimetry.py','verify_unmarked_low_degree_core_obstruction.py','lower_bounds_extension_20261004/verify_extension.py']
proof=['EXACT_NORMALIZED_LENS_PENALTY.md','MARKED_APEX_HINGE_CHARGE.md','DEEP_CORE_CURVATURE_WITNESSES.md','UNMARKED_LOW_DEGREE_CORE_OBSTRUCTION.md','ONE_POSITIVE_CURVATURE_ISOPERIMETRY.md','FULL_FACE_RANGE_ONE_SUPPORT.md','FULL_APEX_LINEAR_HALFSIDE_CONJUGATE.md','JENSEN_SLAB_EAR_SUPPORT.md','LINEAR_LENS_B34_0p11321_PROOF.md','LINEAR_BOOTSTRAP_B34_0p11322_PROOF.md','lower_bounds_extension_20261004/GENERAL_DISK_ISOPERIMETRY.md','lower_bounds_extension_20261004/CORE_CUT_ISOPERIMETRY.md','lower_bounds_extension_20261004/PROOF_EXTENSION.md','lower_bounds_extension_20261004/STAR_PREMISES_0p11307.md','disk100_certification_20261004/original/disk100_continued_proof/previous/GLOBAL_LOWER_PROOF.md']
paths=[Path(__file__).resolve(),ENTRY,PROPOSAL,HERE/'verify_B34_q4_hinge_charge_0p11323.py',HERE/'PROOF_B34_11323.md']+[WORK/x for x in code+proof]
def bind(p):
    b=p.read_bytes();return {'path':str(p.relative_to(BASE)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
before=[bind(p) for p in paths]
cmd=[sys.executable,'-B','-S',str(ENTRY)]
run=subprocess.run(cmd,cwd=HERE,text=True,capture_output=True)
assert run.returncode==0,(run.returncode,run.stderr)
result=json.loads(run.stdout)
assert result['status']=='PASS' and result['radius']==str(R) and result['B']==B and result['m']==100
assert result['normalized_boundary_envelope']['required_center_norm_squared_upper']==str(1-R*R)
assert result['normalized_boundary_envelope']['variance_coefficient']=='0'
assert result['q4_hinge_allocation']['required_center_norm_squared_upper']==str(1-R*R)
assert result['q4_hinge_allocation']['halfside_multiplier']==str(K)
assert result['geometry']['remaining_boundary_counts']==list(range(31,40))
assert result['geometry']['minimum_M']==22 and result['geometry']['n99_exclusion']['cases']==96
assert F(result['geometry']['old_normalized_loss_upper'])>1 and F(result['geometry']['core_cut_gap'])>0
assert result['arbitrary_ears'] and result['arbitrary_bad_q1'] and result['arbitrary_all_boundary_q0'] and result['no_second_deficit_spend']
assert json.loads((HERE/'hinge_B34_complete_0p11323_result.json').read_text())==result
optcmd=[sys.executable,'-B','-S','-O',str(ENTRY)]
opt=subprocess.run(optcmd,cwd=HERE,text=True,capture_output=True)
assert opt.returncode!=0 and 'Assertions must remain enabled' in opt.stderr
D=json.loads(PROPOSAL.read_text())
assert D['radius']==str(R) and D['B']==B and D['halfside_multiplier']==str(K) and D['paid_q4_charge']=='1/50'
mu=PI/B;sm=sine(mu);rho=cosine(mu)-(q(R).sq()-sm.sq()).sqrt()
Q=B*(mu-sm*rho+q(K)*q(R)*sm*rho);C0=conjugate(K,F(0))
width=q(2)/(1+(1-2*q(R)).sqrt());y=(q(K)+q(K*K+8).sqrt())/4
badcap=width+(1-y.sq()).sqrt()*(y-q(K));ear=ear_cap(R,K)
expected=[t for t in itertools.combinations_with_replacement(range(4),3) if not(1 in t and 3 in t)]
assert len(expected)==16 and (1,1,1) in expected
rows=[];faces=vertices=0;minimum=None
for j,(lo,hi,req) in enumerate([(22,23,2),(24,25,1),(26,407,0)]):
    row=D['rows'][j];den=row['denominator'];pd=row['potential_denominator']
    assert den>0 and pd>0 and row['U']==lo and row['ears']==0
    assert row['support']=='linear_q4_hinge' and row['curvature_flag']==(2 if req==2 else 0)
    ls=[F(row['high_potential'],pd),F(row['boundary_potential'],pd),F(0),F(row['deep_potential'],pd)]
    assert ls[0]<0 and ls[1]<0 and ls[3]>0 and max(ls)-min(ls)<1
    cs=[F(row[x],den) for x in ['charge_a','charge_b','charge_0','charge_deep']]
    ta=F(row['interface_a'],den);tz=F(row['interface_0'],den)
    assert ta>=0 and tz>=0 and row['interface_deep']==0
    assert [tuple(c['indices']) for c in row['faces']]==expected
    fg=[]
    for cell in row['faces']:
        ids=tuple(cell['indices']);val,acute,degenerate=face_bound([ls[i] for i in ids],F(cell['nu'],den))
        credit=sum((tau for i in range(3) for lab,tau in [(0,ta),(2,tz)] if {ids[i],ids[(i+1)%3]}=={lab,1}),F(0))
        allowance=A+q(sum((cs[i] for i in ids),F(0))-credit);gap=allowance.l-val.u
        assert gap>0,(lo,ids,F(gap,S));fg.append(gap);faces+=1
    u0,beta,eta,apex,flag=[q(F(row[x],den)) for x in ['u0','beta','eta','apex','flag']]
    assert apex.l==apex.u==0 and flag.l>=0
    if req==0:assert flag.u==0
    lb=-ls[1];vg=[];domains=Counter()
    for p in range(5):
        for d in range(3,100):
            if p>=d:continue
            ids=[2,3] if p==0 and d<=5 else [0 if d>=7 else 2]
            for ix in ids:
                lv=ls[ix];score=p*(conjugate(K,lv+lb)-C0)-q(lv)*(6-d+p)*ANG+q((d-p)*cs[ix])
                if p:score-=q(2*(ta if ix==0 else tz))
                if p==4:score-=q(F(1,50))
                allowance=u0+p*beta+(d-6)*eta
                if ix==3:allowance-=(6-d if req==2 else 1)*flag
                gap=allowance.l-score.u
                assert gap>0,(lo,p,d,ix,F(gap,S));vg.append(gap);vertices+=1;domains[(p,ix)]+=1
    assert len(vg)==485
    def center(M,e,b):
        U=M+2*e;ordinary=B-2*e-b
        return (130+e)*A+ordinary*C0+66*u0+ordinary*beta+(28+e-b-U)*eta-req*flag+U*q(cs[1])-q(lb)*((2-e)*PI+U*ANG)+e*ear+b*badcap
    endpoint=center(lo,0,0)
    ms=-eta+q(cs[1])-q(lb)*ANG
    es=A-2*C0-2*beta-eta+2*q(cs[1])+q(lb)*PI-2*q(lb)*ANG+ear
    bs=badcap-C0-beta-eta
    assert ms.u<0 and es.u<0 and bs.u<0
    def vector(M,e,b):
        U=M+2*e;ordinary=B-2*e-b
        return (130+e,ordinary,66,ordinary,28+e-b-U,-req,U,e-2,-U,e,b)
    v0=vector(lo,0,0);vm=(0,0,0,0,-1,0,1,0,-1,0,0);ve=(1,-2,0,-2,-1,0,2,1,-2,1,0);vb=(0,-1,0,-1,-1,0,0,0,0,0,1)
    count=0
    for e in range(18):
        for b in range(B-2*e+1):
            for M in range(lo,min(hi,390+e)+1):
                assert vector(M,e,b)==tuple(v0[k]+(M-lo)*vm[k]+e*ve[k]+b*vb[k] for k in range(11));count+=1
    gap=PI.l-(q(R).sq()*endpoint+Q).u
    assert gap>0
    reported=result['branches'][j]
    assert reported['area_margin']==str(F(gap,S))
    assert reported['minimum_face_slack']==str(F(min(fg),S)) and reported['minimum_vertex_slack']==str(F(min(vg),S))
    minimum=gap if minimum is None else min(minimum,gap)
    rows.append({'M_range':[lo,hi if req else None],'deep_requirement':req,'face_supports':len(fg),'vertex_supports':len(vg),'enlarged_count_profiles_checked':count,'potential_range':str(max(ls)-min(ls)),'minimum_face_slack':str(F(min(fg),S)),'minimum_vertex_slack':str(F(min(vg),S)),'M_slope_upper':str(F(ms.u,S)),'ear_slope_upper':str(F(es.u,S)),'bad_q1_slope_upper':str(F(bs.u,S)),'area_margin':str(F(gap,S)),'local_domain_counts':{str(k):v for k,v in sorted(domains.items())}})
assert (faces,vertices)==(48,1455) and result['minimum_area_margin']==str(F(minimum,S))
charges=[F(1,200)*max(F(0),(p+1)*F(9,100)-F(1733,5000))/(2*R*R) for p in range(B)]
assert [str(x) for x in charges]==result['q4_hinge_allocation']['normalized_area_charges']
assert charges[4]==F(2585000,128210329) and charges[4]-F(1,50)==F(1039671,6410516450)
assert sine(q(F(1733,5000))).l>q(3*R).u
assert before==[bind(p) for p in paths],'Bound sources changed during audit'
review=['Whole-cover norm normalization precedes all classification','Six-cell Jensen applies to any six selected endpoint arcs; no contiguous-fan premise','Proper edge subsets have p+1 endpoints; each endpoint cell belongs to at most two owners','The delta bank pays the q4 charge once, with variance coefficient zero','Deep flags allow degree3,4,5 and disconnected/bridged cores; no unique-five or simple-core premise','All16 full-face triples include BBB and degenerate-vertex caps; no actual-angle acuteness','All degrees3..99 and separate deep/nondeep unmarked low types are included','Original e,b,U counts reconstruct the shifted allowance on all enlarged finite count profiles','Generic enlarged covers normalize before perturbation/classification; finite-type closed-domain limit retains strict endpoint gaps']
receipt={'status':'PASS','audit_date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Complete normalized B34 branch only at 113231/1000000; no all-count theorem or exact optimum','radius':str(R),'B':B,'m':100,'python_version':platform.python_version(),'fresh_entry_command':cmd,'fresh_entry_result':result,'fresh_entry_stdout_sha256':hashlib.sha256(run.stdout.encode()).hexdigest(),'author_saved_result_agrees':True,'optimized_mode_negative_test':{'command':optcmd,'returncode':opt.returncode,'required_rejection':'Assertions must remain enabled'},'independent_reconstruction':{'face_supports':faces,'vertex_supports':vertices,'rows':rows,'minimum_area_margin':str(F(minimum,S)),'complete_M_domain':'all integers M>=22','ears_domain':'0<=e<=17','bad_q1_domain':'0<=b<=34-2e','degree_domain':'3..99; 0<=p<=4 and p<d','all_boundary_q0_included':True,'split_fans_allowed':True,'required_center_norm_squared_upper':str(1-R*R),'q4_charge':str(charges[4]),'paid_charge':'1/50','q4_charge_excess':str(charges[4]-F(1,50)),'endpoint_owner_multiplicity':2,'variance_spent':'0','analytic_review':review},'dependency_bindings':before,'sources_unchanged_during_audit':True,'formalization_status':'Analytic mathematical geometry/topology review, not a machine formal proof'}
md=f'''# Independent audit: complete B34 hinge branch at R=.11323

PASS. A fresh standard-library entry and a separately assembled face, vertex,
and aggregate-count reconstruction both pass. This is the B34 branch for
exactly100 arbitrary-center congruent disks covering the closed unit disk;
other boundary counts remain separate obligations.

## Exact results

- Radius:{R}; B34; m100; normalized center norm squared:{1-R*R}
- Full-face supports:48; vertex supports:1455; coherent M ranges:3
- Minimum area gap:{F(minimum,S)} > .0002345271275686
- Author saved output equals independent fresh output
- Python -O rejects immediately:Assertions must remain enabled

The companion JSON records the complete fresh output, independent local
slacks and slopes, full original-count reconstruction, command/stdout hash,
and SHA-256/byte bindings for the proposal, verifier, computational helpers
and mathematical dependencies. All bound sources were unchanged throughout.

## Independent geometry/accounting review

Whole-cover normalization precedes the construction and classification of
all diagrams. Its inversion identity preserves old covered subsets of the
unit disk. No diagram is retained across center motion, and no older or
stronger-radius norm cap is transferred. At this radius m<=99 is excluded,
and surviving boundary counts are31..39. The B34 old loss upper budget is
above1; its actual value gives the positive general core-cut comparison and
M=U-2e>=22, without the obsolete loss<1 shortcut.

The six-cell Jensen comparison applies to any six endpoint arcs of total
full mass<=.6932, because it depends only on cardinality and mass. An apex
with p>=5 has at least six endpoint cells whose whole assigned arcs lie in
its radius3R footprint. Therefore p<=4 even for split fans. A p4 owner has
at least five endpoint cells; each boundary cell belongs to at most two
owners because it is incident to only two boundary-cycle edges. Thus the
hinge delta(t)>=(1/200)(.09-t)_+ pays normalized charge2585000/128210329,
exceeding1/50 by1039671/6410516450 for every q4 apex.

The same compensated half-side inequality supplies the delta bank. Its
variance coefficient is zero. Only the paid q4 charge is spent in the star
functional; the positive p3 charge and q4 excess are discarded. There is
no second variance, radial or boundary-deficit payment.

All16 label triples include BBB and repeated deep labels. A distinguished
deep vertex cannot meet a boundary vertex by planarity. The mandatory
degenerate-vertex cap is included, so no actual-angle acuteness is assumed.
Every d=3..99,p=0..4,p<d is covered, with separate deep/nondeep unmarked
degree3,4,5 types. The M22/23 flag uses weighted6-d; M24/25 uses one deep
low-degree witness. Induced-core blocks allow boundary chords, bridges,
disconnected components, isolated vertices and all-boundary q0/q1 faces.
No degree window, unique-five, simple/chordless-core or lattice premise is
introduced. Terminal BI credits are reserved within the same q0 face
allowances before their two terminal occurrences are used at marked apices.

The independently assembled original e,b,U incidence functional equals
the shifted functional on every profile in a deliberately enlarged finite
count domain. Its M, ear and bad-q1 coefficients are strictly negative in
all rows. Consequently three lower-endpoint evaluations cover all integers
M>=22, arbitrary ears and every permitted bad-q1 count.

## Arbitrary endpoint covers and scope

For an endpoint cover, first enlarge the radius, normalize ALL centers at
that enlarged radius, then perturb within strict coverage slack. Take a
constant finite combinatorial type and a compact convergent subsequence as
radii decrease toR. Closed full-angle/length/arc domains and uniform strict
final gaps exclude the B34 limiting branch. Normalization precedes every
classification. Geometry/topology are analytically reviewed mathematical
arguments, not machine-formalized proofs.

No reviewed source or historical .11322 checkpoint was changed. This
additive audit does not promote B34 alone into an all-count lower bound or
an exact optimum.
'''
with JO.open('x') as f:f.write(json.dumps(receipt,indent=2)+'\n')
with MO.open('x') as f:f.write(md)
print(json.dumps({'status':'PASS','receipt':str(JO),'audit':str(MO),'face_supports':faces,'vertex_supports':vertices,'minimum_area_margin':str(F(minimum,S)),'count_profiles':sum(z['enlarged_count_profiles_checked'] for z in rows),'source_bindings':len(before),'optimized_mode_rejected':True},indent=2))
