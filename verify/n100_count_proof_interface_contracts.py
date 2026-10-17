"""Complete saved count-domain replay plus typed radius/ear adapter controls."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
import n100_count_proof_interfaces as I
R=Path(__file__).resolve().parents[1]
def payload(radius,tuples):return {'n':100,'semantics_id':I.SEMANTICS,'configuration_id':'declared-normalized-cover-branch','radius_units':'radius','radius_upper':str(radius),'tuples':tuples}
def main():
 outer=json.loads((R/'verify/out/n100-radius-local-joint-domain.json').read_text(encoding='utf-8'));ears=json.loads((R/'verify/out/n100-ear-marked-joint-cuts.json').read_text(encoding='utf-8'));baseline=outer['layers'][-1]['remaining_triples'];requests=[]
 for layer in outer['layers']:requests.append(('radius_joint',payload(layer['radius_upper'],baseline)))
 rho=F(ears['radius_upper_inclusive']);seed=payload(rho,[[c['m'],c['B'],c['B']] for c in ears['family_rows']]);lifted,lift_certificate=I.lift_to_ears(seed);requests.append(('ear_marked',lifted));requests.append(('ear_marked',payload(rho,[[100,32,32,7]])));requests.append(('ear_marked',payload(rho+F(1,10**12),[[100,32,32,7]])))
 negative=[]
 for label,change in [('B_is_arbitrary_arcs',lambda p:p.update(semantics_id='arbitrary-owner-arc-count')),('squared_radius_used',lambda p:p.update(radius_units='squared')),('outside_certified_radius',lambda p:p.update(radius_upper=str(I.U+F(1,10**12)))),('B_exceeds_k',lambda p:p.update(tuples=[[100,33,32]])),('float_radius',lambda p:p.update(radius_upper=0.113)),('wrong_n',lambda p:p.update(n=99)),('missing_configuration',lambda p:p.pop('configuration_id')),('noninteger_label',lambda p:p.update(tuples=[[100,32,'32']]))]:
  p=payload(rho,[[100,32,32]]);change(p);negative.append(label);requests.append(('radius_joint',p))
 results,receipt=I.run_batch(requests);assert [len(r['remaining']) for r in results[:4]]==[93,193,319,404]
 for r,layer in zip(results[:4],outer['layers']):assert r['remaining']==layer['remaining_triples'] and [100,32,32] in r['remaining']
 decorated=results[4];assert decorated['ear_bound_applied'];expected={(c['m'],c['B'],e) for c in ears['family_rows'] for e in c['remaining_ear_counts']};actual={(m,B,e) for m,B,k,e in decorated['remaining']};assert actual==expected
 assert results[5]['status']=='EXCLUDED' and results[6]['status']=='NOT_EXCLUDED' and not results[6]['ear_bound_applied'];assert all(r['status']=='PRECONDITION_MISSING' for r in results[7:]);assert receipt['outer_scalar_cases']==204 and receipt['ear_scalar_cases']==153
 # Lifting preserves each count branch and enumerates every possible actual e.
 assert all(lifted[k]==seed[k] for k in ('configuration_id','radius_units','radius_upper','semantics_id'));assert {(m,B,k) for m,B,k,e in lifted['tuples']}==set(map(tuple,seed['tuples']))
 bad=copy.deepcopy(seed);bad['tuples']=[[32,32,32]]
 try:I.lift_to_ears(bad)
 except ValueError:negative.append('no_interior_vertex_ear_lift')
 else:raise AssertionError('invalid ear lift')
 out=R/'verify/out/n100-count-proof-interface-contracts.json';assert not out.exists();paths=[R/'verify/n100_count_proof_interfaces.py',R/'verify/n100_pruning_catalogue.py',R/'verify/n100_recursive_joint_area_independent.py'];out.write_text(json.dumps({'schema':'n100-count-proof-interface-contracts/v1','four_radius_domain_counts':[len(r['remaining']) for r in results[:4]],'all357_saved_scalar_cases_recomputed':receipt,'four_layers_match_full_saved_domains':True,'candidate_label_retained_not_proven_feasible':True,'ear_decoration_adapter':lift_certificate,'ear_decorated_remaining_count':len(decorated['remaining']),'all17_ear_families_match_saved_counts':True,'tight_endpoint_excludes_e7':results[5],'just_above_endpoint_retains_e7':results[6],'negative_controls':negative,'scope':'radius-local/ear scalar and finite domain replays; recursive frontier and geometric premises inherited; exact canonical count domains with explicit decoration lift; no arbitrary B=k identification','global_optimality':False,'bindings':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS count interfaces;204 outer +153 ear scalars;93/193/319/404;ear endpoint control;negative controls',len(negative))
if __name__=='__main__':main()
