"""Reviewed support/contractor variants, separate from frozen earlier interfaces."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
from n100_proof_interfaces import require,exact_data
import n100_continuous_proof_interfaces as C
import n100_voronoi_joint_cramer as J
import n100_voronoi_preconditioned as P
from n100_arc_budget_interfaces import audit_lens,pi_check,U,SEM
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def joint_variant(payload):
 try:
  exact_data(payload);base={'context':payload['context'],'boxes':payload['boxes'],'constraints':[],'sweep_limit':1};require(C.run(base)['status']=='NOT_EXCLUDED','invalid real parent boxes');indices=payload['sites'];v=payload['vertex'];require(type(v) is int and 0<=v<len(payload['boxes']) and len(indices)==3 and len(set(indices))==3 and all(type(i) is int and 0<=i<len(payload['boxes']) and i!=v for i in indices),'three distinct sites');sites=[payload['boxes'][i] for i in indices];box=payload['boxes'][v];method=payload['method']
  if method=='joint_cramer':
   out,used=J.joint(box,sites);alt,altused=J.joint(box,sites,True);require((out,used)==(alt,altused),'Fraction Cramer replay');detail={'usable_determinant':used,'independent_scope':'shared interval products, separate Fraction endpoint quotient'}
  elif method=='fixed_preconditioner':
   out,usable,active=P.contract_joint(box,sites);detail={'usable_scalar_coefficients':usable,'active_midpoint_adjugate':active,'independent_scope':'legacy rational quotient audit; full separate contractor not provided'}
  elif method=='determinant_corners':
   values=[]
   for corner in product(*[s[2*k:2*k+2] for s in sites for k in (0,1)]):
    ax,ay,bx,by,cx,cy=corner;d=(bx-ax)*(cy-ay)-(by-ay)*(cx-ax);require(d==bx*cy-bx*ay-ax*cy-by*cx+by*ax+ay*cx,'multi-affine determinant expansion');values.append(d)
   return {'status':'NOT_EXCLUDED','determinant_interval':[min(values),max(values)],'zero_excluded_from_determinant':min(values)>0 or max(values)<0,'scope':'diagnostic determinant interval only; neither nonsingularity nor singularity is infeasibility','proof_input':payload,'global_optimality':False}
  else:raise ValueError('unknown joint variant')
  if out is not None:require(box[0]<=out[0]<=out[1]<=box[1] and box[2]<=out[2]<=out[3]<=box[3],'contraction enclosure')
  return {'status':'EXCLUDED' if out is None else 'NOT_EXCLUDED','vertex_box':out,'detail':detail,'proof_input':payload,'scope':'declared three-site equal-distance necessary system only; map bridge inherited','global_optimality':False}
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:return {'status':'PRECONDITION_MISSING','reason':str(e),'global_optimality':False}

def free_intercept_context():
 lp=R/'verify/out/n100-arc-lens-support.json';fp=R/'verify/out/n100-arc-lens-free-intercept.json';lens=json.loads(lp.read_text(encoding='utf-8'));free=json.loads(fp.read_text(encoding='utf-8'));require(sha(R/'verify/n100_arc_lens_support.py')==lens['script_sha256'] and sha(R/'verify/n100_arc_lens_free_intercept.py')==free['script_sha256'] and free['input_sha256']==sha(lp),'free support source chain');receipt=audit_lens(lens);require(F(free['radius'])==F(lens['radius'])==U and F(free['delta'])==F(lens['delta']),'support same radius/delta');a,b=F(free['slope']),F(free['intercept']);require(a>=0,'nonnegative slope for half-arc lower transfer');lines=[(F(s['arc_half_upper']),F(s['lens_area_upper'])) for s in lens['steps']]+[(F(lens['maximum_half_arc_upper']),F(0))];slacks=[b-a*p-area for p,area in lines];require(all(s>=0 for s in slacks),'affine envelope violation');active=[p for (p,area),slack in zip(lines,slacks) if slack==0];pl,ph=map(F,lens['pi_interval']);pi_check(pl,ph);require(bool(active),'no tight support');require(min(active)*54<=pl<=max(active)*54 if a>0 else max(active)*54>=pl,'convex optimality for fixed envelope/k54');require(54*b-a*pl==F(free['k54_objective']),'objective binding')
 return {'radius':U,'delta':F(free['delta']),'slope':a,'intercept':b,'pi':(pl,ph),'support_lines':len(lines),'lens_receipt':receipt,'bindings':{p.relative_to(R).as_posix():sha(p) for p in [lp,fp,R/'verify/n100_arc_lens_support.py',R/'verify/n100_arc_lens_free_intercept.py']}}

def free_intercept_filter(payload,ctx):
 try:
  exact_data(payload);require(payload.get('semantics_id')==SEM and payload.get('configuration_id') and payload.get('radius_units')=='radius' and F(payload['radius'])==U,'fixed-radius/count semantics');m,k=payload['m'],payload['k'];require(type(m) is int and type(k) is int and 0<=k<=m<=100,'service count');pl,ph=ctx['pi'];margin=pl*(1-2*U+ctx['delta'])**2-(m-k)*ph*U*U-k*ctx['intercept']+ctx['slope']*pl
  return {'status':'EXCLUDED' if margin>0 else 'NOT_EXCLUDED','area_deficit_lower':str(margin),'proof_input':payload,'bindings':ctx['bindings'],'scope':'fixed affine upper support; optimal only for saved rectangular envelope/k54, not all geometry','additive_area_budget':False,'global_optimality':False}
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:return {'status':'PRECONDITION_MISSING','reason':str(e),'global_optimality':False}
