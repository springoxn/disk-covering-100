"""Recursive source/contract inventory. Locator matches never activate proofs."""
from pathlib import Path
from collections import Counter,defaultdict
import ast,json,hashlib
from n100_pruning_catalogue import FAMILIES,WITHDRAWN,family
from n100_unified_proof_interface_registry import ADAPTERS,OVERRIDES
R=Path(__file__).resolve().parents[1]
# Family-level proof obligations. Unreviewed sources remain disabled even if
# they locate to a family with an executable representative adapter.
DETAIL={
'proof_plumbing':('protocol','none','no geometric resource','schema/hash/replay checks only','no mathematical verdict','metadata or trace'),
'counterexamples_controls':('control instance','declared','none','exact counterexample or mutation target','reject false transfers; never positive feasibility','exact witness or rejected mutation'),
'local_theorem_transfer':('specified center box','squared','one local theorem domain','certified theorem chain; labels; rational orthogonal frame; strict endpoint','same box intersection only; no global lift without root tree','LOCAL chain and corner inclusion'),
'weighted_capacity':('center box and nonnegative weighted target pool','squared','finite target service weight','all admitted patterns overapproximate service; exact strict deficit','intersect only; do not add deficits','independent per-center weighted maxima'),
'box_patterns':('center box and finite target pool','squared','finite target assignment','mean/variance obstruction necessary; retained pattern union overapproximates service','intersect; survival is not a cover','all necessary pattern eliminations and finite union DP'),
'hall_witness_tree':('center box or complete split tree','squared','separated finite target assignment','strict pair separation; conservative adjacency; LOCAL has extra theorem premise','one box exclusion; global only after all root/split leaves replay','Hall deficiency/matching or complete node receipts'),
'small_pool_capacity':('center box and bounded target pool','squared','finite target assignment','closed pair/triple tests; exact upper capacities; strict sum deficit','intersect only; radius equality retained','explicit MEC/Gram independent pattern checks'),
'multiradius_profiles':('fixed radial-type multiplicity vector','exact radius U','target-area and circle-arc budgets','fixed distances; multiplicities sum100; Darboux lens bounds','each target necessary; deficits not added across overlapping targets','all slab heights/partitions and arc-series checks'),
'continuous_spatial_tree':('closed real box tree','context-bound','whole parent solution domain','closed child union covers parent; original constraints replayed; every leaf addressed','global only if no unresolved leaves','unique nodes, exact splits, contraction/leaf traces'),
'voronoi_contractors':('same-map real center/vertex boxes','context-bound squared constraints','necessary equations','Voronoi ownership bridge; nonzero denominator for division; singular interval retained','intersect necessary contractions on identical parent','exact outward interval/fraction endpoint receipts'),
'arc_cap_lens':('normalized distinct circle-serving count domain','exact radius U','circle arcs and inner area','norm-cap normalization; arc monotonicity; Darboux envelope; source chain','affine support replaces support; no additive shared area','segment/slab replays; positive area gap'),
'ear_topology':('normalized boundary word or actual-ear count domain','radius','actual disjoint marked ear area','B distinct cells; tip-overlap step2; disjoint packing; actual ears not free decoration','marked joint budget replaces kappa; decoration lift preserves parent','exact packing/word enumeration plus scalar replay'),
'recursive_radius_counts':('normalized count domain with recursive inner target','radius','inner-disk coverage and joint area','recursive normalization; all inner boundary counts; monotone radius/service transfer explicitly scoped','domain filtering; conditional frontier cannot become unconditional','all scalar exclusions at certified endpoint'),
'boundary_count_area':('effective m, distinct B cells, distinct k servers','radius','joint area/perimeter necessities','B<=k<=m<=100; longchord conditional; independent normalization lemmas','same-domain intersection; no B=k assumption','exact scalar bounds and complete saved count set'),
'axis_core_geometry':('one declared fixed core and placement domain','explicit per artifact','fixed-core necessary incidence','correct paired-dart owners; complete placement-domain chain; axis subdivisions are not B','no full-map transfer; withdrawn artifact paths/hashes rejected','integer incidence/ownership and placement replay'),
'shared_center_geometry':('same fixed-map continuous real boxes','context-bound','necessary distance/circle constraints','corrected562 incidences; same parent/frame/radius; outward rounding','empty excludes declared system; nonempty remains unresolved','primitive replay and complete node domain trace'),
'finite_arc_constraint_learning':('finite tiles with exact continuous parent','context-bound','finite relaxation assignments','ordered cycle includes prefix state; nogoods proved on same parent/tiles','finite support only; continuous projection needs bridge','independent cycle support/oracle; parent-bound conflict trace'),
'map_compilation_enumeration':('dart map or explicitly bound polynomial domain','explicit radius or squared t','one declared map/domain','parallel darts; face links/Euler/connectedness; all-map enumeration separate; justified substitutions','one-map SOS refutation does not cover other maps','compiled polynomials or exact negative-one identity'),
'cover_upper_certificate':('one fixed configuration','radius','union coverage of unit disk','exact endpoint/configuration; independent union coverage','upper bound only, no lower-bound exclusion','coverage certificate and configuration bindings'),
'discovery_diagnostics':('driver/probe/search candidate','none','none','numeric/search failure is not infeasibility','no proof acceptance without separate exact checker','logs or candidate only')}
EXTRA={'n100_shared_support_session':'arc_cap_lens','n100_interface_timing_calibration':'proof_plumbing','n100_interface_runtime_dependencies':'proof_plumbing','n100_pruning_recursive_inventory':'proof_plumbing'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def locator(p):
 stem=p.stem;rel=p.relative_to(R).as_posix()
 if p.name=='verify_extension.py' and 'certified_bounds_11323' in rel:return 'recursive_radius_counts'
 if rel=='proofs/n100_geometry_check.py':return 'counterexamples_controls'
 if rel=='runtime/candidates-n100/make_candidates_n100.py':return 'cover_upper_certificate'
 if rel.startswith('_recon/') or any(t in stem for t in ('cooperative','refine','polish','stationarity','sqp','server','pilot','_probe','_contact_lp','active_contact_analysis')):return 'discovery_diagnostics'
 if stem in EXTRA:return EXTRA[stem]
 if stem in OVERRIDES:return OVERRIDES[stem]
 f=family(stem)
 if f=='unclassified_review_required' and ('interface_' in stem or 'shared_support' in stem):return 'proof_plumbing'
 return f

def main():
 listing=R/'verify/out/n100-recursive-source-paths-133.txt';observed=R/'verify/out/n100-interface-runtime-dependencies.json';runtime=json.loads(observed.read_text(encoding='utf-8'));paths={Path(p.replace('\\','/')).as_posix() for p in listing.read_text(encoding='utf-8').splitlines() if p.strip()};paths.add(Path(__file__).relative_to(R).as_posix());consumed={r['path']:r for r in runtime['observed_project_files'] if r['kind']=='code'};paths.update(consumed);static_path=R/'verify/out/n100-interface-dependency-audit-v2.json';static=json.loads(static_path.read_text(encoding='utf-8'));paths.update(n['path'] for n in static['nodes'] if n['kind']=='.py');active=defaultdict(list)
 for row in ADAPTERS:active['verify/'+row[1]].append(row[2])
 active['verify/n100_shared_support_session.py'].append('SupportSession.run');groups=defaultdict(list);rows=[];unclassified=[]
 for rel in sorted(paths):
  p=R/rel;assert p.is_file(),'missing source '+rel;text=p.read_text(encoding='utf-8-sig');tree=ast.parse(text);h=sha(p);groups[h].append(rel);f=locator(p);f=f if f in DETAIL else 'UNCLASSIFIED_REVIEW_REQUIRED'
  if f=='UNCLASSIFIED_REVIEW_REQUIRED':unclassified.append(rel)
  exploratory=rel.startswith(('_recon/','tools/')) or any(t in p.stem for t in ('probe','pilot','refine','polish','cooperative','stationarity','server','anneal','contact_lp','discover_'))
  frozen=('/frozen-' in rel or rel.startswith('runtime/boundary-line-replay-118/'))
  role='REGISTERED_ADAPTER_ONLY' if rel in active else 'FROZEN_SNAPSHOT_NO_NEW_AUTHORITY' if frozen else 'OBSERVED_SUPPORT_CALLED_SCOPE_ONLY' if rel in consumed else 'DISCOVERY_OR_SERVER_DRIVER_NO_PROOF_AUTHORITY' if exploratory else 'CONTROL_OR_PROTOCOL_ONLY' if f in ('proof_plumbing','counterexamples_controls','discovery_diagnostics') else 'LEGACY_SOURCE_CONTRACT_REVIEW_REQUIRED'
  literal_paths=set()
  for n in ast.walk(tree):
   if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.endswith('.json') and '\n' not in n.value:
    raw=n.value.replace('\\','/');candidate=R/raw
    if not candidate.is_file() and '/' not in raw:candidate=R/'verify/out'/raw
    if candidate.is_file() and candidate.resolve().is_relative_to(R):literal_paths.add(candidate.relative_to(R).as_posix())
  imports=[]
  for n in ast.walk(tree):
   modules=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module] if isinstance(n,ast.ImportFrom) and n.module else []
   for m in modules:
    for parent in (p.parent,R/'verify'):
     c=parent/(m.replace('.','/')+'.py')
     if c.is_file():imports.append(c.relative_to(R).as_posix());break
  rows.append({'source':rel,'sha256':h,'family_contract':f,'role':role,'documented_intent':ast.get_docstring(tree) or '', 'registered_entrypoints':active.get(rel,[]),'public_functions':[n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))],'static_local_imports':sorted(set(imports)),'existing_literal_json_candidates':[{'path':a,'sha256':sha(R/a),'withdrawn':a in WITHDRAWN,'reference_is_actual_consumption':False} for a in sorted(literal_paths)],'actually_observed_in_suite':rel in consumed,'source_specific_semantics_independently_reviewed':False,'activation':'only registered entrypoint contracts; all other functions/mains disabled as new proof leaves'})
 aliases=[{'sha256':h,'paths':ps,'meaning':'byte-identical sources; no transfer of domain or acceptance authority'} for h,ps in groups.items() if len(ps)>1];contracts=[]
 for f in DETAIL:
  domain,units,resource,premise,composition,certificate=DETAIL[f];contracts.append({'family':f,'domain':domain,'radius_units':units,'resource':resource,'required_premises':premise,'certificate':certificate,'composition':composition,'additive_by_default':False,'member_sources':[r['source'] for r in rows if r['family_contract']==f],'unreviewed_members_return':'PRECONDITION_MISSING; source-specific theorem/domain bridge missing','family_locator_is_activation_authority':False})
 quarantine=[{'path':p,'sha256':sha(R/p),'reason':why,'replacement':replacement,'replacement_sha256':sha(R/replacement)} for p,(why,replacement) in WITHDRAWN.items()];out=R/'verify/out/n100-pruning-recursive-inventory-v3.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-pruning-recursive-inventory/v1','summary':{'listed_filename_paths':len(listing.read_text(encoding='utf-8').splitlines()),'unique_source_paths_with_observed_nonfilename_dependencies':len(rows),'unique_source_contents':len(groups),'alias_groups':len(aliases),'role_counts':dict(Counter(r['role'] for r in rows)),'unclassified':unclassified},'family_contracts':contracts,'sources':rows,'source_content_aliases':aliases,'withdrawn_artifacts':quarantine,'scope':'frozen recursive filename census plus actual local-code dependency closure; exhaustive path/AST metadata within this set, not individual semantic theorem reproof','mathematical_verdict':None,'global_optimality':False,'bindings':{listing.relative_to(R).as_posix():sha(listing),observed.relative_to(R).as_posix():sha(observed),static_path.relative_to(R).as_posix():sha(static_path),'verify/n100_unified_proof_interface_registry.py':sha(R/'verify/n100_unified_proof_interface_registry.py')},'script_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8');print('PASS recursive inventory',len(rows),'paths',len(groups),'contents',len(aliases),'alias groups');print('ROLES',json.dumps(Counter(r['role'] for r in rows)));print('UNCLASSIFIED',json.dumps(unclassified))
if __name__=='__main__':main()
