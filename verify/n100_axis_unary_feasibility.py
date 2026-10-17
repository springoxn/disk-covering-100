"""Rational points in every unary four-axis disk intersection on the fixed core.
Grid search failure is unresolved, never exclusion. Acceptance uses integers only.
"""
from pathlib import Path
from collections import deque,Counter
from math import isqrt
import json,hashlib,argparse
from n100_dart_independent_canonicalization import loops,need
ROOT=Path(__file__).resolve().parents[1]
UN=1154469548855829;UD=10**16
AXES=((1,0),(0,1),(-1,0),(0,-1))
def find(ds,Q):
    bounds=[((2*d+1)*UN*Q)**2//UD**2 for d in ds]
    order=sorted(range(-Q,Q+1),key=abs)
    for x in order:
        h=isqrt(Q*Q-x*x);lo,hi=-h,h
        for (ax,ay),b in zip(AXES,bounds):
            v=b-(x-ax*Q)**2
            if v<0:break
            h=isqrt(v);lo=max(lo,ay*Q-h);hi=min(hi,ay*Q+h)
            if lo>hi:break
        else:
            y=max(lo,min(0,hi))
            need(x*x+y*y<=Q*Q,'unit witness')
            need(all(((x-a*Q)**2+(y-b*Q)**2)*UD**2<=((2*d+1)*UN*Q)**2 for (a,b),d in zip(AXES,ds)),'axis witness')
            return [x,y,Q]
    return None

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-axis-unary-feasibility.json');args=ap.parse_args()
    cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';pp=ROOT/'verify/out/n100-axis-dual-chain-pruning.json';load=lambda p:json.loads(p.read_text(encoding='utf-8'))
    core=load(cp)['core'];prior=load(pp);A=core['alpha'];fc=loops(core['phi']);owner={d:i for i,row in enumerate(fc) for d in row};outface=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');sites=[owner[A[d]] for d in reversed(fc[outface])];adj={i:set() for i in range(len(fc)) if i!=outface}
    for d,e in enumerate(A):
        a,b=owner[d],owner[e]
        if outface not in (a,b):adj[a].add(b)
    D={}
    for s in set(sites):
        dist={s:0};q=deque([s])
        while q:
            f=q.popleft()
            for g in adj[f]:
                if g not in dist:dist[g]=dist[f]+1;q.append(g)
        need(len(dist)==100,'connected');D[s]=dist
    vectors=Counter(tuple(D[sites[p[i]]][f] for i in range(4)) for p in prior['retained_axis_edge_placements'] for f in adj)
    witnesses=[];unresolved=[];scales=Counter()
    for ds,multiplicity in sorted(vectors.items()):
        point=None
        for Q in (64,256,1024,4096):
            point=find(ds,Q)
            if point is not None:break
        if point is None:unresolved.append(list(ds))
        else:witnesses.append({'distances':list(ds),'point_integer_xy_denominator':point,'occurrences':multiplicity});scales[point[2]]+=1
    need(sum(vectors.values())==477600,'full face-placement domain')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    result={'schema':'n100-axis-unary-feasibility/v1','verified_integer_witnesses':True,'radius_numerator':UN,'radius_denominator':UD,'placements':4776,'face_placement_pairs':sum(vectors.values()),'unique_distance_vectors':len(vectors),'rational_witness_count':len(witnesses),'unresolved_count':len(unresolved),'unresolved':unresolved,'witnesses':witnesses,'grid_scales':dict(scales),'all_unary_intersections_certified_nonempty':not unresolved,'scope':'independent face centers constrained only by unit disk and four propagated axis-distance disks; adjacent-center, shared-vertex and coverage constraints omitted','consequence_if_all_nonempty':'No valid separation using only these five unary disk inequalities can exclude these placements; does not preclude joint constraints across faces or tighter distances','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,pp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS unary intersections:',len(witnesses),'rational witnesses,',len(unresolved),'unresolved,',sum(vectors.values()),'face-placement pairs;scales',dict(scales))
if __name__=='__main__':main()
