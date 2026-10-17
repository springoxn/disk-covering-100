from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
i=load('verify/out/n100-local-widened-independent.json');pc=i['parent_certificate'];assert i['audit_verified'] and sha(pc['receipt'])==pc['receipt_sha256'] and sha(pc['script'])==pc['script_sha256']
paths=['verify/out/n100-first-order-rod-dual.json','verify/out/n100-fixed-rod-local-budget.json','verify/out/n100-local-augmented-audit.json','verify/out/n100-cover-hole-bridge.json','verify/out/n100-cover-bridge-review.json','verify/out/n100-local-widened-budget.json','verify/out/n100-local-widened-independent.json','verify/out/n100-local-leaf-example.json','verify/out/n100-local-leaf-check.json']
records={p:load(p) for p in paths};checked=[]
for p,obj in records.items():
 for key in ['source_sha256','sources_sha256','dependencies_sha256','inputs_sha256','binding']:
  for path,h in obj.get(key,{}).items():
   assert sha(path)==h,(p,key,path);checked.append([p,path,h])
 if 'checker_sha256' in obj:
  script={'verify/out/n100-first-order-rod-dual.json':'verify/n100_first_order_rod_dual.py','verify/out/n100-fixed-rod-local-budget.json':'verify/n100_fixed_rod_local_budget.py','verify/out/n100-local-augmented-audit.json':'verify/n100_local_augmented_audit.py','verify/out/n100-cover-hole-bridge.json':'verify/n100_cover_hole_bridge.py','verify/out/n100-cover-bridge-review.json':'verify/n100_cover_bridge_review.py','verify/out/n100-local-widened-budget.json':'verify/n100_local_widened_budget.py','verify/out/n100-local-widened-independent.json':'verify/n100_local_widened_independent.py','verify/out/n100-local-leaf-check.json':'verify/n100_local_leaf.py'}[p]
  assert sha(script)==obj['checker_sha256'];checked.append([p,script,obj['checker_sha256']])
leaf=records['verify/out/n100-local-leaf-check.json'];assert leaf['verified'] and sha(leaf['leaf_path'])==leaf['leaf_sha256']
# Completion gate requires concrete independently verified universal evidence.
required=['complete_topology_enumeration','all_m_less_than_100_excluded','all_other_graph_domains_excluded','candidate_graph_complement_excluded','degenerate_branches_closed','global_endpoint_identity','optimal_radius_irreducible_polynomial','rational_root_isolation']
missing={key:{'verified':False,'reason':'No accepted completion evidence supplied in this session.'} for key in required}
def gate(evidence):return all(evidence.get(k,{}).get('verified') is True and evidence[k].get('artifact') and evidence[k].get('independent_receipt') for k in required)
assert not gate(missing)
# reject an attempted upgrade based solely on accepted local evidence
fake=copy.deepcopy(missing);fake['global_endpoint_identity']={'verified':True,'artifact':leaf['leaf_path']}
assert not gate(fake)
out={'schema':'n100-local-chain-ledger/v1','verified_local_chain_bindings':True,'hash_links_checked':len(checked),'hash_links':checked,'local_leaf_accepted':True,'local_leaf_claim':'one small labelled center box below candidate squared radius; candidate rotation gauge need not be imposed on input','global_completion_requirements':missing,'completion_gate':False,'local_only_upgrade_rejected':True,'global_optimality':False,'minimal_polynomial_obtained':False,'artifacts_sha256':{p:sha(p) for p in paths},'checker_sha256':sha('verify/n100_local_chain_ledger.py')}
p=R/'verify/out/n100-local-chain-ledger.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('PASS local proof-chain ledger:',len(checked),'hash links; accepted one LOCAL leaf; 8 global completion requirements unfulfilled; local-only upgrade rejected')
