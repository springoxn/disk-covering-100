"""Exact witness/partition verifier. No floating point and no contact topology assumptions.
The mathematical compactness justification is in docs/n100-global-witness-tree.md.
"""
from fractions import Fraction as F
from pathlib import Path
import json, hashlib, copy
ROOT=Path(__file__).resolve().parents[1]

def require(ok, message):
    if not ok: raise ValueError(message)

def interval(raw):
    require(isinstance(raw,list) and len(raw)==2,'interval shape')
    a,b=map(F,raw); require(a<=b,'reversed interval'); return a,b

def dist1(p, ab):
    a,b=ab
    return (a-p)**2 if p<a else ((p-b)**2 if p>b else F(0))

def verify(tree, require_global=True):
    require(tree.get('schema')=='disk-cover-witness-tree/v1','schema')
    n=tree['n']; require(type(n) is int and n>=1,'n')
    box=[interval(z) for z in tree['root_box']]
    require(len(box)==2*n+1,'root dimension')
    require(box[-1][0]>=0,'negative squared radius')
    full=all(z==(F(-1),F(1)) for z in box[:-1]) and box[-1][0]==0
    if require_global: require(full,'not the full normalized center domain')
    nodes=tree['nodes']; require(isinstance(nodes,dict),'node table')
    seen=set(); stats={'splits':0,'witness_leaves':0,'outside_disk_leaves':0}
    # Explicit stack makes termination and exact child inheritance independent of recursion limits.
    stack=[(tree['root'],box)]
    while stack:
        key,b=stack.pop()
        require(isinstance(key,str) and key in nodes,'missing node')
        require(key not in seen,'cycle or shared node'); seen.add(key)
        node=nodes[key]; kind=node['type']
        if kind=='SPLIT':
            d=node['coordinate']; require(type(d) is int and 0<=d<len(b),'split coordinate')
            cut=F(node['cut']); lo,hi=b[d]; require(lo<cut<hi,'split not interior')
            left=list(b);right=list(b);left[d]=(lo,cut);right[d]=(cut,hi)
            stats['splits']+=1
            stack.extend([(node['left'],left),(node['right'],right)])
        elif kind=='WITNESS':
            p=list(map(F,node['point'])); require(len(p)==2,'witness dimension')
            require(sum(v*v for v in p)<=1,'witness outside target')
            lower=[dist1(p[0],b[2*j])+dist1(p[1],b[2*j+1]) for j in range(n)]
            require(all(v>b[-1][1] for v in lower),'witness fails strict all-center exclusion')
            stats['witness_leaves']+=1
        elif kind=='OUTSIDE_CENTER_DISK':
            j=node['center'];require(type(j) is int and 0<=j<n,'center index')
            require(dist1(F(0),b[2*j])+dist1(F(0),b[2*j+1])>1,'center domain not outside')
            stats['outside_disk_leaves']+=1
        else: raise ValueError('unknown leaf type')
    require(seen==set(nodes),'unreachable nodes')
    return {'verified':True,'n':n,'full_normalized_domain':full,
            'squared_radius_upper':str(box[-1][1]),'nodes':len(seen),**stats,
            'scope':'all normalized configurations' if full else 'specified root box only'}

def make_root(n,T):return [['-1','1'] for _ in range(2*n)]+[['0',str(T)]]

def controls():
    # A full n=1 proof for every t <= 99/100, without asserting the exact endpoint.
    one={'schema':'disk-cover-witness-tree/v1','n':1,'root':'s',
         'root_box':make_root(1,F(99,100)),
         'nodes':{'s':{'type':'SPLIT','coordinate':0,'cut':'0','left':'l','right':'r'},
                  'l':{'type':'WITNESS','point':['1','0']},
                  'r':{'type':'WITNESS','point':['-1','0']}}}
    # Valid degenerate 100-center region; not a complete global n=100 tree.
    hundred={'schema':'disk-cover-witness-tree/v1','n':100,'root':'w',
             'root_box':[['-1/2','1/2'] for _ in range(200)]+[['0','1/5']],
             'nodes':{'w':{'type':'WITNESS','point':['1','0']}}}
    outside={'schema':'disk-cover-witness-tree/v1','n':1,'root':'o',
             'root_box':[['4/5','1'],['4/5','1'],['0','1']],
             'nodes':{'o':{'type':'OUTSIDE_CENTER_DISK','center':0}}}
    results=[verify(one),verify(hundred,False),verify(outside,False)]
    rejected=[]
    tests=[]
    def add(name,src,mutate,global_mode=True):
        z=copy.deepcopy(src);mutate(z);tests.append((name,z,global_mode))
    add('missing_child',one,lambda z:z['nodes'].pop('r'))
    add('shared_child',one,lambda z:z['nodes']['s'].__setitem__('right','l'))
    add('cycle',one,lambda z:z['nodes']['s'].__setitem__('left','s'))
    add('endpoint_split',one,lambda z:z['nodes']['s'].__setitem__('cut','1'))
    add('strict_endpoint_failure',one,lambda z:z['root_box'][-1].__setitem__(1,'1'))
    add('witness_outside_disk',one,lambda z:z['nodes']['l'].__setitem__('point',['2','0']))
    add('wrong_witness',one,lambda z:z['nodes']['l'].__setitem__('point',['-1','0']))
    add('unreachable_node',one,lambda z:z['nodes'].__setitem__('extra',{'type':'WITNESS','point':['0','0']}))
    add('restricted_box_global_upgrade',hundred,lambda z:None)
    add('hundred_full_domain_false_exclusion',hundred,lambda z:z.__setitem__('root_box',make_root(100,F(1,5))))
    add('negative_radius',one,lambda z:z['root_box'][-1].__setitem__(0,'-1'))
    add('invalid_outside_disk',outside,lambda z:z['root_box'].__setitem__(0,['0','1']),False)
    add('dimension_mismatch',one,lambda z:z['root_box'].pop(0))
    for name,z,g in tests:
        try:verify(z,g)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise RuntimeError('control accepted: '+name)
    return one,hundred,results,rejected

if __name__=='__main__':
    one,hundred,results,rejected=controls()
    op=ROOT/'verify/out/n100-global-witness-tree-interface.json'
    require(not op.exists(),'refuse overwrite')
    output={'schema':'n100-global-witness-interface-test/v1','verified':True,
            'arithmetic':'integer and Fraction only','examples':[one,hundred],
            'results':results,'rejected_controls':rejected,
            'n100_complete_tree_supplied':False,'n100_global_optimality':False,
            'minimal_polynomial_obtained':False,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    op.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('PASS full n=1 tree, restricted n=100 box, outside-disk leaf;',len(rejected),'negative controls rejected; no n=100 global tree')
