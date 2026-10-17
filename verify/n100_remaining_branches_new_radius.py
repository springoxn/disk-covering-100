"""Fresh-process probes for remaining global branches at explicit new radius.
Proposal radius metadata is adapted; rows untouched. No global theorem claim.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,subprocess,importlib.util,argparse,traceback,hashlib
R=Path(__file__).resolve().parents[1];P=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';W=P/'working';S=P/'lower_staging'
TASKS={'B33_low':W/'verify_B33_lowM_prerequisites_0p11323.py','B33_high':W/'verify_B33_highM_any_five_0p11323.py','B33_M26':W/'verify_N26_seven_face_metric_0p11322.py','B33_M27':W/'verify_N27_metric_chord_cases_0p11322.py','B33_ear':W/'verify_B33_one_ear_metric_0p11323.py','B33_coherent':W/'verify_B33_M25_coherent_five.py','B34_full':S/'B34_0p11323/verify_hinge_B34_complete_0p11323.py','B35_envelope':W/'lower_staging/B35_0p11323/verify_normalized_boundary_penalty_0p11323.py','B35_full':W/'lower_staging/B35_0p11323/check_B35_complete_0p11323_v2.py'}
META={'B33_lowM_prerequisites_0p11323_proposals.json','B33_highM_any_five_0p11323_proposal.json','hinge_B34_0p11323_proposals.json'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--task',choices=list(TASKS));a=ap.parse_args();target=F(11324,100000)
 if a.task:
  path=TASKS[a.task];sys.path[:0]=[str(path.parent),str(W),str(W/'lower_bounds_extension_20261004'),str(S)];before=path.read_bytes();text=before.decode('utf-8');changes={k:text.count(k) for k in ('F(1733,2500)','F(1733,5000)')};text=text.replace('F(1733,2500)','F(17331,25000)').replace('F(1733,5000)','F(17331,50000)');spec=importlib.util.spec_from_file_location('new_radius_component',path);m=importlib.util.module_from_spec(spec);exec(compile(text,str(path),'exec'),m.__dict__);m.R=target
  if a.task=='B35_full':m.boundary.R=target
  if a.task=='B34_full':m.hinge.R=target;m.hinge.SPAN=F(17331,25000)
  original=Path.read_text;adapted=[]
  def read(self,*args,**kwargs):
   data=original(self,*args,**kwargs)
   if self.name in META:
    obj=json.loads(data);old=obj.get('radius');obj['radius']=str(target);adapted.append({'path':str(self),'old_radius':old,'only_change':'root radius metadata'});return json.dumps(obj)
   return data
  Path.read_text=read
  try:result=m.verify();status='ARITHMETIC_PASS';failure=[]
  except Exception as e:
   status='NOT_CLOSED';result={'error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()};failure=[];tb=e.__traceback__
   while tb:
    frame=tb.tb_frame;scale=frame.f_globals.get('S');vals={}
    for key,value in frame.f_locals.items():
     if key in ('margin','final','final25','degree_margin','coregap','footprint','payment','difference','gap','shifted','ear','bad','charge','minimum','endpoint'):
      if hasattr(value,'l') and hasattr(value,'u') and isinstance(scale,int):vals[key]=[str(F(value.l,scale)),str(F(value.u,scale))]
      elif isinstance(value,(int,F)):vals[key]=str(value)
    if vals:failure.append({'source':frame.f_code.co_filename,'line':tb.tb_lineno,'values':vals})
    tb=tb.tb_next
  finally:Path.read_text=original
  assert path.read_bytes()==before;print(json.dumps({'task':a.task,'radius':str(target),'status':status,'result':result,'failure_locals':failure,'source':path.relative_to(R).as_posix(),'source_sha256':hashlib.sha256(before).hexdigest(),'adapted_fan_literal_counts':changes,'adapted_metadata':adapted,'scope':'named component arithmetic only; radius propagation enumerated explicitly; remaining global premises not inferred'}));return
 folder=R/'runtime/remaining-branches-141';assert not folder.exists();folder.mkdir(parents=True);rows=[]
 for task in TASKS:
  with (folder/(task+'.json')).open('w',encoding='utf-8') as out,(folder/(task+'.stderr.txt')).open('w',encoding='utf-8') as err:done=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--task',task],cwd=R,stdout=out,stderr=err)
  assert done.returncode==0,task;row=json.loads((folder/(task+'.json')).read_text(encoding='utf-8'));rows.append(row);print(task,row['status'],flush=True)
 out=R/'verify/out/n100-remaining-branches-141.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-remaining-branches-new-radius/v1','target_radius':str(target),'fresh_processes':len(rows),'components':rows,'all_branches_closed':False,'global_bound_improved':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
