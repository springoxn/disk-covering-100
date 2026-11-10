#!/usr/bin/env python3
"""Exact coherent five-star replacement for the frozen B33 M25 face row."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,itertools,json
from verify_star_lp_duals import q,S,PI
from exact_signed_sine_full_face_support import face_bound
from exact_range_one_face_support import face_bound as old_face_bound
from polygon_star_perimeter_support import support as polygon_support
ROOT=Path(__file__).resolve().parent
A=3*q(3).sqrt()/4;ANG=PI/3
def verify():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 table=ROOT/'hinge_B33_lowM_0p11322_proposals.json'
 row=json.loads(table.read_text())['rows'][-1]
 assert row['branch']=='M25' and row['M']==25 and row['deep_witnesses']==1
 assert row['denominator']==10**10 and row['potential_denominator']==10**8
 assert [row[k] for k in ('high_potential','boundary_potential','deep_potential')]==[-33285141,-27065539,30011312]
 assert [row[k] for k in ('charge_a','charge_b','charge_0','charge_deep','interface_a','interface_0','interface_deep')]==[242021094,138623045,500,343633517,195349539,0,0]
 labels=[F(row['high_potential'],10**8),F(row['boundary_potential'],10**8),F(0),F(row['deep_potential'],10**8)]
 charges=[F(row[k],10**10) for k in ('charge_a','charge_b','charge_0','charge_deep')]
 credit=F(row['interface_a'],10**10)
 def original_allowance(ids):
  return A+q(sum((charges[i] for i in ids),F(0))-credit*sum({ids[i],ids[(i+1)%3]}=={0,1} for i in range(3)))
 triples=[t for t in itertools.combinations_with_replacement(range(4),3) if not(1 in t and 3 in t)]
 assert [tuple(z['indices']) for z in row['faces']]==triples and len(triples)==16
 for cell in row['faces']:
  ids=cell['indices'];bound,_,_=old_face_bound([labels[i] for i in ids],F(cell['nu'],10**10))
  assert original_allowance(ids).l>bound.u
 ppath=ROOT/'B33_M25_coherent_five_proposal.json';proposal=json.loads(ppath.read_text())
 assert proposal['schema']=='B33-M25-coherent-five-replacement-v1'
 den=proposal['denominator'];assert type(den) is int and den==10**10
 assert proposal['epsilon']==[3,10] and proposal['tau']==[13,10]
 eps=F(3,10);tau=F(13,10);weight=1-eps;kappa=eps*tau
 expected=[]
 for n in (1,2):
  idslist=itertools.product([0,2],[0,2],[0,1,2]) if n==1 else itertools.product([0,2],repeat=3)
  expected += [(n,list(ids)) for ids in idslist]
 assert [(z['selected_edges'],z['labels']) for z in proposal['outside']]==expected
 outside={1:[],2:[]}
 for cell in proposal['outside']:
  n=cell['selected_edges'];ids=cell['labels'];nu=cell['nu'];assert type(nu) is int
  edges=[F(0),F(0),kappa] if n==1 else [kappa,F(0),kappa]
  cap,acute,boundary=face_bound([labels[i] for i in ids],edges,F(nu,den))
  assert len(boundary)==3 and all(cap.u>=z.u for z in [acute]+boundary)
  difference=F(cap.u-original_allowance(ids).l,S)
  outside[n].append(dict(labels=ids,extra_upper=str(difference)))
 D1=max(F(z['extra_upper']) for z in outside[1]);D2=max(F(z['extra_upper']) for z in outside[2])
 J=max((5-2*j)*D1+j*D2 for j in range(3))
 cycles=set()
 for bits in itertools.product((0,1),repeat=5):
  if sum(bits)>3:continue
  counts=tuple(sum(bits[i]+bits[(i+1)%5]==h for i in range(5)) for h in range(3))
  cycles.add((sum(bits),counts))
 received={(z['high_neighbors'],tuple(z['counts'])) for z in proposal['central']}
 assert received==cycles and len(received)==len(proposal['central'])==6
 star=polygon_support(5,eps,-eps*tau);gains=[];cases=[];face_checks=0
 for case in proposal['central']:
  k=case['high_neighbors'];counts=case['counts']
  assert sum(counts)==5 and counts[1]+2*counts[2]==2*k
  rawy=case['center_potential'];assert type(rawy) is int;y=F(rawy,den)
  assert [z['high_base_corners'] for z in case['cells']]==[h for h,n in enumerate(counts) if n]
  joint=star-q(y-labels[3])*ANG
  for cell in case['cells']:
   h=cell['high_base_corners'];nu=cell['nu'];assert type(nu) is int
   residual=[y]+[labels[0]]*h+[F(0)]*(2-h)
   assert max(residual)-min(residual)<weight
   cap,acute,boundary=face_bound([x/weight for x in residual],[F(0)]*3,F(nu,den))
   joint+=counts[h]*q(weight)*cap;face_checks+=1
  old=5*A+q(5*charges[3]+2*k*charges[0]+(10-2*k)*charges[2])
  gain=old-joint-q(J);assert gain.l>q(F(68,1000)).u
  gains.append(F(gain.l,S));cases.append(dict(high_neighbors=k,counts=counts,free_center_potential=str(y),
   central_upper=str(F(joint.u,S)),original_central_allowance_lower=str(F(old.l,S)),
   normalized_gain_lower=str(F(gain.l,S))))
 return dict(status='PASS',scope='Local coherent face-row replacement only. Requires a selected deep degree5, no other positive-labelled site in its outside faces, and at most3 high-labelled neighbors; global radius/profile premises are separate.',
  reference_proposal_sha256=hashlib.sha256(table.read_bytes()).hexdigest(),local_proposal_sha256=hashlib.sha256(ppath.read_bytes()).hexdigest(),
  epsilon=str(eps),polygon_halfperimeter_penalty=str(tau),cancelled_outside_halfedge_coefficient=str(kappa),
  original_face_checks=16,neighbor_cycles=6,residual_central_face_checks=face_checks,
  one_edge_outside_signatures=12,two_edge_outside_signatures=8,
  original_high_boundary_credit_retained=str(credit),outside_D1=str(D1),outside_D2=str(D2),outside_total_upper=str(J),
  minimum_normalized_gain=str(min(gains)),cases=cases,outside=outside)
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

