"""Replay all 32 survivors in the largest gap class and rank contraction."""
from pathlib import Path
import json,hashlib,argparse
from n100_boundary_circle_propagation import run
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def gaps(p):return tuple((p[(i+1)%4]-p[i])%32 for i in range(4))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-class77711.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 core=load(ROOT/'verify/out/n100-cubic-core-roundtrip.json')['core'];prior=load(ROOT/'verify/out/n100-axis-coupled-boxes.json');dom=load(ROOT/'verify/out/n100-boundary-circle-survivor-domain.json');members=[tuple(p) for p in dom['survivor_axis_edge_placements'] if gaps(p)==(7,7,7,11)];need(len(members)==32,'32 members');rows=[]
 for p in members:
  root=next(r['boxes'] for r in prior['retained'] if tuple(r['placement'])==p);a=run(core,list(p),root);b=run(core,list(p),root,True);need(a==b,'main independent mismatch');need(not a['excluded'],'class survivor excluded');rows.append({'placement':list(p),'sweeps':a['sweeps'],'fixed':a['fixed'],'distance_tests':a['distance_tests'],'circle_tests':a['circle_tests'],'center_total_width_reduction':a['center_total_width_reduction'],'boxes':a['boxes']})
 rows.sort(key=lambda r:(-r['center_total_width_reduction'],r['placement']));out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-class77711/v1','verified_integer_class_replay':True,'gap_class':[7,7,7,11],'member_count':len(rows),'all_nonexcluded':True,'rows':rows,'ranking':'center_total_width_reduction descending, placement lexicographic','scope':'one fixed core, complete32-member survivor class; nonempty fixed boxes unresolved','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-boundary-circle-survivor-domain.json',ROOT/'verify/out/n100-axis-coupled-boxes.json',ROOT/'verify/n100_boundary_circle_propagation.py')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS class 77711',len(rows),'all fixed; top',rows[0]['placement'],rows[0]['center_total_width_reduction'])
if __name__=='__main__':main()
