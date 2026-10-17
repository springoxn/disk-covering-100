"""v2 adapter retaining frozen v1 artifacts; add separated-witness Hall leaves."""
from pathlib import Path
import json,hashlib,copy
from fractions import Fraction as F
import n100_hybrid_local_tree as old
import n100_separated_witness_hall as hall
R=Path(__file__).resolve().parents[1];req=old.req

def verify(z,global_required=True):
    req(z['schema']=='disk-cover-hybrid-tree/v2','schema')
    n=z['n'];req(type(n) is int and n>0,'n')
    B=[old.base.interval(p) for p in z['root_box']]
    req(len(B)==2*n+1 and B[-1][0]>=0,'root')
    full=all(p==(F(-1),F(1)) for p in B[:-1]) and B[-1][0]==0
    req(full or not global_required,'restricted root')
    seen=set();stack=[(z['root'],B)];counts={'hall':0,'other':0,'split':0}
    while stack:
        k,b=stack.pop();req(k not in seen,'cycle/shared');seen.add(k);node=z['nodes'][k]
        if node['type']=='SPLIT':
            d=node['coordinate'];req(type(d) is int and 0<=d<len(b),'coordinate');c=F(node['cut'])
            lo,hi=b[d];req(lo<c<hi,'cut');l=list(b);r=list(b);l[d]=(lo,c);r[d]=(c,hi)
            stack.extend([(node['left'],l),(node['right'],r)]);counts['split']+=1
        else:
            raw=[[str(a),str(v)] for a,v in b]
            if node['type']=='SEPARATED_WITNESS_HALL':hall.verify(raw,node['points']);counts['hall']+=1
            else:old.verify({'schema':'disk-cover-hybrid-tree/v1','n':n,'root':'leaf','root_box':raw,'nodes':{'leaf':node}},False);counts['other']+=1
    req(seen==set(z['nodes']),'unreachable')
    return {'verified':True,'full_domain':full,'nodes':len(seen),'leaf_counts':counts}

if __name__=='__main__':
    h=hall.json.loads((R/'verify/out/n100-separated-witness-hall.json').read_text(encoding='utf-8'))
    leaf={'type':'SEPARATED_WITNESS_HALL','points':h['example_points']}
    z={'schema':'disk-cover-hybrid-tree/v2','n':100,'root':'s','root_box':h['example_box'],
       'nodes':{'s':{'type':'SPLIT','coordinate':199,'cut':'0','left':'l','right':'r'},'l':leaf,'r':copy.deepcopy(leaf)}}
    result=verify(z,False);rejected=[]
    for name,mutate,g in [('global_upgrade',lambda q:None,True),('missing_hall_child',lambda q:q['nodes'].pop('l'),False),
                         ('duplicate_hall_points',lambda q:q['nodes']['r']['points'].__setitem__(1,['-1','0']),False)]:
        q=copy.deepcopy(z);mutate(q)
        try:verify(q,g)
        except (ValueError,KeyError):rejected.append(name)
        else:raise RuntimeError('control accepted')
    # Replay previously saved LOCAL examples through v2 to check compatibility.
    saved=json.loads((R/'verify/out/n100-hybrid-local-tree-interface.json').read_text(encoding='utf-8'))
    compat=[]
    for q in saved['examples']:
        q['schema']='disk-cover-hybrid-tree/v2';compat.append(verify(q,False))
    p=R/'verify/out/n100-hybrid-hall-tree.json';req(not p.exists(),'refuse overwrite')
    p.write_text(json.dumps({'verified':True,'hall_tree':z,'result':result,'local_compatibility':compat,
        'rejected_controls':rejected,'n100_global_tree_supplied':False,'global_optimality':False,
        'bindings':{v:old.sha(v) for v in ['verify/n100_hybrid_local_tree.py','verify/n100_separated_witness_hall.py','verify/out/n100-separated-witness-hall.json','verify/out/n100-hybrid-local-tree-interface.json']},
        'checker_sha256':old.sha('verify/n100_hybrid_hall_tree.py')},indent=2)+'\n',encoding='utf-8')
    print('PASS two Hall leaves inherit split boxes; two LOCAL examples compatible; three tree controls rejected')
