"""Independent uncentered-moment replay of all multi-axis variance tests."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,argparse
from n100_axis_dual_chain_independent import cycles,need
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-axis-multianchor-independent.json');args=ap.parse_args()
    cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';pp=ROOT/'verify/out/n100-axis-dual-chain-pruning.json';sp=ROOT/'verify/out/n100-axis-multianchor-pruning.json'
    load=lambda p:json.loads(p.read_text(encoding='utf-8'));core=load(cp)['core'];prior=load(pp);result=load(sp)
    A=core['alpha'];fc=cycles(core['phi']);N=len(fc);own={d:i for i,row in enumerate(fc) for d in row};outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');sites=[own[A[d]] for d in reversed(fc[outer])]
    D=[[999]*N for _ in range(N)]
    for i in range(N):D[i][i]=0
    for d,e in enumerate(A):
        a,b=own[d],own[e]
        if outer not in (a,b):D[a][b]=D[b][a]=1
    for k in range(N):
        if k==outer:continue
        for i in range(N):
            if D[i][k]>=999:continue
            for j in range(N):D[i][j]=min(D[i][j],D[i][k]+D[k][j])
    U2=F(1154469548855829,10**16)**2;axis=((1,0),(0,1),(-1,0),(0,-1));subsets=((0,1,2),(0,1,3),(0,2,3),(1,2,3),(0,1,2,3));cache={};kept=set();excluded=set();tests=0
    for p in prior['retained_axis_edge_placements']:
        fail=False
        for f in range(N):
            if f==outer:continue
            ds=tuple(D[sites[p[i]]][f] for i in range(4))
            if ds not in cache:
                fail_here=False
                for ids in subsets:
                    w=[F(1,(2*ds[i]+1)**2) for i in ids];W=sum(w);sx=sum(wi*axis[i][0] for wi,i in zip(w,ids));sy=sum(wi*axis[i][1] for wi,i in zip(w,ids));tests+=1
                    if W*W-sx*sx-sy*sy>len(ids)*W*U2:fail_here=True;break
                cache[ds]=fail_here
            if cache[ds]:fail=True;break
        (excluded if fail else kept).add(tuple(p))
    need(kept==set(map(tuple,result['retained'])),'retained set')
    need(excluded=={tuple(row['placement']) for row in result['excluded']},'excluded set')
    need(len(kept)==result['retained_count'] and len(excluded)==result['excluded_count'],'counts')
    # Rational identity equivalent to centered variance; negative sign control.
    weights=(F(1),F(2),F(3));pts=((1,0),(0,1),(-1,0));W=sum(weights);sx=sum(w*p[0] for w,p in zip(weights,pts));sy=sum(w*p[1] for w,p in zip(weights,pts))
    centered=sum(w*((F(p[0])-sx/W)**2+(F(p[1])-sy/W)**2) for w,p in zip(weights,pts));moment=sum(w*(p[0]**2+p[1]**2) for w,p in zip(weights,pts))-(sx*sx+sy*sy)/W
    need(centered==moment and centered!=sum(weights)+(sx*sx+sy*sy)/W,'moment identity/sign control')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-axis-multianchor-independent/v1','verified':True,'retained_count':len(kept),'excluded_count':len(excluded),'distance_vectors_checked':len(cache),'rational_subset_tests':tests,'complete_partition_equal':True,'method':'independent Floyd distances and uncentered rational moment inequality versus BFS and centered variance','sign_control_rejected':True,'machine_verified_geometry':False,'global_optimality':False,'scope':'only declared five subset/weight choices on fixed core, not all possible convex separation weights','bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,pp,sp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent uncentered moments:',len(excluded),'excluded',len(kept),'retained;',len(cache),'distance vectors,',tests,'subset tests;moment sign control passed')
if __name__=='__main__':main()
