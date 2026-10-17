"""Audit bridge for a fresh full-output-equivalence execution receipt.
This checks receipt coverage and current hashes; mathematical premises stay inherited.
Use the full revalidation program to reproduce arithmetic, not this lightweight gate.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,copy
import n100_interface_dependency_audit as D
R=Path(__file__).resolve().parents[1]
RECEIPT='verify/out/n100-boundary-circle-full-revalidation.json'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_bridge(z):
 need(z['schema']=='n100-boundary-circle-full-revalidation/v1','receipt schema');need(z['all4776_primary_independent_and_historical_outputs_identical'] is True,'missing complete replay claim');need(z['script_sha256']==sha(R/'verify/n100_boundary_circle_full_revalidation.py'),'receipt source hash')
 for path,h in z['bindings'].items():
  p=D.resolve(path);need(p is not None and p.is_file() and sha(p)==h,'changed receipt dependency')
 oldpath='verify/out/n100-boundary-circle-full.json';need(z['historical_artifact_sha256']==sha(R/oldpath),'historical artifact binding');old=json.loads((R/oldpath).read_text(encoding='utf-8'));source='verify/n100_boundary_circle_propagation.py';mismatches=[]
 for path,h in old['bindings'].items():
  if sha(R/path)!=h:mismatches.append({'path':Path(path).as_posix(),'old_sha256':h,'current_sha256':sha(R/path)})
 need(len(mismatches)==1 and mismatches[0]['path']==source and z['source_mismatch_bridge']==mismatches,'bridge must cover exact sole mismatch')
 expected={tuple(r['placement']):r for r in old['results']};prior=json.loads((R/'verify/out/n100-axis-coupled-boxes.json').read_text(encoding='utf-8'));domain={tuple(r['placement']) for r in prior['retained']};rows=z['results'];need(len(rows)==4776 and len({tuple(r['placement']) for r in rows})==4776 and domain==set(expected)=={tuple(r['placement']) for r in rows},'complete unique placement domain')
 for r in rows:
  e=expected[tuple(r['placement'])];need(all(r[k]==e[k] for k in ('full_result_sha256','excluded','sweeps')),'historical result coverage mismatch')
 need(z['histogram']==old['histogram'],'histogram agreement');return {'artifact':oldpath,'source':source,'old_source_sha256':mismatches[0]['old_sha256'],'current_source_sha256':mismatches[0]['current_sha256'],'receipt':RECEIPT,'receipt_sha256':sha(R/RECEIPT),'placements':4776,'scope':'saved execution receipt coverage and snapshot hashes; arithmetic reproduced by separate full dual-implementation run','analytic_geometry_reproved':False}

def main():
 p=R/RECEIPT;z=json.loads(p.read_text(encoding='utf-8'));bridge=check_bridge(z);audit=D.audit(D.ROOTS);unbridged=[]
 for issue in audit['issues']:
  if issue.get('source')==bridge['artifact'] and issue.get('target')==bridge['source'] and issue['kind']=='HASH_MISMATCH':issue['resolution']='BRIDGED_BY_FRESH_ALL4776_OUTPUT_EQUIVALENCE_RECEIPT'
  else:unbridged.append(issue)
 need(not unbridged,'new unbridged dependency issue');controls=[]
 for label,change in [('missing_placement',lambda q:q['results'].pop()),('duplicate_placement',lambda q:q['results'].__setitem__(1,q['results'][0])),('false_result_digest',lambda q:q['results'][0].update(full_result_sha256='0'*64)),('wrong_source_bridge',lambda q:q['source_mismatch_bridge'][0].update(current_sha256='0'*64))]:
  bad=copy.deepcopy(z);change(bad)
  try:check_bridge(bad)
  except ValueError:controls.append(label)
  else:raise AssertionError(label)
 audit.update(schema='n100-interface-dependency-bridged-audit/v1',bridges=[bridge],unbridged_issues=unbridged,bridge_negative_controls=controls,scope='explicit/static dependency audit with a fresh full-output revalidation receipt; complete dynamic/analytic dependency closure still pending',global_optimality=False,script_sha256=sha(Path(__file__)))
 for r in audit['root_dependency_states']:
  if r['known_invalid_dependencies']:r['binding_gate']='BRIDGED_EXPLICIT_BINDING_ERROR; original historical hash unchanged'
 out=R/'verify/out/n100-interface-dependency-bridged-audit.json';need(not out.exists(),'overwrite');out.write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8');print('PASS bridged dependency audit;4776 receipts;0 unbridged issues;controls',len(controls))
if __name__=='__main__':main()
