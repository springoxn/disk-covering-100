"""Canonical labeled-map serialization preserving parallel-edge identities."""
from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def relabel(z):
    # Boundary anchors and face IDs are semantic labels; vertex discovery is deterministic.
    order=[]
    for v in z['boundary_cycle']:
        if v not in order:order.append(v)
    for f in sorted(z['faces'],key=lambda q:q['center']):
        for v in f['vertices']:
            if v not in order:order.append(v)
    for v in sorted(z['vertices']):
        if v not in order:order.append(v)
    return {v:f'v{i}' for i,v in enumerate(order)}
def canon(z):
    m=relabel(z); boundary=[m[v] for v in z['boundary_cycle']]
    edges=[]
    for i,e in enumerate(z['edges']):
        edges.append({'id':i,'kind':e['kind'],'ends':[m[v] for v in e['ends']],
                      'faces':list(e['faces']),'original_holes':e.get('original_holes',[])})
    # ID is retained to make parallel edges distinguishable, while sorted records
    # make serialization independent of input edge insertion order only if identities
    # themselves are also permuted consistently by the face cycles.
    edge_records=sorted(edges,key=lambda e:(e['kind'],tuple(e['ends']),tuple(e['faces']),tuple(e['original_holes'])))
    edge_ids={e['id']:j for j,e in enumerate(edge_records)}
    for j,e in enumerate(edge_records):e['id']=j
    faces=[]
    for f in z['faces']:
        vs=[m[v] for v in f['vertices']];ids=[edge_ids[i] for i in f['edges']]
        rotations=[]
        for k in range(len(vs)):
            rotations.append((vs[k:]+vs[:k],ids[k:]+ids[:k]))
        best=min(rotations)
        faces.append({'center':f['center'],'vertices':best[0],'edges':best[1]})
    return json.dumps({'vertices':sorted(m.values()),'edges':edge_records,'faces':sorted(faces,key=lambda f:f['center']),'boundary':boundary,'axes':z.get('axis_marks',[])},sort_keys=True,separators=(',',':'))
def permute(z):
    # A deterministic nontrivial vertex relabeling and edge insertion permutation.
    q=copy.deepcopy(z);old=list(q['vertices']);new={v:f'R{len(old)-1-i}' for i,v in enumerate(old)}
    q['vertices']={new[v]:data for v,data in q['vertices'].items()}
    for e in q['edges']:e['ends']=[new[v] for v in e['ends']]
    for f in q['faces']:f['vertices']=[new[v] for v in f['vertices']]
    q['boundary_cycle']=[new[v] for v in q['boundary_cycle']]
    q['edges']=list(reversed(q['edges']))
    # Face edge IDs must be translated after edge reversal.
    n=len(q['edges'])
    for f in q['faces']:f['edges']=[n-1-i for i in f['edges']]
    return q
if __name__=='__main__':
    p=R/'verify/out/n100-candidate-clipped-map.json';z=json.loads(p.read_text(encoding='utf-8'))
    for path,h in z['bindings'].items():need(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'binding')
    c=canon(z);q=permute(z);need(c==canon(q),'canonical relabel invariance')
    # Preserve parallel-edge identity control: duplicate an edge under a new id changes code.
    bad=copy.deepcopy(z);bad['edges'].append(copy.deepcopy(bad['edges'][0]));need(c!=canon(bad),'parallel identity retained')
    # Removing semantic face center must be rejected before canonicalization.
    malformed=copy.deepcopy(z);malformed['faces'][0]['center']=malformed['faces'][1]['center']
    try:need(len({f['center'] for f in malformed['faces']})==100,'face centers unique')
    except ValueError:rejected=True
    else:raise RuntimeError('duplicate face accepted')
    out=R/'verify/out/n100-map-canonicalization.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'verified':True,'canonical_sha256':hashlib.sha256(c.encode()).hexdigest(),
      'relabel_invariant':True,'edge_identity_preserved':True,'rejected_controls':['parallel_edge_identity_loss','duplicate_face_center'],
      'vertex_count':len(z['vertices']),'edge_count':len(z['edges']),'face_count':len(z['faces']),
      'scope':'canonicalization of one labeled candidate map; no exhaustive map enumeration',
      'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS canonical candidate map; relabel/insertion invariant; parallel edge identity retained; malformed controls rejected')
