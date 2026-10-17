"""Final reviewed adapter registry, adding distribution and safe sessions.
No legacy source is activated by merely belonging to a family.
"""
from pathlib import Path
import ast,json,hashlib
from n100_unified_proof_interface_registry import ADAPTERS
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 old=json.loads((R/'verify/out/n100-unified-proof-interface-registry.json').read_text(encoding='utf-8'));adapters=old['adapters'];require=lambda x: x or (_ for _ in ()).throw(ValueError('registry binding'))
 for a in adapters:require(sha(R/a['source'])==a['sha256'])
 for ident,entry,domain,resource,premise,certificate in [
 ('annular_distribution','run','center_norm_bound_domain','annular target area','annulus contained; source domain certifies every center norm interval','n100-center-distribution-interface-contracts.json'),
 ('translated_target_distribution','run','center_rectangle_domain','translated target disk area','target inside unit disk; all center rectangles bound original domain','n100-center-distribution-interface-contracts.json'),
 ('anchor_disk_intersection','anchor_variance','explicit_disk_constraint_intersection','weighted squared distances','nonnegative radii squared and weights; graph/map lift separate','n100-center-distribution-interface-contracts.json')]:
  source=R/'verify/n100_center_distribution_interfaces.py';adapters.append({'id':ident,'source':source.relative_to(R).as_posix(),'sha256':sha(source),'entrypoint':entry,'domain':domain,'radius_units':'squared_constraints' if entry=='anchor_variance' else 'radius_upper','resource':resource,'premises':premise,'verdict_scope':'declared domain only','composition':'intersect necessary conditions; no additive area deficits','entrypoint_scope':'declared domains; use method annular_norm_counts or translated_target_counts for run','certificate':'verify/out/'+certificate})
 source=R/'verify/n100_shared_support_session.py';adapters.append({'id':'shared_support_session','source':source.relative_to(R).as_posix(),'sha256':sha(source),'entrypoint':'SupportSession.run','domain':'service_count','radius_units':'exact_U','resource':'one certified lens supports constrained and free intercept conditions','premises':'fresh constructor and current hash bindings on every call; norm-cap semantics','verdict_scope':'fixed-U necessary support only','composition':'intersection; never add overlapping deficits','certificate':'verify/out/n100-shared-support-session.json'});sources=[]
 for p in sorted((R/'verify').glob('*n100*.py')):
  tree=ast.parse(p.read_text(encoding='utf-8-sig'));sources.append({'path':p.relative_to(R).as_posix(),'sha256':sha(p),'purpose':ast.get_docstring(tree) or '', 'listed_is_not_semantic_review':True})
 disposition=R/'verify/out/n100-legacy-rule-disposition.json';require(len(json.loads(disposition.read_text(encoding='utf-8'))['legacy_sources'])==174);out=R/'verify/out/n100-final-proof-interface-registry.json';require(not out.exists());out.write_text(json.dumps({'schema':'n100-proof-interface-registry/v2','adapters':adapters,'family_contracts':'verify/out/n100-pruning-recursive-inventory-v3.json','conditional_legacy_contracts':disposition.relative_to(R).as_posix(),'conditional_legacy_gate':'n100_legacy_rule_disposition.gate','conditional_legacy_activation':'PRECONDITION_MISSING until source-specific bridges/replay supplied','current_verify_source_snapshot':sources,'proof_acceptance':'only specific registered entrypoint and its domain/premises; imported or same-family sources gain no independent authority','global_optimality':False,'bindings':{'verify/out/n100-unified-proof-interface-registry.json':sha(R/'verify/out/n100-unified-proof-interface-registry.json'),disposition.relative_to(R).as_posix():sha(disposition)},'script_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8');print('PASS final registry',len(adapters),'groups;',len(sources),'top-level sources;174 conditional legacy modules remain gated')
if __name__=='__main__':main()
