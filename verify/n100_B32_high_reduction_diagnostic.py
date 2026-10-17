"""Diagnose high-M reduction beyond the known marked-low failure.
Only marked margin assertion disabled; never accepts altered residual classification.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,importlib.util,traceback
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';W=P/'working';S=P/'lower_staging';sys.path[:0]=[str(S),str(W),str(W/'lower_bounds_extension_20261004')]
def main():
 path=S/'verify_B32_highM_complete_0p11323.py';before=path.read_bytes();text=before.decode('utf-8');rules=[('geometry.cluster_exclusion(B,5,F(1733,2500),3,F(1,1000))','geometry.cluster_exclusion(B,5,F(17331,25000),3,F(1,1000))'),('marked_margin=raw+rr.sq()*q(marked);assert marked_margin.l>0','marked_margin=raw+rr.sq()*q(marked) # diagnostic: do not assert positive')]
 for a,b in rules:assert text.count(a)==1;text=text.replace(a,b)
 spec=importlib.util.spec_from_file_location('high_diagnostic_147',path);m=importlib.util.module_from_spec(spec);exec(compile(text,str(path),'exec'),m.__dict__);m.R=F(11324,100000);capture={}
 def tracer(frame,event,arg):
  if event=='return' and frame.f_code.co_name=='reduce_profiles' and frame.f_globals is m.__dict__:
   gaps=frame.f_locals.get('gaps',{});capture['marked_candidates']=[{'p':p,'d':d,'slack':str(v)} for (p,d),v in gaps.items() if p>0 and d<=5]
 sys.setprofile(tracer)
 try:result=m.reduce_profiles();status='DIAGNOSTIC_OTHER_REDUCTION_CHECKS_PASS';result['status']='DIAGNOSTIC_NOT_A_PROOF';result['remaining_profiles_original_not_accepted']=result.pop('remaining_profiles');result['marked_low_profiles_still_open']=[{'M':26,'ears':0,'bad_q1':0,'low_degree':5,'low_p':p,'high_degree':7,'high_p':h,'others_degree':6} for p in (1,2,3) for h in range(4)]
 except Exception as e:status='NOT_CLOSED';result={'error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()}
 finally:sys.setprofile(None)
 assert path.read_bytes()==before;out=ROOT/'verify/out/n100-B32-high-reduction-diagnostic-147.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-highM-exact-diagnostic/v1','radius':str(m.R),'status':status,'result':result,'captured':capture,'disabled_assertion':'only marked_margin positivity; altered remainder classification not accepted','full_B32_closed':False,'global_bound_improved':False,'adapted_source_sha256':hashlib.sha256(text.encode()).hexdigest(),'source_sha256':hashlib.sha256(before).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('HIGH DIAGNOSTIC',status,result.get('error',result.get('marked_low_margin')),flush=True)
if __name__=='__main__':main()
