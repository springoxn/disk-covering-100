"""Read-only evidence audit of stages101-114; writes a new ledger only."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
NAMES=['recursive_inner_envelope','inner_radial_hierarchy','directional_center_counts','boundary_count_semantics','recursive_joint_area','recursive_radius_frontier','recursive_ear_obstruction','radius_count_strata','radius_local_joint_domain','outer_ear_family_cuts','uniform_outer_ear_topology','disjoint_ear_group_cuts','total_ear_face_cuts','ear_marked_joint_cuts']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 rows=[];checks=0
 for name in NAMES:
  paths=[R/'verify/out'/('n100-'+name.replace('_','-')+suffix+'.json') for suffix in ['', '-independent']];primary,ind=[json.loads(p.read_text(encoding='utf-8')) for p in paths];scripts=[R/'verify'/('n100_'+name+suffix+'.py') for suffix in ['', '_independent']];entry={'name':name,'files':[]}
  for path,obj,script in zip(paths,[primary,ind],scripts):
   assert obj.get('global_optimality') is False,(name,'global claim');assert script.is_file();checks+=2
   if 'script_sha256' in obj:assert obj['script_sha256']==sha(script),(name,'stale script');checks+=1
   for rel,expected in obj.get('bindings',{}).items():
    target=R/rel;assert target.is_file() and sha(target)==expected,(name,'stale binding',rel);checks+=1
   entry['files'].append({'path':str(path.relative_to(R)),'sha256':sha(path),'script':str(script.relative_to(R)),'script_sha256':sha(script),'script_hash_stored_in_certificate':'script_sha256' in obj})
  assert ind['input_sha256']==sha(paths[0]),(name,'independent input mismatch');checks+=1
  rows.append(entry)
 # Check radius-domain counts and topology controls from the actual saved files.
 domain=json.loads((R/'verify/out/n100-radius-local-joint-domain.json').read_text(encoding='utf-8'));assert [c['remaining_triple_count'] for c in domain['layers']]==[93,193,319,404];assert [c['remaining_family_count'] for c in domain['layers']]==[17,32,48,57];checks+=2
 final=json.loads((R/'verify/out/n100-ear-marked-joint-cuts.json').read_text(encoding='utf-8'));improved={(r['m'],r['B']):max(r['remaining_ear_counts']) for r in final['family_rows']};assert improved[(99,35)]==4 and improved[(99,36)]==4 and improved[(99,37)]==1;checks+=3
 out=R/'verify/out/n100-stage115-evidence-ledger.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-stage115-evidence-ledger/v1','all_integrity_checks_passed':True,'checks':checks,'stages_audited':14,'certificate_count':28,'script_count':28,'entries':rows,'current_domains':[{'radius_upper':c['radius_upper'],'triples':c['remaining_triple_count'],'families':c['remaining_family_count'],'minimum_nonserving':c['minimum_nonserving']} for c in domain['layers']],'latest_ear_upper_controls':[[99,35,4],[99,36,4],[99,37,1]],'open_objective_items':['complete enumeration and exclusion of all relevant maps in surviving count families','global infeasibility below candidate radius','exact optimal configuration and minimal polynomial with irreducibility and rational root isolation','end-to-end verified global optimality certificate'],'scope':'byte-integrity and finite saved-state audit; not an independent rerun of all computations nor proof of analytic geometry; cited global radius endpoints inherited, not reverified by this ledger','global_optimality':False,'script_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8');print('PASS stage115 ledger','checks',checks,'certificates28/scripts28','domains93/193/319/404')
if __name__=='__main__':main()
