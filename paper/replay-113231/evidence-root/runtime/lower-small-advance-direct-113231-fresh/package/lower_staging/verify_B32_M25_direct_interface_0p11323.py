#!/usr/bin/env python3
"""Exact B32 M25 coherent metric/interface exclusion at .11323."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,itertools,subprocess,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent/'working'
sys.path.insert(0,str(HERE))
sys.path[:0]=[str(ROOT),str(ROOT/'signed_edge_metric_20261004')]
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_linear_halfside_marked_conjugate import conjugate
from verify_jensen_slab_ear_support import cap as ear_cap
import verify_tight_hinges_B32_0p11323 as hinge
from exact_range_one_face_support import face_bound as ordinary_bound
from polygon_star_perimeter_support import support as polygon_support
from exact_signed_sine_full_face_support import face_bound
R=F(113231,1000000);B=32;K=F(11,25);
FAN=F(119,2000)*(4*F(187,2000)-F(3467,10000))/(2*R*R)
PROFILES=[(0,[7,7]),(0,[8]),(1,[7]),(2,[])]
PATTERNS=[(0,[5,0,0]),(1,[3,2,0]),(2,[2,2,1]),(2,[1,4,0])]
def verify():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 p=HERE/'B32_M25_direct_interface_0p11323_proposal.json';data=json.loads(p.read_text())
 assert data['schema']=='B32-M25-direct-interface-R23-v1'
 assert data['radius']==str(R) and data['B']==B
 assert data['halfside_multiplier']==[11,25]
 den=data['denominator'];assert type(den) is int and den==10**12
 def rational(v):
  assert type(v) is int
  return F(v,den)
 labels=list(map(rational,data['labels']));charges=list(map(rational,data['charges']))
 D=list(map(rational,data['outside_allowances']))
 interface=rational(data['interface_H']);assert interface>0
 assert data['interface_O']==data['ordinary_credit_per_marked']==0
 def credit(ids):return interface*sum({ids[j],ids[(j+1)%3]}=={0,1} for j in range(3))
 assert len(labels)==len(charges)==3 and len(D)==2 and labels[2]==0
 a,b=-labels[0],-labels[1];assert a>0 and b>=0 and min(charges)>=0 and min(D)>=0
 assert data['epsilon']==[1,2] and data['perimeter_penalty']==[13,10]
 eps=F(1,2);weight=1-eps;tau=F(13,10);kappa=eps*tau
 # Same-radius topology, degree, ear, variance and short-arc prerequisites.
 raw=subprocess.check_output([sys.executable,'-B','-S',str(HERE/'refresh_B32_low_core_0p11323.py')],cwd=ROOT,text=True)
 premises=json.loads(raw);assert premises['status']=='PASS' and premises['radius']==str(R) and premises['B']==32 and premises['m']==100
 rem=premises['remaining_case']
 assert rem['M']==25 and rem['unique_low_degree']==5 and rem['low_marked_incidence']==0
 assert rem['low_has_no_original_boundary_neighbor'] is True
 assert rem['other_degrees']==[6,7,8] and rem['maximum_high_degree_vertices']==2
 assert {(x['ears'],x['degree7'],x['degree8']) for x in rem['degree_ear_profiles']}=={(0,2,0),(0,0,1),(1,1,0),(2,0,0)}
 A=3*q(3).sqrt()/4;ANG=PI/3;C0=conjugate(K,F(0));EAR=ear_cap(R,K)
 scalar=hinge.verify_case(0)
 assert scalar['status']=='PASS' and F(scalar['radius'])==R and scalar['B']==B
 assert F(scalar['required_center_norm_squared_upper'])==1-R*R
 assert F(scalar['halfside_multiplier'])==K
 assert F(scalar['hinge_slope'])==F(119,2000) and F(scalar['hinge_zero'])==F(187,2000)
 assert sine(q(F(3467,10000))).l>q(3*R).u
 assert FAN>F(63,1000)
 expected=[list(ids) for ids in itertools.combinations_with_replacement(range(3),3) if ids!=(0,0,0)]
 assert [x['ids'] for x in data['face_rows']]==expected
 face_slacks=[]
 for row in data['face_rows']:
  ids=row['ids'];upper,_,_=face_bound([labels[i] for i in ids],[0,0,0],rational(row['nu']))
  slack=(A+q(sum((charges[i] for i in ids),F(0))-credit(ids))).l-upper.u
  assert slack>0,('face',ids,F(slack,S));face_slacks.append(slack)
 expected=[(1,[x,y,z]) for x,y,z in itertools.product([0,2],[0,2],[0,1,2]) if [x,y,z].count(0)<=2]
 expected += [(2,list(ids)) for ids in itertools.product([0,2],repeat=3) if ids.count(0)<=2]
 assert [(x['selected_edges'],x['ids']) for x in data['outside_rows']]==expected
 outside_slacks=[];boundary_dominance=False
 for row in data['outside_rows']:
  m=row['selected_edges'];ids=row['ids'];edge=[0,0,kappa] if m==1 else [kappa,0,kappa]
  upper,acute,boundaries=face_bound([labels[i] for i in ids],edge,rational(row['nu']))
  boundary_dominance |= max(x.l for x in boundaries)>acute.u
  slack=(A+q(sum((charges[i] for i in ids),F(0))-credit(ids)+D[m-1])).l-upper.u
  assert slack>0,('outside',m,ids,F(slack,S));outside_slacks.append(slack)
 J=max((5-2*j)*D[0]+j*D[1] for j in range(3))
 assert [(s['high_neighbors'],s['counts']) for s in data['stars']]==PATTERNS
 poly=polygon_support(5,1,-tau);star_caps=[];cells=0
 for star in data['stars']:
  k=star['high_neighbors'];counts=star['counts'];y=rational(star['center_potential'])
  assert sum(counts)==5 and counts[1]+2*counts[2]==2*k
  assert [f['high_base_vertices'] for f in star['faces']]==[h for h in range(3) if counts[h]]
  cap=q(eps)*poly-q(y)*ANG
  for row in star['faces']:
   h=row['high_base_vertices'];ls=[y]+[-a]*h+[F(0)]*(2-h)
   normalized=[v/weight for v in ls]
   assert max(normalized)-min(normalized)<1
   z,_,_=ordinary_bound(normalized,rational(row['nu']))
   cap+=counts[h]*q(weight)*z;cells+=1
  star_caps.append(cap)
 assert len(face_slacks)==9 and len(outside_slacks)==18 and cells==8
 half=PI/B;s=sine(half);c=cosine(half);H=s*(q(R).sq()-s.sq()).sqrt()+half-s*c
 rho=c-(q(R).sq()-s.sq()).sqrt()
 outer=B*(H+q(K)*q(R)*s*rho)
 rows=[];minimum=None
 for e,degrees in PROFILES:
  high=len(degrees);ordinary=67-high;U=25+2*e
  assert sum(d-6 for d in degrees)==2-e
  for ps in itertools.product(range(4),repeat=high):
   po=B-2*e-sum(ps);assert 0<=po<=3*ordinary
   constant=(134+e)*A+(B-2*e)*C0+e*EAR
   constant+=po*(conjugate(K,b)-C0)-q(b)*((2-e)*PI+U*ANG)
   for d,pmark in zip(degrees,ps):
    constant+=pmark*(conjugate(K,b-a)-C0)+q(a*(6-d+pmark))*ANG-q(FAN*int(pmark==3)+2*interface*int(pmark>0))
   for si,(k,counts) in enumerate(PATTERNS):
    if k>high:continue
    center=constant-5*A+star_caps[si]+q(J)
    center+=q((sum(d-p for d,p in zip(degrees,ps))-2*k)*charges[0]+U*charges[1]+(6*ordinary-po+5-(15-2*k))*charges[2])
    margin=PI-(q(R).sq()*center+outer)
    assert margin.l>0,('final',e,degrees,ps,si,F(margin.l,S))
    minimum=margin.l if minimum is None else min(minimum,margin.l)
    rows.append(dict(ears=e,high_degrees=degrees,high_marked=list(ps),star_pattern=si,area_margin_lower=str(F(margin.l,S))))
 assert len(rows)==81
 return dict(status='PASS',radius=str(R),B=32,m=100,M=25,
  scope='Complete remaining M25 branch under freshly replayed same-radius premises; high-M and other boundary counts are separate',
  proposal_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),premises=premises,
  labels=list(map(str,labels)),charges=list(map(str,charges)),epsilon=str(eps),perimeter_penalty=str(tau),
  ordinary_face_supports=9,outside_face_supports=18,central_face_supports=cells,integer_profile_cases=81,
  minimum_face_slack=str(F(min(face_slacks),S)),minimum_outside_slack=str(F(min(outside_slacks),S)),
  boundary_dominates_in_supplied_rows=boundary_dominance,
  outside_total_allowance=str(J),halfside_multiplier=str(K),high_boundary_terminal_credit=str(interface),
  q3_hinge_charge=str(FAN),normalized_ear_cap_upper=str(F(EAR.u,S)),
  same_radius_boundary_scalar=scalar,required_center_norm_squared_upper=str(1-R*R),minimum_area_margin=str(F(minimum,S)),rows=rows)
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)
