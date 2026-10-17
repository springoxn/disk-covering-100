"""Independent complete replay of unary disk-feasibility witness catalogue.
Uses direct integer inequalities and independent Floyd distance coverage.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,argparse,copy
ROOT=Path(__file__).resolve().parents[1]
def need(x,msg):
    if not x:raise ValueError(msg)
def cycles(p):
    rows=[];done=set()
    for d in range(len(p)):
        if d in done:continue
        row=[];q=d
        while q not in done:done.add(q);row.append(q);q=p[q]
        need(q==d,'cycle');rows.append(row)
    return rows
def check_catalogue(z,expected):
    un=z['radius_numerator'];ud=z['radius_denominator'];need((un,ud)==(1154469548855829,10**16),'radius')
    got={};margins=[];axes=((1,0),(0,1),(-1,0),(0,-1))
    for w in z['witnesses']:
        ds=tuple(w['distances']);need(ds not in got,'duplicate vector');x,y,q=w['point_integer_xy_denominator'];need(q>0 and x*x+y*y<=q*q,'unit disk')
        for (a,b),d in zip(axes,ds):
            gap=((2*d+1)*un*q)**2-((x-a*q)**2+(y-b*q)**2)*ud**2
            need(gap>=0,'axis disk');margins.append(gap)
        got[ds]=w['occurrences']
    need(got==dict(expected),'catalogue coverage/multiplicity')
    need(z['unresolved_count']==0 and z['unresolved']==[] and z['all_unary_intersections_certified_nonempty'],'no unresolved')
    need(len(got)==z['unique_distance_vectors']==z['rational_witness_count'] and sum(got.values())==z['face_placement_pairs'],'totals')
    return min(margins)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-axis-unary-independent.json');args=ap.parse_args()
    cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';pp=ROOT/'verify/out/n100-axis-dual-chain-pruning.json';sp=ROOT/'verify/out/n100-axis-unary-feasibility.json';load=lambda p:json.loads(p.read_text(encoding='utf-8'))
    core=load(cp)['core'];prior=load(pp);z=load(sp);A=core['alpha'];fc=cycles(core['phi']);n=len(fc);own={d:i for i,row in enumerate(fc) for d in row};outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');sites=[own[A[d]] for d in reversed(fc[outer])]
    D=[[1000]*n for _ in range(n)]
    for i in range(n):D[i][i]=0
    for d,e in enumerate(A):
        i,j=own[d],own[e]
        if outer not in (i,j):D[i][j]=D[j][i]=1
    for k in range(n):
        if k==outer:continue
        for i in range(n):
            if D[i][k]>=1000:continue
            for j in range(n):
                alt=D[i][k]+D[k][j]
                if alt<D[i][j]:D[i][j]=alt
    need(len(prior['retained_axis_edge_placements'])==4776,'placement count')
    expected=Counter(tuple(D[sites[p[i]]][f] for i in range(4)) for p in prior['retained_axis_edge_placements'] for f in range(n) if f!=outer)
    gap=check_catalogue(z,expected);controls=[]
    for name,alter in [('missing_vector',lambda q:q['witnesses'].pop()),('outside_point',lambda q:q['witnesses'][0].__setitem__('point_integer_xy_denominator',[100,100,1])),('wrong_multiplicity',lambda q:q['witnesses'][0].__setitem__('occurrences',0)),('wrong_radius',lambda q:q.__setitem__('radius_numerator',1))]:
        damaged=copy.deepcopy(z);alter(damaged)
        try:check_catalogue(damaged,expected)
        except ValueError:controls.append(name)
    need(len(controls)==4,'corruption controls')
    out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-axis-unary-independent/v1','verified':True,'distance_vectors':len(expected),'face_placement_pairs':sum(expected.values()),'all_five_disk_constraints_checked':True,'min_integer_axis_slack':gap,'complete_catalogue_matches_independent_floyd':True,'rejected_controls':controls,'method':'no witness generator import; integer inequalities and independently recomputed distances and multiplicities','scope':'product of per-face unary relaxations only, not a feasible covering or coupled model','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,pp,sp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent integer witnesses:',len(expected),'vectors,',sum(expected.values()),'face-placement pairs;4 corruptions rejected;minimum integer slack',gap)
if __name__=='__main__':main()
