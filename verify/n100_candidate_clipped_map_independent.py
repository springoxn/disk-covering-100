"""Independent candidate-map combinatorial manifold replay."""
from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def check(z):
    vertices=z['vertices'];edges=z['edges'];faces=z['faces'];need(len(faces)==100,'faces')
    uses={i:[] for i in range(len(edges))}
    for f,face in enumerate(faces):
        vs=face['vertices'];ids=face['edges'];need(face['center']==f and len(vs)==len(ids) and len(set(vs))==len(vs),'simple face')
        for a,b,i in zip(vs,vs[1:]+vs[:1],ids):
            e=edges[i];need(a in vertices and b in vertices and set(e['ends'])=={a,b} and f in e['faces'],'face-edge agreement')
            uses[i].append((f,1 if e['ends']==[a,b] else -1))
    adj={f:[] for f in range(100)}
    for i,e in enumerate(edges):
        need(len(uses[i])==len(e['faces']) and sorted(f for f,d in uses[i])==sorted(e['faces']),'edge owners')
        need(len(e['faces']) in (1,2),'regular edges')
        if len(uses[i])==2:
            (f,a),(g,b)=uses[i];relation=-a*b;adj[f].append((g,relation));adj[g].append((f,relation))
    signs={0:1};stack=[0]
    while stack:
        f=stack.pop()
        for g,r in adj[f]:
            if g in signs:need(signs[g]==signs[f]*r,'nonorientable')
            else:signs[g]=signs[f]*r;stack.append(g)
    need(len(signs)==100,'dual connected')
    boundary=z['boundary_cycle'];need(len(set(boundary))==len(boundary)==36,'simple boundary')
    boundary_set={frozenset((a,b)) for a,b in zip(boundary,boundary[1:]+boundary[:1])}
    actual={frozenset(e['ends']) for e in edges if len(e['faces'])==1};need(actual==boundary_set,'boundary completeness')
    # Vertex links: incident faces give adjacency of edge identities around each vertex.
    for v in vertices:
        incident={i for i,e in enumerate(edges) if v in e['ends']};link={i:set() for i in incident}
        for face in faces:
            vs=face['vertices']
            if v not in vs:continue
            k=vs.index(v);a=face['edges'][k-1];b=face['edges'][k];link[a].add(b);link[b].add(a)
        start=next(iter(incident));seen={start};stack=[start]
        while stack:
            for i in link[stack.pop()]:
                if i not in seen:seen.add(i);stack.append(i)
        need(seen==incident,'disconnected vertex link')
        deg=sorted(len(a) for a in link.values())
        need(deg==([1,1]+[2]*(len(incident)-2) if v in boundary else [2]*len(incident)),'vertex link not circle/path')
    need(len(vertices)-len(edges)+len(faces)==1,'Euler');need(len(vertices)<=202 and len(edges)<=301,'budgets')
    return {'V':len(vertices),'E':len(edges),'faces':len(faces),'boundary_edges':len(boundary),'orientable':True,'all_vertex_links_regular':True}
if __name__=='__main__':
    p=R/'verify/out/n100-candidate-clipped-map.json';z=json.loads(p.read_text(encoding='utf-8'))
    for path,h in z['bindings'].items():need(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'binding')
    need(hashlib.sha256((R/'verify/n100_candidate_clipped_map.py').read_bytes()).hexdigest()==z['checker_sha256'],'export script')
    result=check(z);reject=[]
    for name,mutate in [('missing_edge',lambda q:q['edges'].pop()),('damaged_face_cycle',lambda q:q['faces'][0]['vertices'].__setitem__(0,'E')),('missing_axis_boundary',lambda q:q['boundary_cycle'].remove('E')),('wrong_edge_owner',lambda q:q['edges'][0].__setitem__('faces',[99]))]:
        q=copy.deepcopy(z);mutate(q)
        try:check(q)
        except (ValueError,IndexError,KeyError):reject.append(name)
        else:raise RuntimeError('negative accepted '+name)
    out=R/'verify/out/n100-candidate-clipped-map-independent.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'verified':True,'result':result,'rejected_controls':reject,
        'scope':'independent combinatorial disk-manifold replay; does not prove geometric edge completeness or enumerate other maps',
        'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS independent orientable disk map,100 faces,202 vertex links,four corruption rejects')
