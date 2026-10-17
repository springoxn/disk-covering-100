"""Write the candidate-radius six-branch ledger after certificate 225."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 cert=ROOT/'verify/out/n100-candidate-complete-225.json';j=json.loads(cert.read_text(encoding='utf-8'));assert j['status']=='PASS' and j['all_six_closed'];out=ROOT/'verify/out/n100-six-branch-ledger-226.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-six-branch-ledger/v11','target_radius':j['candidate_radius'],'accepted_global_lower_bound':j['accepted_global_lower_bound'],'closed_branches':j['closed_branches'],'pending_branches':[],'all_six_closed':True,'global_bound_improved':True,'certificate':'verify/out/n100-candidate-complete-225.json','certificate_sha256':sha(cert),'scope':'Candidate radius only; original R=0.11324 remains unproved because its B36 direct obstruction persists.','next_priority':'Bisection above 0.113235 using the same full B36 replay and scalar budget audit.'},indent=2)+'\n');print('LEDGER226 PASS accepted candidate',j['candidate_radius'],flush=True)
if __name__=='__main__':main()
