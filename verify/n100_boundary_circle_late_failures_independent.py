"""Independent checks for late-failure witness statistics."""
from pathlib import Path
from collections import Counter
import json,hashlib,argparse
from n100_axis_coupled_boxes import radiussquared
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def gaps(p):return tuple((p[(i+1)%4]-p[i])%32 for i in range(4))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-late-failures-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 z=load(ROOT/'verify/out/n100-boundary-circle-capped160.json');p=load(ROOT/'verify/out/n100-boundary-circle-late-failures.json');cases=[]
 for r in z['results']:
  q=r['result']
  if q['excluded'] and q['sweeps']>=59:
   f=q['failure'];a,b=q['boxes'][f[1]],q['boxes'][f[2]];dx=max(a[0]-b[1],b[0]-a[1],0);dy=max(a[2]-b[3],b[2]-a[3],0);cases.append({'placement':r['placement'],'gaps':list(gaps(r['placement'])),'sweeps':q['sweeps'],'failure_indices':f[1:3],'coordinate_gap_squared':dx*dx+dy*dy,'radius_squared_upper':radiussquared(1),'strict_margin':dx*dx+dy*dy-radiussquared(1)})
 need(cases==[{'placement':x['placement'],'gaps':x['gaps'],'sweeps':x['sweeps'],'failure_indices':x['failure_indices'],'coordinate_gap_squared':x['coordinate_gap_squared'],'radius_squared_upper':x['radius_squared_upper'],'strict_margin':x['strict_margin']} for x in p['cases']],'witness equality');need(all(x['strict_margin']>0 for x in cases),'strict')
 gh=Counter(tuple(x['gaps']) for x in cases);need({str(k):v for k,v in sorted(gh.items())}==p['gap_groups'],'groups');out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-late-failures-independent/v1','verified':True,'late_count':len(cases),'witnesses_equal':True,'all_strict_margins_positive':True,'gap_groups_equal':True,'failure_index_classes':len({tuple(x['failure_indices']) for x in cases}),'method':'independent JSON traversal and recomputed box gaps/radius upper bounds','scope':'12 fixed-core deep exclusions','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in (ROOT/'verify/out/n100-boundary-circle-capped160.json',ROOT/'verify/out/n100-boundary-circle-late-failures.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent late witnesses',len(cases),'strict, groups',dict(gh))
if __name__=='__main__':main()
