"""Deepen the 24 capped stage50 cases to 160 sweeps."""
from pathlib import Path
import json,hashlib,argparse
from n100_boundary_circle_propagation import run
from n100_boundary_circle_independent import replay
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-capped160.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';full=ROOT/'verify/out/n100-boundary-circle-full.json';core=load(cp)['core'];prior=load(bp);z=load(full);capped=[r for r in z['results'] if not r['excluded'] and not r['fixed']];need(len(capped)==24,'24 capped')
 rows=[]
 for num,rec in enumerate(capped,1):
  p=rec['placement'];root=next(x['boxes'] for x in prior['retained'] if x['placement']==p);main=run(core,p,root,limit=160);ind,w=replay(core,p,root,limit=160);need(main==ind,'deep replay mismatch '+str(p));rows.append({'placement':p,'result':main,'independent_failure':w});print('progress',num,main['excluded'],main.get('fixed'),main['sweeps'],flush=True)
 candidate=load(ROOT/'verify/out/n100-axis-subdivision-pruning.json')['candidate_axis_edge_indices'];need(candidate not in [r['placement'] for r in rows],'candidate should not be capped')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-capped160/v1','verified_integer_deep_scan':True,'input_count':24,'sweep_limit':160,'results':rows,'excluded_count':sum(r['result']['excluded'] for r in rows),'fixed_count':sum((not r['result']['excluded']) and r['result']['fixed'] for r in rows),'capped_count':sum((not r['result']['excluded']) and (not r['result']['fixed']) for r in rows),'candidate_retained':True,'scope':'the24 capped leaves of stage50, same necessary circle/quadrant/shared-vertex relaxation; nonempty remains unresolved','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,full,ROOT/'verify/n100_boundary_circle_propagation.py',ROOT/'verify/n100_boundary_circle_independent.py')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS capped160',sum(r['result']['excluded'] for r in rows),'excluded',sum((not r['result']['excluded']) and r['result']['fixed'] for r in rows),'fixed',sum((not r['result']['excluded']) and (not r['result']['fixed']) for r in rows),'capped')
if __name__=='__main__':main()
