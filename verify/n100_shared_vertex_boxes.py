"""Shared-vertex interval propagation on two fixed-core axis placements."""
from pathlib import Path
import json,hashlib,argparse
from n100_axis_coupled_boxes import build,contract,radiussquared,Q
from n100_dart_independent_canonicalization import loops,need
ROOT=Path(__file__).resolve().parents[1]
def run(core,root,p,sites,adj,D,sweeps):
 A=core['alpha'];fc=loops(core['phi']);vc=loops(core['sigma']);vo={d:i for i,row in enumerate(vc) for d in row};outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');inner=[i for i in range(len(fc)) if i!=outer];fi={f:i for i,f in enumerate(inner)};C=len(inner);boxes=[b[:] for b in root]+[[-Q,Q,-Q,Q] for _ in vc];cons=[]
 for i in range(C):
  cons += [(i,C+vo[d],radiussquared(1)) for d in fc[inner[i]]]
 count=0
 for sw in range(sweeps):
  changed=False
  for a,b,r2 in cons:
   old=boxes[a];new=contract(old,boxes[b],r2);count+=1
   if new is None:return {'excluded':True,'sweeps':sw+1,'contractions':count,'failure':[a,b,r2,old,boxes[b]]}
   if new!=old:boxes[a]=new;changed=True
   old=boxes[b];new=contract(old,boxes[a],r2);count+=1
   if new is None:return {'excluded':True,'sweeps':sw+1,'contractions':count,'failure':[b,a,r2,old,boxes[a]]}
   if new!=old:boxes[b]=new;changed=True
  if not changed:return {'excluded':False,'fixed':True,'sweeps':sw+1,'contractions':count,'boxes':boxes,'vertices':len(vc),'constraints':len(cons)}
 return {'excluded':False,'fixed':False,'sweeps':sweeps,'contractions':count,'boxes':boxes,'vertices':len(vc),'constraints':len(cons)}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-shared-vertex-boxes.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';sp=ROOT/'verify/out/n100-axis-subdivision-pruning.json';core=load(cp)['core'];prior=load(bp);cand=load(sp)['candidate_axis_edge_indices'];sites,adj,D=build(core);cases=[prior['retained'][0],next(x for x in prior['retained'] if x['placement']==cand)];rows=[]
 for row in cases:rows.append({'placement':row['placement'],'result':run(core,row['boxes'],row['placement'],sites,adj,D,12)})
 need(not rows[1]['result']['excluded'],'candidate excluded');out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-shared-vertex-boxes/v2','verified_integer_propagation':True,'cases':rows,'candidate_retained':True,'scope':'two fixed core placements; vertex boxes are unit-disk relaxation, boundary-circle equations omitted; nonempty boxes unresolved','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,sp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS shared-vertex boxes',[(r['placement'],r['result']['excluded'],r['result']['fixed'],r['result']['contractions']) for r in rows])
if __name__=='__main__':main()
