"""Six-branch ledger after completeB35; B>=36 explicitly pending."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 previous=ROOT/'verify/out/n100-11324-six-branch-ledger-185.json';proof=ROOT/'verify/out/n100-B35-complete-203.json';j=json.loads(previous.read_text(encoding='utf-8'));b=json.loads(proof.read_text(encoding='utf-8'));assert b['status']=='PASS' and b['full_B35_closed'] and F(b['radius'])==F(2831,25000)
 for rel,h in b['bindings'].items():assert sha(ROOT/rel)==h
 j['schema']='n100-six-branch-progress/v8';j['closed_branches']=['B31','B32','B33','B34','B35'];j['pending_branches']=['B36plus'];j['branches']['B35']={'status':'PASS','evidence':proof.relative_to(ROOT).as_posix(),'M_partition':b['M_partition'],'independent_lowM_margin_min':b['independent_lowM_margin_min'],'high_models':16};j['all_six_closed']=False;j['global_bound_improved']=False;j['next_priority']='B>=36 capped pair same-radius support; keep full support coverage and positive total/B slope margins';j['source_bindings']={p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),previous,proof)};out=ROOT/'verify/out/n100-11324-six-branch-ledger-204.json';assert not out.exists();out.write_text(json.dumps(j,indent=2)+'\n',encoding='utf-8');print('LEDGER204 PASS B31-B35closed; tailpending; global0.1132301 unchanged',flush=True)
if __name__=='__main__':main()
