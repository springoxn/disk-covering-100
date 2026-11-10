#!/usr/bin/env python3
"""Exact B32 reduction at .11318 to one flat-core combinatorial class.

No actual-triangle acuteness or variance bound is assumed. Run fresh with
assertions enabled; floating point and numerical optimization are not used.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, importlib, itertools, json, sys, zipfile
from functools import lru_cache
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import verify_extension as g
import verify_unmarked_low_degree_core_obstruction as core_obstruction
from verify_star_lp_duals import q,S,PI
from exact_angle_conjugates import sine_conjugate
from exact_quadratic_marked_conjugate import conjugate,verify as verify_marked_conjugate
from verify_potential_star_duals import sine,cosine

R=F(5659,50000);B=32;DEN=10**9
SHA='3f8e603344f4996d66acde7bcf0631628a1df879734fab8110c63c120f6f6324'
BASE='disk100_ear_angular_stage_20261004/'
ROWS=[
  {
    "U": 25,
    "lb": 156009786,
    "a": 280014573,
    "c": 219975427,
    "charges": [
      14830514,
      4635310,
      23,
      21524604
    ],
    "u0": 10000,
    "beta": 148657647,
    "eta": -158737786,
    "nus": [
      -780014573,
      -737473127,
      -680008968,
      -589036039,
      -696264424,
      -640806609,
      -553687538,
      -588157077,
      -505958566,
      -431409618,
      -656009786,
      -602066613,
      -517979878,
      -550315496,
      -470184292,
      -396334336,
      -500000000,
      -422690335,
      -350078055,
      -280024573
    ]
  },
  {
    "U": 26,
    "lb": 218852017,
    "a": 274033677,
    "c": 225956323,
    "charges": [
      14287216,
      9088633,
      23,
      22054335
    ],
    "u0": 10000,
    "beta": 210043077,
    "eta": -164317706,
    "nus": [
      -774033677,
      -755408526,
      -676324380,
      -583055143,
      -737025715,
      -659105780,
      -567593256,
      -586371232,
      -501879628,
      -425428722,
      -718852017,
      -641959729,
      -552029374,
      -569710930,
      -486159970,
      -409991853,
      -500000000,
      -420463898,
      -345918462,
      -274043677
    ]
  }
]
FAN_CHARGE=F(1,50)


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    g.R=R;g.check_kappa();g.check_concavity_factorization()
    g.exclude_all(99,R)
    survivors=[b for b in range(3,100) if g.classify(100,b,R)['status']=='not excluded']
    assert survivors==[31,32,33,34,35,36,37,38]
    obstruction=core_obstruction.verify()
    geometry={
        'remaining_boundary_counts':survivors,
        'no_all_boundary_q1':g.cluster_exclusion(B,4,F(571,1250),2,F(1,1000)),
        'q_at_most_three':g.cluster_exclusion(B,5,F(6931,10000),3,F(1,1000))}
    # Global H tangent deficit plus weighted overlap pays each q3 star.
    assert R*R<F(5,9)
    rr=q(R);mu=PI/B;sm=sine(mu);cm=cosine(mu)
    hm=(rr.sq()-sm.sq()).sqrt()
    Hm=sm*hm+mu-sm*cm
    Hp=cm*(rr.sq()-2*sm.sq())/hm+2*sm.sq()
    curvature=(Hm-mu*Hp)/mu.sq()
    assert curvature.l>q(F(1,2)).u
    D=4*mu-q(F(6931,20000))
    assert D.l>0
    charge=q(F(1,2))*D.sq()/(4*rr.sq())
    assert charge.l>q(FAN_CHARGE).u
    for k in range(1,11):
        denominator=6*k-2-F(k*k,2)
        assert denominator>0 and F(k,1)/denominator>=F(1,4)
    # Full-simplex localization for any label range <=1/2. These conservative
    # nonacute/degenerate score caps are all strictly below equilateral area.
    root3=q(3).sqrt();A=3*root3/4
    localization=[A-(1+PI/12),A-PI/3,A-(root3/2+PI/8)]
    assert all(z.l>0 for z in localization)
    archive=ROOT/'ear_stage_review_20261004'/'disk100_ear_angular_stage_20261004.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==SHA
    with zipfile.ZipFile(archive) as z:
        manifest=json.loads(z.read(BASE+'MANIFEST_SHA256.json'))
        for name,digest in manifest.items():
            assert hashlib.sha256(z.read(BASE+name)).hexdigest()==digest
    assert 'verify_earaware_allcounts' not in sys.modules and 'verify_support' not in sys.modules
    sys.path.insert(0,str(archive.resolve())+'/'+BASE+'research/new_stage_degrees_refined')
    v=importlib.import_module('verify_earaware_allcounts')
    v.R=R;v.B=B;v.K=F(0)
    marked_parameter=verify_marked_conjugate()
    @lru_cache(None)
    def marked(multiplier):
        interval=conjugate(F(0),multiplier)
        return v.I(F(interval.l,S),F(interval.u,S))
    t=v.PI/B;s=v.sin(t);c=v.cos(t);h=(R*R-s*s).sqrt()
    # k=0: the boundary bound is exactly H-concavity, with no coupled-length
    # correction and no use of the source helper's positive-k tangent proof.
    baseline=(198-2*B)*v.A*R*R+B*R*R*marked(F(0))+B*(s*h+t-s*c)
    ear_cap=F(413,200)
    width=(1-(1-2*v.I(R)).sqrt())/R
    assert (width+1).b<ear_cap
    faces=list(itertools.combinations_with_replacement(range(4),3))
    types={(qq,d) for qq in range(4) for d in range(max(3,qq+1),100)}
    results=[];minimum=None
    for row in ROWS:
        U=row['U'];lb=F(row['lb'],DEN);a=F(row['a'],DEN)
        positive=F(row['c'],DEN)
        labels=[-a,-lb,F(0),positive];charges=[F(x,DEN) for x in row['charges']]
        assert 0<lb<a and positive>0 and a+positive<F(1,2) and len(row['nus'])==len(faces)
        face_min=None
        for ids,rawnu in zip(faces,row['nus']):
            ls=[labels[i] for i in ids];nu=q(F(rawnu,DEN))
            assert max(ls)-min(ls)<=F(1,2)
            upper=(PI*nu+sum((sine_conjugate(nu-q(x)) for x in ls),q(0))
                   -PI*q(sum(ls,F(0)))/3)
            gap=A+q(sum((charges[i] for i in ids),F(0)))-upper
            assert gap.l>0,('face support',U,ids,F(gap.l,S))
            face_min=gap.l if face_min is None else min(face_min,gap.l)
        u0=F(row['u0'],DEN);beta=F(row['beta'],DEN);eta=F(row['eta'],DEN)
        assert u0>=0
        vertex_min=None
        low_unmarked=None;low_any=None
        for qq,d in sorted(types):
            ix=0 if d>=7 else 3 if d<=5 else 2;lv=labels[ix]
            score=(qq*(marked(lv+lb)-marked(F(0)))-lv*(6-d+qq)*v.ANG
                   +(d-qq)*charges[ix])
            gap=u0+beta*qq+eta*(d-6)+(FAN_CHARGE if qq==3 else 0)-score
            assert gap.a>=0,('vertex support',U,qq,d,gap.enc())
            vertex_min=gap.a if vertex_min is None else min(vertex_min,gap.a)
            if d<=5:
                low_any=gap.a if low_any is None else min(low_any,gap.a)
                if qq==0:
                    low_unmarked=gap.a if low_unmarked is None else min(low_unmarked,gap.a)
        coeff=-eta-lb*v.ANG+charges[1]
        if U==25:assert coeff.a>0
        else:assert U==26 and coeff.b<0
        ear_coefficient=v.A-2*marked(F(0))+ear_cap-2*beta+eta+lb*v.PI
        assert ear_coefficient.b<0
        shifted_ear=ear_coefficient+2*coeff
        assert shifted_ear.b<0
        gain=68*u0+B*beta+eta*(B-6-U)-lb*(2*v.PI+U*v.ANG)+U*charges[1]
        margin=v.PI-(baseline+R*R*gain)
        sigma=low_unmarked if U==25 else low_any
        assert sigma is not None and sigma>0
        flagged=margin+R*R*sigma
        assert flagged.a>F(1,20000),('flagged area contradiction',U,flagged.enc())
        minimum=flagged.a if minimum is None else min(minimum,flagged.a)
        results.append({'branch':'M<=25: compulsory unmarked low degree' if U==25 else 'M>=26: exclude every low degree',
                        'corner_labels':[str(x) for x in labels],
                        'corner_charges':[str(x) for x in charges],
                        'face_multisets_checked':len(faces),
                        'minimum_face_support_margin':str(F(face_min,S)),
                        'vertex_types_checked':len(types),
                        'minimum_vertex_support_margin':str(vertex_min),
                        'M_coefficient':coeff.enc(),'per_ear_coefficient_upper':str(ear_coefficient.b),
                        'shifted_ear_coefficient_upper':str(shifted_ear.b),
                        'ordinary_area_margin_lower':str(margin.a),
                        'minimum_low_degree_reduced_cost':str(sigma),
                        'flagged_area_margin_lower':str(flagged.a)})
    # M>=26 with no degree<=5 star has nonnegative total degree excess.
    # Euler gives that excess as 26-M-e, forcing M26,e0 and every degree6.
    assert [(M,e) for M in range(26,100) for e in range(17)
            if 26-M-e>=0]==[(26,0)]
    # Core-block isoperimetry excludes extra components/chords, bridges,
    # and two or more face-bearing blocks in the all-degree-six remainder.
    assert 6*110>22**2
    assert 6*108>24**2
    assert 6*108>3**2+23**2
    # A core boundary chord splits perimeters summing to28, with both>=3.
    assert 6*108>3**2+25**2
    assert 108==2*68-26-2
    # Flat lattice development: a repeated boundary vertex would split
    # the unit walk into two lengths at least3, giving this impossible cap.
    assert 6*108>3**2+23**2 and 6*108>25**2
    return {'status':'PASS','radius':str(R),'B':B,'m':100,
            'scope':'Reduction only: the remaining flat-core graph family still needs complete metric exclusion; no new B32 or global bound',
            'core_obstruction_status':obstruction['status'],
            'remaining_case':{'ears':0,'U':26,'interior_vertices':68,'all_interior_degrees':6,
                              'boundary_chords':0,'interior_bridges':0,'core_components':1,
                              'core_boundary_chords':0,'remaining_marked_incidences_upper':2,
                              'core_vertices':68,'core_boundary_vertices':26,'core_faces':108,
                              'ring_q0_faces':26,'ordinary_q1_faces':32,
                              'flat_lattice_development_injective':True,'coordinate_width_sum':26},
            'geometry':geometry,'archive_sha256':SHA,'archive_members_verified':len(manifest),
            'halfside_multiplier':'0','actual_triangle_acuteness_required':False,
            'global_H_variance_coefficient':'1/2','per_q3_star_charge':str(FAN_CHARGE),
            'available_normalized_charge_lower':str(F(charge.l,S)),
            'ear_cap':str(ear_cap),'arbitrary_ears_allowed':True,
            'full_simplex_localization_margins':[str(F(z.l,S)) for z in localization],
            'global_marked_conjugate':marked_parameter,
            'total_face_multisets':40,'total_vertex_supports':2*len(types),
            'minimum_flagged_area_margin':str(minimum),'branches':results}


if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
