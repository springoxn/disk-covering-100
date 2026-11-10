"""Compose direct same-radius .113231 fresh replays and source audits."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
tag='direct-113231-fresh';folder=ROOT/f'runtime/lower-small-advance-{tag}'
paths={'first':ROOT/f'verify/out/n100-lower-small-advance-{tag}.json','traced':ROOT/f'verify/out/n100-radius-dependency-audit-{tag}.json','controls':ROOT/'verify/out/n100-direct-113231-controls.json'}
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a,b,c=[read(paths[k]) for k in ['first','traced','controls']]
R=F(113231,1000000)
assert a['exit_code']==0 and a['all_six_branch_arithmetic_closed']
assert a['upstream_unchanged'] and a['transformed_copy_unchanged_during_replay']
assert b['exit_code']==0 and b['all_branches_replayed'] and not b['entries_with_other_global_R']
assert c['status']=='PASS_TRANSFORMATION_AND_NEGATIVE_CONTROLS'
assert all(F(x['radius'])==R for x in (a,b,c))
first=a['result'];second=read(folder/'audit.stdout.json')
assert first['status']==second['status']=='PASS'
assert first['theorem']==second['theorem']=='r_D(100)>'+str(R)
branches=['B31','B32','B33','B34','B35','B36plus']
assert first['complete_surviving_boundary_counts']==second['complete_surviving_boundary_counts']==list(range(31,40))
bridge=first['common_count_bridge']
assert bridge['n']==99 and F(bridge['radius'])==R and F(bridge['minimum_area_margin'])>0
rows=[]
for branch in branches:
    x=first[branch]['result'];y=second[branch]['result']
    assert x['status']==y['status']=='PASS' and F(x['radius'])==F(y['radius'])==R
    key=next(k for k in ['minimum_area_margin','minimum_reported_area_margin','minimum_area_margin_at_B36'] if k in x)
    assert F(x[key])>0 and x[key]==y[key]
    rows.append({'branch':branch,'radius':str(R),'minimum_margin':x[key],'source':first[branch]['source']})
manifest=read(folder/'transformation.json')
original=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323'
for rel,digest in manifest['source_snapshot'].items():assert sha(original/rel)==digest
for rel,digest in manifest['copy_snapshot'].items():assert sha(folder/'package'/rel)==digest
# Record the formula needed for the strict endpoint; not a formalization of geometry.
sourcepaths=[Path(__file__),ROOT/'verify/n100_lower_small_advance.py',ROOT/'verify/n100_radius_dependency_audit.py',ROOT/'verify/n100_radius_process_trace.py',ROOT/'verify/n100_direct_113231_controls.py',folder/'transformation.json',folder/'stdout.json',folder/'stderr.txt',folder/'audit.stdout.json',folder/'audit.stderr.txt',*paths.values()]
result={'schema':'n100-direct-same-radius-full-replay/v1','status':'PASS_ALL_SIX_BRANCH_ARITHMETIC_AT_SAME_RADIUS','radius':str(R),'claim_of_analytic_chain':'r_D(100)>'+str(R),'fresh_bottom_up_numeric_entry':'working/verify_all_11323.py','fresh_full_runs':2,'uses_0p113235_certificates':False,'uses_saved_branch_PASS_reports_for_acceptance':False,'original_release_unchanged':True,'transformed_copy_unchanged':True,'required_center_norm_squared_upper':str(1-R*R),'count_bridge':bridge,'complete_surviving_boundary_counts':list(range(31,40)),'all_six_branch_arithmetic_closed':True,'branch_margins':rows,'tail_boxes':first['B36plus']['result']['complete_capped_pair'],'parameter_trace':{'process_count':b['process_count'],'loaded_source_count':b['loaded_source_count'],'other_global_R_entries':b['entries_with_other_global_R'],'scope':'Tracked verifier calls and registered imported modules; full 626-file manifest binds anonymous dynamic loaders too.'},'negative_controls':c['controls'],'geometry_independently_reproved':False,'machine_verified_geometry':False,'analytic_dependencies':['Same-radius normalization of every center, followed by rebuilding the common diagram and m/B classification.','Normalized star/face bounds, hinge payments and signed edge cancellation.','Planar graph and combinatorial isoperimetric lemmas including degenerate limits.','Compactness and continuity convert exclusion of the closed endpoint into a strict radius lower bound.'],'scope':'Full fresh arithmetic replay of the existing analytic proof chain at .113231. Not an independent derivation of all analytic geometric premises, and no assertion that .11324 is proved.','bindings':{p.relative_to(ROOT).as_posix():sha(p) for p in sourcepaths}}
out=ROOT/'verify/out/n100-direct-113231-complete.json'
assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['bindings','negative_controls','analytic_dependencies','count_bridge']},indent=2))
