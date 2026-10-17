"""Independent survivor-domain partition audit."""
from pathlib import Path
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-survivor-domain-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 full=load(ROOT/'verify/out/n100-boundary-circle-full.json');deep=load(ROOT/'verify/out/n100-boundary-circle-capped160.json');prior=load(ROOT/'verify/out/n100-axis-dual-chain-pruning.json');z=load(ROOT/'verify/out/n100-boundary-circle-survivor-domain.json');base={tuple(x) for x in prior['retained_axis_edge_placements']};old={tuple(r['placement']) for r in full['results'] if r['excluded']};new={tuple(r['placement']) for r in deep['results'] if r['result']['excluded']};surv=base-old-new
 need(len(base)==4776 and len(old)==564 and len(new)==12 and old.isdisjoint(new) and len(surv)==4200,'partition counts');need([list(p) for p in sorted(surv)]==z['survivor_axis_edge_placements'],'survivor list');need(sorted(map(tuple,z['survivor_axis_edge_placements']))==sorted(surv),'order');need(tuple(z['candidate_axis_edge_indices']) in surv,'candidate');need(set(surv)|old|new==base and not (surv&(old|new)),'complete partition')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-survivor-domain-independent/v1','verified':True,'base_count':len(base),'stage50_excluded':len(old),'stage51_excluded':len(new),'survivor_count':len(surv),'partition_equal':True,'candidate_retained':True,'method':'independent set construction from stage39, stage50, stage51; sorted list and disjoint union assertions','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-axis-dual-chain-pruning.json',ROOT/'verify/out/n100-boundary-circle-full.json',ROOT/'verify/out/n100-boundary-circle-capped160.json',ROOT/'verify/out/n100-boundary-circle-survivor-domain.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent survivor partition',len(base),'=',len(old),'+',len(new),'+',len(surv))
if __name__=='__main__':main()
