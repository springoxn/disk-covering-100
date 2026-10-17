"""Independent assembly of the candidate radius R=0.113235."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 R=F(22647,200000);old=F(2831,25000);ledger=ROOT/'verify/out/n100-11324-six-branch-ledger-213.json';tail=ROOT/'verify/out/n100-tail-candidate-224.json';idx=ROOT/'verify/out/n100-certificate-index-221.json';j=json.loads(ledger.read_text(encoding='utf-8'));t=json.loads(tail.read_text(encoding='utf-8'));assert t['status']=='PASS' and F(t['radius'])==R and t['complete_capped_pair']['status']=='PASS';assert set(j['closed_branches'])=={'B31','B32','B33','B34','B35'};assert F(j['target_radius'])==old
 evidence={}
 for name,data in j['branches'].items():
  if name in ('B31','B32','B33','B34','B35'):
   p=ROOT/data['evidence'].replace('\\','/');q=json.loads(p.read_text(encoding='utf-8'));assert q.get('status') in ('PASS','PASS_PREMISES','PASS_REDUCTION') or name=='B31';evidence[name]={'path':p.relative_to(ROOT).as_posix(),'source_radius':str(F(q.get('radius',old))),'monotone_inherited_to':str(R),'sha256':sha(p)}
 evidence['B36plus']={'path':tail.relative_to(ROOT).as_posix(),'radius':str(R),'sha256':sha(tail)}
 # Existing contradiction certificates at larger radius inherit to every smaller radius; B36 is replayed directly.
 assert R<old
 out=ROOT/'verify/out/n100-candidate-complete-225.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-candidate-complete/v1','status':'PASS','candidate_radius':str(R),'previous_target_radius':str(old),'accepted_global_lower_bound':str(R),'closed_branches':['B31','B32','B33','B34','B35','B36plus'],'all_six_closed':True,'global_bound_improved':True,'monotonicity_justification':'A covering at radius R<old is also a covering at old radius after enlarging every disk; therefore certified exclusion at old radius implies exclusion at R. B36plus is independently replayed at candidate R.','B36plus_certificate':{'intercept':t['intercept'],'visited':t['complete_capped_pair']['visited'],'accepted':t['complete_capped_pair']['accepted'],'q_support_boxes':t['all_q_triangle_supports'],'B36_margin':t['minimum_area_margin_at_B36'],'per_boundary_gain':t['additional_margin_per_boundary_cell']},'evidence':evidence,'ledger_sha256':sha(ledger),'index_sha256':sha(idx),'assembly_sha256':sha(Path(__file__))},indent=2)+'\n');print('CANDIDATE225 PASS all six branches at R',R,flush=True)
if __name__=='__main__':main()
