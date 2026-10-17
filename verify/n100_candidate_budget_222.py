"""Exact scalar budget certificate for candidate R=0.113237."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W/'lower_bounds_extension_20261004')];import verify_extension as v
def main():
 R=F(113237,10**6);L=F(75097,10**7);mu=F(92531,10**7);K=F(973,3125);A=F(129903810568,10**11);margin=(1-mu)*v.PL-((198-36)*A+36*K)*R*R-36*L;gain=(A-K)*R*R-L;assert margin>0 and gain>0;out=ROOT/'verify/out/n100-candidate-budget-222.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-candidate-budget/v1','status':'PASS','radius':str(R),'intercept':str(L),'slope':str(mu),'marked_constant':str(K),'B36_margin':str(margin),'per_boundary_gain':str(gain),'scope':'Scalar budget only; full pair-domain and other-branch replays remain required.','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n');print('BUDGET222 PASS',float(margin),flush=True)
if __name__=='__main__':main()
