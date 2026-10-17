"""Independent replay of the B=24 ear exclusion for the inner 58-disk case."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial,isqrt
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def sqrtiv(x):
 S=10**35;k=isqrt(x.numerator*S*S//x.denominator);return F(k,S),F(k+1,S)
def siniv(x):
 a=sum((F((-1)**j,factorial(2*j+1))*x**(2*j+1) for j in range(27)),F(0));e=x**55/factorial(55);return a-e,a+e
def main():
 path=ROOT/'verify/out/n100-recursive-ear-obstruction.json';z=json.loads(path.read_text(encoding='utf-8'));prior=json.loads((ROOT/'verify/out/n100-recursive-joint-area.json').read_text(encoding='utf-8'));t=F(z['normalized_inner_radius']);need(z['inner_disk_count']==58 and t==F(prior['normalized_radius']),'binding');pl=F(314159,100000);ph=F(314160,100000);Alo=F(3,4)*sqrtiv(F(3))[0];Ahi=F(3,4)*sqrtiv(F(3))[1];kap=F(461134488,10**9);x=2*t;c=F(1);ss=F(0)
 for j in range(30):ss+=c*x**(2*j+1);c*=F((2*j+1)**2,2*(j+1)*(2*j+3))
 gamma=F((2*(ss+c*x**61/(1-x*x))).numerator*10**30//(2*(ss+c*x**61/(1-x*x))).denominator+1,10**30);need(gamma==F(z['three_arc_angle_upper']),'angle replay')
 def hup(a,b):
  sl=siniv(a/2)[0];sh=siniv(b/2)[1];return sh*sqrtiv(t*t-sl*sl)[1]+(b-siniv(a)[0])/2
 for row in z['rows']:
  B=row['inner_boundary_cells'];small=gamma/3;lo=(2*pl-gamma)/(B-3);hi=(2*ph-gamma)/(B-3);hs=3*hup(small,small)+(B-3)*hup(lo,hi);base=((2*58-B-2)*Ahi+B*kap)*t*t;deficit=pl-base-hs;main_hs=F(row['boundary_function_sum_upper']);main_base=F(row['triangle_anchor_base_upper']);main_def=F(row['strict_area_deficit']);need(hs>=main_hs and base>=main_base and deficit<=main_def,'independent outward comparison');need((deficit>0)==row['ear_excluded'],'row verdict')
 need(z['no_ear_B']==[24] and z['not_excluded_B']==[25,26,27,28],'ear output');out=ROOT/'verify/out/n100-recursive-ear-obstruction-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-recursive-ear-obstruction-independent/v1','verified_independent_B24_ear_arithmetic':True,'inner_disk_count':58,'B_rows_checked':5,'excluded_ear_B':[24],'unresolved_B':[25,26,27,28],'scope':'independent rational replay of proposed ear area bound; topology ear lemma and Jensen concentration lemma remain analytic dependencies; no new global count reduction','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent ear B24 only; unresolved B25-28')
if __name__=='__main__':main()
