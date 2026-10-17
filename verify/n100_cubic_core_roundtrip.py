"""Suppress four degree-two axes, preserving directed subdivision paths.
No core simplicity assumption: parallel edges and loops remain distinct darts.
"""
from pathlib import Path
import json,hashlib,argparse
from collections import Counter
from n100_dart_map_canonicalization import permutations
from n100_dart_independent_canonicalization import loops,need
from n100_generic_map_compiler import compile_model
ROOT=Path(__file__).resolve().parents[1]
def compress(phi,tags):
    n=len(phi);alpha=[d^1 for d in range(n)];sigma=[phi[alpha[d]] for d in range(n)]
    vertices=loops(sigma);removed=set();axes=[]
    for row in vertices:
        marks={tags[d][1] for d in row}
        if marks!={''}:
            need(len(row)==2 and len(marks)==1 and next(iter(marks)) in '0123','axis degree/tag')
            removed.update(row);axes.append({'axis':next(iter(marks)),'darts':row})
        else:need(len(row)==3,'nonaxis degree')
    need(sorted(a['axis'] for a in axes)==list('0123'),'four axes')
    kept=[d for d in range(n) if d not in removed];ids={d:i for i,d in enumerate(kept)}
    paths=[];A=[];Sig=[]
    for d in kept:
        path=[d];cur=d
        while alpha[cur] in removed:
            cur=sigma[alpha[cur]];need(cur not in path,'axis-only cycle');path.append(cur)
        paths.append(path);A.append(ids[alpha[cur]]);Sig.append(ids[sigma[d]])
    P=[Sig[A[d]] for d in range(len(kept))]
    need(sorted(d for path in paths for d in path)==list(range(n)),'path partition')
    need(all(A[A[d]]==d and A[d]!=d for d in range(len(A))),'core pairing')
    need(all(paths[A[d]]==[alpha[q] for q in reversed(paths[d])] for d in range(len(A))),'reverse subdivision path')
    need(all(len(row)==3 for row in loops(Sig)),'cubic core')
    return {'alpha':A,'phi':P,'sigma':Sig,'kept_original_darts':kept,'subdivision_paths':paths,'axes':axes,'core_tags':[[tags[d][0],''] for d in kept]}
def restore(core):
    paths=core['subdivision_paths'];kept=core['kept_original_darts'];A=core['alpha'];Sig=core['sigma'];n=sum(map(len,paths))
    alpha=[None]*n;sigma=[None]*n;tags=[None]*n
    for i,path in enumerate(paths):
        rev=paths[A[i]];need(len(path)==len(rev),'reverse length')
        for d,e in zip(path,reversed(rev)):
            need(alpha[d] is None or alpha[d]==e,'edge consistency');alpha[d]=e;tags[d]=[core['core_tags'][i][0],'']
        sigma[path[0]]=kept[Sig[i]]
        for j in range(len(path)-1):sigma[alpha[path[j]]]=path[j+1]
    for item in core['axes']:
        row=item['darts'];need(sigma[row[0]]==row[1] and sigma[row[1]]==row[0],'axis rotation')
        for d in row:tags[d][1]=item['axis']
    need(sorted(alpha)==list(range(n)) and sorted(sigma)==list(range(n)),'restored permutations')
    return alpha,[sigma[alpha[d]] for d in range(n)],tags

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-cubic-core-roundtrip.json');args=ap.parse_args()
    src=ROOT/'verify/out/n100-candidate-clipped-map.json';g=json.loads(src.read_text(encoding='utf-8'));compile_model(g)
    pp,tt=permutations(g);phi=[pp[d] for d in range(len(pp))];tags=[tt[d] for d in range(len(pp))]
    core=compress(phi,tags);alpha,p,t=restore(core)
    need(alpha==[d^1 for d in range(len(phi))] and p==phi and t==tags,'exact full roundtrip')
    V=len(loops(core['sigma']));E=len(core['alpha'])//2;F=len(loops(core['phi']))
    need((V,E,F)==(198,297,101) and V-E+F==2,'core inventory')
    # Verify outer/inner distinction is preserved through every subdivision path.
    for i,path in enumerate(core['subdivision_paths']):need(all(tags[d][0]==core['core_tags'][i][0] for d in path),'face type along path')
    import copy
    bad=copy.deepcopy(core);bad['subdivision_paths'][0].append(bad['subdivision_paths'][0][0])
    rejected=False
    try:restore(bad)
    except (ValueError,IndexError,TypeError):rejected=True
    need(rejected,'damaged subdivision accepted')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-cubic-core-roundtrip/v1','verified':True,'original_inventory':{'V':202,'E':301,'F_with_outer':101},'core_inventory':{'V':V,'E':E,'F_with_outer':F},'core':core,'exact_alpha_phi_tags_roundtrip':True,'subdivision_paths_partition_all_original_darts':True,'face_type_preserved':True,'damaged_subdivision_rejected':True,'global_enumeration_complete':False,'global_optimality':False,'scope':'one real n100 candidate; invertible axis suppression implementation, no claim of core generation completeness; loops and parallel edges not merged','bindings':{str(src.relative_to(ROOT)):hashlib.sha256(src.read_bytes()).hexdigest()},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print('PASS real n100 cubic core V198/E297/F101; all602 original darts restored exactly with axes and face tags; corrupt subdivision rejected')
if __name__=='__main__':main()
