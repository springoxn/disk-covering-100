"""Boundary-circle annulus necessary cut on two fixed core placements."""
from pathlib import Path
import json,hashlib,argparse
from n100_axis_coupled_boxes import build,Q
from n100_dart_independent_canonicalization import loops,need
ROOT=Path(__file__).resolve().parents[1];UN=1154469548855829;UD=10**16
def annulus(box):
 threshold=UD-UN;mx=max(abs(box[0]),abs(box[1]));my=max(abs(box[2]),abs(box[3]))
 return None if mx*mx+my*my < (threshold*Q//UD)**2 else box
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-annulus-boxes-v2.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';sp=ROOT/'verify/out/n100-axis-subdivision-pruning.json';core=load(cp)['core'];prior=load(bp);cand=load(sp)['candidate_axis_edge_indices'];fc=loops(core['phi']);outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');boundary_faces={f for f,row in enumerate(fc) if f!=outer and any(core['core_tags'][d][0]=='outer' for d in row)};rows=[]
 for row in (prior['retained'][0],next(x for x in prior['retained'] if x['placement']==cand)):
  removed=[f for f in boundary_faces if annulus(row['boxes'][f]) is None];rows.append({'placement':row['placement'],'annulus_empty_faces':sorted(removed),'retained':not removed})
 need(not rows[1]['annulus_empty_faces'],'candidate falsely excluded');out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-annulus-boxes/v2','verified_integer_boundary_cut':True,'boundary_faces':sorted(boundary_faces),'cases':rows,'candidate_retained':True,'cut':'Only a face owning an outer boundary dart must have |center|>=1-U; boxes wholly inside radius 1-U are empty','scope':'necessary annulus cut on two fixed core fixed-point boxes; no angular endpoint constraints and no full enumeration','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,sp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS boundary annulus',[(r['placement'],len(r['annulus_empty_faces'])) for r in rows])
if __name__=='__main__':main()
