"""Exact audit of the frozen candidate's active incidence map.
This audits the candidate map only; it is not a complete map enumeration.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,itertools
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def main():
    topo=json.loads((R/'runtime/external-disk100-strict-local-replay/source/algebraic_cover_topology.json').read_text(encoding='utf-8'))
    sys=json.loads((R/'runtime/external-disk100-strict-local-replay/source/polynomial_system.json').read_text(encoding='utf-8'))
    tri=[tuple(z) for z in topo['triangles']]; hull=list(topo['hull']);boundary=list(topo['boundary_order'])
    need(len(tri)==178 and len(hull)==20 and len(boundary)==32,'frozen counts')
    need(all(len(z)==3 and len(set(z))==3 for z in tri),'nondegenerate combinatorial triangles')
    V=sorted(set(v for z in tri for v in z));edges=set()
    for a,b,c in tri:
        for e in ((a,b),(b,c),(c,a)):edges.add(tuple(sorted(e)))
    # triangles share edges; boundary hull edges are the outer polygon edges.
    hull_edges={tuple(sorted((hull[i],hull[(i+1)%len(hull)]))) for i in range(len(hull))}
    internal_edges=edges-hull_edges
    E=len(edges);Vn=len(V);Fn=len(tri)+1
    # Check connected incidence and Euler sphere relation.
    adj={v:set() for v in V}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    seen={V[0]};stack=[V[0]]
    while stack:
        u=stack.pop()
        for v in adj[u]:
            if v not in seen:seen.add(v);stack.append(v)
    need(seen==set(V),'connected')
    need(Vn-E+Fn==2,'sphere Euler')
    # Internal edge incidence exactly 2 and hull edges exactly1 in triangle set.
    inc={e:0 for e in edges}
    for z in tri:
        for a,b in itertools.combinations(z,2):inc[tuple(sorted((a,b)))]+=1
    need(all(inc[e]==2 for e in internal_edges),'internal two-sided')
    need(all(inc[e]==1 for e in hull_edges),'hull one-sided')
    # Active KKT incidence is 114 triangles + 32 boundary pairs =146 hole rows.
    need(len(sys['internal_active_triangles'])==114 and len(sys['boundary_active_pairs'])==32,'system rows')
    active=[tuple(z) for z in sys['internal_active_triangles']];pairs=sys['boundary_active_pairs']
    need(all(len(z)==3 for z in active) and all(len(z)==2 for z in pairs),'active shape')
    need(len({tuple(sorted(z)) for z in active})==114,'unique active supports')
    need({tuple(sorted(z)) for z in active}<={tuple(sorted(z)) for z in tri},'active supports subset')
    out=R/'verify/out/n100-candidate-topology-audit.json'
    if out.exists():raise FileExistsError(out)
    out.write_text(json.dumps({'schema':'n100-candidate-topology-audit/v1','verified':True,
      'triangle_count':len(tri),'active_interior_triangle_rows':len(active),'boundary_pair_rows':len(pairs),
      'distinct_vertices':Vn,'distinct_edges':E,'hull_vertex_count':len(hull),'face_count_including_outer':Fn,
      'internal_edge_count':len(internal_edges),'hull_edge_count':len(hull_edges),'connected':True,
      'euler_sphere':'V-E+F=2','internal_edges_two_sided':True,'hull_edges_one_sided':True,
      'boundary_order_length':len(boundary),'boundary_order_unique':len(set(boundary))==len(boundary),
      'sources':{'topology_sha256':hashlib.sha256((R/'runtime/external-disk100-strict-local-replay/source/algebraic_cover_topology.json').read_bytes()).hexdigest(),
                 'system_sha256':hashlib.sha256((R/'runtime/external-disk100-strict-local-replay/source/polynomial_system.json').read_bytes()).hexdigest()},
      'scope':'frozen candidate incidence audit only; no enumeration of other maps or global optimality',
      'global_optimality':False,'minimal_polynomial_obtained':False,
      'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print('PASS candidate topology:',Vn,'vertices',E,'edges',Fn,'faces; Euler and two-sided incidence')
if __name__=='__main__':main()
