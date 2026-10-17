"""Independent structural/source-binding checks of recursive inventory.
This deliberately does not turn family templates into theorem verification.
"""
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib,copy,ast
from n100_unified_proof_interface_registry import ADAPTERS
from n100_pruning_catalogue import WITHDRAWN
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(x,m):
 if not x:raise ValueError(m)
def check(z):
 active=defaultdict(list)
 for row in ADAPTERS:active['verify/'+row[1]].append(row[2])
 active['verify/n100_shared_support_session.py'].append('SupportSession.run');rows=z['sources'];paths=[r['source'] for r in rows];require(len(paths)==len(set(paths)),'duplicate source');groups=defaultdict(list);byfamily=defaultdict(list)
 for r in rows:
  p=R/r['source'];require(p.resolve().is_relative_to(R) and p.is_file(),'source path');require(sha(p)==r['sha256'],'source hash');groups[r['sha256']].append(r['source']);byfamily[r['family_contract']].append(r['source']);require(r['registered_entrypoints']==active.get(r['source'],[]),'unauthorized activation');require((r['role']=='REGISTERED_ADAPTER_ONLY')==bool(r['registered_entrypoints']),'role activation disagreement');require(r['source_specific_semantics_independently_reviewed'] is False,'unearned semantic review');tree=ast.parse(p.read_text(encoding='utf-8-sig'));require(r['public_functions']==[n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))],'AST surface mismatch')
 expected={h:sorted(v) for h,v in groups.items() if len(v)>1};given={g['sha256']:sorted(g['paths']) for g in z['source_content_aliases']};require(expected==given,'content alias partition');families=z['family_contracts'];require(len(families)==20 and len({f['family'] for f in families})==20,'family count')
 for f in families:
  require(sorted(f['member_sources'])==sorted(byfamily[f['family']]),'family member missing');require(all(f[k] for k in ('domain','radius_units','resource','required_premises','certificate','composition')),'incomplete contract');require(f['family_locator_is_activation_authority'] is False and f['additive_by_default'] is False,'unsafe composition authority')
 require(set(byfamily)<=set(f['family'] for f in families),'unknown family');require(z['mathematical_verdict'] is None and z['global_optimality'] is False,'false mathematical verdict');require(set(q['path'] for q in z['withdrawn_artifacts'])==set(WITHDRAWN),'withdrawn set missing')
 for q in z['withdrawn_artifacts']:require(sha(R/q['path'])==q['sha256'],'withdrawn hash');require(q['reason']==WITHDRAWN[q['path']][0],'withdrawal reason')
 return {'source_paths':len(rows),'unique_source_contents':len(groups),'family_contracts':len(families),'alias_groups':len(expected),'registered_adapter_modules':sum(bool(r['registered_entrypoints']) for r in rows),'conditional_legacy_modules':sum(r['role']=='LEGACY_SOURCE_CONTRACT_REVIEW_REQUIRED' for r in rows)}
def main():
 source=R/'verify/out/n100-pruning-recursive-inventory-v3.json';z=json.loads(source.read_text(encoding='utf-8'));summary=check(z);controls=[]
 for label,change in [('false_hash',lambda b:b['sources'][0].update(sha256='0'*64)),('duplicate_source',lambda b:b['sources'].append(copy.deepcopy(b['sources'][0]))),('unearned_activation',lambda b:b['sources'][0].update(registered_entrypoints=['main'])),('unearned_semantic_review',lambda b:b['sources'][0].update(source_specific_semantics_independently_reviewed=True)),('missing_family_member',lambda b:next(f for f in b['family_contracts'] if f['member_sources'])['member_sources'].pop()),('false_additive_budget',lambda b:b['family_contracts'][0].update(additive_by_default=True))]:
  bad=copy.deepcopy(z);change(bad)
  try:check(bad)
  except ValueError:controls.append(label)
  else:raise AssertionError(label)
 out=R/'verify/out/n100-pruning-recursive-inventory-controls.json';require(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-pruning-recursive-inventory-controls/v1','structural_and_source_bindings_verified':summary,'rejected_controls':controls,'mathematical_verdict':None,'scope':'metadata/activation/alias/source consistency, not reproof of174 conditional legacy modules','bindings':{source.relative_to(R).as_posix():sha(source),'verify/n100_pruning_recursive_inventory.py':sha(R/'verify/n100_pruning_recursive_inventory.py')},'script_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8');print('PASS recursive inventory controls',json.dumps(summary),'rejected',len(controls))
if __name__=='__main__':main()
