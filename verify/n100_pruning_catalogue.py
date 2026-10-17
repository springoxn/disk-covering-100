"""Fail-closed catalogue census and historical-artifact quarantine.

Family tags locate code; they never authorize a new proof interface.
"""
from pathlib import Path
from collections import Counter
import ast,json,hashlib
R=Path(__file__).resolve().parents[1]
# Artifact-level invalidation: current scripts may also generate corrected versions.
WITHDRAWN={
 'verify/out/n100-boundary-annulus-boxes-v2.json':('paired-dart owner bug; empty boundary set','verify/out/n100-boundary-owner-correction.json'),
 'verify/out/n100-boundary-annulus-independent.json':('replays the same invalid empty owner set','verify/out/n100-boundary-owner-correction-independent.json'),
 'verify/out/n100-boundary-annulus-full.json':('paired-dart owner bug; empty boundary set','verify/out/n100-boundary-owner-correction.json'),
 'verify/out/n100-boundary-annulus-full-independent.json':('replays the same invalid empty owner set','verify/out/n100-boundary-owner-correction-independent.json'),
 'verify/out/n100-axis-coownership-chord-full-v2.json':('false all4776 exclusions; corrected v3 excludes0','verify/out/n100-axis-coownership-chord-full-v3.json'),
}
REVIEWED={
 'n100_separated_witness_hall':'separated_hall',
 'n100_nonseparated_capacity_cut':'small_pool_capacity',
 'n100_box_aware_capacity':'box_aware_patterns',
 'n100_weighted_witness_capacity':'weighted_capacity',
 'n100_hall_automatic_search':'automatic_hall',
 'n100_hybrid_local_tree':'local_root_box',
}
FAMILIES=[
 ('proof_plumbing',('proof_interface','pruning_source_inventory','pruning_catalogue','stage','evidence_ledger','audit_inputs'),'protocol','none','no geometric verdict'),
 ('counterexamples_controls',('counterexample','disconnected_boundary','negative_witness','angular_energy','finite_grid','integer_relaxation','dual_limit','obstruction_independent','rational_controls','interface_controls'),'control','varies','reject false rules; no positive feasibility transfer'),
 ('local_theorem_transfer',('first_order_rod','full_circumcenter','simplex_lift','boundary_pair_intersections','local_','kkt','cover_bridge','cover_hole','cover_transfer','midpoint_box','widened_center','widened_budget','lifting','gauge'),'local_box','squared','requires certified local theorem, transfer bridge and label/gauge binding'),
 ('weighted_capacity',('weighted_witness',),'center_box','squared','nonnegative rational weights; per-center admitted patterns overapproximate service'),
 ('box_patterns',('box_aware','candidate_pattern','expanded_hole'),'center_box','squared','mean-energy pattern relaxation plus exact union DP; source-derived pools not complete geometry'),
 ('hall_witness_tree',('hall','global_witness','hybrid_','witness_calibration'),'center_box_or_tree','squared','strictly separated pool for Hall; verify full root/splits separately'),
 ('small_pool_capacity',('nonseparated_capacity',),'center_box','squared','finite target pool, pair/triple circle tests; strict capacity deficit'),
 ('multiradius_profiles',('multiradius',),'radial_type_count_domain','radius','multiple target lens budgets; reweighted relaxation witness is not a cover'),
 ('continuous_spatial_tree',('spatial_',),'continuous_box_or_tree','radius','full inherited parent coverage and exact splits; finite support union needs domain binding'),
 ('voronoi_contractors',('voronoi_',),'same_map_continuous_box','squared','nearest-site and bisector equalities conditional on declared diagram; interval contractions keep all solutions'),
 ('arc_cap_lens',('arc_cap','arc_lens','boundary_lens'),'radial_count_domain','radius','arc/lens budgets and intercept supports; no double allocation'),
 ('ear_topology',('_ear','m99_boundary_representatives'),'boundary_word_or_count_domain','radius','same normalized diagram and distinct B cells; ear triangles and packing semantics'),
 ('recursive_radius_counts',('recursive_','radius_count','radius_local','inner_radial','annular_center','directional_center'),'count_domain_or_center_box','radius','inner disk normalization; directional test domain and independent coverage explicit'),
 ('boundary_count_area',('serving_count','boundary_count','boundary_interior','cap_area','cap_frontier','sharp_envelope','strengthened','count_domain','lowerbound','longchord'),'count_domain','radius','B distinct cells differs from k circle servers; longchord remains conditional'),
 ('axis_core_geometry',('axis_','boundary_annulus','boundary_owner'),'fixed_core_placement','radius','fixed-core only; corrected paired-dart ownership; retain equality'),
 ('shared_center_geometry',('shared_vertex','circle_center','boundary_circle','center_spatial'),'continuous_box','radius','necessary interval constraints over inherited same map; unresolved is not feasible'),
 ('finite_arc_constraint_learning',('arc_','boundary_arc','boundary_order'),'finite_tiles_with_parent_box','radius','finite relaxation order/nogoods conditional on parent; finite supports project via proved inclusion'),
 ('map_compilation_enumeration',('one_interior','dart','cubic','map_','face_axis','quadratic_cover','clipped_map','topology_audit','expanded_map','generic_strict'),'combinatorial_map_or_polynomial','varies','parallel darts preserved; bounded enumeration is not full global maps'),
 ('cover_upper_certificate',('coverage','lattice97','upperbound','real_algebraic_endpoint'),'fixed_configuration','radius','upper covering proof, not lower-bound pruning'),
 ('discovery_diagnostics',('contact_direction','run_'),'driver_or_probe','none','do not interpret discovery failure as infeasibility'),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def family(stem):
 for ident,terms,obj,units,premise in FAMILIES:
  if any(t in stem for t in terms):return ident
 return 'unclassified_review_required'
def policy(rel,digest,quarantine):
 rel=str(rel).replace('\\','/')
 if rel in quarantine:return {'decision':'QUARANTINED','reason':quarantine[rel]['reason']}
 for entry in quarantine.values():
  if digest==entry['sha256']:return {'decision':'QUARANTINED','reason':'content alias of withdrawn artifact'}
 return {'decision':'UNREVIEWED','reason':'absence from quarantine is not proof acceptance'}
def main():
 quarantine={p:{'sha256':sha(R/p),'reason':why,'replacement':replacement,'replacement_sha256':sha(R/replacement)} for p,(why,replacement) in WITHDRAWN.items()};rows=[]
 for p in sorted((R/'verify').glob('*.py')):
  if 'n100' not in p.stem:continue
  tree=ast.parse(p.read_text(encoding='utf-8-sig'));stem=p.stem;fam=family(stem);functions=[n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))];doc=ast.get_docstring(tree) or ''
  if stem in REVIEWED:role='reviewed_callable'
  elif any(t in stem for t in ('independent','audit','ledger')):role='independent_replay_or_audit'
  elif fam=='counterexamples_controls':role='control_or_counterexample'
  elif fam in ('proof_plumbing','discovery_diagnostics'):role='plumbing_or_driver'
  else:role='method_or_helper_review_required'
  refs=sorted({n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.endswith('.json') and '\n' not in n.value and len(n.value)<350});rows.append({'script':str(p.relative_to(R)).replace('\\','/'),'sha256':sha(p),'family_locator':fam,'family_tag_authority':'locator_only; semantic review required','role':role,'interface_id':REVIEWED.get(stem),'eligible_for_composition':stem in REVIEWED,'eligibility_scope':'only corresponding verified callable contract; not arbitrary legacy main() outputs' if stem in REVIEWED else 'disabled pending semantic review','docstring':doc,'functions':functions,'json_literal_candidates':refs})
 names=[r['script'] for r in rows];assert len(names)==len(set(names));assert set(REVIEWED)<={Path(n).stem for n in names};tests=[]
 for path,e in quarantine.items():
  assert policy(path,e['sha256'],quarantine)['decision']=='QUARANTINED';assert policy('verify/out/renamed-copy.json',e['sha256'],quarantine)['decision']=='QUARANTINED';tests.extend([path,'hash-alias:'+path])
 assert policy('verify/out/unknown.json','0'*64,quarantine)['decision']=='UNREVIEWED';assert policy('verify/out/n100-axis-coownership-chord-full-v3.json',sha(R/'verify/out/n100-axis-coownership-chord-full-v3.json'),quarantine)['decision']=='UNREVIEWED'
 # A legacy verified:true flag must never override a withdrawal.
 bad=json.loads((R/'verify/out/n100-axis-coownership-chord-full-v2.json').read_text(encoding='utf-8'));good=json.loads((R/'verify/out/n100-axis-coownership-chord-full-v3.json').read_text(encoding='utf-8'));assert bad['verified'] and bad['excluded_count']==4776 and good['excluded_count']==0
 out=R/'verify/out/n100-pruning-catalogue-v3.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-pruning-catalogue/v3','scope':'all current top-level verify Python filenames containing n100; nested runtime/lit/tool scripts not censused; tags are discovery locators, not completed semantic audits','script_count':len(rows),'family_counts':dict(Counter(r['family_locator'] for r in rows)),'role_counts':dict(Counter(r['role'] for r in rows)),'family_contract_locators':[{'id':i,'input_family':o,'radius_units':u,'premise_to_review':p,'activation':'reviewed leaf adapters only; otherwise disabled'} for i,t,o,u,p in FAMILIES],'scripts':rows,'quarantine':quarantine,'quarantine_controls':tests,'unknown_and_corrected_artifacts_require_review':True,'legacy_verified_true_does_not_override_withdrawal':True,'global_optimality':False,'script_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8');print('PASS catalogue',len(rows),'scripts;',len(REVIEWED),'reviewed callable sources;',len(quarantine),'quarantined artifacts;',len(tests),'path/hash rejection tests');print('FAMILIES',dict(Counter(r['family_locator'] for r in rows)));print('UNCLASSIFIED',[r['script'] for r in rows if r['family_locator']=='unclassified_review_required'])
if __name__=='__main__':main()
