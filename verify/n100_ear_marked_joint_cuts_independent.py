"""Independent conservative re-evaluation of all actual ear-count joint tests."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_recursive_joint_area_independent import rnd,atan,series,sqrtiv,need
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'verify/out/n100-ear-marked-joint-cuts.json';z=json.loads(p.read_text(encoding='utf-8'));ap=R/'verify/out/n100-disjoint-ear-group-cuts.json';angles=json.loads(ap.read_text(encoding='utf-8'));priorp=R/'verify/out/n100-total-ear-face-cuts.json';prior=json.loads(priorp.read_text(encoding='utf-8'));need(z['input_sha256']==hashlib.sha256(priorp.read_bytes()).hexdigest(),'binding');r=F(z['radius_upper_inclusive']);g=F(angles['three_arc_sum_upper']);arc=F(angles['individual_arc_upper']);pl,ph=rnd(16*atan(F(1,5),40)-4*atan(F(1,239),41),16*atan(F(1,5),41)-4*atan(F(1,239),40));A=F(3,4)*sqrtiv(F(3))[1];G1=sqrtiv((207+33*sqrtiv(F(33))[1])/128)[1];G2=sqrtiv(9+6*sqrtiv(F(3))[1])[1]/2
 def H(a,b):
  sl=series(a/2)[0];sh=series(b/2)[1];need(0<sl<=sh<r,'root domain');return sh*sqrtiv(r*r-sl*sl)[1]+(b-series(a)[0])/2
 reports=[];checked=0
 need(len(z['family_rows'])==len(prior['family_rows'])==17,'all families')
 for c,pc in zip(z['family_rows'],prior['family_rows']):
  m,B=c['m'],c['B'];need((m,B,c['prior_ear_upper'])==(pc['m'],pc['B'],pc['maximum_total_ear_faces']),'prior limits');need([t['ear_count'] for t in c['tests']]==list(range(c['prior_ear_upper']+1)),'all ear counts');kept=[]
  for test in c['tests']:
   e=test['ear_count'];q=(e-1)//2 if B%4==2 and e==B//2 else (e+1)//2;need(q==test['guaranteed_disjoint_groups'],'packing lower');k=B-3*q;cap=2*pl-q*g-k*arc;checked+=1
   if test['status']=='excluded by arc capacity':need(cap>0,'capacity exclusion');continue
   need(cap<=0 and k>0,'Jensen branch');lo=(2*pl-q*g)/k;hi=(2*ph-q*g)/k
   if test['status']=='undecided domain':kept.append(e);continue
   hs=(3*q*H(g/3,g/3) if q else 0)+k*H(lo,hi);base=((2*m-2*B-2+e)*A+(B-2*e)*G1+e*G2)*r*r;gap=pl-base-hs;need((gap>0)==test['status'].startswith('excluded'),'independent deficit sign')
   if gap<=0:kept.append(e)
  need(kept==c['remaining_ear_counts'],'all ear count results');reports.append({'m':m,'B':B,'prior_ear_upper':c['prior_ear_upper'],'remaining_ear_counts':kept})
 out=R/'verify/out/n100-ear-marked-joint-cuts-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-ear-marked-joint-cuts-independent/v1','verified_all_ear_count_signs':True,'ear_count_cases_checked':checked,'family_rows':reports,'scope':'independent interval arithmetic all saved ear-count tests; prior angle/packing geometry inherited from separately audited certificates; not geometric map feasibility or family exclusion','global_optimality':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent marked-ear joint all',checked,'ear counts; improved',[(r['m'],r['B'],max(r['remaining_ear_counts'],default=-1)) for r in reports if max(r['remaining_ear_counts'],default=-1)<r['prior_ear_upper']])
if __name__=='__main__':main()
