"""Ledger append: B36 obstruction branch classified as direct-term bottleneck."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 prev=ROOT/'verify/out/n100-11324-six-branch-ledger-211.json';diag=ROOT/'verify/out/n100-tail-point-branch-212.json';j=json.loads(prev.read_text(encoding='utf-8'));d=json.loads(diag.read_text(encoding='utf-8'));assert d['status']=='PASS' and d['B36_closed'] is False
 for rel,h in d['bindings'].items():assert sha(ROOT/rel)==h
 j['schema']='n100-six-branch-progress/v10';j['branches']['B36plus']['direct_term_diagnostic']=diag.relative_to(ROOT).as_posix();j['branches']['B36plus']['support_overestimation_at_obstruction']=False;j['next_priority']='Replace or tighten the direct pair/angle relaxation for B36; support-box refinement alone is mathematically insufficient';j['source_bindings'].update({p.relative_to(ROOT).as_posix():sha(p) for p in (Path(__file__),prev,diag)});out=ROOT/'verify/out/n100-11324-six-branch-ledger-213.json';assert not out.exists();out.write_text(json.dumps(j,indent=2)+'\n',encoding='utf-8');print('LEDGER213 PASS direct-term bottleneck recorded; B36 pending',flush=True)
if __name__=='__main__':main()
