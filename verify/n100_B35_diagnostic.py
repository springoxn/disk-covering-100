"""B35 target-radius diagnostic preserving all non-flagged assertions."""
from pathlib import Path
import sys,json,subprocess,builtins,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'verify'))
def main():
 if len(sys.argv)==2 and sys.argv[1]=='--worker':
  import n100_remaining_branches_new_radius as old
  comp=builtins.compile;seen=[]
  def adapt(text,filename,*a,**kw):
   if Path(str(filename)).name=='check_B35_complete_0p11323_v2.py':
    rules=[('assert low.l>0;z[\'M_le24_flagged_margin\']=str(F(low.l,S))',"z['M_le24_flagged_margin']=str(F(low.l,S))"),("assert low.l>0;z['any_low_degree_margin']=str(F(low.l,S))","z['any_low_degree_margin']=str(F(low.l,S))"),("'scope':'Complete B35 branch for globally normalized diagrams; normalization must precede B/graph classification'","'scope':'Diagnostic: flagged low-M assertions intentionally reported, all other original checks retained'")]
    for src,dst in rules:assert text.count(src)==1;text=text.replace(src,dst)
    seen.append(True)
   return comp(text,filename,*a,**kw)
  builtins.compile=adapt;sys.argv=[sys.argv[0],'--task','B35_full']
  try:old.main();assert seen==[True]
  finally:builtins.compile=comp
  return
 done=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--worker'],cwd=ROOT,text=True,capture_output=True);assert done.returncode==0,done.stderr;row=json.loads(done.stdout);out=ROOT/'verify/out/n100-B35-diagnostic-181.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B35-flagged-lowM-diagnostic/v1','status':'PASS_PREMISES' if row['status']=='ARITHMETIC_PASS' else 'NOT_CLOSED','radius':'2831/25000','replay':row,'B35_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'verify/n100_remaining_branches_new_radius.py')}},indent=2)+'\n',encoding='utf-8');print('B35 DIAG',row['status'],flush=True)
if __name__=='__main__':main()
