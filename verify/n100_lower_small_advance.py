"""Uniform small-radius advance in isolated complete release copy.
All upstream assertions and fixed supports retained; original release immutable.
"""
from pathlib import Path
from fractions import Fraction as F
import json,re,shutil,hashlib,subprocess,sys,time,argparse
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--numerator',type=int,default=1132301);ap.add_argument('--denominator',type=int,default=10000000);ap.add_argument('--tag',default='142');a=ap.parse_args();target=F(a.numerator,a.denominator);assert F(11323,100000)<target<F(11324,100000);folder=ROOT/f'runtime/lower-small-advance-{a.tag}';assert not folder.exists();folder.mkdir(parents=True);copy=folder/'package';shutil.copytree(SOURCE,copy,ignore=shutil.ignore_patterns('__pycache__'));before={p.relative_to(SOURCE).as_posix():sha(p) for p in SOURCE.rglob('*') if p.is_file() and '__pycache__' not in p.parts};changes=[]
 for relative in before:
  path=copy/relative
  if path.suffix not in ('.py','.json'):continue
  text=path.read_text(encoding='utf-8');new,n=re.subn(r'F\(\s*11323\s*,\s*100000\s*\)',f'F({target.numerator},{target.denominator})',text);string_count=new.count('11323/100000');new=new.replace('11323/100000',str(target))
  if new!=text:
   path.write_text(new,encoding='utf-8',newline='');changes.append({'path':relative,'old_sha256':before[relative],'new_sha256':sha(path),'exact_radius_literal_replacements':n,'rational_radius_string_replacements':string_count})
 transformed={rel:sha(copy/rel) for rel in before};(folder/'transformation.json').write_text(json.dumps({'radius':str(target),'source_snapshot':before,'copy_snapshot':transformed,'changes':changes,'rule':'only exact Fraction baseline radius11323/100000 and rational-string radius occurrences replaced; filenames and all fixed-row supports unchanged'},indent=2)+'\n',encoding='utf-8');start=time.perf_counter_ns()
 with (folder/'stdout.json').open('w',encoding='utf-8') as out,(folder/'stderr.txt').open('w',encoding='utf-8') as err:done=subprocess.run([sys.executable,'-B','-S','working/verify_all_11323.py'],cwd=copy,stdout=out,stderr=err)
 assert all(sha(SOURCE/rel)==h for rel,h in before.items());assert all(sha(copy/rel)==h for rel,h in transformed.items());receipt={'schema':'n100-uniform-small-radius-advance/v1','radius':str(target),'exit_code':done.returncode,'elapsed_ns':time.perf_counter_ns()-start,'upstream_unchanged':True,'transformed_copy_unchanged_during_replay':True,'changed_files':len(changes),'transformation_manifest_sha256':sha(folder/'transformation.json'),'stdout_sha256':sha(folder/'stdout.json'),'stderr_sha256':sha(folder/'stderr.txt'),'script_sha256':sha(Path(__file__)),'all_six_branch_arithmetic_closed':False,'global_bound_improved':False}
 if done.returncode==0:
  result=json.loads((folder/'stdout.json').read_text(encoding='utf-8'));assert result['status']=='PASS' and result['theorem']=='r_D(100)>'+str(target);assert result['complete_surviving_boundary_counts']==list(range(31,40));assert all(result[k]['result']['radius']==str(target) for k in ('B31','B32','B33','B34','B35','B36plus'));receipt['all_six_branch_arithmetic_closed']=True;receipt['result']=result;receipt['pending']='independent same-radius dependency, arithmetic and geometric transfer review before accepting stronger global theorem'
 else:receipt['stderr_tail']=(folder/'stderr.txt').read_text(encoding='utf-8')[-12000:]
 out=ROOT/f'verify/out/n100-lower-small-advance-{a.tag}.json';assert not out.exists();out.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print('UNIFORM ADVANCE',str(target),'exit',done.returncode,'six branch arithmetic',receipt['all_six_branch_arithmetic_closed'],flush=True)
if __name__=='__main__':main()
