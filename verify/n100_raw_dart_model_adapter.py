"""Raw paired-dart decoder and enumeration-to-model calibration."""
from pathlib import Path
from itertools import permutations as enum
import json,hashlib
from n100_generic_map_compiler import compile_model
from n100_dart_map_canonicalization import permutations,canonical
from n100_small_map_enumeration_calibration import classify
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def orbits(p):
    need(sorted(p)==list(range(len(p))),'permutation');left=set(range(len(p)));out=[]
    while left:
        a=min(left);row=[];d=a
        while d in left:row.append(d);left.remove(d);d=p[d]
        need(d==a,'cycle');out.append(row)
    return out

def decode(phi,outer_dart,axis_darts):
    n=len(phi);need(n>0 and n%2==0,'dart count');fc=orbits(phi);vc=orbits([phi[d^1] for d in range(n)])
    origin={d:i for i,c in enumerate(vc) for d in c};face={d:i for i,c in enumerate(fc) for d in c}
    need(0<=outer_dart<n and len(axis_darts)==4 and all(0<=d<n for d in axis_darts),'marks range');outer=face[outer_dart]
    need(len(vc)-n//2+len(fc)==2,'genus')
    for c in fc:need(len(c)>=2 and len({origin[d] for d in c})==len(c),'simple face')
    need(len(fc[outer])>=4,'boundary length');need(all(origin[d]!=origin[d^1] and face[d]!=face[d^1] for d in range(n)),'loop/bridge')
    seen={0};stack=[0]
    while stack:
        d=stack.pop()
        for e in (d^1,phi[d]):
            if e not in seen:seen.add(e);stack.append(e)
    need(len(seen)==n,'disconnected')
    names={i:f'v{i}' for i in range(len(vc))};inner=[f for f in range(len(fc)) if f!=outer];labels={f:i for i,f in enumerate(inner)}
    E=[{'ends':[names[origin[d]],names[origin[d^1]]],'faces':[labels[f] for f in (face[d],face[d^1]) if f!=outer]} for d in range(0,n,2)]
    F=[{'center':labels[f],'vertices':[names[origin[d]] for d in fc[f]],'edges':[d//2 for d in fc[f]]} for f in inner]
    G={'vertices':{v:{} for v in names.values()},'edges':E,'faces':F,'boundary_cycle':[names[origin[d]] for d in reversed(fc[outer])],'axis_marks':[names[origin[d]] for d in axis_darts]}
    compile_model(G);return G

def main():
    load=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
    G=load('verify/out/n100-candidate-clipped-map.json');p,tags=permutations(G);phi=[p[i] for i in range(len(p))];outer=next(d for d,t in tags.items() if t[0]=='outer');axes=[next(d for d,t in tags.items() if t[1]==str(i)) for i in range(4)]
    rebuilt=decode(phi,outer,axes);need(canonical(G)==canonical(rebuilt),'roundtrip');M=compile_model(rebuilt);need((M['variables'],len(M['equalities']),len(M['inequalities']))==(605,44,986),'candidate counts')
    accepted=[];prior=[];codes=set();errors={}
    for image in enum((0,2,4,6,8,9)):
        q=[None]*10
        for a,b in zip((1,7,5,3),(7,5,3,1)):q[a]=b
        for a,b in zip((0,2,4,6,8,9),image):q[a]=b
        c=classify(q)
        if c is not None:prior.append(tuple(q))
        try:g=decode(q,1,[0,2,4,6]);m=compile_model(g)
        except ValueError as e:errors[str(e)]=errors.get(str(e),0)+1;continue
        need((m['variables'],len(m['equalities']),len(m['inequalities']))==(13,12,34),'small counts');need(c is not None,'extra acceptance');accepted.append(tuple(q));codes.add(c)
    need(set(accepted)==set(prior) and len(accepted)==12 and len(codes)==6,'acceptance set')
    rejected=[]
    for name,q,o,a in [('nonpermutation',[0]*10,1,[0,2,4,6]),('repeated_axis',phi,outer,[axes[0]]*4),('wrong_axis_order',phi,outer,[axes[0],axes[2],axes[1],axes[3]])]:
        try:decode(q,o,a)
        except ValueError:rejected.append(name)
        else:raise RuntimeError('bad input accepted')
    paths=['verify/out/n100-candidate-clipped-map.json','verify/out/n100-small-map-enumeration-calibration.json','verify/n100_generic_map_compiler.py','verify/n100_dart_map_canonicalization.py','verify/n100_small_map_enumeration_calibration.py']
    out=R/'verify/out/n100-raw-dart-model-adapter.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'verified':True,'candidate_roundtrip_canonical_match':True,'candidate_counts':[605,44,986],'candidate_decoded_map':rebuilt,'permutations_examined':720,'accepted_permutations':accepted,'accepted_count':12,'canonical_orbits':6,'acceptance_set_equal_to_prior_classifier':True,'rejection_histogram':errors,'negative_controls':rejected,'scope':'raw-dart to model adapter; shared compiler and canonicalizer; no continuous solving or n100 enumeration','bindings':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in paths},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS candidate602-dart roundtrip;720 permutations,12 accepted,6 orbits;all models compiled;3 malformed inputs rejected')
if __name__=='__main__':main()
