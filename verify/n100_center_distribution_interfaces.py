"""Exact necessary area/distribution cuts for declared center domains.
Complements the fixed-radius saved-profile adapters with arbitrary rational targets.
"""
from fractions import Fraction as F
import hashlib,json
from n100_proof_interfaces import exact_data,require,canonical_box

def run(method,payload):
 try:
  exact_data(payload);r=F(payload['radius_upper']);require(r>0,'positive radius');require(payload.get('target')=='closed_unit_disk' and payload.get('radius_units')=='radius','type');p=json.loads(json.dumps(payload));possible=[]
  if method=='annular_norm_counts':
   a,b=map(F,p['annulus']);require(0<=a<b<=1,'annulus contained');bounds=[tuple(map(F,z)) for z in p['center_norm_bounds']];require(all(0<=lo<=hi for lo,hi in bounds) and 0<len(bounds)<=100,'radial bounds');lo=max(F(0),a-r);hi=b+r;possible=[i for i,(x,y) in enumerate(bounds) if x<=hi and y>=lo];area=b*b-a*a
  elif method=='translated_target_counts':
   q=tuple(map(F,p['target_center']));s=F(p['target_radius']);require(len(q)==2 and 0<s<=1 and sum(v*v for v in q)<=(1-s)**2,'target disk contained');boxes=[canonical_box([z[:2],z[2:],['0',str(r*r)]]) for z in p['center_boxes']];require(0<len(boxes)<=100,'centers');threshold=(s+r)**2
   for i,box in enumerate(boxes):
    d=sum((F(lo)-x)**2 if x<F(lo) else (x-F(hi))**2 if x>F(hi) else F(0) for x,(lo,hi) in zip(q,box[:2]))
    if d<=threshold:possible.append(i)
   area=s*s
  else:raise ValueError('unknown method')
  ratio=area/(r*r);required=-((-ratio.numerator)//ratio.denominator);excluded=len(possible)<required;fingerprint=hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest();return {'status':'EXCLUDED' if excluded else 'NOT_EXCLUDED','method':method,'proof_input':p,'domain_fingerprint':fingerprint,'possible_center_indices':possible,'required_centers_area_only':required,'area_ratio_without_pi':str(ratio),'strict_area_deficit_without_pi':str(area-len(possible)*r*r),'scope':'declared center domain only; necessary area subadditivity; tangent possibilities retained; no sum of overlapping-target deficits','global_optimality':False}
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:return {'status':'PRECONDITION_MISSING','reason':str(e),'global_optimality':False}

def anchor_variance(points,radii_squared,weights):
 """Refute a declared intersection of disks; geometric model lift separate."""
 exact_data([points,radii_squared,weights]);P=[tuple(map(F,p)) for p in points];T=list(map(F,radii_squared));W=list(map(F,weights));require(len(P)==len(T)==len(W)>0 and all(len(p)==2 for p in P),'dimensions');require(all(t>=0 for t in T) and all(w>=0 for w in W) and sum(W)>0,'nonnegative radii/weights');total=sum(W);mean=tuple(sum(w*p[d] for w,p in zip(W,P))/total for d in (0,1));variance=sum(w*sum((p[d]-mean[d])**2 for d in (0,1)) for w,p in zip(W,P));budget=sum(w*t for w,t in zip(W,T));return {'status':'EXCLUDED' if variance>budget else 'NOT_EXCLUDED','mean':[str(v) for v in mean],'variance':str(variance),'budget':str(budget),'gap':str(variance-budget),'scope':'intersection of explicitly declared disks only; graph-path/map bridge not supplied','global_optimality':False}
