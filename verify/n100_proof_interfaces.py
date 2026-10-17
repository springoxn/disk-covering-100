"""Typed proof plumbing for reviewed n100 leaves; structural planning is not proof.

Only integer/rational data reach geometric acceptance. Float telemetry belongs
outside this module. Unreviewed methods and implicit representation changes fail.
"""
from fractions import Fraction as F
import hashlib,json
import n100_separated_witness_hall as hall
import n100_nonseparated_capacity_cut as capacity

STATUSES={'EXCLUDED','NOT_EXCLUDED','UNDECIDED','PRECONDITION_MISSING'}
METHODS={
 'separated_hall':{'input':'center_box','radius_units':'squared','resource':'finite_witness_assignment','additive':False,'review':'callable','checker':'n100_separated_witness_hall.verify','independence':'example-only independent bounds in legacy certificate'},
 'small_pool_capacity':{'input':'center_box','radius_units':'squared','resource':'finite_witness_assignment','additive':False,'review':'callable','checker':'n100_nonseparated_capacity_cut.independent_capacity','independence':'all excluded leaf capacities independently replayed'},
 'hybrid_capacity_tree':{'input':'split_tree','radius_units':'squared','resource':'domain_cover','additive':False,'review':'contract_only','checker':'n100_hybrid_capacity_tree.verify','independence':'inherits leaf checks; root and split coverage must also pass'},
 'recursive_count':{'input':'count_domain','radius_units':'radius','resource':'inner_disk_area','additive':False,'review':'contract_only','checker':'n100_recursive_joint_area_independent.main','independence':'saved full finite domain; geometry inherited'},
 'radius_local_joint':{'input':'count_domain','radius_units':'radius','resource':'triangle_anchor_boundary_area','additive':False,'review':'contract_only','checker':'n100_radius_local_joint_domain_independent.main','independence':'all saved families and triples; geometry inherited'},
 'ear_marked_joint':{'input':'boundary_word','radius_units':'radius','resource':'triangle_anchor_boundary_area','additive':False,'review':'contract_only','checker':'n100_ear_marked_joint_cuts_independent.main','independence':'saved ear-count scalar cases; geometry inherited'},
 'ear_representative':{'input':'boundary_word','radius_units':'radius','resource':'triangle_anchor_boundary_area','additive':False,'review':'contract_only','checker':'n100_m99_boundary_representatives_independent.main','independence':'all saved representatives and scalar cases; geometry inherited'},
}

def require(ok,msg):
 if not ok:raise ValueError(msg)
def exact_data(x):
 if isinstance(x,float):raise ValueError('floating-point proof datum')
 if isinstance(x,dict):
  for v in x.values():exact_data(v)
 elif isinstance(x,(list,tuple)):
  for v in x:exact_data(v)
def canonical_box(raw):
 require(isinstance(raw,list) and len(raw)>=3 and len(raw)%2==1,'box dimension');box=[]
 for pair in raw:
  require(len(pair)==2,'interval dimension');a,b=map(F,pair);require(a<=b,'interval orientation');box.append([str(a),str(b)])
 require(F(box[-1][0])>=0,'negative squared radius');return box
def fingerprint(box):return hashlib.sha256(json.dumps(box,separators=(',',':')).encode()).hexdigest()
def run_leaf(method,payload):
 """Return a same-box necessary exclusion; never upgrade to a global result."""
 try:
  exact_data(payload);require(method in ('separated_hall','small_pool_capacity'),'unreviewed callable');require(payload.get('radius_units')=='squared','squared radius required');require(payload.get('target')=='closed_unit_disk','target required');box=canonical_box(payload['box']);points=payload['points']
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:return {'status':'PRECONDITION_MISSING','reason':str(e),'global_optimality':False}
 result={'proof_input':{'target':'closed_unit_disk','radius_units':'squared','box':box,'points':points},'method':method,'domain_type':'center_box','domain_fingerprint':fingerprint(box),'radius_units':'squared','squared_radius_upper':box[-1][1],'n':(len(box)-1)//2,'scope':'specified_box_only','global_optimality':False}
 try:
  if method=='separated_hall':
   try:certificate=hall.verify(box,points)
   except ValueError as e:
    if str(e)=='Hall deficiency absent':result.update(status='NOT_EXCLUDED',certificate=None);return result
    raise
   result.update(status='EXCLUDED',certificate=certificate,independent_replay='not_generalized_by_this_adapter')
  else:
   certificate=capacity.cut(box,points)
   if certificate['excluded']:
    capacity.independent_capacity(box,points,certificate)
    result.update(status='EXCLUDED',certificate=certificate,independent_replay='Gram_and_clamped_distance')
   else:result.update(status='NOT_EXCLUDED',certificate=certificate)
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:result.update(status='PRECONDITION_MISSING',reason=str(e))
 return result

def intersect_leaf_results(results):
 """AND necessary constraints on exactly the same inherited box; no addition."""
 require(bool(results),'empty results');require(all(r.get('status') in STATUSES for r in results),'result status');require(all('domain_fingerprint' in r for r in results),'missing domain binding');first=results[0]
 for r in results:
  require('proof_input' in r and 'method' in r,'missing replay input')
  replay=run_leaf(r['method'],r['proof_input'])
  require(replay==r,'leaf result replay mismatch')
  require((r['domain_type'],r['domain_fingerprint'],r['radius_units'],r['n'])==(first['domain_type'],first['domain_fingerprint'],first['radius_units'],first['n']),'different proof domains')
 status='EXCLUDED' if any(r['status']=='EXCLUDED' for r in results) else ('PRECONDITION_MISSING' if any(r['status']=='PRECONDITION_MISSING' for r in results) else ('UNDECIDED' if any(r['status']=='UNDECIDED' for r in results) else 'NOT_EXCLUDED'))
 return {'status':status,'domain_fingerprint':first['domain_fingerprint'],'scope':'specified_box_only','rule':'intersection_of_necessary_conditions','global_optimality':False}

def validate_plan(nodes,mode='INTERSECT'):
 """Check wiring only. A valid plan has no mathematical verdict by itself."""
 require(mode in ('INTERSECT','SEQUENCE','ADD_BOUNDS'),'composition mode');require(bool(nodes),'empty plan');seen={};resources=set();bindings=None
 for node in nodes:
  require(node['id'] not in seen,'duplicate node');require(node['method'] in METHODS,'unknown/unreviewed method');m=METHODS[node['method']];ctx=node['context'];exact_data(ctx)
  require(ctx['domain_type']==m['input'] and ctx['radius_units']==m['radius_units'],'type/radius mismatch');require(ctx.get('instance_id') and ctx.get('representation_id') and ctx.get('normalization_id') and ctx.get('radius_domain_id'),'missing context binding')
  require(node.get('premises_satisfied') is True,'unresolved premises');require(all(p in seen for p in node.get('depends_on',[])),'missing/forward/cyclic dependency')
  key=tuple(ctx[k] for k in ('domain_type','instance_id','representation_id','normalization_id','radius_units','radius_domain_id'))
  if bindings is None:bindings=key
  require(key==bindings,'explicit verified adapter required between domains')
  if mode=='ADD_BOUNDS':
   require(m['additive'],'method has no additive budget certificate');require(m['resource'] not in resources,'duplicate area/witness budget')
  resources.add(m['resource']);seen[node['id']]=node
 return {'structurally_valid':True,'method_ids':[n['method'] for n in nodes],'mode':mode,'scope':'planning_only; premises flag is not a verified certificate','mathematical_verdict':None,'global_optimality':False}
