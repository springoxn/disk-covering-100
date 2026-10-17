"""Correct annulus ownership and exhaustive orientation-preserving automorphisms.
Integer-only arithmetic. Historical empty-boundary scans are NOT accepted inputs.
"""
from pathlib import Path
from collections import deque
import json, hashlib, argparse
from n100_dart_independent_canonicalization import loops
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x: raise ValueError(m)
def automorphisms(A,P,tags):
    n=len(A); root=0; accepted=[]; rejected=[]
    for target in range(n):
        mapping={root:target}; todo=deque([root]); conflict=None
        while todo and conflict is None:
            d=todo.popleft(); e=mapping[d]
            if tags[d]!=tags[e]: conflict='tag'; break
            for src,dst in ((A[d],A[e]),(P[d],P[e])):
                if src in mapping:
                    if mapping[src]!=dst: conflict='permutation'; break
                else: mapping[src]=dst;todo.append(src)
        if conflict is not None: rejected.append([target,conflict]);continue
        need(len(mapping)==n and len(set(mapping.values()))==n,'connected bijection')
        M=[mapping[d] for d in range(n)]
        need(all(M[A[d]]==A[M[d]] and M[P[d]]==P[M[d]] and tags[d]==tags[M[d]] for d in range(n)),'automorphism')
        accepted.append(M)
    need(len(accepted)+len(rejected)==n,'all root images')
    return accepted,rejected

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-owner-correction.json');args=ap.parse_args()
    cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';pp=ROOT/'verify/out/n100-axis-dual-chain-pruning.json';apath=ROOT/'verify/out/n100-axis-subdivision-pruning.json'
    load=lambda p:json.loads(p.read_text(encoding='utf-8'))
    core=load(cp)['core'];boxes=load(bp);prior=load(pp);candidate=load(apath)['candidate_axis_edge_indices']
    A=core['alpha'];P=core['phi'];tags=core['core_tags'];fc=loops(P);owner={d:i for i,row in enumerate(fc) for d in row}
    outside=[d for d,t in enumerate(tags) if t[0]=='outer'];outside_faces={owner[d] for d in outside};need(len(outside_faces)==1,'one outer face');outer=next(iter(outside_faces))
    # Outer tag belongs to OUTER dart, and its twin belongs to its inner owner.
    actual=sorted({owner[A[d]] for d in outside});need(len(outside)==32 and len(actual)==32 and outer not in actual,'32 actual owners')
    historical=[f for f,row in enumerate(fc) if f!=outer and any(tags[d][0]=='outer' for d in row)]
    need(historical==[],'historical bug reproduced')
    inner=[f for f in range(len(fc)) if f!=outer];index={f:i for i,f in enumerate(inner)}
    # Independently derive adjacency via unordered edge sides rather than outer dart tags.
    alt=set()
    for d,e in enumerate(A):
        if d>=e: continue
        sides={owner[d],owner[e]}
        if outer in sides: alt.update(sides-{outer})
    need(set(actual)==alt,'boundary edge-side ownership')
    expected=set(map(tuple,prior['retained_axis_edge_placements']));need(expected=={tuple(r['placement']) for r in boxes['retained']} and len(expected)==4776,'full input domain')
    Q=2**20;UN=1154469548855829;UD=10**16;threshold=(UD-UN)**2*Q*Q
    excluded=[];survivors=[];minimum=None;tests=0
    for row in boxes['retained']:
        failures=[]
        for f in actual:
            b=row['boxes'][index[f]];need(len(b)==4 and b[0]<=b[1] and b[2]<=b[3],'ordered box')
            maxnorm=max(abs(b[0]),abs(b[1]))**2+max(abs(b[2]),abs(b[3]))**2
            slack=maxnorm*UD**2-threshold;tests+=1
            minimum=slack if minimum is None else min(minimum,slack)
            if slack<0: failures.append({'core_face':f,'center_index':index[f],'box':b,'norm_upper_squared_scaled':maxnorm,'strict_gap':-slack})
        if failures:excluded.append({'placement':row['placement'],'failures':failures})
        else:survivors.append(row['placement'])
    need(candidate in survivors,'candidate excluded')
    # True arithmetic controls, including rejection on the open side only.
    def empty(b):return (max(abs(b[0]),abs(b[1]))**2+max(abs(b[2]),abs(b[3]))**2)*UD**2<threshold
    need(empty([0,0,0,0]) and not empty([Q,Q,0,0]),'origin/circle controls')
    autos,rejected=automorphisms(A,P,tags);need(autos==[list(range(len(A)))],'actual core has trivial oriented automorphism group')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    result={'schema':'n100-boundary-owner-correction/v1','verified_integer_audit':True,'historical_empty_boundary_bug_reproduced':True,'supersedes':['stage45 annulus claims','stage46 annulus claims'],'boundary_face_ids':actual,'center_index_by_boundary_face':{str(f):index[f] for f in actual},'independent_edge_side_owner_sets_equal':True,'placements':4776,'annulus_checks':tests,'annulus_excluded_count':len(excluded),'excluded':excluded,'retained_count':len(survivors),'candidate_retained':True,'minimum_signed_annulus_slack':minimum,'annulus_test':'max_norm_squared_scaled*UD^2 < (UD-UN)^2*Q^2, strict cross multiplication with no sqrt rounding',
    'automorphism_root_images_checked':len(A),'orientation_preserving_automorphism_count':len(autos),'automorphism_maps':autos,'rejected_root_images':rejected,'axis_placement_orbit_count':4776,'automorphism_scope':'oriented, outer-face-preserving combinatorial automorphisms; excludes reflections and geometric axis-label rotations',
    'machine_verified_geometry':False,'global_optimality':False,'scope':'one fixed core only; nonempty annulus-box intersections are not feasible coverings; no full core enumeration',
    'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,pp,apath)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS corrected owners',len(actual),'annulus checks',tests,'excluded',len(excluded),'retained',len(survivors),'oriented autos',len(autos),'root images',len(A))
if __name__=='__main__': main()
