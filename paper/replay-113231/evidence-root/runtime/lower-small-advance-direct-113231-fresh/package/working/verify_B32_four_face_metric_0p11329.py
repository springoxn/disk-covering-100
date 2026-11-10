#!/usr/bin/env python3
"""Four exact face supports for the conditional B32 all-six P26/F108 core."""
from fractions import Fraction as F
import json
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_signed_sine_full_face_support import face_bound
from exact_linear_halfside_marked_conjugate import conjugate
import verify_exact_lens_boundary_0p11322 as boundary
R=F(11329,100000);B=32;K=F(11,25)
LR=F(-20663069056,10**11);LB=F(-72993038978,10**11);TAU=F(6623191134,10**10)
PATTERNS=[('DDD',[F(0)]*3,[F(0)]*3,62,F(-1,2)),
 ('DDR',[F(0),F(0),LR],[F(0)]*3,20,F(-56597508864,10**11)),
 ('DRR',[F(0),LR,LR],[-TAU,F(0),F(0)],26,F(-75767205590,10**11)),
 ('BRR',[LR,LR,LB],[F(0),F(0),TAU],26,F(-75767203850,10**11))]
def verify():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 boundary.R=R;boundary.B=B;boundary.K=K;boundary.CURVATURE=F(0)
 envelope=boundary.verify();assert envelope['status']=='PASS'
 assert envelope['radius']==str(R) and envelope['B']==B and F(envelope['halfside_multiplier'])==K
 assert F(envelope['required_center_norm_squared_upper'])==1-R*R
 assert 62+20+26==108 and 3*62+2*20+26==42*6
 assert 20+2*26==3*108-42*6==72
 assert sum(row[3] for row in PATTERNS)==134
 center=q(0);rows=[]
 for name,labels,edges,count,nu in PATTERNS:
  guard=1-(max(labels)-min(labels)+sum((max(-x,F(0)) for x in edges),F(0))/2)
  assert guard>0
  cap,acute,edgecaps=face_bound(labels,edges,nu)
  assert len(edgecaps)==3 and all(cap.u>=z.u for z in [acute]+edgecaps)
  center+=count*cap
  rows.append(dict(pattern=name,multiplicity=count,guard=str(guard),support_upper=str(F(cap.u,S))))
 center+=B*conjugate(K,LR-LB)-q(B*LR)*PI/3+q(LB)*(2*PI+26*PI/3)
 rr=q(R);mu=PI/B;s=sine(mu);rho=cosine(mu)-(rr.sq()-s.sq()).sqrt()
 outer=B*(mu-s*rho+q(K)*rr*s*rho)
 margin=PI-rr.sq()*center-outer;assert margin.l>0
 return dict(status='PASS',radius=str(R),B=B,m=100,
  scope='Conditional all-six simple chordless P26/F108 core with the standard26-face annulus. No catalog completeness or universal radius theorem is asserted.',
  required_center_norm_squared_upper=str(1-R*R),halfside_multiplier=str(K),
  core_vertices=68,core_boundary=26,core_faces=108,deep_vertices=42,
  shared_edge_pairs=26,shared_edge_multiplier=str(TAU),corner_potentials=['0',str(LR),str(LB)],
  face_supports=4,face_cases=rows,normalized_boundary_envelope=envelope,
  normalized_center_upper=str(F(center.u,S)),outer_boundary_upper=str(F(outer.u,S)),
  area_margin=str(F(margin.l,S)),graph_catalog_used=False,boundary_turn_window_used=False)
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

