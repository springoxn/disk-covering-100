"""Refine one certified lens parameter; no floating point decisions."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_boundary_lens_threshold import lens,need,R

def main():
 src=R/'verify/out/n100-boundary-lens-threshold.json';z=json.loads(src.read_text(encoding='utf-8'));d=F(z['delta']);pi=tuple(map(F,z['pi_interval']));n=4096;scale=10**8;old=F(z['radius_cut']);lo=int(old*scale);hi=11544696
 def value(q,save=False):
  cap,slabs=lens(F(q,scale),d,n,save);r=F(q,scale);margin=pi[0]*(1-2*r+d)**2-45*pi[1]*r*r-55*cap;return margin,cap,slabs
 need(value(lo)[0]>0 and value(hi)[0]<0,'search endpoints');trace=[]
 while hi-lo>1:
  mid=(lo+hi)//2;score,cap,_=value(mid);trace.append({'radius':str(F(mid,scale)),'deficit':str(score)});
  if score>0:lo=mid
  else:hi=mid
 margin,cap,slabs=value(lo,True);r=F(lo,scale);need(r>old and margin>0 and pi[1]*r*r>cap,'improvement and count monotonicity');out=R/'verify/out/n100-boundary-lens-refined.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-lens-refined/v1','radius_cut':str(r),'delta':str(d),'inner_radius':str(1-2*r+d),'pi_interval':z['pi_interval'],'subinterval_count':n,'lens_area_upper':str(cap),'area_deficit_lower':str(margin),'prior_radius_cut':str(old),'next_fixed_parameter_radius':str(F(hi,scale)),'next_fixed_parameter_margin':str(value(hi)[0]),'trace':trace,'slabs':slabs,'scope':'fixed delta only; strict conditional k>=55 exclusion, not continuous optimum or global radius lower bound','global_optimality':False,'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS refined lens',r,'delta',d,'strips',n)
if __name__=='__main__':main()
