"""Export candidate clipped-map incidence, retaining independent edge identities.
Geometry depends on accepted root-box empty-circle and boundary-owner certificates.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json,hashlib
R=Path(__file__).resolve().parents[1];S='runtime/external-disk100-strict-local-replay/source/'
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def cycles(edges):
    result=[]
    for f in range(100):
        selected=[(i,e) for i,e in enumerate(edges) if f in e['faces']];adj={}
        for i,e in selected:
            a,b=e['ends'];adj.setdefault(a,[]).append((b,i));adj.setdefault(b,[]).append((a,i))
        need(adj and all(len(z)==2 for z in adj.values()),'face degree2')
        start=min(adj);v=start;previous=None;vs=[];es=[]
        while True:
            need(v not in vs,'premature face repeat');vs.append(v)
            nxt=[z for z in adj[v] if z[1]!=previous][0];w,i=nxt;es.append(i);previous=i;v=w
            if v==start:break
        need(len(es)==len(selected),'disconnected face components');result.append({'center':f,'vertices':vs,'edges':es})
    return result

def main():
    inv=load('verify/out/n100-full-circumcenter-root-box.json');bc=load('verify/out/n100-boundary-pair-intersections.json');s=load(S+'polynomial_system.json');m=load(S+'rational_midpoint.json')
    need(inv['verified'] and bc['verified'],'receipts')
    for cert in (inv,bc):
        for p,h in cert['bindings'].items():need(sha(p)==h,'source hash')
    inside={r['triangle_index']:r for r in inv['rows'] if r['kind']=='inside'}
    vertices={f'I{i}':{'type':'circumcenter','triangle_index':i} for i in inside}
    pairs=s['boundary_active_pairs'];order=bc['cycle_order']
    for h in order:vertices[f'B{h}']={'type':'boundary_root_hole','hole_index':h}
    endpoints={}
    for i,row in inside.items():
        for pair in combinations(row['support'],2):endpoints.setdefault(tuple(sorted(pair)),[]).append(f'I{i}')
    for h,pair in enumerate(pairs):endpoints.setdefault(tuple(sorted(pair)),[]).append(f'B{h}')
    edges=[]
    for pair,ends in sorted(endpoints.items()):
        need(len(ends)==2 and ends[0]!=ends[1],'clipped edge endpoint count')
        edges.append({'kind':'bisector_segment','ends':ends,'faces':list(pair)})
    before={'vertices':len(vertices),'internal_edges':len(edges)}
    D=int(m['denominator']);rho=F(1,10**58);x=[F(int(z),D) for z in m['numerators']]
    axis={'E':(F(1),F(0)),'N':(F(0),F(1)),'W':(F(-1),F(0)),'S':(F(0),F(-1))};axes_used=[];boundary=[]
    for row in bc['rows']:
        h,j,owner=row['from_hole'],row['to_hole'],row['owner_center'];A=x[428+2*h:430+2*h];B=x[428+2*j:430+2*j]
        inserted=[]
        for name,P in axis.items():
            ca=A[0]*P[1]-A[1]*P[0];cb=P[0]*B[1]-P[1]*B[0]
            # Each axis has one nonzero coordinate; cross coordinate error <=rho.
            if ca-rho>0 and cb-rho>0:inserted.append(name)
        need(len(inserted)<=1,'short arc multiple axes')
        chain=[f'B{h}']
        if inserted:
            name=inserted[0];need(name not in axes_used,'duplicate axis');axes_used.append(name)
            vertices[name]={'type':'axis','coordinates':list(map(str,axis[name]))};chain.append(name)
        chain.append(f'B{j}')
        for a,b in zip(chain,chain[1:]):
            boundary.append(a);edges.append({'kind':'unit_circle_arc','ends':[a,b],'faces':[owner],'original_holes':[h,j]})
    need(set(axes_used)==set(axis),'four axes')
    faces=cycles(edges);V=len(vertices);E=len(edges);need(V-E+100==1,'Euler disk');need(V<=202 and E<=301,'model budgets')
    degree={v:0 for v in vertices}
    for e in edges:
        for v in e['ends']:degree[v]+=1
    need(all(d==(2 if v in axis else 3) for v,d in degree.items()),'vertex degrees')
    op=R/'verify/out/n100-candidate-clipped-map.json';need(not op.exists(),'overwrite')
    deps=['verify/out/n100-full-circumcenter-root-box.json','verify/out/n100-boundary-pair-intersections.json','verify/out/n100-full-circumcenter-independent.json','verify/out/n100-boundary-owner-independent.json',S+'polynomial_system.json',S+'rational_midpoint.json']
    op.write_text(json.dumps({'verified_combinatorial_export':True,'vertices':vertices,'edges':edges,'faces':faces,'boundary_cycle':boundary,'axis_marks':['E','N','W','S'],
        'counts_before_axis_insertion':before,'V':V,'E':E,'inner_faces':100,'boundary_edges':len(boundary),
        'geometry_dependency':'accepted root empty-circle classification and whole-boundary ownership, convex Voronoi cells; explicit root-box edge-segment completeness review remains required',
        'scope':'one candidate map incidence export; no complete topology enumeration or global exclusion',
        'bindings':{p:sha(p) for p in deps},'checker_sha256':sha('verify/n100_candidate_clipped_map.py'),
        'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS clipped candidate incidence: V',V,'E',E,'100 simple face cycles, four axes, degree and Euler budgets')
if __name__=='__main__':main()
