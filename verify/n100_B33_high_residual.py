"""Exact B33 highM residual reduction without the failed one-five exclusion.
Retains old valid K=.44 and hinge=.03; proves two5/shifted exclusions instead.
"""
from pathlib import Path
import sys,json,subprocess,builtins,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'verify'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if len(sys.argv)==2 and sys.argv[1]=='--worker':
  import n100_remaining_branches_new_radius as old
  compile0=builtins.compile;seen=[]
  def adapt(text,filename,*a,**kw):
   if Path(str(filename)).name=='verify_B33_highM_any_five_0p11323.py':
    rules=[('from verify_global_star_anchor_degree_window import verify as degree_check','from n100_B33_degree_window_stdlib import verify as degree_check'),('margin=PI-(rr.sq()*center+Q);assert margin.l>0','margin=PI-(rr.sq()*center+Q)\n    two_five=margin+rr.sq()*flag\n    shifted_low_margins={"M>=27":margin-rr.sq()*slope,"ears>=1":margin-rr.sq()*shifted,"bad_q1>=1":margin-rr.sq()*bad}\n    assert two_five.l>0 and all(x.l>0 for x in shifted_low_margins.values())'),("scope='Every interior degree is at least six; ears and bad q1 are not yet excluded'","scope='Residual reduction only: zero degree5 original Euler cases or unique5 M26 e0 b0 with high curvature2'"),("degree5_contradiction_margin=str(F(margin.l,S)),","degree5_contradiction_margin=str(F(margin.l,S)),two_degree5_margin=str(F(two_five.l,S)),shifted_low_margins={k:str(F(v.l,S)) for k,v in shifted_low_margins.items()},")]
    for src,dst in rules:assert isinstance(text,str) and text.count(src)==1;text=text.replace(src,dst)
    seen.append(True)
   return compile0(text,filename,*a,**kw)
  builtins.compile=adapt;sys.argv=[sys.argv[0],'--task','B33_high']
  try:old.main();assert seen==[True]
  finally:builtins.compile=compile0
  return
 assert len(sys.argv)==1;done=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--worker'],cwd=ROOT,text=True,capture_output=True);assert done.returncode==0,done.stderr;row=json.loads(done.stdout);passed=row['status']=='ARITHMETIC_PASS';res=row['result'];remaining=[]
 if passed:
  from fractions import Fraction as F
  assert F(res['two_degree5_margin'])>0 and all(F(v)>0 for v in res['shifted_low_margins'].values());assert F(res['degree5_contradiction_margin'])<0
  for high in ([7,7],[8]):assert sum(d-6 for d in high)==2;remaining.append({'M':26,'ears':0,'bad_q1':0,'unique_degree5':True,'low_marked_range':[0,4],'high_degrees':high,'high_marked_ranges':[[0,d-1] for d in high],'other_interior_degrees':6,'boundary_neighbor_split_pending':True})
  assert 27-26+1==2
 out=ROOT/'verify/out/n100-B33-high-residual-159.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-B33-highM-precise-residual/v1','status':'PASS_REDUCTION' if passed else 'NOT_CLOSED','radius':'2831/25000','B':33,'M_domain':'M>=26','source_replay':row,'no_degree5_Euler_cases':res.get('remaining_Euler_cases',[]),'degree5_remaining_profiles':remaining,'one_degree5_exclusion_not_assumed':True,'old_K_and_original_hinge_reverified':True,'high_M_closed':False,'full_B33_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),ROOT/'verify/n100_remaining_branches_new_radius.py',ROOT/'verify/n100_B33_degree_window.py',ROOT/'verify/n100_B33_degree_window_stdlib.py',ROOT/'verify/out/n100-B33-degree-window-151.json',ROOT/'verify/out/n100-B33-degree-window-independent-153.json')}},indent=2)+'\n',encoding='utf-8');print('B33 HIGH RESIDUAL',passed,'two5 margin',res.get('two_degree5_margin'),'remaining degree5 macroprofiles',len(remaining),flush=True)
if __name__=='__main__':main()
