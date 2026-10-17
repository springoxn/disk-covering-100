"""Composable exact contractors on closed REAL boxes with integer outward bounds.

Verdicts refer to the declared constraint system. Fixed-core compiler supplies
conditional geometric premises; arbitrary user equations do not authorize cover cuts.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib,copy
import n100_axis_coupled_boxes as distance
from n100_axis_coupled_boxes_independent import clip
import n100_boundary_circle_propagation as circle
import n100_voronoi_bisector_vertex as bisector
import n100_voronoi_nearest_sites as nearest
from n100_proof_interfaces import require,exact_data
R=Path(__file__).resolve().parents[1]
Q=distance.Q

def interval_add(a,b):return a[0]+b[0],a[1]+b[1]
def interval_mul(a,b):
 values=[x*y for x in a for y in b];return min(values),max(values)
def independent_bisector(v,a,b):
 c=[];T=(0,0)
 for k in (0,1):
  A=a[2*k:2*k+2];B=b[2*k:2*k+2];c.append((2*(B[0]-A[1]),2*(B[1]-A[0])))
  def sq(z):return (0 if z[0]<=0<=z[1] else min(z[0]**2,z[1]**2),max(z[0]**2,z[1]**2))
  x,y=sq(A),sq(B);T=interval_add(T,(x[0]-y[1],x[1]-y[0]))
 residual=interval_add(T,interval_add(interval_mul(c[0],v[:2]),interval_mul(c[1],v[2:])));
 if not residual[0]<=0<=residual[1]:return None
 out=list(v)
 for k in (0,1):
  if c[k][0]<=0<=c[k][1]:continue
  other=1-k;rest=interval_add(T,interval_mul(c[other],out[2*other:2*other+2]));ratios=[F(-t,d) for t in rest for d in c[k]];lo,hi=min(ratios),max(ratios);out[2*k]=max(out[2*k],lo.numerator//lo.denominator);out[2*k+1]=min(out[2*k+1],-((-hi.numerator)//hi.denominator))
  if out[2*k]>out[2*k+1]:return None
 return out

def norm_bounds(box,alternative=False):
 if alternative:
  corners=list(product(box[:2],box[2:]));high=max(x*x+y*y for x,y in corners);near=[min(max(0,box[2*k]),box[2*k+1]) for k in (0,1)];return sum(x*x for x in near),high
 low=sum(0 if box[2*k]<=0<=box[2*k+1] else min(box[2*k]**2,box[2*k+1]**2) for k in (0,1));high=sum(max(box[2*k]**2,box[2*k+1]**2) for k in (0,1));return low,high

def step(boxes,c,alternative=False):
 op=c['op'];v=c['v'];box=boxes[v]
 if op=='distance_le':
  require(type(c['radius2']) is int and c['radius2']>=0,'distance radius2');return (clip if alternative else distance.contract)(box,boxes[c['b']],c['radius2'])
 if op=='circle_eq':
  signs=c['signs'];require(len(signs)==2 and all(type(s) is int and s in (-1,1) for s in signs),'quadrant signs');return circle.circle(box,signs,alternative)
 if op=='bisector_eq':return independent_bisector(box,boxes[c['a']],boxes[c['b']]) if alternative else bisector.bisect_vertex(box,boxes[c['a']],boxes[c['b']])
 if op=='nearest_le':return nearest.leq_vertex(box,boxes[c['a']],boxes[c['b']],alternative)
 if op=='norm_range':
  lo,hi=F(c['lower2']),F(c['upper2']);require(0<=lo<=hi,'norm range');a,b=norm_bounds(box,alternative);return None if b<lo or a>hi else list(box)
 raise ValueError('unknown contractor')

def run(payload):
 try:
  exact_data(payload);ctx=payload['context'];require(ctx.get('semantics_id')=='scaled-real-map-boxes/v1' and ctx.get('scale')==Q,'real box scale semantics');require(all(isinstance(ctx.get(k),str) and ctx[k] for k in ('map_id','frame_id','parent_box_id','radius_domain_id')),'map/frame/parent binding');boxes=copy.deepcopy(payload['boxes']);require(bool(boxes) and all(len(b)==4 and all(type(v) is int for v in b) and b[0]<=b[1] and b[2]<=b[3] for b in boxes),'integer outward boxes');constraints=payload['constraints'];limit=payload['sweep_limit'];require(type(limit) is int and limit>0,'positive sweep limit')
  for c in constraints:
   require(c.get('map_id')==ctx['map_id'],'constraint map binding')
   for k in ('v','a','b'):
    if k in c:require(type(c[k]) is int and 0<=c[k]<len(boxes),'variable index')
  trace=[];tests=0;failure=None;fixed=False
  for sweep in range(limit):
   changed=0
   for i,c in enumerate(constraints):
    new=step(boxes,c);ind=step(boxes,c,True);require(new==ind,'alternate contractor mismatch');tests+=1
    if new is None:failure={'constraint_index':i,'constraint':c,'input_boxes':[boxes[c[k]] for k in ('v','a','b') if k in c]};break
    old=boxes[c['v']];require(old[0]<=new[0]<=new[1]<=old[1] and old[2]<=new[2]<=new[3]<=old[3],'not a contraction')
    if old!=new:boxes[c['v']]=new;changed+=1
   trace.append(changed)
   if failure:break
   if not changed:fixed=True;break
  return {'status':'EXCLUDED' if failure else ('NOT_EXCLUDED' if fixed else 'UNDECIDED'),'proof_input':payload,'boxes':boxes,'failure':failure,'fixed_point':fixed,'sweeps':sweep+1,'primitive_tests':tests,'trace':trace,'context':ctx,'scope':'declared_constraint_system_only; geometric necessity inherited separately','covering_exclusion_authorized_without_bridge':False,'global_optimality':False,'independent_replay_scope':'distance and bisector separate implementations; norm corner/clamp; nearest/circle alternate arithmetic shares formulas'}
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:return {'status':'PRECONDITION_MISSING','reason':str(e),'global_optimality':False}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compile_fixed_core(placement,nearest_all=False,sweep_limit=1):
 cp=R/'verify/out/n100-cubic-core-roundtrip.json';bp=R/'verify/out/n100-axis-coupled-boxes.json';core=json.loads(cp.read_text(encoding='utf-8'))['core'];prior=json.loads(bp.read_text(encoding='utf-8'));require(prior['script_sha256']==sha(R/'verify/n100_axis_coupled_boxes.py'),'parent source binding')
 for path,h in prior['bindings'].items():require(sha(R/path)==h,'parent dependency binding')
 row=next(r for r in prior['retained'] if r['placement']==placement);boxes,edges,quads=circle.setup(core,placement,row['boxes']);mapid=sha(cp);ctx={'semantics_id':'scaled-real-map-boxes/v1','scale':Q,'map_id':mapid,'frame_id':'ordered-fixed-unit-axes','radius_domain_id':'r<=1154469548855829/10000000000000000','parent_box_id':sha(bp)+':'+','.join(map(str,placement))};ops=[]
 for v,signs in sorted(quads.items()):ops.append({'op':'circle_eq','v':100+v,'signs':list(signs)})
 for a,b in edges:
  for v,w in ((a,b),(b,a)):ops.append({'op':'distance_le','v':v,'b':w,'radius2':distance.radiussquared(1)})
 for v,a,b in bisector.equations(edges):ops.append({'op':'bisector_eq','v':v,'a':a,'b':b})
 if nearest_all:
  owners={}
  for a,v in edges:owners.setdefault(v,set()).add(a)
  for v,sites in sorted(owners.items()):
   for b in range(100):
    if b not in sites:ops.append({'op':'nearest_le','v':v,'a':min(sites),'b':b})
 for c in ops:c['map_id']=mapid
 return {'context':ctx,'boxes':boxes,'constraints':ops,'sweep_limit':sweep_limit},{'geometry_bridge':'inherited fixed Voronoi core; distinct labelled sites and declared incidences/quadrants; no full map enumeration','bindings':{str(p.relative_to(R)).replace('\\','/'):sha(p) for p in [cp,bp,R/'verify/n100_boundary_circle_propagation.py']},'constraint_count':len(ops),'global_optimality':False}

def intersect_results(results):
 require(bool(results),'empty results');first=results[0]
 for r in results:
  require('proof_input' in r and run(r['proof_input'])==r,'contractor replay mismatch');require(r['context']==first['context'] and r['proof_input']['boxes']==first['proof_input']['boxes'],'different parent/frame/map domain')
 if any(r['status']=='EXCLUDED' for r in results):return {'status':'EXCLUDED','scope':'declared_constraint_systems_on_same_parent_only','global_optimality':False}
 boxes=copy.deepcopy(first['proof_input']['boxes'])
 for r in results:
  for i,b in enumerate(r['boxes']):
   boxes[i]=[max(boxes[i][0],b[0]),min(boxes[i][1],b[1]),max(boxes[i][2],b[2]),min(boxes[i][3],b[3])]
   if boxes[i][0]>boxes[i][1] or boxes[i][2]>boxes[i][3]:return {'status':'EXCLUDED','scope':'same-parent necessary contractions have empty intersection','global_optimality':False}
 return {'status':'NOT_EXCLUDED','boxes':boxes,'scope':'joint necessary box; no feasibility claim','global_optimality':False}
