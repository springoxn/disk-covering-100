"""Outward integer interval propagation for coupled face-center relaxations.
Boxes encode real scaled coordinates, NOT an integer lattice restriction.
Only empty boxes prove exclusion; nonempty/capped iterates are unresolved.
"""
from pathlib import Path
from math import isqrt
from collections import deque,Counter
import json,hashlib,argparse
from n100_dart_independent_canonicalization import loops,need
ROOT=Path(__file__).resolve().parents[1]
UN=1154469548855829;UD=10**16;Q=2**20
AXES=((1,0),(0,1),(-1,0),(0,-1))
def ceilroot(n):
    need(n>=0,'negative sqrt');s=isqrt(n);return s if s*s==n else s+1
def radiussquared(k):return ((k*UN*Q)**2+UD**2-1)//UD**2
def gap(a,b):return max(0,a[0]-b[1],b[0]-a[1])
def contract(a,b,R2):
    # Necessary: exists real a_point in a, b_point in b with distance²<=R2.
    if sum(gap(a[2*j:2*j+2],b[2*j:2*j+2])**2 for j in (0,1))>R2:return None
    out=list(a)
    for dim in (0,1):
        other=1-dim;g=gap(a[2*other:2*other+2],b[2*other:2*other+2]);remain=R2-g*g
        if remain<0:return None
        allowance=ceilroot(remain);out[2*dim]=max(out[2*dim],b[2*dim]-allowance);out[2*dim+1]=min(out[2*dim+1],b[2*dim+1]+allowance)
        if out[2*dim]>out[2*dim+1]:return None
    return out

def build(core):
    A=core['alpha'];fc=loops(core['phi']);own={d:i for i,row in enumerate(fc) for d in row};outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');inner=[f for f in range(len(fc)) if f!=outer];index={f:i for i,f in enumerate(inner)};sites=[index[own[A[d]]] for d in reversed(fc[outer])];adj=[set() for _ in inner]
    for d,e in enumerate(A):
        a,b=own[d],own[e]
        if outer not in (a,b):adj[index[a]].add(index[b])
    D={}
    for s in set(sites):
        dist={s:0};todo=deque([s])
        while todo:
            f=todo.popleft()
            for g in adj[f]:
                if g not in dist:dist[g]=dist[f]+1;todo.append(g)
        need(len(dist)==100,'connected');D[s]=dist
    return sites,[sorted(a) for a in adj],D

def propagate(p,sites,adj,D,limit):
    boxes=[[-Q,Q,-Q,Q] for _ in adj];unit=[0,0,0,0];anchors=[[a*Q,a*Q,b*Q,b*Q] for a,b in AXES];count=0
    unary=[]
    for f in range(len(adj)):
        constraints=[(unit,Q*Q)]+[(anchors[i],radiussquared(2*D[sites[p[i]]][f]+1)) for i in range(4)];unary.append(constraints)
    edgeR=radiussquared(2)
    for sweep in range(limit):
        changed=False
        for f in range(len(adj)):
            constraints=[('unary'+str(i),b,r2) for i,(b,r2) in enumerate(unary[f])]+[('neighbor'+str(g),boxes[g],edgeR) for g in adj[f]]
            for label,b,r2 in constraints:
                previous=boxes[f];new=contract(previous,b,r2);count+=1
                if new is None:return {'excluded':True,'sweeps':sweep+1,'contractions':count,'failure':{'face':f,'constraint':label,'box':previous,'other_box':list(b),'radius_squared_upper':r2},'boxes':boxes}
                if new!=previous:boxes[f]=new;changed=True
        if not changed:return {'excluded':False,'fixed_point':True,'sweeps':sweep+1,'contractions':count,'boxes':boxes}
    return {'excluded':False,'fixed_point':False,'sweeps':limit,'contractions':count,'boxes':boxes}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-axis-coupled-boxes.json');ap.add_argument('--sweeps',type=int,default=16);args=ap.parse_args()
    cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';pp=ROOT/'verify/out/n100-axis-dual-chain-pruning.json';candidatep=ROOT/'verify/out/n100-axis-subdivision-pruning.json';load=lambda p:json.loads(p.read_text(encoding='utf-8'));core=load(cp)['core'];prior=load(pp);candidate=load(candidatep)['candidate_axis_edge_indices'];sites,adj,D=build(core)
    # Algorithm arithmetic sanity controls: enclosing intervals, disjoint singleton points.
    need(contract([0,0,0,0],[3,3,4,4],24) is None,'outside singleton')
    need(contract([0,0,0,0],[3,3,4,4],25)==[0,0,0,0],'tangent singleton')
    rows=[];retained=[];excluded=[];hist=Counter();fixed=0;total=0
    for p in prior['retained_axis_edge_placements']:
        r=propagate(p,sites,adj,D,args.sweeps);total+=r['contractions'];hist[r['sweeps']]+=1
        if r['excluded']:excluded.append({'placement':p,'result':r})
        else:
            retained.append(p);fixed+=r['fixed_point'];rows.append({'placement':p,'fixed_point':r['fixed_point'],'sweeps':r['sweeps'],'boxes':r['boxes']})
    need(candidate in retained,'actual candidate falsely excluded')
    output={'schema':'n100-axis-coupled-boxes/v1','verified_integer_propagation':True,'scale':Q,'radius_numerator':UN,'radius_denominator':UD,'maximum_sweeps':args.sweeps,'input_count':len(prior['retained_axis_edge_placements']),'excluded_count':len(excluded),'retained_count':len(retained),'retained_fixed_points':fixed,'sweep_histogram':dict(hist),'contractions':total,'excluded':excluded,'retained':rows,'candidate_retained':True,'edge_radius_squared_upper_scaled':radiussquared(2),'rounding':'squared radii rounded up; integer square roots rounded up; coordinates encode closed real intervals divided by scale','scope':'unit-disk plus four propagated axis disks plus adjacent-center distance relaxation on one fixed core; nonempty boxes are unresolved','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,pp,candidatep)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8');print('PASS coupled boxes:',len(excluded),'excluded,',len(retained),'retained;',fixed,'fixed points;',total,'contractions;candidate retained;hist',dict(hist))
if __name__=='__main__':main()
