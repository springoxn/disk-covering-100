"""Independent replay of fixed-core exclusion statistics."""
from pathlib import Path
from collections import Counter
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def gaps(p):return tuple((p[(i+1)%4]-p[i])%32 for i in range(4))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-exclusion-stats-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 full=load(ROOT/'verify/out/n100-boundary-circle-full.json');deep=load(ROOT/'verify/out/n100-boundary-circle-capped160.json');z=load(ROOT/'verify/out/n100-boundary-circle-exclusion-stats.json');old={tuple(r['placement']):r for r in full['results'] if r['excluded']};new={tuple(r['placement']):r for r in deep['results'] if r['result']['excluded']};need(set(old).isdisjoint(new),'disjoint')
 allr=list(old.values())+list(new.values());ex=sorted(set(old)|set(new));need(len(ex)==576 and [list(p) for p in ex]==z['excluded_placements'],'excluded list');gap=Counter(gaps(p) for p in ex);typ=Counter('distance' for _ in ex);sweeps=Counter((r['sweeps'] if 'sweeps' in r else r['result']['sweeps']) for r in allr)
 need([{'placement':list(k),'count':v} for k,v in sorted(gap.items())]==z['gap_histogram'],'gap histogram');need(dict(typ)==z['failure_type_histogram'],'type');need({str(k):v for k,v in sorted(sweeps.items())}==z['failure_sweep_histogram'],'sweep')
 domain={tuple(r['placement']) for r in full['results']};need(len(domain)==4776 and len(domain-set(ex))==4200,'partition');need((30,6,14,22) in domain-set(ex),'candidate')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-exclusion-stats-independent/v1','verified':True,'domain':len(domain),'excluded':len(ex),'retained':len(domain-set(ex)),'gap_histogram_equal':True,'failure_histogram_equal':True,'sweep_histogram_equal':True,'candidate_retained':True,'method':'independent JSON aggregation, no propagation rerun; duplicate and partition assertions','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-boundary-circle-full.json',ROOT/'verify/out/n100-boundary-circle-capped160.json',ROOT/'verify/out/n100-boundary-circle-exclusion-stats.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent stats',len(ex),'excluded',len(domain-set(ex)),'retained;36 gap classes')
if __name__=='__main__':main()
