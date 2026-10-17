"""Probe full81-profile B32 M25 row using freshly replayed new low premises."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,importlib.util,traceback
R=Path(__file__).resolve().parents[1];P=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';W=P/'working';S=P/'lower_staging';sys.path[:0]=[str(R/'verify'),str(S),str(W),str(W/'signed_edge_metric_20261004'),str(W/'lower_bounds_extension_20261004')]
import n100_B32_low_coherent as low

def main():
 target=F(11324,100000);premise=low.verify();assert premise['status']=='PASS';path=S/'verify_B32_M25_direct_interface_0p11323.py';spec=importlib.util.spec_from_file_location('direct_new_radius',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.R=target;m.hinge.R=target;m.FAN=F(119,2000)*(4*F(187,2000)-F(3467,10000))/(2*target*target);read=Path.read_text;check=m.subprocess.check_output;calls=[]
 def metadata(self,*a,**kw):
  text=read(self,*a,**kw)
  if self.resolve()==(S/'B32_M25_direct_interface_0p11323_proposal.json').resolve():data=json.loads(text);data['radius']=str(target);return json.dumps(data)
  return text
 def premises(args,*a,**kw):
  assert len(args)==4 and Path(args[-1]).resolve()==(S/'refresh_B32_low_core_0p11323.py').resolve();calls.append('fresh exact low.verify result substituted for fixed-radius child entry');return json.dumps(premise['original_low_prerequisite_result'])
 Path.read_text=metadata;m.subprocess.check_output=premises;failure=[]
 try:result=m.verify();status='ARITHMETIC_PASS'
 except Exception as error:
  result={'error_type':type(error).__name__,'error':str(error),'traceback':traceback.format_exc()};status='NOT_CLOSED';tb=error.__traceback__
  while tb:
   f=tb.tb_frame;scale=f.f_globals.get('S');values={}
   for key in ('margin','minimum','FAN','U','e','high','center','outer'):
    x=f.f_locals.get(key)
    if hasattr(x,'l') and hasattr(x,'u') and isinstance(scale,int):values[key]=[str(F(x.l,scale)),str(F(x.u,scale))]
    elif isinstance(x,(int,F)):values[key]=str(x)
   if values:failure.append({'source':f.f_code.co_filename,'line':tb.tb_lineno,'values':values})
   tb=tb.tb_next
 finally:Path.read_text=read;m.subprocess.check_output=check
 out=R/'verify/out/n100-B32-M25-new-radius-141.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B32-M25-new-radius/v1','radius':str(target),'status':status,'result':result,'failure_locals':failure,'fresh_low_prerequisites_replayed':True,'low_M24_coherent_gain':premise['M24_normalized_gain'],'same_radius_child_adapter':calls,'hinge_radius_explicitly_set':str(m.hinge.R),'FAN_recomputed_at_current_radius':str(m.FAN),'proposal_adaptation':'root radius metadata only; coefficients unmodified','full_B32_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),path,R/'verify/n100_B32_low_coherent.py',R/'verify/n100_B32_M24_coherent.py')}},indent=2)+'\n',encoding='utf-8');print('M25',status,result.get('minimum_area_margin',result.get('error')),flush=True)
if __name__=='__main__':main()
