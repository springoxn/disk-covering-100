"""Select largest survivor gap class and one representative placement."""
from pathlib import Path
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def gaps(p):return tuple((p[(i+1)%4]-p[i])%32 for i in range(4))
def need(x,m):
 if not x:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-branch-priority.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 z=load(ROOT/'verify/out/n100-boundary-circle-survivor-domain.json');prof=load(ROOT/'verify/out/n100-boundary-circle-survivor-gap-profile.json');S=[tuple(p) for p in z['survivor_axis_edge_placements']];best=max(prof['profiles'],key=lambda r:(r['survivors'],tuple(-x for x in r['gaps'])));members=[p for p in S if gaps(p)==tuple(best['gaps'])];need(members and len(members)==best['survivors'],'class members');rep=min(members);out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-branch-priority/v1','verified':True,'selection':'maximum survivor count, ties lexicographic gaps then placement','selected_gaps':best['gaps'],'survivor_count':best['survivors'],'excluded_count':best['excluded'],'representative':list(rep),'members_count':len(members),'candidate_selected':rep==(30,6,14,22),'scope':'priority selection only; no geometric exclusion','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-boundary-circle-survivor-domain.json',ROOT/'verify/out/n100-boundary-circle-survivor-gap-profile.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS priority gaps',best,'representative',rep)
if __name__=='__main__':main()
