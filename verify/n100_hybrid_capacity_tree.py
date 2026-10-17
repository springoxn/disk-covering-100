"""Hybrid tree v3: frozen v2 leaves plus exact small-pool capacity leaves."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
import n100_hybrid_hall_tree as prior
from n100_nonseparated_capacity_cut import cut, independent_capacity
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def verify(tree,global_required=True):
    need(tree['schema']=='disk-cover-hybrid-tree/v3','schema')
    n=tree['n'];need(type(n) is int and n>0,'n')
    box=[tuple(map(F,z)) for z in tree['root_box']]
    need(len(box)==2*n+1 and all(len(z)==2 and z[0]<=z[1] for z in box) and box[-1][0]>=0,'box')
    full=all(z==(F(-1),F(1)) for z in box[:-1]) and box[-1][0]==0
    need(full or not global_required,'restricted root')
    seen=set();stack=[(tree['root'],box)];leaves=0;splits=0
    while stack:
        key,b=stack.pop();need(key not in seen and key in tree['nodes'],'missing/shared/cyclic node');seen.add(key)
        node=tree['nodes'][key]
        if node['type']=='SPLIT':
            d=node['coordinate'];need(type(d) is int and 0<=d<len(b),'coordinate');c=F(node['cut']);lo,hi=b[d];need(lo<c<hi,'cut')
            left=b.copy();right=b.copy();left[d]=(lo,c);right[d]=(c,hi)
            stack.extend([(node['left'],left),(node['right'],right)]);splits+=1
        else:
            raw=[[str(lo),str(hi)] for lo,hi in b]
            if node['type']=='WITNESS_CAPACITY':
                result=cut(raw,node['points']);need(result['excluded'],'no capacity deficit')
                independent_capacity(raw,node['points'],result)
            else:
                prior.verify({'schema':'disk-cover-hybrid-tree/v2','n':n,'root':'l','root_box':raw,'nodes':{'l':node}},False)
            leaves+=1
    need(seen==set(tree['nodes']),'unreachable')
    return {'verified':True,'full_domain':full,'nodes':len(seen),'splits':splits,'leaves':leaves}
def main():
    p=ROOT/'verify/out/n100-nonseparated-capacity-cut.json';z=json.loads(p.read_text(encoding='utf-8'))
    leaf={'type':'WITNESS_CAPACITY','points':z['points']}
    tree={'schema':'disk-cover-hybrid-tree/v3','n':100,'root':'s','root_box':z['root_box'],'nodes':{'s':{'type':'SPLIT','coordinate':199,'cut':'0','left':'l','right':'r'},'l':leaf,'r':copy.deepcopy(leaf)}}
    result=verify(tree,False);rejected=[]
    for label,mutation,g in [('global_upgrade',lambda q:None,True),('missing_child',lambda q:q['nodes'].pop('l'),False),('two_outer_centers',lambda q:q['root_box'].__setitem__(196,['-1','1']),False)]:
        q=copy.deepcopy(tree);mutation(q)
        try:verify(q,g)
        except (ValueError,KeyError):rejected.append(label)
    need(len(rejected)==3,'controls')
    # Real candidate center boxes are a negative control, not a new exclusion.
    mp=ROOT/'runtime/external-disk100-strict-local-replay/source/rational_midpoint.json'
    mid=json.loads(mp.read_text(encoding='utf-8'));den=int(mid['denominator']);u=F(z['radius_upper'])
    checks=[]
    for width in (F(1,1000),F(1,100),F(1,10)):
        candidate=[]
        for value in mid['numerators'][:200]:
            x=F(int(value),den);candidate.append([str(x-width),str(x+width)])
        candidate.append(['0',str(u*u)])
        control=cut(candidate,z['points']);need(not control['excluded'],'false candidate exclusion')
        checks.append({'half_width':str(width),'capacity_sum':control['capacity_sum'],'excluded':False})
    output={'schema':'n100-hybrid-capacity-tree-calibration/v1','verified':True,'tree':tree,'result':result,'negative_controls_rejected':rejected,'candidate_center_box_controls':checks,
        'global_optimality':False,'minimal_polynomial_obtained':False,'complete_global_tree_supplied':False,
        'scope':'capacity leaves with exact inherited split boxes; calibration only; no new count-family exclusion',
        'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [p,mp,ROOT/'verify/n100_nonseparated_capacity_cut.py',ROOT/'verify/n100_hybrid_hall_tree.py']},
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=ROOT/'verify/out/n100-hybrid-capacity-tree.json';need(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('PASS v3 inherited capacity leaves; 3 tree corruptions rejected; actual candidate boxes at 3 widths not excluded')
if __name__=='__main__':main()
