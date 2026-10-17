"""Independently certify the final excluded disjoint-ear-group count of every family."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_recursive_joint_area_independent import atan,rnd,series,sqrtiv,need
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'verify/out/n100-disjoint-ear-group-cuts.json';z=json.loads(p.read_text(encoding='utf-8'));rho=F(z['radius_upper_inclusive']);g=F(z['three_arc_sum_upper']);arc=F(z['individual_arc_upper']);pl,ph=rnd(16*atan(F(1,5),40)-4*atan(F(1,239),41),16*atan(F(1,5),41)-4*atan(F(1,239),40));Ahi=F(3,4)*sqrtiv(F(3))[1];kap=F(461134488,10**9)
 for x,upper in [(rho,arc),(2*rho,g)]:
  c=sqrtiv(1-x*x)[0];v=x/c;need(0<v<1 and 2*atan(v,31)<=upper,'independent atan half-arc bound')
 def H(a,b):
  sl=series(a/2)[0];sh=series(b/2)[1];need(0<sl<=sh<rho,'Jensen radicand');return sh*sqrtiv(rho*rho-sl*sl)[1]+(b-series(a)[0])/2
 results=[]
 source=R/'verify/out/n100-radius-local-joint-domain.json';src=json.loads(source.read_text(encoding='utf-8'))['layers'][0];need(z['input_sha256']==hashlib.sha256(source.read_bytes()).hexdigest(),'source binding');need([(c['m'],c['B']) for c in z['family_rows']]==sorted({tuple(t[:2]) for t in src['remaining_triples']}),'all17 families')
 for c in z['family_rows']:
  m,B=c['m'],c['B'];e=c['maximum_disjoint_three_site_ear_groups']+1;need(e<=B//3,'nontrivial group limit');test=c['tests'][-1];need(test['groups']==e and test['status'].startswith('excluded'),'saved decisive test');need(g*B<6*pl,'concentrated mean');k=B-3*e;capacity=2*pl-e*g-k*arc
  if test['status']=='excluded by arc capacity':need(capacity>0,'independent capacity gap');gap=capacity
  else:
   need(k>0,'remaining arcs');lo=(2*pl-e*g)/k;hi=(2*ph-e*g)/k;hs=3*e*H(g/3,g/3)+k*H(lo,hi);base=((2*m-B-2)*Ahi+B*kap)*rho*rho;gap=pl-hs-base;need(gap>0,'independent area gap')
  results.append({'m':m,'B':B,'maximum_disjoint_ear_groups':e-1,'independent_positive_gap':str(gap),'proof':test['status']})
 out=R/'verify/out/n100-disjoint-ear-group-cuts-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-disjoint-ear-group-cuts-independent/v1','verified_decisive_exclusion_all17_families':True,'radius_upper_inclusive':str(rho),'results':results,'scope':'independent atan angle bounds and decisive excluded count per family; does not independently replay nondecisive trial counts; all limits concern disjoint three-site ear groups, not total ears; uniformity analytic via endpoint bound as stage111','global_optimality':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent decisive ear-group bounds all',len(results),'families')
if __name__=='__main__':main()
