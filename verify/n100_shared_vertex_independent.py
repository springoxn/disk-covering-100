"""Independent replay of shared face-center/vertex interval propagation."""
from pathlib import Path
import json,hashlib,argparse
from n100_dart_independent_canonicalization import loops,need
from n100_axis_coupled_boxes_independent import clip,cycles
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-shared-vertex-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';sp=ROOT/'verify/out/n100-shared-vertex-boxes-v2.json';core=load(cp)['core'];prior=load(bp);z=load(sp);A=core['alpha'];fc=cycles(core['phi']);vc=cycles(core['sigma']);vo={d:i for i,row in enumerate(vc) for d in row};outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');inner=[f for f in range(len(fc)) if f!=outer];fi={f:i for i,f in enumerate(inner)};Q=z['cases'][0]['result']['boxes'][0][1] if False else 2**20;un=1154469548855829;ud=10**16
 def rad(k):return -(-((k*un*Q)**2)//ud**2)
 rows=[]
 for case in z['cases']:
  p=case['placement'];saved=case['result'];root=next(x['boxes'] for x in prior['retained'] if x['placement']==p);boxes=[b[:] for b in root]+[[-Q,Q,-Q,Q] for _ in vc];constraints=[]
  for f in inner:
   i=fi[f]
   for d in fc[f]:constraints.append((i,len(inner)+vo[d],rad(1)))
  count=0;fixed=False;fail=None
  for sw in range(12):
   changed=False
   for a,b,r2 in constraints:
    old=boxes[a];new=clip(old,boxes[b],r2);count+=1
    if new is None:fail=[a,b,r2,old,boxes[b]];break
    if new!=old:boxes[a]=new;changed=True
    old=boxes[b];new=clip(old,boxes[a],r2);count+=1
    if new is None:fail=[b,a,r2,old,boxes[a]];break
    if new!=old:boxes[b]=new;changed=True
   if fail:break
   if not changed:fixed=True;break
  need(fail is None and saved['excluded'] is False,'unexpected exclusion');need(fixed==saved['fixed'] and sw+1==saved['sweeps'] and count==saved['contractions'] and boxes==saved['boxes'],'replay equality');rows.append({'placement':p,'constraints':len(constraints),'contractions':count,'fixed':fixed,'face_vertex_incidence':sum(len(fc[f]) for f in inner)})
 need(all(r['face_vertex_incidence']==562 for r in rows),'incidence count');out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-shared-vertex-independent/v1','verified':True,'cases':rows,'all_boxes_equal':True,'face_vertex_origin_replayed':True,'scope':'two fixed core placements; unit-disk vertex relaxation only','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,sp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent shared vertices',rows)
if __name__=='__main__':main()
