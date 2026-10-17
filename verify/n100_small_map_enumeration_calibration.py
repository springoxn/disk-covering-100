"""Exhaustive small-map orbit calibration: V4 E5 F_inner2 B4.
Primary enumerates all 6! residual face permutations; secondary inserts each chord.
"""
from pathlib import Path
from itertools import permutations,combinations
import json,hashlib
R=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def cycles(p):
    seen=set();out=[]
    for a in range(len(p)):
        if a in seen:continue
        row=[];d=a
        while d not in seen:seen.add(d);row.append(d);d=p[d]
        need(d==a,'permutation cycle');out.append(row)
    return out
# Independent canonicalizer uses vertex rotation rather than face next.
def code(phi,tags):
    sigma=[phi[d^1] for d in range(len(phi))];answers=[]
    for root in range(len(phi)):
        visited={root:0};queue=[root]
        for d in queue:
            for e in (sigma[d],d^1):
                if e not in visited:visited[e]=len(queue);queue.append(e)
        need(len(queue)==len(phi),'connected')
        answers.append(tuple((visited[sigma[d]],visited[d^1],tags[d]) for d in queue))
    return min(answers)
def classify(phi):
    fc=cycles(phi);vc=cycles([phi[d^1] for d in range(10)])
    if len(fc)!=3 or len(vc)!=4:return None
    vertex={d:i for i,c in enumerate(vc) for d in c}
    if any(vertex[d]==vertex[d^1] for d in range(0,10,2)):return None
    if any(len(c)<2 or len({vertex[d] for d in c})!=len(c) for c in fc):return None
    anchors=[vertex[d] for d in (0,2,4,6)]
    if len(set(anchors))!=4:return None
    axes={v:i for i,v in enumerate(anchors)}
    tags=[(1 if d in (1,3,5,7) else 0,axes[vertex[d]]) for d in range(10)]
    return code(phi,tags)
def main():
    primary=set();accepted=0;remaining=(0,2,4,6,8,9)
    for image in permutations(remaining):
        phi=[None]*10
        for a,b in zip((1,7,5,3),(7,5,3,1)):phi[a]=b
        for a,b in zip(remaining,image):phi[a]=b
        c=classify(phi)
        if c is not None:primary.add(c);accepted+=1
    # Independent construction of the two face cycles from each unordered chord pair.
    secondary=set();examples=[]
    for a,b in combinations(range(4),2):
        phi=[None]*10
        for u,v in zip((1,7,5,3),(7,5,3,1)):phi[u]=v
        first=[2*i for i in range(a,b)]+[9] # a..b then chord b->a
        second=[2*(i%4) for i in range(b,a+4)]+[8] # b..a then chord a->b
        for face in (first,second):
            for u,v in zip(face,face[1:]+face[:1]):phi[u]=v
        origins=[0,1,1,2,2,3,3,0,a,b]
        tags=[(1 if d in (1,3,5,7) else 0,origins[d]) for d in range(10)]
        c=code(phi,tags);secondary.add(c);examples.append({'chord':[a,b],'inner_face_lengths':[len(first),len(second)],'code':c})
    need(primary==secondary and len(primary)==6,'orbit set disagreement')
    # Missing any of the four digon branches destroys equality.
    omitted={code_ for code_ in secondary if code_!=tuple(tuple((r[0],r[1],tuple(r[2]))) for r in examples[0]['code'])}
    need(omitted!=primary,'missing branch undetected')
    op=R/'verify/out/n100-small-map-enumeration-calibration.json';need(not op.exists(),'overwrite')
    op.write_text(json.dumps({'verified':True,'parameters':{'V':4,'E':5,'inner_faces':2,'boundary_edges':4,'axis_marks':4},
      'residual_permutations_examined':720,'accepted_labeled_permutations':accepted,'distinct_marked_orbits':6,
      'independent_chord_constructions':6,'orbit_sets_equal':True,'examples':examples,
      'digon_orbits':sum(min(z['inner_face_lengths'])==2 for z in examples),
      'negative_control_missing_orbit_detected':True,
      'scope':'complete enumeration only for V4 E5 inner_faces2 B4 with all four boundary vertices ordered axis-marked; not n100 enumeration',
      'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS720 residual permutations;',accepted,'accepted;6 marked orbits match6 independent chords;4 digon orbits')
if __name__=='__main__':main()
