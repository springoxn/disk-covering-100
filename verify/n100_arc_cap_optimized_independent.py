"""Squared-rational replay of saved optimized arc-cap support and actual count domain."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def main():
 path=ROOT/'verify/out/n100-arc-cap-optimized.json';z=json.loads(path.read_text(encoding='utf-8'));r=F(z['radius']);M=F(z['maximum_half_arc_upper']);c=r/M;row=z['best_for_k54'];delta=F(row['delta']);a=F(row['slope']);need(0<c and c*c<=1-r*r,'uniform arc denominator');last=F(0);count=0
 for s in z['best_support_steps']:
  lo=F(s['u_lower']);hi=F(s['u_upper']);need(lo==last and hi>lo and hi<=delta,'contiguous partition');last=hi;d=1-r+hi;cos=(1-r*r+d*d)/(2*d);p=F(s['arc_half_upper']);cap=F(s['cap_upper']);depth=delta-lo;factor=F(4,3)-depth/(5*r);need(d*d<1-r*r and 0<cos<=1,'short arc branch');need(p>=0 and p*p*c*c>=1-cos*cos,'squared arc bound');need(factor>0 and cap>0 and cap*cap>=2*r*depth**3*factor*factor,'squared cap integral bound');need(a*(M-p)>=cap,'linear support');count+=1
 need(last==delta and count==z['segments_per_parameter'],'complete support');pl,ph=map(F,z['pi_interval']);
 def atan(q,n):return sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(n)),F(0))
 need(pl<16*atan(5,10)-4*atan(239,9) and ph>16*atan(5,9)-4*atan(239,10),'independent pi');m54=pl*(1-2*r+delta)**2-46*ph*r*r-a*(54*M-pl);m55=m54+ph*r*r-a*M;need(str(m54)==row['k54_margin'] and str(m55)==row['k55_margin'],'margin recomputation');need((m54>0)==z['k54_excluded_by_best'] and ph*r*r>a*M,'count monotonicity');front={}
 for item in z['frontier']:
  m=item['m'];front[m]=[k for k in range(m+1) if pl*((1-2*r+delta)**2+a)-m*ph*r*r+k*(ph*r*r-a*M)<=0];need(front[m]==item['allowed_k'],'all m-k intervals')
 families=json.loads((ROOT/'verify/out/n100-vonequinox-count-domain-bound.json').read_text(encoding='utf-8'))['surviving_m_B_families'];triples=[[m,b,k] for m,b in families for k in front[m] if k>=b];need(triples==z['compatible_triples'] and len(triples)==z['compatible_triple_count'],'B<=k exact domain');prior=json.loads((ROOT/'verify/out/n100-arc-cap-mk-frontier.json').read_text(encoding='utf-8'));old={(m,b,k) for m,b,lo,hi in prior['remaining_m_B_families'] for k in range(lo,hi+1)};current=set(map(tuple,triples));combined=old&current;out=ROOT/'verify/out/n100-arc-cap-optimized-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-arc-cap-optimized-independent/v1','verified_squared_rational_support':True,'verified_segments':count,'k54_excluded':m54>0,'k55_excluded':m55>0,'old_triple_count':len(old),'new_support_triple_count':len(current),'joint_triple_count':len(combined),'additional_triples_removed':len(old-combined),'removed_triples':sorted(old-combined),'scope':'independent saved support, pi and full count-domain arithmetic; not full parameter-grid optimization replay or independently formal geometry','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS optimized independent','segments',count,'k54',m54>0,'joint triples',len(combined),'removed',len(old-combined))
if __name__=='__main__':main()
