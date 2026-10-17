"""Necessary graph-metric cuts for four-axis insertions on a real core.
Each inner-face adjacency supplies a shared vertex, hence center distance<=2U.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import deque,Counter
from itertools import combinations
import json,hashlib,argparse
from n100_dart_independent_canonicalization import loops,need
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-axis-dual-chain-pruning.json');args=ap.parse_args()
    cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';pp=ROOT/'verify/out/n100-axis-subdivision-pruning.json'
    core=json.loads(cp.read_text(encoding='utf-8'))['core'];prior=json.loads(pp.read_text(encoding='utf-8'));A=core['alpha'];P=core['phi'];faces=loops(P);owner={d:i for i,row in enumerate(faces) for d in row}
    outer=next(i for i,row in enumerate(faces) if core['core_tags'][row[0]][0]=='outer');boundary=[A[d] for d in reversed(faces[outer])];sites=[owner[d] for d in boundary]
    adj={f:{} for f in range(len(faces)) if f!=outer}
    for d,e in enumerate(A):
        if d>e:continue
        a,b=owner[d],owner[e]
        if outer in (a,b):continue
        need(a!=b,'interior self-face edge');adj[a][b]=d;adj[b][a]=e
    paths={}
    for a in set(sites):
        discovered={a:[a]};queue=deque([a])
        while queue:
            f=queue.popleft()
            for g in sorted(adj[f]):
                if g not in discovered:discovered[g]=discovered[f]+[g];queue.append(g)
        need(len(discovered)==100,'inner connected')
        for b in set(sites):paths[a,b]=discovered[b]
    U=F(prior['radius']);coords=[(1,0),(0,1),(-1,0),(0,-1)];kept=[];excluded=[];hist=Counter()
    for placement in prior['retained_axis_edge_placements']:
        found=None
        for i,j in combinations(range(4),2):
            a,b=sites[placement[i]],sites[placement[j]];path=paths[a,b];k=len(path)
            distance=sum((coords[i][q]-coords[j][q])**2 for q in (0,1));gap=F(distance)-4*k*k*U*U
            if gap>0:
                found={'axis_pair':[i,j],'face_path':path,'directed_core_edge_darts':[adj[x][y] for x,y in zip(path,path[1:])],'disk_chain_length':k,'axis_distance_squared':distance,'squared_distance_gap':str(gap)};break
        if found:excluded.append({'placement':placement,'witness':found});hist[str(found['axis_distance_squared'])+':'+str(found['disk_chain_length'])]+=1
        else:kept.append(placement)
    need(prior['candidate_axis_edge_indices'] in kept,'actual candidate falsely excluded');need(len(kept)+len(excluded)==5280,'partition')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-axis-dual-chain-pruning/v1','verified_rational_graph_cuts':True,'radius':str(U),'prior_placements':5280,'excluded_count':len(excluded),'retained_count':len(kept),'excluded':excluded,'retained_axis_edge_placements':kept,'boundary_face_owners':sites,'outer_face':outer,'candidate_retained':True,'exclusion_histogram':dict(hist),
        'analytic_dependencies':['every adjacent pair of inner-face disks contains their common vertex so their center distance<=2U','axis belongs to the disk owning its subdivided outer edge','triangle inequality along k face disks gives axis distance<=2kU'],
        'scope':'graph-metric necessary cuts on all prior axis placements of one real core; no solving retained models or complete n100 core enumeration','machine_verified_geometry':False,'global_optimality':False,'new_n100_count_families_excluded':0,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,pp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print('PASS exact dual-chain cuts:',len(excluded),'excluded,',len(kept),'retained;actual candidate retained;histogram',dict(hist))
if __name__=='__main__':main()
