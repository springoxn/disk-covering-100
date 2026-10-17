"""Audit cubic map dual while retaining every dart/edge identity."""
from pathlib import Path
from collections import Counter
import json,hashlib,argparse
from n100_dart_independent_canonicalization import loops,need
ROOT=Path(__file__).resolve().parents[1]
def analyze(core):
    A=core['alpha'];P=core['phi'];S=core['sigma'];n=len(A)
    need(all(P[d]==S[A[d]] for d in range(n)),'map equation')
    faces=loops(P);vertices=loops(S);owner={d:i for i,row in enumerate(faces) for d in row};origin={d:i for i,row in enumerate(vertices) for d in row}
    dual_sigma=P;dual_phi=[dual_sigma[A[d]] for d in range(n)]
    need(dual_phi==S,'dual face permutation')
    edges=[(d,A[d]) for d in range(n) if d<A[d]]
    dual_pairs=Counter(tuple(sorted((owner[d],owner[e]))) for d,e in edges)
    primal_pairs=Counter(tuple(sorted((origin[d],origin[e]))) for d,e in edges)
    outer_faces={owner[d] for d,t in enumerate(core['core_tags']) if t[0]=='outer'};need(len(outer_faces)==1,'outer tag');outer=outer_faces.pop()
    need(all((core['core_tags'][d][0]=='outer')==(owner[d]==outer) for d in range(n)),'entire outer cycle')
    parallel=[{'face_pair':list(pair),'edges':count} for pair,count in sorted(dual_pairs.items()) if count>1]
    return {'dual_vertices':len(faces),'dual_edges':len(edges),'dual_faces':len(loops(dual_phi)),'all_dual_faces_triangular':all(len(row)==3 for row in loops(dual_phi)),
        'outer_dual_vertex':outer,'outer_degree':len(faces[outer]),'distinct_outer_neighbors':len({owner[A[d]] for d in faces[outer]}),
        'dual_loops':sum(count for (a,b),count in dual_pairs.items() if a==b),'dual_parallel_classes':parallel,
        'primal_loops':sum(count for (a,b),count in primal_pairs.items() if a==b),'primal_parallel_classes':sum(count>1 for count in primal_pairs.values()),
        'dual_vertex_degrees':dict(Counter(map(len,faces))),'dual_alpha':A,'dual_sigma':dual_sigma,'dual_phi':dual_phi}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-cubic-dual-audit.json');args=ap.parse_args()
    src=ROOT/'verify/out/n100-cubic-core-roundtrip.json';data=json.loads(src.read_text(encoding='utf-8'));r=analyze(data['core'])
    need((r['dual_vertices'],r['dual_edges'],r['dual_faces'])==(101,297,198),'dual inventory');need(r['all_dual_faces_triangular'],'triangulation')
    need(r['dual_vertices']-r['dual_edges']+r['dual_faces']==2,'Euler')
    out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-cubic-dual-audit/v1','verified':True,'candidate_dual':r,'simple_dual_for_this_candidate':r['dual_loops']==0 and not r['dual_parallel_classes'],'global_simple_dual_reduction_proven':False,'n100_complete_enumeration':False,'global_optimality':False,'scope':'exact permutation dual of one certified combinatorial candidate; candidate simplicity does not imply completeness of simple triangulation generators','input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print('PASS dual V101/E297/F198, triangular faces; outer degree',r['outer_degree'],'distinct neighbors',r['distinct_outer_neighbors'],'loops',r['dual_loops'],'parallel classes',len(r['dual_parallel_classes']))
if __name__=='__main__':main()
