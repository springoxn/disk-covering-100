#!/usr/bin/env python3
"""Exact B32 graph support using the stronger independently verified window."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE
sys.path[:0]=[str(ROOT),str(ROOT/'signed_edge_metric_20261004'),str(ROOT/'lower_bounds_extension_20261004'),str(ROOT/'signed_edge_metric_B32_20261004')]
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine
from exact_signed_sine_full_face_support import face_bound
from exact_boundary_conjugates import arc_support
from exact_angle_conjugates import marked_conjugate
from verify_signed_graph import edge_incidence
from export_B32_P26_F108_families import validate_graph,iter_graphs
R=F(453,4000);TL=F(307,5000);DIFF=F(11,100)
def verify(graph_path,certificate):
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 raw=Path(graph_path).read_bytes();g=json.loads(raw)
 assert hashlib.sha256(raw).hexdigest()==certificate['graph_sha256']
 assert certificate['family_id']==g['family_id'] and certificate['radius']==[453,4000]
 assert certificate['schema']=='B32-tight-turn-bootstrap-joint-v1'
 graph_check=validate_graph(g)
 generated=next(x for x in iter_graphs() if x['family_id']==g['family_id'])
 assert json.loads(json.dumps(generated))==g
 den=certificate['denominator'];assert type(den) is int and den==10**12
 arrays=[certificate[k] for k in ('u','tau','face_multipliers')]
 assert all(type(x) is int for xs in arrays for x in xs)
 assert type(certificate['arc_sum_multiplier']) is int
 assert len(arrays[0])==100 and len(arrays[2])==134
 us=[F(x,den) for x in arrays[0]];zeta=F(certificate['arc_sum_multiplier'],den)
 faces=g['core_q0_triangles']+g['ring_q0_triangles'];q1=g['q1_triangles'];outer=g['outer_boundary_ids']
 assert len(faces)==134 and len(q1)==len(outer)==32
 outer_edges={tuple(sorted((outer[i],outer[(i+1)%32]))) for i in range(32)}
 marked_edges=[tuple(sorted(v for v in f['vertices'] if v!=f['interior_apex'])) for f in q1]
 assert len(set(marked_edges))==32 and set(marked_edges)==outer_edges
 incidence=edge_incidence(faces)
 assert certificate['edge_ids']==[list(e) for e,rows in incidence] and len(arrays[1])==len(incidence)
 ts=[[F(0)]*3 for f in faces]
 for value,(edge,((f,i),(h,j))) in zip(arrays[1],incidence):
  ts[f][i]=F(value,den);ts[h][j]=-F(value,den)
  assert ts[f][i]+ts[h][j]==0
  assert tuple(sorted((faces[f][(i+1)%3],faces[f][(i+2)%3])))==edge
  assert tuple(sorted((faces[h][(j+1)%3],faces[h][(j+2)%3])))==edge
 import check_tight_B32_turn_window_0p11325 as geometry
 from verify_pure_metric import verify as verify_bootstrap
 base_path=ROOT/'signed_edge_metric_B32_20261004'/'certificates'/(g['family_id']+'.json')
 base_raw=base_path.read_bytes();assert hashlib.sha256(base_raw).hexdigest()==certificate['bootstrap_certificate_sha256']
 base=json.loads(base_raw);initial=verify_bootstrap(g,base,raw);assert initial['status']=='PASS'
 cap0=F(initial['normalized_center_upper']);assert cap0<=F(1149,5)
 old_u=[F(x,base['denominator']) for x in base['u']]
 for face in q1:assert F(-3,10)<=old_u[face['interior_apex']]<=F(-1,5)
 window=geometry.verify();assert window['status']=='PASS' and window['B']==32 and F(window['radius_upper'])>=R
 assert F(window['normalized_center_upper_bound'])==F(1149,5)
 assert F(window['half_arc_lower'])>=TL and F(window['adjacent_boundary_weight_difference_upper'])>=DIFF
 assert F(window['actual_edge_over_radius_lower'])==F(9,10) and window['marked_potential_difference_penalty']=='25/16'
 weights=[us[v] for v in outer]
 maximum_difference=max(abs(weights[i]-weights[(i+1)%32]) for i in range(32))
 assert maximum_difference<=DIFF
 total=2*PI*q(sum(us[:68]));minimum_guard=None;boundary_active=0
 for face,edge,nu in zip(faces,ts,arrays[2]):
  labels=[-us[v] for v in face]
  guard=1-(max(labels)-min(labels)+sum((max(-t,F(0)) for t in edge),F(0))/2)
  assert guard>0
  minimum_guard=guard if minimum_guard is None else min(minimum_guard,guard)
  cap,acute,bounds=face_bound(labels,edge,F(nu,den))
  boundary_active+=int(max(x.l for x in bounds)>acute.u)
  total+=cap-PI*q(sum((us[v] for v in face),F(0))/3)
 for face in q1:
  apex=face['interior_apex'];a,b=[v for v in face['vertices'] if v!=apex]
  mean=(us[a]+us[b])/2;tilt=us[apex]-mean;difference=us[a]-us[b]
  assert F(-1,2)<tilt<3
  total+=marked_conjugate(q(tilt))-PI*q(mean)+q(F(25,16)*difference*difference)
 T=R*R;boundary=PI*q(zeta+T*sum(weights));retained=0
 for i,w in enumerate(weights):
  beta=T*(weights[(i-1)%32]-2*w+weights[(i+1)%32])/2
  alpha=2*T*w+zeta
  cap,count=arc_support(R,alpha,beta,TL);boundary+=cap;retained+=count
 margin=PI.l-(q(T)*total+boundary).u
 assert margin>0,('Conditional area support failed',F(margin,S))
 return dict(status='PASS',scope='This supplied B32 catalog graph is excluded at the stated radius using an independently replayed pure support/window; complete branch reduction remains separate',
  family_id=g['family_id'],radius=str(R),graph_sha256=certificate['graph_sha256'],graph_check=graph_check,
  pure_normalized_center_cap=str(cap0),geometry_status=window['status'],
  q0_face_supports=134,q1_unequal_base_supports=32,boundary_arc_supports=32,cancelled_shared_edges=len(incidence),
  retained_arc_roots=retained,minimum_full_face_guard=str(minimum_guard),boundary_active_faces=boundary_active,
  maximum_neighbor_weight_difference=str(maximum_difference),half_arc_support_lower=str(TL),area_margin=str(F(margin,S)))
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('graph');parser.add_argument('certificate');args=parser.parse_args()
 print(json.dumps(verify(args.graph,json.loads(Path(args.certificate).read_text())),indent=2))

