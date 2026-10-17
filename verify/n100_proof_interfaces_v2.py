"""Second reviewed batch: box-energy union DP and weighted finite capacity.

Extends contracts without modifying the v1 modules or their certificate bindings.
"""
from fractions import Fraction as F
from itertools import combinations
import copy
import n100_proof_interfaces as base
import n100_box_aware_capacity as aware
import n100_weighted_witness_capacity as weighted

METHODS=copy.deepcopy(base.METHODS)
METHODS.update({
 'box_aware_patterns':{'input':'center_box','radius_units':'squared','resource':'finite_witness_assignment','additive':False,'review':'callable','checker':'n100_box_aware_capacity.independent','independence':'all retained pattern and union-DP decisions independently replayed'},
 'weighted_capacity':{'input':'center_box','radius_units':'squared','resource':'finite_witness_assignment','additive':False,'review':'callable','checker':'n100_proof_interfaces_v2.weighted_replay','independence':'arbitrary accepted input explicit-circle pair/triple patterns and clamped reach; not merely saved example'},
})

def d2(a,b):return sum((x-y)**2 for x,y in zip(a,b))
def explicit_mec(points):
 """Independent candidate-center enumeration, used only on 0..3 points."""
 if not points:return F(0)
 candidates=[(p,F(0)) for p in points]
 for a,b in combinations(points,2):
  c=tuple((x+y)/2 for x,y in zip(a,b));candidates.append((c,d2(c,a)))
 for a,b,c in combinations(points,3):
  u=(b[0]-a[0],b[1]-a[1]);v=(c[0]-a[0],c[1]-a[1]);D=2*(u[0]*v[1]-u[1]*v[0])
  if not D:continue
  L=d2(a,b);M=d2(a,c);center=(a[0]+(L*v[1]-M*u[1])/D,a[1]+(u[0]*M-v[0]*L)/D);candidates.append((center,d2(center,a)))
 radii=[r for c,r in candidates if all(d2(c,p)<=r for p in points)];base.require(bool(radii),'no enclosing candidate');return min(radii)

def weighted_replay(box,points,weights,certificate):
 P=[tuple(map(F,p)) for p in points];W=list(map(F,weights));k=len(P);t=F(box[-1][1]);forbidden=[]
 for size in (2,3):
  for ids in combinations(range(k),size):
   if explicit_mec([P[i] for i in ids])>t:forbidden.append(sum(1<<i for i in ids))
 masks=[s for s in range(1<<k) if not any(s&b==b for b in forbidden)];weights_by_mask={s:sum((W[i] for i in range(k) if s>>i&1),F(0)) for s in masks};caps=[]
 for j in range((len(box)-1)//2):
  reach=0
  for i,p in enumerate(P):
   c=[min(max(p[d],F(box[2*j+d][0])),F(box[2*j+d][1])) for d in (0,1)]
   if d2(c,p)<=t:reach|=1<<i
  caps.append(max(weights_by_mask[s] for s in masks if s&reach==s))
 total=sum(W,F(0));upper=sum(caps,F(0));base.require([str(v) for v in caps]==certificate['per_center_capacity_upper'],'independent weighted capacities');base.require(str(total)==certificate['total_weight'] and str(upper)==certificate['sum_capacity_upper'],'independent weighted totals');base.require((upper<total)==certificate['excluded'],'independent weighted decision');return {'verified':True,'explicit_small_MEC_checks':sum(1 for size in (2,3) for ids in combinations(range(k),size)),'admitted_masks':len(masks)}

def run_leaf(method,payload):
 if method in ('separated_hall','small_pool_capacity'):return base.run_leaf(method,payload)
 try:
  base.exact_data(payload);base.require(method in ('box_aware_patterns','weighted_capacity'),'unreviewed callable');base.require(payload.get('radius_units')=='squared' and payload.get('target')=='closed_unit_disk','target/radius type');box=base.canonical_box(payload['box']);points=payload['points'];base.require(isinstance(points,list),'point list')
  if method=='weighted_capacity':
   weights=payload['weights'];base.require(isinstance(weights,list) and len(weights)==len(points),'weight list');base.require(all(F(w)>=0 for w in weights),'negative weight')
  proof_input={'target':'closed_unit_disk','radius_units':'squared','box':box,'points':points}
  if method=='weighted_capacity':proof_input['weights']=weights
  result={'proof_input':proof_input,'method':method,'domain_type':'center_box','domain_fingerprint':base.fingerprint(box),'radius_units':'squared','squared_radius_upper':box[-1][1],'n':(len(box)-1)//2,'scope':'specified_box_only','global_optimality':False}
  if method=='box_aware_patterns':
   certificate=aware.search(box,points);ind=aware.independent(box,points,certificate)
  else:
   certificate=weighted.capacity(box,points,weights);ind=weighted_replay(box,points,weights,certificate)
  result.update(status='EXCLUDED' if certificate['excluded'] else 'NOT_EXCLUDED',certificate=certificate,independent_replay=ind);return result
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:return {'status':'PRECONDITION_MISSING','reason':str(e),'global_optimality':False}

def intersect_leaf_results(results):
 base.require(bool(results),'empty results');first=results[0]
 for r in results:
  base.require('proof_input' in r and 'method' in r,'missing replay input');base.require(run_leaf(r['method'],r['proof_input'])==r,'leaf replay mismatch')
  base.require(r.get('status') in base.STATUSES and 'domain_fingerprint' in r,'missing proof domain')
  base.require(all(r.get(k)==first.get(k) for k in ('domain_type','domain_fingerprint','radius_units','n')),'different proof domains')
 status='EXCLUDED' if any(r['status']=='EXCLUDED' for r in results) else ('PRECONDITION_MISSING' if any(r['status']=='PRECONDITION_MISSING' for r in results) else ('UNDECIDED' if any(r['status']=='UNDECIDED' for r in results) else 'NOT_EXCLUDED'))
 return {'status':status,'domain_fingerprint':first['domain_fingerprint'],'scope':'specified_box_only','rule':'intersection_of_necessary_conditions','global_optimality':False}

def validate_plan(nodes,mode='INTERSECT'):
 base.require(mode in ('INTERSECT','SEQUENCE','ADD_BOUNDS') and bool(nodes),'plan mode/size');seen=set();context=None
 for node in nodes:
  base.require(node['id'] not in seen and node['method'] in METHODS,'unknown/duplicate node');m=METHODS[node['method']];c=node['context'];base.exact_data(c);base.require(c['domain_type']==m['input'] and c['radius_units']==m['radius_units'],'input type');base.require(node.get('premises_satisfied') is True,'unresolved premises');base.require(all(p in seen for p in node.get('depends_on',[])),'dependency order')
  key=tuple(c.get(k) for k in ('domain_type','instance_id','representation_id','normalization_id','radius_units','radius_domain_id'));base.require(all(key),'missing context binding')
  if context is None:context=key
  base.require(key==context,'explicit adapter required');base.require(mode!='ADD_BOUNDS' or m['additive'],'no additive budget certificate');seen.add(node['id'])
 return {'structurally_valid':True,'mode':mode,'method_ids':[n['method'] for n in nodes],'scope':'planning_only; no arithmetic or analytic premise verification','mathematical_verdict':None,'global_optimality':False}
