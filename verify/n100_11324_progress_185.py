"""Ledger after complete B34 at target radius and B35 diagnostic."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 prev=ROOT/'verify/out/n100-11324-six-branch-ledger-175.json';data=json.loads(prev.read_text(encoding='utf-8'));b34=ROOT/'verify/out/n100-B34-complete-180.json';b35=ROOT/'verify/out/n100-B35-diagnostic-184.json';c=json.loads(b34.read_text(encoding='utf-8'));d=json.loads(b35.read_text(encoding='utf-8'));assert c['status']=='PASS' and c['full_B34_closed'] and F(c['radius'])==F(2831,25000);assert d['status']=='PASS_PREMISES' and not d['B35_closed'];assert F(d['radius'])==F(2831,25000)
 for cert in (c,d):
  for rel,h in cert['bindings'].items():assert sha(ROOT/rel)==h
 data['schema']='n100-six-branch-progress/v6';data['closed_branches']=['B31','B32','B33','B34'];data['pending_branches']=['B35','B36plus'];data['branches']['B34']={'status':'PASS','evidence':b34.relative_to(ROOT).as_posix(),'M_partition':['M<=25','M>=26'],'chordless_models':23,'onechord_models':47,'minimum_reported_positive_margin':c['minimum_reported_positive_margin']};data['branches']['B35']={'status':'NOT_CLOSED','diagnostic':b35.relative_to(ROOT).as_posix(),'M24_or_less_flagged':'negative and retained','M25_restricted_margin':d['replay']['result']['branches'][3]['restricted_M25_margin'],'M26_restricted_margin':d['replay']['result']['branches'][4]['restricted_M26_margin'],'reason':'All support premises replay; flagged lowM and restricted M25/M26 rows negative. Needs separate local replacement/metric.'};data['all_six_closed']=False;data['global_bound_improved']=False;data['next_priority']='B35 M25/M26 local metric or coherent replacement, then B>=36 tail';data['source_bindings']={p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),prev,b34,b35)};out=ROOT/'verify/out/n100-11324-six-branch-ledger-185.json';assert not out.exists();out.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');print('LEDGER185 PASS B31-B34 closed; B35 flagged M25/M26 negative; tail pending',flush=True)
if __name__=='__main__':main()
