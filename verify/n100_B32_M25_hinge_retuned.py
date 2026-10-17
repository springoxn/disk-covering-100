"""Retuned M25 hinge slope with synchronized FAN at explicit new radius.
Every original assertion remains; no failed hinge is accepted.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,importlib.util,traceback,argparse,subprocess
R=Path(__file__).resolve().parents[1];P=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';W=P/'working';S=P/'lower_staging';sys.path[:0]=[str(R/'verify'),str(S),str(W),str(W/'signed_edge_metric_20261004'),str(W/'lower_bounds_extension_20261004')]
import n100_B32_low_coherent as low
from verify_star_lp_duals import q,PI,S as SCALE
from verify_potential_star_duals import sine,cosine

def inter(x):return [str(F(x.l,SCALE)),str(F(x.u,SCALE))]
def endpoint(target,slope):
 rr=q(target);K=q(F(11,25));T=rr.sq();mu=PI/32;sm=sine(mu);cm=cosine(mu);hm=(T-sm.sq()).sqrt();b=T*K*(hm*cm+sm.sq())/rr
 # outer(mu) uses asin(sm/rr), from exact acos helper.
 from exact_angle_conjugates import acos_interval
 asn=lambda x:PI/2-acos_interval(x)
 fm=sm*hm+mu-sm*cm+b*(asn(sm/rr)-mu);dm=cm*(T-2*sm.sq())/hm+2*sm.sq()+b*(cm/hm-1);p=K*T*(2*(1-rr)).sqrt();g=fm-dm*mu-p-q(slope)*q(F(187,2000));return {'zero_arc_deficit_after_hinge':inter(g),'zero_arc_maximum_slope':inter((fm-dm*mu-p)/q(F(187,2000)))}

def worker(slope):
 target=F(11324,100000);premise=low.verify();assert premise['status']=='PASS';path=S/'verify_B32_M25_direct_interface_0p11323.py';before=path.read_bytes();text=before.decode('utf-8');assert text.count('F(119,2000)')==2;text=text.replace('F(119,2000)',f'F({slope.numerator},{slope.denominator})');spec=importlib.util.spec_from_file_location('retuned_M25',path);m=importlib.util.module_from_spec(spec);exec(compile(text,str(path),'exec'),m.__dict__);m.R=target;m.hinge.R=target;m.hinge.SETTINGS=((F(11,25),F(187,2000),slope),)+m.hinge.SETTINGS[1:];m.FAN=slope*(4*F(187,2000)-F(3467,10000))/(2*target*target);read=Path.read_text;check=m.subprocess.check_output;calls=[]
 def metadata(self,*a,**kw):
  txt=read(self,*a,**kw)
  if self.resolve()==(S/'B32_M25_direct_interface_0p11323_proposal.json').resolve():d=json.loads(txt);d['radius']=str(target);return json.dumps(d)
  return txt
 def premises(args,*a,**kw):
  assert len(args)==4 and Path(args[-1]).resolve()==(S/'refresh_B32_low_core_0p11323.py').resolve();calls.append('actual new-radius low.verify replay');return json.dumps(premise['original_low_prerequisite_result'])
 Path.read_text=metadata;m.subprocess.check_output=premises;failed=[]
 try:result=m.verify();status='ARITHMETIC_PASS'
 except Exception as e:
  result={'error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()};status='NOT_CLOSED';tb=e.__traceback__
  while tb:
   f=tb.tb_frame;scale=f.f_globals.get('S');values={}
   for key in ('margin','minimum','FAN','gap','U','e','high','center','outer','j'):
    x=f.f_locals.get(key)
    if hasattr(x,'l') and hasattr(x,'u') and isinstance(scale,int):values[key]=[str(F(x.l,scale)),str(F(x.u,scale))]
    elif isinstance(x,(int,F)):values[key]=str(x)
   if values:failed.append({'source':f.f_code.co_filename,'line':tb.tb_lineno,'values':values})
   tb=tb.tb_next
 finally:Path.read_text=read;m.subprocess.check_output=check
 assert path.read_bytes()==before
 return {'radius':str(target),'slope':str(slope),'FAN':str(m.FAN),'status':status,'result':result,'endpoint':endpoint(target,slope),'failure_locals':failed,'fresh_low_prerequisites_replayed':True,'same_radius_child_calls':calls,'coefficient_adaptation':'two source slope literals, hinge SETTINGS[0], and FAN all changed consistently; original source/data unchanged','adapted_source_sha256':hashlib.sha256(text.encode()).hexdigest()}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--slope');a=ap.parse_args()
 if a.slope:print(json.dumps(worker(F(a.slope))));return
 folder=R/'runtime/B32-M25-hinge-retuned-142';assert not folder.exists();folder.mkdir(parents=True);rows=[]
 for index,slope in enumerate(('0.05945','0.0594','0.0593')):
  with (folder/(str(index)+'.json')).open('w',encoding='utf-8') as out,(folder/(str(index)+'.stderr.txt')).open('w',encoding='utf-8') as err:p=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--slope',slope],cwd=R,stdout=out,stderr=err)
  assert p.returncode==0;row=json.loads((folder/(str(index)+'.json')).read_text(encoding='utf-8'));rows.append(row);print(slope,row['status'],row['result'].get('minimum_area_margin',row['result'].get('error')),flush=True)
 result={'schema':'n100-M25-retuned-hinge/v1','radius':'2831/25000','candidates':rows,'old_slope_endpoint':endpoint(F(11324,100000),F(119,2000)),'global_bound_improved':False,'full_B32_closed':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};out=R/'verify/out/n100-B32-M25-hinge-retuned-142.json';assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
