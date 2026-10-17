"""Retune B32 fan angle consistently in fresh subprocesses.
Only two exact source literals L and L/2 are adapted; upstream unchanged.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys,subprocess,argparse,importlib.util,traceback
R=Path(__file__).resolve().parents[1];P=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';W=P/'working';S=P/'lower_staging';TASKS={'low':('refresh_B32_low_core_0p11323.py','verify'),'high':('verify_B32_highM_complete_0p11323.py','reduce_profiles')}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--task',choices=list(TASKS));a=ap.parse_args()
 if a.task:
  sys.path[:0]=[str(S),str(W),str(W/'lower_bounds_extension_20261004')];name,fn=TASKS[a.task];path=S/name;before=path.read_bytes();text=before.decode('utf-8');counts=[text.count('F(1733,2500)'),text.count('F(1733,5000)')];assert counts[0]==1 and counts[1]==(1 if a.task=='low' else 0);text=text.replace('F(1733,2500)','F(17331,25000)').replace('F(1733,5000)','F(17331,50000)');spec=importlib.util.spec_from_file_location('fan_component',path);m=importlib.util.module_from_spec(spec);exec(compile(text,str(path),'exec'),m.__dict__);m.R=F(11324,100000)
  try:result=getattr(m,fn)();status='ARITHMETIC_PASS'
  except Exception as e:result={'error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()};status='NOT_CLOSED'
  assert path.read_bytes()==before;print(json.dumps({'task':a.task,'radius':str(m.R),'fan_angle':'17331/25000','source_literal_replacements_L_and_half':counts,'status':status,'result':result,'upstream_source_sha256':hashlib.sha256(before).hexdigest(),'adapted_source_sha256':hashlib.sha256(text.encode('utf-8')).hexdigest(),'upstream_unchanged':True}));return
 folder=R/'runtime/B32-retuned-fan-140';assert not folder.exists();folder.mkdir(parents=True);rows=[]
 for task in TASKS:
  with (folder/(task+'.json')).open('w',encoding='utf-8') as out,(folder/(task+'.stderr.txt')).open('w',encoding='utf-8') as err:z=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--task',task],cwd=R,stdout=out,stderr=err)
  assert z.returncode==0;row=json.loads((folder/(task+'.json')).read_text(encoding='utf-8'));rows.append(row);print(task,row['status'],flush=True)
 out=R/'verify/out/n100-B32-retuned-fan-140.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B32-retuned-fan/v1','radius':'2831/25000','fan_angle':'17331/25000','components':rows,'global_bound_improved':False,'B32_complete':False,'scope':'retuned fan and half-angle consistent in low prerequisite and high profile checks; low M25 full81-case closure remains separate','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
