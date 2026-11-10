#!/usr/bin/env python3
"""Exact supplied-graph metric support under explicit pending lens premises."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path[:0]=[str(ROOT),str(ROOT/'signed_edge_metric_20261004'),str(ROOT/'lower_bounds_extension_20261004')]
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine
from exact_signed_sine_full_face_support import face_bound
from exact_boundary_conjugates import arc_support
from exact_angle_conjugates import marked_conjugate
from verify_signed_graph import edge_incidence
from export_flat_N26_q3_corner_families import validate_graph,iter_graphs
R=F(11321,100000);TL=F(679,10000);DIFF=F(79,1000)
def verify(graph_path,certificate):
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 raw=Path(graph_path).read_bytes();g=json.loads(raw)
 assert hashlib.sha256(raw).hexdigest()==certificate['graph_sha256']
 assert certificate['family_id']==g['family_id'] and certificate['radius']==[11321,100000]
 assert certificate['schema']=='q3-corner-conditional-joint-v1'
 graph_check=validate_graph(g)
 generated=next(x for x in iter_graphs() if x['family_id']==g['family_id'])
 assert json.loads(json.dumps(generated))==g
 den=certificate['denominator'];assert type(den) is int and den==10**12
 arrays=[certificate[k] for k in ('u','tau','face_multipliers')]
 assert all(type(x) is int for xs in arrays for x in xs)
 assert type(certificate['arc_sum_multiplier']) is int
 assert len(arrays[0])==100 and len(arrays[2])==132
 us=[F(x,den) for x in arrays[0]];zeta=F(certificate['arc_sum_multiplier'],den)
 faces=g['core_q0_triangles']+g['ring_q0_triangles'];q1=g['q1_triangles'];outer=g['outer_boundary_ids']
 assert len(faces)==132 and len(q1)==len(outer)==33
 outer_edges={tuple(sorted((outer[i],outer[(i+1)%33]))) for i in range(33)}
 marked_edges=[tuple(sorted(v for v in f['vertices'] if v!=f['interior_apex'])) for f in q1]
 assert len(set(marked_edges))==33 and set(marked_edges)==outer_edges
 incidence=edge_incidence(faces)
 assert certificate['edge_ids']==[list(e) for e,rows in incidence] and len(arrays[1])==len(incidence)
 ts=[[F(0)]*3 for f in faces]
 for value,(edge,((f,i),(h,j))) in zip(arrays[1],incidence):
  ts[f][i]=F(value,den);ts[h][j]=-F(value,den)
  assert ts[f][i]+ts[h][j]==0
  assert tuple(sorted((faces[f][(i+1)%3],faces[f][(i+2)%3])))==edge
  assert tuple(sorted((faces[h][(j+1)%3],faces[h][(j+2)%3])))==edge
 weights=[us[v] for v in outer]
 maximum_difference=max(abs(weights[i]-weights[(i+1)%33]) for i in range(33))
 assert maximum_difference<=DIFF
 assert sine(q(TL)).u<(q(R)*F(3,5)).l
 assert F(3,5)**2>F(9,2)*DIFF
 total=2*PI*q(sum(us[:67]));minimum_guard=None;boundary_active=0
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
  beta=T*(weights[(i-1)%33]-2*w+weights[(i+1)%33])/2
  alpha=2*T*w+zeta
  cap,count=arc_support(R,alpha,beta,TL);boundary+=cap;retained+=count
 margin=PI.l-(q(T)*total+boundary).u
 assert margin>0,('Conditional area support failed',F(margin,S))
 return dict(status='PASS',scope='Algebraic supplied-graph dual conditional on all explicitly stated lens premises; no universal or unconditional graph exclusion',
  family_id=g['family_id'],radius=str(R),graph_sha256=certificate['graph_sha256'],graph_check=graph_check,
  pending_geometric_premises=['Actual normalized half-arc sine is greater than3/5','Every marked base exceeds9R/10',
    'Inner reference edges exceed3R/5 and the same orientation constant9/(4R) holds','Outer-angle absorption for neighbor differences<=79/1000',
    'The ordinary marked unequal-base cap25/16 applies'],
  q0_face_supports=132,q1_unequal_base_supports=33,boundary_arc_supports=33,cancelled_shared_edges=len(incidence),
  retained_arc_roots=retained,minimum_full_face_guard=str(minimum_guard),boundary_active_faces=boundary_active,
  maximum_neighbor_weight_difference=str(maximum_difference),half_arc_support_lower=str(TL),area_margin=str(F(margin,S)))
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('graph');parser.add_argument('certificate');args=parser.parse_args()
 print(json.dumps(verify(args.graph,json.loads(Path(args.certificate).read_text())),indent=2))
