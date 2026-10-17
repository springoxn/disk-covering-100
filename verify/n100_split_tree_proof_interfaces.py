"""Complete closed-real-box split trees; unresolved leaves never prove exclusion."""
import copy
from n100_proof_interfaces import require,exact_data
import n100_continuous_proof_interfaces as C

def compact(result):return {k:v for k,v in result.items() if k!='proof_input'}
def generate(root,depth=3):
 require(type(depth) is int and depth>=0,'depth');nodes=[]
 def visit(payload,level):
  idx=len(nodes);nodes.append(None);r=C.run(payload);require(r['status']!='PRECONDITION_MISSING','invalid root/child');row={'replay':compact(r)}
  if r['status']=='EXCLUDED':row['kind']='excluded'
  else:
   choices=[(b[2*d+1]-b[2*d],v,d) for v,b in enumerate(r['boxes']) for d in (0,1)];width,v,d=max(choices)
   if level>=depth or width<2:row['kind']='unresolved'
   else:
    cut=(r['boxes'][v][2*d]+r['boxes'][v][2*d+1])//2;left=copy.deepcopy(payload);right=copy.deepcopy(payload);left['boxes']=copy.deepcopy(r['boxes']);right['boxes']=copy.deepcopy(r['boxes']);left['boxes'][v][2*d+1]=cut;right['boxes'][v][2*d]=cut;row.update(kind='split',variable=v,coordinate=d,cut=cut,children=[visit(left,level+1),visit(right,level+1)])
  nodes[idx]=row;return idx
 visit(copy.deepcopy(root),0);return {'schema':'n100-closed-real-split-tree/v1','root':root,'nodes':nodes,'global_optimality':False}

def verify(tree):
 exact_data(tree);require(tree.get('schema')=='n100-closed-real-split-tree/v1','tree schema');nodes=tree['nodes'];require(bool(nodes),'empty tree');seen=set();excluded=0;unresolved=0;calls=0
 def visit(idx,payload):
  nonlocal excluded,unresolved,calls
  require(type(idx) is int and 0<=idx<len(nodes) and idx not in seen,'tree cycle/reused/missing child');seen.add(idx);row=nodes[idx];r=C.run(payload);calls+=1;require(r['status']!='PRECONDITION_MISSING' and compact(r)==row['replay'],'leaf/propagation full replay');kind=row['kind']
  if kind=='excluded':require(r['status']=='EXCLUDED','false excluded leaf');excluded+=1;return
  require(r['status']!='EXCLUDED','nonexcluded node carries contradiction')
  if kind=='unresolved':unresolved+=1;return
  require(kind=='split','unknown node kind');v,d,cut=row['variable'],row['coordinate'],row['cut'];require(type(v) is int and 0<=v<len(r['boxes']) and type(d) is int and d in (0,1) and type(cut) is int,'split type');lo,hi=r['boxes'][v][2*d:2*d+2];require(lo<cut<hi and len(row['children'])==2,'closed partition progress');left=copy.deepcopy(payload);right=copy.deepcopy(payload);left['boxes']=copy.deepcopy(r['boxes']);right['boxes']=copy.deepcopy(r['boxes']);left['boxes'][v][2*d+1]=cut;right['boxes'][v][2*d]=cut
  for child,expected in zip(row['children'],(left,right)):visit(child,expected)
 visit(0,tree['root']);require(len(seen)==len(nodes),'unreachable extra nodes');return {'status':'EXCLUDED' if not unresolved else 'UNDECIDED','nodes_replayed':calls,'excluded_leaves':excluded,'unresolved_leaves':unresolved,'root_coverage':'closed intervals [lo,cut] union [cut,hi] exactly cover each contracted parent; true solutions retained by contraction','scope':'entire declared root constraint domain only; geometry bridge inherited separately','global_optimality':False}
