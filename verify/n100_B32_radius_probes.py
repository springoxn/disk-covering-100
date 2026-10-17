"""Probe B32 subcomponents in fresh processes at explicit radius.
Original assertions stay enabled; failure is diagnostic, not infeasibility.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,argparse,json,importlib.util,subprocess,traceback,hashlib
R=Path(__file__).resolve().parents[1];P=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';W=P/'working';S=P/'lower_staging';TASKS={'low_prerequisites':('refresh_B32_low_core_0p11323.py','verify'),'high_profiles':('verify_B32_highM_complete_0p11323.py','reduce_profiles'),'high_topology':('verify_B32_highM_complete_0p11323.py','topology_checks'),'high_deep_five':('verify_B32_highM_complete_0p11323.py','direct_deep_five'),'high_four_face':('verify_B32_highM_complete_0p11323.py','four_face_metric')}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--task',choices=list(TASKS));ap.add_argument('--radius',default='0.11324');ap.add_argument('--run-dir',default='runtime/B32-radius-probes-139');a=ap.parse_args();folder=R/a.run_dir
 if a.task:
  sys.path[:0]=[str(S),str(W),str(W/'lower_bounds_extension_20261004')];name,fn=TASKS[a.task];path=S/name;spec=importlib.util.spec_from_file_location('target_component',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.R=F(a.radius)
  try:result=getattr(module,fn)();status='ARITHMETIC_PASS'
  except Exception as error:result={'error_type':type(error).__name__,'error':str(error),'traceback':traceback.format_exc()};status='NOT_CLOSED'
  print(json.dumps({'task':a.task,'radius':str(F(a.radius)),'status':status,'result':result,'source':path.relative_to(R).as_posix(),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'scope':'named subcomponent only; other subcomponents and full B32 low direct interface remain separate'}));return
 assert not folder.exists();folder.mkdir(parents=True);rows=[]
 for task in TASKS:
  with (folder/(task+'.json')).open('w',encoding='utf-8') as out,(folder/(task+'.stderr.txt')).open('w',encoding='utf-8') as err:done=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--task',task,'--radius',a.radius],cwd=R,stdout=out,stderr=err)
  assert done.returncode==0,task;row=json.loads((folder/(task+'.json')).read_text(encoding='utf-8'));rows.append(row);print(task,row['status'],flush=True)
 out=R/'verify/out/n100-B32-radius-probes-139.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B32-new-radius-probes/v1','radius':str(F(a.radius)),'fresh_processes':5,'components':rows,'B32_complete':False,'remaining':'low-M25 coherent81-profile direct interface not yet adapted; any failed subcomponent needs strengthening','global_lower_bound_improved':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
