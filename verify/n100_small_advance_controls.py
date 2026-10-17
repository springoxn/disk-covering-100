"""Negative controls and distribution integrity for the small-radius advance."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,subprocess,ast,re
ROOT=Path(__file__).resolve().parents[1]
def main():
 folder=ROOT/'runtime/lower-small-advance-143';package=folder/'package';manifest=json.loads((folder/'transformation.json').read_text(encoding='utf-8'));radius=F(manifest['radius']);control=folder/'negative-control';assert not control.exists();control.mkdir();checks={}
 for label,code in [('optimized_mode',None),('wrong_radius_metadata',"from fractions import Fraction as F\nimport verify_B31_global_low_degree_0p11323 as m\nm.R=F(11323,100000)\nm.verify()")]:
  cmd=[sys.executable,'-B','-S','-O','working/verify_all_11323.py'] if code is None else [sys.executable,'-B','-S','-c',code];cwd=package if code is None else package/'working'
  with (control/(label+'.stdout.txt')).open('w',encoding='utf-8') as out,(control/(label+'.stderr.txt')).open('w',encoding='utf-8') as err:p=subprocess.run(cmd,cwd=cwd,stdout=out,stderr=err)
  stderr=(control/(label+'.stderr.txt')).read_text(encoding='utf-8');assert p.returncode!=0
  if code is None:assert 'Assertions must remain enabled' in stderr
  else:assert 'AssertionError' in stderr
  checks[label]={'expected_rejection':True,'exit_code':p.returncode,'stderr':stderr,'stdout_sha256':hashlib.sha256((control/(label+'.stdout.txt')).read_bytes()).hexdigest()}
 assert all(hashlib.sha256((package/rel).read_bytes()).hexdigest()==h for rel,h in manifest['copy_snapshot'].items())
 out=ROOT/'verify/out/n100-small-advance-controls-143.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-new-radius-controls/v1','status':'PASS','radius':str(radius),'checks':checks,'proof_sources_unchanged':True,'controls_only':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS optimized mode and wrong-radius metadata both rejected; proof sources unchanged',flush=True)
if __name__=='__main__':main()
