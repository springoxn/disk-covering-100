"""Build exact remaining fixed-core domain after all certified exclusions."""
from pathlib import Path
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-survivor-domain.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 full=load(ROOT/'verify/out/n100-boundary-circle-full.json');deep=load(ROOT/'verify/out/n100-boundary-circle-capped160.json');prior=load(ROOT/'verify/out/n100-axis-dual-chain-pruning.json');sub=load(ROOT/'verify/out/n100-axis-subdivision-pruning.json');base={tuple(p) for p in prior['retained_axis_edge_placements']};need(len(base)==4776,'base')
 excluded={tuple(r['placement']) for r in full['results'] if r['excluded']};deep_new={tuple(r['placement']) for r in deep['results'] if r['result']['excluded']};need(not excluded&deep_new,'disjoint');excluded|=deep_new;need(len(excluded)==576,'excluded576');survivors=sorted(base-excluded);need(len(survivors)==4200,'survivors4200');candidate=tuple(sub['candidate_axis_edge_indices']);need(candidate in survivors,'candidate')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-survivor-domain/v1','verified':True,'input_domain':len(base),'excluded_stage50_51':len(excluded),'survivor_count':len(survivors),'survivor_axis_edge_placements':[list(p) for p in survivors],'candidate_axis_edge_indices':list(candidate),'candidate_retained':True,'excluded_disjoint':True,'scope':'one fixed core; survivor list after strict circle/vertex-box exclusions; survivors are unresolved necessary domains, not feasible coverings','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-axis-dual-chain-pruning.json',ROOT/'verify/out/n100-boundary-circle-full.json',ROOT/'verify/out/n100-boundary-circle-capped160.json',ROOT/'verify/out/n100-axis-subdivision-pruning.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS survivor domain',len(base),'->',len(survivors),'candidate',candidate)
if __name__=='__main__':main()
