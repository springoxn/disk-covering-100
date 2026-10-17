"""Complete bounded map families via permutations versus recursive face splitting.
Allows parallel edges and digons; ordered four axes on first boundary vertices.
"""
from pathlib import Path
from itertools import permutations,combinations
from math import factorial
import json,hashlib,argparse,time
from n100_dart_independent_canonicalization import canon,face_code,loops,need
ROOT=Path(__file__).resolve().parents[1]
def classify(phi,B,q):
    n=len(phi);alpha=[d^1 for d in range(n)];fc=loops(phi);vc=loops([phi[d^1] for d in range(n)])
    if len(fc)!=q+2 or len(vc)!=B:return None
    vertex={d:i for i,row in enumerate(vc) for d in row}
    if any(vertex[d]==vertex[d^1] for d in range(0,n,2)):return None
    if any(len(row)<2 or len({vertex[d] for d in row})!=len(row) for row in fc):return None
    anchors=[vertex[2*i] for i in range(B)]
    if len(set(anchors))!=B:return None
    axes={anchors[i]:i for i in range(4)}
    tags=[(int(d<B*2 and d%2==1),axes.get(vertex[d],-1)) for d in range(n)]
    raw=alpha,phi,tags
    try:return raw,face_code(raw),canon(*raw)[0]
    except ValueError:return None

def generate_chords(B,q):
    # Each split inserts a new paired edge and produces two oriented simple faces.
    states=[([list(range(0,2*B,2))],[i//2 if i%2==0 else (i//2+1)%B for i in range(2*B)])]
    for depth in range(q):
        new=[]
        for faces,origins in states:
            for f,row in enumerate(faces):
                for i,j in combinations(range(len(row)),2):
                    a,b=origins[row[i]],origins[row[j]]
                    if a==b:continue
                    e=len(origins)
                    first=row[i:j]+[e+1];second=row[j:]+row[:i]+[e]
                    new.append((faces[:f]+faces[f+1:]+[first,second],origins+[a,b]))
        states=new
    outer=[2*i+1 for i in reversed(range(B))];answer=[]
    for faces,origins in states:
        phi=[None]*(2*(B+q))
        for row in faces+[outer]:
            for a,b in zip(row,row[1:]+row[:1]):phi[a]=b
        need(all(v is not None for v in phi),'construction')
        got=classify(phi,B,q);need(got is not None,'constructed illegal map');answer.append(got)
    return answer

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-expanded-map-enumeration.json');args=ap.parse_args()
    results=[];start=time.monotonic()
    for B,q in ((5,1),(6,1),(4,2)):
        n=2*(B+q);outer=[2*i+1 for i in reversed(range(B))];remaining=[d for d in range(n) if d not in outer]
        primary={};secondary={};pcodes={};labeled=0
        for image in permutations(remaining):
            phi=[None]*n
            for a,b in zip(outer,outer[1:]+outer[:1]):phi[a]=b
            for a,b in zip(remaining,image):phi[a]=b
            got=classify(phi,B,q)
            if got is None:continue
            raw,pc,ic=got;labeled+=1
            need(pc not in pcodes or pcodes[pc]==ic,'primary orbit splits');pcodes[pc]=ic
            primary.setdefault(ic,raw)
        constructed=generate_chords(B,q)
        for raw,pc,ic in constructed:secondary.setdefault(ic,raw)
        need(set(primary)==set(secondary),'independent generated orbit sets differ')
        need(len(pcodes)==len(primary),'cross canonical partition disagreement')
        # Explicit isomorphism for every orbit between independently generated representatives.
        witnesses=[]
        for key in sorted(primary):
            one,two=primary[key],secondary[key];_,o1=canon(*one);_,o2=canon(*two);mapping=dict(zip(o1,o2))
            for d,e in mapping.items():need(mapping[one[0][d]]==two[0][e] and mapping[one[1][d]]==two[1][e] and one[2][d]==two[2][e],'isomorphism')
            witnesses.append([mapping[d] for d in range(n)])
        need(set(list(secondary)[1:])!=set(primary),'missing orbit control')
        results.append({'boundary_vertices':B,'edges':B+q,'inner_faces':q+1,'axis_vertices':[0,1,2,3],
            'residual_permutations_examined':factorial(len(remaining)),'accepted_labeled_maps':labeled,'distinct_orbits':len(primary),'recursive_face_split_histories':len(constructed),
            'orbit_sets_equal':True,'cross_canonical_partition_agrees':True,'isomorphism_witnesses':witnesses,
            'orbit_representatives':[{'alpha':raw[0],'phi':raw[1],'tags':raw[2]} for key,raw in sorted(primary.items())],
            'missing_orbit_detected':True})
        print('PASS bounded family B',B,'chords',q,'permutations',factorial(len(remaining)),'labeled',labeled,'orbits',len(primary),'histories',len(constructed),flush=True)
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-expanded-map-enumeration/v1','verified':True,'families':results,'arithmetic':'integer permutation checks','n100_complete_enumeration':False,'global_optimality':False,'scope':'three specified disk-map families, all vertices on boundary, four ordered axes; no interior vertices or full n100 families','bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['verify/n100_dart_independent_canonicalization.py','verify/n100_dart_map_canonicalization.py']},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'elapsed_seconds_reporting_only':time.monotonic()-start},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
