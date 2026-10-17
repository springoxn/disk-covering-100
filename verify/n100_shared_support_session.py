"""Shared lens audit for constrained and free-intercept supports.
No caller-supplied contexts. Every public call checks the current bound files.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys
import n100_arc_budget_interfaces as A
import n100_proof_interface_variants as V
from n100_proof_interfaces import exact_data,require
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot_valid(expected,actual):return expected==actual
class SupportSession:
 def __init__(self):
  files=['verify/out/n100-arc-lens-support.json','verify/out/n100-arc-lens-free-intercept.json','verify/out/n100-arc-cap-rational-support.json','verify/n100_arc_lens_support.py','verify/n100_arc_lens_free_intercept.py','verify/n100_arc_cap_rational_support.py','verify/n100_arc_budget_interfaces.py','verify/n100_proof_interface_variants.py','verify/n100_proof_interfaces.py','verify/n100_shared_support_session.py'];self._bindings={p:sha(R/p) for p in files}
  for module in tuple(sys.modules.values()):
   raw=getattr(module,'__file__',None)
   if raw:
    path=Path(raw).resolve()
    if path.suffix=='.py' and path.is_relative_to(R):self._bindings[path.relative_to(R).as_posix()]=sha(path)
  lens=json.loads((R/files[0]).read_text(encoding='utf-8'));free=json.loads((R/files[1]).read_text(encoding='utf-8'));cap=json.loads((R/files[2]).read_text(encoding='utf-8'));require(lens['script_sha256']==self._bindings[files[3]] and free['script_sha256']==self._bindings[files[4]] and cap['script_sha256']==self._bindings[files[5]],'support source binding');require(lens['input_sha256']==self._bindings[files[2]] and free['input_sha256']==self._bindings[files[0]],'support input chain');audit=A.audit_lens(lens);require(F(free['radius'])==F(lens['radius'])==A.U and F(free['delta'])==F(lens['delta']),'support radius/delta');a,b=F(free['slope']),F(free['intercept']);require(a>=0,'free slope');lines=[(F(s['arc_half_upper']),F(s['lens_area_upper'])) for s in lens['steps']]+[(F(lens['maximum_half_arc_upper']),F(0))];slacks=[b-a*p-area for p,area in lines];require(all(s>=0 for s in slacks),'free support');active=[p for (p,area),slack in zip(lines,slacks) if slack==0];pl,ph=map(F,lens['pi_interval']);A.pi_check(pl,ph);require(bool(active) and (min(active)*54<=pl<=max(active)*54 if a>0 else max(active)*54>=pl),'fixed-envelope optimum');require(54*b-a*pl==F(free['k54_objective']),'free objective');self._lens=lens;self._free={'radius':A.U,'delta':F(free['delta']),'slope':a,'intercept':b,'pi':(pl,ph),'bindings':dict(self._bindings)};self._receipt={'lens_slabs_replayed':audit['slabs'],'free_support_lines':len(lines),'shared_lens_replays':1};self._assert_current()
 def _assert_current(self):require(snapshot_valid(self._bindings,{p:sha(R/p) for p in self._bindings}),'stale support session')
 def run(self,payload):
  exact_data(payload);self._assert_current();require(payload.get('radius_units')=='radius' and F(payload['radius'])==A.U,'exact U; no radius transfer');require(payload.get('configuration_id') and payload.get('semantics_id')==A.SEM,'same service semantics');m,k=payload['m'],payload['k'];require(type(m) is int and type(k) is int and 0<=k<=m<=100,'service counts');z=self._lens;pl,ph=F(314159,100000),F(314160,100000);a,delta,M=F(z['slope']),F(z['delta']),F(z['maximum_half_arc_upper']);margin=pl*(1-2*A.U+delta)**2-(m-k)*ph*A.U**2-a*(k*M-pl);free=V.free_intercept_filter(payload,self._free);require(free['status'] in ('EXCLUDED','NOT_EXCLUDED'),'free context');lens={'status':'EXCLUDED' if margin>0 else 'NOT_EXCLUDED','area_deficit_lower':str(margin)};return {'status':'EXCLUDED' if lens['status']=='EXCLUDED' or free['status']=='EXCLUDED' else 'NOT_EXCLUDED','lens':lens,'free_intercept':{'status':free['status'],'area_deficit_lower':free['area_deficit_lower']},'proof_input':dict(payload),'bindings':dict(self._bindings),'replay_receipt':dict(self._receipt),'scope':'same fixed-U service-count domain; intersection of two necessary supports; no additive deficits','global_optimality':False}
