"""Fixed-radius arc/cap, arc/lens and radial-profile proof adapters.

All positive area/arc surplus verdicts are relaxation survival, never covers.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,hashlib
from n100_arc_cap_independent import audit as cap_audit
from n100_proof_interfaces import exact_data,require
R=Path(__file__).resolve().parents[1]
U=F(1154469548855829,10**16)
SEM='norm-cap-circle-serving-count/v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read_bound(name,bindings):
 p=R/'verify/out'/name;z=json.loads(p.read_text(encoding='utf-8'));bindings[str(p.relative_to(R)).replace('\\','/')]=sha(p);sp=R/'verify'/(p.stem.replace('-','_')+'.py');require(sp.exists() and sha(sp)==z['script_sha256'],'primary source hash');bindings[str(sp.relative_to(R)).replace('\\','/')]=sha(sp);return z

def pi_check(pl,ph):
 def atan(q,n):return sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(n)),F(0))
 require(pl<16*atan(5,10)-4*atan(239,9) and ph>16*atan(5,9)-4*atan(239,10),'Machin pi bounds')

def audit_lens(z):
 r=F(z['radius']);delta=F(z['delta']);a=F(z['slope']);M=F(z['maximum_half_arc_upper']);c=r/M;s=1-2*r+delta;N=z['radial_interval_count'];n=z['slabs_per_lens'];require(r==U and 0<c and c*c<=1-r*r and 0<delta<r,'lens parameters');require(len(z['steps'])==N,'radial coverage');last=F(0);checked=0
 for row in z['steps']:
  lo,hi=F(row['u_lower']),F(row['u_upper']);require(lo==last and hi-lo==delta/N,'radial partition');last=hi;d=1-r+hi;cos=(1-r*r+d*d)/(2*d);p=F(row['arc_half_upper']);require(d*d<1-r*r and 0<cos<=1 and p>=0 and p*p*c*c>=1-cos*cos,'arc upper');depth=delta-lo;left=1-2*r+lo;require(len(row['slab_heights_upper'])==n,'slabs');area=F(0)
  for i,raw in enumerate(row['slab_heights_upper']):
   x=depth*i/n;y=depth*(i+1)/n;rad=min(r*r-(r-y)**2,s*s-(left+x)**2);h=F(raw);require(rad>=0 and h>0 and h*h>=4*rad,'squared height');area+=depth*h/n;checked+=1
  require(area==F(row['lens_area_upper']) and a*(M-p)>=area,'lens support')
 require(last==delta,'tail');pl,ph=map(F,z['pi_interval']);pi_check(pl,ph);require(ph*r*r>a*M,'count monotonicity');margin=pl*s*s-46*ph*r*r-a*(54*M-pl);require(margin==F(z['k54_margin']) and (margin>0)==z['k54_excluded'],'k54 verdict');return {'slabs':checked,'intervals':N,'k54_excluded':margin>0}

def audit_profiles(z,M):
 r=F(z['radius']);pl,ph=map(F,z['pi_interval']);require(r==U,'profile radius');pi_check(pl,ph);types={t['kind']:t for t in z['types']};require(set(types)=={'near','tail'},'radial types');c=r/M;require(c>0 and c*c<=1-r*r,'arc c bound');checked=0;profiles=[]
 for ty in types.values():
  d=F(ty['distance']);cos=(1-r*r+d*d)/(2*d);sin2=1-cos*cos;require(0<cos<1,'service-circle arc');S=10**24;lo,hi=0,S
  while hi-lo>1:
   mid=(lo+hi)//2
   if mid*mid*sin2.denominator<=sin2.numerator*S*S:lo=mid
   else:hi=mid
  x=F(lo,S);lower=sum((F(comb(2*j,j),4**j*(2*j+1))*x**(2*j+1) for j in range(8)),F(0));upper=F(ty['half_arc_upper']);require(lower==F(ty['half_arc_lower']) and upper>0 and upper*upper*c*c>=sin2,'independent arc bounds')
 require([F(p['target_radius']) for p in z['profiles']]==[F(j,100) for j in range(1,101)],'100 target radii')
 for p in z['profiles']:
  t=F(p['target_radius']);parts={}
  for part in p['parts']:
   d=F(types[part['type']]['distance']);left=max(-t,d-r);right=min(t,d+r);rows=part['slabs'];L=V=F(0)
   if left>=right:require(not rows,'empty lens')
   else:
    require(len(rows)==512,'profile slab count')
    for j,row in enumerate(rows):
     a,b,l,h=map(F,row);require(a==left+(right-left)*j/512 and b==left+(right-left)*(j+1)/512,'profile partition');v0=[t*t-a*a,t*t-b*b];v1=[r*r-(a-d)**2,r*r-(b-d)**2];low=max(F(0),min(v0+v1));max0=t*t if a<=0<=b else max(v0);max1=r*r if a<=d<=b else max(v1);high=max(F(0),min(max0,max1));require(0<=l<=h and l*l<=4*low and h*h>=4*high,'profile heights');L+=(b-a)*l;V+=(b-a)*h;checked+=1
   require(L==F(part['lower']) and V==F(part['upper']),'profile integral');parts[part['type']]=(L,V)
  require(set(parts)==set(types),'all radial parts');profiles.append((t,parts))
 return types,profiles,checked

def build_context():
 bindings={};cap=read_bound('n100-arc-cap-rational-support.json',bindings);lens=read_bound('n100-arc-lens-support.json',bindings);radial=read_bound('n100-multiradius-capacity.json',bindings);require(F(cap['radius'])==U,'cap radius');require(lens['input_sha256']==bindings['verify/out/n100-arc-cap-rational-support.json'] and radial['input_sha256']==bindings['verify/out/n100-arc-lens-support.json'],'input chain');a=cap_audit(cap);b=audit_lens(lens);types,profiles,strips=audit_profiles(radial,F(lens['maximum_half_arc_upper']));return {'cap':cap,'lens':lens,'types':types,'profiles':profiles,'bindings':bindings,'replay_counts':{'cap_segments':a['segments'],'lens_slabs':b['slabs'],'profile_slabs':strips,'target_radii':len(profiles)},'inherited_premises':['norm-cap whole-cover normalization with services counted anew at this exact radius','short-arc formula and monotonicity; sum half arcs >= pi','cap integral inequality and lens Darboux enclosure','area subadditivity; sums count multiplicity and do not certify union coverage','positive arcsin series lower bound']}

def apply(method,payload,ctx):
 try:
  exact_data(payload);require(method in ('arc_cap','arc_lens','radial_profiles'),'method');require(payload.get('radius_units')=='radius' and F(payload['radius'])==U,'fixed exact radius U required; no implicit uniform transfer');require(payload.get('configuration_id') and payload.get('semantics_id')==SEM,'configuration/norm-cap semantics');proof_input=dict(payload)
  if method in ('arc_cap','arc_lens'):
   m,k=payload['m'],payload['k'];require(type(m) is int and type(k) is int and 0<=k<=m<=100,'distinct service counts');z=ctx['cap' if method=='arc_cap' else 'lens'];delta=F(z['delta']);a=F(z['slope']);M=F(z['maximum_half_arc_upper']);pl,ph=F(314159,100000),F(314160,100000);margin=pl*(1-2*U+delta)**2-(m-k)*ph*U*U-a*(k*M-pl);status='EXCLUDED' if margin>0 else 'NOT_EXCLUDED';detail={'area_deficit_lower':str(margin),'m':m,'k':k,'slope':str(a),'delta':str(delta)}
  else:
   counts=payload['counts'];require(set(counts)=={'near','tail','central'} and all(type(v) is int and v>=0 for v in counts.values()) and sum(counts.values())==100,'integer radial multiplicities');pl,ph=F(314159,100000),F(314160,100000);arcL=sum((counts[name]*F(ty['half_arc_lower']) for name,ty in ctx['types'].items()),F(0));arcU=sum((counts[name]*F(ty['half_arc_upper']) for name,ty in ctx['types'].items()),F(0));rows=[]
   for t,parts in ctx['profiles']:
    lo=counts['central']*pl*min(t,U)**2+sum((counts[name]*part[0] for name,part in parts.items()),F(0));hi=counts['central']*ph*min(t,U)**2+sum((counts[name]*part[1] for name,part in parts.items()),F(0));verdict='EXCLUDED' if hi<pl*t*t else ('NOT_EXCLUDED' if lo>=ph*t*t else 'UNDECIDED');rows.append({'target_radius':str(t),'verdict':verdict,'area_deficit_lower':str(pl*t*t-hi),'capacity_surplus_lower':str(lo-ph*t*t)})
   status='EXCLUDED' if arcU<pl or any(p['verdict']=='EXCLUDED' for p in rows) else ('NOT_EXCLUDED' if arcL>=ph and all(p['verdict']=='NOT_EXCLUDED' for p in rows) else 'UNDECIDED');detail={'arc_sum_lower':str(arcL),'arc_sum_upper':str(arcU),'target_rows':rows,'capacity_satisfied_is_cover':False}
  return {'status':status,'method':method,'proof_input':proof_input,'scope':'fixed_radius_necessary_budget_only','detail':detail,'budget_resource':'circle_arcs_and_inner_target_area','additive_with_other_area_bounds':False,'bindings':ctx['bindings'],'inherited_premises':ctx['inherited_premises'],'global_optimality':False}
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:return {'status':'PRECONDITION_MISSING','reason':str(e),'global_optimality':False}

def run_batch(requests):
 ctx=build_context();return [apply(method,payload,ctx) for method,payload in requests],{'replay_counts':ctx['replay_counts'],'bindings':ctx['bindings']}
