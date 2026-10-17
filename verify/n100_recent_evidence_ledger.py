"""Current recent certificate binding audit only, not geometric proof replay."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
PAIRS='candidate-topology-audit:candidate_topology_audit candidate-map-embedding:candidate_map_embedding full-circumcenter-root-box:full_circumcenter_root_box full-circumcenter-independent:full_circumcenter_independent boundary-pair-intersections:boundary_pair_intersections boundary-owner-independent:boundary_owner_independent candidate-clipped-map:candidate_clipped_map candidate-clipped-map-independent:candidate_clipped_map_independent candidate-quadratic-cover-model:candidate_quadratic_cover_model candidate-quadratic-cover-model-independent:candidate_quadratic_cover_model_independent map-canonicalization:map_canonicalization dart-map-canonicalization:dart_map_canonicalization small-map-enumeration-calibration:small_map_enumeration_calibration generic-map-compiler:generic_map_compiler generic-map-compiler-independent:generic_map_compiler_independent raw-dart-model-adapter:raw_dart_model_adapter face-axis-global-exclusion:face_axis_global_exclusion face-axis-infeasibility-independent:face_axis_infeasibility_independent boundary-serving-count:boundary_serving_count boundary-serving-count-independent:boundary_serving_count_independent face-axis-raw-variable-certificates-v2:face_axis_raw_variable_certificates face-axis-raw-independent:face_axis_raw_independent disconnected-boundary-owner-counterexample:disconnected_boundary_owner_counterexample disconnected-boundary-owner-independent:disconnected_boundary_owner_independent boundary-interior-count:boundary_interior_count boundary-interior-count-independent:boundary_interior_count_independent boundary-cap-area-branch:boundary_cap_area_branch boundary-cap-area-independent:boundary_cap_area_independent'
def audit():
    hashes={}
    for p in (R/'verify/out').glob('n100-*.json'):hashes.setdefault(sha(p),[]).append(p.relative_to(R).as_posix())
    rows=[];failures=[];links=0
    for pair in PAIRS.split():
        receipt,script=pair.split(':');rp=R/f'verify/out/n100-{receipt}.json';sp=R/f'verify/n100_{script}.py';z=json.loads(rp.read_text(encoding='utf-8'));errors=[]
        if z.get('checker_sha256')!=sha(sp):errors.append('checker hash mismatch')
        bound=[]
        for key in ('bindings','sources_sha256','dependencies_sha256'):
            for path,h in z.get(key,{}).items():
                p=R/path;ok=p.is_file() and sha(p)==h;links+=1;bound.append({'path':path,'matched':ok})
                if not ok:errors.append('dependency mismatch: '+path)
        parent=None
        if 'input_sha256' in z:
            parent=hashes.get(z['input_sha256'],[]);links+=1
            if not parent:errors.append('unresolved parent hash')
        if z.get('global_optimality') is not False or z.get('minimal_polynomial_obtained') is not False:errors.append('scope flags not explicitly false')
        rows.append({'receipt':rp.relative_to(R).as_posix(),'receipt_sha256':sha(rp),'checker':sp.relative_to(R).as_posix(),'bound_files':bound,'parent_hash_matches':parent,'errors':errors})
        failures.extend([{'receipt':receipt,'error':e} for e in errors])
    return rows,failures,links
if __name__=='__main__':
    rows,failures,links=audit();out=R/'verify/out/n100-recent-evidence-ledger.json'
    if out.exists():raise FileExistsError(out)
    out.write_text(json.dumps({'binding_audit_passed':not failures,'receipt_count':len(rows),'dependency_links_checked':links,'rows':rows,'failures':failures,'excluded_unaccepted_receipts':['verify/out/n100-face-axis-raw-variable-certificates.json'],'unaccepted_reason':'initial quotient generator did not verify reconstruction; superseded by v2 and independent full-variable check','scope':'hash/binding/scope ledger only; no independent geometry replay or complete proof chain certification','remaining_obligations':['complete unrestricted map enumeration including degeneracies','exclude noncandidate maps and candidate domain outside local ball','close universal lower bound at algebraic candidate','true optimum primitive irreducible minimal polynomial','irreducibility and rational root isolation tied to global equality'],'global_optimality':False,'minimal_polynomial_obtained':False,'checker_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8')
    print('binding audit',len(rows),'receipts',links,'links',len(failures),'failures')
    for e in failures:print(e)
    if failures:raise SystemExit(1)
