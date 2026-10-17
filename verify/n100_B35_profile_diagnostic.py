"""B35 M25/M26 vertex-gap profile diagnostic, preserving exact source checks."""
from pathlib import Path
import sys,json,subprocess,builtins,hashlib
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working/lower_staging/B35_0p11323/check_B35_complete_0p11323_v2.py'
def main():
 if len(sys.argv)==2 and sys.argv[1]=='--worker':
  import n100_remaining_branches_new_radius as old
  comp=builtins.compile;seen=[]
  def adapt(text,filename,*a,**kw):
   if Path(str(filename)).name==SRC.name:
    rules=[("assert low.l>0;z['M_le24_flagged_margin']=str(F(low.l,S))","z['M_le24_flagged_margin']=str(F(low.l,S))"),("assert low.l>0;z['any_low_degree_margin']=str(F(low.l,S))","z['any_low_degree_margin']=str(F(low.l,S))"),("z,m,c,gaps,ear,bad=bounds(RESTRICTED,True);assert m.l>0","z,m,c,gaps,ear,bad=bounds(RESTRICTED,True);z['restricted_M25_margin']=str(F(m.l,S))"),("z,m,c,gaps,ear,bad=bounds(M26_RESTRICTED,True,2);assert m.l>0","z,m,c,gaps,ear,bad=bounds(M26_RESTRICTED,True,2);z['restricted_M26_margin']=str(F(m.l,S))"),("gaps[p,d]=F(gap,S);vertex_count+=1","gaps[p,d]=F(gap,S);vertex_count+=1\n             if restricted and (M in (25,26)) and d in (6,7,8,9,10,12,20,50,99): z.setdefault('profile_gaps',[]).append([p,d,str(F(gap,S))])")]
    for src,dst in rules:assert text.count(src)==1,(src,text.count(src));text=text.replace(src,dst)
    seen.append(True)
   return comp(text,filename,*a,**kw)
  builtins.compile=adapt;sys.argv=[sys.argv[0],'--task','B35_full']
  try:old.main();assert seen==[True]
  finally:builtins.compile=comp
  return
 done=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--worker'],cwd=ROOT,text=True,capture_output=True);assert done.returncode==0,done.stderr;row=json.loads(done.stdout);out=ROOT/'verify/out/n100-B35-profile-diagnostic-186.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B35-profile-gaps/v1','status':'PASS_PREMISES' if row['status']=='ARITHMETIC_PASS' else 'NOT_CLOSED','radius':'2831/25000','replay':row,'B35_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),SRC,ROOT/'verify/n100_remaining_branches_new_radius.py')}},indent=2)+'\n',encoding='utf-8');print('B35 PROFILE DIAG',row['status'],flush=True)
if __name__=='__main__':main()
