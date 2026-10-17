"""Independent check that the stage26 unresolved count is a finite-pool statement.
No new geometry is asserted here.
"""
from pathlib import Path
import json,hashlib
from fractions import Fraction as F
from n100_box_aware_capacity import independent,need
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=ROOT/'verify/out/n100-candidate-pattern-pruning.json';z=json.loads(p.read_text(encoding='utf-8'))
    need(z['excluded_case_count']==16 and z['unresolved_case_count']==16 and len(z['cases'])==32,'stage26 counts')
    for row in z['cases']:independent(row['box'],z['points'],row['result'])
    for c in z['candidate_controls']:need(c['excluded'] is False,'candidate control')
    need(z['domain_exhaustive'] is False and z['count_families_excluded']==0,'scope')
    out=ROOT/'verify/out/n100-stage26-scope-audit.json';need(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps({'schema':'n100-stage26-scope-audit/v1','verified':True,'replayed_cases':32,'excluded':16,'unresolved':16,'candidate_controls':3,'domain_exhaustive':False,'count_families_excluded':0,'global_optimality':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS stage26 finite-scope audit: 32 cases, 16/16, 3 candidate controls, no global upgrade')
if __name__=='__main__':main()
