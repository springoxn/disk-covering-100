"""Exact B33 highM new-K row replay, all original assertions retained."""
from pathlib import Path
import sys,json,subprocess,hashlib,builtins
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'verify'));CANDIDATE=ROOT/'runtime/B33-high-row-discovery-154/proposal.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if len(sys.argv)==2 and sys.argv[1]=='--worker':
  import n100_remaining_branches_new_radius as old
  candidate=json.loads(CANDIDATE.read_text(encoding='utf-8'));K=F(*candidate['halfside_multiplier']);assert candidate['radius']=='2831/25000';read=Path.read_text;compile0=builtins.compile;seen=[]
  def adapted_read(self,*a,**kw):
   text=read(self,*a,**kw)
   if self.name=='B33_highM_any_five_0p11323_proposal.json':seen.append('proposal');return json.dumps(candidate)
   return text
  def adapted_compile(text,filename,*a,**kw):
   if Path(str(filename)).name=='verify_B33_highM_any_five_0p11323.py':
    for src,dst in [('from verify_global_star_anchor_degree_window import verify as degree_check','from n100_B33_degree_window_stdlib import verify as degree_check'),('K=F(11,25)',f'K=F({K.numerator},{K.denominator})')]:assert isinstance(text,str) and text.count(src)==1;text=text.replace(src,dst)
    seen.append('source')
   return compile0(text,filename,*a,**kw)
  Path.read_text=adapted_read;builtins.compile=adapted_compile;sys.argv=[sys.argv[0],'--task','B33_high']
  try:old.main();assert seen==['source','proposal']
  finally:Path.read_text=read;builtins.compile=compile0
  return
 assert len(sys.argv)==1;done=subprocess.run([sys.executable,'-B','-S',str(Path(__file__).resolve()),'--worker'],cwd=ROOT,text=True,capture_output=True);assert done.returncode==0,done.stderr;row=json.loads(done.stdout);row['adapted_halfside_multiplier']=json.loads(CANDIDATE.read_text(encoding='utf-8'))['halfside_multiplier'];row['bindings']={p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),CANDIDATE,ROOT/'verify/n100_B33_degree_window_stdlib.py',ROOT/'verify/n100_B33_degree_window.py',ROOT/'verify/out/n100-B33-degree-window-151.json',ROOT/'verify/out/n100-B33-degree-window-independent-153.json',ROOT/'verify/n100_remaining_branches_new_radius.py')};row['full_B33_closed']=False;row['global_bound_improved']=False
 if row['status']=='ARITHMETIC_PASS':row['result']['proposal_sha256']=sha(CANDIDATE)
 out=ROOT/'verify/out/n100-B33-high-new-K-155.json';assert not out.exists();out.write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8');print('B33 HIGH NEWK',row['status'],row['result'].get('degree5_contradiction_margin',row['result'].get('error')),flush=True)
if __name__=='__main__':main()
