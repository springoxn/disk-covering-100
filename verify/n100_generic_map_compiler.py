"""Generic closed quadratic model compiler for ordered-axis disk maps."""
from pathlib import Path
import json,hashlib,copy
from itertools import combinations
from n100_candidate_quadratic_cover_model import polynomial as poly
from n100_dart_map_canonicalization import permutations
from n100_small_map_enumeration_calibration import cycles
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def compile_model(g):
    edges=g['edges'];faces=g['faces'];names=list(g['vertices']);boundary=g['boundary_cycle'];marks=g['axis_marks'];m=len(faces)
    need(sorted(f['center'] for f in faces)==list(range(m)) and m>0,'face labels')
    need(len(boundary)>=4 and len(set(boundary))==len(boundary) and set(boundary)<=set(names),'boundary')
    need(len(marks)==len(set(marks))==4 and set(marks)<=set(boundary),'marks')
    rot=boundary[boundary.index(marks[0]):]+boundary[:boundary.index(marks[0])];need([rot.index(v) for v in marks]==sorted(rot.index(v) for v in marks),'mark order')
    uses={i:[] for i in range(len(edges))}
    for f in faces:
        vs,ids=f['vertices'],f['edges'];need(len(vs)>=2 and len(set(vs))==len(vs) and len(vs)==len(ids),'simple face')
        for a,b,i in zip(vs,vs[1:]+vs[:1],ids):
            need(a in names and b in names and 0<=i<len(edges) and edges[i]['ends'] in ([a,b],[b,a]),'incidence');uses[i].append(f['center'])
    for i,e in enumerate(edges):need(len(e['ends'])==2 and e['ends'][0]!=e['ends'][1] and len(uses[i]) in (1,2) and len(set(uses[i]))==len(uses[i]) and sorted(uses[i])==sorted(e['faces']),'edge sides')
    outer=[i for i,u in uses.items() if len(u)==1];need(len(outer)==len(boundary),'outer length')
    for a,b in zip(boundary,boundary[1:]+boundary[:1]):need(sum(edges[i]['ends'] in ([a,b],[b,a]) for i in outer)==1,'outer identity')
    phi,tags=permutations(g);p=[phi[i] for i in range(2*len(edges))];vc=cycles([p[d^1] for d in range(len(p))]);fc=cycles(p)
    need(len(vc)==len(names) and len(fc)==m+1 and len(vc)-len(edges)+len(fc)==2,'sphere')
    for c in vc:need(len({edges[d//2]['ends'][d%2] for d in c})==1,'vertex link')
    need(len(names)<=2*m+2 and len(edges)<=3*m+1,'budget')
    pv={v:[2*i,2*i+1] for i,v in enumerate(names)};cv={j:[2*len(names)+2*j,2*len(names)+2*j+1] for j in range(m)};t=2*(len(names)+m);eq=[];iq=[]
    def put(target,kind,terms):target.append({'kind':kind,'terms':terms})
    put(iq,'t_nonnegative',poly(linear=[(1,t)]));put(iq,'t_at_most_one',poly(1,linear=[(-1,t)]))
    for v,(a,b) in pv.items():put(iq,'vertex_in_D',poly(1,squares=[(-1,a),(-1,b)]))
    for j,(a,b) in cv.items():put(iq,'center_in_D',poly(1,squares=[(-1,a),(-1,b)]))
    for f in faces:
        a,b=cv[f['center']]
        for v in f['vertices']:
            u,w=pv[v];put(iq,'face_vertex_distance',poly(linear=[(1,t)],squares=[(-1,u),(-1,w),(-1,a),(-1,b)],crosses=[(2,u,a),(2,w,b)]))
    for v in boundary:
        a,b=pv[v];put(eq,'boundary_unit_circle',poly(-1,squares=[(1,a),(1,b)]))
    for v,coord in zip(marks,[(1,0),(0,1),(-1,0),(0,-1)]):
        for d,c in enumerate(coord):put(eq,'axis_coordinate',poly(-c,linear=[(1,pv[v][d])]))
    for q,(a,b) in enumerate(zip(marks,marks[1:]+marks[:1])):
        chain=[a];at=boundary.index(a)
        while chain[-1]!=b:at=(at+1)%len(boundary);chain.append(boundary[at])
        for v in chain:
            for d,s in enumerate([(1,1),(-1,1),(-1,-1),(1,-1)][q]):put(iq,'quadrant_sign',poly(linear=[(s,pv[v][d])]))
        d=[1,0,1,0][q];s=[1,-1,-1,1][q]
        for a,b in zip(chain,chain[1:]):put(iq,'boundary_monotone',poly(linear=[(s,pv[b][d]),(-s,pv[a][d])]))
    need(len(eq)==len(boundary)+8 and len(iq)==len(names)+m+2*len(edges)+2*len(boundary)+10,'constraint counts')
    return {'variables':t+1,'t_index':t,'equalities':eq,'inequalities':iq}
def chord(a,b):
    faces=[]
    for vs,ids in [(list(range(a,b+1)),list(range(a,b))+[4]),([i%4 for i in range(b,a+5)],[i%4 for i in range(b,a+4)]+[4])]:faces.append({'center':len(faces),'vertices':list(map(str,vs)),'edges':ids})
    edges=[{'ends':[str(i),str((i+1)%4)],'faces':[f['center'] for f in faces if i in f['edges']]} for i in range(4)]+[{'ends':[str(a),str(b)],'faces':[0,1]}]
    return {'vertices':{str(i):{} for i in range(4)},'edges':edges,'faces':faces,'boundary_cycle':list('0123'),'axis_marks':list('0123')}
if __name__=='__main__':
    load=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
    g=load('verify/out/n100-candidate-clipped-map.json');old=load('verify/out/n100-candidate-quadratic-cover-model.json');model=compile_model(g)
    for key in ('equalities','inequalities'):need(model[key]==[{k:c[k] for k in ('kind','terms')} for c in old[key]],'candidate mismatch')
    models=[]
    for a,b in combinations(range(4),2):
        h=chord(a,b);z=compile_model(h);need((z['variables'],len(z['equalities']),len(z['inequalities']))==(13,12,34),'small counts');models.append({'chord':[a,b],'map':h,'model':z})
    rejects=[]
    for name,mut in [('repeated_axis',lambda h:h['axis_marks'].__setitem__(1,h['axis_marks'][0])),('missing_face_edge',lambda h:h['faces'][0]['edges'].pop()),('wrong_owner',lambda h:h['edges'][0].__setitem__('faces',[99]))]:
        h=copy.deepcopy(g);mut(h)
        try:compile_model(h)
        except (ValueError,IndexError,KeyError):rejects.append(name)
        else:raise RuntimeError('invalid map accepted')
    out=R/'verify/out/n100-generic-map-compiler.json';need(not out.exists(),'overwrite');paths=['verify/out/n100-candidate-clipped-map.json','verify/out/n100-candidate-quadratic-cover-model.json','verify/n100_candidate_quadratic_cover_model.py','verify/n100_dart_map_canonicalization.py','verify/n100_small_map_enumeration_calibration.py']
    out.write_text(json.dumps({'verified':True,'candidate1030_polynomials_identical':True,'candidate_model':model,'small_models':models,'rejected_controls':rejects,'scope':'generic map interface compiler; shared polynomial constructor, no independent compiler or continuous solver, no n100 enumeration','bindings':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in paths},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS all1030 candidate polynomials identical;six13-variable models compiled;3 invalid maps rejected')
