"""Complete V5/E7/B4 disk maps with internal degree>=3.
Primary residual permutations; secondary three spokes to three boundary vertices.
"""
from pathlib import Path
from itertools import permutations,combinations_with_replacement
from collections import Counter
import argparse,json,hashlib,time
from n100_dart_independent_canonicalization import canon,face_code,loops,witness,need
from n100_raw_dart_model_adapter import decode
from n100_generic_map_compiler import compile_model
ROOT=Path(__file__).resolve().parents[1]
OUTER=(1,7,5,3);REMAIN=(0,2,4,6,8,9,10,11,12,13)
def classify(phi):
    fc=loops(phi)
    if len(fc)!=4 or any(len(row)<2 for row in fc):return None
    vc=loops([phi[d^1] for d in range(14)])
    if len(vc)!=5:return None
    vertex={d:i for i,row in enumerate(vc) for d in row};boundary=[vertex[d] for d in (0,2,4,6)]
    if len(set(boundary))!=4:return None
    inner=set(range(5))-set(boundary)
    if len(inner)!=1:return None
    internal=inner.pop()
    if len(vc[internal])<3:return None
    if any(vertex[d]==vertex[d^1] for d in range(0,14,2)):return None
    if any(len({vertex[d] for d in row})!=len(row) for row in fc):return None
    axes={v:i for i,v in enumerate(boundary)};tags=[(int(d in OUTER),axes.get(vertex[d],-1)) for d in range(14)]
    raw=([d^1 for d in range(14)],phi,tags)
    try:return raw,face_code(raw),canon(*raw)[0]
    except ValueError:return None

def secondary():
    examples=[]
    for selected in combinations_with_replacement(range(4),3):
        if len(set(selected))<2:continue
        faces=[]
        for i,a in enumerate(selected):
            j=(i+1)%3;b=selected[j];path=[];v=a
            while v!=b:path.append(2*v);v=(v+1)%4
            # Preserve distinct spoke identities even for repeated boundary endpoints.
            faces.append(path+[8+2*j,9+2*i])
        phi=[None]*14
        for face in faces+[list(OUTER)]:
            for a,b in zip(face,face[1:]+face[:1]):phi[a]=b
        got=classify(phi);need(got is not None,'spoke construction');examples.append(got)
    return examples

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-one-interior-map-enumeration.json');args=ap.parse_args()
    start=time.monotonic();orbits={};primarycodes={};accepted=0;examined=0
    for image in permutations(REMAIN):
        examined+=1;phi=[None]*14
        for a,b in zip(OUTER,OUTER[1:]+OUTER[:1]):phi[a]=b
        for a,b in zip(REMAIN,image):phi[a]=b
        got=classify(phi)
        if got is None:continue
        raw,pc,ic=got;accepted+=1;orbits.setdefault(ic,raw)
        need(pc not in primarycodes or primarycodes[pc]==ic,'canonical disagreement');primarycodes[pc]=ic
    independent={ic:raw for raw,pc,ic in secondary()}
    need(set(orbits)==set(independent) and len(orbits)==16,'orbit sets: primary '+str(len(orbits))+' secondary '+str(len(independent)))
    models=[]
    for ic,raw in sorted(orbits.items()):
        iso=witness(raw,independent[ic]);g=decode(raw[1],1,[0,2,4,6]);m=compile_model(g)
        need(len(g['vertices'])==5 and len(g['edges'])==7 and len(g['faces'])==3,'decoded inventory')
        models.append({'raw':{'alpha':raw[0],'phi':raw[1],'tags':raw[2]},'independent_spoke_isomorphism':iso,'map':g,'model':m})
    need(len(primarycodes)==16 and examined==3628800,'enumeration totals')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-one-interior-map-enumeration/v1','verified':True,'parameters':{'vertices':5,'edges':7,'boundary_vertices':4,'internal_vertices':1,'internal_degree_minimum':3,'inner_faces':3},'residual_permutations_examined':examined,'accepted_labeled_maps':accepted,'orbits':len(orbits),'independent_spoke_constructions':len(independent),'complete_orbit_sets_equal':True,'models':models,
        'scope':'only V5/E7/B4 with one internal vertex degree>=3 and simple faces; no n100 complete map family','n100_complete_enumeration':False,'global_optimality':False,'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['verify/n100_dart_independent_canonicalization.py','verify/n100_raw_dart_model_adapter.py','verify/n100_generic_map_compiler.py']},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'elapsed_seconds_reporting_only':time.monotonic()-start},indent=2)+'\n',encoding='utf-8');print('PASS one-interior family:',examined,'permutations,',accepted,'labeled maps,',len(orbits),'orbits=',len(independent),'independent spoke maps;models compiled;seconds',time.monotonic()-start)
if __name__=='__main__':main()
