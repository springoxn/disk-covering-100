"""Targeted diagnosis only: stale full-scan source binding is NOT repaired here."""
from pathlib import Path
import json,hashlib
from n100_boundary_circle_propagation import run
from n100_boundary_circle_independent import replay
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 cp=R/'verify/out/n100-cubic-core-roundtrip.json';bp=R/'verify/out/n100-axis-coupled-boxes.json';sp=R/'verify/out/n100-boundary-circle-full.json';core=json.loads(cp.read_text(encoding='utf-8'))['core'];prior=json.loads(bp.read_text(encoding='utf-8'))['retained'];old=json.loads(sp.read_text(encoding='utf-8'));records={tuple(r['placement']):r for r in old['results']};selected=[prior[0],prior[len(prior)//2],next(r for r in prior if r['placement']==[30,6,14,22])];rows=[]
 for row in selected:
  result=run(core,row['placement'],row['boxes']);alt,w=replay(core,row['placement'],row['boxes']);assert result==alt;expected=records[tuple(row['placement'])]['full_result_sha256'];actual=digest(result);rows.append({'placement':row['placement'],'primary_equals_independent':True,'saved_full_result_digest_matches':actual==expected,'expected_result_sha256':expected,'actual_result_sha256':actual,'excluded':result['excluded']});print('SAMPLE',row['placement'],'saved match',actual==expected,flush=True)
 script=R/'verify/n100_boundary_circle_propagation.py';expected=next(h for p,h in old['bindings'].items() if Path(p).name==script.name);out=R/'verify/out/n100-dependency-stale-binding-diagnosis.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-dependency-stale-binding-diagnosis/v1','source_binding_mismatch':{'expected':expected,'actual':sha(script)},'samples':rows,'sample_count':len(rows),'full_scan_count':len(prior),'full_dependency_chain_accepted':False,'scope':'three targeted arithmetic replays; sample agreement does not repair historical source hashes or certify unsampled placements','global_optimality':False,'bindings':{str(p.relative_to(R)):sha(p) for p in [cp,bp,sp,script,R/'verify/n100_boundary_circle_independent.py']},'script_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8');print('PASS diagnostic only;full historical binding remains invalid')
if __name__=='__main__':main()
