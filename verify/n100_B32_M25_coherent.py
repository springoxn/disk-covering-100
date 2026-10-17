"""Exact original81-profile M25 replay for newly discovered coherent proposal.
New data are candidates only; all original arithmetic assertions are executed.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,importlib.util,traceback
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';W=P/'working';S=P/'lower_staging';sys.path[:0]=[str(ROOT/'verify'),str(S),str(W),str(W/'signed_edge_metric_20261004'),str(W/'lower_bounds_extension_20261004')]
import n100_B32_low_coherent as low

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 candidate_path=ROOT/'runtime/B32-M25-coherent-discovery-v2-142/proposal.json';candidate=json.loads(candidate_path.read_text(encoding='utf-8'));eps=F(*candidate['epsilon']);tau=F(*candidate['perimeter_penalty']);assert 0<eps<1 and tau>0 and candidate['radius']=='2831/25000';premise=low.verify();assert premise['status']=='PASS';target=F(11324,100000);slope=F(1189,20000);path=S/'verify_B32_M25_direct_interface_0p11323.py';before=path.read_bytes();text=before.decode('utf-8');changes=[('F(119,2000)',f'F({slope.numerator},{slope.denominator})',2),('assert data[\'epsilon\']==[1,2] and data[\'perimeter_penalty\']==[13,10]',f'assert data[\'epsilon\']=={candidate["epsilon"]!r} and data[\'perimeter_penalty\']=={candidate["perimeter_penalty"]!r}',1),('eps=F(1,2);weight=1-eps;tau=F(13,10);kappa=eps*tau',f'eps=F({eps.numerator},{eps.denominator});weight=1-eps;tau=F({tau.numerator},{tau.denominator});kappa=eps*tau',1)]
 for old,new,count in changes:assert text.count(old)==count;text=text.replace(old,new)
 spec=importlib.util.spec_from_file_location('M25_new_coherent',path);m=importlib.util.module_from_spec(spec);exec(compile(text,str(path),'exec'),m.__dict__);m.R=target;m.hinge.R=target;m.hinge.SETTINGS=((F(11,25),F(187,2000),slope),)+m.hinge.SETTINGS[1:];m.FAN=slope*(4*F(187,2000)-F(3467,10000))/(2*target*target);read=Path.read_text;check=m.subprocess.check_output;child=[]
 def adapt(self,*args,**kw):
  if self.resolve()==(S/'B32_M25_direct_interface_0p11323_proposal.json').resolve():return json.dumps(candidate)
  return read(self,*args,**kw)
 def premises(args,*a,**kw):
  assert len(args)==4 and Path(args[-1]).resolve()==(S/'refresh_B32_low_core_0p11323.py').resolve();child.append('fresh low.verify result');return json.dumps(premise['original_low_prerequisite_result'])
 Path.read_text=adapt;m.subprocess.check_output=premises;failure=[]
 try:
  result=m.verify();assert result['integer_profile_cases']==81 and F(result['minimum_area_margin'])>0;status='ARITHMETIC_PASS';result['upstream_proposal_file_sha256']=result.pop('proposal_sha256');result['proposal_sha256']=sha(candidate_path)
 except Exception as e:
  status='NOT_CLOSED';result={'error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()};tb=e.__traceback__
  while tb:
   f=tb.tb_frame;scale=f.f_globals.get('S');vals={}
   for key in ('margin','minimum','gap','slack','U','e','high','center','outer','si','D','J'):
    x=f.f_locals.get(key)
    if hasattr(x,'l') and hasattr(x,'u') and isinstance(scale,int):vals[key]=[str(F(x.l,scale)),str(F(x.u,scale))]
    elif isinstance(x,(int,F)):vals[key]=str(x)
   if vals:failure.append({'source':f.f_code.co_filename,'line':tb.tb_lineno,'values':vals})
   tb=tb.tb_next
 finally:Path.read_text=read;m.subprocess.check_output=check
 assert path.read_bytes()==before;out=ROOT/'verify/out/n100-B32-M25-coherent-142.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B32-M25-coherent-new-radius/v1','radius':str(target),'status':status,'result':result,'failure_locals':failure,'epsilon':str(eps),'tau':str(tau),'hinge_slope':str(slope),'FAN':str(m.FAN),'fresh_low_premises':child,'source_adaptation':'slope and FAN synchronized; fixed epsilon/tau assertions retuned to explicit candidate values; every support/domain/final assertion retained','geometry_scope':'same complete remaining M25 topology and four star patterns as original; all numeric supports replayed; inherited geometric lemmas remain dependencies','full_B32_closed':False,'global_bound_improved':False,'adapted_source_sha256':hashlib.sha256(text.encode()).hexdigest(),'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),candidate_path,path,ROOT/'verify/n100_B32_low_coherent.py',ROOT/'verify/n100_B32_M24_coherent.py')}},indent=2)+'\n',encoding='utf-8');print('EXACT M25',status,result.get('minimum_area_margin',result.get('error')),flush=True)
if __name__=='__main__':main()
