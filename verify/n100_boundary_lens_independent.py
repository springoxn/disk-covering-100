"""Independent saved-strip and area-deficit verification, without square-root calls."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def atan(q,n):
 power=F(1,q);result=F(0)
 for j in range(n):result+=(-1)**j*power/(2*j+1);power/=q*q
 return result

def main():
 path=ROOT/'verify/out/n100-boundary-lens-threshold.json';z=json.loads(path.read_text(encoding='utf-8'));r=F(z['radius_cut']);d=F(z['delta']);s=F(z['inner_radius']);n=z['subinterval_count'];need(0<d<r<F(1,2) and s==1-2*r+d and s<=1,'geometry parameters');need(len(z['slabs'])==n,'all strips');area=F(0);S=10**20
 for i,row in enumerate(z['slabs']):
  a=F(i,n)*d;b=F(i+1,n)*d;need(F(row['a'])==a and F(row['b'])==b,'exact strip partition');small=r*r-(r-b)**2;target=s*s-(s-d+a)**2;rad=min(small,target);height=F(row['height_upper']);need(rad==F(row['chosen_square_upper']) and small==F(row['small_disk_square_upper']) and target==F(row['target_disk_square_upper']),'independent squared-height formulas');need(rad>=0 and (height/2-F(1,S))**2<=rad<(height/2)**2,'saved rational sqrt enclosure');area+=(b-a)*height
 pi=(16*atan(5,8)-4*atan(239,7),16*atan(5,7)-4*atan(239,8));need(list(map(str,pi))==z['pi_interval'],'independent pi');need(area==F(z['lens_area_upper']),'strip total');margin=pi[0]*s*s-45*pi[1]*r*r-55*area;need(margin==F(z['area_deficit_lower']) and margin>0,'strict saved deficit');need(pi[1]*r*r>area,'deficit increases with k');need(r>F(z['old_threshold']) and area<F(z['old_tangent_cap_upper_same_parameters']),'improved threshold and cap');next_r=F(z['next_radius_grid']['radius']);need(next_r-r==F(1,10**8),'adjacent saved radius grid')
 rejected=False
 try:
  row=z['slabs'][n//2];a=F(row['chosen_square_upper']);h=F(row['height_upper'])/2;need((h/2)**2>a,'understated strip accepted')
 except ValueError:rejected=True
 need(rejected,'negative understated height control')
 out=ROOT/'verify/out/n100-boundary-lens-independent.json';need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-lens-independent/v1','verified_rational_strip_replay':True,'strip_count':n,'all_squared_height_enclosures_checked':True,'pi_recurrence_agrees':True,'lens_area_upper':str(area),'area_deficit_lower':str(margin),'radius_cut':str(r),'serving_count_at_least':55,'strict_improvement_from':z['old_threshold'],'deficit_increases_in_serving_count':True,'understated_height_control_rejected':True,'analytic_dependency':'overlap of two disks decreases with center separation; slab sup bounds and area subadditivity; enlarge disks to extend exclusion to smaller radii with at least55 boundary-intersecting disks','scope':'independent arithmetic verification of saved cut, not independent full parameter search or continuous-optimality theorem; global lower bound unchanged','global_optimality':False,'minimal_polynomial_obtained':False,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent lens strips',n,'cut',r,'strict deficit',margin>0)
if __name__=='__main__':main()
