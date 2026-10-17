"""Complete finite spatial branch trees over a fixed necessary box domain.
An unresolved leaf never counts as exclusion. Children cover parent's real box.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,argparse
from n100_axis_coupled_boxes import build,contract,radiussquared,Q,AXES
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def propagate(boxes,unary,adj,limit):
    B=[row[:] for row in boxes];edge=radiussquared(2);steps=0
    for sweep in range(limit):
        changed=False
        for f in range(len(B)):
            cons=[('unary'+str(i),b,r) for i,(b,r) in enumerate(unary[f])]+[('neighbor'+str(g),B[g],edge) for g in adj[f]]
            for label,b,r in cons:
                old=B[f];new=contract(old,b,r);steps+=1
                if new is None:return {'empty':True,'boxes':B,'sweeps':sweep+1,'steps':steps,'failure':{'face':f,'constraint':label,'box':old,'other_box':list(b),'r2':r}}
                if new!=old:B[f]=new;changed=True
        if not changed:return {'empty':False,'boxes':B,'fixed':True,'sweeps':sweep+1,'steps':steps}
    return {'empty':False,'boxes':B,'fixed':False,'sweeps':limit,'steps':steps}
def tree(root,unary,adj,focus,depth,limit):
    nodes=[]
    def visit(B,level):
        idx=len(nodes);nodes.append(None);r=propagate(B,unary,adj,limit);record={'level':level,'propagation':r}
        if r['empty']:record['kind']='excluded'
        elif level>=depth:record['kind']='unresolved'
        else:
            choices=[(r['boxes'][f][2*d+1]-r['boxes'][f][2*d],-f,-d,f,d) for f in focus for d in (0,1)];width,_,_,f,d=max(choices)
            if width<=1:record['kind']='unresolved'
            else:
                lo,hi=r['boxes'][f][2*d:2*d+2];mid=(lo+hi)//2;left=[b[:] for b in r['boxes']];right=[b[:] for b in r['boxes']];left[f][2*d+1]=mid;right[f][2*d]=mid
                record.update(kind='split',face=f,coordinate=d,split=mid,interval=[lo,hi],children=[visit(left,level+1),visit(right,level+1)])
        nodes[idx]=record;return idx
    visit(root,0);hist=Counter(row['kind'] for row in nodes)
    return {'nodes':nodes,'summary':dict(hist),'root_excluded':hist['unresolved']==0,'steps':sum(row['propagation']['steps'] for row in nodes)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=6);ap.add_argument('--sweeps',type=int,default=16);ap.add_argument('--out',default='verify/out/n100-spatial-branch-trees.json');args=ap.parse_args()
    cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';apath=ROOT/'verify/out/n100-axis-subdivision-pruning.json';load=lambda p:json.loads(p.read_text(encoding='utf-8'));sites,adj,D=build(load(cp)['core']);prior=load(bp);candidate=load(apath)['candidate_axis_edge_indices'];selected=[prior['retained'][0]['placement'],candidate];rows=[]
    for p in selected:
        root=next(row['boxes'] for row in prior['retained'] if row['placement']==p);axes=[[a*Q,a*Q,b*Q,b*Q] for a,b in AXES];unary=[[([0,0,0,0],Q*Q)]+[(axes[i],radiussquared(2*D[sites[p[i]]][f]+1)) for i in range(4)] for f in range(100)]
        # Focus on the axis0 disk and its inner neighbors to branch coupled coordinates.
        f=sites[p[0]];focus=sorted(set([f]+adj[f]));result=tree(root,unary,adj,focus,args.depth,args.sweeps);rows.append({'placement':p,'focus_faces':focus,'tree':result})
    need(not rows[-1]['tree']['root_excluded'],'candidate root falsely excluded')
    out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-spatial-branch-trees/v1','verified_integer_branching':True,'scale':Q,'max_depth':args.depth,'max_sweeps':args.sweeps,'cases':rows,'candidate_root_not_excluded':True,'split_semantics':'closed intervals [lo,mid] and [mid,hi]; union exactly parent, shared midpoint allowed','scope':'bounded branch trees for2 retained axis placements of one fixed core; roots inherit verified necessary boxes; unresolved leaves are not feasible configurations','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,apath,ROOT/'verify/n100_axis_coupled_boxes.py')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    for row in rows:print('PASS tree',row['placement'],row['tree']['summary'],'root_excluded',row['tree']['root_excluded'],'steps',row['tree']['steps'])
if __name__=='__main__':main()
