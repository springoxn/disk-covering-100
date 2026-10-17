"""Independent atan bounds and integer squared-norm hierarchy replay."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def atan(x,n):return sum((F((-1)**j,2*j+1)*x**(2*j+1) for j in range(n)),F(0))
def sqrtlo(x):
 lo=0;hi=10**30;S=hi
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid*mid*x.denominator<=x.numerator*S*S:lo=mid
  else:hi=mid
 return F(lo,S)
def main():
 path=ROOT/'verify/out/n100-inner-radial-hierarchy.json';z=json.loads(path.read_text(encoding='utf-8'));U=F(z['radius_upper']);pl,ph=map(F,z['pi_bracket']);need(pl<16*atan(F(1,5),10)-4*atan(F(1,239),9) and ph>16*atan(F(1,5),9)-4*atan(F(1,239),10),'pi');f6=list(map(F,z['f6_interval']));f5=list(map(F,z['f5_interval']));need(0<f6[0]<=f6[1] and f6[0]**2<=F(27,4)<=f6[1]**2,'hexagon radical');q=[(F(64,25)*f*f-10)/2 for f in f5];need(0<q[0]<=q[1] and q[0]**2<=5<=q[1]**2,'pentagon radicals')
 for c in z['cuts']:
  s=F(c['target_radius']);t=F(c['normalized_radius']);T=F(c['angle_upper']);B=c['boundary_arcs_lower'];n=c['excluded_disk_count_upper'];need(t==U/s and F(c['center_norm_strict_upper'])==s+U,'scaling');x=t/sqrtlo(1-t*t);need(0<x<1 and atan(x,19)<T<F(1,3) and (B-1)*T<pl,'independent angle bound');term=F(1);H=F(0)
  for j in range(8):H+=term;term*=-(2*T)**2/F((2*j+2)*(2*j+3))
  coef=n-6-B;G=coef*f6[1 if coef>=0 else 0]+(6+B)*f5[1];margin=pl*H-t*t*G;need(n+1==c['minimum_centers'] and H==F(c['sinc_lower']) and G==F(c['G_upper']) and margin==F(c['strict_margin'])>0,'count envelope')
 source=ROOT/'verify/out/n100-spatial-leaf-joint.json';joint=json.loads(source.read_text(encoding='utf-8'));arc=json.loads((ROOT/'verify/out/n100-arc-center-projection.json').read_text(encoding='utf-8'));candidate=next(c for c in arc['cases'] if c['source_node'] is None);cases=[('candidate',candidate['result']['boxes'])]+[(str(c['tree_node']),c['arc_result']['boxes']) for c in joint['leaves'] if not c['excluded']];need(len(cases)==len(z['box_rows']),'all box cases');excluded=0
 for (name,boxes),saved in zip(cases,z['box_rows']):
  need(name==saved['case'],'case id');case_bad=False
  for cut,result in zip(z['cuts'],saved['cuts']):
   bound=(F(cut['target_radius'])+U)**2*2**40;poss=[];certain=[]
   for i,b in enumerate(boxes[:100]):
    xmin=0 if b[0]<=0<=b[1] else min(b[0]**2,b[1]**2);ymin=0 if b[2]<=0<=b[3] else min(b[2]**2,b[3]**2);xmax=max(b[0]**2,b[1]**2);ymax=max(b[2]**2,b[3]**2)
    if (xmin+ymin)*bound.denominator<bound.numerator:poss.append(i)
    if (xmax+ymax)*bound.denominator<bound.numerator:certain.append(i)
   bad=len(poss)<cut['minimum_centers'];need(poss==result['possible_centers'] and certain==result['certain_centers'] and bad==result['excluded'],'integer norm screening');case_bad|=bad
  need(case_bad==saved['excluded'],'case verdict');excluded+=case_bad
 need(excluded==z['excluded_box_count'],'all exclusions');out=ROOT/'verify/out/n100-inner-radial-hierarchy-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-inner-radial-hierarchy-independent/v1','verified_independent_atan_radicals_and_integer_norms':True,'cuts_checked':len(z['cuts']),'box_cases_checked':len(cases),'excluded_box_count':excluded,'center_count_lowers':[c['minimum_centers'] for c in z['cuts']],'scope':'independent constants and integer norm-cardinality screening; analytic Voronoi geometry inherited, no global optimum','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent hierarchy','counts',[c['minimum_centers'] for c in z['cuts']],'cases',len(cases),'excluded',excluded)
if __name__=='__main__':main()
