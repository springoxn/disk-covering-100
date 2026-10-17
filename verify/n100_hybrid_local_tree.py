"""Hybrid exact partition checker; reuses frozen witness checker and validates LOCAL separately."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
import n100_global_witness_tree as base
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
req=base.require
BP='verify/out/n100-local-widened-budget.json';IP='verify/out/n100-local-widened-independent.json'
MP='runtime/external-disk100-strict-local-replay/source/rational_midpoint.json'
LP='verify/out/n100-local-chain-ledger.json'

def context():
    b=load(BP);i=load(IP);m=load(MP);ledger=load(LP)
    req(b['verified'] and i['audit_verified'] and ledger['verified_local_chain_bindings'],'acceptance')
    req(i['parent_certificate']['receipt_sha256']==sha(BP),'independent budget binding')
    req(i['parent_certificate']['script_sha256']==b['checker_sha256']==sha('verify/n100_local_widened_budget.py'),'budget script')
    req(i['checker_sha256']==sha('verify/n100_local_widened_independent.py'),'audit script')
    for p,h in b['dependencies_sha256'].items():req(sha(p)==h,'budget dependency')
    for owner,p,h in ledger['hash_links']:req(sha(p)==h,'ledger dependency')
    x=[F(int(v),int(m['denominator'])) for v in m['numerators']]
    binding={p:sha(p) for p in (BP,IP,MP,LP)}
    return x,F(1,10**58),F(b['constants']['ungauged_center_radius']),binding

def scale(a,I):return tuple(sorted((a*I[0],a*I[1])))
def add(I,J):return I[0]+J[0],I[1]+J[1]

def local(box,node,ctx):
    x,rho,eps,binding=ctx
    req(len(box)==201,'LOCAL requires 100 centers')
    req(node['binding']==binding,'LOCAL binding')
    perm=node['permutation'];req(len(perm)==100 and all(type(v) is int for v in perm) and sorted(perm)==list(range(100)),'permutation')
    a,b=map(F,node['rotation']);req(a*a+b*b==1,'orthogonal rotation')
    # Forward map from input label perm[j] to root label j; root-frame inclusion.
    for j,k in enumerate(perm):
        u,v=box[2*k:2*k+2]
        for d,I in enumerate((add(scale(a,u),scale(-b,v)),add(scale(b,u),scale(a,v)))):
            req(max(abs(I[0]-x[2*j+d]),abs(I[1]-x[2*j+d]))+rho<=eps,'LOCAL center inclusion')
    req(box[-1][0]>=0 and box[-1][1]<x[492]-rho,'LOCAL strict endpoint')

def verify(tree,global_required=True):
    req(tree['schema']=='disk-cover-hybrid-tree/v1','schema')
    n=tree['n'];req(type(n) is int and n>=1,'n')
    box=[base.interval(v) for v in tree['root_box']];req(len(box)==2*n+1 and box[-1][0]>=0,'root')
    full=all(I==(F(-1),F(1)) for I in box[:-1]) and box[-1][0]==0
    req(full or not global_required,'restricted root')
    ctx=context();seen=set();stack=[(tree['root'],box)];locals_count=0
    while stack:
        key,B=stack.pop();req(key not in seen,'cycle/shared');seen.add(key);node=tree['nodes'][key]
        if node['type']=='SPLIT':
            d=node['coordinate'];req(type(d) is int and 0<=d<len(B),'coordinate')
            c=F(node['cut']);lo,hi=B[d];req(lo<c<hi,'cut')
            L=list(B);U=list(B);L[d]=(lo,c);U[d]=(c,hi)
            stack.extend([(node['left'],L),(node['right'],U)])
        elif node['type']=='LOCAL_ROOT_CENTER_BOX':local(B,node,ctx);locals_count+=1
        else:
            base.verify({'schema':'disk-cover-witness-tree/v1','n':n,'root':'leaf','root_box':[[str(a),str(b)] for a,b in B],'nodes':{'leaf':node}},False)
    req(seen==set(tree['nodes']),'unreachable')
    return {'verified':True,'full_domain':full,'nodes':len(seen),'local_leaves':locals_count}

if __name__=='__main__':
    ctx=context();x,rho,eps,binding=ctx
    margins=[1-(abs(x[2*j])+rho)**2-(abs(x[2*j+1])+rho)**2 for j in range(100)]
    req(min(margins)>F(1,50),'normalized root domain')
    leaf=load('verify/out/n100-local-leaf-example.json')
    node={'type':'LOCAL_ROOT_CENTER_BOX','binding':binding,'permutation':list(range(100)),'rotation':['1','0']}
    tree={'schema':'disk-cover-hybrid-tree/v1','n':100,'root':'l','root_box':leaf['center_intervals']+[leaf['squared_radius_interval']],'nodes':{'l':node}}
    results=[verify(tree,False)]
    # Rational quarter-turn with reversed labels, independently inverse-transform each box.
    rotated=copy.deepcopy(tree);coords=rotated['root_box'];new=[]
    for k in range(100):
        j=99-k;u,v=[tuple(map(F,I)) for I in coords[2*j:2*j+2]]
        new.extend([[str(v[0]),str(v[1])],[str(-u[1]),str(-u[0])]])
    rotated['root_box']=new+[coords[-1]];rotated['nodes']['l']['permutation']=list(reversed(range(100)))
    rotated['nodes']['l']['rotation']=['0','1'];results.append(verify(rotated,False))
    rejected=[]
    tests=[]
    def test(name,mutate,g=False):
        z=copy.deepcopy(tree);mutate(z);tests.append((name,z,g))
    test('global_upgrade',lambda z:None,True)
    test('wrong_rotation',lambda z:z['nodes']['l'].__setitem__('rotation',['1','1']))
    test('duplicate_label',lambda z:z['nodes']['l']['permutation'].__setitem__(0,1))
    test('wrong_binding',lambda z:z['nodes']['l']['binding'].__setitem__(BP,'0'*64))
    test('wide_center',lambda z:z['root_box'].__setitem__(0,['-1','1']))
    test('radius_crosses_root',lambda z:z['root_box'].__setitem__(-1,['0',str(x[492]+rho)]))
    for name,z,g in tests:
        try:verify(z,g)
        except (ValueError,KeyError):rejected.append(name)
        else:raise RuntimeError('negative accepted '+name)
    op=R/'verify/out/n100-hybrid-local-tree-interface.json';req(not op.exists(),'refuse overwrite')
    op.write_text(json.dumps({'verified':True,'results':results,'rejected_controls':rejected,
        'all_100_root_center_boxes_inside_disk':True,'minimum_norm_squared_margin':str(min(margins)),
        'examples':[tree,rotated],'binding':binding,'checker_sha256':sha('verify/n100_hybrid_local_tree.py'),
        'base_checker_sha256':sha('verify/n100_global_witness_tree.py'),
        'n100_global_tree_supplied':False,'n100_global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS 100 centers inside D; LOCAL identity and rotation/relabeling; 49 ledger links; 6 controls rejected; no global tree')
