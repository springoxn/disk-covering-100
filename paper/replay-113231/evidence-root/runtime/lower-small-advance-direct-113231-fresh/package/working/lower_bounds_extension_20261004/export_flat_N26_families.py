#!/usr/bin/env python3
"""Validated marked-fringe extensions of the complete flat N26 core catalog.

Default output is a compact graph index. Use --family ID for one full graph,
or import iter_graphs() to receive the preferred face/vertex schema directly.
"""
from collections import defaultdict,Counter
from pathlib import Path
import hashlib
import json
import sys

CATALOG=Path(__file__).with_name('flat_N26_core_catalog.json')


def automorphisms(core):
    points=[tuple(p) for p in core['axial_vertices']]
    ids={p:i for i,p in enumerate(points)}
    original=tuple(sorted(tuple(sorted(points[i] for i in tri)) for tri in core['triangles']))
    maps=[]
    for reflected in (False,True):
        for rotation in range(6):
            image=[]
            for x,y in points:
                if reflected:
                    x,y=y,x
                for unused in range(rotation):
                    x,y=-y,x+y
                image.append((x,y))
            xmin=min(p[0] for p in image)
            ymin=min(p[1] for p in image)
            image=[(x-xmin,y-ymin) for x,y in image]
            transformed=tuple(sorted(tuple(sorted(image[i] for i in tri)) for tri in core['triangles']))
            if transformed==original:
                maps.append([ids[p] for p in image])
    assert maps
    return maps


def placements(core):
    ring=core['boundary_ids']
    choices=[i for i,q in enumerate(core['boundary_face_incidences']) if q in (3,4)]
    autos=automorphisms(core)
    groups=defaultdict(list)
    for position in choices:
        orbit=min(a[ring[position]] for a in autos)
        groups[orbit].append(position)
    return [min(ps) for ps in groups.values()],len(choices),len(autos),groups


def validate_graph(graph):
    faces=graph['core_q0_triangles']+graph['ring_q0_triangles']+[x['vertices'] for x in graph['q1_triangles']]
    adjacency=defaultdict(set)
    edges=defaultdict(list)
    links=defaultdict(lambda:defaultdict(set))
    for tri in faces:
        assert len(set(tri))==3
        for i in range(3):
            v,a,b=tri[i],tri[(i+1)%3],tri[(i+2)%3]
            links[v][a].add(b)
            links[v][b].add(a)
            adjacency[v].update((a,b))
            edges[tuple(sorted((v,a)))].append((v,a))
    outer=graph['outer_boundary_ids']
    boundary_edges={tuple(sorted((outer[i],outer[(i+1)%33]))) for i in range(33)}
    assert len(faces)==165 and len(edges)==264 and set(adjacency)==set(range(100))
    for e,orientations in edges.items():
        if e in boundary_edges:
            assert len(orientations)==1
        else:
            assert len(orientations)==2 and orientations[0]==tuple(reversed(orientations[1]))
    assert boundary_edges=={e for e,fs in edges.items() if len(fs)==1}
    for v,link in links.items():
        start=next(iter(link))
        reached={start}
        todo=[start]
        while todo:
            u=todo.pop()
            for w in link[u]-reached:
                reached.add(w)
                todo.append(w)
        assert reached==set(link)
        ds=Counter(len(x) for x in link.values())
        if v<67:
            assert set(ds)=={2}
        else:
            assert ds[1]==2 and set(ds)<={1,2}
    special=graph['selected_degree_seven_vertex']
    assert all(len(adjacency[v])==(7 if v==special else 6) for v in range(67))
    q=Counter(x['interior_apex'] for x in graph['q1_triangles'])
    assert len(graph['q1_triangles'])==33 and len(graph['core_q0_triangles'])==106
    assert len(graph['ring_q0_triangles'])==26 and max(q.values())<=2
    assert sum(4-len(adjacency[v]) for v in outer)==7
    return {'vertices':100,'edges':264,'faces':165,'B':33,'I':67,'N':26,
            'marked_apex_count_K':len(q),'interior_degree_histogram':{'6':66,'7':1},
            'outer_degree_histogram':dict(sorted(Counter(len(adjacency[v]) for v in outer).items())),
            'oriented_edge_check':'PASS','all_vertex_links_check':'PASS'}


def build_graph(core,position):
    ring=core['boundary_ids']
    incidences=core['boundary_face_incidences']
    assert incidences[position] in (3,4)
    p=[4-q for q in incidences]
    assert sum(p)==32 and min(p)>=0 and max(p)<=2
    p[position]+=1
    assert sum(p)==33 and max(p)<=2
    ring_faces=[]
    q1=[]
    offset=0
    for i,vi in enumerate(ring):
        chain=[67+(offset+j)%33 for j in range(p[i]+1)]
        for a,b in zip(chain,chain[1:]):
            q1.append({'vertices':[a,b,vi],'interior_apex':vi})
        ring_faces.append([vi,chain[-1],ring[(i+1)%26]])
        offset+=p[i]
    assert offset==33
    graph={'family_id':core['core_id']+'_special_'+str(position).zfill(2),
           'core_id':core['core_id'],'selected_ring_position':position,
           'selected_degree_seven_vertex':ring[position],
           'selected_degree_seven_type':[p[position],incidences[position]+2],
           'outer_boundary_ids':list(range(67,100)),'interior_ids':list(range(67)),
           'ring_ids':ring,'q1_fan_sizes_in_ring_order':p,
           'core_q0_triangles':core['triangles'],'ring_q0_triangles':ring_faces,
           'q1_triangles':q1,
           'coordinate_warning':'The core axial labels describe only a combinatorial development, not actual covering centers'}
    graph['verification']=validate_graph(graph)
    return graph


def iter_graphs():
    data=json.loads(CATALOG.read_text())
    assert data['status']=='PASS' and data['core_count']==57
    for core in data['cores']:
        positions,unused,unused2,unused3=placements(core)
        for position in sorted(positions):
            yield build_graph(core,position)


def index():
    data=json.loads(CATALOG.read_text())
    rows=[]
    raw=0
    for core in data['cores']:
        positions,n,aut_count,groups=placements(core)
        raw+=n
        for position in sorted(positions):
            graph=build_graph(core,position)
            rows.append({k:graph[k] for k in ('family_id','core_id','selected_ring_position',
                                             'selected_degree_seven_vertex','selected_degree_seven_type','verification')})
    return {'status':'PASS','core_count':len(data['cores']),'raw_degree_seven_placements':raw,
            'symmetry_representative_families':len(rows),
            'core_catalog_sha256':hashlib.sha256(CATALOG.read_bytes()).hexdigest(),
            'families':rows,
            'scope':'Conditional flat N26/F106 critical graph family only, not all possible disk-covering graphs'}


if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--family':
        matches=[g for g in iter_graphs() if g['family_id']==sys.argv[2]]
        assert len(matches)==1
        print(json.dumps(matches[0],separators=(',',':')))
    else:
        print(json.dumps(index(),separators=(',',':')))
