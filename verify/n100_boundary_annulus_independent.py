"""Independent replay of boundary-owner annulus boxes."""
from pathlib import Path
import json,hashlib,argparse,copy
from n100_dart_independent_canonicalization import loops,need
ROOT=Path(__file__).resolve().parents[1];UN=1154469548855829;UD=10**16;Q=2**20
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-annulus-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';sp=ROOT/'verify/out/n100-boundary-annulus-boxes-v2.json';core=load(cp)['core'];z=load(sp);prior=load(bp);fc=loops(core['phi']);outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');bf={f for f,row in enumerate(fc) if f!=outer and any(core['core_tags'][d][0]=='outer' for d in row)};threshold=UD-UN
 def empty(box):return max(abs(box[0]),abs(box[1]))**2+max(abs(box[2]),abs(box[3]))**2 < (threshold*Q//UD)**2
 got=[]
 for row in prior['retained']:
  if row['placement'] in [x['placement'] for x in z['cases']]:got.append({'placement':row['placement'],'empty_faces':sorted(f for f in bf if empty(row['boxes'][f]))})
 need(got==[{'placement':x['placement'],'empty_faces':x['annulus_empty_faces']} for x in z['cases']],'annulus replay');need(all(not x['empty_faces'] for x in got),'candidate/controls retained')
 need(empty([-1,1,-1,1]),'origin box must be annulus-empty')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-annulus-independent/v1','verified':True,'cases':got,'boundary_face_set_replayed':sorted(bf)==z['boundary_faces'],'integer_annulus_replay':True,'scope':'two fixed core cases and outer-owner faces only','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,sp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent boundary annulus',got)
if __name__=='__main__':main()
