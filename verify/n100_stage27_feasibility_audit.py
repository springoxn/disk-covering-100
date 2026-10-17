"""Independently verify finite-pool covers and detect genuinely feasible boxes.
Fresh upstream exact coverage replay is performed before using that configuration.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def check_cover(box,points,cover):
    need(cover['found'] is True,'cover missing')
    C=[tuple(map(F,p)) for p in cover['centers']];P=[tuple(map(F,p)) for p in points];assign=cover['assignment'];t=F(box[-1][1])
    need(len(C)==(len(box)-1)//2 and len(assign)==len(P),'dimensions')
    for j,c in enumerate(C):
        need(len(c)==2 and all(F(box[2*j+d][0])<=c[d]<=F(box[2*j+d][1]) for d in (0,1)),'center outside box')
    margins=[]
    for p,j in zip(P,assign):
        need(type(j) is int and 0<=j<len(C),'assignment')
        dx=p[0]-C[j][0];dy=p[1]-C[j][1];margins.append(t-dx*dx-dy*dy)
    need(min(margins)>=0,'uncovered witness')
    need(F(cover['minimum_margin'])==min(margins),'margin binding')
    return {'verified':True,'points':len(P),'minimum_margin':str(min(margins))}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-stage27-feasibility-audit.json');args=ap.parse_args()
    expanded=ROOT/'verify/out/n100-expanded-hole-pool.json';prior=ROOT/'verify/out/n100-candidate-pattern-pruning.json'
    z=json.loads(expanded.read_text(encoding='utf-8'));parents=json.loads(prior.read_text(encoding='utf-8'))
    mp=ROOT/'runtime/external-disk100-strict-local-replay/source/rational_midpoint.json';mid=json.loads(mp.read_text(encoding='utf-8'));x=[F(int(v),int(mid['denominator'])) for v in mid['numerators']]
    finite=[]
    for pool in z['pool_results']:
        pts=[[str(v) for v in x[200+2*h:202+2*h]] for h in range(pool['pool_holes'])]
        count=0
        for index,row in enumerate(pool['cases']):
            if row['finite_cover']['found']:
                check_cover(parents['cases'][index]['box'],pts,row['finite_cover']);need(not row['excluded_by_window'],'contradicting exclusion');count+=1
        need(count==16,'finite cover count')
        finite.append({'pool_size':pool['pool_holes'],'explicit_cover_cases':count})
    # A fresh full continuous-domain cover certification, not merely a stored receipt.
    folder=ROOT/'runtime/disk100-release-lf-67ebf1c/strict_upper_margin_1154469'
    sys.path.insert(0,str(folder));from verify_margin import verify_files
    config=folder/'configuration.json';cert=folder/'cover_certificate.json';ledger=folder/'margin_ledger.json'
    continuous=verify_files(config,cert,ledger);need(continuous['covering_exact_verified'],'continuous coverage')
    q=json.loads(config.read_text(encoding='utf-8'));C=[tuple(F(v,q['coordinate_denominator']) for v in p) for p in q['centers_numerators']]
    contained=[];not_contained=[]
    for index,row in enumerate(parents['cases']):
        b=row['box'];ok=all(F(b[2*j+d][0])<=C[j][d]<=F(b[2*j+d][1]) for j in range(100) for d in (0,1))
        if ok:
            need(not row['result']['excluded'],'false exclusion of continuous cover');contained.append(index)
        else:not_contained.append(index)
    need(bool(contained),'no genuine feasible boxes')
    output={'schema':'n100-stage27-feasibility-audit/v1','verified':True,'finite_pool_cover_audits':finite,'genuinely_feasible_parent_case_indices':contained,'not_containing_this_configuration_indices':not_contained,
        'fresh_continuous_cover_replay':continuous,'all_parent_boxes_exclusion_is_impossible':True,
        'scope':'finite-pool and specific-box feasibility controls; no global optimum or lower-bound change',
        'global_optimality':False,'count_families_excluded':0,
        'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (expanded,prior,mp,config,cert,ledger,folder/'verify_margin.py',folder/'critical_candidates.py')},
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=ROOT/args.out;need(not out.exists(),'refuse overwrite');out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('PASS independent finite covers: 16 cases at each pool size; fresh full cover replay; genuinely feasible boxes:',len(contained),contained)
if __name__=='__main__':main()
