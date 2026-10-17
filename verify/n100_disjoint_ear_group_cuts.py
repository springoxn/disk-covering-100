"""Bound the number of vertex-disjoint three-site ear groups uniformly below rho."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_recursive_ear_obstruction import E,H_upper,ROOT

def asinhi(x):
 c=F(1);s=F(0)
 for j in range(32):s+=c*x**(2*j+1);c*=F((2*j+1)**2,2*(j+1)*(2*j+3))
 raw=s+c*x**65/(1-x*x);D=10**30
 return F(raw.numerator*D//raw.denominator+1,D)
def main():
 p=ROOT/'verify/out/n100-radius-local-joint-domain.json';source=json.loads(p.read_text(encoding='utf-8'));layer=source['layers'][0];rho=F(layer['radius_upper']);gamma=2*asinhi(2*rho);arcmax=2*asinhi(rho);small=gamma/3;rows=[]
 for m,B in sorted({tuple(t[:2]) for t in layer['remaining_triples']}):
  E.need(B*gamma<6*E.PL,'concentrated group mean');base=((2*m-B-2)*E.AH+B*E.KAPPA)*rho*rho;tests=[];maximum=B//3
  for e in range(1,B//3+1):
   k=B-3*e;capacity=2*E.PL-e*gamma-k*arcmax
   if capacity>0:test={'groups':e,'status':'excluded by arc capacity','positive_margin':str(capacity)}
   else:
    E.need(k>0,'all arcs grouped must violate capacity');lo=(2*E.PL-e*gamma)/k;hi=(2*E.PH-e*gamma)/k
    if E.sin_at(hi/2)[1]>=rho:
     test={'groups':e,'status':'undecided Jensen domain'}
    else:
     hs=3*e*H_upper(rho,small,small)+k*H_upper(rho,lo,hi);gap=E.PL-base-hs;test={'groups':e,'status':'excluded by area' if gap>0 else 'not excluded','area_deficit':str(gap)}
   tests.append(test)
   if test['status'].startswith('excluded'):maximum=e-1;break
  rows.append({'m':m,'B':B,'maximum_disjoint_three_site_ear_groups':maximum,'tests':tests})
 out=ROOT/'verify/out/n100-disjoint-ear-group-cuts.json';E.need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-disjoint-ear-group-cuts/v1','radius_upper_inclusive':str(rho),'three_arc_sum_upper':str(gamma),'individual_arc_upper':str(arcmax),'family_rows':rows,'analytic_dependencies':['three assigned arcs belonging to each ear triple have sum<=2asin(2r)','choose e ears with pairwise disjoint triples of boundary site owners so exactly3e disjoint arcs are charged','use H_r<=H_rho; Jensen on3e group and remaining B-3e arcs; group total<=e*gamma and gamma*B<6pi','if e*gamma+(B-3e)*arcmax<2pi coverage impossible; otherwise valid-domain Jensen may certify area loss','r<=rho uniformity by same endpoint exterior bounds as stage111'],'scope':'uniform cardinality bound on vertex-disjoint ear triples, not total ears, not family exclusion; undecided Jensen domains retained','global_optimality':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS disjoint ear bounds',[(c['m'],c['B'],c['maximum_disjoint_three_site_ear_groups']) for c in rows])
if __name__=='__main__':main()
