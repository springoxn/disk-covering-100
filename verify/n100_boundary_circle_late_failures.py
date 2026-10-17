"""Late-failure witness extraction for stage51 deep exclusions."""
from pathlib import Path
from collections import defaultdict
import json,hashlib,argparse
from n100_axis_coupled_boxes import radiussquared
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def gaps(p):return tuple((p[(i+1)%4]-p[i])%32 for i in range(4))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-late-failures.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 z=load(ROOT/'verify/out/n100-boundary-circle-capped160.json');late=[]
 for r in z['results']:
  q=r['result'];
  if q['excluded'] and q['sweeps']>=59:
   f=q['failure'];need(f[0]=='distance','late distance');a,b=q['boxes'][f[1]],q['boxes'][f[2]];dx=max(a[0]-b[1],b[0]-a[1],0);dy=max(a[2]-b[3],b[2]-a[3],0);margin=dx*dx+dy*dy-radiussquared(1);late.append({'placement':r['placement'],'gaps':list(gaps(r['placement'])),'sweeps':q['sweeps'],'failure_indices':f[1:3],'failure_boxes':[a,b],'axis_gap_signature':str(gaps(r['placement'])),'coordinate_gap_squared':dx*dx+dy*dy,'radius_squared_upper':radiussquared(1),'strict_margin':margin})
 need(len(late)==12,'12 late')
 groups=defaultdict(list)
 for x in late:groups[tuple(x['gaps'])].append(x)
 need(sum(map(len,groups.values()))==12,'group partition');need(all(x['coordinate_gap_squared']>x['radius_squared_upper'] if x['radius_squared_upper'] is not None else True for x in late),'strict')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-late-failures/v1','verified':True,'late_count':len(late),'sweep_threshold':59,'cases':late,'gap_groups':{str(k):len(v) for k,v in sorted(groups.items())},'uniform_failure_indices':len({tuple(x['failure_indices']) for x in late})==1,'scope':'12 stage51 deep exclusions only; fixed core necessary relaxation','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-boundary-circle-capped160.json',ROOT/'verify/out/n100-boundary-circle-exclusion-stats.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS late witnesses',len(late),'groups',dict((str(k),len(v)) for k,v in groups.items()),'failure index classes',len({tuple(x['failure_indices']) for x in late}))
if __name__=='__main__':main()
