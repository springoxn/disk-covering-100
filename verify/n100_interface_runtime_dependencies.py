"""Join observed runtime reads with explicit/static dependency census.
Reads and hashes do not imply recomputation of a theorem.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,sys,platform
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 replay=R/'runtime/interface-suite-replay-130/replay.json';static=R/'verify/out/n100-interface-dependency-audit-v2.json';z=json.loads(replay.read_text(encoding='utf-8'));d=json.loads(static.read_text(encoding='utf-8'));assert z['all_nine_stages_passed'] and not z['changed_during_suite'];known={n['path'] for n in d['nodes']};rows=[]
 for rel,h in z['actual_project_read_union_sha256'].items():
  p=R/rel;assert sha(p)==h,'observed input changed';kind='bytecode_execution_snapshot' if p.suffix=='.pyc' else 'code' if p.suffix=='.py' else 'data_or_inherited_certificate' if p.suffix=='.json' else 'analytic_or_support_document';rows.append({'path':rel,'sha256':h,'kind':kind,'in_static_closure':rel in known,'used_in_stages':[s['source'] for s in z['stages'] if rel in s['actual_project_reads_sha256']],'mathematical_recomputation_authority':'not inferred from open/hash event; see each checker scope'})
 stages=[]
 for s in z['stages']:
  original=R/'verify/out'/s['output'];fresh=replay.parent/s['output'];assert sha(original)==sha(fresh)==s['output_sha256'];stages.append({'checker':s['source'],'fresh_certificate':fresh.relative_to(R).as_posix(),'saved_certificate':original.relative_to(R).as_posix(),'sha256':s['output_sha256'],'exit_code':s['exit_code'],'byte_identical':True,'trace_entries':len(s['actual_project_reads_sha256'])})
 controls=[]
 for label,bad in [('changed_hash','0'*64),('missing_hash','')]:
  assert sha(replay)!=bad;controls.append(label+'_differs_from_current_receipt')
 out=R/'verify/out/n100-interface-runtime-dependencies.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-interface-runtime-dependencies/v1','all_nine_fresh_certificates_byte_identical':True,'stages':stages,'observed_project_files':rows,'summary':{'observed_files':len(rows),'kinds':dict(Counter(r['kind'] for r in rows)),'observed_outside_static_closure':sum(not r['in_static_closure'] for r in rows),'nonbytecode_observed_outside_static_closure':sum(not r['in_static_closure'] and r['kind']!='bytecode_execution_snapshot' for r in rows),'static_files_not_observed_in_this_suite':len(known-set(z['actual_project_read_union_sha256']))},'environment':{'python':sys.version,'platform':platform.platform()},'timings_used_for_prediction':False,'scope':'runtime closure of these nine concrete checker executions; no completeness for arbitrary parameters/dynamic branches; inherited theorem computations not re-run merely by hashing','global_optimality':False,'bindings':{replay.relative_to(R).as_posix():sha(replay),static.relative_to(R).as_posix():sha(static), 'verify/run_n100_interface_suite.py':sha(R/'verify/run_n100_interface_suite.py')},'script_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8');print('PASS runtime dependency ledger',len(rows),'files;',json.dumps(Counter(r['kind'] for r in rows)),'nonbytecode new',sum(not r['in_static_closure'] and r['kind']!='bytecode_execution_snapshot' for r in rows))
if __name__=='__main__':main()
