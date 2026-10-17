"""Six-branch current ledger after fullB33 at target radius."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 previous=ROOT/'verify/out/n100-11324-six-branch-ledger-160.json';path=ROOT/'verify/out/n100-B33-complete-167-v2.json';data=json.loads(previous.read_text(encoding='utf-8'));b33=json.loads(path.read_text(encoding='utf-8'));assert b33['status']=='PASS' and b33['full_B33_closed'] and F(b33['radius'])==F(2831,25000)
 for rel,h in b33['bindings'].items():assert sha(ROOT/rel)==h
 p31=ROOT/'verify/out/n100-B31-at-11324.json';p32=ROOT/'verify/out/n100-B32-complete-149.json';a=json.loads(p31.read_text(encoding='utf-8'));b=json.loads(p32.read_text(encoding='utf-8'));assert a['result']['status']=='PASS' and a['original_checker_all_assertions_passed'];assert b['status']=='PASS' and b['full_B32_closed'];assert F(a['radius'])==F(b['radius'])==F(2831,25000)
 guard=ROOT/'verify/n100_B33_complete_167_v2.py';control=subprocess.run([sys.executable,'-O',str(guard)],cwd=ROOT,text=True,capture_output=True);assert control.returncode!=0 and 'Assertions must remain enabled' in control.stderr
 data['schema']='n100-six-branch-progress/v4';data['closed_branches']=['B31','B32','B33'];data['pending_branches']=['B34','B35','B36plus'];data['branches']['B33']={'status':'PASS','evidence':path.relative_to(ROOT).as_posix(),'M_partition':['M<=25','M>=26'],'unique5_actual_B_neighbor_split_complete':True,'ring_metric_models':108,'minimum_reported_positive_margin':b33['minimum_reported_positive_margin']};data['all_six_closed']=False;data['global_bound_improved']=False;data['next_priority']='B34 M24..25 deficit, then B35 flagged lowM, then B>=36 envelope';data['B33_optimized_mode_rejected']={'exit_code':control.returncode,'expected_message':'Assertions must remain enabled'};data['source_bindings']={p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),previous,path,p31,p32,guard)};out=ROOT/'verify/out/n100-11324-six-branch-ledger-168.json';assert not out.exists();out.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');print('LEDGER168 PASS: closedB31/B32/B33; pendingB34/B35/tail; global0.1132301 unchanged',flush=True)
if __name__=='__main__':main()
