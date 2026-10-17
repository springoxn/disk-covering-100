"""Gap-profile of the 4200 fixed-core survivor placements."""
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def gaps(p):return tuple((p[(i+1)%4]-p[i])%32 for i in range(4))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-survivor-gap-profile.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 z=load(ROOT/'verify/out/n100-boundary-circle-survivor-domain.json');stats=load(ROOT/'verify/out/n100-boundary-circle-exclusion-stats.json');surv=[tuple(p) for p in z['survivor_axis_edge_placements']];excluded=[tuple(p) for p in stats['excluded_placements']];allp=set(surv)|set(excluded);need(len(surv)==4200 and len(excluded)==576 and len(allp)==4776,'partition')
 ss=Counter(gaps(p) for p in surv);ee=Counter(gaps(p) for p in excluded);allclasses=sorted(set(ss)|set(ee));rows=[{'gaps':list(k),'survivors':ss[k],'excluded':ee[k],'total':ss[k]+ee[k],'survivor_fraction_num':ss[k],'survivor_fraction_den':ss[k]+ee[k]} for k in allclasses];need(sum(x['survivors'] for x in rows)==4200 and sum(x['excluded'] for x in rows)==576,'totals');empty=[x['gaps'] for x in rows if x['survivors']==0];candidate=(30,6,14,22);need(candidate in surv,'candidate')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-survivor-gap-profile/v1','verified':True,'survivor_count':4200,'excluded_count':576,'gap_class_count':len(rows),'profiles':rows,'empty_survivor_gap_classes':empty,'candidate_retained':True,'priority':'sort future branch work by survivor count descending; classes with zero survivors already fully excluded by current fixed-core certificates','scope':'one fixed core axis domain; gap statistics do not imply cross-core combinatorial theorem','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-boundary-circle-survivor-domain.json',ROOT/'verify/out/n100-boundary-circle-exclusion-stats.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS survivor gap profile',len(rows),'classes; empty',len(empty),'survivors',len(surv))
if __name__=='__main__':main()
