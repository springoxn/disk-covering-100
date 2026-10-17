"""Engineering certificate index for the current radius search."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def main():
 ledger=ROOT/'verify/out/n100-11324-six-branch-ledger-213.json';j=json.loads(ledger.read_text(encoding='utf-8'));rows=[]
 for name,data in j['branches'].items():
  ev=[]
  for k in ('evidence','B37plus_evidence','B36_obstruction','direct_term_diagnostic'):
   if k in data:
    p=ROOT/data[k].replace('\\','/');item={'field':k,'path':p.relative_to(ROOT).as_posix(),'exists':p.exists()}
    if p.exists():item['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();item['status']=json.loads(p.read_text(encoding='utf-8')).get('status')
    ev.append(item)
  rows.append({'branch':name,'status':data.get('status'),'evidence':ev})
 out=ROOT/'verify/out/n100-certificate-index-221.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-certificate-index/v1','ledger':ledger.relative_to(ROOT).as_posix(),'target_radius':j['target_radius'],'accepted_global_lower_bound':j['accepted_global_lower_bound'],'branches':rows,'all_six_closed':j['all_six_closed'],'global_bound_improved':j['global_bound_improved'],'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n');print('INDEX221 PASS',flush=True)
if __name__=='__main__':main()
