"""Recursive inner-disk Voronoi envelope, with exact service-count consequences."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt,factorial
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def root(v):
 S=10**24;n=isqrt(v.numerator*S*S//v.denominator);return F(n,S),F(n+1,S)
def main():
 U=F(1154469548855829,10**16);s=1-2*U;t=U/s;T=F(151,1000);pl=F(314159,100000);ph=F(314160,100000);need(0<t<T<F(1,6) and 20*T<pl,'angle and boundary21');
 # asin(t)<=t/sqrt(1-t^2); certify this is <T by squaring.
 coeff=F(1);series=F(0)
 for j in range(16):
  series+=coeff*t**(2*j+1);coeff*=F((2*j+1)**2,2*(j+1)*(2*j+3))
 asin_hi=series+coeff*t**33/(1-t*t)
 need(asin_hi<T,'asin series bound');f6=F(3,2)*root(F(3))[1];f5=F(5,8)*root(10+2*root(F(5))[1])[1];f6lo=F(3,2)*root(F(3))[0];f5lo=F(5,8)*root(10+2*root(F(5))[0])[0];need(f6lo>f5 and 6*f5lo>5*f6,'positive slope/intercept');h=sum((F((-1)**j,factorial(2*j+1))*(2*T)**(2*j) for j in range(6)),F(0));G=28*f6+27*f5;margin=pl*h-t*t*G;need(margin>0,'at most55 inner disks excluded');
 oldpath=ROOT/'verify/out/n100-arc-cap-mk-frontier.json';old=json.loads(oldpath.read_text(encoding='utf-8'));triples={(m,b,k) for m,b,lo,hi in old['remaining_m_B_families'] for k in range(lo,hi+1)};kept=sorted(x for x in triples if x[0]-x[2]>=56);removed=sorted(triples-set(kept));fam=sorted({(m,b) for m,b,k in kept});allfam=sorted({(m,b) for m,b,k in triples});out=ROOT/'verify/out/n100-recursive-inner-envelope.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-recursive-inner-envelope/v1','radius_upper':str(U),'inner_radius':str(s),'normalized_radius':str(t),'asin_upper':str(T),'pi_bracket':[str(pl),str(ph)],'inner_boundary_arc_count_lower':21,'excluded_inner_disk_count_upper':55,'minimum_non_circle_serving_disks':56,'normalized_area_lower':str(pl*h),'normalized_polygon_area_upper':str(t*t*G),'strict_margin':str(margin),'f6_upper':str(f6),'f5_upper':str(f5),'sinc_lower':str(h),'G_upper':str(G),'prior_triples':len(triples),'remaining_triples':kept,'removed_triples':removed,'remaining_triple_count':len(kept),'removed_triple_count':len(removed),'prior_families':len(allfam),'remaining_families':fam,'removed_families':sorted(set(allfam)-set(fam)),'analytic_dependencies':['circle-serving disks at U have center norm>=1-U, cannot enter |x|<1-2U','finite union of remaining closed disks covering open inner disk covers its closure','scale inner disk to unit disk','general Voronoi polygon envelope: sum nominal sides<=6N-6-B; area upper<=t^2*((N-6-B)*f6+(6+B)*f5)','B>=21 from half arcs<=asin(t)<T and 20T<pi','inscribed polygon area>=pi*sinc(asin(t))>pi*sinc(T)'],'scope':'universal necessary service-count cut at U, arbitrary centers via projected normalized inner coverage; analytic Voronoi reduction inherited from existing proof, not formal kernel geometry','global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [oldpath,ROOT/'proofs/n100-sharp-envelope-lowerbound.md']},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS recursive inner55 excluded; nonserving>=56','triples',len(triples),'->',len(kept),'families',len(allfam),'->',len(fam))
if __name__=='__main__':main()
