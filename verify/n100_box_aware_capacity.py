"""Exact box-aware witness patterns and finite-pool union dynamic programming.
Every discarded pattern has a rational average squared-distance obstruction.
Retained patterns are a relaxation: no completeness claim for disk/box feasibility.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def point_distance(p,rect):
    return sum((lo-x)**2 if x<lo else ((x-hi)**2 if x>hi else F(0)) for x,(lo,hi) in zip(p,rect))
def mean_bound(points,rect):
    n=len(points);mean=tuple(sum(p[d] for p in points)/n for d in (0,1))
    variance=sum(sum((p[d]-mean[d])**2 for d in (0,1)) for p in points)/n
    return variance+point_distance(mean,rect)
def patterns(box,raw):
    B=[tuple(map(F,z)) for z in box];P=[tuple(map(F,p)) for p in raw]
    need(len(B)>=3 and len(B)%2==1 and all(len(z)==2 and z[0]<=z[1] for z in B) and B[-1][0]>=0,'box')
    need(0<len(P)<=12 and len(set(P))==len(P) and all(len(p)==2 and sum(x*x for x in p)<=1 for p in P),'pool')
    t=B[-1][1];rows=[]
    for j in range((len(B)-1)//2):
        rect=B[2*j:2*j+2]
        reach=sum(1<<i for i,p in enumerate(P) if point_distance(p,rect)<=t)
        allowed=[0];bad=[]
        subsets=[];s=reach
        while s:
            subsets.append(s);s=(s-1)&reach
        subsets.sort(key=lambda s:(s.bit_count(),s))
        for s in subsets:
            if any(s&v==v for v in bad):continue
            pts=[p for i,p in enumerate(P) if s>>i&1]
            lb=mean_bound(pts,rect)
            if lb>t:bad.append(s)
            else:allowed.append(s)
        maximal=[s for s in allowed if not any(s!=v and s&v==s for v in allowed)]
        rows.append({'reachable_mask':reach,'rejected_minimal_masks':bad,'maximal_retained_masks':maximal})
    return rows

def solve_patterns(rows,size):
    target=(1<<size)-1;states={0};trace=[1]
    for row in rows:
        states={s|v for s in states for v in row['maximal_retained_masks']}
        # A larger covered set dominates each of its subsets for future union coverage.
        states={s for s in states if not any(s!=v and s&v==s for v in states)}
        trace.append(len(states))
        if target in states:return {'excluded':False,'state_counts':trace,'reason':'relaxed union covers pool'}
    return {'excluded':True,'state_counts':trace,'terminal_masks':sorted(states),'reason':'no union of one retained pattern per center covers pool'}
def search(box,points):
    rows=patterns(box,points)
    return {'rows':rows,**solve_patterns(rows,len(points))}

def independent(box,raw,result):
    P=[tuple(map(F,p)) for p in raw];t=F(box[-1][1]);rows=[]
    for j,row in enumerate(result['rows']):
        rect=[tuple(map(F,box[2*j+d])) for d in (0,1)]
        reach=0
        for i,p in enumerate(P):
            q=[min(max(p[d],rect[d][0]),rect[d][1]) for d in (0,1)]
            if sum((p[d]-q[d])**2 for d in (0,1))<=t:reach|=1<<i
        need(reach==row['reachable_mask'],'reach mismatch')
        for s in row['rejected_minimal_masks']:
            pts=[p for i,p in enumerate(P) if s>>i&1];need(bool(pts) and s&reach==s,'invalid rejecting subset')
            mean=[sum(p[d] for p in pts)/len(pts) for d in (0,1)]
            q=[min(max(mean[d],rect[d][0]),rect[d][1]) for d in (0,1)]
            # Independent average evaluated at the box projection of the barycenter.
            total=sum(sum((p[d]-q[d])**2 for d in (0,1)) for p in pts)
            need(total>len(pts)*t,'invalid energy obstruction')
        allowed=[s for s in range(1<<len(P)) if s&reach==s and not any(s&b==b for b in row['rejected_minimal_masks'])]
        maximal=[s for s in allowed if not any(s!=v and s&v==s for v in allowed)]
        need(maximal==sorted(row['maximal_retained_masks']),'retained mask omission')
        rows.append(maximal)
    # Independent bitset-of-states implementation, retains all states (no dominance pruning).
    states={0}
    for options in rows:states={a|b for a in states for b in options}
    excluded=(1<<len(P))-1 not in states
    need(excluded==result['excluded'],'union DP mismatch')
    return {'verified':True,'excluded':excluded,'terminal_state_count_without_dominance':len(states)}

def main():
    from n100_nonseparated_capacity_cut import cut
    import copy
    u=F(1154469548855829,10**16);t=u*u
    pool=[['67/100','0'],['83/100','0']]
    box=[['-1/2','1/2'] for _ in range(198)]+[['13/20','17/20'],['9/100','1/10'],['0',str(t)]]
    old=cut(box,pool);need(not old['excluded'],'old checker unexpectedly strong')
    z=search(box,pool);need(z['excluded'],'box pair not excluded');audit=independent(box,pool,z)
    compatible=copy.deepcopy(box);compatible[199]=['0','1/10'];c=search(compatible,pool);need(not c['excluded'],'valid common center control');independent(compatible,pool,c)
    # Hall subset hidden by an irrelevant witness with excess neighboring capacity.
    pool2=pool+[['-3/4','0']]
    box2=copy.deepcopy(box);box2[0:4]=[['-4/5','-7/10'],['0','0'],['-4/5','-7/10'],['0','0']]
    z2=search(box2,pool2);need(z2['excluded'],'hidden deficiency missed');audit2=independent(box2,pool2,z2)
    old2=cut(box2,pool2);need(not old2['excluded'],'old whole-pool capacity cut already excludes')
    rejected=[]
    for label,change in [('omit_feasible_pattern',lambda q:q['rows'][99].__setitem__('maximal_retained_masks',[0])),('fake_reject_singleton',lambda q:q['rows'][99]['rejected_minimal_masks'].append(1)),('false_union_result',lambda q:q.__setitem__('excluded',False))]:
        q=copy.deepcopy(z);change(q)
        try:independent(box,pool,q)
        except ValueError:rejected.append(label)
    need(len(rejected)==3,'negative controls')
    output={'schema':'n100-box-aware-capacity/v1','verified':True,'radius_upper':str(u),'pool':pool,'box':box,'old_capacity_not_excluded':True,'result':z,'independent':audit,
        'common_center_control_not_excluded':True,'hidden_deficiency_case':{'pool':pool2,'box':box2,'result':z2,'independent':audit2,'old_whole_pool_capacity_not_excluded':True},
        'negative_controls_rejected':rejected,'arithmetic':'Fraction only',
        'analytic_dependency':'sum ||c-p_i||^2 = k||c-mean||^2 + sum ||p_i-mean||^2; nearest point to rectangle is coordinate clamp',
        'retained_patterns_are_overapproximation':True,'complete_for_retained_finite_patterns':True,'global_optimality':False,'new_count_families_excluded':0,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=ROOT/'verify/out/n100-box-aware-capacity.json';need(not out.exists(),'refuse overwrite');out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('PASS box-aware pair and hidden-subset cuts missed by old capacity; independent energy/union DP; feasible-center control and 3 corruptions')
if __name__=='__main__':main()
