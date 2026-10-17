"""Optimize exact arc-cap support slopes; assess k54 at the global upper radius."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_arc_cap_rational_support import ROOT,need,sqrt_bounds,cap_upper

def main():
 src=ROOT/'verify/out/n100-arc-cap-rational-support.json';old=json.loads(src.read_text(encoding='utf-8'));r=F(old['radius']);c=sqrt_bounds(1-r*r)[0];M=r/c;pl=F(314159,100000);ph=F(314160,100000);N=1000;rows=[];best=None
 for j in range(10,51):
  delta=F(j,1000);steps=[];slope=F(0)
  for i in range(N):
   lo=delta*i/N;hi=delta*(i+1)/N;d=1-r+hi;co=(1-r*r+d*d)/(2*d);need(d*d<1-r*r and 0<co<=1,'monotonic branch');p=sqrt_bounds(1-co*co)[1]/c;cap=cap_upper(r,delta-lo);need(p<M,'positive arc slack');slope=max(slope,cap/(M-p));steps.append({'u_lower':str(lo),'u_upper':str(hi),'arc_half_upper':str(p),'cap_upper':str(cap)})
  # Fixed rational slope rounded upward, keeping certificates compact.
  den=10**12;slope=F(-((-slope.numerator*den)//slope.denominator),den);m54=pl*(1-2*r+delta)**2-46*ph*r*r-slope*(54*M-pl);m55=m54+ph*r*r-slope*M;row={'delta':str(delta),'slope':str(slope),'k54_margin':str(m54),'k55_margin':str(m55)};rows.append(row)
  if best is None or m54>best[0]:best=(m54,row,steps)
 margin,row,steps=best;need(all(F(row['slope'])*(M-F(s['arc_half_upper']))>=F(s['cap_upper']) for s in steps),'all optimal supports');families=json.loads((ROOT/'verify/out/n100-vonequinox-count-domain-bound.json').read_text(encoding='utf-8'))['surviving_m_B_families'];front=[];triples=[]
 for m in range(76,101):
  accepted=[k for k in range(m+1) if pl*(1-2*r+F(row['delta']))**2-(m-k)*ph*r*r-F(row['slope'])*(k*M-pl)<=0];front.append({'m':m,'allowed_k':accepted})
 for m,b in families:
  triples.extend([m,b,k] for k in front[m-76]['allowed_k'] if k>=b)
 out=ROOT/'verify/out/n100-arc-cap-optimized.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-arc-cap-optimized/v1','radius':str(r),'maximum_half_arc_upper':str(M),'pi_interval':[str(pl),str(ph)],'segments_per_parameter':N,'parameter_grid':rows,'best_for_k54':row,'best_support_steps':steps,'k54_excluded_by_best':margin>0,'frontier':front,'compatible_triples':triples,'compatible_triple_count':len(triples),'family_count':len(families),'scope':'best on finite delta grid with rational safe slopes; not continuous optimality or feasible coverings; arbitrary-center geometry inherits prior analytic reduction','global_optimality':False,'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS optimized supports','best delta',row['delta'],'slope',row['slope'],'k54 excluded',margin>0,'triples',len(triples),flush=True)
if __name__=='__main__':main()
