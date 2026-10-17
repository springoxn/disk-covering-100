"""Independent atan/square arithmetic replay of recursive inner-envelope count cut."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def atan(x,n):return sum((F((-1)**j,2*j+1)*x**(2*j+1) for j in range(n)),F(0))
def audit(z):
 U=F(z['radius_upper']);s=F(z['inner_radius']);t=F(z['normalized_radius']);T=F(z['asin_upper']);pl,ph=map(F,z['pi_bracket']);need(s==1-2*U>0 and t==U/s,'scaling');need(pl<16*atan(F(1,5),10)-4*atan(F(1,239),9) and ph>16*atan(F(1,5),9)-4*atan(F(1,239),10),'independent pi')
 # Binary lower sqrt; asin(t)=atan(t/sqrt(1-t²)); monotonic atan.
 S=10**30;v=1-t*t;lo=0;hi=S
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid*mid*v.denominator<=v.numerator*S*S:lo=mid
  else:hi=mid
 c=F(lo,S);need(0<c and c*c<=v<(c+F(1,S))**2,'sqrt enclosure');x=t/c;need(0<x<1 and atan(x,17)<T and 20*T<pl,'independent atan angle and boundary21');f6=F(z['f6_upper']);f5=F(z['f5_upper']);need(f6>0 and f6*f6>=F(27,4),'f6 radical');q=(F(64,25)*f5*f5-10)/2;need(f5>0 and q>0 and q*q>=5,'f5 nested radical');need(F(2598,1000)**2<F(27,4)<F(2599,1000)**2,'f6 coarse bounds');a=(F(64,25)*F(2377,1000)**2-10)/2;b=(F(64,25)*F(2378,1000)**2-10)/2;need(0<a<b and a*a<5<b*b,'f5 coarse bounds');need(F(2598,1000)>F(2378,1000) and 6*F(2377,1000)>5*F(2599,1000),'secant slope and intercept positive')
 term=F(1);h=F(0)
 for j in range(6):
  h+=term;term*=-(2*T)**2/F((2*j+2)*(2*j+3))
 G=28*f6+27*f5;gap=pl*h-t*t*G;need(h==F(z['sinc_lower']) and G==F(z['G_upper']) and gap==F(z['strict_margin'])>0,'independent envelope deficit');need(z['inner_boundary_arc_count_lower']==21 and z['excluded_inner_disk_count_upper']==55 and z['minimum_non_circle_serving_disks']==56,'count theorem label');return gap

def main():
 path=ROOT/'verify/out/n100-recursive-inner-envelope.json';z=json.loads(path.read_text(encoding='utf-8'));gap=audit(z);oldpath=ROOT/'verify/out/n100-arc-cap-mk-frontier.json';old=json.loads(oldpath.read_text(encoding='utf-8'));oldT={(m,b,k) for m,b,lo,hi in old['remaining_m_B_families'] for k in range(lo,hi+1)};newT=sorted((m,b,k) for m,b,k in oldT if k<=m-56);need(newT==list(map(tuple,z['remaining_triples'])),'all retained triples');removed=sorted(oldT-set(newT));need(removed==list(map(tuple,z['removed_triples'])),'all removed triples');oldF={(m,b) for m,b,k in oldT};newF={(m,b) for m,b,k in newT};need(sorted(newF)==list(map(tuple,z['remaining_families'])) and sorted(oldF-newF)==list(map(tuple,z['removed_families'])),'family reduction');bad=[]
 for key,value in [('minimum_non_circle_serving_disks',57),('strict_margin','1'),('asin_upper','3/20')]:
  q=copy.deepcopy(z);q[key]=value
  try:audit(q)
  except ValueError:bad.append(key)
  else:raise ValueError('corruption accepted')
 out=ROOT/'verify/out/n100-recursive-inner-envelope-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-recursive-inner-envelope-independent/v1','verified_independent_atan_radicals_and_domain':True,'minimum_non_circle_serving_disks':56,'prior_triples':len(oldT),'remaining_triples':len(newT),'removed_triples':len(removed),'prior_families':len(oldF),'remaining_families':len(newF),'removed_families':len(oldF-newF),'strict_margin':str(gap),'rejected_controls':bad,'scope':'independent arithmetic/domain replay; universal Voronoi polygon, arc and closure lemmas remain explicitly analytic, inherited from existing reviewed proof','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent recursive envelope; nonserving56','triples',len(oldT),'->',len(newT),'families',len(oldF),'->',len(newF),'controls',len(bad))
if __name__=='__main__':main()
