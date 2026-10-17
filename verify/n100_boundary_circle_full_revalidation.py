"""Full output-equivalence revalidation for a stale historical source binding.
Does not modify old certificates. Timing telemetry never affects acceptance.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,time
from n100_boundary_circle_propagation import run
from n100_boundary_circle_independent import replay
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def main():
 cp=R/'verify/out/n100-cubic-core-roundtrip.json';bp=R/'verify/out/n100-axis-coupled-boxes.json';sp=R/'verify/out/n100-boundary-circle-full.json';pp=R/'verify/out/n100-axis-dual-chain-pruning.json';script=R/'verify/n100_boundary_circle_propagation.py';ind=R/'verify/n100_boundary_circle_independent.py'
 paths=[cp,bp,sp,pp,script,ind,R/'verify/n100_axis_coupled_boxes.py',R/'verify/n100_axis_coupled_boxes_independent.py'];bindings={p.relative_to(R).as_posix():sha(p) for p in paths};core=json.loads(cp.read_text(encoding='utf-8'))['core'];prior=json.loads(bp.read_text(encoding='utf-8'));old=json.loads(sp.read_text(encoding='utf-8'));frontier=json.loads(pp.read_text(encoding='utf-8'));records={tuple(r['placement']):r for r in old['results']};domain={tuple(r['placement']) for r in prior['retained']};need(len(domain)==len(prior['retained'])==4776 and domain==set(records)==set(map(tuple,frontier['retained_axis_edge_placements'])),'full placement identity')
 mismatch=[]
 for path,h in old['bindings'].items():
  if sha(R/path)!=h:mismatch.append({'path':Path(path).as_posix(),'old_sha256':h,'current_sha256':sha(R/path)})
 need(len(mismatch)==1 and mismatch[0]['path']==script.relative_to(R).as_posix(),'only intended stale binding may differ');rows=[];hist=Counter();start=time.perf_counter_ns();primary_ns=independent_ns=0
 for num,row in enumerate(prior['retained'],1):
  tick=time.perf_counter_ns();result=run(core,row['placement'],row['boxes']);primary_ns+=time.perf_counter_ns()-tick;tick=time.perf_counter_ns();alt,w=replay(core,row['placement'],row['boxes']);independent_ns+=time.perf_counter_ns()-tick;need(result==alt,'independent full output mismatch');expected=records[tuple(row['placement'])];actual=digest(result);need(actual==expected['full_result_sha256'],'historical full output drift');need(result['excluded']==expected['excluded'] and result['sweeps']==expected['sweeps'],'status/sweep');rows.append({'placement':row['placement'],'full_result_sha256':actual,'excluded':result['excluded'],'sweeps':result['sweeps']});hist['excluded' if result['excluded'] else 'fixed' if result['fixed'] else 'capped']+=1
  if num%256==0:print('PROGRESS',num,'/',len(domain),dict(hist),'elapsed_seconds',round((time.perf_counter_ns()-start)/10**9),flush=True)
 need(all(sha(R/path)==h for path,h in bindings.items()),'inputs changed during full replay');out=R/'verify/out/n100-boundary-circle-full-revalidation.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-full-revalidation/v1','all4776_primary_independent_and_historical_outputs_identical':True,'placement_domain_identity_verified':True,'source_mismatch_bridge':mismatch,'historical_artifact_sha256':bindings[sp.relative_to(R).as_posix()],'results':rows,'histogram':dict(hist),'timing_telemetry_ns':{'primary':primary_ns,'independent':independent_ns,'whole_scan':time.perf_counter_ns()-start},'scope':'fresh all-placement fixed-core output equivalence; replacement receipt for only one stale source binding; no full map enumeration or new geometry theorem','geometry_premises':'inherited fixed-core/axis/quadrant incidence necessity; primary and independent interval arithmetic replayed for all4776','global_optimality':False,'bindings':bindings,'script_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8');print('PASS all4776 full revalidation',dict(hist),flush=True)
if __name__=='__main__':main()
