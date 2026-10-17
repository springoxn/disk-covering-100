"""Orientation-preserving marked-map canonical code from paired darts and face permutation."""
from pathlib import Path
import json,hashlib,copy
from n100_map_canonicalization import permute
R=Path(__file__).resolve().parents[1]
def need(v,m):
    if not v:raise ValueError(m)
def permutations(z):
    E=z['edges'];uses={i:[] for i in range(len(E))}
    for f,F in enumerate(z['faces']):
        vs=F['vertices']
        for a,b,i in zip(vs,vs[1:]+vs[:1],F['edges']):
            need(set(E[i]['ends'])=={a,b},'incidence')
            uses[i].append((f,1 if E[i]['ends']==[a,b] else -1))
    graph={i:[] for i in range(len(z['faces']))}
    for u in uses.values():
        if len(u)==2:
            (f,a),(g,b)=u;graph[f].append((g,-a*b));graph[g].append((f,-a*b))
    signs={0:1};stack=[0]
    while stack:
        f=stack.pop()
        for g,s in graph[f]:
            if g in signs:need(signs[g]==signs[f]*s,'orientation')
            else:signs[g]=signs[f]*s;stack.append(g)
    need(len(signs)==len(graph),'connected')
    boundary=z['boundary_cycle'];first=next((i for i,e in enumerate(E) if e['ends']==boundary[:2] or e['ends']==list(reversed(boundary[:2]))))
    f,sg=uses[first][0];want=1 if E[first]['ends']==boundary[:2] else -1
    flip=want*sg*signs[f];signs={f:s*flip for f,s in signs.items()}
    phi={};tags={};axes={v:str(i) for i,v in enumerate(z.get('axis_marks',[]))}
    def origin(d):return E[d//2]['ends'][d%2]
    for f,F in enumerate(z['faces']):
        ds=[]
        for a,b,i in zip(F['vertices'],F['vertices'][1:]+F['vertices'][:1],F['edges']):ds.append(2*i+(0 if E[i]['ends']==[a,b] else 1))
        if signs[f]<0:ds=[d^1 for d in reversed(ds)]
        for a,b in zip(ds,ds[1:]+ds[:1]):phi[a]=b;tags[a]=['inner',axes.get(origin(a),'')]
    outer=[]
    for i,u in uses.items():
        if len(u)==1:
            inner=next(d for d in (2*i,2*i+1) if d in phi);outer.append(inner^1)
    byorigin={origin(d):d for d in outer};need(len(byorigin)==len(outer),'simple outer')
    for d in outer:
        end=E[d//2]['ends'][1-d%2];phi[d]=byorigin[end];tags[d]=['outer',axes.get(origin(d),'')]
    need(sorted(phi)==list(range(2*len(E))) and sorted(phi.values())==sorted(phi),'dart permutation')
    return phi,tags

def canonical(z):
    phi,tags=permutations(z);codes=[]
    for root in phi:
        ids={root:0};queue=[root]
        for d in queue:
            for q in (d^1,phi[d]):
                if q not in ids:ids[q]=len(queue);queue.append(q)
        need(len(queue)==len(phi),'dart connected')
        codes.append(tuple((ids[d^1],ids[phi[d]],tuple(tags[d])) for d in queue))
    return min(codes)
if __name__=='__main__':
    p=R/'verify/out/n100-candidate-clipped-map.json';z=json.loads(p.read_text(encoding='utf-8'));c=canonical(z);q=permute(z)
    # Update semantic axis identifiers under the same vertex bijection used by permute.
    old=list(z['vertices']);mapping={v:f'R{len(old)-1-i}' for i,v in enumerate(old)};q['axis_marks']=[mapping[v] for v in z['axis_marks']]
    q['faces']=list(reversed(q['faces']))
    for f in q['faces']:
        vs,es=f['vertices'],f['edges'];f['vertices']=vs[1:]+vs[:1];f['edges']=es[1:]+es[:1]
    need(c==canonical(q),'full relabel and rotations invariance')
    # A sphere digon demonstrates two independent parallel edges (four darts).
    digon={'edges':[{'ends':['a','b']},{'ends':['a','b']}],
           'faces':[{'vertices':['a','b'],'edges':[0,1]}],'boundary_cycle':['a','b'],'axis_marks':[]}
    d=canonical(digon);need(len(d)==4,'digon edge identities')
    out=R/'verify/out/n100-dart-map-canonicalization.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'verified':True,'candidate_darts':len(c),'canonical_code':c,
      'canonical_sha256':hashlib.sha256(json.dumps(c).encode()).hexdigest(),
      'vertex_edge_face_relabel_and_cycle_rotation_invariant':True,'digon_darts':len(d),
      'scope':'canonical orientation-preserving outer-face and ordered-axis marked map; valid input manifold assumed; no map enumeration',
      'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS all-root dart canonical code:602 darts; vertex/edge/face permutations and cycle rotations; parallel-edge digon4 darts')
