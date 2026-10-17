"""B34 target-radius diagnostic: retain every premise and other area assertions."""
from pathlib import Path
import sys,json,subprocess,builtins,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'verify'))
def main():
 if len(sys.argv)==2 and sys.argv[1]=='--worker':
  import n100_remaining_branches_new_radius as old
  comp=builtins.compile;seen=[]
  def adapt(text,filename,*a,**kw):
   if Path(str(filename)).name=='verify_hinge_B34_complete_0p11323.py':
    rules=[("assert gap>0,('area',branch,F(gap,S))","if idx!=1:assert gap>0,('area',branch,F(gap,S))"),('vertex_min=None\n','vertex_min=None;neutral_low=[];positive_low=[]\n'),("assert gap>0,('vertex',branch,p,d,ix,F(gap,S))","assert gap>0,('vertex',branch,p,d,ix,F(gap,S))\n            if ix==2 and d<=5:neutral_low.append((p,d,F(gap,S)))\n            if ix==3:positive_low.append((p,d,F(gap,S)))"),("'bad_q1_coefficient_upper':str(F(bad.u,S)),'area_margin':str(F(gap,S))}","'bad_q1_coefficient_upper':str(F(bad.u,S)),'area_margin':str(F(gap,S)),'M_slope_upper':str(F(slope.u,S)),'neutral_low_slacks':[(p,d,str(v)) for p,d,v in neutral_low],'positive_low_slacks':[(p,d,str(v)) for p,d,v in positive_low]}") ,("'scope':'Complete B34 branch after whole-cover norm normalization; no all-count radius theorem'","'scope':'Diagnostic only; M24 endpoint area assertion deliberately not accepted, other2 area assertions retained'")]
    for src,dst in rules:assert text.count(src)==1,(src,text.count(src));text=text.replace(src,dst)
    seen.append(True)
   return comp(text,filename,*a,**kw)
  builtins.compile=adapt;sys.argv=[sys.argv[0],'--task','B34_full']
  try:old.main();assert seen==[True]
  finally:builtins.compile=comp
  return
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 done=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--worker'],cwd=ROOT,text=True,capture_output=True);assert done.returncode==0,done.stderr;row=json.loads(done.stdout);out=ROOT/'verify/out/n100-B34-diagnostic-169.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B34-M24-diagnostic/v1','radius':'2831/25000','status':'PASS_PREMISES' if row['status']=='ARITHMETIC_PASS' else 'NOT_CLOSED','replay':row,'B34_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),ROOT/'verify/n100_remaining_branches_new_radius.py')}},indent=2)+'\n',encoding='utf-8');print('B34 DIAG',row['status'],flush=True)
 if row['status']=='ARITHMETIC_PASS':
  print('budget',row['result']['geometry']['old_normalized_loss_upper'],flush=True)
  for z in row['result']['branches']:print(z['branch'],z['area_margin'],'slope',z['M_slope_upper'],'neutralmin',min(__import__('fractions').Fraction(v) for p,d,v in z['neutral_low_slacks']),flush=True)
if __name__=='__main__':main()
