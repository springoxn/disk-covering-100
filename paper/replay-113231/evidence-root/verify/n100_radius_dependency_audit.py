"""Independent fresh-process dependency/radius replay of a transformed package."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,subprocess,sys,os,time,argparse
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--tag',default='143');a=ap.parse_args();folder=ROOT/f'runtime/lower-small-advance-{a.tag}';package=folder/'package';manifest_path=folder/'transformation.json';manifest=json.loads(manifest_path.read_text(encoding='utf-8'));radius=F(manifest['radius']);original=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';assert all(sha(original/rel)==h for rel,h in manifest['source_snapshot'].items());assert all(sha(package/rel)==h for rel,h in manifest['copy_snapshot'].items());logs=folder/'independent-radius-trace';assert not logs.exists();logs.mkdir();tracer=ROOT/'verify/n100_radius_process_trace.py';env=dict(os.environ,N100_AUDIT_PACKAGE=str(package));start=time.perf_counter_ns()
 with (folder/'audit.stdout.json').open('w',encoding='utf-8') as out,(folder/'audit.stderr.txt').open('w',encoding='utf-8') as err:done=subprocess.run([sys.executable,'-B','-S',str(tracer),str(logs),'working/verify_all_11323.py'],cwd=package,env=env,stdout=out,stderr=err)
 processes=[json.loads(p.read_text(encoding='utf-8')) for p in logs.glob('process-*.json')];entries=[e for p in processes for e in p['verifier_entries']];loaded={rel:h for p in processes for rel,h in p['loaded_package_modules'].items()};assert all(manifest['copy_snapshot'][rel]==h for rel,h in loaded.items());assert all(sha(package/rel)==h for rel,h in manifest['copy_snapshot'].items());result=None;table={}
 if done.returncode==0:
  result=json.loads((folder/'audit.stdout.json').read_text(encoding='utf-8'));assert result['status']=='PASS'
  for branch in ('B31','B32','B33','B34','B35','B36plus'):
   row=result[branch]['result'];assert F(row['radius'])==radius;key=next(k for k in ('minimum_area_margin','minimum_reported_area_margin','minimum_area_margin_at_B36') if k in row);assert F(row[key])>0;table[branch]={'radius':row['radius'],'margin':row[key],'source':result[branch]['source']}
 # Entries declaring R are reported for manual context review; theorem-independent
 # scalar sample checks may legitimately use other radii.
 differences=[e for e in entries if 'R' in e['parameters'] and F(e['parameters']['R'])!=radius];receipt={'schema':'n100-radius-dependency-audit/v1','radius':str(radius),'exit_code':done.returncode,'elapsed_ns':time.perf_counter_ns()-start,'process_count':len(processes),'loaded_source_count':len(loaded),'loaded_source_sha256':loaded,'all_loaded_sources_bound_to_transformation_manifest':True,'entries':entries,'entries_with_other_global_R':differences,'branch_margins':table,'all_branches_replayed':done.returncode==0,'geometric_transfer_review_pending':True,'global_bound_improved':False,'bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),tracer,manifest_path,folder/'audit.stdout.json',folder/'audit.stderr.txt')}};out=ROOT/f'verify/out/n100-radius-dependency-audit-{a.tag}.json';assert not out.exists();out.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print('DEPENDENCY AUDIT EXIT',done.returncode,'processes',len(processes),'sources',len(loaded),'other R entries',len(differences),flush=True)
if __name__=='__main__':main()
