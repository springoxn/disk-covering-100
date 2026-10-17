"""Fresh independent replay of stage26 pattern certificates; never trusts saved PASS.
Use --out to select a fresh receipt path; existing receipts are preserved.
"""
from pathlib import Path
import argparse,json,hashlib
from fractions import Fraction as F
from n100_box_aware_capacity import independent,need
ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='verify/out/n100-stage26-independent-replay.json');args=parser.parse_args()
    paths=['verify/out/n100-box-aware-capacity.json','verify/out/n100-candidate-pattern-pruning.json','verify/out/n100-boundary-interface-controls.json']
    scripts=['verify/n100_box_aware_capacity.py','verify/n100_candidate_pattern_pruning.py','verify/n100_boundary_interface_controls.py']
    data=[];bindings={}
    for name,script in zip(paths,scripts):
        p=ROOT/name;z=json.loads(p.read_text(encoding='utf-8'))
        need(z['script_sha256']==hashlib.sha256((ROOT/script).read_bytes()).hexdigest(),'script hash')
        for dep,h in z.get('bindings',{}).items():need(hashlib.sha256((ROOT/dep).read_bytes()).hexdigest()==h,'dependency hash')
        data.append(z);bindings[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    pattern,candidate,interface=data
    independent(pattern['box'],pattern['pool'],pattern['result'])
    hidden=pattern['hidden_deficiency_case'];independent(hidden['box'],hidden['pool'],hidden['result'])
    results=[]
    for row in candidate['cases']:results.append(independent(row['box'],candidate['points'],row['result']))
    need(sum(z['excluded'] for z in results)==16 and len(results)==32,'scope counts')
    split=candidate['inherited_split'];parent=split['parent_box'];d=split['coordinate'];c=F(split['cut'])
    need(F(parent[d][0])<c<F(parent[d][1]),'split')
    for i,child in enumerate(split['children']):
        expected=[v.copy() for v in parent];expected[d]=[parent[d][0],str(c)] if i==0 else [str(c),parent[d][1]]
        need(child['box']==expected,'child inheritance');need(independent(child['box'],candidate['points'],child['result'])['excluded'],'split child')
    r=F(interface['radius']);d1=F(interface['inner_center_norm']);d2=F(interface['outer_center_norm']);C2=1-r*r
    need(1-r<d1<d2 and d2*d2<C2,'cap domain')
    threshold=(C2+d1*d1)/(2*d1);middle=(d1+d2)/2
    need(middle<threshold<1,'dominated service arc')
    outside=F(interface['normalization_collision']['modified_center_original_norm'])
    need(outside*outside>C2 and C2/outside==d1 and d1*d1<C2,'piecewise collision')
    need(not candidate['domain_exhaustive'] and candidate['count_families_excluded']==0,'scope upgrade')
    out=ROOT/args.out;need(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps({'schema':'n100-stage26-independent-replay/v1','verified':True,'fresh_numeric_checks':True,'candidate_cases_replayed':32,'candidate_cases_excluded':16,'candidate_cases_unresolved':16,'inherited_children_replayed':2,'interface_rational_countercontrols_recomputed':True,'global_optimality':False,'count_families_excluded':0,'bindings':bindings,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print('PASS independent fresh stage26 replay: 32 candidate cases, 16 excluded/16 unresolved; 2 inherited children; 2 interface countercontrols')
if __name__=='__main__':main()
