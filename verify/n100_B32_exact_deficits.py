"""Capture exact locals at B32 failed assertions without bypassing them."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,subprocess,runpy,traceback,io,contextlib,argparse,hashlib
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--task',choices=['low','high']);a=ap.parse_args()
 if a.task:
  records=[];fmt=traceback.format_exc
  def observe(*args,**kwargs):
   tb=sys.exception().__traceback__
   while tb:
    f=tb.tb_frame;locals_=f.f_locals;scale=f.f_globals.get('S');values={}
    for key in ('final24','m24','two_low','raw','one','two','marked_margin','flag','marked','slope','shifted_ear','bad','rr','payment','margin'):
     if key not in locals_:continue
     x=locals_[key]
     if hasattr(x,'l') and hasattr(x,'u') and scale:values[key]={'lower':str(F(x.l,scale)),'upper':str(F(x.u,scale))}
     elif isinstance(x,(int,F)):values[key]=str(x)
    if values:records.append({'source':f.f_code.co_filename,'line':tb.tb_lineno,'function':f.f_code.co_name,'values':values})
    tb=tb.tb_next
   return fmt(*args,**kwargs)
  traceback.format_exc=observe;sys.argv=['n100_B32_retuned_fan.py','--task',a.task];buf=io.StringIO()
  with contextlib.redirect_stdout(buf):runpy.run_path(str(R/'verify/n100_B32_retuned_fan.py'),run_name='__main__')
  row=json.loads(buf.getvalue());row['exact_failure_locals']=records;print(json.dumps(row));return
 folder=R/'runtime/B32-exact-deficits-141';assert not folder.exists();folder.mkdir(parents=True);rows=[]
 for task in ('low','high'):
  with (folder/(task+'.json')).open('w',encoding='utf-8') as out,(folder/(task+'.stderr.txt')).open('w',encoding='utf-8') as err:z=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--task',task],cwd=R,stdout=out,stderr=err)
  assert z.returncode==0;row=json.loads((folder/(task+'.json')).read_text(encoding='utf-8'));rows.append(row);assert row['status']=='NOT_CLOSED';values=row['exact_failure_locals'][-1]['values'];key='final24' if task=='low' else 'marked_margin';assert F(values[key]['upper'])<0;print(task,key,values[key],flush=True)
 out=R/'verify/out/n100-B32-exact-deficits-141.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B32-exact-deficits/v1','radius':'2831/25000','components':rows,'both_failed_margins_upper_strictly_negative':True,'original_assertions_not_skipped':True,'global_bound_improved':False,'bindings':{p.relative_to(R).as_posix():sha(p) for p in (Path(__file__),R/'verify/n100_B32_retuned_fan.py')}},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
