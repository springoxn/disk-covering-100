"""Independent vertex-rotation DFS map canon plus explicit isomorphism witnesses.
Input face permutations may come from a shared adapter; canon algorithm is separate.
"""
from pathlib import Path
from itertools import permutations
import json,hashlib,random
from n100_dart_map_canonicalization import permutations as adapt,canonical as primary
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def canon(alpha,phi,tags):
    n=len(alpha);need(sorted(alpha)==list(range(n)) and sorted(phi)==list(range(n)),'permutation')
    need(all(alpha[alpha[i]]==i and alpha[i]!=i for i in range(n)),'edge pairing')
    sigma=[phi[alpha[i]] for i in range(n)];inverse=[0]*n
    for i,j in enumerate(sigma):inverse[j]=i
    best=None;order=None
    for root in range(n):
        todo=[root];seen=set();seq=[]
        while todo:
            d=todo.pop()
            if d in seen:continue
            seen.add(d);seq.append(d)
            todo.extend([alpha[d],inverse[d],sigma[d]])
        need(len(seq)==n,'disconnected')
        index={d:i for i,d in enumerate(seq)}
        code=tuple((index[sigma[d]],index[alpha[d]],tuple(tags[d])) for d in seq)
        if best is None or code<best:best,order=code,seq
    return best,order

def witness(a,b):
    ca,oa=canon(*a);cb,ob=canon(*b);need(ca==cb,'not isomorphic')
    mapping=dict(zip(oa,ob));aa,pa,ta=a;ab,pb,tb=b
    need(len(set(mapping.values()))==len(aa),'bijection')
    for d,e in mapping.items():
        need(mapping[aa[d]]==ab[e] and mapping[pa[d]]==pb[e] and tuple(ta[d])==tuple(tb[e]),'isomorphism witness')
    return [mapping[d] for d in range(len(aa))]
def relabel(data,seed):
    a,p,t=data;n=len(a);labels=list(range(n));random.Random(seed).shuffle(labels);A=[0]*n;P=[0]*n;T=[None]*n
    for d,e in enumerate(labels):A[e]=labels[a[d]];P[e]=labels[p[d]];T[e]=t[d]
    return A,P,T

def face_code(data):
    # Direct replay of primary alpha/phi BFS rule for raw small-map permutations.
    alpha,phi,tags=data;answer=[]
    for root in range(len(alpha)):
        seq=[root];ids={root:0}
        for d in seq:
            for e in (alpha[d],phi[d]):
                if e not in ids:ids[e]=len(seq);seq.append(e)
        need(len(seq)==len(alpha),'connected')
        answer.append(tuple((ids[alpha[d]],ids[phi[d]],tuple(tags[d])) for d in seq))
    return min(answer)
def loops(p):
    visited=set();answer=[]
    for root in range(len(p)):
        if root in visited:continue
        seq=[];d=root
        while d not in visited:visited.add(d);seq.append(d);d=p[d]
        need(d==root,'cycle');answer.append(seq)
    return answer

def main():
    source=ROOT/'verify/out/n100-candidate-clipped-map.json';G=json.loads(source.read_text(encoding='utf-8'));p,t=adapt(G);n=len(p)
    data=([d^1 for d in range(n)],[p[d] for d in range(n)],[t[d] for d in range(n)])
    c,order=canon(*data);witnesses=[]
    for seed in (19,37,101):witnesses.append(witness(data,relabel(data,seed)))
    primary_code=primary(G);need(face_code(data)==primary_code,'adapter primary mismatch')
    # Recover and verify explicit map from saved primary BFS code to actual candidate.
    saved=ROOT/'verify/out/n100-dart-map-canonicalization.json';z=json.loads(saved.read_text(encoding='utf-8'))
    A=[r[0] for r in z['canonical_code']];P=[r[1] for r in z['canonical_code']];T=[r[2] for r in z['canonical_code']]
    old_mapping=witness(data,(A,P,T))
    small=[];remaining=(0,2,4,6,8,9)
    for image in permutations(remaining):
        phi=[None]*10
        for a,b in zip((1,7,5,3),(7,5,3,1)):phi[a]=b
        for a,b in zip(remaining,image):phi[a]=b
        vertices=loops([phi[d^1] for d in range(10)]);faces=loops(phi)
        if len(vertices)!=4 or len(faces)!=3:continue
        v={d:i for i,row in enumerate(vertices) for d in row}
        if any(v[d]==v[d^1] for d in range(0,10,2)):continue
        if any(len(row)<2 or len({v[d] for d in row})!=len(row) for row in faces):continue
        axes=[v[d] for d in (0,2,4,6)]
        if len(set(axes))!=4:continue
        marks={vv:i for i,vv in enumerate(axes)};tags=[(int(d in (1,3,5,7)),marks[v[d]]) for d in range(10)]
        raw=([d^1 for d in range(10)],phi,tags);small.append((raw,face_code(raw),canon(*raw)[0]))
    need(len(small)==12,'labeled small family')
    pairchecks=0
    for raw,pc,ic in small:
        for other,op,oi in small:
            need((pc==op)==(ic==oi),'orbit partition mismatch')
            if ic==oi:witness(raw,other)
            pairchecks+=1
    need(len({z[2] for z in small})==6,'orbit count')
    altered=list(data[2]);altered[0]=['corrupted','axis'];bad=(data[0],data[1],altered)
    need(canon(*bad)[0]!=c,'tag corruption missed')
    out=ROOT/'verify/out/n100-dart-independent-canonicalization.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-dart-independent-canonicalization/v1','verified':True,'algorithm':'all-root DFS vertex rotation and inverse; explicit alpha/phi/tag isomorphism witnesses','candidate_darts':n,'candidate_code':c,'candidate_to_saved_primary_mapping':old_mapping,'candidate_arbitrary_dart_relabel_witnesses':witnesses,'small_labeled_maps':len(small),'small_orbits':6,'pairwise_orbit_comparisons':pairchecks,'tag_corruption_rejected':True,'adapter_shared_with_primary':True,'independent_canonical_algorithm':True,'complete_n100_enumeration':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (source,saved,ROOT/'verify/n100_dart_map_canonicalization.py')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent DFS canon:602-dart primary isomorphism witness;3 arbitrary relabelings;12 small maps/6 orbits/144 pair checks;tag corruption rejected')
if __name__=='__main__':main()
