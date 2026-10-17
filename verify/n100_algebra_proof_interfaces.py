"""Map-to-polynomial adapter and exact factored-SOS/ideal refutation checker."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
from n100_proof_interfaces import require,exact_data
from n100_generic_map_compiler import compile_model
from n100_face_axis_global_exclusion import strongest
R=Path(__file__).resolve().parents[1]

def fingerprint(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def clean(p):return {m:v for m,v in p.items() if v}
def parse(terms,n):
 out={}
 for coefficient,indices in terms:
  require(all(type(i) is int and 0<=i<n for i in indices),'polynomial variable index');c=F(coefficient);m=tuple(sorted(indices));out[m]=out.get(m,F(0))+c
 return clean(out)
def add(*polys):
 out={}
 for p in polys:
  for m,c in p.items():out[m]=out.get(m,F(0))+c
 return clean(out)
def scale(p,c):return clean({m:c*v for m,v in p.items()})
def multiply(a,b):
 out={}
 for m,c in a.items():
  for k,d in b.items():s=tuple(sorted(m+k));out[s]=out.get(s,F(0))+c*d
 return clean(out)
def substitute(p,values):
 out={}
 for mon,c in p.items():
  free=[]
  for i in mon:
   if i in values:c*=values[i]
   else:free.append(i)
  key=tuple(free);out[key]=out.get(key,F(0))+c
 return clean(out)
def sos(entries,n):
 result={}
 for e in entries:
  w=F(e['weight']);require(w>=0,'negative SOS weight');p=parse(e['poly'],n);result=add(result,scale(multiply(p,p),w))
 return result

def verify_refutation(model,proof):
 try:
  exact_data(model);exact_data(proof);n=model['variables'];require(type(n) is int and n>0 and type(model['t_index']) is int and 0<=model['t_index']<n,'model variables');require(proof['model_fingerprint']==fingerprint(model),'wrong polynomial model');require(proof['radius_units']=='squared','squared radius required');upper=F(proof['squared_radius_upper']);require(upper>=0,'squared radius domain');eq=[parse(c['terms'],n) for c in model['equalities']];iq=[parse(c['terms'],n) for c in model['inequalities']];iq.append({():upper,(model['t_index'],):F(-1)});values={}
  for raw,v in proof.get('fixed_variables',{}).items():
   require(type(raw) in (str,int) and str(raw)==str(int(raw)) and 0<=int(raw)<n,'fixed index');i=int(raw);v=F(v);require(any(set(p)<={(i,),()} and p.get((i,),0)!=0 and p.get((i,),0)*v+p.get((),0)==0 for p in eq),'substitution not justified by a model equality');values[i]=v
  eq=[substitute(p,values) for p in eq];iq=[substitute(p,values) for p in iq];rhs=sos(proof.get('free_sos',[]),n)
  for term in proof.get('inequality_multipliers',[]):
   i=term['index'];require(type(i) is int and 0<=i<len(iq),'inequality reference');rhs=add(rhs,multiply(sos(term['sos'],n),iq[i]))
  for term in proof.get('equality_multipliers',[]):
   i=term['index'];require(type(i) is int and 0<=i<len(eq),'equality reference');rhs=add(rhs,multiply(parse(term['poly'],n),eq[i]))
  require(rhs=={():F(-1)},'negative-one coefficient identity failed')
  return {'status':'EXCLUDED','model_fingerprint':fingerprint(model),'proof_input':proof,'scope':'entire declared polynomial domain at explicit squared-radius upper bound','identity':'-1 = SOS + sum(SOS_i*g_i) + sum(h_j*f_j), g_i>=0 and f_j=0','fixed_variables_verified':len(values),'global_optimality':False}
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:return {'status':'PRECONDITION_MISSING','reason':str(e),'global_optimality':False}

def compile_map(g):
 exact_data(g);names=set(g['vertices']);require(bool(names),'empty map');adj={v:set() for v in names}
 for e in g['edges']:
  a,b=e['ends'];require(a in names and b in names,'unknown edge endpoint');adj[a].add(b);adj[b].add(a)
 seen={next(iter(names))};todo=list(seen)
 while todo:
  for w in adj[todo.pop()]:
   if w not in seen:seen.add(w);todo.append(w)
 require(seen==names,'disconnected map');model=compile_model(g)
 return model,{'map_fingerprint':fingerprint(g),'model_fingerprint':fingerprint(model),'connected_checked':True,'variables':model['variables'],'scope':'one declared connected dart map; parallel edges retain explicit identities; no map enumeration completeness','global_optimality':False}

def two_axis_filter(g,squared_radius_upper):
 exact_data(squared_radius_upper);require(F(squared_radius_upper)>=0,'nonnegative exact squared radius');model,bridge=compile_map(g);c=strongest(g,model)
 if c is None:return {'status':'NOT_EXCLUDED','reason':'no face contains two fixed axis marks','map_bridge':bridge,'global_optimality':False}
 T=F(squared_radius_upper);gap=F(c['t_lower_bound'])-T
 if gap<=0:return {'status':'NOT_EXCLUDED','reason':'two-axis radius bound not strict at this endpoint','map_bridge':bridge,'global_optimality':False}
 proof={'model_fingerprint':fingerprint(model),'radius_units':'squared','squared_radius_upper':str(T),'fixed_variables':c['fixed_axis_substitution'],'free_sos':[{'weight':str(1/gap),'poly':[['1',[s['center_coordinate_index']]],[-F(s['offset']),[]]]} for s in c['square_terms']],'inequality_multipliers':[{'index':i,'sos':[{'weight':str(F(1,2)/gap),'poly':[['1',[]]]}]} for i in c['distance_constraint_indices']]+[{'index':len(model['inequalities']),'sos':[{'weight':str(1/gap),'poly':[['1',[]]]}]}],'equality_multipliers':[]}
 # JSON proof data must remain portable; convert all rational coefficients to text.
 for term in proof['free_sos']:
  for row in term['poly']:row[0]=str(row[0])
 result=verify_refutation(model,proof);require(result['status']=='EXCLUDED','generated refutation rejected');result['map_bridge']=bridge;return result
