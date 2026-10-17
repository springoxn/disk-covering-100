"""Stage28 ledger: bind primary/independent arc-cap certificates and scope."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    p=ROOT/'verify/out/n100-arc-cap-rational-support.json';q=ROOT/'verify/out/n100-arc-cap-independent.json'
    a=json.loads(p.read_text(encoding='utf-8'));b=json.loads(q.read_text(encoding='utf-8'))
    need(a['machine_verified_geometry'] is False and b['machine_verified_geometry'] is False,'scope')
    need(a['global_optimality'] is False and b['global_optimality'] is False,'global')
    need(b['result']['segments']==2000 and len(a['steps'])==2000,'segments')
    margin=F(a['k55_area_margin_lower']);need(margin>0 and b['result']['area_margin_lower']==str(margin),'margin')
    need(F(b['result']['minimum_support_gap'])>0,'support')
    need(len(b['rejected_controls'])==3,'controls')
    bindings={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (p,q,ROOT/'verify/n100_arc_cap_rational_support.py',ROOT/'verify/n100_arc_cap_independent.py')}
    out=ROOT/'verify/out/n100-stage28-ledger.json';need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-stage28-ledger/v1','verified':True,'arc_cap_primary_and_independent_bound':True,'certified_implication':'under listed analytic dependencies, k>=55 impossible at U, hence k<=54','new_m_B_families_excluded':0,'global_optimality':False,'minimal_polynomial_obtained':False,'machine_verified_geometry':False,'bindings':bindings,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS stage28 ledger: primary/independent 2000-segment arc-cap certificates bound; k<=54 implication scoped; no global upgrade')
if __name__=='__main__':main()
