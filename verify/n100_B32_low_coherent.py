"""Replay B32 low prerequisites with exact coherent M24 replacement.
Preserves existing row, adds certified gain once, updates fan and half-angle.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,importlib.util
R=Path(__file__).resolve().parents[1];P=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323';W=P/'working';S=P/'lower_staging';sys.path[:0]=[str(R/'verify'),str(S),str(W),str(W/'lower_bounds_extension_20261004')]
import n100_B32_M24_coherent as local

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
 certificate=local.verify();gain=F(certificate['certified_normalized_gain']);assert gain==F(19,100);path=S/'refresh_B32_low_core_0p11323.py';before=path.read_bytes();text=before.decode('utf-8');needle='final24=m24+rr.sq()*q(g24[0,5]);assert final24.l>0';assert text.count(needle)==1 and text.count('F(1733,2500)')==1 and text.count('F(1733,5000)')==1;text=text.replace('F(1733,2500)','F(17331,25000)').replace('F(1733,5000)','F(17331,50000)').replace(needle,'final24=m24+rr.sq()*q(g24[0,5])+rr.sq()*q(F(19,100));assert final24.l>0');spec=importlib.util.spec_from_file_location('coherent_low_prerequisites',path);module=importlib.util.module_from_spec(spec);exec(compile(text,str(path),'exec'),module.__dict__);module.R=F(11324,100000);row=module.LOW24;expected=certificate['fixed_original_LOW24'];assert all(row[k]==expected[k] for k in ('a','lb','c','charges'));assert module.DEN==expected['denominator'];result=module.verify();assert result['status']=='PASS' and result['radius']==str(module.R) and F(result['M24_margin'])>0 and path.read_bytes()==before
 # Compare old failed M24 margin from unchanged-row independent replay.
 deficits=R/'verify/out/n100-B32-exact-deficits-141.json';old=json.loads(deficits.read_text(encoding='utf-8'));low=next(c for c in old['components'] if c['task']=='low');values=low['exact_failure_locals'][-1]['values']['final24'];new_margin=F(result['M24_margin']);delta=module.R*module.R*gain;assert F(values['lower'])+delta-F(1,10**20)<=new_margin<=F(values['upper'])+delta+F(1,10**20)
 return {'status':'PASS','radius':str(module.R),'B':32,'M_domain':'M<=25 prerequisites','M24_local_replacement_used_once':True,'M24_normalized_gain':str(gain),'new_LOW24_margin':result['M24_margin'],'original_LOW24_margin_interval':values,'local_replacement':certificate,'original_low_prerequisite_result':result,'source_adaptation':'L and L/2 consistently retuned; add exact19/100 gain once in original M24 total; all original assertions retained','adapted_source_sha256':hashlib.sha256(text.encode()).hexdigest(),'geometry_bridge':'Original isolated LOW24 face domain permits only(2,2,positive), so all5 neighbors have ordinary label; unique positive is the selected deep5. Its ring has5 distinct interior edges, each one outside triangle. C5 triangle edge counts checked; no more than2 selected edges per outside face. Existing potential correction and forced-five credit unchanged. Physical halfedge terms cancel once. Inherited complete-star theorem required.','full_B32_closed':False,'global_bound_improved':False,'bindings':{p.relative_to(R).as_posix():sha(p) for p in (Path(__file__),path,deficits,R/'verify/n100_B32_M24_coherent.py')}}
def main():
 result=verify();out=R/'verify/out/n100-B32-low-coherent-141.json';assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS B32 low prerequisites at11324;M24 repaired with single coherent gain;M24 margin',result['new_LOW24_margin'])
if __name__=='__main__':main()
