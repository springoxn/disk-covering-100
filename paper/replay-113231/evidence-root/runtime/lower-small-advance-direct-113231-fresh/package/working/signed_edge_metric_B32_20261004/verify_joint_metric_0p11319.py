#!/usr/bin/env python3
"""Exact graph-conditional exclusion with shared metrics and boundary angles."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,sys,time
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'lower_bounds_extension_20261004'));sys.path.insert(0,str(ROOT/'signed_edge_metric_20261004'))
from exact_signed_conjugates import I,q,S,PI
from wide_metric_conjugates import triangle_support,localization_guards
from exact_boundary_conjugates import arc_support
from exact_angle_conjugates import marked_conjugate
from verify_signed_graph import edge_incidence
import check_uniform_B32_boundary_window_0p1132 as geometry

def verify(graph_path,certificate):
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    start=time.monotonic();raw=Path(graph_path).read_bytes();assert hashlib.sha256(raw).hexdigest()==certificate['graph_sha256'];g=json.loads(raw)
    assert certificate['schema']=='B32-joint-boundary-metric-v1' and g['family_id']==certificate['family_id']
    from export_B32_P26_F108_families import validate_graph
    graph_check=validate_graph(g)
    assert g['interior_ids']==list(range(68)) and set(g['outer_boundary_ids'])==set(range(68,100))
    faces=g['core_q0_triangles']+g['ring_q0_triangles'];q1=g['q1_triangles'];assert len(faces)==134 and len(q1)==32
    outer=g['outer_boundary_ids'];outer_edges={tuple(sorted((outer[i],outer[(i+1)%32]))) for i in range(32)}
    for face in faces:assert all(tuple(sorted((face[i],face[(i+1)%3]))) not in outer_edges for i in range(3))
    marked_edges=[]
    for face in q1:
        a=face['interior_apex'];assert a<68 and a in face['vertices'] and sum(v<68 for v in face['vertices'])==1
        marked_edges.append(tuple(sorted(v for v in face['vertices'] if v!=a)))
    assert set(marked_edges)==outer_edges
    den=certificate['denominator'];assert type(den) is int and den>0
    arrays=[certificate['u'],certificate['tau'],certificate['face_multipliers'],certificate['pure_face_multipliers']]
    assert all(type(v) is int for xs in arrays for v in xs)
    assert len(arrays[0])==100 and len(arrays[2])==len(arrays[3])==134
    assert type(certificate['arc_sum_multiplier']) is int
    us=[F(v,den) for v in arrays[0]];zeta=F(certificate['arc_sum_multiplier'],den)
    incidence=edge_incidence(faces);assert len(arrays[1])==len(incidence)
    assert certificate['edge_ids']==[list(e) for e,rows in incidence]
    ts=[[F(0)]*3 for _ in faces]
    for z,(edge,((f,i),(h,j))) in zip(arrays[1],incidence):
        ts[f][i]=F(z,den);ts[h][j]=-F(z,den)
        assert tuple(sorted((faces[f][(i+1)%3],faces[f][(i+2)%3])))==edge
        assert tuple(sorted((faces[h][(j+1)%3],faces[h][(j+2)%3])))==edge
        assert ts[f][i]+ts[h][j]==0
    radius=F(*certificate['radius']);assert radius==F(11319,100000)
    pure=2*PI*q(sum(us[:68]));pure_us=us[:68]+[F(0)]*32
    for face,edge,eta in zip(faces,ts,arrays[3]):
        pure+=triangle_support([pure_us[v] for v in face],edge,F(eta,den))
    for face in q1:
        apex=face['interior_apex'];assert F(-3,10)<=us[apex]<=F(-1,5)
        pure+=marked_conjugate(q(us[apex]))
    assert pure.u<=230*S,'The geometry-window pure-center premise failed'
    premise=geometry.verify()
    assert premise['status']=='PASS' and F(premise['radius_upper'])>=radius
    T=radius*radius;weights=[us[v] for v in outer]
    maximum_difference=max(abs(weights[i]-weights[(i+1)%32]) for i in range(32));assert maximum_difference<=F(1,40)
    total=2*PI*q(sum(us[:68]));minimum_guard=None
    for face,edge,eta in zip(faces,ts,arrays[2]):
        cs=[us[v] for v in face];gaps=localization_guards(cs,edge);lo=min(z.l for z in gaps)
        minimum_guard=lo if minimum_guard is None else min(minimum_guard,lo)
        total+=triangle_support(cs,edge,F(eta,den))
    for face in q1:
        apex=face['interior_apex'];a,b=[v for v in face['vertices'] if v!=apex]
        mean=(us[a]+us[b])/2;tilt=us[apex]-mean;difference=us[a]-us[b]
        total+=marked_conjugate(q(tilt))-PI*q(mean)+q(F(25,16)*difference*difference)
    boundary=PI*q(zeta+T*sum(weights));root_count=0
    for i,w in enumerate(weights):
        b=T*(weights[(i-1)%32]-2*w+weights[(i+1)%32])/2;a=2*T*w+zeta
        support,roots=arc_support(radius,a,b);boundary+=support;root_count+=roots
    upper=q(T)*total+boundary;margin=PI.l-upper.u
    assert margin>0,('Joint graph exclusion failed',str(F(margin,S)))
    return dict(status='PASS',scope='This specified no-ear graph is excluded at the reported radius, with arbitrary actual coordinates. No complete graph catalog or universal improvement is claimed.',family_id=g['family_id'],radius=str(radius),graph_sha256=certificate['graph_sha256'],graph_check=graph_check,geometry_status=premise['status'],pure_normalized_center_upper=str(F(pure.u,S)),q0_face_supports=134,q1_unequal_base_supports=32,cancelled_shared_edges=len(incidence),boundary_arc_supports=32,retained_quadratic_roots=root_count,maximum_neighbor_weight_difference=str(maximum_difference),minimum_localization_gap=str(F(minimum_guard,S)),area_margin=str(F(margin,S)),area_margin_approx=margin/S,seconds_reporting_only=time.monotonic()-start)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('graph');p.add_argument('certificate');p.add_argument('--output');a=p.parse_args();result=verify(a.graph,json.loads(Path(a.certificate).read_text()))
    if a.output:Path(a.output).write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
