"""Independent squared-height and arc audit of saved joint lens support."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def main():
 path=ROOT/'verify/out/n100-arc-lens-support.json';z=json.loads(path.read_text(encoding='utf-8'));r=F(z['radius']);delta=F(z['delta']);a=F(z['slope']);M=F(z['maximum_half_arc_upper']);c=r/M;s=1-2*r+delta;N=z['radial_interval_count'];n=z['slabs_per_lens'];need(0<c and c*c<=1-r*r and 0<delta<r and 0<s<=1,'geometry domain');need(len(z['steps'])==N,'radial coverage');last=F(0);strips=0
 for j,row in enumerate(z['steps']):
  lo=F(row['u_lower']);hi=F(row['u_upper']);need(lo==last and hi-lo==delta/N,'radial partition');last=hi;d=1-r+hi;cos=(1-r*r+d*d)/(2*d);p=F(row['arc_half_upper']);need(d*d<1-r*r and 0<cos<=1 and p>=0 and p*p*c*c>=1-cos*cos,'arc enclosure');depth=delta-lo;left=1-2*r+lo;need(len(row['slab_heights_upper'])==n,'slab coverage');area=F(0)
  for i,htext in enumerate(row['slab_heights_upper']):
   x=depth*i/n;y=depth*(i+1)/n;small=r*r-(r-y)**2;target=s*s-(left+x)**2;rad=min(small,target);h=F(htext);need(rad>=0 and h>0 and (h/2)**2>rad,'height square upper');area+=depth*h/n;strips+=1
  need(area==F(row['lens_area_upper']) and a*(M-p)>=area,'lens total and joint linear support')
 need(last==delta,'radial tail');pl,ph=map(F,z['pi_interval']);
 def atan(q,n):return sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(n)),F(0))
 need(pl<16*atan(5,10)-4*atan(239,9) and ph>16*atan(5,9)-4*atan(239,10),'pi bounds');margin=pl*s*s-46*ph*r*r-a*(54*M-pl);need(margin==F(z['k54_margin']) and (margin>0)==z['k54_excluded'],'saved k54 verdict');need(ph*r*r>a*M,'monotone count gain');families=json.loads((ROOT/'verify/out/n100-vonequinox-count-domain-bound.json').read_text(encoding='utf-8'))['surviving_m_B_families'];triples=[[m,b,k] for m,b in families for k in range(b,m+1) if pl*(s*s+a)-m*ph*r*r+k*(ph*r*r-a*M)<=0];need(triples==z['compatible_triples'],'all m B k arithmetic');old=json.loads((ROOT/'verify/out/n100-arc-cap-optimized.json').read_text(encoding='utf-8'))['compatible_triples'];joint=set(map(tuple,old))&set(map(tuple,triples));removed=sorted(set(map(tuple,old))-joint);need([list(t) for t in sorted(joint)]==z['old_count_domain_intersection'] and [list(t) for t in removed]==z['additional_triples_removed'],'count domain intersection');out=ROOT/'verify/out/n100-arc-lens-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-arc-lens-independent/v1','verified_saved_rational_joint_support':True,'radial_intervals_checked':N,'lens_slabs_checked':strips,'k54_excluded':margin>0,'old_triples':len(old),'joint_triples':len(joint),'additional_triples_removed':len(removed),'pi_checked_independently':True,'scope':'independent saved arithmetic using squared inequalities and separate formulas; no independent full parameter optimization or formal analytic geometry','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent arc lens','radial',N,'slabs',strips,'k54',margin>0,'removed',len(removed))
if __name__=='__main__':main()
