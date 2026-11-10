#!/usr/bin/env python3
"""Graph generator for the compact N27 core-witness catalog."""
from collections import defaultdict,Counter
from pathlib import Path
import hashlib
import json
import sys
from lattice_mesh_utils import region_faces,canonical,mesh

CATALOG=Path(__file__).with_name('flat_N27_core_catalog.json')

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
    assert all(len(adjacency[v])==6 for v in range(67))
    q=Counter(x['interior_apex'] for x in graph['q1_triangles'])
    assert len(graph['q1_triangles'])==33 and len(graph['core_q0_triangles'])==105
    assert len(graph['ring_q0_triangles'])==27 and max(q.values())<=2
    assert sum(4-len(adjacency[v]) for v in outer)==6
    return {'vertices':100,'edges':264,'faces':165,'B':33,'I':67,'N':27,
            'marked_apex_count_K':len(q),'interior_degree_histogram':{'6':67},
            'outer_degree_histogram':dict(sorted(Counter(len(adjacency[v]) for v in outer).items())),
            'oriented_edge_check':'PASS','all_vertex_links_check':'PASS'}


def iter_graphs():
    data=json.loads(CATALOG.read_text())
    assert data['status']=='PASS' and data['core_count']==len(data['core_witnesses'])
    region_cache={}
    for index,(ri,deleted) in enumerate(data['core_witnesses']):
        if ri not in region_cache:
            region_cache[ri]=region_faces(data['containing_regions'][ri])[0]
        deleted=set(deleted)
        remaining=[tri for i,tri in enumerate(region_cache[ri]) if i not in deleted]
        unused,oriented=canonical(remaining)
        core=mesh(oriented,None,67,105,27,{2,3,4})
        assert core is not None
        ring=core['boundary_ids']
        p=[4-q for q in core['boundary_face_incidences']]
        assert sum(p)==33 and min(p)>=0 and max(p)<=2
        q1=[]
        connectors=[]
        offset=0
        for i,vi in enumerate(ring):
            chain=[67+(offset+j)%33 for j in range(p[i]+1)]
            for a,b in zip(chain,chain[1:]):
                q1.append({'vertices':[a,b,vi],'interior_apex':vi})
            connectors.append([vi,chain[-1],ring[(i+1)%27]])
            offset+=p[i]
        assert offset==33
        graph={'family_id':'flat_N27_'+str(index).zfill(4),
               'outer_boundary_ids':list(range(67,100)),'interior_ids':list(range(67)),
               'ring_ids':ring,'q1_fan_sizes_in_ring_order':p,
               'core_q0_triangles':core['triangles'],'ring_q0_triangles':connectors,
               'q1_triangles':q1,
               'coordinate_warning':'The source axial coordinates are combinatorial development labels, not disk centers'}
        graph['verification']=validate_graph(graph)
        yield graph


def verify_all():
    histogram=Counter()
    ids_by_K=defaultdict(list)
    count=0
    for graph in iter_graphs():
        K=graph['verification']['marked_apex_count_K']
        histogram[K]+=1
        ids_by_K[K].append(graph['family_id'])
        count+=1
    return {'status':'PASS','graph_count':count,
            'core_catalog_sha256':hashlib.sha256(CATALOG.read_bytes()).hexdigest(),
            'marked_apex_histogram':dict(sorted(histogram.items())),
            'family_ids_by_marked_apex_count':dict(sorted(ids_by_K.items())),
            'checks':'All100 vertex links,264 edge incidences,165 faces and67 degree-six interior vertices verified for every graph',
            'scope':'Conditional N27 graph candidates; completeness depends on the stated strip/corner-cut classification'}


if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--family':
        found=False
        for graph in iter_graphs():
            if graph['family_id']==sys.argv[2]:
                print(json.dumps(graph,separators=(',',':')))
                found=True
                break
        assert found
    else:
        print(json.dumps(verify_all(),separators=(',',':')))
