"""Ledger after exact B>=37 closure and unresolved B36 obstruction."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 prev=ROOT/'verify/out/n100-11324-six-branch-ledger-204.json';b35=ROOT/'verify/out/n100-B35-complete-203.json';tail=ROOT/'verify/out/n100-tail-B37plus-210-a.json';obs=ROOT/'verify/out/n100-tail-support-obstruction-206.json';j=json.loads(prev.read_text(encoding='utf-8'));a=json.loads(b35.read_text(encoding='utf-8'));t=json.loads(tail.read_text(encoding='utf-8'));o=json.loads(obs.read_text(encoding='utf-8'));assert a['full_B35_closed'] and t['status']=='PASS' and t['boundary_counts']=='37..99' and o['status']=='PASS_OBSTRUCTION_TO_OLD_RELAXATION';assert F(t['radius'])==F(2831,25000)
 for c in (a,t,o):
  for rel,h in c['bindings'].items():assert sha(ROOT/rel)==h
 j['schema']='n100-six-branch-progress/v9';j['branches']['B36plus']={'status':'NOT_CLOSED','B37plus_status':'PASS','B37plus_evidence':tail.relative_to(ROOT).as_posix(),'B36_status':'NOT_CLOSED','B36_obstruction':obs.relative_to(ROOT).as_posix(),'reason':'B>=37 exact 93257-box cover passes with L=19/2500, but B36 budget permits only L≈0.00750553 while old pair relaxation has exact point lower bound≈0.0075099921; fixed constants cannot close B36.'};j['closed_branches']=['B31','B32','B33','B34','B35'];j['pending_branches']=['B36'];j['all_six_closed']=False;j['global_bound_improved']=False;j['next_priority']='B36 synchronized tighter pair support or new scalar metric; B37plus is already closed conditionally';j['source_bindings']={p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),prev,b35,tail,obs)};out=ROOT/'verify/out/n100-11324-six-branch-ledger-211.json';assert not out.exists();out.write_text(json.dumps(j,indent=2)+'\n',encoding='utf-8');print('LEDGER211 PASS B31-B35 closed; B37plus closed; B36 pending exact obstruction',flush=True)
if __name__=='__main__':main()
