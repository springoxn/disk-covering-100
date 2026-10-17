"""Independent full replay of fixed-core annulus scan."""
from pathlib import Path
import json,hashlib,argparse
from n100_dart_independent_canonicalization import loops,need
ROOT=Path(__file__).resolve().parents[1];UN=1154469548855829;UD=10**16;Q=2**20
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-annulus-full-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';sp=ROOT/'verify/out/n100-boundary-annulus-full.json';core=load(cp)['core'];prior=load(bp);z=load(sp);fc=loops(core['phi']);outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');bf=sorted(f for f,row in enumerate(fc) if f!=outer and any(core['core_tags'][d][0]=='outer' for d in row));need(bf==z['boundary_faces'],'boundary faces')
 bad=[]
 for row in prior['retained']:
  empty=[]
  for f in bf:
   b=row['boxes'][f];mx=max(abs(b[0]),abs(b[1]));my=max(abs(b[2]),abs(b[3]))
   if mx*mx+my*my < (UD-UN)**2*Q*Q//UD**2:empty.append(f)
  if empty:bad.append({'placement':row['placement'],'faces':empty})
 need(bad==z['excluded'],'full replay');need(len(bad)==0,'unexpected exclusions')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-annulus-full-independent/v1','verified':True,'placements':len(prior['retained']),'boundary_faces_replayed':bf,'excluded_count':len(bad),'complete_equal':True,'candidate_retained':True,'scope':'all fixed-core stage42 placements; annulus only','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,sp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent full annulus',len(prior['retained']),'placements; no exclusions')
if __name__=='__main__':main()
