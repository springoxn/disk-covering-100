"""Count/ear proof-domain adapters: same normalized diagram, exact radius domains.

Replays outer finite scalar classifications and actual-ear finite tests. Inner
frontier and geometric lemmas remain explicitly inherited certificate premises.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib
from n100_recursive_joint_area_independent import rnd,atan,series,sqrtiv,need
from n100_proof_interfaces import exact_data
from n100_pruning_catalogue import WITHDRAWN
R=Path(__file__).resolve().parents[1]
SEMANTICS='normalized-distinct-boundary-cells/v1'
U=F(1154469548855829,10**16)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(rel,bindings):
 rel=rel.replace('\\','/');need(rel not in WITHDRAWN,'withdrawn proof input');p=(R/rel).resolve();need(p.is_relative_to(R),'outside project');z=json.loads(p.read_text(encoding='utf-8'));bindings[rel]=sha(p)
 if 'script_sha256' in z:
  name=p.stem.replace('-','_')+'.py';script=R/'verify'/name
  if script.exists():need(sha(script)==z['script_sha256'],'source binding changed');bindings[str(script.relative_to(R)).replace('\\','/')]=sha(script)
 for dep,h in z.get('bindings',{}).items():
  dp=(R/dep).resolve();need(dp.is_relative_to(R) and dep.replace('\\','/') not in WITHDRAWN,'invalid inherited dependency');need(sha(dp)==h,'inherited hash binding');bindings[dep.replace('\\','/')]=h
 return z

def build_context():
 bindings={};strata=load('verify/out/n100-radius-count-strata.json',bindings);outer=load('verify/out/n100-radius-local-joint-domain.json',bindings);prior=load('verify/out/n100-total-ear-face-cuts.json',bindings);ears=load('verify/out/n100-ear-marked-joint-cuts.json',bindings);angles=load('verify/out/n100-disjoint-ear-group-cuts.json',bindings)
 need(outer['source_sha256']==bindings['verify/out/n100-radius-count-strata.json'],'outer input binding');need(ears['input_sha256']==bindings['verify/out/n100-total-ear-face-cuts.json'],'ear input binding');pl,ph=rnd(16*atan(F(1,5),40)-4*atan(F(1,239),41),16*atan(F(1,5),41)-4*atan(F(1,239),40));al,ah=[3*x/4 for x in sqrtiv(F(3))];kap=F(461134488,10**9)
 @lru_cache(None)
 def trig(B):return (*rnd(series(pl/B)[0],series(ph/B)[1]),*rnd(series(ph/B,True)[0],series(pl/B,True)[1]))
 need(len(outer['layers'])==len(strata['layers'])==4,'four count layers');layers=[];checked=0
 for layer,src in zip(outer['layers'],strata['layers']):
  r=F(layer['radius_upper']);need(r==F(src['radius_upper']) and layer['minimum_nonserving']==src['minimum_nonserving'],'layer identity');old=set(map(tuple,src['triples']));families={t[:2] for t in old};need([(c['m'],c['B']) for c in layer['outer_family_rows']]==sorted(families),'complete family list');alive=set()
  for row in layer['outer_family_rows']:
   m,B=row['m'],row['B'];sl,sh,cl,ch=trig(B);checked+=1
   if sl>r:status='arc exclusion'
   else:
    need(sh<r,'arc interval overlap');coef=F(2*m-2,B)-1;low=(coef*al+kap)*r*r+sl*sqrtiv(r*r-sh*sh)[0]-sh*ch;high=(coef*ah+kap)*r*r+sh*sqrtiv(r*r-sl*sl)[1]-sl*cl
    if high<0:status='area exclusion'
    else:need(low>0,'undecided outer scalar');status='not excluded';alive.add((m,B))
   need(status==row['status'],'outer independent sign')
  new={t for t in old if t[:2] in alive};need(sorted(new)==list(map(tuple,layer['remaining_triples'])) and sorted(old-new)==list(map(tuple,layer['removed_triples'])),'outer full domain');need(len(new)==layer['remaining_triple_count'],'outer count');layers.append({'upper':r,'triples':new,'label':layer['label']})
 need(all(a['upper']<b['upper'] and a['triples']<=b['triples'] for a,b in zip(layers,layers[1:])) and layers[-1]['upper']==U,'nested count domains')
 r=F(ears['radius_upper_inclusive']);g=F(angles['three_arc_sum_upper']);arc=F(angles['individual_arc_upper']);A=F(3,4)*sqrtiv(F(3))[1];G1=sqrtiv((207+33*sqrtiv(F(33))[1])/128)[1];G2=sqrtiv(9+6*sqrtiv(F(3))[1])[1]/2;ear_rows={};ear_checks=0
 def H(a,b):
  sl=series(a/2)[0];sh=series(b/2)[1];need(0<sl<=sh<r,'ear square-root domain');return sh*sqrtiv(r*r-sl*sl)[1]+(b-series(a)[0])/2
 need(len(ears['family_rows'])==len(prior['family_rows'])==17,'all ear families')
 for c,pc in zip(ears['family_rows'],prior['family_rows']):
  m,B=c['m'],c['B'];need((m,B,c['prior_ear_upper'])==(pc['m'],pc['B'],pc['maximum_total_ear_faces']),'ear prior binding');need([t['ear_count'] for t in c['tests']]==list(range(c['prior_ear_upper']+1)),'all ear tests');kept=[]
  for t in c['tests']:
   e=t['ear_count'];q=(e-1)//2 if B%4==2 and e==B//2 else (e+1)//2;need(q==t['guaranteed_disjoint_groups'],'packing');k=B-3*q;cap=2*pl-q*g-k*arc;ear_checks+=1
   if t['status']=='excluded by arc capacity':need(cap>0,'ear capacity');continue
   need(cap<=0 and k>0,'ear remainder')
   if t['status']=='undecided domain':kept.append(e);continue
   hs=(3*q*H(g/3,g/3) if q else 0)+k*H((2*pl-q*g)/k,(2*ph-q*g)/k);gap=pl-((2*m-2*B-2+e)*A+(B-2*e)*G1+e*G2)*r*r-hs;need((gap>0)==t['status'].startswith('excluded'),'ear independent sign')
   if gap<=0:kept.append(e)
  need(kept==c['remaining_ear_counts'],'ear retained counts');ear_rows[m,B]={'prior_maximum':c['prior_ear_upper'],'remaining':set(kept)}
 return {'layers':layers,'ear_upper':r,'ear_rows':ear_rows,'bindings':bindings,'outer_scalar_cases':checked,'ear_scalar_cases':ear_checks,'inherited_premises':['certified inner frontier/recursive count strata','same-radius normalized single-arc boundary diagram','distinct B cells, distinct k circle-serving disks, B<=k<=m<=100','marked triangle geometry, arc concavity and ear-packing theorems']}

def fingerprint(payload):return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def apply_in_context(method,payload,ctx):
 try:
  exact_data(payload);need(method in ('radius_joint','ear_marked'),'method');need(payload.get('n')==100 and payload.get('semantics_id')==SEMANTICS,'n/diagram semantics');need(payload.get('configuration_id') and payload.get('radius_units')=='radius','configuration/radius type');r=F(payload['radius_upper']);need(0<r<=U,'radius outside certified domain');width=3 if method=='radius_joint' else 4;raw=payload['tuples'];need(isinstance(raw,list) and all(isinstance(t,list) and len(t)==width and all(type(v) is int for v in t) for t in raw),'typed tuples');tuples=sorted(set(map(tuple,raw)));need(all(1<=B<=k<=m<=100 for m,B,k,*rest in tuples),'B/k/m order')
  if width==4:need(all(0<=e<=B//2 and m>B for m,B,k,e in tuples),'actual-ear topology domain')
  canonical={'n':100,'semantics_id':SEMANTICS,'configuration_id':payload['configuration_id'],'radius_units':'radius','radius_upper':str(r),'tuples':[list(t) for t in tuples]};applicable=[l for l in ctx['layers'] if r<=l['upper']];layer=applicable[0];kept=[];removed=[];ear_applies=r<=ctx['ear_upper']
  for t in tuples:
   allowed=t[:3] in layer['triples']
   if width==4 and ear_applies and t[:2] in ctx['ear_rows']:allowed=allowed and t[3] in ctx['ear_rows'][t[:2]]['remaining']
   (kept if allowed else removed).append(list(t))
  return {'status':'EXCLUDED' if tuples and not kept else 'NOT_EXCLUDED','method':method,'domain_type':'count_domain' if width==3 else 'ear_decorated_count_domain','proof_input':canonical,'domain_fingerprint':fingerprint(canonical),'selected_radius_layer':layer['label'],'selected_layer_upper':str(layer['upper']),'ear_bound_applied':width==4 and ear_applies,'remaining':kept,'removed':removed,'scope':'necessary_domain_only; surviving labels are not covers','inherited_premises':ctx['inherited_premises'],'bindings':ctx['bindings'],'global_optimality':False}
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:return {'status':'PRECONDITION_MISSING','reason':str(e),'global_optimality':False}

def run_batch(requests):
 ctx=build_context();return [apply_in_context(method,payload,ctx) for method,payload in requests],{'outer_scalar_cases':ctx['outer_scalar_cases'],'ear_scalar_cases':ctx['ear_scalar_cases'],'bindings':ctx['bindings']}

def lift_to_ears(payload):
 exact_data(payload);need(payload.get('semantics_id')==SEMANTICS and payload.get('n')==100,'lift semantics');need(payload.get('configuration_id') and payload.get('radius_units')=='radius','lift configuration/radius');need(0<F(payload['radius_upper'])<=U,'lift radius');tuples=payload['tuples'];need(all(len(t)==3 and all(type(v) is int for v in t) and 1<=t[1]<=t[2]<=t[0]<=100 and t[0]>t[1] for t in tuples),'lift interior-vertex count domain');lifted=dict(payload);lifted['tuples']=[list(t)+[e] for t in sorted(set(map(tuple,tuples))) for e in range(t[1]//2+1)];return lifted,{'adapter':'count_to_actual_ear_decoration','parent_input_fingerprint':fingerprint(payload),'proof_premise':'nonadjacent ear tips with interior vertices imply e<=floor(B/2); all allowed e enumerated','preserves_configuration_and_radius':True,'global_optimality':False}
