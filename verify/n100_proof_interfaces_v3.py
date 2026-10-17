"""Third batch: automatic Hall discovery and dependency-bound LOCAL leaves."""
from fractions import Fraction as F
import copy
import n100_proof_interfaces_v2 as previous
import n100_hall_automatic_search as automatic
import n100_hybrid_local_tree as local
base=previous.base
METHODS=copy.deepcopy(previous.METHODS)
METHODS.update({
 'automatic_hall':{'input':'center_box','radius_units':'squared','resource':'finite_witness_assignment','additive':False,'review':'callable','checker':'n100_hall_automatic_search.independent or matching_replay','independence':'excluded subset clamped-distance replay; nonexcluded supplied-pool matching explicitly checked'},
 'local_root_box':{'input':'center_box','radius_units':'squared','resource':'certified_local_neighborhood','additive':False,'review':'callable','checker':'dependency-bound local context plus four-corner independent inclusion','independence':'inclusion and relabel/rotation checked independently; upstream local theorem/analytic bridges inherited'},
})

def matching_replay(box,points,result):
 P=[tuple(map(F,p)) for p in points];n=(len(box)-1)//2;t=F(box[-1][1]);pairs=result['matching'];base.require(sorted(i for i,j in pairs)==list(range(len(P))),'matching must saturate pool');base.require(len({j for i,j in pairs})==len(pairs),'matching repeated center')
 for i,j in pairs:
  base.require(type(i) is int and type(j) is int and 0<=j<n,'matching indices');p=P[i];nearest=[min(max(p[d],F(box[2*j+d][0])),F(box[2*j+d][1])) for d in (0,1)];base.require(sum((p[d]-nearest[d])**2 for d in (0,1))<=t,'matching edge absent')
 return {'verified':True,'saturated_pool':len(P),'claim':'no_Hall_deficiency_for_this_pool_only'}

def local_replay(box,node,ctx):
 x,rho,eps,binding=ctx;base.require(len(box)==201 and node['binding']==binding,'LOCAL dimension/binding');perm=node['permutation'];base.require(len(perm)==100 and all(type(v) is int for v in perm) and sorted(perm)==list(range(100)),'LOCAL labels');a,b=map(F,node['rotation']);base.require(a*a+b*b==1,'rational unit rotation')
 for j,k in enumerate(perm):
  us=tuple(map(F,box[2*k]));vs=tuple(map(F,box[2*k+1]))
  for u in us:
   for v in vs:
    base.require(abs(a*u-b*v-x[2*j])+rho<=eps and abs(b*u+a*v-x[2*j+1])+rho<=eps,'four-corner root inclusion')
 lo,hi=map(F,box[-1]);base.require(0<=lo<=hi<x[492]-rho,'strict local radius');return {'verified':True,'corner_checks':400,'center_count':100,'bindings':binding,'claim':'specified_box_below_certified_root_only'}

def run_leaf(method,payload):
 if method not in ('automatic_hall','local_root_box'):return previous.run_leaf(method,payload)
 try:
  base.exact_data(payload);base.require(payload.get('target')=='closed_unit_disk' and payload.get('radius_units')=='squared','target/radius semantics');box=base.canonical_box(payload['box']);proof_input={'target':'closed_unit_disk','radius_units':'squared','box':box};result={'method':method,'domain_type':'center_box','domain_fingerprint':base.fingerprint(box),'radius_units':'squared','squared_radius_upper':box[-1][1],'n':(len(box)-1)//2,'scope':'specified_box_only','global_optimality':False}
  if method=='automatic_hall':
   points=payload['points'];base.require(isinstance(points,list) and bool(points),'nonempty witness pool');proof_input['points']=points;certificate=automatic.find(box,points)
   if certificate['excluded']:replay=automatic.independent(box,certificate['points'])
   else:replay=matching_replay(box,points,certificate)
   result.update(status='EXCLUDED' if certificate['excluded'] else 'NOT_EXCLUDED',certificate=certificate,independent_replay=replay)
  else:
   node=payload['local_node'];proof_input['local_node']=node;ctx=local.context();local.local([tuple(map(F,p)) for p in box],node,ctx);replay=local_replay(box,node,ctx);result.update(status='EXCLUDED',certificate={'local_binding':ctx[3],'strict_squared_radius_upper':str(ctx[0][492]-ctx[1]),'center_radius':str(ctx[2]),'rotation':node['rotation'],'permutation':node['permutation']},independent_replay=replay)
  result['proof_input']=proof_input;return result
 except (ValueError,KeyError,TypeError,ZeroDivisionError,AssertionError) as e:return {'status':'PRECONDITION_MISSING','reason':str(e),'global_optimality':False}

def intersect_leaf_results(results):
 base.require(bool(results),'empty results');first=results[0]
 for r in results:
  base.require('proof_input' in r and 'method' in r,'missing replay input');base.require(run_leaf(r['method'],r['proof_input'])==r,'leaf replay mismatch');base.require(r.get('status') in base.STATUSES and 'domain_fingerprint' in r,'missing result domain');base.require(all(r.get(k)==first.get(k) for k in ('domain_type','domain_fingerprint','radius_units','n')),'different domains')
 status='EXCLUDED' if any(r['status']=='EXCLUDED' for r in results) else ('PRECONDITION_MISSING' if any(r['status']=='PRECONDITION_MISSING' for r in results) else ('UNDECIDED' if any(r['status']=='UNDECIDED' for r in results) else 'NOT_EXCLUDED'))
 return {'status':status,'domain_fingerprint':first['domain_fingerprint'],'scope':'specified_box_only','rule':'intersection_of_necessary_conditions','global_optimality':False}

def validate_plan(nodes,mode='INTERSECT'):
 base.require(mode in ('INTERSECT','SEQUENCE','ADD_BOUNDS') and bool(nodes),'plan mode/size');seen=set();context=None
 for node in nodes:
  base.require(node['id'] not in seen and node['method'] in METHODS,'unknown/duplicate node');m=METHODS[node['method']];c=node['context'];base.exact_data(c);base.require(c['domain_type']==m['input'] and c['radius_units']==m['radius_units'],'input type');base.require(node.get('premises_satisfied') is True,'unresolved premises');base.require(all(p in seen for p in node.get('depends_on',[])),'dependency order');key=tuple(c.get(k) for k in ('domain_type','instance_id','representation_id','normalization_id','radius_units','radius_domain_id'));base.require(all(key),'missing context binding')
  if context is None:context=key
  base.require(key==context,'explicit adapter required');base.require(mode!='ADD_BOUNDS' or m['additive'],'no additive budget certificate');seen.add(node['id'])
 return {'structurally_valid':True,'mode':mode,'method_ids':[n['method'] for n in nodes],'scope':'planning_only; no arithmetic or analytic premise verification','mathematical_verdict':None,'global_optimality':False}
