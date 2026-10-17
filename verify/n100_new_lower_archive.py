"""Archive accepted stronger lower bound with exact hash/CRC extraction check."""
from pathlib import Path
import json,hashlib,zipfile,ast
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 folder=ROOT/'runtime/lower-small-advance-143';cert=ROOT/'verify/out/n100-new-lower-bound-143.json';result=json.loads(cert.read_text(encoding='utf-8'));assert result['status']=='PASS' and result['global_bound_improved'];manifest=json.loads((folder/'transformation.json').read_text(encoding='utf-8'));files={f'package/{rel}':folder/'package'/rel for rel in manifest['copy_snapshot']};files.update({n:folder/n for n in ('transformation.json','run_new_lower.py')});files['README.md']=folder/'README.md';files['docs/result-n100-stage143-new-lower-bound.md']=ROOT/'docs/result-n100-stage143-new-lower-bound.md'
 for path in (cert,ROOT/'verify/out/n100-lower-small-advance-143.json',ROOT/'verify/out/n100-radius-dependency-audit-143.json',ROOT/'verify/out/n100-small-advance-controls-143.json'):files['verify/out/'+path.name]=path
 ast.parse((folder/'run_new_lower.py').read_text(encoding='utf-8'));archive=ROOT/'runtime/n100-new-lower-bound-1132301.zip';assert not archive.exists();snapshot={name:sha(path) for name,path in files.items()}
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,path in files.items():z.write(path,name)
  z.writestr('DELIVERY_SHA256.json',json.dumps(snapshot,indent=2)+'\n')
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and len(z.infolist())==len(snapshot)+1;assert all(hashlib.sha256(z.read(name)).hexdigest()==h for name,h in snapshot.items());names=set(z.namelist());assert not any('..' in Path(name).parts or Path(name).is_absolute() for name in names)
 out=ROOT/'verify/out/n100-new-lower-bound-archive-143.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-new-lower-archive/v1','status':'PASS','archive':archive.relative_to(ROOT).as_posix(),'sha256':sha(archive),'bytes':archive.stat().st_size,'members':len(snapshot)+1,'CRC_and_member_hashes_verified':True,'entry_syntax_verified':True,'entry_full_replay_scope':'underlying verify_all entry completed twice; delivery wrapper manifest/result assertions syntax checked, not third full execution','proof_claim':'r_D(100)>1132301/10000000','entry':'python -B -S run_new_lower.py','delivery_hashes':snapshot,'script_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8');print('PASS ARCHIVE',archive.name,'members',len(snapshot)+1,'CRC/hash all match',flush=True)
if __name__=='__main__':main()
