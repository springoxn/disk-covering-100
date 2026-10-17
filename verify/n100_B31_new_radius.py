"""Explicit same-radius B31 arithmetic replay using fixed dimensionless rows.
Only proposal radius metadata is adapted; every coefficient remains identical.
Geometric proof transfer is recorded separately from exact source replay.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,copy
R=Path(__file__).resolve().parents[1];W=R/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'lower_bounds_extension_20261004')]
import verify_B31_global_low_degree_0p11323 as B

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 target=F(11324,100000);proposal=(W/'B31_global_low_degree_0p11323_proposals.json').resolve();original=Path.read_text;before=proposal.read_bytes();old=json.loads(before);new=copy.deepcopy(old);new['radius']=str(target);assert new['rows']==old['rows'];B.R=target
 def read(self,*a,**kw):
  return json.dumps(new) if self.resolve()==proposal else original(self,*a,**kw)
 Path.read_text=read
 try:result=B.verify()
 finally:Path.read_text=original
 assert result['status']=='PASS' and F(result['radius'])==target and proposal.read_bytes()==before;first=R/'verify/out/n100-lower-radius-bottleneck-firstpass.json';z=json.loads(first.read_text(encoding='utf-8'));independent=next(row for row in z['radius_samples'] if F(row['radius'])==target);assert len(result['branches'])==2
 for a,b in zip(result['branches'],independent['B31_fixed_rows']):assert a['M_endpoint']==b['M_endpoint'] and a['area_margin']==b['area_margin_interval'][0] and a['shifted_ear_upper']==b['shifted_ear_upper'] and a['bad_q1_upper']==b['bad_q1_upper']
 out=R/'verify/out/n100-B31-at-11324.json';assert not out.exists();files=[Path(__file__),proposal,W/'verify_B31_global_low_degree_0p11323.py',first];out.write_text(json.dumps({'schema':'n100-B31-new-radius/v1','radius':str(target),'B':31,'original_checker_all_assertions_passed':True,'proposal_change':'radius metadata only; fixed dimensionless rows/charges/potentials byte-value equal','source_release_unchanged':True,'independent_final_margin_and_ear_bad_recomputation_matches':True,'result':result,'geometric_transfer_obligations':['same-radius whole-cover normalization then rebuild diagram','unconditional full-star degree-loss inequality and current budget comparison','whole-disk /6 and induced-core /5 isoperimetry','same full-face labels, signed edge cancellation and single budget use','closed endpoint finite-type continuity argument'],'scope':'full B31 numeric checker at11324 with its written geometric skeleton; no statement about B32..B35 or tail','global_lower_bound_improved':False,'bindings':{p.relative_to(R).as_posix():sha(p) for p in files},'script_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8');print('PASS B31 at11324;40 face32 vertex supports;full numeric obligations;minimum area margin',result['minimum_area_margin'])
if __name__=='__main__':main()
