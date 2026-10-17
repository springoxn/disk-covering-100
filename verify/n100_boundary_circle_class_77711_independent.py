"""Independent class replay audit from the saved 32-row certificate."""
from pathlib import Path
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def gaps(p):return tuple((p[(i+1)%4]-p[i])%32 for i in range(4))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-class77711-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 z=load(ROOT/'verify/out/n100-boundary-circle-class77711.json');dom=load(ROOT/'verify/out/n100-boundary-circle-survivor-domain.json');S=[tuple(p) for p in dom['survivor_axis_edge_placements'] if gaps(p)==(7,7,7,11)];rows=z['rows'];need(len(S)==32 and len(rows)==32,'32');need(sorted(tuple(r['placement']) for r in rows)==sorted(S),'members');need(all(r['fixed'] and r['sweeps']>0 for r in rows),'fixed');need(all(r['distance_tests']>0 and r['circle_tests']==32*r['sweeps'] for r in rows),'counters');need(rows==sorted(rows,key=lambda r:(-r['center_total_width_reduction'],r['placement'])),'ranking')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-class77711-independent/v1','verified':True,'gap_class':[7,7,7,11],'member_count':32,'all_members_equal_domain':True,'all_fixed':True,'all_nonexcluded':True,'ranking_equal':True,'top_placement':rows[0]['placement'],'top_width_reduction':rows[0]['center_total_width_reduction'],'method':'independent survivor-domain membership, counter invariants and rank verification; no propagation rerun','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-boundary-circle-class77711.json',ROOT/'verify/out/n100-boundary-circle-survivor-domain.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent class audit',len(rows),'top',rows[0]['placement'])
if __name__=='__main__':main()
