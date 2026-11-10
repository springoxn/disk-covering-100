#!/usr/bin/env python3
"""Full graph export of the 16 reduced B32 flat-core families.

Default output is a compact index. Use --family ID for one graph, or
import iter_graphs() for the complete oriented face schema.
"""
from collections import defaultdict,Counter
from pathlib import Path
import hashlib,json,sys

CATALOG=Path(__file__).with_name('B32_P26_F108_core_catalog.json')


def validate_graph(graph):
    assert graph['interior_ids']==list(range(68))
    assert graph['outer_boundary_ids']==list(range(68,100))
    faces=graph['core_q0_triangles']+graph['ring_q0_triangles']+[x['vertices'] for x in graph['q1_triangles']]
    adjacency=defaultdict(set);edges=defaultdict(list)
    links=defaultdict(lambda:defaultdict(set))
    for tri in faces:
        assert len(set(tri))==3
        for i in range(3):
            v,a,b=tri[i],tri[(i+1)%3],tri[(i+2)%3]
            links[v][a].add(b);links[v][b].add(a)
            adjacency[v].update((a,b))
            edges[tuple(sorted((v,a)))].append((v,a))
    outer=graph['outer_boundary_ids']
    boundary_edges={tuple(sorted((outer[i],outer[(i+1)%32]))) for i in range(32)}
    assert len(faces)==166 and len(edges)==265 and set(adjacency)==set(range(100))
    for edge,orientations in edges.items():
        if edge in boundary_edges:assert len(orientations)==1
        else:assert len(orientations)==2 and orientations[0]==tuple(reversed(orientations[1]))
    assert boundary_edges=={edge for edge,uses in edges.items() if len(uses)==1}
    reached={0};todo=[0]
    while todo:
        v=todo.pop()
        for w in adjacency[v]-reached:reached.add(w);todo.append(w)
    assert len(reached)==100
    for v,link in links.items():
        start=next(iter(link));seen={start};todo=[start]
        while todo:
            a=todo.pop()
            for b in link[a]-seen:seen.add(b);todo.append(b)
        assert seen==set(link)
        degrees=Counter(len(x) for x in link.values())
        if v<68:assert set(degrees)=={2}
        else:assert degrees[1]==2 and set(degrees)<={1,2}
    assert all(len(adjacency[v])==6 for v in range(68))
    marked=Counter(x['interior_apex'] for x in graph['q1_triangles'])
    assert len(graph['core_q0_triangles'])==108
    assert len(graph['ring_q0_triangles'])==26 and len(graph['q1_triangles'])==32
    assert max(marked.values())<=2
    for f in graph['q1_triangles']:
        apex=f['interior_apex'];assert apex<68 and apex in f['vertices']
        assert tuple(sorted(v for v in f['vertices'] if v!=apex)) in boundary_edges
    assert sum(4-len(adjacency[v]) for v in outer)==6
    return {'vertices':100,'edges':265,'faces':166,'B':32,'I':68,'N':26,
            'marked_apex_count_K':len(marked),'interior_degree_histogram':{'6':68},
            'max_marked_fan_size':max(marked.values()),
            'outer_degree_histogram':dict(sorted(Counter(len(adjacency[v]) for v in outer).items())),
            'oriented_edge_check':'PASS','all_vertex_links_check':'PASS','connected':'PASS'}


def build_graph(core):
    ring=core['boundary_ids'];hs=core['boundary_face_incidences']
    p=[4-h for h in hs]
    assert len(ring)==26 and sum(p)==32 and min(p)>=0 and max(p)<=2
    ring_faces=[];q1=[];offset=0
    for i,vi in enumerate(ring):
        chain=[68+(offset+j)%32 for j in range(p[i]+1)]
        for a,b in zip(chain,chain[1:]):
            q1.append({'vertices':[a,b,vi],'interior_apex':vi})
        ring_faces.append([vi,chain[-1],ring[(i+1)%26]])
        offset+=p[i]
    assert offset==32
    graph={'family_id':core['core_id'],'core_id':core['core_id'],
           'outer_boundary_ids':list(range(68,100)),'interior_ids':list(range(68)),
           'ring_ids':ring,'q1_fan_sizes_in_ring_order':p,
           'core_q0_triangles':core['triangles'],'ring_q0_triangles':ring_faces,
           'q1_triangles':q1,'core_axial_labels':core['axial_vertices'],
           'coordinate_warning':'Axial labels specify only a combinatorial unit-triangle development, not actual covering centers'}
    graph['verification']=validate_graph(graph)
    return graph


def iter_graphs():
    data=json.loads(CATALOG.read_text())
    assert data['status']=='PASS' and data['core_count']==16
    for core in data['cores']:yield build_graph(core)


def index():
    graphs=list(iter_graphs())
    return {'status':'PASS','families_count':len(graphs),
            'core_catalog_sha256':hashlib.sha256(CATALOG.read_bytes()).hexdigest(),
            'families':[{'family_id':g['family_id'],'verification':g['verification']} for g in graphs],
            'scope':'Complete conditional reduced B32 family only; all16 graphs still need metric exclusion'}


if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--family':
        matches=[g for g in iter_graphs() if g['family_id']==sys.argv[2]]
        assert len(matches)==1
        print(json.dumps(matches[0],separators=(',',':')))
    else:print(json.dumps(index(),indent=2))
