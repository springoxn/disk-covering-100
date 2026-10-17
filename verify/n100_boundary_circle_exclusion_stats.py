"""Exact combinatorial statistics for 576 fixed-core circle exclusions."""
from pathlib import Path
from collections import Counter
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def gaps(p):return tuple((p[(i+1)%4]-p[i])%32 for i in range(4))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-exclusion-stats.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 full=load(ROOT/'verify/out/n100-boundary-circle-full.json');deep=load(ROOT/'verify/out/n100-boundary-circle-capped160.json');source=set()
 old=[]
 for r in full['results']:
  if r['excluded']:old.append(r);source.add(tuple(r['placement']))
 new=[]
 for r in deep['results']:
  if r['result']['excluded']:
   need(tuple(r['placement']) not in source,'duplicate exclusion');new.append(r)
 allrows=old+new;need(len(allrows)==576,'576 exclusions')
 bygap=Counter(gaps(r['placement']) for r in allrows);bytype=Counter((r['failure'][0] if 'failure' in r else r['result']['failure'][0]) for r in allrows);bysweep=Counter((r['sweeps'] if 'sweeps' in r else r['result']['sweeps']) for r in allrows);allplacements={tuple(r['placement']) for r in full['results']};need(len(allplacements)==4776,'domain')
 excluded=set(tuple(r['placement']) for r in allrows);retained=allplacements-excluded;need(len(retained)==4200,'partition')
 candidate=(30,6,14,22);need(candidate in retained,'candidate retained')
 rows=[{'placement':list(k),'count':v} for k,v in sorted(bygap.items())]
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-exclusion-stats/v1','verified':True,'input_domain':4776,'stage50_exclusions':len(old),'stage51_new_exclusions':len(new),'total_exclusions':len(allrows),'retained_fixed_core_domain':len(retained),'candidate_retained':True,'gap_histogram':rows,'failure_type_histogram':dict(bytype),'failure_sweep_histogram':{str(k):v for k,v in sorted(bysweep.items())},'excluded_placements':sorted(map(list,excluded)),'scope':'one fixed core; combines exact stage50 full scan and stage51 capped160 scan; no other cores','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-boundary-circle-full.json',ROOT/'verify/out/n100-boundary-circle-capped160.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS exclusion stats',len(old),len(new),dict(bytype),dict(bysweep),'gap classes',len(bygap))
if __name__=='__main__':main()
