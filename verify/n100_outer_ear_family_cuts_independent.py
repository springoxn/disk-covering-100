"""Independent conservative arithmetic for original-disk ear family conditions."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_recursive_joint_area_independent import atan,rnd,sqrtiv,series,need
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'verify/out/n100-outer-ear-family-cuts.json';z=json.loads(p.read_text(encoding='utf-8'));srcp=R/'verify/out/n100-radius-local-joint-domain.json';src=json.loads(srcp.read_text(encoding='utf-8'))['layers'][0];need(z['input_sha256']==hashlib.sha256(srcp.read_bytes()).hexdigest(),'source binding');r=F(z['radius']);need(r==F(src['radius_upper']),'radius identity');pl,ph=rnd(16*atan(F(1,5),40)-4*atan(F(1,239),41),16*atan(F(1,5),41)-4*atan(F(1,239),40));Ahi=F(3,4)*sqrtiv(F(3))[1];kappa=F(461134488,10**9);x=2*r;c=F(1);v=F(0)
 for j in range(32):v+=c*x**(2*j+1);c*=F((2*j+1)**2,2*(j+1)*(2*j+3))
 gh=2*(v+c*x**65/(1-x*x));gamma=F(z['three_arc_sum_upper']);need(gh<=gamma,'independent longer asin bound')
 def H(a,b):
  sl=series(a/2)[0];sh=series(b/2)[1];need(0<sl<=sh<r,'positive H radicand');return sh*sqrtiv(r*r-sl*sl)[1]+(b-series(a)[0])/2
 families=sorted({tuple(t[:2]) for t in src['remaining_triples']});need([(a['m'],a['B']) for a in z['family_rows']]==families,'all17 families');noear=[];rows=[]
 for a in z['family_rows']:
  m,B=a['m'],a['B'];need(B*gamma<6*pl,'group monotonicity domain');small=gamma/3;lo=(2*pl-gamma)/(B-3);hi=(2*ph-gamma)/(B-3);boundary=3*H(small,small)+(B-3)*H(lo,hi);base=((2*m-B-2)*Ahi+B*kappa)*r*r;gap=pl-boundary-base;status='ear excluded by area' if gap>0 else 'not excluded';need(status==a['status'],'independent strict sign');need((F(a['strict_area_deficit'])>0)==(gap>0),'saved gap sign');
  if gap>0:noear.append((m,B))
  rows.append({'m':m,'B':B,'independent_deficit':str(gap),'status':status})
 need(noear==list(map(tuple,z['no_ear_families'])) and len(noear)==z['no_ear_count']==2,'all ear flags');out=R/'verify/out/n100-outer-ear-family-cuts-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-outer-ear-family-cuts-independent/v1','verified_all17_fixed_radius_ear_tests':True,'radius':str(r),'no_ear_families':noear,'rows':rows,'scope':'independent numeric constants and conservative rational signs; topology and concavity analytic premises inherited; flags certified at saved fixed radius only, not whole intervals','global_optimality':False,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent17 ear tests; noear',noear)
if __name__=='__main__':main()
