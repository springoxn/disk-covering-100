"""Multi-anchor metric propagation on retained axis placements.
For a face chain path, center c must lie in intersections of rational disks
|c-a_i|<=2*k_i*U; variance identity gives exact emptiness lower bounds.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from collections import deque,Counter
import json,hashlib,argparse,copy
from n100_dart_independent_canonicalization import loops,need
ROOT=Path(__file__).resolve().parents[1]
def lower_intersection(points,radii):
    # For any weights, sum w_i|c-p_i|² >= weighted variance.
    best=F(0);witness=None
    for i,j in combinations(range(len(points)),2):
        wi=F(1);wj=F(1);gap=sum((points[i][q]-points[j][q])**2 for q in (0,1))/(radii[i]+radii[j])**2
        if gap>best:best,witness=gap,(i,j)
    return best,witness
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-axis-multianchor-pruning.json');args=ap.parse_args()
    cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';pp=ROOT/'verify/out/n100-axis-dual-chain-pruning.json';core=json.loads(cp.read_text(encoding='utf-8'))['core'];prior=json.loads(pp.read_text(encoding='utf-8'));A=core['alpha'];P=core['phi'];faces=loops(P);own={d:i for i,row in enumerate(faces) for d in row};outer=next(i for i,row in enumerate(faces) if core['core_tags'][row[0]][0]=='outer');boundary=[A[d] for d in reversed(faces[outer])];sites=[own[d] for d in boundary]
    adj={f:{} for f in range(101) if f!=outer}
    for d,e in enumerate(A):
        if d>e:continue
        a,b=own[d],own[e]
        if outer not in (a,b):adj[a][b]=1;adj[b][a]=1
    D={}
    for s in set(sites):
        dist={s:0};q=deque([s])
        while q:
            f=q.popleft()
            for g in adj[f]:
                if g not in dist:dist[g]=dist[f]+1;q.append(g)
        D[s]=dist
    U=F(1154469548855829,10**16);axis=((1,0),(0,1),(-1,0),(0,-1));kept=[];excluded=[];hist=Counter()
    cache={}
    for p in prior['retained_axis_edge_placements']:
        found=None
        for face in adj:
            ds=tuple(D[sites[p[i]]][face] for i in range(4))
            if ds in cache:
                if cache[ds] is not None:found=dict(cache[ds],face=face);break
                continue
            radius2=[(2*d+1)**2*U*U for d in ds]
            for ids in ((0,1,2),(0,1,3),(0,2,3),(1,2,3),(0,1,2,3)):
                # Positive rational inverse-radius weights; necessary variance budget.
                weights=[1/radius2[i] for i in ids];W=sum(weights)
                mx=sum(w*axis[i][0] for w,i in zip(weights,ids))/W
                my=sum(w*axis[i][1] for w,i in zip(weights,ids))/W
                variance=sum(w*((axis[i][0]-mx)**2+(axis[i][1]-my)**2) for w,i in zip(weights,ids))
                budget=sum(w*radius2[i] for w,i in zip(weights,ids))
                if variance>budget:
                    found={'face':face,'axis_ids':list(ids),'graph_distances':[D[sites[p[i]]][face] for i in ids],'radius_squared':[str(radius2[i]) for i in ids],'weights':list(map(str,weights)),'variance':str(variance),'budget':str(budget),'gap':str(variance-budget)};break
            cache[ds]=None if found is None else {k:v for k,v in found.items() if k!='face'}
            if found:break
        if found:excluded.append({'placement':p,'witness':found});hist[str(len(found['axis_ids']))]+=1
        else:kept.append(p)
    candidate_path=ROOT/'verify/out/n100-axis-subdivision-pruning.json';candidate=json.loads(candidate_path.read_text(encoding='utf-8'))['candidate_axis_edge_indices']
    need(candidate in kept,'candidate excluded');need(len(kept)+len(excluded)==4776,'partition')
    out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-axis-multianchor-pruning/v1','verified_rational':True,'prior_count':4776,'excluded_count':len(excluded),'retained_count':len(kept),'excluded':excluded,'retained':kept,'candidate_retained':True,'histogram':dict(hist),'analytic_dependencies':['center-to-axis bound is (2*graph_distance+1)*U by triangle inequality','positive weighted squared-distance sum equals weighted variance plus total_weight times squared distance to weighted mean'], 'scope':'three/four-axis positive weighted variance test at every inner face of one fixed core; no global core enumeration','machine_verified_geometry':False,'global_optimality':False,'new_count_families_excluded':0,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,pp,candidate_path)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS multianchor:',len(excluded),'excluded,',len(kept),'retained;candidate retained;hist',dict(hist))
if __name__=='__main__':main()
