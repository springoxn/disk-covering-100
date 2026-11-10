#!/usr/bin/env python3
"""Exact signed-edge full-domain exclusion of a supplied B32 graph."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,sys,time
ROOT=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(ROOT),str(ROOT/'lower_bounds_extension_20261004'),str(ROOT/'signed_edge_metric_20261004')]
from exact_signed_conjugates import I,q,S,PI
from wide_metric_conjugates import triangle_support,localization_guards
from exact_angle_conjugates import marked_conjugate
from verify_potential_star_duals import sine
from verify_signed_graph import edge_incidence
from export_B32_P26_F108_families import validate_graph

def verify(graph,certificate,raw=None):
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    started=time.monotonic()
    if raw is None:raw=json.dumps(graph,indent=2).encode()
    else:assert json.loads(raw)==graph
    assert hashlib.sha256(raw).hexdigest()==certificate['graph_sha256']
    assert certificate['schema']=='B32-pure-signed-metric-v1' and certificate['family_id']==graph['family_id']
    check=validate_graph(graph)
    assert graph['interior_ids']==list(range(68)) and graph['outer_boundary_ids']==list(range(68,100))
    faces=graph['core_q0_triangles']+graph['ring_q0_triangles'];marked=graph['q1_triangles'];assert len(faces)==134 and len(marked)==32
    outer=graph['outer_boundary_ids'];boundary_edges={tuple(sorted((outer[i],outer[(i+1)%32]))) for i in range(32)}
    for face in faces:assert all(tuple(sorted((face[i],face[(i+1)%3]))) not in boundary_edges for i in range(3))
    apices=[0]*68;marked_edges=[]
    for face in marked:
        apex=face['interior_apex'];assert type(apex) is int and 0<=apex<68 and apex in face['vertices']
        assert sum(v<68 for v in face['vertices'])==1
        marked_edges.append(tuple(sorted(v for v in face['vertices'] if v!=apex)));apices[apex]+=1
    assert set(marked_edges)==boundary_edges
    den=certificate['denominator'];assert type(den) is int and den>0
    arrays=[certificate['u'],certificate['tau'],certificate['face_multipliers']]
    assert len(arrays[0])==68 and len(arrays[2])==134
    assert all(type(v) is int for row in arrays for v in row)
    us=[F(x,den) for x in arrays[0]]+[F(0)]*32
    incidence=edge_incidence(faces);assert len(arrays[1])==len(incidence)
    assert certificate['edge_ids']==[list(edge) for edge,rows in incidence]
    ts=[[F(0)]*3 for _ in faces]
    for value,(edge,((f,i),(h,j))) in zip(arrays[1],incidence):
        ts[f][i]=F(value,den);ts[h][j]=-F(value,den)
        assert tuple(sorted((faces[f][(i+1)%3],faces[f][(i+2)%3])))==edge
        assert tuple(sorted((faces[h][(j+1)%3],faces[h][(j+2)%3])))==edge
        assert ts[f][i]+ts[h][j]==0
    total=2*PI*q(sum(us[:68]));minimum=None
    for v,count in enumerate(apices):
        if count:total+=count*marked_conjugate(q(us[v]))
    for face,edge,eta in zip(faces,ts,arrays[2]):
        corners=[us[v] for v in face];guards=localization_guards(corners,edge);gap=min(x.l for x in guards);minimum=gap if minimum is None else min(minimum,gap)
        total+=triangle_support(corners,edge,F(eta,den))
    radius=F(*certificate['radius']);assert radius==F(2829,25000)
    R=q(radius);theta=2*PI/32;ss=sine(theta/2);H=ss*(R.sq()-ss.sq()).sqrt()+(theta-sine(theta))/2
    margin=PI.l-(R.sq()*total+32*H).u
    assert margin>0,('B32 graph metric exclusion failed',graph['family_id'],str(F(margin,S)))
    return dict(status='PASS',scope='This supplied B32 graph is excluded with unrestricted actual center coordinates; catalog and universal branch reduction are separate premises',family_id=graph['family_id'],radius=str(radius),graph_sha256=certificate['graph_sha256'],graph_check=check,q0_supports=134,q1_supports=32,cancelled_edges=len(incidence),normalized_center_upper=str(F(total.u,S)),minimum_localization_gap=str(F(minimum,S)),area_margin=str(F(margin,S)),seconds_reporting_only=time.monotonic()-started)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('graph');a.add_argument('certificate');v=a.parse_args();raw=Path(v.graph).read_bytes();print(json.dumps(verify(json.loads(raw),json.loads(Path(v.certificate).read_text()),raw),indent=2))
