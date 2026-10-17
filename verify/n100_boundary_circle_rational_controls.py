"""Exact rational controls for boundary circle contractors, not completeness proof."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
from n100_boundary_circle_propagation import circle,Q
from n100_boundary_circle_independent import circle as alternate
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def main():
 count=0
 for k in range(41):
  t=F(k,40);x=Q*(1-t*t)/(1+t*t);y=Q*2*t/(1+t*t)
  need(x*x+y*y==Q*Q,'rational circle identity')
  for sx,sy in ((1,1),(-1,1),(-1,-1),(1,-1)):
   xx,yy=sx*x,sy*y
   for pad in (0,1,17,10001):
    b=[xx.numerator//xx.denominator-pad,-(-xx.numerator//xx.denominator)+pad,yy.numerator//yy.denominator-pad,-(-yy.numerator//yy.denominator)+pad]
    a=circle(b,(sx,sy));other=alternate(b,(sx,sy));need(a==other and a is not None,'contractors equal and retain point')
    need(a[0]<=xx<=a[1] and a[2]<=yy<=a[3],'exact rational point retained');count+=1
 # Deliberate wrong quadrant and interior/exterior boxes exercise strict rejection.
 need(circle([Q,Q,0,0],(-1,1)) is None,'wrong quadrant rejected')
 need(circle([0,Q//2,0,Q//2],(1,1)) is None,'strictly interior rejected')
 need(circle([Q,Q,Q,Q],(1,1)) is None,'strictly exterior rejected')
 out=ROOT/'verify/out/n100-boundary-circle-rational-controls.json';need(not out.exists(),'overwrite')
 sources=[ROOT/'verify/n100_boundary_circle_propagation.py',ROOT/'verify/n100_boundary_circle_independent.py']
 out.write_text(json.dumps({'schema':'n100-boundary-circle-rational-controls/v1','verified':True,'exact_rational_unit_circle_points':164,'enclosing_box_cases':count,'all_exact_points_retained':True,'strict_rejection_controls':3,'arithmetic':'Fraction and integer only','scope':'controls, not a proof of global optimality or complete verification of all box inputs','bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS rational circle controls',count,'enclosures and3 rejections')
if __name__=='__main__':main()
