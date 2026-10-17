"""Independent replay of coupled-box certificates with exact integer bounds."""
from pathlib import Path
from math import isqrt
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def require(ok,msg):
    if not ok:raise ValueError(msg)
def cycles(p):
    seen=set();rows=[]
    for d in range(len(p)):
        if d in seen:continue
        q=d;row=[]
        while q not in seen:seen.add(q);row.append(q);q=p[q]
        require(q==d,'cycle');rows.append(row)
    return rows
def upper_sqrt(v):
    require(v>=0,'sqrt');return isqrt(v-1)+1 if v else 0

def clip(box,other,r2):
    dx=max(box[0]-other[1],other[0]-box[1],0);dy=max(box[2]-other[3],other[2]-box[3],0)
    if dx*dx+dy*dy>r2:return None
    out=[]
    for dim in (0,1):
        j=2*(1-dim);near=max(box[j]-other[j+1],other[j]-box[j+1],0);available=r2-near*near
        if available<0:return None
        step=upper_sqrt(available);k=2*dim;low=max(box[k],other[k]-step);high=min(box[k+1],other[k+1]+step)
        if low>high:return None
        out.extend((low,high))
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-axis-coupled-boxes-independent.json');args=ap.parse_args()
    cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';pp=ROOT/'verify/out/n100-axis-dual-chain-pruning.json';sp=ROOT/'verify/out/n100-axis-coupled-boxes.json';load=lambda p:json.loads(p.read_text(encoding='utf-8'))
    core=load(cp)['core'];prior=load(pp);z=load(sp);A=core['alpha'];fc=cycles(core['phi']);own={d:i for i,row in enumerate(fc) for d in row};outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');inner=[i for i in range(len(fc)) if i!=outer];index={f:i for i,f in enumerate(inner)};sites=[index[own[A[d]]] for d in reversed(fc[outer])];adj=[set() for _ in inner];N=len(inner)
    D=[[1000]*N for _ in inner]
    for i in range(N):D[i][i]=0
    for d,e in enumerate(A):
        f,g=own[d],own[e]
        if outer not in (f,g):i,j=index[f],index[g];adj[i].add(j);D[i][j]=1
    for k in range(N):
        for i in range(N):
            if D[i][k]>=1000:continue
            for j in range(N):D[i][j]=min(D[i][j],D[i][k]+D[k][j])
    Q=z['scale'];un=z['radius_numerator'];ud=z['radius_denominator'];require((Q,un,ud)==(2**20,1154469548855829,10**16),'parameters')
    def radius(k):
        v=(k*un*Q)**2;d=ud**2;return -(-v//d)
    edge=radius(2);require(edge==z['edge_radius_squared_upper_scaled'],'edge radius')
    require(clip([0,0,0,0],[3,3,4,4],24) is None and clip([0,0,0,0],[3,3,4,4],25)==[0,0,0,0],'tangent control')
    saved={tuple(row['placement']):(False,row) for row in z['retained']}
    for row in z['excluded']:require(tuple(row['placement']) not in saved,'duplicate');saved[tuple(row['placement'])]=(True,row['result'])
    require(set(saved)==set(map(tuple,prior['retained_axis_edge_placements'])),'full placement partition')
    axes=((1,0),(0,1),(-1,0),(0,-1));checked=0;excluded=0;total=0
    for p in prior['retained_axis_edge_placements']:
        is_excluded,row=saved[tuple(p)];boxes=[[-Q,Q,-Q,Q] for _ in inner];unary=[];failure=None;fixed=False
        for f in range(N):
            unary.append([([0,0,0,0],Q*Q)]+[([a*Q,a*Q,b*Q,b*Q],radius(2*D[sites[p[i]]][f]+1)) for i,(a,b) in enumerate(axes)])
        for sweep in range(z['maximum_sweeps']):
            changed=False
            for f in range(N):
                cons=[('unary'+str(i),point,r2) for i,(point,r2) in enumerate(unary[f])]+[('neighbor'+str(g),boxes[g],edge) for g in sorted(adj[f])]
                for label,other,r2 in cons:
                    old=boxes[f];new=clip(old,other,r2);total+=1
                    if new is None:failure={'face':f,'constraint':label,'box':old,'other_box':list(other),'radius_squared_upper':r2};break
                    if old!=new:boxes[f]=new;changed=True
                if failure:break
            if failure:break
            if not changed:fixed=True;break
        require((failure is not None)==is_excluded,'exclusion replay')
        require(boxes==row['boxes'] and sweep+1==row['sweeps'],'exact final boxes/sweeps')
        if failure:require(failure==row['failure'],'failure witness');excluded+=1
        else:require(fixed==row['fixed_point'],'fixed status')
        checked+=1
    require(total==z['contractions'] and excluded==z['excluded_count'] and checked-excluded==z['retained_count'],'totals')
    # Test enough square-root rounding boundaries to reject floor-root misuse.
    require(all((upper_sqrt(v)-1)**2<v<=upper_sqrt(v)**2 for v in range(1,1000)),'rounding inequalities')
    out=ROOT/args.out;require(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-axis-coupled-boxes-independent/v1','verified':True,'placements_replayed':checked,'excluded_count':excluded,'retained_count':checked-excluded,'contractions_replayed':total,'all_final_boxes_and_failures_equal':True,'method':'independent Floyd distances, independent interval contractor, alternate upward sqrt and radius division; complete schedule replay','rounding_boundaries_checked':999,'tangent_controls_passed':True,'machine_verified_geometry':False,'global_optimality':False,'scope':'sound interval relaxation of fixed-core center constraints only; unresolved boxes do not certify feasibility','bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,pp,sp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent coupled boxes:',checked,'placements',excluded,'excluded',total,'contractions;all final boxes equal')
if __name__=='__main__':main()
