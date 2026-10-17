"""Find Hall-deficient subsets of a supplied pairwise-separated witness pool.
The augmenting-path search is complete for that pool, not for all geometric witnesses.
"""
from fractions import Fraction as F
from pathlib import Path
import json, hashlib, copy
from n100_separated_witness_hall import verify as check_leaf
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok: raise ValueError(msg)
def find(box,points):
    need(len(box)%2==1 and len(box)>=3,'dimension')
    B=[tuple(map(F,z)) for z in box]
    need(all(len(z)==2 and z[0]<=z[1] for z in B) and B[-1][0]>=0,'box')
    P=[tuple(map(F,p)) for p in points];n=(len(B)-1)//2;T=B[-1][1]
    need(all(len(p)==2 and sum(x*x for x in p)<=1 for p in P),'target')
    need(all(sum((a-b)**2 for a,b in zip(p,q))>4*T for i,p in enumerate(P) for q in P[:i]),'separation')
    def lower(p,j):
        total=F(0)
        for x,(lo,hi) in zip(p,B[2*j:2*j+2]):
            if x<lo: total+=(lo-x)**2
            elif x>hi: total+=(x-hi)**2
        return total
    adj=[[j for j in range(n) if lower(p,j)<=T] for p in P]
    match={}
    def augment(i,seen):
        for j in adj[i]:
            if j in seen:continue
            seen.add(j)
            if j not in match or augment(match[j],seen):
                match[j]=i
                return True
        return False
    for i in range(len(P)):
        seen=set()
        if not augment(i,seen):
            # Alternating reachable vertices yield |N(S)| < |S|.
            subset={i}|{match[j] for j in seen if j in match}
            raw=[[str(x) for x in P[k]] for k in sorted(subset)]
            certificate=check_leaf(box,raw)
            return {'excluded':True,'selected_indices':sorted(subset),'points':raw,'leaf':certificate,'adjacency':adj}
    return {'excluded':False,'matching':[[i,j] for j,i in sorted(match.items())],'adjacency':adj,'scope':'no Hall deficiency in supplied separated pool'}

def independent(box,points):
    # Recompute distances with clamping; no imported geometry arithmetic.
    t=F(box[-1][1]);P=[tuple(map(F,p)) for p in points]
    need(all(sum(x*x for x in p)<=1 for p in P),'outside')
    need(all(sum((p[k]-q[k])**2 for k in (0,1))>4*t for i,p in enumerate(P) for q in P[:i]),'separation')
    union=set()
    for p in P:
        for j in range((len(box)-1)//2):
            nearest=[min(max(p[k],F(box[2*j+k][0])),F(box[2*j+k][1])) for k in (0,1)]
            if sum((p[k]-nearest[k])**2 for k in (0,1))<=t:union.add(j)
    need(len(union)<len(P),'no deficiency')
    return {'verified':True,'union':sorted(union),'deficiency':len(P)-len(union)}

def main():
    u=F(1154469548855829,10**16);t=u*u
    pool=[['1','0'],['3/5','4/5'],['0','1'],['-3/5','4/5'],['-1','0'],['-3/5','-4/5'],['0','-1'],['3/5','-4/5']]
    # The pool is not selected by the algorithm to fit the example.
    results=[]
    for available in (1,3,7,8):
        box=[['-1/2','1/2'] for _ in range(2*(100-available))]+[['-1','1'] for _ in range(2*available)]+[['0',str(t)]]
        z=find(box,pool)
        need(z['excluded']==(available<8),'matching control')
        if z['excluded']:
            z['independent']=independent(box,z['points'])
        else:
            need(len(z['matching'])==8 and len({j for i,j in z['matching']})==8,'injective matching')
        results.append({'available_outer_centers':available,'root_box':box,'result':z})
    full=[['-1','1'] for _ in range(200)]+[['0',str(t)]]
    need(not find(full,pool)['excluded'],'false global exclusion')
    rejected=[]
    for label,points in [('duplicate',pool+[pool[0]]),('outside',pool+[['2','0']])]:
        try:find(full,points)
        except ValueError:rejected.append(label)
    bad=copy.deepcopy(results[0]['result']['points']);bad[0]=['0','0']
    try:independent(results[0]['root_box'],bad)
    except ValueError:rejected.append('corrupted_selected_witness')
    need(len(rejected)==3,'negative controls')
    output={'schema':'n100-hall-automatic-search/v1','verified':True,'pool':pool,'results':results,
        'full_center_domain_not_excluded':True,'negative_controls_rejected':rejected,
        'algorithm':'augmenting paths; failed path gives alternating reachable Hall subset',
        'complete_for_supplied_separated_pool':True,'complete_for_all_geometric_witnesses':False,
        'arithmetic':'Fraction only','global_optimality':False,'minimal_polynomial_obtained':False,
        'scope':'general search implementation calibrated on restricted 100-center boxes; no candidate-neighborhood or count-family exclusion',
        'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['verify/n100_separated_witness_hall.py','verify/n100_global_witness_tree.py']},
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=ROOT/'verify/out/n100-hall-automatic-search.json';need(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('PASS automatic Hall subsets for 1/3/7 available centers; 8-center and full-domain controls not excluded; independent leaf arithmetic and 3 corruptions rejected')
if __name__=='__main__':main()
