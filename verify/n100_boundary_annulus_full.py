"""Full fixed-core scan of boundary-owner annulus emptiness."""
from pathlib import Path
import json,hashlib,argparse
from n100_dart_independent_canonicalization import loops,need
ROOT=Path(__file__).resolve().parents[1];UN=1154469548855829;UD=10**16;Q=2**20
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-annulus-full.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';core=load(cp)['core'];z=load(bp);fc=loops(core['phi']);outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');bf=sorted(f for f,row in enumerate(fc) if f!=outer and any(core['core_tags'][d][0]=='outer' for d in row));threshold=UD-UN;excluded=[]
 for row in z['retained']:
  bad=[f for f in bf if max(abs(row['boxes'][f][0]),abs(row['boxes'][f][1]))**2+max(abs(row['boxes'][f][2]),abs(row['boxes'][f][3]))**2 < (threshold*Q//UD)**2]
  if bad:excluded.append({'placement':row['placement'],'faces':bad})
 need(not excluded,'unexpected full-core annulus exclusion');out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-annulus-full/v1','verified':True,'input_placements':len(z['retained']),'boundary_faces':bf,'excluded_count':len(excluded),'excluded':excluded,'retained_count':len(z['retained'])-len(excluded),'candidate_retained':True,'scope':'all fixed-core placements after stage42; annulus necessary cut only, no angular boundary equalities','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS full annulus scan',len(z['retained']),'placements;excluded',len(excluded),'boundary faces',bf)
if __name__=='__main__':main()
