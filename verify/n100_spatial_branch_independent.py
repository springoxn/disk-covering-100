"""Independent spatial-tree coverage audit and interval replay.
Shared independent contractor from prior stage, no branch generator import.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,argparse,copy
from n100_axis_coupled_boxes_independent import cycles,clip
ROOT=Path(__file__).resolve().parents[1]
def need(x,msg):
    if not x:raise ValueError(msg)
def structure(nodes):
    seen=set()
    def visit(idx,depth):
        need(isinstance(idx,int) and 0<=idx<len(nodes) and idx not in seen,'tree child uniqueness');seen.add(idx);r=nodes[idx];need(r['level']==depth,'depth')
        if r['kind']=='split':
            lo,hi=r['interval'];need(lo<r['split']<hi,'proper split');need(len(r['children'])==2,'binary children')
            for ch in r['children']:visit(ch,depth+1)
        else:need(r['kind'] in ('excluded','unresolved'),'leaf kind')
    visit(0,0);need(len(seen)==len(nodes),'no orphan nodes');return Counter(r['kind'] for r in nodes)
def replay(B,unary,adj,edge,limit):
    boxes=[b[:] for b in B];steps=0
    for sweep in range(limit):
        changed=False
        for f in range(len(boxes)):
            constraints=[('unary'+str(i),b,r2) for i,(b,r2) in enumerate(unary[f])]+[('neighbor'+str(g),boxes[g],edge) for g in adj[f]]
            for label,other,r2 in constraints:
                old=boxes[f];new=clip(old,other,r2);steps+=1
                if new is None:return {'empty':True,'boxes':boxes,'sweeps':sweep+1,'steps':steps,'failure':{'face':f,'constraint':label,'box':old,'other_box':list(other),'r2':r2}}
                if new!=old:boxes[f]=new;changed=True
        if not changed:return {'empty':False,'boxes':boxes,'fixed':True,'sweeps':sweep+1,'steps':steps}
    return {'empty':False,'boxes':boxes,'fixed':False,'sweeps':limit,'steps':steps}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-spatial-branch-independent.json');args=ap.parse_args()
    cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';sp=ROOT/'verify/out/n100-spatial-branch-trees.json';load=lambda p:json.loads(p.read_text(encoding='utf-8'));core=load(cp)['core'];prior=load(bp);z=load(sp);A=core['alpha'];fc=cycles(core['phi']);own={d:i for i,row in enumerate(fc) for d in row};outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');inner=[i for i in range(len(fc)) if i!=outer];index={f:i for i,f in enumerate(inner)};sites=[index[own[A[d]]] for d in reversed(fc[outer])];adj=[set() for _ in inner];N=len(inner);D=[[1000]*N for _ in inner]
    for i in range(N):D[i][i]=0
    for d,e in enumerate(A):
        a,b=own[d],own[e]
        if outer not in (a,b):i,j=index[a],index[b];adj[i].add(j);D[i][j]=1
    adj=[sorted(row) for row in adj]
    for k in range(N):
        for i in range(N):
            if D[i][k]>=1000:continue
            for j in range(N):D[i][j]=min(D[i][j],D[i][k]+D[k][j])
    Q=z['scale'];need(Q==2**20,'scale');axes=((1,0),(0,1),(-1,0),(0,-1));un=1154469548855829;ud=10**16
    def radius(k):return -(-((k*un*Q)**2)//(ud**2))
    summaries=[]
    for case in z['cases']:
        p=case['placement'];nodes=case['tree']['nodes'];counts=structure(nodes);need(dict(counts)==case['tree']['summary'],'summary')
        root=next(r['boxes'] for r in prior['retained'] if r['placement']==p);unary=[[([0,0,0,0],Q*Q)]+[([a*Q,a*Q,b*Q,b*Q],radius(2*D[sites[p[i]]][f]+1)) for i,(a,b) in enumerate(axes)] for f in range(N)]
        def visit(idx,B):
            node=nodes[idx];r=replay(B,unary,adj,radius(2),z['max_sweeps']);need(r==node['propagation'],'all node propagation fields')
            if node['kind']=='excluded':need(r['empty'],'empty leaf');return
            need(not r['empty'],'nonempty node')
            if node['kind']=='split':
                f,d=node['face'],node['coordinate'];need(f in case['focus_faces'] and d in (0,1),'split variable');lo,hi=r['boxes'][f][2*d:2*d+2];need([lo,hi]==node['interval'],'parent interval');mid=node['split'];need(lo<mid<hi,'cover split')
                left=[b[:] for b in r['boxes']];right=[b[:] for b in r['boxes']];left[f][2*d+1]=mid;right[f][2*d]=mid
                visit(node['children'][0],left);visit(node['children'][1],right)
        visit(0,root);need(case['tree']['root_excluded']==(counts['unresolved']==0),'root exclusion')
        need(case['tree']['steps']==sum(row['propagation']['steps'] for row in nodes),'steps')
        summaries.append({'placement':p,'nodes':len(nodes),'counts':dict(counts),'root_excluded':case['tree']['root_excluded']})
    controls=[]
    for label,alter in [('duplicate_child',lambda n:n[0]['children'].__setitem__(1,n[0]['children'][0])),('nonproper_split',lambda n:n[0].__setitem__('split',n[0]['interval'][1]))]:
        damaged=copy.deepcopy(z['cases'][0]['tree']['nodes']);alter(damaged)
        try:structure(damaged)
        except ValueError:controls.append(label)
    need(len(controls)==2,'structural controls')
    out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-spatial-branch-independent/v1','verified':True,'case_summaries':summaries,'all_node_propagations_replayed':True,'all_splits_cover_parent':True,'no_missing_or_duplicate_children':True,'rejected_controls':controls,'method':'independent Floyd distances and prior independent interval contractor; tree traversal checks exact parent-child reconstruction; shares prior core adapter convention','machine_verified_geometry':False,'global_optimality':False,'scope':'two bounded fixed-core root domains; unresolved leaves retained, not feasible-cover witnesses','bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,sp,ROOT/'verify/n100_axis_coupled_boxes_independent.py')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print('PASS independent complete branch trees:',summaries,';2 structural corruptions rejected')
if __name__=='__main__':main()
