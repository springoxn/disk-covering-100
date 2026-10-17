"""Rational whole-disk cover with a disconnected Voronoi boundary owner.
Exact quadtree cells only; no floats in acceptance.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(x,msg):
    if not x:raise ValueError(msg)
C=[(F(1,2),F(0)),(F(9,10),F(0)),(F(-1,2),F(1,2)),(F(-1,2),F(-1,2))];r=F(99,100)
def d2(p,c):return sum((a-b)**2 for a,b in zip(p,c))
def certify():
    stack=[(F(-1),F(1),F(-1),F(1),0)];leaves=[]
    while stack:
        x0,x1,y0,y1,depth=stack.pop()
        lo_x=F(0) if x0<=0<=x1 else min(abs(x0),abs(x1));lo_y=F(0) if y0<=0<=y1 else min(abs(y0),abs(y1))
        if lo_x**2+lo_y**2>1:leaves.append([list(map(str,(x0,x1,y0,y1))),'outside']);continue
        corners=[(x,y) for x in (x0,x1) for y in (y0,y1)]
        index=next((j for j,c in enumerate(C) if all(d2(p,c)<=r*r for p in corners)),None)
        if index is not None:leaves.append([list(map(str,(x0,x1,y0,y1))),index]);continue
        need(depth<14,'quadtree unresolved');xm=(x0+x1)/2;ym=(y0+y1)/2
        for a,b in ((x0,xm),(xm,x1)):
            for c,d in ((y0,ym),(ym,y1)):stack.append((a,b,c,d,depth+1))
    return leaves
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-disconnected-boundary-owner-control.json');args=ap.parse_args()
    points=[(F(3,5),F(4,5)),(F(1),F(0)),(F(3,5),F(-4,5)),(F(-4,5),F(3,5))];w=[]
    for p in points:
        need(sum(x*x for x in p)==1,'unit witness');dist=[d2(p,c) for c in C];winner=min(range(4),key=lambda j:dist[j]);need(all(dist[winner]<dist[j] for j in range(4) if j!=winner),'strict winner');w.append({'point':list(map(str,p)),'distances_squared':list(map(str,dist)),'unique_owner':winner})
    need([z['unique_owner'] for z in w]==[0,1,0,2] or [z['unique_owner'] for z in w]==[0,1,0,3],'alternating owners')
    leaves=certify();out=ROOT/args.out;need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-disconnected-boundary-owner-control/v1','verified_rational_cover':True,'centers':[list(map(str,c)) for c in C],'radius':str(r),'ordered_circle_witnesses':w,'leaves':leaves,'quadtree_partition_method':'recursive midpoint4 split from[-1,1]^2; strict outside-distance or all4 corners in one convex disk','scope':'four disks at r<1 demonstrate boundary-owner disconnectedness; not n100 endpoint counterexample or generic-position certificate','analytic_dependencies':['distance to fixed center is convex so rectangle corner coverage covers rectangle','alternating strict owners on circle separate boundary owner into at least2 components'],'machine_verified_geometry':False,'n100_simple_dual_reduction_disproved_at_U':False,'global_optimality':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS rational r=.99 whole-unit-disk cover;',len(leaves),'quadtree leaves;alternating boundary owners witness disconnected cell boundary')
if __name__=='__main__':main()
