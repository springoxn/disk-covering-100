#!/usr/bin/env python3
"""Exact graph-conditional covering exclusion with signed shared-edge metrics."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,sys,time
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'lower_bounds_extension_20261004'))
from exact_signed_conjugates import I,q,S,PI,triangle_support,localization_guards
from exact_angle_conjugates import marked_conjugate
from verify_potential_star_duals import sine

def edge_incidence(faces):
 table={}
 for f,tri in enumerate(faces):
  for j in range(3):table.setdefault(tuple(sorted((tri[(j+1)%3],tri[(j+2)%3]))),[]).append((f,j))
 assert all(1<=len(x)<=2 for x in table.values())
 return [(e,rows) for e,rows in sorted(table.items()) if len(rows)==2]

def verify(graph_path,certificate):
 if not __debug__:raise RuntimeError('Assertions must be enabled')
 start=time.monotonic();raw=Path(graph_path).read_bytes();assert hashlib.sha256(raw).hexdigest()==certificate['graph_sha256'];g=json.loads(raw)
 assert certificate['schema']=='signed-q0-shared-edge-v1' and g['family_id']==certificate['family_id']
 n=g['verification']['N']
 if n==27:from export_flat_N27_families import validate_graph
 elif n==26:from export_flat_N26_families import validate_graph
 else:raise ValueError('Unsupported graph branch')
 graph_check=validate_graph(g)
 assert g['interior_ids']==list(range(67)) and set(g['outer_boundary_ids'])==set(range(67,100))
 faces=g['core_q0_triangles']+g['ring_q0_triangles'];q1=g['q1_triangles'];assert len(faces)==132 and len(q1)==33
 outer=g['outer_boundary_ids'];outer_edges={tuple(sorted((outer[i],outer[(i+1)%33]))) for i in range(33)}
 for face in faces:assert all(tuple(sorted((face[i],face[(i+1)%3]))) not in outer_edges for i in range(3))
 marked=[0]*67
 for f in q1:
  a=f['interior_apex'];assert a<67 and a in f['vertices'] and sum(v<67 for v in f['vertices'])==1
  assert tuple(sorted(v for v in f['vertices'] if v!=a)) in outer_edges;marked[a]+=1
 den=certificate['denominator'];assert isinstance(den,int) and den>0
 arrays=[certificate['u'],certificate['tau'],certificate['face_multipliers']]
 assert all(isinstance(v,int) for xs in arrays for v in xs)
 assert len(arrays[0])==67 and len(arrays[2])==132
 us=[F(v,den) for v in arrays[0]]+[F(0)]*33
 incidence=edge_incidence(faces);assert len(arrays[1])==len(incidence)
 assert certificate['edge_ids']==[list(e) for e,rows in incidence]
 tau=[[F(0)]*3 for _ in faces]
 for z,(edge,((f,i),(h,j))) in zip(arrays[1],incidence):
  value=F(z,den);tau[f][i]=value;tau[h][j]=-value
  assert tuple(sorted((faces[f][(i+1)%3],faces[f][(i+2)%3])))==edge
  assert tuple(sorted((faces[h][(j+1)%3],faces[h][(j+2)%3])))==edge
  assert tau[f][i]+tau[h][j]==0
 total=q(0)
 for v in range(67):
  total+=2*PI*q(us[v])
  if marked[v]:
   assert us[v]>-F(1,2);total+=marked[v]*marked_conjugate(q(us[v]))
 minimum_guard=None
 for face,ts,eta in zip(faces,tau,arrays[2]):
  cs=[us[v] for v in face];gaps=localization_guards(cs,ts);lo=min(z.l for z in gaps)
  minimum_guard=lo if minimum_guard is None else min(minimum_guard,lo)
  total+=triangle_support(cs,ts,F(eta,den))
 radius=F(*certificate['radius']);assert 0<radius<1
 R=q(radius);theta=2*PI/33;ss=sine(theta/2)
 boundary=ss*(R.sq()-ss.sq()).sqrt()+(theta-sine(theta))/2
 upper=R.sq()*total+33*boundary;margin=PI.l-upper.u
 assert margin>0,('Signed-edge graph exclusion failed',str(F(margin,S)))
 return dict(status='PASS',scope='This specified combinatorial graph is excluded at the stated radius, with unrestricted actual center coordinates. No universal lower bound or global optimum claim.',family_id=g['family_id'],radius=str(radius),graph_sha256=certificate['graph_sha256'],graph_check=graph_check,q0_face_supports=132,cancelled_shared_edges=len(incidence),minimum_full_simplex_localization_gap=str(F(minimum_guard,S)),normalized_upper_bound=str(F(total.u,S)),area_margin=str(F(margin,S)),area_margin_approx=margin/S,seconds_reporting_only=time.monotonic()-start)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('graph');p.add_argument('certificate');p.add_argument('--output');a=p.parse_args();r=verify(a.graph,json.loads(Path(a.certificate).read_text()))
 if a.output:Path(a.output).write_text(json.dumps(r,indent=2))
 print(json.dumps(r,indent=2))
