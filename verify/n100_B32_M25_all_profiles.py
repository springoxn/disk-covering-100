"""Diagnostic81-profile enumeration: failures recorded, never accepted as proof."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'verify'))
import n100_B32_M25_hinge_retuned as base

def main():
 original_compile=__builtins__.compile if not isinstance(__builtins__,dict) else __builtins__['compile'];import builtins
 needle="assert margin.l>0,('final',e,degrees,ps,si,F(margin.l,S))";changes=[]
 def compile_diag(source,filename,*args,**kwargs):
  if str(filename).endswith('verify_B32_M25_direct_interface_0p11323.py'):
   assert isinstance(source,str) and source.count(needle)==1;source=source.replace(needle,"pass # Diagnostic only: record every margin; this is not a proof acceptance");changes.append(hashlib.sha256(source.encode()).hexdigest())
  return original_compile(source,filename,*args,**kwargs)
 builtins.compile=compile_diag
 try:row=base.worker(F(1189,20000))
 finally:builtins.compile=original_compile
 assert len(changes)==1 and row['status']=='ARITHMETIC_PASS';result=row['result'];assert len(result['rows'])==81;bad=[x for x in result['rows'] if F(x['area_margin_lower'])<=0];assert bad;result['status']='DIAGNOSTIC_NOT_A_PROOF';row['status']='NOT_CLOSED';row['diagnostic_assertion_change']='only final positive margin assertion replaced by recording, all supports/premises retained; returned PASS deliberately relabelled';row['nonpositive_profiles']=bad;row['positive_profiles']=81-len(bad);row['full_B32_closed']=False;row['global_bound_improved']=False;row['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();out=ROOT/'verify/out/n100-B32-M25-all-profile-diagnostic-144.json';assert not out.exists();out.write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8');print('DIAGNOSTIC81 profiles;',len(bad),'nonpositive;worst',result['minimum_area_margin'],flush=True)
if __name__=='__main__':main()
