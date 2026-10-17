"""Controls and actual saved case for support/continuous variants."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
import n100_proof_interface_variants as V
import n100_continuous_proof_interfaces as C
R=Path(__file__).resolve().parents[1]
def main():
 cramer_count=V.J.controls();precond_count=V.P.controls();require=V.require;payload={'context':{'semantics_id':'scaled-real-map-boxes/v1','scale':C.Q,'map_id':'declared-control','frame_id':'fixed','parent_box_id':'control-parent','radius_domain_id':'declared-equal-distances'},'boxes':[[-2,3,-2,3],[0,0,0,0],[2,2,0,0],[0,0,2,2]],'vertex':0,'sites':[1,2,3],'method':'joint_cramer'};rows=[]
 for method in ('joint_cramer','fixed_preconditioner','determinant_corners'):
  payload['method']=method;result=V.joint_variant(copy.deepcopy(payload));require(result['status']=='NOT_EXCLUDED','control retained');rows.append(result)
 singular=copy.deepcopy(payload);singular.update(method='joint_cramer');singular['boxes'][3]=[4,4,0,0];r=V.joint_variant(singular);require(r['status']=='NOT_EXCLUDED' and not r['detail']['usable_determinant'],'singular retained')
 strict=copy.deepcopy(payload);strict['boxes'][0]=[5,6,5,6]
 for method in ('joint_cramer','fixed_preconditioner'):
  strict['method']=method;require(V.joint_variant(strict)['status']=='EXCLUDED','strict reject')
 compiled,bridge=C.compile_fixed_core([30,6,14,22],sweep_limit=1);inc={}
 for c in compiled['constraints']:
  if c['op']=='bisector_eq':inc.setdefault(c['v'],set()).update((c['a'],c['b']))
 vertex=next(v for v,owners in sorted(inc.items()) if len(owners)>=3);sites=sorted(inc[vertex])[:3];actual=[]
 for method in ('joint_cramer','fixed_preconditioner','determinant_corners'):
  p={'context':compiled['context'],'boxes':compiled['boxes'],'vertex':vertex,'sites':sites,'method':method};a=V.joint_variant(p);require(a['status']=='NOT_EXCLUDED','candidate triple retained');actual.append({k:v for k,v in a.items() if k!='proof_input'})
 ctx=V.free_intercept_context();p={'semantics_id':V.SEM,'configuration_id':'normalized-declared-U','radius_units':'radius','radius':str(V.U),'m':100,'k':54};free=V.free_intercept_filter(p,ctx);saved=json.loads((R/'verify/out/n100-arc-lens-free-intercept.json').read_text(encoding='utf-8'));require(F(free['area_deficit_lower'])==F(saved['k54_margin']) and (free['status']=='EXCLUDED')==saved['k54_excluded'],'free-intercept replay')
 controls=[]
 for label,change in [('repeated_site',lambda p:p.update(sites=[1,1,2])),('bad_frame_context',lambda p:p['context'].pop('frame_id')),('float_box',lambda p:p['boxes'][0].__setitem__(0,0.5)),('unknown_method',lambda p:p.update(method='mystery'))]:
  bad=copy.deepcopy(payload);change(bad);require(V.joint_variant(bad)['status']=='PRECONDITION_MISSING',label);controls.append(label)
 bad=copy.deepcopy(p);bad['radius']=str(V.U-F(1,10**12));require(V.free_intercept_filter(bad,ctx)['status']=='PRECONDITION_MISSING','implicit transfer');controls.append('implicit_radius_transfer')
 out=R/'verify/out/n100-proof-interface-variants.json';require(not out.exists(),'overwrite');paths=[R/'verify/n100_proof_interface_variants.py',R/'verify/n100_voronoi_joint_cramer.py',R/'verify/n100_voronoi_preconditioned.py'];out.write_text(json.dumps({'schema':'n100-proof-interface-variants/v1','cramer_rational_controls':cramer_count,'preconditioner_uncertain_center_controls':precond_count,'singular_retained':True,'strict_rejections':True,'control_results':rows,'actual_candidate_triple':{'vertex':vertex,'sites':sites,'results':actual,'bridge':bridge},'free_intercept':free,'free_support_lines_replayed':ctx['support_lines'],'support_lens_receipt':ctx['lens_receipt'],'negative_controls':controls,'scope':'three-site conditional equality contractions and fixed-U affine support; no new global exclusion','global_optimality':False,'bindings':{p.relative_to(R).as_posix():V.sha(p) for p in paths},'script_sha256':V.sha(Path(__file__))},indent=2)+'\n',encoding='utf-8');print('PASS variants;Cramer',cramer_count,'preconditioner',precond_count,'support lines',ctx['support_lines'],'controls',len(controls))
if __name__=='__main__':main()
