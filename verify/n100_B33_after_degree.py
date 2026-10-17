"""Fresh-process B33 low/high replay with the proven new degree window."""
from pathlib import Path
import sys,json,subprocess,hashlib,builtins
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'verify'))
def main():
 if len(sys.argv)==3 and sys.argv[1]=='--task':
  import n100_remaining_branches_new_radius as old
  original=builtins.compile;changes=[]
  def adapt(text,filename,*a,**kw):
   if Path(str(filename)).name in ('verify_B33_lowM_prerequisites_0p11323.py','verify_B33_highM_any_five_0p11323.py'):
    needle='from verify_global_star_anchor_degree_window import verify as check_degrees';assert isinstance(text,str) and text.count(needle)==1;text=text.replace(needle,'from n100_B33_degree_window import verify as check_degrees');changes.append(True)
   return original(text,filename,*a,**kw)
  builtins.compile=adapt
  try:old.main();assert changes==[True]
  finally:builtins.compile=original
  return
 assert len(sys.argv)==1;folder=ROOT/'runtime/B33-new-degree-replay-152';assert not folder.exists();folder.mkdir(parents=True);rows=[]
 for task in ('B33_low','B33_high'):
  done=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--task',task],cwd=ROOT,text=True,capture_output=True);assert done.returncode==0,done.stderr;(folder/(task+'.json')).write_text(done.stdout,encoding='utf-8');row=json.loads(done.stdout);rows.append(row);print(task,row['status'],row['result'].get('error',row['result'].get('minimum_area_margin','')),flush=True)
 out=ROOT/'verify/out/n100-B33-after-degree-152.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B33-new-degree-window-replay/v1','radius':'2831/25000','components':rows,'status':'PASS' if all(x['status']=='ARITHMETIC_PASS' for x in rows) else 'NOT_CLOSED','new_degree_window_used':True,'all_original_row_support_and_final_assertions_retained':True,'full_B33_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'verify/n100_B33_degree_window.py',ROOT/'verify/out/n100-B33-degree-window-151.json',ROOT/'verify/n100_remaining_branches_new_radius.py')}},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
