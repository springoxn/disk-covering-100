"""Fresh replay remaining B33 no-degree5 metric components at target radius."""
from pathlib import Path
import json,subprocess,sys,hashlib
ROOT=Path(__file__).resolve().parents[1]
def main():
 source=ROOT/'verify/n100_remaining_branches_new_radius.py';rows=[]
 for task in ('B33_M26','B33_M27','B33_ear'):
  done=subprocess.run([sys.executable,'-B','-S',str(source),'--task',task],cwd=ROOT,text=True,capture_output=True);assert done.returncode==0,done.stderr;row=json.loads(done.stdout);assert row['status']=='ARITHMETIC_PASS',row;rows.append(row);print(task,row['status'],flush=True)
 out=ROOT/'verify/out/n100-B33-no5-components-166.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B33-no5-conditional-components/v1','status':'PASS','radius':'2831/25000','components':rows,'scope':'Fresh same-radius conditional no5 components; final topology and full low/high coverage composed separately','full_B33_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),source)}},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
