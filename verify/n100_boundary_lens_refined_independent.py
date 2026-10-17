"""Independent no-root arithmetic audit of refined saved lens strips."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(c,m):
 if not c:raise ValueError(m)
def main():
 path=ROOT/'verify/out/n100-boundary-lens-refined.json';z=json.loads(path.read_text(encoding='utf-8'));r=F(z['radius_cut']);d=F(z['delta']);s=1-2*r+d;n=z['subinterval_count'];need(0<d<r<F(1,2) and s<=1 and s==F(z['inner_radius']),'parameter domain');need(len(z['slabs'])==n,'complete partition');area=F(0)
 for i,row in enumerate(z['slabs']):
  a=d*F(i,n);b=d*F(i+1,n);need(a==F(row['a']) and b==F(row['b']),'partition');small=r*r-(r-b)**2;target=s*s-(s-d+a)**2;q=min(small,target);h=F(row['height_upper'])/2;need(q==F(row['chosen_square_upper']) and small==F(row['small_disk_square_upper']) and target==F(row['target_disk_square_upper']),'geometric squares');need(0<=q<h*h and (h-F(1,10**20))**2<=q,'rational sqrt outward enclosure');area+=2*h*(b-a)
 def atan(q,n):return sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(n)),F(0))
 pi=(16*atan(5,8)-4*atan(239,7),16*atan(5,7)-4*atan(239,8));need(list(map(str,pi))==z['pi_interval'],'independent pi');margin=pi[0]*s*s-45*pi[1]*r*r-55*area;need(area==F(z['lens_area_upper']) and margin==F(z['area_deficit_lower'])>0,'positive area deficit');need(pi[1]*r*r>area and r>F(z['prior_radius_cut']),'count monotonicity and improved cut')
 out=ROOT/'verify/out/n100-boundary-lens-refined-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-lens-refined-independent/v1','verified_saved_strip_arithmetic':True,'strip_count':n,'radius_cut':str(r),'area_deficit_lower':str(margin),'all_strips_outward_squared_checks':True,'deficit_increases_with_boundary_count':True,'scope':'saved cut independent arithmetic only; geometric lens monotonicity and area subadditivity remain analytic dependencies; no full search replay or global optimality','global_optimality':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent refined strips',n,'radius',r)
if __name__=='__main__':main()
