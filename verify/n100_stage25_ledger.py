"""Audit stage25 certificate bytes, exact margins and explicitly limited scope."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    paths=['n100-cap-frontier-screen','n100-hall-automatic-search','n100-nonseparated-capacity-cut','n100-hybrid-capacity-tree']
    names=['n100_cap_frontier_screen','n100_hall_automatic_search','n100_nonseparated_capacity_cut','n100_hybrid_capacity_tree']
    binding={};data=[]
    for stem,name in zip(paths,names):
        p=ROOT/f'verify/out/{stem}.json';s=ROOT/f'verify/{name}.py';z=json.loads(p.read_text(encoding='utf-8'))
        need(z['script_sha256']==hashlib.sha256(s.read_bytes()).hexdigest(),'script binding')
        need(z['global_optimality'] is False and z['minimal_polynomial_obtained'] is False,'unsupported global claim')
        for q,h in z.get('bindings',{}).items():need(hashlib.sha256((ROOT/q).read_bytes()).hexdigest()==h,'dependency binding')
        binding[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();data.append(z)
    cap,hall,nonsep,tree=data
    need(F(cap['universal_serving_count_exclusion']['positive_margin'])>0,'cap gap')
    need(cap['new_m_B_families_excluded']==0 and not cap['k_equals_B_bridge_accepted'],'scope')
    need(len(cap['hypothetical_k_equals_B_grid_screen'])==87,'family inventory')
    need([r['result']['excluded'] for r in hall['results']]==[True,True,True,False],'Hall calibration')
    need(nonsep['independent']['verified'] and nonsep['result']['deficiency']==1,'capacity replay')
    need(nonsep['all_pairs_can_fit_in_one_disk'] and nonsep['triple_cannot_fit_in_one_disk'],'triple distinction')
    need(tree['result']['verified'] and not tree['result']['full_domain'],'restricted tree')
    need(len(tree['candidate_center_box_controls'])==3 and not any(z['excluded'] for z in tree['candidate_center_box_controls']),'candidate controls')
    out=ROOT/'verify/out/n100-stage25-ledger.json';need(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps({'schema':'n100-stage25-ledger/v1','verified_bindings_and_scopes':True,'bindings':binding,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'stage_entry_exit_codes_observed':[0,0,0,0],'exit_code_field_is_recorded_not_reexecuted_here':True,'global_optimality':False,'new_count_families_excluded':0,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS stage25 ledger: 4 certificate/script bindings and dependency hashes; rational gap and limited scopes; no global-optimality upgrade')
if __name__=='__main__':main()
